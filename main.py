from pip._vendor import requests
from bs4 import BeautifulSoup

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

