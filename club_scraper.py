import csv
import re
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(options=options)

if __name__ == '__main__':

    SITE = 'https://wpi.campuslabs.com'
    ALL_CLUBS = '/engage/organizations'
    TIMEOUT = 3

    driver.get(SITE + ALL_CLUBS)

    displayed_clubs = 0
    while displayed_clubs < 262:
        # Ensure that "Load More" button has loaded
        load_more_btn = WebDriverWait(driver, TIMEOUT).until(ec.presence_of_element_located(
            (By.XPATH, "/html/body/div[2]/div/div/div/div/div[2]/div/div[2]/div/div[2]/div[2]/button")))
        load_more_btn.click()

        found_clubs = driver.find_elements_by_class_name("DescriptionExcerpt")
        displayed_clubs = len(found_clubs)

    club_links = []
    all_links = driver.find_elements_by_tag_name('a')
    for link in all_links:
        href = link.get_attribute('href')
        if "/engage/organization/" in href:
            club_links.append(href)

    contact_info = []
    for club_link in club_links:
        driver.get(club_link)
        try:
            email_div = driver.find_element_by_xpath(
                "/html/body/div[2]/div/div/div/div/div/div[1]/div[1]/div/div[3]/div/div[2]/div[2]")
        except NoSuchElementException:
            continue
        email = email_div.get_attribute("innerText")
        email = re.findall(r'[\w\.-]+@[\w\.-]+(?:\.[\w]+)+', email)  # filter down to just the email

        if len(email) > 0:
            email = email[0]

        group_name_h1 = driver.find_element_by_xpath(
            "/html/body/div[2]/div/div/div/div/div/div[1]/div[1]/div/div[1]/h1")
        group_name = group_name_h1.get_attribute("innerText")

        print([group_name, email])
        contact_info.append([group_name, email])

    with open('club_contact_info.csv', 'w', newline='') as csvfile:
        header = ['Group Name', 'Email']
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for row in contact_info:
            writer.writerow(row)

    driver.quit()

