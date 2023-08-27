# IMDb User Reviews Scraper
This Python script allows you to scrape user reviews for movies from IMDb and store them in separate CSV files. It utilizes the IMDbPY package, Selenium, and BeautifulSoup to gather movie URLs and scrape user reviews.

Prerequisites
Before using this script, make sure you have the following installed:

Python: This script is written in Python.
Chrome WebDriver: You need to download the Chrome WebDriver and provide its path in the script. This WebDriver is used to control the Chrome browser.
Required Python Packages: Install the required packages using the following command:

 - pip install pandas selenium beautifulsoup4 IMDbPY

## Usage
1. Clone the repository or download the script to your local machine.
2. Install the required packages using the command mentioned above.
3. Download the Chrome WebDriver and set the PATH variable in the script to the path of the WebDriver on your machine.
4. Prepare a CSV file containing movie information (e.g., movie_id, movie_title, year, stripped_title). The script expects this file to be named u.item.
5. Run the script using the command:

    > python movie_user_review_scraper.py

6. The script will first retrieve IMDb URLs for the movies using the IMDbPY package and save them in a CSV file named moviesurl.csv in the data directory.
7. Then, the script will scrape user reviews for each movie from the IMDb URLs and store them in separate CSV files within the reviews directory.

## Important Notes
- The script uses Selenium to interact with IMDb pages and extract user reviews. Make sure to use the appropriate version of Chrome WebDriver compatible with your Chrome browser.
- The number of reviews scraped is set to 1000 per movie. You can adjust this value by changing the while loop condition in the get_review function.
- The script assumes that the data directory and the reviews directory exist in the same directory as the script. Make sure to create these directories before running the script.

## Disclaimer
*Please note that scraping websites might be against their terms of use. Always make sure to review and adhere to the website's terms of use and robots.txt before scraping any data.*

