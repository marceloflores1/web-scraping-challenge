import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    # Setting up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    ### NASA Mars News
    # Defining url and visiting link
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Creating beautifulsoup on webpage
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Scrapping latest news title and paragraph text
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    ### JPL Mars Space Images - Featured Image
    # Defining url and visiting link
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # Creating beautifulsoup on webpage
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Scrapping featured_image_url, added url to relative path
    featured_image_url = url + soup.find('img', class_='headerimage')['src']

    ### Mars Facts
    # Defining url and converting to table, with some formatting
    url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url)
    mars_table = tables[0]
    facts_rows = []
    for index, row in mars_table.iterrows():
        facts_rows.append(row.tolist())
    facts_headers = facts_rows[0]
    facts_rows = facts_rows[1:]
    # Adding to_html code
    mars_table = mars_table.set_index([0])
    mars_facts = mars_table[1:]
    mars_facts.columns = mars_table.iloc[0]
    mars_facts.index.name = ""
    html_mars_facts = mars_facts.to_html().replace("\n","")  

    ### Mars Hemispheres
    # Defining url and visiting link
    url = "https://marshemispheres.com/"
    browser.visit(url)

    # Creating beautifulsoup on webpage
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Creating empty hemisphere links list
    hemisphere_links = []

    # Find all hemispheres using beautifulsoup and loop through them to append links to previous list
    hemispheres = soup.find_all('div', class_='item')
    for hemisphere in hemispheres:
        link = url + hemisphere.find('a')['href']
        hemisphere_links.append(link)

    # Creating empty image urls list    
    hemisphere_image_urls = []

    # Loop through links and visit them to obtain title and image url and append dictionary to previous list
    for link in hemisphere_links:
        browser.visit(link)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('h2', class_='title').text
        image_div = soup.find('div', class_='downloads')
        image_a = image_div.find('ul').find_all('li')[0].find('a')
        img_url = url + image_a['href']
        hemisphere_image_urls.append({"title": title, "img_url": img_url})



    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "facts_headers": facts_headers,
        "facts_rows": facts_rows,
        "hemisphere_image_urls": hemisphere_image_urls,
        "html_mars_facts": html_mars_facts
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
