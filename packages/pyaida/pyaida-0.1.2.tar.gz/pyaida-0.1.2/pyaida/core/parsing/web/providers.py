import requests
from bs4 import BeautifulSoup
from .. import parse_bibtex


class ResourceParseBase:
    """every url is a resource and we can parse the metadata for it"""
    
    
    def _get_open_graph_data(self, url, use_header=False):
        """get graph basic"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://google.com', 
            }  if use_header else {}
                    
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            self.soup = BeautifulSoup(response.content, 'html.parser')
            og_data = {}

            og_data['uri'] = url
            og_image_tag = self.soup.find('meta', property='og:image')
            og_data['image'] = og_image_tag.get('content') if og_image_tag else None
            
            og_title_tag = self.soup.find('meta', property='og:title')
            og_data['title'] = og_title_tag.get('content') if og_title_tag else None

            og_description_tag = self.soup.find('meta', property='og:description')
            og_data['description'] = og_description_tag.get('content') if og_description_tag else ''
            
            """try"""
            for attempt in ['dc.creator', 'author', 'coauthor', 'og:author']:
                recs = self.soup.find_all('meta', {'name':attempt})
                if recs:
                    og_data['author'] = "; ".join(list(map(lambda x: x['content'], recs)))
                    break
            
            
            return og_data 
        else:
            print(f"Failed to fetch page. Status code: {response.status_code}")
            return None


    def handle(self, data:dict):
        """
        base implements
        """
        return {}
            
    def parse_many(self, key, mapping):
            m = mapping[key]
            r= self.soup.find_all('meta',  m)
            r =  [c['content'] for c in r]
            return r
        
    def parse_one(self, key, mapping):
        r = self.parse_many(key, mapping)
        if r: 
            return r[0]
            
    def _run(self,url):
        data = self._get_open_graph_data(url) or {}
        data.update(self.handle(data))
        return data
    
    def __call__(self, url):
        return self._run(url)

 
class Arxiv(ResourceParseBase):
    def handle(self, soup, data=None):
        return {
            'image' : f"https://arxiv.org{data.get('image')}",
            'author':"; ".join(list(map(lambda x: x['content'], 
                                            soup.find_all('meta', {'name':'citation_author'}))))}

class Amazon(ResourceParseBase):
    def handle(self, data):
        d = {}
        try:
            image_tag = self.soup.find("img", {"id": "landingImage"})   
            if image_tag:
                d['image'] = image_tag['src']
            description_div = self.soup.find("div", {"id": "productDescription"})   
            if description_div:
                d['description'] = description_div.get_text(strip=True)
            title_tag = self.soup.find("span", {"id": "productTitle"})   
            if title_tag:
                d['title'] = title_tag.get_text(strip=True)  
 
        except:
            pass
        finally:
            return d
        


class GoodReads(ResourceParseBase):
    def handle(self, data):
        d = {}
        description_div = self.soup.find("div", class_="BookPageMetadataSection__description")
        if description_div:
            d['description'] = description_div.text.strip()
        title = self.soup.find("div", class_="BookPageTitleSection__title")
        if title:
            d['title'] = title.text
        author_div = self.soup.find("div", class_="ContributorLinksList")
        if author_div:
            d['author'] = "; ".join([t.text for t in author_div.find_all('span', class_='ContributorLink__name')])
        return d
 
class GoogleScholarBib(ResourceParseBase):
    def handle(self, data):
        bdata =  parse_bibtex(self.soup.text)
        data['title'] = bdata['content']['title']
        data['author'] = bdata['content']['author']
        data['type'] = bdata['type']
        for f in ['publisher', 'journal', 'volume', 'pages', 'number', 'year']:
            data[f] = bdata['content'].get(f)
    
        """image is whatever resource we have for the type"""

        return data
 
#test nature and other journals 
 
PROVIDERS = {
    "arxiv.org"  : Arxiv(),
    "www.amazon.com" : Amazon(),
    "www.goodreads.com" : GoodReads(),
    "scholar.googleusercontent.com": GoogleScholarBib()
}


def update_config():
    """add database stuff to the providers"""
    pass
