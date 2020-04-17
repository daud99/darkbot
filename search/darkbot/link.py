"""

This module is used to create a LinkNode that can be consumued by a LinkTree
and contains useful Link methods

"""
import requests
import requests.exceptions
import validators
import re
from bs4 import BeautifulSoup

def get_emails(node):
    """Finds all emails associated with node

    Args:
        node (LinkNode): node used to get emails from
    Returns:
        emails (list): list of emails
    """
    emails = []
    response = node.response.text
    mails = re.findall(r'[\w\.-]+@[\w\.-]+', response)
    mails=set(mails)
    for email in mails:
        if LinkNode.valid_email(email):
            #print("self.uri is in getemails : " + node.uri)
            emails.append([email, node.uri, node.name])
    return emails

def get_links(node):
    """Finds all links associated with node

    Args:
        node (LinkNode): node used to get links from
    Returns:
        links (list): list of links
    """
    links = []
    for child in node.children:
        link = child.get('href')
        print(link)
        if link and LinkNode.valid_link(link):
            #print("link : "+link)
            #print("node.uri is :"+node.uri)
            if node.validator in link:
                if "signin" not in link.lower() and "login" not in link.lower() and "signup" not in link.lower():
                    links.append(link)
        elif link and "http" not in link.lower() and LinkNode.valid_link(node.validator+link):
            link=node.validator+link
            #print("link in elif: " +link)
            if node.validator in link:
                if "signin" not in link.lower() and "login" not in link.lower() and "signup" not in link.lower():
                    links.append(link)


    links = set(links)
    return links

class LinkNode:
    """Represents link node in a link tree

    Attributes:
        link (str): link to be used as node
    """

    def __init__(self, link, name, validator):
        # If link has invalid form, throw an error
        if not self.valid_link(link):
            raise ValueError("Invalid link format.")
        # print('self._children = []')
        self._children = []
        # print('self._emails = []')
        self._emails = []
        # print('self._links = []')
        self._links = []

        # Attempts to connect to link, throws an error if link is unreachable
        try:
            self.response = requests.get(link)
        except (requests.exceptions.ChunkedEncodingError,
                requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError,
                ConnectionError) as err:
            raise err

        self._node = BeautifulSoup(self.response.text, 'html.parser')
        self.uri = link
        self.name = name
        self.validator = validator
        print("self.uri is : "+self.uri)
        print("self.name is : " + self.name)
        

    @property
    def emails(self):
        print('email func')
        """
        Getter for node emails
        """
        if not self._emails:
            self._emails = get_emails(self)
        return self._emails

    @property
    def links(self):
        print('link func')
        """
        Getter for node links
        """
        if not self._links:
            self._links = get_links(self)
        return self._links

    @property
    def children(self):
        print('children func')
        """
        Getter for node children
        """
        if not self._children:
            self._children = self._node.find_all('a')
        return self._children

    @staticmethod
    def valid_email(email):
        """Static method used to validate emails"""
        if validators.email(email):
            return True
        return False

    @staticmethod
    def valid_link(link):
        """Static method used to validate links"""
        if validators.url(link):
            return True
        return False
