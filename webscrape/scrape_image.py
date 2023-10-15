import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Define the URL of the webpage you want to scrape
base_url = "https://svasthaayurveda.com/yoga-pose-of-the-month-horse-stance/"
url = base_url  # Start with the first page

# Create a folder to save the images
if not os.path.exists("images"):
    os.mkdir("images")

# Define the keyword or criteria to filter images (e.g., "Horse Stance")
filter_keyword = "Horse Stance"

while url:
    # Send an HTTP GET request to the current page
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.text, "html5lib")

        # Find all image tags on the webpage
        img_tags = soup.find_all("img")

        # Download and save each image on the current page
        for img_tag in img_tags:
            # Get the source URL of the image
            img_url = img_tag.get("src")

            # If the URL is relative, make it absolute
            img_url = urljoin(url, img_url)

            # Send an HTTP GET request to download the image
            img_response = requests.get(img_url)

            if img_response.status_code == 200:
                # Extract the filename from the URL
                img_filename = os.path.basename(img_url)

                # Check if the filter keyword is in the image URL or filename
                if filter_keyword.lower() in img_url.lower() or filter_keyword.lower() in img_filename.lower():
                    # Save the image to the "images" folder
                    with open(os.path.join("images", img_filename), "wb") as img_file:
                        img_file.write(img_response.content)

                    print(f"Downloaded: {img_filename}")

        # Check if there is a "next" button on the current page
        next_button = soup.find("a", text="Next")

        if next_button:
            # Get the URL of the next page and update the 'url' variable
            url = urljoin(base_url, next_button.get("href"))
        else:
            # No "next" button found, exit the loop
            url = None

    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)

print(f"Image scraping for '{filter_keyword}' complete.")
