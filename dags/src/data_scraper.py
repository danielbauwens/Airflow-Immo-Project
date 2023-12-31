import time
import requests
from bs4 import BeautifulSoup
import csv
import json
import re
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import os.path

def get_links(session, pages):
    """
    This function retrieves the links for the property listings.
    
    Parameters:
    session: A requests.Session object for making HTTP requests
    pages: The number of pages to scrape for property links

    Returns:
    links: A list containing the links for each property listing
    """

    links = []  # Initialize an empty list to hold the links
    
    # Loop over the number of pages to scrape
    for i in tqdm(range(pages), desc="Extracting links", ncols=80):
        # URLs for houses and apartments for sale
        url = f"https://www.immoweb.be/en/search/house/for-sale?countries=BE&page={i+1}&orderBy=relevance"
        url2 = f"https://www.immoweb.be/en/search/apartment/for-sale?countries=BE&page={i+1}&orderBy=relevance"

        # Iterate over both URLs
        for urlin in [url, url2]:
            response = session.get(urlin)  # Send a GET request to the URL
            soup = BeautifulSoup(response.content, 'html.parser')  # Parse the response content with BeautifulSoup
            memories = soup.find_all(class_='card__title-link')  # Find all elements with the class 'card__title-link'

            # Loop over all the links found
            for link in memories:
                if link.find_parent('h3'):  # If the link has a parent element of 'h3', ignore it
                    continue
                else:  # If the link does not have a parent element of 'h3', append it to the links list
                    links.append(link.get('href'))

    print("Links extracted successfully!")

    return links  # Return the list of links




def initialize_csv():
    """
    This function initializes a CSV file with the specified headers.

    It uses the csv module's DictWriter to create a CSV file that can be easily 
    written to using dictionaries. The keys of the dictionaries will correspond 
    to the headers in the CSV file.

    The filename is hardcoded to "property_data.csv", and the headers are a list 
    of strings that correspond to the data that will be written to the file.
    """

    # Define the filename
    filename = "./data/property_data.csv"

    # Define the headers of the CSV file. These are the names of the fields each row will have.
    headers = [
        "city",
        "zip",
        "kitchen",
        "type",
        "subtype",
        "price",
        "saletype",
        "bedrooms",
        "living_area",
        "terrace",
        "terrace_area",
        "garden",
        "garden_area",
        "landplot",
        "facades",
        "pool",
        "ID",
        "building_state",
        "URL"
    ]

    # Open the file in write mode. The newline='' argument is necessary for the csv module to work properly on both 
    # Windows and Unix systems. The file is opened in utf-8 encoding to support a wide range of characters.
    if os.path.isfile('./data/property_data.csv'):
        pass
    else:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            # Create a DictWriter object. This object will be used to write rows to the CSV file. The fieldnames 
            # argument defines the order in which values in the dictionary are written to the CSV file.
            writer = csv.DictWriter(f, fieldnames=headers)
            
            # Write the headers to the CSV file. This is done by calling the writeheader method on the DictWriter object.
            writer.writeheader()

