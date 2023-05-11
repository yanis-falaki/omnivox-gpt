from langchain.tools import BaseTool, Tool, tool
import json
import datetime
import pytz
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
import requests
import os

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
    """Useful for when you need to download an assignment. The input for this tool is a class in format of Course code and Description, 
    and the assignment description field i.e class_name tilda description. You can get a list of assignments with descriptions for a particular class using the get_assignments tool.
    Example inputs:
    201-NYC-05 LINEAR ALGEBRA ~ Assignment 1
    201-NYB-05 CALCULUS II ~ Sigma Notation
    345-102-MQ WORLD VIEWS ~ Debate Instructions"""
    class_assignment = input.split(' ~ ', 1)

    try:
        with open(f"./data/{class_assignment[0]}/assignments.json", "r") as f:
            json_object = json.load(f)
    except:
        print(f"./data/{class_assignment[0]}/assignments.json")
        return "Invalid Input"
    
    for d in json_object:
        if d["description"] == class_assignment[1]:
            assignment_link = d["assignment_link"]
            if assignment_link == "null" or assignment_link is None:
                return "There is no document attatched to this assignment"
    

    # set up the Chrome driver
    driver = webdriver.Chrome()

    # navigate to the website and log in
    driver.get("https://tav.omnivox.ca/Login/")
    driver.find_element(By.ID, "Identifiant").send_keys(os.environ.get("OMNI_USERNAME"))
    driver.find_element(By.ID, "Password").send_keys(os.environ.get("OMNI_PASSWORD"))
    driver.find_element(By.ID, "Password").submit()

    # Navigate to class list
    driver.find_element(
        By.CSS_SELECTOR, ".raccourci.id-service_CVIE.code-groupe_lea"
    ).click()

    # need to parse class name to select proper element
    code_class = class_assignment[0].split(" ", 1)

    # selecting the proper elements
    title = driver.find_element(By.XPATH, f"//..//*[contains(text(), '{code_class[0]}') and contains(text(), '{code_class[1]}')]")
    content = title.find_element(By.XPATH, "../..")

    # This gets to the assignment section, changing the last index to 1 changes to documents
    content.find_elements(By.XPATH, "./child::*")[1].find_elements(By.XPATH, "./child::*")[2].click()

    # Open assignment window
    driver.find_element(By.XPATH, f"//..//*[contains(text(), '{class_assignment[1]}')]").click()

    # opens pop-up window, must select it
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[1])

    # Open pdf file
    driver.find_element(By.ID, "ALienFichierLie2").click()

    # creating request session
    session = requests.Session()

    # Need to copy cookies to session
    url = driver.current_url
    cookies = driver.get_cookies()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])
        
    # need to add headers as well
    for request in driver.requests:
        headers = request.headers # <----------- Request headers
    for key, value in headers.items():
        session.headers[key] = value

    response = session.get(url)
    print(url)
    print(response)

    # create directory if does not exist, then write to file
    directory = f"./data/downloads/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(f"{directory}/{class_assignment[0]}-{class_assignment[1]}.pdf", "wb") as f:
        f.write(response.content)

    # close the driver
    driver.quit()

    if response.status_code == 200:
        return "Downloaded Succesfully."
    elif response.status_code == 403:
        return "Download failed. Response 403"
    else:
        return f"Download failed. Response {response.status_code}"


@tool
def query_attatchments(query:str):
    """Useful for when you need to ask questions about assignments or documents that have been downloaded. In order to query a document or assignment,
    you must first download them."""