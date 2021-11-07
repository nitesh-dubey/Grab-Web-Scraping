# Grab-Web-Scraping
This Repository contains the Python script for scraping the Latitude, Longitude, Name and ID of restaurants from [GrabFood](https://food.grab.com/ph/en/)

## Contents
<ul>
  <li><strong>scrape_latlng.py</strong> - <i>Script for Scraping latitude, longitude, name and id of all restaurants at a place in Manila</i></li>
  <li><strong>output_latlng.json</strong> - <i>Contains the scraped data in JSON format (538 restaurants)</i></li>
  <li><strong>restaurant_urls.txt</strong> - <i>Contains the urls of all scraped restaurants</i></li>
</ul>

## How to Run
```bash
  python scrape_latlng.py
```

## Solution
The GrabFood Website is made using NextJS with SSR. 

From the [Restaurant List Page](https://food.grab.com/ph/en/), we can get the Latitude and Longitude of only first few restaurants, because the *NEXT_DATA* which is used in hydration of the NextJS app, contains the latitude and longitude of only first few restaurants.
We don't get the latitudes and longitudes of the subsequent restaurants obtained by clicking *Load More* button.

So to get the Latitude of Longitude of All restaurants on this page, I have coded the following approach using Selenium.

<ul>
  <li>From the <a href="https://food.grab.com/ph/en/">Restaurant List Page</a> scrape the URLs of all the restaurants, after clicking the <i>Load More</i> button several times to the end of page.</li>
  
  <li>Visit each URL, and scrape the Latitude, Longitude, Restaurant Name and ID from the page props.</li>
</ul>
