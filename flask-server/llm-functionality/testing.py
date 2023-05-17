import time
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
import os
import requests
import mimetypes

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

title = driver.find_element(By.XPATH, "//..//*[contains(text(), '201-NYB-05') and contains(text(), 'CALCULUS II')]")
content = title.find_element(By.XPATH, "../..")

# This get's to the assignment section, changing the last index to 2 changes to assignments
content.find_elements(By.XPATH, "./child::*")[1].find_elements(By.XPATH, "./child::*")[1].click()

document_name = 'Course outline 201-NYB-05 sect. 02216'
#document_name = "Basic Integrals"


try:
    document_link = driver.find_element(By.XPATH, f"//*[contains(text(), '{document_name}')").get_attribute("href")
except:
    try:
        xpath = ''
        split_name = document_name.split(' ')
        for i in range(len(split_name)):
            if i == 0:
                xpath = f"//*[contains(text(), '{split_name[i]}')"
            elif i == len(split_name) -1:
                xpath += f" and contains(text(), '{split_name[i]}')]"
            else:
                xpath += f" and contains(text(), '{split_name[i]}')"
        document_link = driver.find_element(By.XPATH, xpath).get_attribute("href")
    except:
        print("No document element found when web scraping")


# need to copy url and cookies to pass to requests library
session = requests.Session()

cookies = driver.get_cookies()
for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'])

# need to add headers as well
for request in driver.requests:
  headers = request.headers # <----------- Request headers
for key, value in headers.items():
    session.headers[key] = value

response = session.get(document_link)

# Get the file extension
content_type = response.headers.get('Content-Type')
file_extension = mimetypes.guess_extension(content_type)

# save the document to a file
with open(f"{document_name}{file_extension}", "wb") as f:
    f.write(response.content)


# close the driver
driver.quit()

