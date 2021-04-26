# Dev Project Notes:

# Consider moving to a Java front-end but build the front-end bones in Tkinter with Python for now. Python for back-end
# data management whatever language the front-end is written in.

# https://www.spareroom.co.uk/

# Inputs to site necessary: Postcode and Mile-Radius.

# Take one page room prices with these variables and average them into an "area-average room-price" variable.

# Extra input variables to think about: prices-averaged (amount of rooms-prices taken from the site and averaged),
# Weekly/Monthly rent type, To-move-in date, Length-of-stay, Days available, property type, Room amenities,
# Number of rooms, Rooms-for, share-with, age-range, household types (household options), size of household,
# property preferences, misc, keywords. (Basically the sidebar),
# see https://www.spareroom.co.uk/flatshare/?search_id=1033109264&

# CEO of Property Deals Insight, Nitin Aggarwal, has asked for an application, however,
# also explore the web-extension option, web-application app, and consider port to mobile app,
# for IOS you'd need to translate Python code to Swift.

# Need to add a tutorial "How to use the application" command.

# in terms of differing prices between pcm and pw, they both have unique abbr titles.
# Respectively: <abbr title="">pw</abbr> and <abbr title="">pcm</abbr>

from bs4 import BeautifulSoup
import requests

processing = "..."


opening_message = "\nThank you for using Property Deals Insight's spareroom.com room rate average calculator. Please " \
                  "be aware that the current version of the application is a demo and may be subject to change." \
                  "\n\nTo start, open your web browser and navigate to https://www.spareroom.co.uk/.\n\nNext, type " \
                  "in the area in which you would like to average the prices of rooms for e.g 'DE' for Derby. " \
                  "\n(If you are looking for certain types of listings i.e rooms specifically for couples, then " \
                  "please remember to tick those options on the left side of the screen and click 'Apply filters')" \
                  "\n\nLastly, copy and paste the resultant URL of the page into the 'Paste the page address here:' " \
                  "prompt.\n\nType 'Author signature' in the 'Paste page the address here:'" \
                  " prompt to see the author signature.\n\nIf you encounter any bugs or issues, please contact " \
                  "joebcox@outlook.com with the details. Thank you.\n\n...\n"


blank_space = " "


author_signature = "This application was made by Joe Benjamin Cox on behalf of Property Deals Insight Ltd.\n\n"\
                   + processing + "\n\nAuthor contact details:\n\nPhone: 07842 742291\n\n" \
                                  "Email: joebcox@outlook.com\n\n" + processing + "\n\n"


def getting_the_page():

    global html_address
    global current_offset
    global next_offset
    global prices
    global next_page_button_finder
    global soup
    global pages_scraped
    global next_page_address_finder

    html_address = input("Paste page the address here:")

    current_offset = 10
    next_offset = 20
    pages_scraped = 0

    html_text = requests.get(html_address).text

    soup = BeautifulSoup(html_text, 'lxml')
    prices = soup.find_all('strong', class_='listingPrice')

    next_page_button_finder = soup.find('ul', class_='navnext').text

    next_page_button_finder = next_page_button_finder.strip()

    next_page_address_finder = soup.find('ul', class_='navnext').findAll('li')[-1].find('a')['href']

    if html_address == "Author signature":

        print(blank_space)
        print(processing)
        print(blank_space)

        print(author_signature)

        getting_the_page()

    else:
        getting_amount_of_results_to_average()


def getting_amount_of_results_to_average():

    global prices
    global soup

    print(blank_space)
    print(processing)
    print(blank_space)

    global html_address
    global prices
    global next_page_soup
    global next_page_address
    global current_offset
    global next_offset
    global next_page_button_finder
    global pages_scraped


    while next_page_button_finder == "Next >>":

        html_address = html_address.replace("?search_id=", "")
        html_address = html_address.replace("&", "")

        next_offset_string = str(next_offset)

        next_page_address = html_address + next_page_address_finder

        next_page_address = next_page_address.replace("offset=10", "offset=" + next_offset_string)

        print("scraping: " + next_page_address)

        current_offset += 10
        next_offset += 10

        next_page_text = requests.get(next_page_address).text

        next_page_soup = BeautifulSoup(next_page_text, 'lxml')
        next_page_prices = next_page_soup.find_all('strong', class_='listingPrice')

        next_page_button_finder = next_page_soup.find('ul', class_='navnext').text

        next_page_button_finder = next_page_button_finder.strip()

        prices = prices + next_page_prices

        pages_scraped += 1
        pages_scraped_string = str(pages_scraped)

        print("checking for another page...")
        print("pages scraped: " + pages_scraped_string)
        print(blank_space)
        print(processing)
        print(blank_space)

    else:
        refining_the_prices()


def refining_the_prices():

    global no_pound

    prices_string = str(prices)

    pound_punctuation = '£-<=">/!'

    no_pound = ""

    for char in prices_string:

        if char not in pound_punctuation:
            no_pound = no_pound + char

    no_pound = no_pound.replace("a", " ")

    print("extracting the numbers...")
    print(blank_space)
    print(processing)
    print(blank_space)
    extracting_the_numbers()


def extracting_the_numbers():
    global numbers

    numbers = []

    for word in no_pound.split():

        if word.isdigit():
                numbers.append(int(word))

    print("averaging the numbers...")
    averaging_the_numbers()


def averaging_the_numbers():
    average = sum(numbers) / len(numbers)

    print(blank_space)
    print(processing)
    print(blank_space)
    print("The price average is:")
    print(average)
    print(blank_space)
    print(processing)
    print(blank_space)

    getting_the_page()


getting_the_page()
