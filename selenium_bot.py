from selenium import webdriver
from functions import login, logout, close_notifications, get_posts_links, get_post_info
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
    print(len(post_links), 'posts')
    with open('posts_info.txt', 'w') as posts_info:
        collected = 0
        displayed = set()
        for link in post_links:
            collected += 1
            driver.get(link)
            driver.implicitly_wait(1)
            views, likes, type_media, date = get_post_info(driver)
            posts_info.write(f'link: {link}\n')
            posts_info.write(f'type: {type_media}\n')
            posts_info.write(f'date: {date}\n')
            if likes != None:
                posts_info.write(f'likes: {likes}\n')
            if views != None:
                posts_info.write(f'views: {views}\n')
            posts_info.write('\n')
            percentage = int(100*collected / len(post_links))
            if percentage % 5 == 0 and percentage not in displayed:
                print(f'collected {percentage}%')
                displayed.add(percentage)
end = datetime.now()
print(end-beggining)
