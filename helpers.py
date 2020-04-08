from bs4 import BeautifulSoup

def trim_html(src, start, end):
    tmp = src[src.index(start)+len(start):src.index(end)]
    tmp = tmp.replace('<br/>','\n')
    tmp = tmp.replace('<i>','')
    tmp = tmp.replace('</i>','')
    tmp = tmp.replace(u'\u2014','--')
    tmp = tmp.replace(u'\u2019',"'")
    return tmp.strip()

def ul_to_list(src):
    soup = BeautifulSoup(src, 'html.parser')
    items = []
    for li in soup.find_all("li"):
        items.append(li.string.strip())
    return items