"""I am a 30 year old person having 2 kids, wife and parents. 
I with my family are living in Banglore. My annual income is 45lakhs.
 My monthly expenses are on average 2lakhs. 
 I have only 1 emi (included in expenses) for my car. 
 I want to buy a new house almost costing 4cr. 
 My current house values almost 1.2cr. 
 I have 5 lakhs in lumsup 3 different mutual funds each.
   My risk profile is moderate. I have invested 10 lakhs in equity as well.
"""


import streamlit as st
import sys
import os
from backend.agent_manager import get_agent_advice
from backend.news_fetcher import fetch_latest_news
from vector_store.chromadb_store import ChromaVectorStore
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"logs/app_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# App configuration
st.set_page_config(
    layout="wide", 
    page_title="Multi-Agent Financial Analyzer",
    page_icon="💰"
)

def main():
    try:
        st.title("Multi-Agent Financial Analyzer")
        
        # Instantiate the vector store for additional context retrieval
        @st.cache_resource
        def get_vector_store():
            try:
                return ChromaVectorStore()
            except Exception as e:
                logger.error(f"Failed to initialize vector store: {e}")
                st.error("Could not connect to document database. Some features may be limited.")
                return None
                
        vector_store = get_vector_store()

        # Sidebar: Task selection, additional context query, and news inclusion
        with st.sidebar:
            st.title("Navigation")
            
            # Authentication placeholder (could be expanded)
            if 'authenticated' not in st.session_state:
                st.session_state.authenticated = False
                
            # Simple authentication mechanism
            if not st.session_state.authenticated:
                st.subheader("Login")
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                if st.button("Login"):
                    # In production, use proper authentication
                    if username == "admin" and password == "password":
                        st.session_state.authenticated = True
                        st.success("Logged in successfully!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
                st.stop()
            
            # User is authenticated, show navigation
            st.success("Logged in ✓")
            if st.button("Logout"):
                st.session_state.authenticated = False
                st.rerun()
                
            task_option = st.radio(
                "Select Task", 
                ["Generic Advice", "Portfolio Management", "Domain-Specific Advice"]
            )
            
            additional_context_query = st.text_input(
                "Context Query", 
                placeholder="Enter keywords for news and document insights",
                help="Keywords to search in our knowledge base and news"
            )
            
            include_latest_news = st.checkbox(
                "Include Latest News", 
                value=True,
                help="Fetch and analyze the latest financial news related to your query"
            )
            
            st.divider()
            st.markdown("### Advanced Settings")
            
            temperature = st.slider(
                "AI Creativity", 
                min_value=0.0, 
                max_value=1.0, 
                value=0.7, 
                step=0.1,
                help="Higher values make responses more creative but potentially less accurate"
            )
            
            max_tokens = st.slider(
                "Response Length", 
                min_value=256, 
                max_value=4096, 
                value=1024, 
                step=256,
                help="Maximum length of the AI-generated response"
            )

        # Document context retrieval
        retrieved_docs = []
        doc_context = ""
        if vector_store and additional_context_query:
            with st.spinner("Retrieving additional context from documents..."):
                try:
                    retrieved_docs = vector_store.query(additional_context_query, n_results=3)
                    doc_context = "\n\n".join(retrieved_docs) if retrieved_docs else ""
                except Exception as e:
                    logger.error(f"Error retrieving documents: {e}")
                    st.warning("Could not retrieve document context. Continuing without it.")

        # News context retrieval
        news_context = ""
        if include_latest_news and additional_context_query:
            with st.spinner("Fetching latest news..."):
                try:
                    news_context = fetch_latest_news(query=additional_context_query, num_articles=5)
                except Exception as e:
                    logger.error(f"Error fetching news: {e}")
                    st.warning("Could not fetch latest news. Continuing without it.")

        # Combine the contexts
        additional_context = ""
        if doc_context:
            additional_context += f"Document Context:\n{doc_context}\n\n"
        if news_context:
            additional_context += f"Latest News:\n{news_context}"
        if not additional_context:
            additional_context = "No additional context provided."

        # Main content area
        st.write("### Task: " + task_option)
        
        # Create tabs for input and history
        tab1, tab2 = st.tabs(["Get Advice", "History"])
        
        with tab1:
            if task_option == "Generic Advice":
                st.header("Generic Financial Advice")
                user_input = st.text_area(
                    "Describe your situation and the advice you need:",
                    placeholder="Example: I'm 35 years old with 50,000 INR in savings. How should I invest for retirement?",
                    height=150
                )
                
                if st.button("Get Advice", key="generic", use_container_width=True):
                    if not user_input.strip():
                        st.error("Please enter your financial situation and question.")
                        st.stop()
                        
                    with st.spinner("Generating personalized financial advice..."):
                        try:
                            answer = get_agent_advice(
                                "generic", 
                                context=additional_context, 
                                user_input=user_input,
                                temperature=temperature,
                                max_tokens=max_tokens
                            )
                            
                            # Save to history
                            if 'history' not in st.session_state:
                                st.session_state.history = []
                            st.session_state.history.append({
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "task": "Generic Advice",
                                "query": user_input,
                                "response": answer
                            })
                            
                            st.subheader("Advice")
                            st.markdown(answer)
                            
                            # Feedback mechanism
                            col1, col2 = st.columns(2)
                            with col1:
                                st.button("👍 Helpful", key="helpful_generic")
                            with col2:
                                st.button("👎 Not Helpful", key="not_helpful_generic")
                        except Exception as e:
                            logger.error(f"Error generating advice: {e}")
                            st.error("An error occurred while generating advice. Please try again.")

            elif task_option == "Portfolio Management":
                st.header("Portfolio and Asset Management")
                
                # Example template
                with st.expander("See example portfolio format"):
                    st.code("""
Stocks: 40% (AAPL 10%, MSFT 8%, AMZN 7%, other tech 15%)
Bonds: 30% (Treasury 20%, Corporate 10%)
Real Estate: 20% (REITs)
Cash: 10%
Risk profile: Moderate
Investment horizon: 10 years
                    """)
                
                portfolio_details = st.text_area(
                    "Enter your portfolio details (asset classes, sectors, stocks, etc.):",
                    placeholder="Example: Stocks 60% (Tech 30%, Finance 20%, Healthcare 10%), Bonds 30%, Cash 10%",
                    height=150
                )
                
                user_input = st.text_area(
                    "Specify what you want to analyze:",
                    placeholder="Example: Analyze my portfolio's risk profile and suggest adjustments for a recession scenario",
                    height=100
                )
                
                if st.button("Analyze Portfolio", key="portfolio", use_container_width=True):
                    if not portfolio_details.strip() or not user_input.strip():
                        st.error("Please enter both your portfolio details and analysis request.")
                        st.stop()
                        
                    with st.spinner("Analyzing portfolio and generating recommendations..."):
                        try:
                            answer = get_agent_advice(
                                "portfolio", 
                                portfolio_details=portfolio_details, 
                                context=additional_context, 
                                user_input=user_input,
                                temperature=temperature,
                                max_tokens=max_tokens
                            )
                            
                            # Save to history
                            if 'history' not in st.session_state:
                                st.session_state.history = []
                            st.session_state.history.append({
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "task": "Portfolio Management",
                                "query": f"Portfolio: {portfolio_details}\nQuery: {user_input}",
                                "response": answer
                            })
                            
                            st.subheader("Portfolio Recommendations")
                            st.markdown(answer)
                            
                            # Feedback mechanism
                            col1, col2 = st.columns(2)
                            with col1:
                                st.button("👍 Helpful", key="helpful_portfolio")
                            with col2:
                                st.button("👎 Not Helpful", key="not_helpful_portfolio")
                        except Exception as e:
                            logger.error(f"Error analyzing portfolio: {e}")
                            st.error("An error occurred while analyzing your portfolio. Please try again.")

            elif task_option == "Domain-Specific Advice":
                st.header("Domain-Specific Investment Advice")
                
                # Domain selection to give more structure
                domain_type = st.selectbox(
                    "Select investment domain",
                    ["Tech Stocks", "Cryptocurrency", "Real Estate", "Commodities", "ETFs & Mutual Funds", "Other"],
                    help="Choose the specific investment domain you need advice on"
                )
                
                domain_details = st.text_area(
                    f"Enter details of your {domain_type.lower()} holdings:",
                    placeholder=f"Example: I own Bitcoin (30%), Ethereum (40%), and Solana (30%)" if domain_type == "Cryptocurrency" else "List your specific investments in this domain",
                    height=150
                )
                
                user_input = st.text_area(
                    "Specify the advice you need:",
                    placeholder="Example: Should I rebalance my crypto portfolio given recent market volatility?",
                    height=100
                )
                
                if st.button("Get Domain Advice", key="domain", use_container_width=True):
                    if not domain_details.strip() or not user_input.strip():
                        st.error("Please enter both your domain holdings and advice request.")
                        st.stop()
                        
                    with st.spinner(f"Generating specialized advice for {domain_type}..."):
                        try:
                            # Include domain type in the context
                            domain_context = f"Investment Domain: {domain_type}\n\n{domain_details}"
                            
                            answer = get_agent_advice(
                                "domain", 
                                domain_details=domain_context,
                                context=additional_context, 
                                user_input=user_input,
                                temperature=temperature,
                                max_tokens=max_tokens
                            )
                            
                            # Save to history
                            if 'history' not in st.session_state:
                                st.session_state.history = []
                            st.session_state.history.append({
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "task": f"Domain Advice: {domain_type}",
                                "query": f"Holdings: {domain_details}\nQuery: {user_input}",
                                "response": answer
                            })
                            
                            st.subheader(f"{domain_type} Investment Recommendations")
                            st.markdown(answer)
                            
                            # Feedback mechanism
                            col1, col2 = st.columns(2)
                            with col1:
                                st.button("👍 Helpful", key="helpful_domain")
                            with col2:
                                st.button("👎 Not Helpful", key="not_helpful_domain")
                        except Exception as e:
                            logger.error(f"Error generating domain advice: {e}")
                            st.error("An error occurred while generating domain-specific advice. Please try again.")
        
        # History tab
        with tab2:
            st.header("Advice History")
            if 'history' not in st.session_state or not st.session_state.history:
                st.info("No advice history yet. Get some advice first!")
            else:
                # Display history in reverse chronological order
                for i, item in enumerate(reversed(st.session_state.history)):
                    with st.expander(f"{item['timestamp']} - {item['task']}"):
                        st.subheader("Your Query")
                        st.markdown(item["query"])
                        st.subheader("Response")
                        st.markdown(item["response"])
                        
                        # Option to delete this history item
                        if st.button("Delete This Record", key=f"delete_{i}"):
                            # Find the index in the original list
                            original_idx = len(st.session_state.history) - 1 - i
                            st.session_state.history.pop(original_idx)
                            st.rerun()
                
                # Clear all history button
                if st.button("Clear All History"):
                    st.session_state.history = []
                    st.rerun()
                    
        # Footer
        st.divider()
        st.markdown(
            """
            <div style="text-align: center; color: gray; font-size: 0.8em;">
                Multi-Agent Financial Analyzer v2.0 | Disclaimer: This tool provides informational guidance only, not financial advice. 
                Consult with a certified financial advisor before making investment decisions.
            </div>
            """, 
            unsafe_allow_html=True
        )
                
    except Exception as e:
        logger.critical(f"Application error: {e}", exc_info=True)
        st.error("An unexpected error occurred. Please refresh the page and try again.")
        st.exception(e)

if __name__ == "__main__":
    # Ensure log directory exists
    os.makedirs("logs", exist_ok=True)
    main()