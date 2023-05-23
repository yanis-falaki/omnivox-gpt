from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os
import yaml
from dotenv import load_dotenv

load_dotenv('../../.env')

month_map = {
    "Jan": "January",
    "Feb": "February",
    "Mar": "March",
    "Apr": "April",
    "May": "May",
    "Jun": "June",
    "Jul": "July",
    "Aug": "August",
    "Sep": "September",
    "Oct": "October",
    "Nov": "November",
    "Dec": "December"
}


def Login(driver, id, password):
    driver.get("https://tav.omnivox.ca/Login")
    driver.find_element(By.ID, "Identifiant").send_keys(f"{id}")
    driver.find_element(By.ID, "Password").send_keys(f"{password}")
    driver.find_element(By.ID, "Password").submit()


def ScrapeClassList(driver):
    driver.find_element(
        By.CSS_SELECTOR, ".raccourci.id-service_CVIE.code-groupe_lea"
    ).click()
    class_elements = driver.find_elements(
        By.CSS_SELECTOR, ".card-panel.section-spacing"
    )
    return class_elements


# make a a list of dictionaries, each dictionary contains the keys: description, date, source. Each dictionary is a document
def ScrapeDocuments(driver, element):
    documents = []
    element.click()
    categories = driver.find_elements(
        By.CSS_SELECTOR, ".CategorieDocument.CategorieDocumentEtudiant"
    )
    for category in categories:
        tbody = category.find_elements(By.XPATH, "./child::*")[1]
        category_name = (
            category.find_elements(By.XPATH, "./child::*")[0]
            .find_elements(By.XPATH, "./child::*")[0]
            .text
        )
        tr_list = tbody.find_elements(By.XPATH, "./child::*")
        tr_list.pop()
        for tr in tr_list:
            td_list = tr.find_elements(By.XPATH, "./child::*")
            description_element = td_list[1]
            date_element = td_list[2]
            source_element = td_list[3]

            #source_link = source_element.find_elements(By.XPATH, "./child::*")[
            #    0
            #].get_attribute("href")
            # Formatting date from 3 letter month to full month name
            date = date_element.find_elements(By.XPATH, "./child::*")[0].text
            date_split = date.split(' ', 1)
            short_month = date_split[0].split("\n", 1)[1]
            month = f"{month_map[short_month]}"
            formatted_date = f"Distributed {month} {date_split[1]}"

            description = description_element.find_elements(By.XPATH, "./child::*")[
                0
            ].text
            #description = description.replace('\n', ' ')
            document = {
                "category": category_name,
                "description": description,
                "date_distributed": formatted_date,
            #    "document_link": source_link,
            }
            documents.append(document)

    driver.find_element(
        By.CSS_SELECTOR, ".raccourci.id-service_CVIP.code-groupe_lea"
    ).click()
    return documents


def ScrapeAssignments(driver, element):
    element.click()
    assignments = []
    category = "Assignments"

    try:
        parent = driver.find_element(By.CSS_SELECTOR, "#tabListeTravEtu")
    except:
        driver.find_element(
            By.CSS_SELECTOR, ".raccourci.id-service_CVIP.code-groupe_lea"
        ).click()
        return
    tr_list = parent.find_elements(By.XPATH, "./child::*")[0].find_elements(
        By.XPATH, "./child::*"
    )
    tr_list.pop(0)
    for tr in tr_list:
        if (
            len(tr.find_elements(By.XPATH, "./child::*")) == 2
            and tr.find_elements(By.XPATH, "./child::*")[1].get_attribute("class")
            == "TitreCategorie"
        ):
            category = tr.find_elements(By.XPATH, "./child::*")[1].text
            continue

        # Get all <td>s which are necessary
        td_list = tr.find_elements(By.XPATH, "./child::*")
        description_element = td_list[1]
        date_element = td_list[2]
        submission_element = td_list[3]

        # Get relavent text
        submission_status = submission_element.text
        date = date_element.find_elements(By.XPATH, "./child::*")[0].text
        description = description_element.text

        # Formatting date from 3 letter month to full month name
        date_split = date.split('-', 1)
        month = f"{month_map[date_split[0]]}"
        formatted_date = f"{month} {date_split[1]}"

        # Get linked document to assignment
        description_element.find_element(By.XPATH, ".//a").click()
        # opens pop-up window, must select it
        window_handles = driver.window_handles
        driver.switch_to.window(window_handles[1])
        if driver.find_element(By.ID, "lblDocumentLie").text == "No document":
            has_attachment = False
        else: has_attachment = True
        driver.close()
        driver.switch_to.window(window_handles[0])

        document = {
            "category": category,
            "description": description,
            "deadline": formatted_date,
            "submission_status": submission_status,
            "has_attachment": has_attachment,
        }
        assignments.append(document)
    driver.find_element(
        By.CSS_SELECTOR, ".raccourci.id-service_CVIP.code-groupe_lea"
    ).click()
    return assignments


