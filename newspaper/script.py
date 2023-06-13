import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv


class SiteRequest:

    def __init__(self):
        self.collection = []
        self.add_to_collection()
        self.login = 'jorddyishere@gmail.com'
        self.password = 'QweQwe!23)'

    def add_to_collection(self):
        file_name = 'newspapers_search_terms.xlsx'
        sheet = 'Sheet1'

        df = pd.read_excel(io=file_name, sheet_name=sheet)
        print(df.values)
        vals = list(map(list, df.values))
        for values in vals:
            self.collection.append([x for x in values if not isinstance(x, float)])

    def get_values(self):
        driver = webdriver.Chrome()
        for lst in self.collection:
            driver.get(f'https://www.newspapers.com/search/?query={lst[0]}&dr_year={lst[1]}-{lst[2]}')
            time.sleep(3)

            sign_in = driver.find_element(By.XPATH, '/html/body/div[1]/div/header/nav/div[2]/div/div/ul/li[1]/a')
            sign_in.click()
            time.sleep(3)

            s_in = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[1]/div/div/div/div/p[2]/a')
            s_in.click()
            time.sleep(3)

            s_i = driver.find_element(By.XPATH, '//*[@id="signinlink"]')
            s_i.click()
            time.sleep(3)

            log = driver.find_element(By.XPATH, '//*[@id="username"]')
            log.send_keys(self.login)

            pas = driver.find_element(By.XPATH, '//*[@id="password"]')
            pas.send_keys(self.password)

            but = driver.find_element(By.XPATH, '//*[@id="modal-SignInModal"]/div/div[2]/div/div[3]/div/button')
            but.click()
            time.sleep(10)

            driver.get(f'https://www.newspapers.com/search/?query={lst[0]}&dr_year={lst[1]}-{lst[2]}')

            # for i in range(5):
            #     show_more = driver.find_element(By.XPATH,'//*[@id="content"]/div/div[1]/div/div[3]/div/div[2]/div/button')
            #     show_more.click()
            #     time.sleep(5)

            time.sleep(5)

            titles = driver.find_elements(By.XPATH, "//h2[@class='h5 mb-1']")
            page_numbers = driver.find_elements(By.XPATH, "//p[@class='text-muted text-uppercase text-small mb-1']")
            locations = driver.find_elements(By.XPATH, "//p[@title='Location']")
            dates = driver.find_elements(By.XPATH, "//p[@class='ml-n1 mb-1 text-dark']")
            time.sleep(3)

            print([[x.text for x in titles], [x.text for x in page_numbers], [x.text for x in locations], [x.text for x in dates]])

# s = SiteRequest()
# s.get_values()

res = [['The San Francisco Examiner', 'The News and Observer', 'The Spokesman-Review', 'The Spokesman-Review', 'The San Francisco Examiner', 'Petaluma Argus-Courier', 'The Times', 'The Daily Item', 'The San Francisco Examiner', 'El Paso Herald-Post'], ['PAGE 15', 'PAGE 12', 'PAGE 13', 'PAGE 8', 'PAGE 3', 'PAGE 2', 'PAGE 11', 'PAGE 3', 'PAGE 3', 'PAGE 8'], ['San Francisco, California', 'Raleigh, North Carolina', 'Spokane, Washington', 'Spokane, Washington', 'San Francisco, California', 'Petaluma, California', 'San Mateo, California', 'Lynn, Massachusetts', 'San Francisco, California', 'El Paso, Texas'], ['Sunday, December 07, 1969', 'Monday, December 01, 1969', 'Thursday, December 18, 1969', 'Thursday, December 18, 1969', 'Monday, December 08, 1969', 'Monday, December 22, 1969', 'Saturday, December 27, 1969', 'Saturday, December 27, 1969', 'Wednesday, December 24, 1969', 'Saturday, December 27, 1969']]



new_res = []

for i in range(len(res[0])):
    new_res.append([res[0][i], res[1][i], res[2][i], res[3][i]])

df = pd.DataFrame(new_res, columns=['Title', 'Page Number', 'Location', 'Date'])
# with open(f'newspaper_articles_search_term_date_to_search_start_date_to_search_end.csv', 'w') as csvfile:
#     spam_writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     counter = 0
#     for i in range(len(res[0])):
#         spam_writer.writerow([res[0][i], res[1][i], res[2][i], res[3][i]])

df.to_excel('newspaper_articles_search_term_date_to_search_start_date_to_search_end.xlsx', sheet_name='Sheet1')