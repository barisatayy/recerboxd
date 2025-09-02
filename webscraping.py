from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def get_user_data(username1, username2):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    browser = webdriver.Chrome(options=options)
    wait = WebDriverWait(browser, 10)

    all_users_watched_data = {}
    all_users_watchlist_data = {}
    usernames = [username1, username2]

    for user in usernames:
        page = 1
        user_watched_data = []
        while True:
            url = f"https://letterboxd.com/{user}/films/page/{page}/"
            browser.get(url)
            try:
                film_divs = wait.until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.react-component[data-item-name]")))
            except TimeoutException:
                break
            if not film_divs: break
            for film_div in film_divs:
                name = film_div.get_attribute("data-item-name")
                rating = None
                try:
                    rating_element = film_div.find_element(By.XPATH, '../p/span[contains(@class, "rating")]')
                    rating = rating_element.text
                except NoSuchElementException:
                    pass
                user_watched_data.append((name, rating))
            page += 1
        all_users_watched_data[user] = user_watched_data

        page = 1
        user_watchlist_films = []
        while True:
            url = f"https://letterboxd.com/{user}/watchlist/page/{page}/"
            browser.get(url)
            try:
                film_divs = wait.until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.react-component[data-item-name]")))
            except TimeoutException:
                break
            if not film_divs: break
            for film_div in film_divs:
                name = film_div.get_attribute("data-item-name")
                user_watchlist_films.append(name)
            page += 1
        all_users_watchlist_data[user] = user_watchlist_films

    user1_watched = all_users_watched_data.get(username1, [])
    user2_watched = all_users_watched_data.get(username2, [])
    user1_watchlist_set = set(all_users_watchlist_data.get(username1, []))
    user2_watchlist_set = set(all_users_watchlist_data.get(username2, []))

    user1_watched_names = {film[0] for film in user1_watched}
    user2_watched_names = {film[0] for film in user2_watched}
    common_watched_films = sorted(list(user1_watched_names.intersection(user2_watched_names)))

    user1_ratings = {film[0]: film[1] for film in user1_watched if film[1] is not None}
    user2_ratings = {film[0]: film[1] for film in user2_watched if film[1] is not None}

    same_rated_films = []
    highly_rated_common_films = []
    for film_name in common_watched_films:
        if film_name in user1_ratings and film_name in user2_ratings:
            if user1_ratings[film_name] == user2_ratings[film_name]:
                same_rated_films.append(f"{film_name}: {user1_ratings[film_name]}")
                if len(user1_ratings[film_name]) >= 4:
                    highly_rated_common_films.append(film_name)

    common_watchlist_films = sorted(list(user1_watchlist_set.intersection(user2_watchlist_set)))
    browser.quit()

    return {
        'ortak_filmler': common_watched_films,
        'ayni_puanli_filmler': same_rated_films,
        'ortak_watchlist': common_watchlist_films,
        'user1_watched_full': user1_watched_names,
        'user2_watched_full': user2_watched_names,
        'user1_watchlist_full': list(user1_watchlist_set),
        'user2_watchlist_full': list(user2_watchlist_set),
        'highly_rated_common': highly_rated_common_films
    }
