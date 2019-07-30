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
import urllib.request
import urllib.error
import urllib.parse


def get_soup(url, header):
    # return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),
    # 'html.parser')
    return BeautifulSoup(urllib.request.urlopen(
        urllib.request.Request(url, headers=header)),
        'html.parser')


parser = argparse.ArgumentParser()
parser.add_argument('query', type=str, help='What to search Bing for?')
parser.add_argument('-d', '--dir', type=str,
                    default='~/Pictures', help='Where to store the pics?')
parser.add_argument('-s', '--save', action='store_true', help='Store the images locally.')
args = parser.parse_args()

if not os.path.exists(args.dir):
    print("Warning: the path you've specified doesn't exist:")
    print(args.dir)
    exit(2)

query = urllib.parse.quote(args.query)
url2 = "http://www.bing.com/images/search?q={}&qft=+filterui:imagesize-custom_400_600&FORM=HDRSC2".format(
    query)
# I got this link by checking network requests made by Bing while you scroll down their page...
url = "https://www.bing.com/images/async?q={}&first={}&count=35&relp=35&qft=+filterui%3aimagesize-custom_400_600+filterui%3aphoto-photo&scenario=ImageBasicHover&datsrc=N_I&layout=RowBased&mmasync=1&dgState=x*0_y*0_h*0_c*6_i*71_r*13&IG=83897C3217364C41BBE00B0CE65C7782&SFX=3&iid=images.5947"

print("Scraping URL:", url.format(query, 1))


total = 100
first = 1
ActualImages = {}  # contains the link for Large original images, type of  image
while len(ActualImages) < total:
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    soup = get_soup(url.format(query, first), header)
    for a in soup.find_all("a", {"class": "iusc"}):
        # print a
        m = json.loads(a['m'])
        turl = m["turl"]
        murl = m["murl"]

        image_name = urllib.parse.urlsplit(murl).path.split("/")[-1]
        print("Found image:", image_name)
        ActualImages[image_name] = turl
    first += 35

print("Found total", len(ActualImages), "images")
outdir = os.path.join(args.dir, args.query.replace(' ', '_').lower())
os.makedirs(outdir, exist_ok=True)

with open(os.path.join(outdir, 'links.json'), 'w') as o:
    json.dump(ActualImages, o, indent=2)

if not args.save:
    exit(0)

name_stub = args.query.replace(' ', '_') + "_{:04d}.{}"
# save the images
for i, (image_name, turl) in enumerate(ActualImages.items()):
    try:
        raw_img = urllib.request.urlopen(turl).read()
    except Exception as e:
        print("could not load : " + image_name)
        print(e)
        continue

    write_name = name_stub.format(i, os.path.splitext(image_name)[1])
    with open(os.path.join(outdir, write_name), 'wb') as f:
        f.write(raw_img)
