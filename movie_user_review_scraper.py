# ## IMDb User Reviews Scraper

import pandas as pd #Using panda to create our dataframe
# Import Selenium and its sub libraries
import selenium
from selenium import webdriver
# Import BS4
import requests #needed to load the page for BS4
from bs4 import BeautifulSoup

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re
import time

# ### Retrieve URLs using IMDbPY package


from imdb import IMDb

def get_imdb_url(movies):
    
    ia = IMDb()

    movie_ids = []
    movie_years = []
    movie_titles = []
    imdb_urls = []
    
    for index in range(0, len(movies)-1):
        
        movie_id = movies['movie_id'][index]
        movie_year = movies['year'][index]
        movie_title = movies['stripped_title'][index]                
        
        # Search for the movie
        search_results = ia.search_movie(movie_title)

        if not search_results:
            print(f"Movie '{movie_title}' not found on IMDb.")
            continue

        movieid = search_results[0].movieID
        movie = ia.get_movie(movieid)
        movie_url = ia.get_imdbURL(movie)
        
        movie_ids.append(movie_id)
        movie_years.append(movie_year)
        movie_titles.append(movie_title)
        imdb_urls.append(movie_url)

    #Build data dictionary for dataframe
    data = {'movie_id': movie_ids, 
            'movie_year': movie_years, 
            'stripped_title': movie_titles,
            'imdb_url' : imdb_urls
        }
    
    #Build dataframe for each movie to export
    movies_data = pd.DataFrame(data)
    
    # Save URLs in a CSV file
    movies_data.to_csv(f'data/moviesurl.csv')


#### Scraping Movie Reviews

def get_review(url_df, folder_name):
    # First step, we will need to import all the necessary libraries:

    # As we chose Chrome as our main web browser, we will need to download Chrome driver and tell Selenium where to find it:

    PATH = r"C:/chromedriver/chromedriver.exe"  # path to the webdriver file

    '''
    Get the review from input as url for IMDB movies list.
    The function takes 2 input the url of the movies and the name of the folder to store the data
    For each folder, the function will grab the review for each movies and store into respective file.
    '''

    #Set initial empty list for each element:
    title = []
    link = url_df['imdb_url']
    year = []      

    # After that, we can use BeautifulSoup to extract the user reviews link 
    #Set an empty list to store user review link
    user_review_links = []
    for i in range(len(url_df)):
        review_link = url_df['imdb_url'][i]+'reviews/?ref_=tt_ql_2'
            
        #Append the newly grabed link into its list
        user_review_links.append(review_link)

    url_df['review_link'] = user_review_links
    
    # Step 2, we will grab the data from each user review page
    # Use Selenium to go to each user review page
    for i in range(0,len(url_df['review_link'])): 
            
        service = Service(PATH)
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)
        print(url_df['review_link'][i])
        driver.get(url_df['review_link'][i])
        driver.implicitly_wait(2) # tell the webdriver to wait for 1 second for the page to load to prevent blocked by anti spam software


        # Set up action to click on 'load more' button
        # note that each page on imdb has 25 reviews
        page = 1 #Set initial variable for while loop
        #We want at least 1000 review, so get 50 at a safe number
        while page<50:  
            try:
                #find the load more button on the webpage
                load_more = driver.find_element(By.ID,'load-more-trigger')
                #click on that button
                load_more.click()
                page+=1 #move on to next loadmore button
            except:
                #If couldnt find any button to click, stop
                print("No button to click! Page ", page)
                break
        # After fully expand the page, we will grab data from whole website
        review = driver.find_elements(By.CLASS_NAME,'review-container')
        #Set list for each element:
        title = []
        content = []
        rating = []
        date = []
        user_name = []
        
        #run for loop to get
        if len(review) > 0:
            for n in range(0,1100):
                try:
                    #Some reviewers only give review text or rating without the other, 
                    #so we use try/except here to make sure each block of content must has all the element before 
                    #append them to the list

                    #Check if each review has all the elements
                    ftitle = review[n].find_element(By.CLASS_NAME,'title').text
                    #For the review content, some of them are hidden as spoiler, 
                    #so we use the attribute 'textContent' here after extracting the 'content' tag
                    fcontent = review[n].find_element(By.CLASS_NAME,'content').get_attribute("textContent").strip()
                    frating = review[n].find_element(By.CLASS_NAME,'rating-other-user-rating').text
                    fdate = review[n].find_element(By.CLASS_NAME,'review-date').text
                    fname = review[n].find_element(By.CLASS_NAME,'display-name-link').text


                    #Then add them to the respective list
                    title.append(ftitle)
                    content.append(fcontent)
                    rating.append(frating)
                    date.append(fdate)
                    user_name.append(fname)
                except:
                    continue
        #Build data dictionary for dataframe
        data = {'User_name': user_name, 
            'Review title': title, 
            'Review Rating': rating,
            'Review date' : date,
            'Review_body' : content
           }
        #Build dataframe for each movie to export
        review = pd.DataFrame(data = data)
        movie = url_df['stripped_title'][i] #grab the movie name from the top50 list    
        review['Movie_name'] = movie #create new column with the same movie name column    
        mid = url_df['movie_id'][i]
        review['movie_id'] = mid
        review.to_csv(f'data/{folder_name}/{mid}.csv') #store them into individual file for each movies, so we can combine or check them later
        driver.quit()
    print("Done processing")


if __name__ == '__main__':
    col_names = ['movie_id',
                 'movie_title',
                 'release_date',
                 'video_release_date',
                 'imdb_url',
                 'unknown',
                 'action',
                 'adventure',
                 'animation',
                 'children',
                 'comedy',
                 'crime',
                 'documentary',
                 'drama',
                 'fantasy',
                 'film_noir',
                 'horror',
                 'musical',
                 'mystery',
                 'romance',
                 'sci_fi',
                 'thriller',
                 'war',
                 'western']

    movies = pd.read_csv('u.item', sep='|', header=None, names=col_names, encoding='ISO-8859-1')
    movies['year'] = movies['movie_title'].str.extract('.*\((.*)\).*', expand=False)
    movies['stripped_title'] = movies['movie_title'].str.replace(r'\s*\(\d+\)$', '')

    #Retrieve movie IMDb URL
    urls = get_imdb_url(movies)
    print("!!!Done retrieving links!!!")

    #Scrape movie reviews
    movies_imdb = movies = pd.read_csv('data/moviesurl.csv')
    movies_imdb = movies_imdb.drop(movies_imdb.columns[movies_imdb.columns.str.contains('Unnamed', case=False)], axis=1)

    get_review(movies_imdb, 'reviews')

