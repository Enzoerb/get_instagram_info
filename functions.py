from selenium.common.exceptions import NoSuchElementException
from user_info import USERNAME, USER_PASSWORD
from os.path import join
from time import sleep


def login(driver):
    username_input = driver.find_element_by_name("username")
    password_input = driver.find_element_by_name("password")
    enter_button = driver.find_element_by_xpath('//button[@class="sqdOP  L3NKy   y3zKF     "]')

    username_input.clear()
    username_input.send_keys(USERNAME)
    password_input.clear()
    password_input.send_keys(USER_PASSWORD)
    enter_button.click()


def close_notifications(driver):
    try:
        not_button = driver.find_element_by_xpath('//button[@class="aOOlW   HoLwm "]')
        not_button.click()
    except NoSuchElementException:
        pass


def logout(driver):
    user_page = driver.find_element_by_xpath('//a[@class="_2dbep qNELH kIKUG"]')
    user_page_link = user_page.get_attribute("href")
    driver.get(user_page_link)
    engine = driver.find_element_by_xpath('//button[@class="wpO6b "]')
    engine.click()
    buttons = driver.find_elements_by_xpath('//button[@class="aOOlW   HoLwm "]')
    logout_button = buttons[-2]
    logout_button.click()


def get_visible_post_links(driver):
    links = set()
    img_div = driver.find_elements_by_xpath('//div[@class="v1Nh3 kIKUG  _bz0w"]')
    for i in img_div:
        link = i.find_element_by_css_selector('a').get_attribute('href')
        links.add(link)
    return links


def get_posts_links(driver):

    links = set()
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep_time = 0
        while sleep_time < 15:
            sleep_time += 1
            if sleep_time == 10:
                driver.execute_script("window.scrollTo(0, 0);")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(1)
            scroll_height = driver.execute_script("return document.body.scrollHeight")
            links = links.union(get_visible_post_links(driver))
            if scroll_height != last_height:
                break
        else:
            break

        last_height = scroll_height

    return links


def get_post_likes(driver):
    likes = None
    like_button = driver.find_elements_by_xpath('//button[@class="sqdOP yWX7d     _8A5w5    "]')
    for element in like_button:
        likes_span = element.find_element_by_css_selector('span')
        likes = likes_span.get_attribute("innerHTML")
        if likes.isnumeric():
            break
    if likes == None:
        button = driver.find_element_by_xpath('//span[@class="vcOH2"]')
        button.click()
        likes_element = driver.find_element_by_xpath('//div[@class="vJRqr"]')
        likes_span = likes_element.find_element_by_css_selector('span')
        likes = likes_span.get_attribute("innerHTML")

    return likes


def get_post_date(driver):
    time_element = driver.find_element_by_xpath('//time[@class="_1o9PC Nzb55"]')
    date = time_element.get_attribute('title')
    return date


def get_post_views(driver):
    views = None
    video_divs = driver.find_elements_by_xpath('//div[@class="kPFhm B1JlO OAXCp "]')
    if len(video_divs) == 1:
        type_media = 'video'
        try:
            views_element = driver.find_element_by_xpath('//span[@class="vcOH2"]')
            views_span = views_element.find_element_by_css_selector('span')
            views = views_span.get_attribute("innerHTML")
        except NoSuchElementException:
            pass
    else:
        type_media = 'photo'
    return views, type_media


def get_post_info(driver):
    date = get_post_date(driver)
    likes = get_post_likes(driver)
    views, type_media = get_post_views(driver)
    return views, likes, type_media, date
