#!/usr/bin/env python3
import time
import re
import pyautogui

from database import JobsDB

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


WORDS_REGEX = re.compile("[a-z]+")


class JobsPage:

    def __init__(self, db):
        self.db = db
        self.words_set = set()
        self.browser = None
        self.username = "maximilianorom7@gmail.com"
        self.password = "masterjobs01"
        self.login_username_id = "username_username"
        self.login_username_button_id = "username_password_continue"
        self.login_password_id = "password_password"
        self.login_password_button_id = "password_control_continue"

    def open_browser(self):
        self.browser = webdriver.Chrome()
        self.browser.get('https://www.upwork.com/ab/account-security/login')
        self.browser.maximize_window()

    def write_textbox_click(self, textbox_id, text, button_id):
        username_box = self.browser.find_element_by_id(textbox_id)
        username_box.send_keys(text)
        time.sleep(3)
        continue_button = self.browser.find_element_by_id(button_id)
        continue_button.click()
        time.sleep(3)

    def write_username(self):
        self.write_textbox_click(
            self.login_username_id,
            self.username,
            self.login_username_button_id
        )

    def write_password(self):
        self.write_textbox_click(
            self.login_password_id,
            self.password,
            self.login_password_button_id
        )

    def login(self):
        self.write_username()
        self.write_password()

    def goto_search(self):
        self.browser.get('https://www.upwork.com/ab/jobs/search/?sort=recency')
        time.sleep(3)

    def click_filters(self):
        filter_button = self.browser.find_element_by_xpath(
            "//div[contains(@class, 'toggle-filters-button') and contains(string(), 'Filters ')]"
        )
        filter_button.click()
        time.sleep(2)

    def set_fixed_price(self):
        fixed_price_button = self.browser.find_element_by_xpath("//span[contains(string(), 'Fixed Price')]")
        fixed_price_button.click()
        time.sleep(2)
        
    def set_category(self):
        category_box = self.browser.find_element_by_id("category-filter")
        category_box.click()
        time.sleep(2)
        category_box.send_keys("WEB, MOBILE & SOFTWARE DEV")
        time.sleep(2)
        first_option = self.browser.find_element_by_xpath("//div[contains(@class, 'dropdown-header')]")
        first_option.click()
        time.sleep(2)

    def set_search_box(self):
        search_box = self.browser.find_element_by_id("search-box-el")
        search_box.send_keys("python")
        search_box.click()
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)

    def setup_filters(self):
        self.click_filters()
        self.set_fixed_price()
        # self.set_category()
        self.set_search_box()
        self.click_filters()

    def main(self):
        self.login()
        self.goto_search()
        self.setup_filters()
        self.read_posts()

    def extract_post_body(self, url):
        post_title = ""
        post_body = ""
        try:
            post_title = self.browser.find_element_by_xpath(
                "//*[@id='job-details-slider']/div/div/job-details/ng-transclude/div[2]/div/div/header/h2"
            ).text
            post_body = self.browser.find_element_by_xpath(
                "//*[@id='job-details-slider']/div/div/job-details/ng-transclude/div[2]/div/div/section[2]/div/div"
            ).text
        except NoSuchElementException as error:
            print(error)
            pass
        else:
            text = f"{post_title} {post_body}"
            text = text.lower()
            words = re.findall(WORDS_REGEX, text)
            words = ' '.join(words)
            if words not in self.words_set:
                self.words_set.add(words)
                self.db.save_post(url, post_title, post_body, words)
                self.db.conn.commit()

    def read_posts(self):
        while True:
            postings = self.browser.find_elements_by_xpath("//*[@id='layout']//section//h4/a")
            for post in postings:
                url = post.get_attribute("href")
                if not url.startswith("http"):
                    continue
                if self.db.is_visited(url):
                    continue
                post.click()
                time.sleep(7)
                self.extract_post_body(url)
                pyautogui.click(150, 300)
                time.sleep(3)
            next_button = self.browser.find_element_by_xpath(
                 "//*[@id='layout']/div[2]/div/div[2]/div/job-list-footer/footer/div[2]/div/ul/li[9]/a/span[1]"
            )
            next_button.click()
            time.sleep(10)

"""
jobs_db = main.JobsDB()
jobs_page = main.JobsPage(jobs_db)
jobs_page.open_browser()
jobs_page.login()
jobs_page.goto_search()
jobs_page.setup_filters()
jobs_page.read_posts()
"""
# //*[@id="layout"]/div[2]/div/div[2]/header/div[1]/div[2]/span[1]/div

def main():
    jobs_db = JobsDB()
    jobs_page = JobsPage(jobs_db)
    jobs_page.open_browser()
    jobs_page.main()

if __name__ == "__main__":
    main()