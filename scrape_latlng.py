# Selenium-wire is used for webdriver instead of Selenium, because we want to monitor
# the network calls and capture the HTTP requests and response made by the website

from seleniumwire import webdriver
from seleniumwire.utils import decode
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import time
import json

firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument("--private")
driver = webdriver.Firefox(options=firefox_options)

location = "manila"

# Visiting the base_url, and searching for a place in Manila, and getting the list of
# all restaurants which can deliver food here
driver.get('https://food.grab.com/ph/en/')
search_input = driver.find_element_by_xpath("//*[@class='ant-input']")
search_button = driver.find_element_by_xpath("//*[@class='ant-btn submitBtn___2roqB ant-btn-primary']")

time.sleep(10)
search_input.send_keys(location)

time.sleep(10)
search_input.send_keys(Keys.ENTER)

time.sleep(10)
search_button.click()

time.sleep(10)

restaurant_list = []
# After the Restaurant List page is loaded, we can get the latitude and longitude
# of first 8 restaurants from the __NEXT_DATA__

soup = bs(driver.page_source, "html.parser")
next_data = json.loads(soup.find(id="__NEXT_DATA__").text)
initial_restaurant_dict = next_data['props']['initialReduxState']['pageRestaurantsV2']['entities']['restaurantList']
for restaurant_id, restaurant in initial_restaurant_dict.items():
    _data = {}
    _data['id'] = restaurant['id']
    _data['name'] = restaurant['name']
    _data['latitude'] = restaurant['latitude']
    _data['longitude'] = restaurant['longitude']

    restaurant_list.append(_data)


# Since we want latlng all the restaurants on this page so we need to click
# Load More till we load to the end of this page

# Since the latlng of only first 8 restaurants are present in __NEXT_DATA__ but we want
# The latlng of all the restaurants on this page, so we need to monitor the requests made
# on clicking Load More button to 'https://portal.grab.com/foodweb/v2/search'
# The response of this request will contain the latlng of next 8 restaurants

# We also need to sleep between clicks to prevent being detected as bots

load_more_button = driver.find_element_by_xpath("//*[@class='ant-btn ant-btn-block']")
time.sleep(10)

click_num = 1
while True:
    try:
        load_more_button.click()

        print(f'Click Number : {click_num}')

        if(click_num % 40 == 0):
            time.sleep(600)
        elif(click_num % 15 == 0):
            time.sleep(300)
        else:
            time.sleep(10)

        click_num += 1
    except:
        break


time.sleep(10)


# Finding all the responses from 'https://portal.grab.com/foodweb/v2/search'
# and getting the latitude, longitude, id and names of all restaurants on this page.

for request in driver.requests:
    if request.response and request.url == 'https://portal.grab.com/foodweb/v2/search':
        res = request.response
        body = decode(res.body, res.headers.get('Content-Encoding', 'identity'))
        body_json = json.loads(body)

        searchMerchants = body_json['searchResult']['searchMerchants']
        for restaurant in searchMerchants:
            _data = {}
            _data['id'] = restaurant['id']
            _data['name'] = restaurant['address']['name']
            _data['latitude'] = restaurant['latlng']['latitude']
            _data['longitude'] = restaurant['latlng']['longitude']

            restaurant_list.append(_data)

output_latlng = {"_total_restaurants": len(restaurant_list), "restaurant_list": restaurant_list}


with open('output_latlng.json', 'w') as f:
    json.dump(output_latlng, f, ensure_ascii=False, indent=4)

print('\nDone...')