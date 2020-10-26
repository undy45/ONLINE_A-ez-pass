from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from time import sleep

import config


class EasyPass:
    def __init__(self):
        self.driver = webdriver.Chrome(config.path_to_driver)
        self.login()
        self.tests_to_do = self.get_list_of_tests_from_file()
        self.list_of_tests_url = self.get_list_of_test_url()
        self.open_list_of_tests()
        self.solve_tests()

    def solve_tests(self):
        for test in self.tests_to_do:
            link = self.get_test_link(test)
            if link is None:
                continue
            self.driver.get(link)
            self.find(By.LINK_TEXT, "Spustit nový odpovědník").click()
            self.find(By.XPATH, "//button[contains(text(), 'Odevzdat')]").click()
            self.find(By.LINK_TEXT, "Prohlídka").click()
            answers = self.driver.find_elements_by_xpath("//span[@class='ok']")
            answers = [answer.text[1:-1].split(',')[0].strip() for answer in answers]
            self.find(By.XPATH, "//a[contains(text(), 'Zpět')]").click()
            self.find(By.LINK_TEXT, "Spustit nový odpovědník").click()
            cells = self.driver.find_elements_by_xpath("//input[@type='text']")
            for i, cell in enumerate(cells):
                cell.send_keys(answers[i])
            self.find(By.XPATH, "//button[contains(text(), 'Odevzdat')]").click()
            sleep(1)
            self.open_list_of_tests()

    def get_list_of_test_url(self):
        self.driver.get(config.student_page)
        self.find(By.XPATH, "//a[span/strong[contains(text(), 'ONLINE_A')]]").click()
        self.find(By.XPATH, ".//div[@class='row student_row_b']/div/a")
        link = self.driver.find_elements_by_xpath(".//div[@class='row student_row_b']/div/a")[-1].get_attribute("href")
        return link

    def open_list_of_tests(self):
        self.driver.get(self.list_of_tests_url)

    def login(self):
        self.driver.get(config.login_url)

        elem = self.driver.find_element_by_name("credential_0")
        elem.send_keys(config.UCO)

        elem = self.driver.find_element_by_name("credential_1")
        elem.send_keys(config.primary_password)
        elem.send_keys(Keys.RETURN)

    def find(self, by_method, pattern, wait_time=10):
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((by_method, pattern))
            )
            return element
        except:
            self.driver.quit()

    def get_list_of_tests_from_file(self):
        with open("tests.txt", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines()]

    def get_test_link(self, test):
        element = self.find(By.XPATH, f".//tr[td/a[contains(text(), '{test}')]]")
        try:
            points = element.find_element_by_xpath("td/div/div/span[@class='pozn_blok']")
            if points.text != "*0":
                return
            test_link = points.find_element_by_xpath("../../../../td[@class='uzel']/a").get_attribute("href")
            return test_link
        except NoSuchElementException:
            test_link = element.find_element_by_xpath("td[@class='uzel']/a").get_attribute("href")
            return test_link


a = EasyPass()
sleep(5)
a.driver.quit()
