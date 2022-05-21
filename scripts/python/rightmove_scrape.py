import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date

#---------------------------------------------------------------------------------------------------------------------


# create lists to store our data
def get_for_sale_properties(ds, **kwargs):
    borough = kwargs['borough']
    print(f"Getting data for borough : {borough}")
    all_apartment_ids = []          # stores apartment ids from links
    all_apartment_bed_number = []   # stores number of beds
    all_apartment_links = []        # stores apartment links
    all_description = []            # stores number of bedrooms in the apartment
    all_address = []                # stores address of apartment
    all_price = []                  # stores the listing price of apartment


#---------------------------------------------------------------------------------------------------------------------

    index = 0
    for pages in range(40):

        # define our user headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
        }

        # the website changes if you are on page 1 as compared to other pages
        if index == 0:
            rightmove = f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%{borough}&sortType=6&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords="

        elif index != 0:
            rightmove = f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%{borough}&sortType=6&index={index}&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords="

        # request our webpage
        res = requests.get(rightmove, headers=headers)

        # check status
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")


#---------------------------------------------------------------------------------------------------------------------


        apartments = soup.find_all("div", class_="l-searchResult is-list")

        # This gets the number of listings
        number_of_listings = soup.find(
            "span", {"class": "searchHeader-resultCount"}
        )
        number_of_listings = number_of_listings.get_text()
        number_of_listings = int(number_of_listings.replace(",", ""))

        for i in range(len(apartments)):
            try:
                # tracks which apartment we are on in the page
                apartment_no = apartments[i]

                # append link
                apartment_info = apartment_no.find("a", class_="propertyCard-link")
                link = "https://www.rightmove.co.uk" + apartment_info.attrs["href"]
                all_apartment_links.append(link)

                # append address
                address = (
                    apartment_info.find("address", class_="propertyCard-address")
                    .get_text()
                    .strip()
                )
                all_address.append(address)

                # append description
                description = (
                    apartment_info.find("h2", class_="propertyCard-title")
                    .get_text()
                    .strip()
                )
                all_description.append(description)

                # append price
                price = (
                    apartment_no.find("div", class_="propertyCard-priceValue")
                    .get_text()
                    .strip()
                )
                all_price.append(price)

            except Exception as err:
                print(f"ERROR: {err}")
                break

        # Code to count how many listings we have scrapped already.
        index = index + 24

        if index >= number_of_listings:
            break

    # append id
    for apartment_link in all_apartment_links:
        all_apartment_ids.append(apartment_link[39:apartment_link.find('#')])
        # print(apartment_link[39:apartment_link.find('#')])

    # append number of beds
    for apartment_description in all_description:
        number_of_beds = apartment_description[:apartment_description.find(' ')]

        if number_of_beds.isdigit():
            all_apartment_bed_number.append(number_of_beds)
        else:
            all_apartment_bed_number.append("NULL")

    print(f"Array lengths: {len(all_apartment_ids)}, {len(all_address)}, {len(all_apartment_bed_number)}, {len(all_apartment_links)}, {len(all_description)}, {len(all_price)}")

    # convert data to dataframe
    data = {
        "ID": all_apartment_ids,
        "Address": all_address,
        "#Beds": all_apartment_bed_number,
        "Links": all_apartment_links,
        "Description": all_description,
        "Price": all_price,
    }
    df = pd.DataFrame.from_dict(data)
    df.to_csv(f"/home/eggzo/airflow/tmp_data/sales_data_{borough}_{ds}.csv", encoding="utf-8", header="true", index = False)
    #df.to_csv(f"sales_data_{borough}_{date.today()}.csv", encoding="utf-8", header="true", index = False)
