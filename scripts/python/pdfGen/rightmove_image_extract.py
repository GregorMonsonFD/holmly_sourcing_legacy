import requests, re

def scrape_images(link):
    # define our user headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    }

    gallery_append = 'media?id=media0&ref=photoCollage&channel=RES_BUY'
    link_replace = '?channel=RES_BUY'
    regex_pattern = r'((?:https:)(?:[/|.|\w|\s|-])*(?:IMG_\d{2}_\d{4})\.(?:jpg|gif|png|jpeg))'

    gallery_link = link.replace(link_replace, gallery_append)

    res = requests.get(gallery_link, headers=headers)

    res.raise_for_status()

    matches = re.findall(regex_pattern, res.text)
    matches_clean = list(dict.fromkeys(matches))

    return matches_clean

