from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import pandas as pd
import time

#Function for all datascraping
def scrape_mars():
    #For MAC users
    #get_ipython().system('which chromedriver')
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    #Master Disctionary for all data to import into Mongo DB
    mission_to_mars = {}

    # NASA Mars News
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news'
    #Using splinter to visit the url and convert to html
    browser.visit(url)
    html = browser.html
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html, 'html.parser')
    # latest News Title and Paragraph Text
    time.sleep(5)
    slide_elem = soup.select_one('ul.item_list li.slide')
    content_title = slide_elem.find('div', class_="content_title")
    if content_title:
        news_title = content_title.find('a').text
    else:
        news_title = ""
    print(news_title)
    #news_date = slide_elem.find('div', class_="list_date").text
    #print(news_date)
    if slide_elem.find('div', class_="article_teaser_body"):
        news_p = slide_elem.find('div', class_="article_teaser_body").text
    else:
        news_p = ""
    print(news_p)
    #Storing the news title and news text into mission_to_mars dictionary
    mission_to_mars['news_title'] = news_title
    mission_to_mars['news_paragraph'] = news_p


    # JPL Mars Space Images - Featured Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    print(type(soup))
    extracted_img_url = soup.find('article')['style']
    print(f'Link:{extracted_img_url}')
    full_image_url = soup.find('a', class_="button fancybox")['data-fancybox-href']
    print(f'Full Image Link:{full_image_url}')
    #splitting the url to get only the basename
    url = url.split('?')[0]
    print(url)
    # Create a list of each bit between slashes
    slashparts = url.split('/')
    # Now join back the first three sections 'http:', '' and 'www.jpl.nasa.gov'
    basename = '/'.join(slashparts[:3])
    print(basename)
    featured_img_url = basename + full_image_url
    print(featured_img_url)
    #Storing the img url into mission_to_mars dictionary
    mission_to_mars['featured_img_url'] = featured_img_url
    
    # Mars Weather     
    url_twitter = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_twitter)
    html_twitter = browser.html
    soup = bs(html_twitter, 'html.parser')
    print(type(soup))
    mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    print(mars_weather)
    #Storing the weather info into mission_to_mars dictionary
    mission_to_mars['mars_weather'] = mars_weather

    # Mars Facts
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    mars_facts_df = tables[1]
    mars_facts_df.columns = ['Mars Planet Profile', 'Fact Values']
    mars_facts_df.set_index(["Mars Planet Profile"])
    mars_facts_html = mars_facts_df.to_html()
    mars_facts_htmlstring = mars_facts_html.replace("\n", "")
    mars_facts_htmlstring
    #Storing the mars fact info into mission_to_mars dictionary
    mission_to_mars['mars_facts'] = mars_facts_htmlstring

    # Mars Hemispheres
    url_hemisphere = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemisphere)
    html_hemisphere = browser.html
    soup = bs(html_hemisphere, 'html.parser')
    print(type(soup))
    #Complete url to split into base value
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    #splitting the url to get only the basename
    url = url.split('?')[0]
    # Create a list of each bit between slashes
    slashparts = url.split('/')
    # Now join back the first three sections 'http:', '' and 'astrogeology.usgs.gov'
    basename = '/'.join(slashparts[:3])
    print(basename)
    #Find all titles 
    titles = soup.find_all('div', class_='description')
    #List to store all dictionaries
    hemisphere_image_urls = []
    for result in titles:
        
        each_title = result.find('h3').text
        each_image_links = result.a['href']
        full_img_links = basename + each_image_links
        
        browser.visit(full_img_links)
        new_html = browser.html
        soup = bs(new_html, 'html.parser')
        partial_img_url = soup.find("img", class_="wide-image")["src"]
        complete_img_url = basename + partial_img_url
        hemisphere_image_urls.append({"title": each_title, "img_url": complete_img_url})
            
    print(hemisphere_image_urls)
    #Storing the mars mehisphere info into mission_to_mars dictionary
    mission_to_mars['mars_hemisphere'] = hemisphere_image_urls

    return mission_to_mars




