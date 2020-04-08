import helpers
import datetime
import json
from bs4 import BeautifulSoup
from requests import get
from dateutil.parser import parse

class AncestryDescription:
    def __init__(self, full_page, name):
        self.general = helpers.trim_html(full_page, '</i></a><br/>', '<h2 class="title">You Might...')
        self.you_might = helpers.ul_to_list(helpers.trim_html(full_page, 'You Might...</h2>', '<h2 class="title">Others Probably...'))
        if 'half' in name.lower():
            self.others_probably = helpers.ul_to_list(helpers.trim_html(full_page, 'Others Probably...</h2>', f'<h1 class="title">{name} Mechanics'))
        else:
            self.others_probably = helpers.ul_to_list(helpers.trim_html(full_page, 'Others Probably...</h2>', '<h2 class="title">Physical Description'))
            self.physical_description = helpers.trim_html(full_page, 'Physical Description</h2>', '<h2 class="title">Society')
            self.society = helpers.trim_html(full_page, 'Society</h2>', '<h2 class="title">Alignment and Religion')
            self.alignment_religion = helpers.trim_html(full_page, 'Alignment and Religion</h2>', '<h2 class="title">Names</h2>')
            self.names = helpers.trim_html(full_page, '<h2 class="title">Names</h2>', f'<h1 class="title">{name} Mechanics').replace('<h3 class="title">Sample Names</h3>', 'Sample names: ')
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    
class Ancestry:
    last_hit = datetime.datetime.now()
    
    def __init__(self, name, url):
        self.name = name
        self.hp = 0
        self.size = ''
        self.speed = 0
        self.boosts = ['']
        self.flaws = ['']
        self.languages = ['']
        self.specials = ['']
        self.url = url
        self.last_updated = 'never'
    
    def to_jsonify(self):
        json = {
            'Name': self.name,
            'Traits': self.traits,
            'Description': {
                'General': self.description.general,
                'YouMight': self.description.you_might,
                'OthersProbably': self.description.others_probably,
                'PhysicalDescription': self.description.physical_description,
                'Society': self.description.society,
                'AlignmentReligion': self.description.alignment_religion,
                'Names': self.description.names
            },
            'HP': self.hp,
            'Size': self.size,
            'Speed': self.speed,
            'Boosts': self.boosts,
            'Flaws': self.flaws,
            'Languages': self.languages,
            'Specials': self.specials,
            'URL': self.url,
            'LastUpdated': self.last_updated
        }
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
        self.hp = helpers.trim_html(ancestral_soup_str, 'Hit Points</h2>', '<h2 class="title">Size')
        self.size = helpers.trim_html(ancestral_soup_str, 'Size</h2>', '<h2 class="title">Speed')
        self.speed = helpers.trim_html(ancestral_soup_str, 'Speed</h2>', '<h2 class="title">Ability Boosts')
        
        if '<h2 class="title">Ability Flaw(s)</h2>' in ancestral_soup_str:
            self.boosts = helpers.trim_html(ancestral_soup_str, 'Ability Boosts</h2>', '<h2 class="title">Ability Flaw(s)').split('\n')
            self.flaws = helpers.trim_html(ancestral_soup_str, 'Ability Flaw(s)</h2>', '<h2 class="title">Languages').split('\n')
        else:
            self.boosts = helpers.trim_html(ancestral_soup_str, 'Ability Boosts</h2>', '<h2 class="title">Languages').split('\n')
        
        specials_soup = ancestral_soup.find_all('h2', class_='title')
        specials_list = [str(s) for s in specials_soup]
        languages_index = -1
        for i in range(len(specials_list)):
            if 'Languages' in specials_list[i]:
                languages_index = i
                specials_list = specials_list[i+1:]
                break

        if languages_index >= 0 and len(specials_list) > 0:
            tmp_languages = helpers.trim_html(ancestral_soup_str, 'Languages</h2>', specials_list[0]).split('\n')
            for i in range(len(tmp_languages)):
                if '<a' in tmp_languages[i]:
                    tmp_languages[i] = helpers.trim_html(tmp_languages[i], '>', '</a>')
            self.languages = tmp_languages
            self.specials = [] # TODO populate specials
        else:
            # TODO languages -> end for Ancestries with no specials
            pass

        # Hit Points
        # Size
        # Speed
        # Ability Boosts
        #     Constitution
        #     Wisdom
        #     Free
        # Ability Flaw(s)
        #     Charisma
        # Languages
        #     Common
        #     Dwarven
        #     Additional languages equal to your Intelligence modifier (if it’s positive). Choose from Gnomish, Goblin, Jotun, Orcish, Terran, Undercommon, and any other languages to which you have access (such as the languages prevalent in your region).
        # Darkvision
        #     You can see in darkness and dim light just as well as you can see in bright light, though your vision in darkness is in black and white.
        # Clan Dagger

        self.last_updated = str(datetime.datetime.now())
        return True

    def get_all():
        """ Returns a list of all ancestries currently on AoN """
        scraped = []
        response = get('http://2e.aonprd.com/Ancestries.aspx')
        Ancestry.last_hit = datetime.datetime.now()
        ancestral_soup = BeautifulSoup(response.text, 'html.parser')
        titles = ancestral_soup.find_all("h2", class_="title")
        links = [t.find_all("a")[1] for t in titles]
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