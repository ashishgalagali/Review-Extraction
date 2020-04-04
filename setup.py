import action as action
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

from selenium.webdriver import ActionChains


def scroll_down(browser):
    """A method for scrolling the page."""
    
    # Get scroll height.
    last_height = browser.execute_script("return document.body.scrollHeight")
    
    while True:
        
        # Scroll down to the bottom.
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait to load the page.
        time.sleep(2)
        
        # Calculate new scroll height and compare with last scroll height.
        new_height = browser.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            break
        
        last_height = new_height


# time.sleep(10)
def get_reviews_without_responses(reviewEle):
    reviewer_name = reviewEle.find_element_by_xpath(".//span[@class='X43Kjb']")
    reviewer_time = reviewEle.find_element_by_xpath(".//span[@class='p2TkOb']")
    fullRating = reviewEle.find_element_by_xpath(".//div[@class='pf5lIe']").find_element_by_css_selector(
        'div').get_attribute('aria-label')
    numericalRating = fullRating.split()
    if reviewEle.find_element_by_xpath(".//span[@jsname='bN97Pc']").get_attribute('style') == 'display: none;':
        review = reviewEle.find_element_by_xpath(".//span[@jsname='fbQN7e']")
    else:
        review = reviewEle.find_element_by_xpath(".//span[@jsname='bN97Pc']")
    print(
        numericalRating[
            1] + "\t" + reviewer_name.text + "\t" + reviewer_time.text + "\t" + review.text + "\t" + "0" + "\t" + "" + "\t" + "" + "\t" +
        "")


def get_reviews_with_responses(reviewEle, developer_responses):
    reviewer_name = reviewEle.find_element_by_xpath(".//span[@class='X43Kjb']")
    reviewer_time = reviewEle.find_element_by_xpath(".//span[@class='p2TkOb']")
    fullRating = reviewEle.find_element_by_xpath(".//div[@class='pf5lIe']").find_element_by_css_selector(
        'div').get_attribute('aria-label')
    numericalRating = fullRating.split()
    response_time = developer_responses.find_element_by_xpath(".//span[@class='p2TkOb']")
    response_developer = developer_responses.find_element_by_xpath(".//span[@class='X43Kjb']")
    
    if reviewEle.find_element_by_xpath(".//span[@jsname='bN97Pc']").get_attribute('style') == 'display: none;':
        review = reviewEle.find_element_by_xpath(".//span[@jsname='fbQN7e']")
    else:
        review = reviewEle.find_element_by_xpath(".//span[@jsname='bN97Pc']")
    print(
        numericalRating[
            1] + "\t" + reviewer_name.text + "\t" + reviewer_time.text + "\t" + review.text + "\t" + "1" + "\t" + response_developer.text + "\t" + response_time.text + "\t" +
        developer_responses.text.split("\n")[1])


def get_reviews(driver, url):
    option = webdriver.ChromeOptions()
    option.add_argument(" — incognito")
    
    # Give the path of the chrome driver downloaded on your local machine
    browser = webdriver.Chrome(driver)
    
    browser.get(url)
    
    browser.maximize_window()
    
    reviewer_name = browser.find_elements_by_xpath("//span[@class='X43Kjb']")
    
    for x in reviewer_name:
        while len(reviewer_name) < 500:
            scroll_down(browser)
            reviewer_name = browser.find_elements_by_xpath("//span[@class='X43Kjb']")
    
    for x in browser.find_elements_by_xpath(".//button[@class='LkLjZd ScJHi OzU4dc  ']"):
        ActionChains(browser).click(x).perform()
    
    reviews = browser.find_elements_by_xpath("//div[@class='zc7KVe']")
    print(
        "RATING\tREVIEWER_NAME\tREVIEW_DATE\tREVIEW_TEXT\tHAS_RESPONSE\tDEVELOPER_NAME\tRESPONSE_DATE\tDEVELOPER_RESPONSE")
    
    for reviewEle in reviews:
        try:
            developer_responses = reviewEle.find_element_by_xpath(".//div[@class='LVQB0b']")
        except NoSuchElementException:
            get_reviews_without_responses(reviewEle)
            continue
        if developer_responses:
            get_reviews_with_responses(reviewEle, developer_responses)


if __name__ == '__main__':
    get_reviews('/Users/raj.g/Downloads/chromedriver',
                "https://play.google.com/store/apps/details?id=de.dfki.appdetox&hl=en_US&showAllReviews=true")
