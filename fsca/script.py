import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Read the Excel file
df = pd.read_excel('FSPExport.xlsx')

# Extract the FSP numbers
fsp_numbers = df['FSPno'].tolist()

# Set up the Selenium WebDriver
driver = webdriver.Chrome()  # Update with the path to your ChromeDriver executable

# Iterate over the FSP numbers
for fsp_number in fsp_numbers:
    # Load the search page
    driver.get('https://www.fsca.co.za/Fais/Search_FSP.htm')

    # Wait for the search field to be visible
    search_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='Search_FSP_No']"))
    )

    # Enter the FSP number and submit the form
    search_field.send_keys(fsp_number)
    driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

    # Wait for the details link to be visible and click on it
    details_link = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//input[@name="bDetails"]'))
    )
    details_link.click()

    # Wait for the Representatives link to be visible and click on it
    representatives_link = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//h2[@class="HeaderText"]'))
    )

    elements = driver.find_elements(By.XPATH, '//h2[@class="HeaderText"]')

    with open(f'{fsp_number}.txt', 'a') as file:
        table = driver.find_element(By.XPATH, "//table[@border=2]")
        file.write(table.text)

        elements[0].click()
        time.sleep(1)
        contact_information = driver.find_element(By.XPATH, "//div[@id='Contact_Info']")
        file.write(contact_information.text)

        elements[1].click()
        time.sleep(1)
        compliance_officers = driver.find_element(By.XPATH, "//div[@id='ComplianceOfficers']")
        file.write(contact_information.text)


        elements[3].click()
        time.sleep(1)
        key_individuals = driver.find_element(By.XPATH, "//div[@id='Key_Individuals']")
        file.write(key_individuals.text)

        elements[4].click()
        time.sleep(1)
        sole_proprietors = driver.find_element(By.XPATH, "//div[@id='Sole_Proprietors']")
        file.write(sole_proprietors.text)

        elements[5].click()
        time.sleep(1)
        products_approved = driver.find_element(By.XPATH, "//div[@id='Products_Approved']")
        file.write(products_approved.text)

        elements[2].click()
        time.sleep(1)
        button = driver.find_element(By.XPATH, '//input[@name="bSearch"]')
        button.click()
        time.sleep(5)
        representatives = driver.find_element(By.XPATH, '//table[@cellpadding="3"]//tbody')
        file.write(representatives.text)


# Close the browser
driver.quit()