"""
Joke Retrieval from API

This module provides a function for retrieving jokes from a specified API URL.

Author: Raigon Augustin
Date: 115.08.2023
"""

# Import necessary module
import requests


def get_joke(api_url):
    """
    Retrieve a joke from the specified API URL.

    This function sends a GET request to the provided API URL to fetch a joke. The joke can be in either a 'twopart'
    format, where it consists of a setup and a delivery, or a 'single' format.

    Args:
        api_url (str): The URL of the API to fetch a joke from.

    Returns:
        str: The retrieved joke.
    """
    response = requests.get(api_url).json()
    if response['type'] == 'twopart':
        return response['setup']+' '+response['delivery']
    else:
        return response['joke']

