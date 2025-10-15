import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv
import google.generativeai as genai


# Load environment variables
load_dotenv()   # Load .env file
genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) # Configure Gemini API key

# --- Configuration ---
API_BASE = "http://127.0.0.1:5000/api/v1"


st.set_page_config(page_title="FinanceAI Advisor", layout="wide")

# --- Header ---
st.title("💰 FinanceAI-Advisor Dashboard")
st.markdown("Smart personal finance management powered by your Flask backend.")

# --- Sidebar Navigation ---
page = st.sidebar.radio("📂 Navigation", ["Dashboard", "Add Transaction", "delete_transaction","Sort Transactions","Visualize Transactions","AI Insights", "Export Data"])

# --- Utility function ---
def get_transactions():
    res = requests.get(f"{API_BASE}/transactions")
    if res.status_code == 200 and res.json()["success"]:
        return pd.DataFrame(res.json()["data"])
    else:
        st.error("Failed to load transactions")
        return pd.DataFrame()

# --- Dashboard Page ---
if page == "Dashboard":
    st.header("📊 Financial Overview")

    df = get_transactions()
    if not df.empty:
        st.dataframe(df, use_container_width=True)

        # Get summary
        summary_res = requests.get(f"{API_BASE}/transactions/summary").json()
        summary = summary_res.get("data", {})

        # Summary stats
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Income", f"₹{summary.get('total_income', 0):,.2f}")
        col2.metric("Total Expenses", f"₹{summary.get('total_expenses', 0):,.2f}")
        col3.metric("Net Balance", f"₹{summary.get('net_balance', 0):,.2f}")

        # Category chart
        if "categories" in summary and summary["categories"]:
            cat_df = pd.DataFrame([
                {"Category": k, "Total": v["total_amount"]}
                for k, v in summary["categories"].items()
            ])
            fig = px.bar(cat_df, x="Category", y="Total", title="Spending by Category", color="Category")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No transactions found. Add one from the sidebar!")

# --- Add Transaction Page ---
elif page == "Add Transaction":
    st.header("➕ Add a New Transaction")
    with st.form("transaction_form"):
        amount = st.number_input("Amount", step=0.01)
        category = st.text_input("Category")
        description = st.text_area("Description")
        transaction_type = st.selectbox("Type", ["income", "expense", "investment", "transfer"])
        tags = st.text_input("Tags (comma separated)")
        submitted = st.form_submit_button("Save Transaction")

        if submitted:
            payload = {
                "amount": amount,
                "category": category,
                "description": description,
                "transaction_type": transaction_type,
                "tags": [t.strip() for t in tags.split(",")] if tags else []
            }
            res = requests.post(f"{API_BASE}/transactions", json=payload)
            if res.status_code == 201:
                st.success("✅ Transaction added successfully!")
            else:
                st.error(f"Failed: {res.json().get('error')}")
elif page == "delete_transaction":
    st.header("🗑️ Delete a Transaction")
    df = get_transactions()
    if not df.empty:
        transaction_ids = df['id'].tolist()
        transaction_id = st.selectbox("Select Transaction ID to Delete", transaction_ids)
        if st.button("Delete Transaction"):
            res = requests.delete(f"{API_BASE}/transactions/{transaction_id}")
            if res.status_code == 200:
                st.success("✅ Transaction deleted successfully!")
            else:
                st.error(f"Failed: {res.json().get('error')}")
    else:
        st.info("No transactions available to delete.")
elif page == "Update Transaction":
    st.header("✏️ Update a Transaction")
    df = get_transactions()
    if not df.empty:
        transaction_ids = df['id'].tolist()
        transaction_id = st.selectbox("Select Transaction ID to Update", transaction_ids)
        transaction = df[df['id'] == transaction_id].iloc[0]

        with st.form("update_form"):
            amount = st.number_input("Amount", value=transaction['amount'], step=0.01)
            category = st.text_input("Category", value=transaction['category'])
            description = st.text_area("Description", value=transaction['description'])
            transaction_type = st.selectbox("Type", ["income", "expense", "investment", "transfer"], index=["income", "expense", "investment", "transfer"].index(transaction['transaction_type']))
            tags = st.text_input("Tags (comma separated)", value=", ".join(transaction.get('tags', [])))
            submitted = st.form_submit_button("Update Transaction")

            if submitted:
                payload = {
                    "amount": amount,
                    "category": category,
                    "description": description,
                    "transaction_type": transaction_type,
                    "tags": [t.strip() for t in tags.split(",")] if tags else []
                }
                res = requests.put(f"{API_BASE}/transactions/{transaction_id}", json=payload)
                if res.status_code == 200:
                    st.success("✅ Transaction updated successfully!")
                else:
                    st.error(f"Failed: {res.json().get('error')}")
    else:
        st.info("No transactions available to update.")
