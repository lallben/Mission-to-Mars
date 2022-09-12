#Import Splinter, BeautifulSoup and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import pandas as pd
import datetime as dt

def scrape_all():
    #Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {
    "news_title": news_title,
    "news_paragraph": news_paragraph,
    "featured_image": featured_image(browser),
    "facts": mars_facts(),
    "hemispheres":mars_hemispheres(browser),
    "last_modified": dt.datetime.now() 
    }
   # Stop webdriver and return data
    browser.quit()
    return data

# Function to scrape Title and Summary paragraphs from news site
def mars_news(browser):
    # Visit the mars NASA news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #Convert browser html into a soup object and the quit borwser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_summ = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    return news_title, news_summ

#Function to capture Featured Image
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    try:
    # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None
    
    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

# Function to scrape table from Mars Facts website
def mars_facts():

    #Add try/except for error handling
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    # Convert dataframe to html
    return df.to_html()

# Function to scrape Mars Hemisphere images and urls
def mars_hemispheres(browser) :
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    # Parse the html with beautifulsoup
    html = browser.html
    imgs_soup = soup(html, 'html.parser')

    # Capture the relevant part of html code in a variable
    items=imgs_soup.find_all('div',class_='item')
    
    # loop through each hemisphere link with error handling
    try:
        for i in range(4):
            #Browse through each link to get the titles and images
            browser.links.find_by_partial_text('Hemisphere')[i].click()

            #Parse the resulting html with soup
            html = browser.html
            imgs_soup = soup(html, 'html.parser')

            #grab titles for each image
            title = imgs_soup.find ('h2',class_='title').text
            # grab link for full image
            img_url = imgs_soup.find('li').a.get('href')
            # Use the base URL to create an absolute URL and browser visit
            img_link=f'https://marshemispheres.com/{img_url}'

            # append items to list
            #hemisphere_image_urls.append({"img_url" : img_link,"title" : title, })

            hemispheres={}
            hemispheres['img_url']=img_link
            hemispheres['title']=title
            hemisphere_image_urls.append(hemispheres)

            browser.back()                                                                                                              

    except BaseException:
        return None

    # print(hemisphere_image_urls)
    return hemisphere_image_urls

# Final Code to End the Exercise
if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())