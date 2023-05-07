from langchain.tools import BaseTool, Tool, tool
import json
import datetime


@tool
def get_classes(input: str):
    """This is useful to get a list of all classes. The classes are given in a format of Course Code and Description"""
    with open("./data/class_list.json", "r") as f:
        data = f.read()
    return data


@tool
def get_assignments(class_name: str):
    """Useful for when you need to get all the assignments for a particular class. The input for this tool is a class in a format of Course Code and Description.
    Example input: 201-NYC-05 LINEAR ALGEBRA"""
    with open(f"./data/{class_name}/assignments.json", "r") as f:
        data = json.load(f)

    # Getting rid of assignment link to reduce token amount
    if data is not None:
        for d in data:
            del d["assignment_link"]

    formatted_data = json.dumps(data)
    return formatted_data


@tool
def get_documents(class_name: str):
    """Useful for when you need to get all the documents for a particular class. The input for this tool is a class in a format of Course Code and Description.
    Example input: 201-NYC-05 LINEAR ALGEBRA"""
    with open(f"./data/{class_name}/documents.json", "r") as f:
        data = json.load(f)

    # Getting rid of document link to reduce token amount
    if data is not None:
        for d in data:
            del d["document_link"]

    formatted_data = json.dumps(data)
    return formatted_data


@tool
def get_date(input=""):
    """Useful for when you need to get the current date"""
    now = datetime.datetime.now()
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
