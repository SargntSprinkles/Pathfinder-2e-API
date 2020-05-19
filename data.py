import ancestries
import backgrounds
import datetime

class Data:
    def __init__(self):
        self.all_ancestries = []
        self.all_backgrounds = []
    
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

        # convert to list of json objects and return
        return [a.to_jsonify() for a in self.all_ancestries]
    
    def get_backgrounds(self, name=None):
        # check for new entries every 20 minutes
        if ((datetime.datetime.now() - backgrounds.Background.last_hit).total_seconds() >= 1200 or
            len(self.all_backgrounds) == 0):
            tmp_backgrounds = backgrounds.Background.get_all()
            for b in tmp_backgrounds:
                if b.name not in [x.name for x in self.all_backgrounds]:
                    self.all_backgrounds.append(b)
        
        # check for a matching name
        if name is not None:
            for b in self.all_backgrounds:
                if b.name.upper() == name.upper():
                    b.scrape()
                    return b.to_jsonify()
            # if no matches are found, report
            return f'Background "{name}" not found'

        # convert to list of json objects and return
        return [b.to_jsonify() for b in self.all_backgrounds]