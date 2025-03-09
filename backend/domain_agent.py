from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from .llm_wrapper import GroqLLM
import logging

logger = logging.getLogger(__name__)

def create_domain_chain(temperature=0.7, max_tokens=1024):
    """
    Creates a LangChain chain for domain-specific investment advice.
    
    Args:
        temperature: Temperature parameter for generation (0.0 to 1.0)
        max_tokens: Maximum number of tokens to generate
        
    Returns:
        LLMChain: The configured chain
    """
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    prompt_template = """
    You are a domain-specific investment advisor.
    Focus on the domain described below (e.g., Tech stocks, cryptocurrency, real estate, commodities, etc.).
    Using the provided domain holdings, latest market news, quarterly results, and insights from finance literature,
    analyze the risks and opportunities.
    
    Domain Holdings:
    {domain_details}
    
    Additional Context:
    {context}
    
    Conversation History:
    {chat_history}
    
    User Query:
    {user_input}
    
    Provide detailed, domain-specific recommendations with the following sections:
    1. Domain Overview: Summarize the current holdings and market conditions for this investment domain
    2. Opportunity Analysis: Identify growth opportunities and positive trends in this domain
    3. Risk Assessment: Highlight specific risks and challenges in this domain
    4. Strategic Recommendations: Provide domain-specific advice on position sizing, entry/exit strategies, and risk management
    5. Next Steps: Suggest specific actions the user can take
    
    Your advice should be tailored to the specific characteristics of the investment domain.
    Be specific with your recommendations while avoiding particular product endorsements.
    """
    prompt = PromptTemplate(
        input_variables=["domain_details", "context", "chat_history", "user_input"],
        template=prompt_template
    )
    llm = GroqLLM(temperature=temperature, max_tokens=max_tokens)
    chain = LLMChain(llm=llm, prompt=prompt, memory=memory)
    return chain

def get_domain_advice(domain_details: str, context: str, user_input: str, temperature=0.7, max_tokens=1024):
    """
    Generates domain-specific investment advice based on user input and domain details.
    
    Args:
        domain_details: Details of the user's domain holdings
        context: Additional context information
        user_input: The user's query
        temperature: Temperature parameter for generation (0.0 to 1.0)
        max_tokens: Maximum number of tokens to generate
        
    Returns:
        str: The generated advice
    """
    logger.info("Generating domain-specific investment advice")
    try:
        chain = create_domain_chain(temperature=temperature, max_tokens=max_tokens)
        chat_history = chain.memory.load_memory_variables({}).get("chat_history", "")
        return chain.run(domain_details=domain_details, context=context, chat_history=chat_history, user_input=user_input)
    except Exception as e:
        logger.error(f"Error generating domain advice: {str(e)}", exc_info=True)
        return "Sorry, I encountered an error while generating domain-specific advice. Please try again or refine your query."