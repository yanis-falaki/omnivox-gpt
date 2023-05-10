from dotenv import load_dotenv

load_dotenv()
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain import PromptTemplate
import tools
from langchain.llms import OpenAI


def run_llm(question:str):
    llm = OpenAI(temperature=0)
    template = """You are a helpful AI assistant, your job is to help students and answer their questions, all your answers must be in second person. All answers must be human readable, as in it wont 
    include brackets, quotes, or anything of that nature (unless it helps make the answer more understandable). Punctuation and capitalization must be gramatically correct, nothing
    can be in all capitalized letters. Examples:
    LINEAR ALGEBRA -> Linear Algebra
    "305-TVB-TV SOCIAL SCIENCE II" -> Social Science II
    Quesion: {question}"""

    tools_for_agent = [
        tools.get_classes,
        tools.get_assignments,
        tools.get_documents,
        tools.get_date,
        tools.get_grade_info,
        tools.download_assignment,
    ]

    agent = initialize_agent(
        tools=tools_for_agent,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    prompt_template = PromptTemplate(template=template, input_variables=["question"])

    result = agent.run(prompt_template.format(question=question))
    return result


if __name__ == "__main__":
    print(run_llm(input()))