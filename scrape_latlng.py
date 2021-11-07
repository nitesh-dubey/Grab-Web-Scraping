from selenium import webdriver
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


# Since we want all the restaurants on this page so we need to click
# Load More till the end of page
# We also need to sleep between clicks to prevent being detected as bots

time.sleep(10)
load_more_button = driver.find_element_by_xpath("//*[@class='ant-btn ant-btn-block']")


while True:
    try:
        time.sleep(10)
        load_more_button.click()
    except:
        break


time.sleep(10)

# After the whole page is loaded now, scrape all the urls of restaurants on this page

# This list will store urls of all restaurants on this page
restaurant_urls = []
soup = bs(driver.page_source, "html.parser")

base_url = 'https://food.grab.com'
for parent in soup.select("div.ant-col-24.RestaurantListCol___1FZ8V.ant-col-md-12.ant-col-lg-6"):
    a_tag = parent.find("a")
    href = a_tag.attrs['href']
    url = base_url + href
    restaurant_urls.append(url)


# Saving Restaurant urls
with open('restaurant_urls.txt', 'w') as f:
    for item in restaurant_urls:
        f.write('%s\n' % item)


# Total Number of Restaurants
print(f'Total Restaurants : {len(restaurant_urls)}\n')

# Output file containing latitude, longitude, name and id of all restaurants on this page
output_json = {"_total_restaurants": len(restaurant_urls), "restaurant_list": []}

restaurant_number = 1
for url in restaurant_urls:

    print(f'Scraping Restaurant Number : {restaurant_number} -----------------------------------------')

    driver.get(url)
    soup = bs(driver.page_source, 'html.parser')
    next_data = json.loads(soup.find(id="__NEXT_DATA__").text)

    restaurant_id = url.split('/')[-1]
    restaurant = next_data["props"]["initialReduxState"]["pageRestaurantDetail"]["entities"][restaurant_id]
    restaurant_name = restaurant["name"]
    restaurant_latitude = restaurant["latlng"]["latitude"]
    restaurant_longitude = restaurant["latlng"]["longitude"]

    data = {}
    data["id"] = restaurant_id
    data["name"] = restaurant_name
    data["latitude"] = restaurant_latitude
    data["longitude"] = restaurant_longitude

    output_json["restaurant_list"].append(data)

    # Waiting for sometime, to avoid flooding the website with requests
    if(restaurant_number % 50 == 0):
        time.sleep(15)
    else:
        time.sleep(5)

    restaurant_number += 1


# Saving the output file
with open('output_latlng.json', 'w') as f:
    json.dump(output_json, f, ensure_ascii=False, indent=4)


print('\nDone...')
