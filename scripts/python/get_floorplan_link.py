import re
import requests
from bs4 import BeautifulSoup

def link_cleanup(link: str):
    link = link.replace('/dir', '')

    start_of_search = len('https://media.rightmove.co.uk/')
    start_of_formatting = link.find('_max', start_of_search)
    end_of_formatting = link.find('.', start_of_search)

    link = link.replace(link[start_of_formatting: end_of_formatting], '')

    return link

def get_floorplan(site: str):
    floorplan_links = []
    floorplans = []
    response = requests.get(site)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')
    urls = [img['src'] for img in img_tags]

    for url in urls:
        if 'FLP' in url:
            floorplan_links.append(url)

    for floorplan in floorplan_links:
        floorplans.append(link_cleanup(floorplan))

    return floorplans