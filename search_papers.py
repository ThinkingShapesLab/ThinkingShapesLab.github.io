import requests
from bs4 import BeautifulSoup
import urllib.parse
import sys
import time

def search(query):
    # Using a slightly different approach for Google Search
    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        r = requests.get(url, headers=headers, timeout=10)
        # print(f"Status: {r.status_code}")
        soup = BeautifulSoup(r.text, 'html.parser')
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('/url?q='):
                link = href.split('/url?q=')[1].split('&')[0]
                link = urllib.parse.unquote(link)
                if 'google.com' not in link:
                    links.append(link)
            elif href.startswith('http'):
                if 'google.com' not in href:
                    links.append(href)
        return links
    except Exception as e:
        print(f"Error searching: {e}")
        return []

def validate(url):
    try:
        r = requests.get(url, allow_redirects=True, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        return r.status_code == 200
    except:
        return False

papers = [
    "Reconstructing Functional 3D Scenes from Egocentric Interaction Videos (FunRec)",
    "SpaceControl: Introducing Test-Time Spatial Control to 3D Generative Modeling",
    "SuperDec: 3D Scene Decomposition with Superquadric Primitives",
    "OpenFunGraph: Open-Vocabulary Functional 3D Scene Graphs",
    "SceneFun3D: Fine-Grained Functionality and Affordance Understanding in 3D Scenes",
    "OpenMask3D: Open-Vocabulary 3D Instance Segmentation",
    "Mask3D: Mask Transformer for 3D Semantic Instance Segmentation"
]

for paper in papers:
    print(f"Paper: {paper}")
    links = search(paper + " project page")
    found = False
    
    # Heuristic for finding the project page
    best_link = None
    for link in links:
        # Check if title or acronym is in URL
        title_words = paper.lower().split()
        acronym = ""
        if "(" in paper and ")" in paper:
            acronym = paper.split("(")[1].split(")")[0].lower()
        
        is_valuable = any(x in link.lower() for x in [acronym, "github.io", "project", "research"])
        is_valuable = is_valuable and not any(x in link.lower() for x in ["arxiv.org", "scholar.google", "youtube.com", "twitter.com"])
        
        if is_valuable:
             if validate(link):
                 best_link = link
                 break
    
    if not best_link:
        # Fallback to any github.io or paper-like site
        for link in links:
            if "github.io" in link or "github.com" in link:
                if validate(link):
                    best_link = link
                    break
                    
    if best_link:
        print(f"URL: {best_link}")
    else:
        print("URL: Not found")
    print("-" * 20)
    time.sleep(1) # Be nice
