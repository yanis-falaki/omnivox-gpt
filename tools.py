from langchain.tools import BaseTool, Tool, tool
import json
import datetime
import pytz
from selenium import webdriver
from selenium.webdriver.common.by import By

@tool
def get_classes(input: str):
    """This is useful to get a list of all classes. The classes are given in a format of Course Code and Description"""
    with open("./data/class_list.json", "r") as f:
        data = f.read()
    return data


@tool
def get_assignments(class_name: str):
    """Useful for when you need to get all the assignments for a particular class. The input for this tool is a class in a format of Course Code and Description.
    Example inputs:
    201-NYC-05 LINEAR ALGEBRA
    201-NYB-05 CALCULUS II
    345-102-MQ WORLD VIEWS
    """
    try:
        with open(f"./data/{class_name}/assignments.json", "r") as f:
            data = json.load(f)
    except: return "The input must be formatted correctly"

    # Getting rid of assignment link to reduce token amount
    if data is not None:
        for d in data:
            del d["assignment_link"]

    formatted_data = json.dumps(data)
    return formatted_data


@tool
def get_documents(class_name: str):
    """Useful for when you need to get all the documents for a particular class. The input for this tool is a class in a format of Course Code and Description.
    Example inputs:
    201-NYC-05 LINEAR ALGEBRA
    201-NYB-05 CALCULUS II
    345-102-MQ WORLD VIEWS
    """
    try:
        with open(f"./data/{class_name}/documents.json", "r") as f:
            data = json.load(f)
    except: return "The input must be formatted correctly"

    # Getting rid of document link to reduce token amount
    if data is not None:
        for d in data:
            del d["document_link"]

    formatted_data = json.dumps(data)
    return formatted_data


@tool
def get_date(input=""):
    """Useful for when you need to get the current date"""
    est_tz = pytz.timezone('US/Eastern')
    now = datetime.datetime.now(tz=est_tz)
    date = now.strftime("%d %B %Y")
    return date


@tool
def get_grade_info(class_name: str):
    """Useful for when you need to either get the student's grade, class average, and class median for any particular class. The input for this tool is a class in format of
    Course code and Description. Example input: 201-NYC-05 LINEAR ALGEBRA"""
    with open(f"./data/grades.json", "r") as f:
        data = json.load(f)

    class_data = None

    for d in data:
        if d["class"] == class_name:
            class_data = d

    return class_data



@tool
def download_assignment(input:str):
    """Useful for when you need to get the link of an assignment. The input for this tool is a class in format of
    Course code and Description, and the assignment description field i.e class_name tilda description, there should be no spaces before or after the tilda.
    You can get a list of assignments with descriptions for a particular class using the get_assignments tool.
    Example inputs:
    201-NYC-05 LINEAR ALGEBRA~Assignment 1
    201-NYB-05 CALCULUS II~Sigma Notation
    345-102-MQ WORLD VIEWS~Debate Instructions"""
    split_string = input.split('~', 1)
    assignment_link = "The assignment does not have a document attatched"

    try:
        with open(f"./data/{split_string[0]}/assignments.json", "r") as f:
            json_object = json.load(f)
    except:
        print(f"./data/{split_string[0]}/assignments.json")
        return "Invalid Input"
    for d in json_object:
        if d["description"] == split_string[1]:
            assignment_link = d["assignment_link"]
    
    # navigating to omnivox and logging in
    driver = webdriver.Chrome()
    driver.get("https://tav.omnivox.ca/Login")
    driver.find_element(By.ID, "Identifiant").send_keys(os.environ.get("OMNI_USERNAME"))
    driver.find_element(By.ID, "Password").send_keys(os.environ.get("OMNI_PASSWORD"))
    driver.find_element(By.ID, "Password").submit()

    # Navigating to document assignment page
    driver.get(assignment_link)

@tool
def query_attatchments(query:str):
    """Useful for when you need to ask questions about assignments or documents that have been downloaded. In order to query a document or assignment,
    you must first download them."""