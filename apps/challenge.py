# Imports Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
# imports pandas
import pandas as pd
import datetime as dt

executable_path = {'executable_path': 'chromedriver.exe'}

def scrape_all():
    # Creates path
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {
    "news_title": news_title,
    "news_paragraph": news_paragraph,
    "featured_image": featured_image(browser),
    "facts": mars_facts(),
    "last_modified": dt.datetime.now(), 
    "hemispheres" : hemispheres(browser)
    }
    return data

    browser.quit()

# creates a function that accesses nasa website and scrapes mars data
def mars_news(browser):
    # Visits the nasa webiste for mars news
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Delay to load page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # sets up html parser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    #adds try/ except for handling scraping errors
    try:
        # searches for parent elem which desired data is stored
        slide_elem = news_soup.select_one('ul.item_list li.slide')

        # finds the first 'a' tag that is stored in parent element slide_elem
        news_title = slide_elem.find("div", class_='content_title').get_text()

        # searches for the paragraph body text of the article
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None
        
    return news_title, news_p

# ### Featured Images
def featured_image(browser):
    # Visit NASA Mars URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Finds the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Finds more info button and clicks
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()

    # Parses the html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    
    # try/ except for error handling
    try: 
    # Finds the image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Uses base url to make absolute url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

def mars_facts():
    # try/ except for error handling
    try:
        # creqates a new dataframe of first html table encountered
        df = pd.read_html('http://space-facts.com/mars/')[0]
    
    except BaseException:
        return None
            
    # sets columns of description and value
    df.columns=['Description', 'Mars']
    # sets description as index
    df.set_index('Description', inplace=True)

    return df.to_html()

def hemispheres(browser):
    # visits websites for hemisphere images and urls
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    hemispheres_url = []
    hemispheres_html = browser.html
    soup = BeautifulSoup(hemispheres_html, 'html.parser')
        
    items = soup.find_all('div', class_ = 'item')

    for i in items:
        hemispheres_url.append('https://astrogeology.usgs.gov' + i.find('a', href = True)['href'])
    
    images = []

    for url in hemispheres_url:
        browser.visit(url)
        hemispheres_html = browser.html
        soup = BeautifulSoup(hemispheres_html, 'html.parser')
        hemispheres_dict = {'title': soup.find('h2', class_='title').text, 'image' : 'https://astrogeology.usgs.gov' + soup.find('img', class_='wide-image').get('src')}
        images.append(hemispheres_dict)
        return 'https://astrogeology.usgs.gov' + soup.find('img', class_='wide-image').get('src')
    

if __name__ == "__main__":
    # Prints scraped data if being run as a script
    print(scrape_all())
