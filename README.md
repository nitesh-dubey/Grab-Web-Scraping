# Grab-Web-Scraping
This Repository contains the Python script for scraping the Latitude, Longitude, Name and ID of restaurants from [GrabFood](https://food.grab.com/ph/en/)

## Contents
<ul>
  <li><strong>scrape_latlng.py</strong> - <i>Script for Scraping latitude, longitude, name and id of all restaurants at a place in Manila</i></li>
  <li><strong>output_latlng.json</strong> - <i>Contains the scraped data in JSON format (538 restaurants)</i></li>

</ul>

## How to Run
```bash
  python scrape_latlng.py
```

## Solution
The GrabFood Website is made using NextJS with SSR. 

On visiting [Restaurant List Page](https://food.grab.com/ph/en/), we can get the Latitude and Longitude of only first 8 restaurants from the *NEXT_DATA*, which is used in hydration of this page.
We don't get the latitudes and longitudes of the subsequent restaurants obtained by clicking *Load More* button directly.

So to get the Latitude of Longitude of all other restaurants on this page, we need to monitor the requests made to *https://portal.grab.com/foodweb/v2/search* on clicking Load More Button.  The responses of these requests will contain the latlng of all other restaurants.

To Scrape the *latitude*, *longitude*, *name* and *id* of all restaurants,  I've used the following method.

<ul>

  <li>On visiting the <a href="https://food.grab.com/ph/en/">Restaurant List Page</a> , scrape the latitudes and  longitudes of first 8 restaurants from <i>NEXT_DATA</i></li>

  <li>Then, after clicking the <i>Load More</i> button several times, till we load to the end of page, capture all the responses from <i>https://portal.grab.com/foodweb/v2/search</i> using selenium-wire.</li>

  <li>Each Response will have the data of 8 restaurants. Scrape the latitudes and longitudes of all restaurants along with their name and Ids from all such responses. </li>

<li>Output the latitudes and longitudes of all restaurants in a <i>JSON</i> file</li>

</ul>