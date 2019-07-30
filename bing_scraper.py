# the code is ripped off Stephen Houser's gist:
# https://gist.github.com/stephenhouser/c5e2b921c3770ed47eb3b75efbc94799

from bs4 import BeautifulSoup
import requests
import re
import sys
import os
import http.cookiejar
import argparse
import json
import urllib.request, urllib.error, urllib.parse

def get_soup(url,header):
    #return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),
    # 'html.parser')
    return BeautifulSoup(urllib.request.urlopen(
        urllib.request.Request(url,headers=header)),
        'html.parser')

parser = argparse.ArgumentParser()
parser.add_argument('query', type=str, help='What to search Bing for?')
parser.add_argument('-d', '--dir', type=str, default='~/Pictures', help='Where to store the pics?')
args = parser.parse_args()

if not os.path.exists(args.dir):
    print("Warning: the path you've specified doesn't exist:")
    print(args.dir)
    exit(2)

query = urllib.parse.quote(args.query)
url="http://www.bing.com/images/search?q={}&FORM=HDRSC2".format(query)
print("Scraping URL:", url)

header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
soup = get_soup(url,header)

ActualImages=[]# contains the link for Large original images, type of  image
for a in soup.find_all("a",{"class":"iusc"}):
    #print a
    m = json.loads(a['m'])
    turl = m["turl"]
    murl = m["murl"]

    image_name = urllib.parse.urlsplit(murl).path.split("/")[-1]
    print("Found image:", image_name)

    ActualImages.append((image_name, turl, murl))

print("Found total" , len(ActualImages),"images")

outdir = os.path.join(args.dir, args.query.replace(' ', '_').lower())
os.makedirs(outdir, exist_ok=True)

# name_stub = args.query.replace(' ', '_')
# save the images
for i, (image_name, turl, murl) in enumerate(ActualImages):
    try:
        raw_img = urllib.request.urlopen(turl).read()
    except Exception as e:
        print("could not load : " + image_name)
        print(e)
        continue

    with open(os.path.join(outdir, image_name), 'wb') as f:
        f.write(raw_img)
exit(1)