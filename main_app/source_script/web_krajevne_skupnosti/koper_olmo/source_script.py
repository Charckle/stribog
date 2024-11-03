# here is the code that checks the integrity of the source page, so that you know  that if there are no hits, its because 
# the page has changed
# users can change the functions so that its specific to their source webpage

import requests
from requests.exceptions import ConnectionError, Timeout, RequestException

from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

# URL of the webpage to scrape
url = "https://www.koper.si/obcina/krajevne-skupnosti/krajevna-skupnost-olmo-prisoje/"

def is_source_OK()-> bool :
    
    if get_content_div():
        return True
    else:
        logger.error(f"Source is NOT OK.")        
        False


def _get_data():
    
    return scrape_articles(url, )



def get_content_div():
    # Send a GET request to the URL
    try:
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, 'html.parser')
            all_items = []
            
            # Find the section containing "Vabila na seje KS"            
            novice_obvestila = soup.find('h3', string='Novice in obvestila').find_next('div', class_='post-grid')
            # Extract all "vabila" items
            novice_obvestila_items = novice_obvestila.find_all("div", class_="card")
            all_items.append(novice_obvestila_items)
            
            # Find the section containing "Vabila na seje KS"            
            vabila_section = soup.find('h3', string='Vabila na seje KS').find_next('div', class_='files-grid')
            # Extract all "vabila" items
            vabila_items = vabila_section.find_all('div', class_='file-item filename')
            all_items.append(vabila_items)
            
            # Find the section containing "Vabila na seje KS"
            zapisniki_section = soup.find('h3', string=' Zapisniki seje KS').find_next('div', class_='files-grid')
            # Extract all "vabila" items
            zapisniki_items = zapisniki_section.find_all('div', class_='file-item filename')
            all_items.append(zapisniki_items)
            
            # Find the section containing "Vabila na seje KS"
            dokumenti_section = soup.find('h3', string=' Dokumenti').find_next('div', class_='files-grid')
            # Extract all "vabila" items
            dokumenti_items = dokumenti_section.find_all('div', class_='file-item filename')
            all_items.append(dokumenti_items)
            
            return all_items
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
    
    
    
    
def scrap_formula(div_content, type_):

    all_data = []
    # Iterate over each article
    for content_ in div_content:
        post_link = url
        post_image = ""
        post_date = content_.find('span', class_='file-date').text.strip()
        post_title = content_.find('a', class_='download pull-right')["title"].strip(".pdf").replace("-"," ")
        post_category = type_
        post_excerpt = post_title

        # Create a dictionary to store the extracted data
        article_data = {
            'post_link': post_link,
            'post_image': post_image,
            'post_date': post_date,
            'post_title': post_title,
            'post_category': post_category,
            'post_excerpt': post_excerpt
        }
        
        all_data.append(article_data)
          
    return all_data

def scrap_formula_othr(div_content, type_):
    
    all_data = []
    # Iterate over each article
    for content_ in div_content:
        post_link = url
        post_image = ""
        post_date = content_.find('span', class_='file-date')
        post_title = content_.text.strip()
        post_title = content_.find_all(string=True)[3].strip(",").strip()
        #print(content_.find_all(string=True))
        post_category = type_
        post_excerpt = post_title

        # Create a dictionary to store the extracted data
        article_data = {
            'post_link': post_link,
            'post_image': post_image,
            'post_date': post_date,
            'post_title': post_title,
            'post_category': post_category,
            'post_excerpt': post_excerpt
        }
        
        all_data.append(article_data)
        
    return all_data


def scrap_formula_card(div_content, type_):
    
    all_data = []
    
    for card in div_content:
        # Find h6 tag
        post_title = card.find("h6").get_text(strip=True) if card.find("h6") else None
        
        # Find div with class "date"
        post_date = card.find("div", class_="date").get_text(strip=True) if card.find("div", class_="date") else None
        
        # Find the "read-more" link
        post_link = card.find("a", class_="read-more")["href"] if card.find("a", class_="read-more") else None
        post_image = ""
        post_category = type_
        post_excerpt = post_title        
        
        article_data = {
            'post_link': post_link,
            'post_image': post_image,
            'post_date': post_date,
            'post_title': post_title,
            'post_category': post_category,
            'post_excerpt': post_excerpt
        }
        
        all_data.append(article_data)
        
    return all_data


def scrape_articles(url):
    content_div = get_content_div()
    if content_div:
        logger.debug(f"Content div found and started scrapping.")
        
        novice_obvestila = content_div[0]        
        vabila = content_div[1]
        zapisniki = content_div[2]
        dokumenti = content_div[3]

        # Append the dictionary to the list of scraped data
        scraped_data = []
        
        for i in scrap_formula_card(novice_obvestila, "novice, obvestila"):
            scraped_data.append(i)   
            
        for i in scrap_formula(vabila, "vabila"):
            scraped_data.append(i)
        
        for i in scrap_formula(zapisniki, "zapisniki"):
            scraped_data.append(i)
        
        for i in scrap_formula_othr(dokumenti, "dokumenti"):
            scraped_data.append(i)
        
        return scraped_data
    else:
        logger.error(f"Could not find the content div.")        
        
        return None



if __name__ == "__main__":
    data_ = _get_data()
    print(data_)