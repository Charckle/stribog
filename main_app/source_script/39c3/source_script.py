# here is the code that checks the integrity of the source page, so that you know  that if there are no hits, its because 
# the page has changed
# users can change the functions so that its specific to their source webpage

import requests
from requests.exceptions import ConnectionError, Timeout, RequestException

from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

# URL of the webpage to scrape
base_url = "https://events.ccc.de/en/"
url = f"{base_url}category/39c3/"

def is_source_OK()-> bool :
    
    if get_content_div():
        return True
    else:
        logger.error(f"Source is NOT OK.")        
        False


def _get_data():
    
    return scrape_articles(url)



def get_content_div():
    # Send a GET request to the URL
    try:
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the div with the specified class
            content_div = soup.select_one("main > div:nth-of-type(2) > div")

            return content_div
        else:
            return False
            
    except ConnectionError as e:
        logger.error(f"Failed to connect to the server. Please check your internet connection or the URL. - {e}")        
        
        return False
    except Timeout as e:
        logger.error(f"The request timed out. Please try again later. - {e}")        
        return False
    except RequestException as e:
        logger.error(f"An error occurred: - {e}")        
        
        return False
    
    
    
    


def scrape_articles(url):
    content_div = get_content_div()
    if content_div:
        logger.debug(f"Content div found and started scrapping.")
        # Find all article elements within the div
        articles = content_div.find_all('article')

        scraped_data = []

        # Iterate over each article
        for article in articles:
            post_link_a = article.find('a')['href']
            post_link = f"{base_url}{post_link_a.split('/en/')[1]}"
            post_image_a = article.find('a').find('img')['src']
            post_image = f"{base_url}media{post_image_a.split('media')[1]}"
            header_ = article.find('header', class_='list__header')
            post_date = header_.find('div', class_='list__meta meta').find('div', class_='meta__item-datetime meta__item').find('time').text.strip()
            post_title = header_.find('a').text.strip()

            post_category = "39c3"
            post_excerpt = article.find('div', class_='content list__excerpt post__content clearfix').text.strip()[:200]
            

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

if __name__ == "__main__":
    data_ = _get_data()
    print(data_)