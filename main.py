from unittest import result
from pip._vendor import requests
from bs4 import BeautifulSoup

def Scrape_HomeFinder():
    state = input("What state? (2 letters) ")
    city = input("What City? ")
    URL = "https://homefinder.com/homes-for-sale/"
    URL = (URL + state + "/" + city)

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find_all(class_="attributes d-flex justify-content-between align-items-start")
    location = soup.find_all(class_="strip")
    links = soup.find_all(class_="listing-tile d-flex flex-column", href = True)


    for house_content,location,link in zip(results,location,links):
        house_price = house_content.find(class_="h4 text-primary mb-0").find(text = True) #price
        house_type = house_content.find(class_="scope-label text-homes-for-sale small") #type
        house_info = house_content.find(class_="text-muted") #rooms, baths, sqft
        street_info = location.find(class_="addr-component h5 mb-0") #street
        city_info = location.find("meta", itemprop="addressLocality") #city
        state_info = location.find("meta", itemprop="addressRegion") #state
        zipcode_info = location.find("meta", itemprop="postalCode") #zipcode
        print()
        print(house_type.text.strip())
        print(house_price.strip())
        print(house_info.text.strip())
        print(street_info.text.strip(), city_info["content"].strip() + ",", state_info["content"].strip(), zipcode_info["content"].strip())
        print("Link: https://homefinder.com" + link['href'])
        print()

def Scrape_Zillow():
    print()
    req_headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.8',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36'
    }
    with requests.Session() as s:   
        locationInput = input("Where is the location? (city, state)")
        URL = 'https://www.zillow.com/homes/for_sale/'+locationInput    
        page = s.get(URL, headers=req_headers)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find_all(class_="list-card list-card-additional-attribution list-card-additional-attribution-space list-card_not-saved")
        # spe = soup.find("ul", { "class" : "list-card-details" }).find_all("li", recursive=False)
        # print(spe.text.split())


        for content in results:
            house_price = content.find(class_="list-card-price")
            house_specs = content.find(class_="list-card-details") #Not formated correctly
            house_type = content.find(class_="list-card-statusText")
            house_address = content.find(class_="list-card-addr")
            house_link = content.find(class_="list-card-link list-card-link-top-margin list-card-img")
            print(house_type.text.strip()[2:len(house_type.text.strip())])
            print(house_specs.text.strip())
            print(house_price.text.strip())
            print(house_address.text.strip())
            print(house_link["href"])
            print()
Scrape_Zillow()