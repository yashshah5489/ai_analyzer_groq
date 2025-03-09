from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from .llm_wrapper import GroqLLM
import logging

logger = logging.getLogger(__name__)

def create_portfolio_chain(temperature=0.7, max_tokens=1024):
    """
    Creates a LangChain chain for portfolio management advice.
    
    Args:
        temperature: Temperature parameter for generation (0.0 to 1.0)
        max_tokens: Maximum number of tokens to generate
        
    Returns:
        LLMChain: The configured chain
    """
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    prompt_template = """
    You are a portfolio and asset management expert.
    The user has provided their portfolio details and risk profile.
    Using the context below (including news, policy updates, and insights from finance books),
    analyze the portfolio and recommend adjustments.
    
    For example, if there is overexposure in a sector affected by negative news (e.g., metals facing tariff hikes),
    advise diversification or hedging.
    
    Portfolio Details:
    {portfolio_details}
    
    Additional Context:
    {context}
    
    Conversation History:
    {chat_history}
    
    User Query:
    {user_input}
    
    Provide a detailed analysis of the portfolio with the following sections:
    1. Portfolio Overview: Summarize the current allocation and identify key strengths and weaknesses
    2. Risk Assessment: Analyze diversification, sector exposure, and overall risk level
    3. Specific Recommendations: Suggest adjustments to improve returns or reduce risk
    4. Action Plan: Provide a clear set of steps the user can take to implement your recommendations
    
    Be specific with percentages and allocation advice but avoid recommending particular stocks or financial products.
    """
    prompt = PromptTemplate(
        input_variables=["portfolio_details", "context", "chat_history", "user_input"],
        template=prompt_template
    )
    llm = GroqLLM(temperature=temperature, max_tokens=max_tokens)
    chain = LLMChain(llm=llm, prompt=prompt, memory=memory)
    return chain

def get_portfolio_advice(portfolio_details: str, context: str, user_input: str, temperature=0.7, max_tokens=1024):
    """
    Generates portfolio management advice based on user input and portfolio details.
    
    Args:
        portfolio_details: Details of the user's portfolio
        context: Additional context information
        user_input: The user's query
        temperature: Temperature parameter for generation (0.0 to 1.0)
        max_tokens: Maximum number of tokens to generate
        
    Returns:
        str: The generated advice
    """
    logger.info("Generating portfolio management advice")
    try:
        chain = create_portfolio_chain(temperature=temperature, max_tokens=max_tokens)
        chat_history = chain.memory.load_memory_variables({}).get("chat_history", "")
        return chain.run(portfolio_details=portfolio_details, context=context, chat_history=chat_history, user_input=user_input)
    except Exception as e:
        logger.error(f"Error generating portfolio advice: {str(e)}", exc_info=True)
        return "Sorry, I encountered an error while generating portfolio advice. Please try again or refine your query."