from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
import time
import random
import csv
import re
#
# already_follow = []
#
# with open('follower.csv', 'r') as csv_file:
#     csv_reader = csv.reader(csv_file)
#     for row in csv_reader:
#         if len(row) != 0:
#             for element in row:
#                 already_follow.append(element)

regex = re.compile('[^a-zA-Z]')


class InstagramBot:
    def __init__(self, username, password):
        self.browser = webdriver.Chrome("chromedriver.exe")

        self.username = username
        self.password = password

        self.browser.delete_all_cookies()
        self.browser.maximize_window()

    def wait_for_object(self, type, string):
        return WebDriverWait(self.browser, 3).until(ec.presence_of_element_located((type, string)))

    def wait_for_objects(self, type, string):
        return WebDriverWait(self.browser, 3).until(ec.presence_of_all_elements_located((type, string)))

    def login(self):
        self.browser.get("https://www.instagram.com")

        window = self.wait_for_object(By.CSS_SELECTOR, '.aOOlW.bIiDR')
        window.click()

        inputs = self.wait_for_objects(By.CSS_SELECTOR, '._2hvTZ.pexuQ.zyHYP')
        inputs[0].send_keys(self.username)
        inputs[1].send_keys(self.password)

        time.sleep(1)

        inputs[1].send_keys(Keys.ENTER)

        time.sleep(2)

    def like_hashtag(self, hashtag, number_of_likes):
        time.sleep(2)
        self.browser.get(f"https://www.instagram.com/explore/tags/{hashtag}/")

        pictures = self.wait_for_objects(By.CSS_SELECTOR, '._9AhH0')
        pictures[0].click()

        for i in range(0, number_of_likes):
            likes = self.wait_for_objects(By.CSS_SELECTOR, 'svg[aria-label="Gefällt mir"]')
            likes[0].click()

            time.sleep(1)

            if i != number_of_likes-1:
                next_window = self.wait_for_object(By.CSS_SELECTOR, '._65Bje.coreSpriteRightPaginationArrow')
                next_window.click()

                time.sleep(random.randint(2, 10))

    def follow_followers(self, root_name, number_follower):
        all_follower = []

        time.sleep(2)

        self.browser.get(f"https://www.instagram.com/{root_name}/")

        time.sleep(2)

        followers = self.wait_for_objects(By.CSS_SELECTOR, '.-nal3')
        followers[1].click()

        for i in range(1, number_follower + 1):
            time.sleep(2)

            src1 = self.wait_for_object(By.XPATH, f'/html/body/div[5]/div/div/div[2]/ul/div/li[{i}]')
            self.browser.execute_script("arguments[0].scrollIntoView();", src1)

            time.sleep(1)

            follower_name = src1.text.split()[0]

            if follower_name in already_follow:
                number_follower += 1
                continue
            else:
                all_follower.append(follower_name)

        with open('follower.csv', 'a') as csv_file:
            csv_writer = csv.writer(csv_file)

            csv_writer.writerow(all_follower)

        for follower in all_follower:
            self.browser.get(f"https://www.instagram.com/{follower}/")

            time.sleep(5)

            subscribe_buttons = self.wait_for_objects(By.XPATH, '//button[text()="Abonnieren"]')
            subscribe_buttons[0].click()

            time.sleep(5)

    def unfollow_users(self, number_unfollow):
        counter = 0
        scroll = 1000
        links = []

        time.sleep(4)

        self.browser.get(f"https://www.instagram.com/{self.username}/")

        time.sleep(2)

        window = self.wait_for_objects(By.CSS_SELECTOR, '.-nal3')
        window[2].click()

        while len(links) < number_unfollow:
            window = self.wait_for_objects(By.CSS_SELECTOR, '.FPmhX.notranslate._0imsa')
            for link in window:
                links.append(link.get_attribute('href'))
            self.browser.execute_script(f"document.querySelector('.isgrP').scrollTo(0, {scroll})")
            scroll += 1000
            time.sleep(2)

        for link in links:
            if counter == 3:
                break

            self.browser.get(f'{link}')

            time.sleep(2)

            unfollow_btn = self.wait_for_object(By.CSS_SELECTOR, '._5f5mN.-fzfL._6VtSN.yZn4P')
            unfollow_btn.click()

            time.sleep(2)

            confirmation = self.wait_for_object(By.CSS_SELECTOR, '.aOOlW.-Cab_')
            confirmation.click()

            time.sleep(2)

            counter += 1

    def comment_posts(self, number_of_comments, hashtag_origin, post_hashtag):
        time.sleep(2)

        random_comments = []
        self.browser.get(f"https://www.instagram.com/explore/tags/{hashtag_origin}/")

        pictures = self.wait_for_objects(By.CSS_SELECTOR, '._9AhH0')
        pictures[0].click()

        time.sleep(2)

        for i in range(0, number_of_comments):
            comments = self.wait_for_objects(By.XPATH, '//div[contains(@class, "C4VMK")]/span')
            comment = regex.sub('', comments[1].text)
            random_comments.append(comment)

            time.sleep(1)

            if i != number_of_comments - 1:
                next_window = self.wait_for_object(By.CSS_SELECTOR, '._65Bje.coreSpriteRightPaginationArrow')
                next_window.click()

                time.sleep(random.randint(2, 10))

        self.browser.get(f"https://www.instagram.com/explore/tags/{post_hashtag}/")

        pictures = self.wait_for_objects(By.CSS_SELECTOR, '._9AhH0')
        pictures[0].click()

        time.sleep(2)

        for i in range(0, number_of_comments):
            comment_box = self.wait_for_object(By.CSS_SELECTOR, '.Ypffh')
            comment_box.click()
            comment_box = self.wait_for_object(By.CSS_SELECTOR, '.Ypffh')
            comment_box.send_keys(random_comments[i])

            time.sleep(2)

            post_button = self.wait_for_object(By.XPATH, '//button[text()="Posten"]')
            post_button.click()

            time.sleep(random.randint(2, 10))

            if i != number_of_comments - 1:
                next_window = self.wait_for_object(By.CSS_SELECTOR, '._65Bje.coreSpriteRightPaginationArrow')
                next_window.click()

                time.sleep(random.randint(2, 10))


bot = InstagramBot(username="maketheworldgreatagaiin", password="save_password3")
bot.login()
# bot.like_hashtag('lifestyle', 3)
# bot.follow_followers("therock", 3)
# bot.unfollow_users(3)
bot.comment_posts(1, 'lifestyle', 'programminghumor')
