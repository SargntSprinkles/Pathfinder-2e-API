import helpers
import datetime
import json
from bs4 import BeautifulSoup
from requests import get
from dateutil.parser import parse

class Background:
    last_hit = datetime.datetime.now()

    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.last_updated = 'never'
    
    def to_jsonify(self):
        json = {
            'Name': self.name,
            # 'Traits': self.traits,
            'URL': self.url
        }

        return json

    def scrape(self):
        """ Visits the URL of the Backgound record and scrapes its data """
        # don't scrape more than once every 20 minutes
        if (self.last_updated != 'never' and
            (datetime.datetime.now() - parse(self.last_updated)).total_seconds() < 1200):
            return False
        
        response = get(self.url)
        background_soup = BeautifulSoup(response.text, 'html.parser')
        
        # scrape traits
        trait_spans = background_soup.find_all('span', class_='trait')
        trait_list = [t.a.contents[0] for t in trait_spans]
        self.traits = trait_list
        
        background_soup_str = str(background_soup)

        self.last_updated = str(datetime.datetime.now())
        return True
    
    def get_all():
        """ Returns a list of all backgrounds currently on AoN """
        Background.last_hit = datetime.datetime.now()
        return [Background(b[0],b[1]) for b in helpers.get_all('Backgrounds','h1')]