#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup


class Bot:
    def __init__(self):
        self.jokes = self.scrape_jokes()

    def tell_joke(self):
        # Generate and return a random joke
        return self.jokes.pop()

    def rate_joke(self, joke):
        # Take a joke and return a random rating from 1 to 10
        return 10  # Placeholder for the rating, you can modify this based on your criteria

    def scrape_jokes(self):
        # Web scraping to get jokes from the internet
        jokes = []
        # Perform web scraping using Beautiful Soup or any other method you prefer
        # Here's an example of scraping 108 jokes from a website
        url = "https://example.com/jokes"  # Replace with the actual URL you want to scrape from
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            joke_elements = soup.find_all("div", class_="joke")  # Adjust the selector based on the website structure
            for joke_element in joke_elements:
                joke = joke_element.text.strip()
                jokes.append(joke)

        return jokes