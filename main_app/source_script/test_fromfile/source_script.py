# here is the code that checks the integrity of the source page, so that you know  that if there are no hits, its because 
# the page has changed
# users can change the functions so that its specific to their source webpage

import requests
from requests.exceptions import ConnectionError, Timeout, RequestException

from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def is_source_OK()-> bool :
    
    if get_content_div():
        return True
    else:
        logger.error(f"Source is NOT OK.")        
        False


def _get_data():
    
    return scrape_articles()



def get_content_div():
    try:
        file_path = 'source_script/content.html'
        
        # Open and read the file
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read the entire content of the file
            file_content = file.read()
        
        # Parse the file content with BeautifulSoup
        soup = BeautifulSoup(file_content, 'html.parser')
        
        content_div = soup.find('ul', id='fruit-list')
        
        #WHAT IF DIV IS NOT FOUND?
        
        return content_div    

    except Exception as e:
        logger.error(f"An error occurred: - {e}")        
        
        return False


def scrape_articles():
    content_div = get_content_div()
    if content_div:
        logger.debug(f"Content div found and started scrapping.")
        # Find all article elements within the div
        articles = content_div.find_all('li')

        scraped_data = []

        # Iterate over each article
        for article in articles:
            post_link = article.get_text()
            post_image = post_link
            post_date = post_link
            post_title = post_link
            post_category = post_link
            post_excerpt = post_link

            # Create a dictionary to store the extracted data
            article_data = {
                'post_link': post_link,
                'post_image': post_image,
                'post_date': post_date,
                'post_title': post_title,
                'post_category': post_category,
                'post_excerpt': post_excerpt
            }

            # Append the dictionary to the list of scraped data
            scraped_data.append(article_data)

        return scraped_data
    else:
        logger.error(f"Could not find the content div.")        
        
        return None

