import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from dotenv import load_dotenv
import google.generativeai as genai
from datetime import datetime, timedelta
import time

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Configuration ---
API_BASE = "http://127.0.0.1:5000/api/v1"

# --- Page Configuration ---
st.set_page_config(
    page_title="MoneyMind AI",
    page_icon="assets/icon.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/sumegh26/FinanceAI-Advisor',
        'Report a bug': "https://github.com/sumegh26/FinanceAI-Advisor/issues",
        'About': "MoneyMind AI - Your AI-Powered Personal Finance Manager"
    }
)

# --- Custom CSS for Enhanced Styling ---
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #1E2530;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #6C757D;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .ai-highlight {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .feature-card {
        border: 1px solid #E9ECEF;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: transform 0.2s;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .sidebar-section {
        background: #F8F9FA;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# --- Utility Functions ---
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_transactions():
    """Fetch transactions from the API with caching"""
    try:
        res = requests.get(f"{API_BASE}/transactions", timeout=10)
        if res.status_code == 200 and res.json()["success"]:
            return pd.DataFrame(res.json()["data"])
        else:
            st.error("❌ Failed to load transactions from backend")
            return pd.DataFrame()
    except requests.RequestException as e:
        st.error(f"❌ Connection error: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=300)
def get_summary():
    """Fetch financial summary with caching"""
    try:
        res = requests.get(f"{API_BASE}/transactions/summary", timeout=10)
        if res.status_code == 200:
            return res.json().get("data", {})
        return {}
    except requests.RequestException:
        return {}

def generate_ai_insights(user_query, summary_data):
    """Generate AI insights using Gemini"""
    try:
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        prompt = f"""
        You are FinanceAI, an expert AI financial advisor with deep knowledge of Indian financial markets and practices. 
        You're integrated into a modern fintech application called FinanceAI-Advisor.
        
        Context: You're helping users understand their personal finances better.
        Data: {summary_data}
        User Question: {user_query}
        
        Guidelines:
        - Be conversational but professional
        - Use Indian Rupee (₹) context
        - Provide actionable, specific advice
        - Include relevant financial tips or insights
        - Keep responses concise but comprehensive
        - Use emojis appropriately for engagement
        
        Provide your financial analysis and recommendations:
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ AI service temporarily unavailable: {str(e)}"

# --- Header Section ---
st.markdown('<h1 class="main-header">🧠 MoneyMind AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Intelligent Personal Finance Management Powered by AI & Advanced Analytics</p>', unsafe_allow_html=True)
st.divider()

# --- Enhanced Sidebar Navigation ---
with st.sidebar:
    st.markdown("### 🚀 Navigation Hub")
    
    st.markdown("""
<a href="#" style="text-decoration:none">
    <div style="
        background: linear-gradient(90deg, #e6855e 0%, #ff686b 100%);
        padding:0.7rem 1.2rem;
        border-radius:1rem;
        text-align:center;
        margin-bottom:1rem;
        font-weight:600;
        font-size:1rem;
        color:#fff;
        box-shadow:0 2px 12px rgba(230, 133, 94, 0.13);
        transition:box-shadow 0.2s;
        letter-spacing:0.5px;
    ">
        <span style="font-size:1.3rem;vertical-align:middle;">🧠 💡 🎯</span>
        <span style="margin-left:0.5rem;">Smart AI Insights&nbsp;<span style='font-size:0.8rem;'>Personalized</span></span>
    </div>
</a>
""", unsafe_allow_html=True)

        
    # Main Navigation
    page = st.radio(
        "",
        [
            "🏠 AI Dashboard", 
            "💰 Transaction Manager", 
            "📈 Analytics & Insights", 
            "📤 Data Export"
        ],
        key="nav_radio"
    )
    
    # Quick Stats Sidebar
    st.markdown("---")
    st.markdown("### ⚡ Quick Status")
    
    # Get real-time summary for sidebar
    sidebar_summary = get_summary()
    if sidebar_summary:
        st.metric(
            "💰 Total Balance", 
            f"₹{sidebar_summary.get('net_balance', 0):,.0f}",
            delta=None
        )
        st.metric(
            "📊 Transactions", 
            f"{sidebar_summary.get('total_transactions', 0)}",
            delta=None
        )

# --- Main Content Based on Navigation ---

if page == "🏠 AI Dashboard":
    # === AI DASHBOARD PAGE ===
    
    # Real-time data loading
    with st.spinner('🔄 Loading your financial data...'):
        df = get_transactions()
        summary = get_summary()
    
    if df.empty:
        st.warning("📝 No transaction data available. Start by adding your first transaction!")
        st.info("💡 **Getting Started**: Use the Transaction Manager to add your income, expenses, and investments.")
    else:
        # === AI INSIGHTS SECTION ===
        st.markdown("## AI Financial Assistant")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            user_query = st.text_input(
                "💬 Ask me anything about your finances:",
                placeholder="e.g., How can I reduce my expenses? What's my spending pattern?",
                key="ai_query"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)  # Spacing
            ai_button = st.button("🚀 Get AI Insights", type="primary", use_container_width=True)
        
        if ai_button and user_query.strip():
            with st.spinner('🤖 FinanceAI is analyzing your data...'):
                ai_response = generate_ai_insights(user_query, summary)
                
                st.markdown("### 💡 AI Recommendations")
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            color: white; padding: 1.5rem; border-radius: 12px; margin: 1rem 0;">
                    <p>{ai_response}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # === KEY METRICS DASHBOARD ===
        st.divider()
        st.markdown("## 📊 Financial Overview")
        
        if summary:
            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
            
            with metric_col1:
                income_delta = "+₹5,000" if summary.get('total_income', 0) > 50000 else None
                st.metric(
                    "💰 Total Income", 
                    f"₹{summary.get('total_income', 0):,.0f}",
                    delta=income_delta,
                    delta_color="normal"
                )
            
            with metric_col2:
                expense_delta = f"-₹{abs(summary.get('total_expenses', 0) * 0.05):,.0f}" if summary.get('total_expenses', 0) > 0 else None
                st.metric(
                    "💸 Total Expenses", 
                    f"₹{summary.get('total_expenses', 0):,.0f}",
                    delta=expense_delta,
                    delta_color="inverse"
                )
            
            with metric_col3:
                net_balance = summary.get('net_balance', 0)
                balance_color = "normal" if net_balance >= 0 else "inverse"
                st.metric(
                    "💹 Net Balance", 
                    f"₹{net_balance:,.0f}",
                    delta=f"₹{abs(net_balance * 0.1):,.0f}",
                    delta_color=balance_color
                )
            
            with metric_col4:
                st.metric(
                    "📈 Transactions", 
                    f"{len(df)}",
                    delta="+12" if len(df) > 20 else "+5",
                    delta_color="normal"
                )
        
        # === INTERACTIVE CHARTS ===
        st.markdown("## 📈 Interactive Analytics")
        
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.markdown("### 🏷️ Category Breakdown")
            if "categories" in summary and summary["categories"]:
                cat_data = []
                for category, data in summary["categories"].items():
                    cat_data.append({
                        "Category": category.title(),
                        "Amount": abs(data["total_amount"]),
                        "Count": data["transaction_count"]
                    })
                
                cat_df = pd.DataFrame(cat_data)
                fig_pie = px.pie(
                    cat_df, 
                    values="Amount", 
                    names="Category",
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                fig_pie.update_layout(height=400, showlegend=True)
                st.plotly_chart(fig_pie, use_container_width=True)
        
        with chart_col2:
            st.markdown("### 📊 Transaction Types")
            if not df.empty:
                type_summary = df.groupby('transaction_type')['amount'].agg(['sum', 'count']).reset_index()
                type_summary.columns = ['Type', 'Total Amount', 'Count']
                type_summary['Type'] = type_summary['Type'].str.title()
                
                fig_bar = px.bar(
                    type_summary,
                    x='Type',
                    y='Total Amount',
                    color='Type',
                    text='Count',
                    color_discrete_sequence=['#667eea', '#764ba2', '#f093fb', '#f5576c']
                )
                fig_bar.update_traces(texttemplate='%{text} txns', textposition='outside')
                fig_bar.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig_bar, use_container_width=True)
        
        # === RECENT TRANSACTIONS ===
        st.markdown("## 📋 Recent Transactions")
        if not df.empty:
            # Display last 10 transactions with better formatting
            recent_df = df.head(10).copy()
            recent_df['amount'] = recent_df['amount'].apply(lambda x: f"₹{x:,.2f}")
            recent_df['transaction_type'] = recent_df['transaction_type'].str.title()
            
            st.dataframe(
                recent_df[['date', 'transaction_type', 'category', 'amount', 'description']],
                use_container_width=True,
                hide_index=True
            )

elif page == "💰 Transaction Manager":
    # === TRANSACTION MANAGEMENT PAGE ===
    st.markdown("## 💰 Transaction Management Hub")
    
    # Tabs for different transaction operations
    tab1, tab2, tab3, tab4 = st.tabs(["➕ Add Transaction", "✏️ Update Transaction", "🗑️ Delete Transaction", "🔍 Search & Filter"])
    
    with tab1:
        st.markdown("### ➕ Add New Transaction")
        with st.form("add_transaction_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                amount = st.number_input("💰 Amount (₹)", min_value=0.01, step=0.01, format="%.2f")
                category = st.selectbox(
                    "🏷️ Category",
                    ["Food & Dining", "Transportation", "Shopping", "Entertainment", 
                     "Healthcare", "Education", "Utilities", "Investment", "Salary", "Other"]
                )
                transaction_type = st.selectbox("📊 Type", ["income", "expense", "investment", "transfer"])
            
            with col2:
                description = st.text_area("📝 Description", max_chars=200)
                tags = st.text_input("🏷️ Tags (comma-separated)", placeholder="groceries, monthly, essential")
                date_input = st.date_input("📅 Date", value=datetime.now())
            
            submitted = st.form_submit_button("💾 Save Transaction", type="primary", use_container_width=True)
            
            if submitted:
                payload = {
                    "amount": float(amount),
                    "category": category,
                    "description": description,
                    "transaction_type": transaction_type,
                    "tags": [tag.strip() for tag in tags.split(",")] if tags else [],
                    "date": date_input.isoformat()
                }
                
                try:
                    res = requests.post(f"{API_BASE}/transactions", json=payload, timeout=10)
                    if res.status_code == 201:
                        st.success("✅ Transaction added successfully!")
                        st.balloons()
                        # Clear cache to refresh data
                        st.cache_data.clear()
                    else:
                        st.error(f"❌ Failed to add transaction: {res.json().get('error', 'Unknown error')}")
                except requests.RequestException as e:
                    st.error(f"❌ Connection error: {str(e)}")
    
    with tab2:
        st.markdown("### ✏️ Update Transaction")
        df = get_transactions()
        if not df.empty:
            transaction_id = st.selectbox(
                "Select Transaction to Update",
                options=df['id'].tolist(),
                format_func=lambda x: f"ID: {x} - {df[df['id']==x]['category'].iloc[0]} - ₹{df[df['id']==x]['amount'].iloc[0]:.2f}"
            )
            
            if transaction_id:
                transaction = df[df['id'] == transaction_id].iloc[0]
                
                with st.form("update_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        new_amount = st.number_input("Amount", value=float(transaction['amount']), step=0.01)
                        new_category = st.text_input("Category", value=transaction['category'])
                        new_type = st.selectbox(
                            "Type", 
                            ["income", "expense", "investment", "transfer"],
                            index=["income", "expense", "investment", "transfer"].index(transaction['transaction_type'])
                        )
                    
                    with col2:
                        new_description = st.text_area("Description", value=transaction['description'])
                        new_tags = st.text_input("Tags", value=", ".join(transaction.get('tags', [])))
                    
                    if st.form_submit_button("🔄 Update Transaction", type="primary"):
                        payload = {
                            "amount": new_amount,
                            "category": new_category,
                            "description": new_description,
                            "transaction_type": new_type,
                            "tags": [t.strip() for t in new_tags.split(",")] if new_tags else []
                        }
                        
                        try:
                            res = requests.put(f"{API_BASE}/transactions/{transaction_id}", json=payload)
                            if res.status_code == 200:
                                st.success("✅ Transaction updated successfully!")
                                st.cache_data.clear()
                            else:
                                st.error(f"❌ Update failed: {res.json().get('error')}")
                        except requests.RequestException as e:
                            st.error(f"❌ Connection error: {str(e)}")
        else:
            st.info("📝 No transactions available to update.")
    
    with tab3:
        st.markdown("### 🗑️ Delete Transaction")
        df = get_transactions()
        if not df.empty:
            transaction_id = st.selectbox(
                "⚠️ Select Transaction to Delete",
                options=df['id'].tolist(),
                format_func=lambda x: f"ID: {x} - {df[df['id']==x]['category'].iloc[0]} - ₹{df[df['id']==x]['amount'].iloc[0]:.2f}"
            )
            
            if transaction_id:
                transaction = df[df['id'] == transaction_id].iloc[0]
                
                st.warning("⚠️ You are about to delete this transaction:")
                st.dataframe({
                    "Field": ["ID", "Amount", "Type", "Category", "Description", "Date"],
                    "Value": [
                        transaction['id'],
                        f"₹{transaction['amount']:.2f}",
                        transaction['transaction_type'],
                        transaction['category'],
                        transaction['description'],
                        transaction['date']
                    ]
                })
                
                if st.button("🗑️ Confirm Delete", type="secondary"):
                    try:
                        res = requests.delete(f"{API_BASE}/transactions/{transaction_id}")
                        if res.status_code == 200:
                            st.success("✅ Transaction deleted successfully!")
                            st.cache_data.clear()
                        else:
                            st.error(f"❌ Delete failed: {res.json().get('error')}")
                    except requests.RequestException as e:
                        st.error(f"❌ Connection error: {str(e)}")
        else:
            st.info("📝 No transactions available to delete.")
    
    with tab4:
        st.markdown("### 🔍 Search & Filter Transactions")
        df = get_transactions()
        
        if not df.empty:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                search_term = st.text_input("🔍 Search", placeholder="Search description, category...")
            with col2:
                filter_type = st.multiselect("📊 Filter by Type", df['transaction_type'].unique())
            with col3:
                filter_category = st.multiselect("🏷️ Filter by Category", df['category'].unique())
            
            # Apply filters
            filtered_df = df.copy()
            
            if search_term:
                filtered_df = filtered_df[
                    filtered_df['category'].str.contains(search_term, case=False, na=False) |
                    filtered_df['description'].str.contains(search_term, case=False, na=False)
                ]
            
            if filter_type:
                filtered_df = filtered_df[filtered_df['transaction_type'].isin(filter_type)]
            
            if filter_category:
                filtered_df = filtered_df[filtered_df['category'].isin(filter_category)]
            
            st.markdown(f"### 📊 Results ({len(filtered_df)} transactions)")
            
            if not filtered_df.empty:
                # Sort options
                sort_col1, sort_col2 = st.columns(2)
                with sort_col1:
                    sort_by = st.selectbox("Sort by", ["date", "amount", "category", "transaction_type"])
                with sort_col2:
                    sort_order = st.selectbox("Order", ["Descending", "Ascending"])
                
                ascending = sort_order == "Ascending"
                filtered_df = filtered_df.sort_values(by=sort_by, ascending=ascending)
                
                # Format for display
                display_df = filtered_df.copy()
                display_df['amount'] = display_df['amount'].apply(lambda x: f"₹{x:,.2f}")
                
                st.dataframe(
                    display_df[['date', 'transaction_type', 'category', 'amount', 'description']],
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("🔍 No transactions match your search criteria.")

elif page == "📈 Analytics & Insights":
    # === ANALYTICS PAGE ===
    st.markdown("## 📈 Advanced Analytics & Insights")
    
    df = get_transactions()
    summary = get_summary()
    
    if df.empty:
        st.warning("📊 No data available for analysis. Please add some transactions first.")
    else:
        # AI-Powered Insights Section
        st.divider()
        st.markdown("### AI-Powered Financial Insights")
        
        insight_tabs = st.tabs(["💡 Smart Tips", "📊 Pattern Analysis", "🎯 Goal Recommendations"])
        
        with insight_tabs[0]:
            if st.button("🚀 Generate Smart Financial Tips", type="primary"):
                with st.spinner("🤖 Analyzing your spending patterns..."):
                    tips_query = "Provide 3 personalized financial tips based on my spending patterns"
                    ai_tips = generate_ai_insights(tips_query, summary)
                    st.markdown(ai_tips)
        
        with insight_tabs[1]:
            if st.button("🔍 Analyze Spending Patterns", type="primary"):
                with st.spinner("🤖 Identifying patterns in your data..."):
                    pattern_query = "Analyze my spending patterns and identify any concerning trends"
                    ai_patterns = generate_ai_insights(pattern_query, summary)
                    st.markdown(ai_patterns)
        
        with insight_tabs[2]:
            if st.button("🎯 Get Goal Recommendations", type="primary"):
                with st.spinner("🤖 Creating personalized goals..."):
                    goal_query = "Suggest 3 realistic financial goals I should set based on my current spending"
                    ai_goals = generate_ai_insights(goal_query, summary)
                    st.markdown(ai_goals)

        st.divider()
        # Time-based analysis
        st.markdown("### 📅 Time-based Analysis")
        
        df['date'] = pd.to_datetime(df['date'])
        df['month_year'] = df['date'].dt.to_period('M').astype(str)
        
        monthly_data = df.groupby(['month_year', 'transaction_type'])['amount'].sum().unstack(fill_value=0)
        
        fig_timeline = go.Figure()
        
        for transaction_type in monthly_data.columns:
            fig_timeline.add_trace(go.Scatter(
                x=monthly_data.index,
                y=monthly_data[transaction_type],
                mode='lines+markers',
                name=transaction_type.title(),
                line=dict(width=3),
                marker=dict(size=8)
            ))
        
        fig_timeline.update_layout(
            title="💹 Monthly Transaction Trends",
            xaxis_title="Month",
            yaxis_title="Amount (₹)",
            height=500,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Category deep dive
        st.markdown("### 🏷️ Category Deep Dive")
        
        if "categories" in summary and summary["categories"]:
            category_insights = []
            for category, data in summary["categories"].items():
                category_insights.append({
                    "Category": category.title(),
                    "Total Amount": data["total_amount"],
                    "Transaction Count": data["transaction_count"],
                    "Average per Transaction": data["total_amount"] / data["transaction_count"]
                })
            
            cat_df = pd.DataFrame(category_insights)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_cat_amount = px.treemap(
                    cat_df,
                    path=['Category'],
                    values='Total Amount',
                    title="💰 Spending by Category (Treemap)"
                )
                st.plotly_chart(fig_cat_amount, use_container_width=True)
            
            with col2:
                fig_cat_freq = px.bar(
                    cat_df.sort_values('Transaction Count', ascending=False),
                    x='Category',
                    y='Transaction Count',
                    color='Average per Transaction',
                    title="📊 Transaction Frequency by Category"
                )
                fig_cat_freq.update_xaxes(tickangle=45)
                st.plotly_chart(fig_cat_freq, use_container_width=True)        

elif page == "📤 Data Export":
    # === DATA EXPORT PAGE ===
    st.markdown("## 📤 Export Your Financial Data")
    
    df = get_transactions()
    
    if df.empty:
        st.warning("📝 No data available to export.")
    else:
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📄 CSV Export")
            st.info("💡 Perfect for Excel analysis and data backup")
            
            if st.button("📥 Download CSV", type="primary", use_container_width=True):
                try:
                    res = requests.get(f"{API_BASE}/transactions/export?format=csv", timeout=30)
                    if res.ok:
                        st.download_button(
                            label="💾 Save CSV File",
                            data=res.content,
                            file_name=f"financeai_transactions_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                        st.success("✅ CSV file ready for download!")
                    else:
                        st.error("❌ Failed to generate CSV export")
                except requests.RequestException as e:
                    st.error(f"❌ Export error: {str(e)}")
        
        with col2:
            st.markdown("#### 📑 PDF Report")
            st.info("💡 Professional report for sharing and archiving")
            
            if st.button("📄 Generate PDF", type="primary", use_container_width=True):
                try:
                    res = requests.get(f"{API_BASE}/transactions/export?format=pdf", timeout=30)
                    if res.ok:
                        st.download_button(
                            label="💾 Save PDF Report",
                            data=res.content,
                            file_name=f"financeai_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                        st.success("✅ PDF report ready for download!")
                    else:
                        st.error("❌ Failed to generate PDF report")
                except requests.RequestException as e:
                    st.error(f"❌ Export error: {str(e)}")
        
        # Data preview
        st.markdown("### 👀 Data Preview")
        st.dataframe(df.head(10), use_container_width=True, hide_index=True)
        
        st.markdown(f"**📊 Total Records:** {len(df)} transactions")

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6C757D; padding: 1rem;">
    <p> <strong>MoneyMind AI</strong> | Powered by Google Gemini AI & Modern Python Stack</p>
</div>
""", unsafe_allow_html=True)