def ScrapeGrades(driver, element, title):
    grade = "-"
    fractional_grade = element.find_elements(
        By.XPATH, ".//span[@class='note-principale']"
    )[0].text
    if fractional_grade != " -  ":
        grade = element.find_element(By.XPATH, ".//span[@class='pourcentage']").text
    average = element.find_elements(By.XPATH, ".//span[@class='note-principale']")[
        1
    ].text
    median = element.find_elements(By.XPATH, ".//span[@class='note-principale']")[
        2
    ].text
    return {
        "class": title,
        "grade": grade,
        "class_average": average,
        "class_median": median,
    }


def ScrapeAnnouncements(driver, element):
    pass


def RefreshElements(driver, i):
    class_elements = driver.find_elements(
        By.CSS_SELECTOR, ".card-panel.section-spacing"
    )
    element = class_elements[i]
    content = element.find_elements(By.XPATH, "./child::*")[1]
    return content.find_elements(By.XPATH, "./child::*")


def ScrapeClass(driver, i):
    class_title = (
        driver.find_elements(By.CSS_SELECTOR, ".card-panel.section-spacing")[i]
        .find_element(By.XPATH, ".//div[@class='card-panel-title']")
        .text
    )
    sections = RefreshElements(driver, i)
    documents = ScrapeDocuments(driver, sections[1])
    sections = RefreshElements(driver, i)
    assignments = ScrapeAssignments(driver, sections[2])
    sections = RefreshElements(driver, i)
    grades = ScrapeGrades(driver, sections[3], class_title)

    # create directory if not exists
    directory = f"./data/{class_title}/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # ScrapeAnnouncements(driver, sections[4])
    with open(f"./data/{class_title}/documents.yaml", "w") as f:
        yaml.dump(documents, f)
    with open(f"./data/{class_title}/assignments.yaml", "w") as f:
        yaml.dump(assignments, f)

    # all class grades will be in one file
    return [grades, class_title]


def start():
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome()
    Login(driver, os.environ.get("OMNI_USERNAME"), os.environ.get("OMNI_PASSWORD"))

    # traverse to class list section
    driver.find_element(
        By.CSS_SELECTOR, ".raccourci.id-service_CVIE.code-groupe_lea"
    ).click()
    # class_elements is a list of cards which contain classes
    class_elements = driver.find_elements(
        By.CSS_SELECTOR, ".card-panel.section-spacing"
    )

    grades = []
    classes = []
    for i in range(len(class_elements)):
        list = ScrapeClass(driver, i)
        grades.append(list[0])
        classes.append(list[1])
        # need to refresh class list
        class_elements = driver.find_elements(
            By.CSS_SELECTOR, ".card-panel.section-spacing"
        )

    # need to load grades outside of loop, as one grade file contains all classes
    with open("./data/grades.yaml", "w") as f:
        yaml.dump(grades, f)
    with open("./data/class_list.yaml", "w") as f:
        yaml.dump(classes, f)


if __name__ == "__main__":
    start()
