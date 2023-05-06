from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

def Login(driver, id, password):
    driver.get("https://tav.omnivox.ca/Login")
    driver.find_element(By.ID, 'Identifiant').send_keys(f'{id}')
    driver.find_element(By.ID, 'Password').send_keys(f'{password}')
    driver.find_element(By.ID, 'Password').submit()


def ScrapeEvents(driver):
    events = driver.find_element(By.CSS_SELECTOR, ".carte-portail.carte-evenement")
    print(events.text)
    return 0


def ScrapeClassList(driver):
    driver.find_element(By.CSS_SELECTOR, ".raccourci.id-service_CVIE.code-groupe_lea").click()
    class_elements = driver.find_elements(By.CSS_SELECTOR, ".card-panel.section-spacing")
    return class_elements


# make a a list of dictionaries, each dictionary contains the keys: description, date, source. Each dictionary is a document
def ScrapeDocuments(driver, element):
    documents = []
    element.click()
    categories = driver.find_elements(By.CSS_SELECTOR, ".CategorieDocument.CategorieDocumentEtudiant")
    for category in categories:
        tbody = category.find_elements(By.XPATH, "./child::*")[1]
        category_name = category.find_elements(By.XPATH, "./child::*")[0].find_elements(By.XPATH, "./child::*")[0].text
        tr_list = tbody.find_elements(By.XPATH, "./child::*")
        tr_list.pop()
        for tr in tr_list:
            td_list = tr.find_elements(By.XPATH, "./child::*")
            description_element = td_list[1]
            date_element = td_list[2]
            source_element = td_list[3]

            source_link = source_element.find_elements(By.XPATH, "./child::*")[0].get_attribute("href")
            date = date_element.find_elements(By.XPATH, "./child::*")[0].text
            description = description_element.find_elements(By.XPATH, "./child::*")[0].text
            document = {"category": category_name, "description": description, "date_distributed": date, "document_link": source_link}
            documents += document
            print(document)

    driver.find_element(By.CSS_SELECTOR, ".raccourci.id-service_CVIP.code-groupe_lea").click()
    return documents
          

def ScrapeAssignments(driver, element):
    element.click()
    assignments = []
    category = "Assignments"
    try :tr_list = driver.find_element(By.ID, "tabListeTravEtu")[0].find_elements(By.XPATH, "./child::*").find_elements(By.XPATH, "./child::*")
    except: driver.find_element(By.CSS_SELECTOR, ".raccourci.id-service_CVIP.code-groupe_lea").click(); return
    tr_list.pop(0)
    for tr in tr_list:
        if len(tr.find_elements(By.XPATH, "./child::*")) == 2 and tr.find_elements(By.XPATH, "./child::*")[1].get_attribute("class") == "TitreCategorie":
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

        # Get linked document to assignment
        description_element.find_element(By.XPATH, ".//a").click()
        # opens pop-up window, must select it
        window_handles = driver.window_handles
        driver.switch_to.window(window_handles[1])
        document_source = driver.find_element(By.ID, "ALienFichierLie2").get_attribute("href")
        driver.close()
        driver.switch_to.window(window_handles[0])

        document = {"category": category, "description": description, "deadline": date, "submission_status": submission_status, "assignment_link": document_source}
        assignments += document
        print(document)
        print(description)
    driver.find_element(By.CSS_SELECTOR, ".raccourci.id-service_CVIP.code-groupe_lea").click()
    return assignments


def ScrapeEvaluations(driver, element):
    pass


def ScrapeAnnouncements(driver, element):
    pass


def RefreshElements(driver, i):
    class_elements = driver.find_elements(By.CSS_SELECTOR, ".card-panel.section-spacing")
    element = class_elements[i]
    content = element.find_elements(By.XPATH, "./child::*")[1]
    return content.find_elements(By.XPATH, "./child::*")


def ScrapeClass(driver, i):
    sections = RefreshElements(driver, i)
    ScrapeDocuments(driver, sections[1])
    sections = RefreshElements(driver, i)
    #ScrapeAssignments(driver, sections[2])
    sections = RefreshElements(driver, i)
    #ScrapeEvaluations(driver, sections[3])
    #ScrapeAnnouncements(driver, sections[4])


def start():
    driver = webdriver.Chrome()
    Login(driver, os.environ.get("OMNI_USERNAME"), os.environ.get("OMNI_PASSWORD"))
    #time.sleep(10)

    # scrape class list
    driver.find_element(By.CSS_SELECTOR, ".raccourci.id-service_CVIE.code-groupe_lea").click()
    # class_elements is a list of cards which contain classes
    class_elements = driver.find_elements(By.CSS_SELECTOR, ".card-panel.section-spacing")
    
    #for i in range(len(class_elements)):
    #   ScrapeClass(driver, i)
       #need to refresh class list
    #   class_elements = driver.find_elements(By.CSS_SELECTOR, ".card-panel.section-spacing")
    ScrapeClass(driver, 1)

if __name__ == "__main__":
    start()