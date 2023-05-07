from dotenv import load_dotenv
load_dotenv()
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.tools import BaseTool, Tool, tool


def get_classes(input=""):
    """This tool returns a list of classes"""
    return "Science, French, English, and Math"


get_classes = Tool.from_function(
    name="Get Classes",
    func=get_classes,
    description="Useful for when you need to answer questions about what classes someone has."
)


llm = ChatOpenAI(temperature=0)
tools = [get_classes]



agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
agent.run("What classes do I have")
