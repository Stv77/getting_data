from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import pickle
import time

chrome_options = webdriver.ChromeOptions()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
chrome_options.add_argument('--user-agent='+userAgent)
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=r'D:\Python\FiverrCrawler\env1\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe')
driver.get('https://www.____.com/search/gigs?query=android%20developer&source=top-bar&search_in=everywhere&search-autocomplete-original-term=android%20developer')
time.sleep(5)
driver.maximize_window()

# running the cookies - uncomment if cookies.pkl exists
time.sleep(100)
pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))

cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)

# containers that will contain the texts (used to convert to csv format)
name_container = "".split()
text_container = "".split()
rating_container = "".split()

# filtering words to filter out the text container
filtering = ['Categories', 'About', 'Support', 'Community', 'More From Fiverr']

time.sleep(5)

while True:
    try:
        # names
        name = driver.find_elements_by_class_name("seller-name")
        for names in name:
            name_container.append(names.text)
        time.sleep(7)

        # titles
        text_display = driver.find_elements_by_class_name("text-display-7")
        for texts in text_display:
            text_container.append(texts.text)
        time.sleep(8)

        # ratings
        rating_texts = driver.find_elements_by_class_name("content-info")
        for ratings in rating_texts:
            rating_container.append(ratings.text)
        time.sleep(10)

        # scrolling & clicking to a certain xpath
        driver.execute_script("arguments[0].scrollIntoView(true);", WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="pagination"]/li[12]/a'))))
        driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pagination"]/li[12]/a'))))
        chrome_options.add_argument('--user-agent='+userAgent)
        time.sleep(5)
        
        #trying to get a new chrome user agent
        chrome_options = webdriver.ChromeOptions()
        ua = UserAgent()
        userAgent = ua.random
        print(userAgent)
        chrome_options.add_argument('--user-agent='+userAgent)

        #hit escape to hinder a pop up message
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(2)
        continue
    except NoSuchElementException or TimeoutException:
        # filtering out text container
        filter_data = [x for x in text_container if
              all(y not in x for y in filtering)]
        
        # save the data into csv from the lists using panda (uncomment to not save to csv)      
        dict = {'names': name_container, 'titles': filter_data, 'ratings': rating_container}
        df = pd.DataFrame(dict)
        df.to_csv('android_developer.csv')
        break