def read_existing_listings(filename):
    with open(filename, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        existing_listings = list(reader)

    return existing_listings

def is_duplicate_listing(data_dict, existing_listings):
        # Iterate over each existing listing in the list of existing_listings
        for existing_listing in existing_listings:
            # Check if the ID of the existing listing matches the ID of the data_dict
            if data_dict['ID'] == existing_listing['ID']:
                return True  # Return True if conditions match, indicating a duplicate listing
            else:
                continue
        return False  # Return False if no duplicate listing is found

def write_to_csv(data_dict):
    """This function writes a dictionary to the CSV file."""
    filename = "./data/property_data.csv"

    # Read existing listings from the CSV file
    existing_listings = read_existing_listings(filename)

    # Append new listings to the CSV file
    # Check for duplicate listings based on ID, Zip Code, and garden area
    if is_duplicate_listing(data_dict, existing_listings) == False:
        # Open the file in append mode to add the new listing
        with open(filename, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data_dict.keys())
            writer.writerow(data_dict)

def process_link(session, url):
    """
    This function processes a single property link. The steps involved in processing the link are:
    1. Fetching the page content using an HTTP GET request.
    2. Parsing the page content using BeautifulSoup.
    3. Extracting the relevant data from the parsed page content.
    4. Writing the extracted data to a CSV file.

    The `session` parameter is an instance of requests.Session. Using a Session object gains efficiency when making
    multiple requests to the same host by reusing the underlying TCP connection.

    The `url` parameter is a string that contains the URL of the property listing that should be processed.
    """

    # Print a status message to indicate which URL is currently being processed.
    print("Processing: ", url)

    # Use the requests.Session instance to make an HTTP GET request to the provided URL. 
    # This sends a request to the server to return the content located at the specified URL.
    response = session.get(url)

    # Parse the content of the response using BeautifulSoup. The "html.parser" argument tells BeautifulSoup to use 
    # Python's built-in HTML parser to parse the page content.
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the relevant data from the parsed page content. This is done by calling the previously defined 
    # 'extract_relevant_data' function, which returns a dictionary of the relevant data.
    data_dict = extract_relevant_data(soup, url)

    # Write the extracted data to the CSV file. This is done by calling the previously defined 'write_to_csv' function,
    # which takes a dictionary of data and writes it to the CSV file as a new row.
    write_to_csv(data_dict)



def extract_relevant_data(soup, url):
    """
    This function extracts the relevant data from the HTML content of a property listing page. 
    It uses the BeautifulSoup instance of the HTML content (`soup`) and the URL of the page (`url`) as inputs.

    After identifying and extracting the relevant data from the HTML content, the function packages the 
    data into a dictionary and returns it.
    """

    # The data we're interested in is contained within a script tag, serialized as a JSON object. 
    # Find the script tag whose content includes "window.dataLayer".
    script = soup.find("script", string=lambda t: "window.dataLayer" in t).string
    #lambda t:"window.dataLayer" in t is a lambda function that takes a single argument t and checks if 
    # the string "window.dataLayer" is present in it. 
    # This function is used as the string argument in soup.find(), which means that it will be called 
    # with the string content of each <script> tag, and the tag will be selected if the function returns True.

    # The script tag's content is a JavaScript command, not just the JSON data, so split the string on 
    # "window.dataLayer = " and take the second part. Remove trailing whitespace and the final semicolon.
    # Then load the resulting string as JSON.
    data = json.loads(script.split("window.dataLayer = ")[1].strip().rstrip(";"))

    # Retrieve the necessary details from the data layer.
    classified_url = url
    classified_id = data[0]["classified"]["id"]  
    classified_type = data[0]["classified"]["type"]
    classified_subtype = data[0]["classified"]["subtype"]  
    classified_price = data[0]["classified"]["price"] 
    classified_kitchen = data[0]["classified"]["kitchen"]["type"]
    classified_room = data[0]["classified"]["bedroom"]["count"]
    classified_terrace = data[0]["classified"]["outdoor"]["terrace"]["exists"]
    classified_garden = data[0]["classified"]["outdoor"]["garden"]["surface"]
    classified_surface_land = data[0]["classified"]["land"]["surface"]
    classified_swimming_pool = data[0]["classified"]["wellnessEquipment"]["hasSwimmingPool"]
    classified_state_of_building = data[0]["classified"]["building"]["condition"]
    classified_zip_code = data[0]["classified"]["zip"]

    # The second part of the data we need is in a different script tag, so again find the script tags 
    # and look for one that contains "window.classified".
    scripts = soup.find_all('script')
    data_class = None
    for script in scripts:
        if 'window.classified' in script.text:  # The variable containing the JSON data
            clas_sting = re.search('window.classified = ({.*?});', script.text).group(1)
            data_class = json.loads(clas_sting)
            break
    

    # Extract the required details from the second data layer.
    classified_cityname = data_class['property']['location']['locality']
    classified_living_area = data_class['property']["netHabitableSurface"]
    classified_number_of_facades = data_class['property']['building']['facadeCount']
    classified_terrace_area = data_class["property"]["terraceSurface"]

    # Identify the saletype based on which sales type flags are set to true.
    flags = data_class['flags']
    sales_types = ['isPublicSale', 'isNotarySale', 'isLifeAnnuitySale', 'isInvestmentProject', 'isSoldOrRented', "isAnInteractiveSale","isUnderOption"]
    classified_sales_type = None

    for sales_type in sales_types:
        if sales_type in flags and flags[sales_type]:
            classified_sales_type = sales_type
            break

    # check number of rooms
    if classified_room == "":
        classified_room = None

    # check kitchen
    if classified_kitchen == "not installed":
        classified_kitchen = 0
    elif classified_kitchen == "":
        classified_kitchen = None
    else:
        classified_kitchen = 1

    # check terrace
    if classified_terrace == "false":
        classified_terrace = 0
    elif classified_terrace == "":
        classified_terrace = None
    else:
        classified_terrace = 1

    # check garden
    if classified_garden == "false":
        classified_garden = 0
        classified_garden_area = None
    elif classified_garden == "":
        classified_garden = None
        classified_garden_area = None
    else:
        classified_garden_area = classified_garden
        classified_garden = 1

    # check pool data
    if classified_swimming_pool == "true":
        classified_swimming_pool = 1
    elif classified_swimming_pool == "":
        classified_swimming_pool = None
    else:
        classified_swimming_pool = 0

    # Return the extracted data as a dictionary.
    return {
        "city": classified_cityname,
        "zip": classified_zip_code,
        "kitchen": classified_kitchen,
        "type": classified_type,
        "subtype": classified_subtype,
        "price": classified_price,
        "saletype": classified_sales_type,
        "bedrooms": classified_room,
        "living_area": classified_living_area,
        "terrace": classified_terrace,
        "terrace_area": classified_terrace_area,
        "garden": classified_garden,
        "garden_area": classified_garden_area,
        "landplot": classified_surface_land,
        "facades": classified_number_of_facades,
        "pool": classified_swimming_pool,
        "ID": classified_id,
        "building_state": classified_state_of_building,
        "URL": classified_url
    }



def main():
    # Record the start time of the script
    start_time = time.time()

    # Create a session object
    session = requests.Session()

    # Set the number of pages to scrape. In this case, it is set to 1, but you can adjust this number based on your needs.
    while True:
        try:
            pages = 1
            break
        except ValueError:
            print("Invalid input! Please enter a valID.")

    # Initialize the CSV file with the right headers. This ensures we have a file ready to hold the data we're going to scrape.
    initialize_csv()

    # Get all the property links from the defined number of pages. This function will return a list of URLs.
    links = get_links(session, pages)

    print("Starting scraping...")

    # Process the links in a multithreaded manner to speed up the process.
    # The number of workers is set to 16, but this can be adjusted based on your system's capabilities.
    num_workers = 16
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        # Use a lambda function to pass the session object to process_link function
        executor.map(lambda url: process_link(session, url), links)

    # Record the end time of the script
    end_time = time.time()

    print("Scraping done!🕸️")
    # Calculate and print the total time taken for the script to execute
    print("Execution time: ", end_time - start_time, "seconds") 

if __name__ == "__main__":
    main()