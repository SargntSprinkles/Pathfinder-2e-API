import helpers
import datetime
import json
from bs4 import BeautifulSoup
from requests import get
from dateutil.parser import parse

class AncestryDescription:
    def __init__(self, full_page, name):
        self.general =                              helpers.trim_html(full_page, '</i></a><br/>', helpers.hxtitle('You Might...', '2'))
        self.you_might = helpers.ul_to_list(        helpers.section_by_title(full_page, 'You Might...'))
        self.others_probably = helpers.ul_to_list(  helpers.section_by_title(full_page, 'Others Probably...'))
        self.physical_description =                 helpers.section_by_title(full_page, 'Physical Description')
        self.society =                              helpers.section_by_title(full_page, 'Society')
        self.alignment_religion =                   helpers.section_by_title(full_page, 'Alignment and Religion')
        self.adventurers =                          helpers.section_by_title(full_page, 'Adventurers')
        self.names =                                helpers.section_by_title(full_page, 'Names')
        self.sample_names =                         helpers.section_by_title(full_page, 'Sample Names')
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class AncestrySpecial:
    def __init__(self, full_page, name):
        self.name = name
        self.description = helpers.section_by_title(full_page, name)
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    
class Ancestry:
    last_hit = datetime.datetime.now()
    
    def __init__(self, name, url):
        self.name = name
        self.hp = 0
        self.size = ''
        self.speed = 0
        self.boosts = []
        self.flaws = []
        self.languages = []
        self.specials = []
        self.url = url
        self.last_updated = 'never'
    
    def to_jsonify(self):
        json = {
            'Name': self.name,
            'Traits': self.traits,
            'HP': self.hp,
            'Size': self.size,
            'Speed': self.speed,
            'Boosts': self.boosts,
            
            'Languages': self.languages,
            'URL': self.url,
            'LastUpdated': self.last_updated
        }

        if len(self.flaws) > 0 and len(self.flaws[0]) > 0:
            json.update({'Flaws': self.flaws})

        description = {}
        if self.description.general != '': description.update({'General': self.description.general})
        if self.description.you_might != '': description.update({'YouMight': self.description.you_might})
        if self.description.others_probably != '': description.update({'OthersProbably': self.description.others_probably})
        if self.description.physical_description != '': description.update({'PhysicalDescription': self.description.physical_description})
        if self.description.society != '': description.update({'Society': self.description.society})
        if self.description.alignment_religion != '': description.update({'AlignmentReligion': self.description.alignment_religion})
        if self.description.adventurers != '': description.update({'Adventurers': self.description.adventurers})
        if self.description.names != '': description.update({'Names': self.description.names})
        if self.description.sample_names != '': description.update({'SampleNames': self.description.sample_names})
        json.update({'Description': description})

        specials = {}
        for s in self.specials:
            specials.update({s.name: s.description})
        if len(specials) > 0:
            json.update({'Specials': specials})
        
        return json

    def scrape(self):
        """ Visits the URL of the Ancestry record and scrapes its data """
        # don't scrape more than once every 20 minutes
        if (self.last_updated != 'never' and
            self.description is not None and
            self.hp is not None and
            self.size is not None and
            self.speed is not None and
            (datetime.datetime.now() - parse(self.last_updated)).total_seconds() < 1200):
            return False
        
        response = get(self.url)
        ancestral_soup = BeautifulSoup(response.text, 'html.parser')
        
        # scrape traits
        trait_spans = ancestral_soup.find_all('span', class_='trait')
        trait_list = [t.a.contents[0] for t in trait_spans]
        self.traits = trait_list
        
        ancestral_soup_str = str(ancestral_soup)

        # scrape description
        self.description = AncestryDescription(ancestral_soup_str, self.name)
        self.hp = helpers.section_by_title(ancestral_soup_str, 'Hit Points')
        self.size = helpers.section_by_title(ancestral_soup_str, 'Size')
        self.speed = helpers.section_by_title(ancestral_soup_str, 'Speed')
        self.boosts = helpers.section_by_title(ancestral_soup_str, 'Ability Boosts').split('\n')
        self.flaws = helpers.section_by_title(ancestral_soup_str, 'Ability Flaw(s)').split('\n')
        self.languages = helpers.section_by_title(ancestral_soup_str, 'Languages').split('\n')
        
        if self.boosts == ['Two free ability boosts']:
            self.boosts = ['Free','Free']
        
        self.specials = []
        
        specials_soup = ancestral_soup.find_all('h2', class_='title')
        specials_list = [str(s) for s in specials_soup]
        languages_index = -1
        for i in range(len(specials_list)):
            if 'Languages' in specials_list[i]:
                languages_index = i
                specials_list = specials_list[i+1:]
                break

        if len(specials_list) > 0:
            # self.specials = specials_list
            for s in specials_list:
                special = AncestrySpecial(ancestral_soup_str, helpers.untitle(s))
                self.specials.append(special)

        self.last_updated = str(datetime.datetime.now())
        return True

    def get_all():
        """ Returns a list of all ancestries currently on AoN """
        scraped = []
        response = get('http://2e.aonprd.com/Ancestries.aspx')
        Ancestry.last_hit = datetime.datetime.now()
        ancestral_soup = BeautifulSoup(response.text, 'html.parser')
        titles = ancestral_soup.find_all("h2", class_="title")
        if len(titles) == 0:
            return scraped
        links = [t.find_all("a")[-1] for t in titles]
        ancestries_list = [[l.contents[0], 'http://2e.aonprd.com/' + l['href']] for l in links]
        for a in ancestries_list:
            name = a[0]
            url = a[1]
            scraped.append(Ancestry(name, url))
        return scraped

# test_ancestries = [
#     {
#         'Name': 'Human',
#         'Traits': [
#             'Human',
#             'Humanoid'
#         ],
#         'Description': {
#             'General': 'Human',
#             'YouMight': [
#                 'Be a human',
#                 'Do human things'
#             ],
#             'OthersProbably': [
#                 'Live longer than you',
#                 'Are older than you'
#             ],
#             'PhysicalDescription': 'Humanistic',
#             'Society': 'Humanitarian',
#             'AlignmentReligion': 'Everything',
#             'Names': 'Namey',
#             'SampleNames': [
#                 'Bob',
#                 'Alice'
#             ]
#         },
#         'HP': '8',
#         'Size': 'Medium',
#         'Speed': '25 feet',
#         'Boosts': [
#             'Free',
#             'Free'
#         ],
#         'Flaws': [
#             'None'
#         ],
#         'Languages': [
#             'Common'
#         ],
#         'Specials': [],
#         'URL': '',
#         'LastUpdated': ''
#     }
# ]