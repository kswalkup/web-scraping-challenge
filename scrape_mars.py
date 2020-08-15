from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=True)

marsData = {}

def marsNewsScrape():
    try:
        browser = init_browser()
        
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)
        
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        
        # Retrieve the parent divs for all articles
        results = soup.find_all('div', class_='list_text')
        newsLead = ""
        newsB = ""
        newsDate = ""
        # loop over results to get article data
        for result in results:
        # scrape the article header 
            newsLead = result.find('a', target='_self').text
            newsB = result.find('div', class_='article_teaser_body').text

            if ',' in newsDate:
                print(newsLead)
                print(newsB)
                print(newsDate)
                break
            else: 
                pass
        
        marsData['newsLead'] = newsLead
        marsData['newsB'] = newsB
        marsData['newsDate'] = newsDate
        
        return marsData
    finally:
        
        browser.quit()

def marsImagesScrape():
    try:
        browser = init_browser()

        imageUrl = 'https://www.jpl.nasa.gov/spaceimages/'
        browser.visit(imageUrl)

        imageHtml = browser.html
        soup = BeautifulSoup(imageHtml, 'html.parser')

        sidebar = soup.find('section', class_='centered_text clearfix main_feature primary_media_feature single')
        categories = sidebar.find_all('footer')

        category_list = []
        url_list = []
        image_url_list = []
        for category in categories:
            title = category.text.strip()
            category_list.append(title)
            image_url = category.find('a')['data-fancybox-href']

        homeUrl = 'https://www.jpl.nasa.gov'
        finalImageUrl = homeUrl + image_url
        finalImageUrl
        
        marsData['finalImageUrl'] = finalImageUrl
        
        return marsData
    finally:
        
        browser.quit()

def marsWeatherScrape():
    try:
        browser = init_browser()
        
        weatherUrl = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weatherUrl)
        
        weatherHtml = browser.html
        soup = BeautifulSoup(weatherHtml, 'html.parser')
        weatherResults = soup.find_all('div', class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")

        weatherTweet = ""

        for weather in weatherResults:
            weatherTweet = weather.find('span', class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0").text

            if 'in' and 'pressure' in weatherTweet:
                print(weatherTweet)
                break
            else: 
                pass

        weatherTweet

        marsData['weatherTweet'] = weatherTweet
        
        return marsData
    finally:
        
        browser.quit() 

def marsFacts():
    factsUrl = 'http://space-facts.com/mars/'
    marsFacts = pd.read_html(factsUrl)
    mars_df = marsFacts[0]
    mars_df.columns = ['Description','Value']
    mars_df.set_index('Description', inplace=True)
    mars_df.to_html()
    savedAssets = mars_df.to_html()
    
    marsData ['marsFacts'] = savedAssets
    
    return marsData

def marsHemiScrape():
    try:
        browser = init_browser()
        
        hemiUrl = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemiUrl)
        
        hemiHtml = browser.html
        soup = BeautifulSoup(hemiHtml, 'html.parser')
        
        hemispheresTopUrl = 'https://astrogeology.usgs.gov'

        findHemi = soup.find_all('div', class_='item')
                             
        image_urls = []
        
        for images in findHemi: 
            title = images.find('h3').text
            leadLink = images.find('a', class_='itemLink product-item')['href']
            browser.visit(hemispheresTopUrl + leadLink)
            leadLink = browser.html
            soup = BeautifulSoup( leadLink, 'html.parser')
            imageSrc = hemispheresTopUrl + soup.find('img', class_='wide-image')['src']
            image_urls.append({"title" : title, "imageSrc" : imageSrc})
        
        marsData['image_urls'] = image_urls
                             
        return marsData
    finally:
        
        browser.quit()  

