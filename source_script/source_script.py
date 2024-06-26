# here is the code that checks the integrity of the source page, so that you know  that if there are no hits, its because 
# the page has changed
# users can change the functions so that its specific to their source webpage

import requests
from requests.exceptions import ConnectionError, Timeout, RequestException

from bs4 import BeautifulSoup

# URL of the webpage to scrape
url = "https://opd.si/jbj"

def is_source_OK(logger)-> bool :
    
    if get_content_div(logger):
        return True
    else:
        logger.error(f"Source is NOT OK.")        
        False


def _get_data(logger):
    
    return scrape_articles(url, logger)



def get_content_div(logger):
    # Send a GET request to the URL
    try:
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the div with the specified class
            content_div = soup.find('div', class_='content-inner grid-view view-has-post')
            
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
    
    
    
    


def scrape_articles(url, logger):
    content_div = get_content_div(logger)
    if content_div:
        logger.debug(f"Content div found and started scrapping.")
        # Find all article elements within the div
        articles = content_div.find_all('article')

        scraped_data = []

        # Iterate over each article
        for article in articles:
            post_link = article.find('a', class_='post-link')['href']
            post_image = article.find('img', class_='wp-post-image')['src']
            post_date = article.find('div', class_='post-date').text.strip()
            post_title = article.find('h2', class_='post-title').text.strip()
            post_category = article.find('a', rel='category tag').text.strip()
            post_excerpt = article.find('div', class_='post-excerpt').text.strip()

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