elif page == "View Transaction":
    st.header("🔍 View Transaction Details")
    df = get_transactions()
    if not df.empty:
        transaction_ids = df['id'].tolist()
        transaction_id = st.selectbox("Select Transaction ID to View", transaction_ids)
        transaction = df[df['id'] == transaction_id].iloc[0]
        st.json(transaction.to_dict())
    else:
        st.info("No transactions available to view.")
elif page == "Search Transactions":
    st.header("🔎 Search Transactions")
    df = get_transactions()
    if not df.empty:
        search_term = st.text_input("Enter search term (category, description, tags)")
        if search_term:
            filtered_df = df[
                df['category'].str.contains(search_term, case=False) |
                df['description'].str.contains(search_term, case=False) |
                df['tags'].apply(lambda tags: any(search_term.lower() in tag.lower() for tag in tags))
            ]
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.info("Please enter a search term to filter transactions.")
    else:
        st.info("No transactions available to search.")
elif page == "Filter Transactions":
    st.header("⚙️ Filter Transactions")
    df = get_transactions()
    if not df.empty:
        transaction_types = df['transaction_type'].unique().tolist()
        selected_types = st.multiselect("Select Transaction Types", transaction_types, default=transaction_types)
        if selected_types:
            filtered_df = df[df['transaction_type'].isin(selected_types)]
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.info("Please select at least one transaction type to filter.")
    else:
        st.info("No transactions available to filter.")
elif page == "Sort Transactions":
    st.header("↕️ Sort Transactions")
    df = get_transactions()
    if not df.empty:
        sort_by = st.selectbox("Sort By", ["amount", "date", "category", "transaction_type"])
        ascending = st.checkbox("Ascending Order", value=True)
        sorted_df = df.sort_values(by=sort_by, ascending=ascending)
        st.dataframe(sorted_df, use_container_width=True)
    else:
        st.info("No transactions available to sort.")
elif page == "Visualize Transactions":
    st.header("📈 Visualize Transactions")
    df = get_transactions()
    if not df.empty:
        chart_type = st.selectbox("Chart Type", ["Bar Chart", "Pie Chart", "Line Chart"])
        if chart_type == "Bar Chart":
            fig = px.bar(df, x="category", y="amount", color="transaction_type", title="Transactions by Category")
        elif chart_type == "Pie Chart":
            fig = px.pie(df, names="category", values="amount", title="Transactions Distribution by Category")
        else:  # Line Chart
            df['date'] = pd.to_datetime(df['date'])
            fig = px.line(df, x="date", y="amount", color="transaction_type", title="Transactions Over Time")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No transactions available to visualize.")
# --- AI Insights Page ---
elif page == "AI Insights":
    st.header("🧠 AI Financial Insights (Google Gemini)")
    summary_res = requests.get(f"{API_BASE}/transactions/summary").json()
    summary = summary_res.get("data", {})

    st.subheader("Current Summary")
    st.json(summary)

    user_query = st.text_input("Ask a question about your finances:")

    if st.button("Generate AI Insights"):
        if user_query.strip():
            with st.spinner("Thinking..."):
                model = genai.GenerativeModel("gemini-2.5-flash")
                # Crafting a detailed prompt for better context in a multi line format
                
                prompt = f"You are a witty and fun financial advisor dealing with rupees and have good knowledge of financial matters especially in the indian context. You are being used in a Financial Insights application called FinanceAI. Provide quick crisp, brief and actionable insights based on the data: {summary}, answer: {user_query}"
                response = model.generate_content(prompt)
                st.markdown("### 💬 Gemini Response")
                st.write(response.text)
        else:
            st.warning("Please enter a question first.")


# --- Export Page ---
elif page == "Export Data":
    st.header("📤 Export Transactions")
    st.markdown("Export your data as CSV or PDF directly from the backend.")

    col1, col2 = st.columns(2)
    if col1.button("⬇️ Download CSV"):
        res = requests.get(f"{API_BASE}/transactions/export?format=csv")
        if res.ok:
            st.download_button(
                label="Save CSV File",
                data=res.content,
                file_name="transactions.csv",
                mime="text/csv"
            )
    if col2.button("⬇️ Download PDF"):
        res = requests.get(f"{API_BASE}/transactions/export?format=pdf")
        if res.ok:
            st.download_button(
                label="Save PDF File",
                data=res.content,
                file_name="transactions.pdf",
                mime="application/pdf"
            )
