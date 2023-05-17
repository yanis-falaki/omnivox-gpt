from dotenv import load_dotenv

load_dotenv("../../.env")
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain import PromptTemplate
import tools
from langchain.llms import OpenAI
from langchain.agents import ConversationalAgent, ZeroShotAgent, AgentExecutor
from langchain.chains import LLMChain


def run_llm(question:str, memory):
    llm = ChatOpenAI(temperature=0)
    
    #template = """You are a helpful AI assistant, your job is to help students and answer their questions, all your answers must be in second person. All answers must be human readable, as in it wont 
    #include brackets, quotes, or anything of that nature (unless it helps make the answer more understandable). Punctuation and capitalization must be gramatically correct, nothing
    #can be in all capitalized letters. Examples:
    #LINEAR ALGEBRA -> Linear Algebra
    #"305-TVB-TA SOCIAL SCIENCE II" -> Social Science II
    #Question: {question}"""

    tools_for_agent = [
        tools.get_classes,
        tools.get_assignments,
        tools.get_documents,
        tools.get_date,
        tools.get_grade_info,
        tools.download_attachment,
    ]

    #agent = initialize_agent(
    #    tools=tools_for_agent,
    #    llm=llm,
    #    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    #    memory=memory,
    #    verbose=True,
    #)

    #prompt_template = PromptTemplate(template=template, input_variables=["question"])

    #result = agent.run(prompt_template.format(question=question))
    #print(memory.buffer)
    #return result


    prefix = """You are a helpful AI assistant, your job is to help students and answer their questions, all your answers must be in second person. All answers must be human readable, as in it wont 
    include brackets, quotes, or anything of that nature (unless it helps make the answer more understandable). Punctuation and capitalization must be gramatically correct, nothing
    can be in all capitalized letters. 
    Examples:
    209-TVS-TB LINEAR ALGEBRA -> Linear Algebra
    305-TVB-TA SOCIAL SCIENCE II -> Social Science II
    You have access to the following tools:"""
    suffix = """Begin!"

    {chat_history}
    Question: {input}
    {agent_scratchpad}"""

    prompt = ZeroShotAgent.create_prompt(
        tools_for_agent, 
        prefix=prefix, 
        suffix=suffix, 
        input_variables=["input", "chat_history", "agent_scratchpad"]
    )
    llm_chain = LLMChain(llm=OpenAI(temperature=0), prompt=prompt)
    agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools_for_agent, verbose=True)
    agent_chain = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools_for_agent, verbose=True, memory=memory)
    result = agent_chain.run(question)
    print(memory.buffer)
    return result


if __name__ == "__main__":
    print(run_llm(input()))