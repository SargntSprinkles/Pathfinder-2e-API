import ancestries
import datetime

class Data:
    def __init__(self):
        self.all_ancestries = []
    
    def get_ancestries(self, name=None):
        # check for new entries every 20 minutes
        if ((datetime.datetime.now() - ancestries.Ancestry.last_hit).total_seconds() >= 1200 or
            len(self.all_ancestries) == 0):
            tmp_ancestries = ancestries.Ancestry.get_all()
            for a in tmp_ancestries:
                if a.name not in [x.name for x in self.all_ancestries]:
                    self.all_ancestries.append(a)
        
        # check for a matching name
        if name is not None:
            for a in self.all_ancestries:
                if a.name.upper() == name.upper():
                    a.scrape()
                    return a.to_jsonify()
            # if no matches are found, report
            return f'Ancestry "{name}" not found'

        # convert to json, append, and return
        json_list = []
        for a in self.all_ancestries:
            a.scrape()
            json_list.append(a.to_jsonify())
        return json_list