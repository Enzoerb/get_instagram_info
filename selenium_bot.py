from selenium import webdriver
from functions import login, logout, close_notifications, get_posts_links, get_post_info, get_all_midia
from datetime import datetime
from user_info import USERNAME

beggining = datetime.now()
with webdriver.Chrome() as driver:
    driver.get("https://www.instagram.com/")
    driver.implicitly_wait(5)
    login(driver)
    driver.implicitly_wait(5)
    close_notifications(driver)
    driver.get(f"https://www.instagram.com/{USERNAME}")
    post_links = get_posts_links(driver)
    with open('posts_info.csv', 'w') as posts_info:
        collected = 0
        displayed = set()
        for link in post_links:
            collected += 1
            driver.get(link)
            driver.implicitly_wait(1)
            views, likes, date = get_post_info(driver)
            all_midia = get_all_midia(driver)
            posts_info.write(f'{link};')
            posts_info.write(f'{all_midia};')
            posts_info.write(f'{date};')
            posts_info.write(f'{likes};')
            posts_info.write(f'{views}')
            posts_info.write('\n')
            percentage = int(100*collected / len(post_links))
            if percentage % 5 == 0 and percentage not in displayed:
                print(f'collected {percentage}%')
                displayed.add(percentage)
end = datetime.now()
print(end-beggining)
