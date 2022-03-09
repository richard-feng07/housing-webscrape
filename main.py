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
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    }
    with requests.Session() as s:   
        locationInput = input("Where is the location? (city, state)")
        URL = 'https://www.zillow.com/homes/for_sale/' + locationInput  
        print()
        print(URL)
        print()
        page = s.get(URL, headers=req_headers)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find_all(class_="list-card list-card-additional-attribution list-card-additional-attribution-space list-card_not-saved")
        
        
        for content in results:
            house_price = content.find(class_="list-card-price")
            house_specs = content.find(class_="list-card-details") #Not formated correctly
            house_type = content.find(class_="list-card-statusText")
            house_address = content.find(class_="list-card-addr")
            house_link = content.find(class_="list-card-link list-card-link-top-margin list-card-img")
            house_realtor = content.find(class_="list-card-extra-info")
            children = house_specs.findChildren()
            house_spec_list = []
            for child in children:
                spec = child.find_next(text=True)
                spec = spec.split()
                house_spec_list.append(spec)
            house_bedroom_num = house_spec_list[0]
            house_bathroom_num = house_spec_list[2]
            house_sqft = house_spec_list[4]

            print(house_type.text.strip()[2:len(house_type.text.strip())])
            print(house_bedroom_num[0], "bedrooms |", house_bathroom_num[0], "bathrooms |", house_sqft[0], "sqft")
            print(house_price.text.strip())
            print(house_link["href"])
            print(house_realtor.text)
            print()

def Scrape_Trulia():
    print()
    req_headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    }
    with requests.Session() as s:
        # state = str(input("Where state? (Abbreviate)"))
        # city = str(input("What city?"))
        URL = 'https://trulia.com/CA/Irvine'
        page = s.get(URL, headers=req_headers)
        soup = BeautifulSoup(page.content, "html.parser")
        house_num = soup.find(class_="Text__TextBase-sc-1cait9d-0-div Text__TextContainerBase-sc-1cait9d-1 dPaHma SearchResultsRemoveBoundary__Container-bx3h4q-1 iFEACH")
        results = soup.find_all(class_="Box__BoxElement-sc-1f5rw0h-0 bsjsJO PropertyCard__PropertyCardContainer-m1ur0x-4 faCQjz")

        # nums = house_num.findChildren()
        print(house_num)
        for content in results:
            house_price = content.find(class_="Text__TextBase-sc-1cait9d-0-div Text__TextContainerBase-sc-1cait9d-1 keMYfJ")
            house_sqft = content.find(class_="Text__TextBase-sc-1cait9d-0-div Text__TextContainerBase-sc-1cait9d-1 dZyoXR")
            house_bdrooms = content.find(class_="Text__TextBase-sc-1cait9d-0-div Text__TextContainerBase-sc-1cait9d-1 bjqKkI")
            house_bthrooms = content.find("div", attrs={"data-testid":"property-baths"})
            house_address = content.find("div", attrs={"data-testid":"property-address"})
            house_link = content.find(class_="Anchor__StyledAnchor-sc-5lya7g-1 gLFHbk")
            house_realtor = content.find(class_="Text__TextBase-sc-1cait9d-0-div Text__TextContainerBase-sc-1cait9d-1 ccZuZv PropertyCard__CapitalizedText-m1ur0x-1 kehSAX")
            
            # print(house_bdrooms.text, house_bthrooms.text, house_sqft.text.strip())
            # print(house_price.text.strip())
            # print(house_address['title'])
            # print("https://trulia.com" + house_link['href'])
            # print(house_realtor)
            # print()
Scrape_Trulia()