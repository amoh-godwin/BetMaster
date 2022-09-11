import requests

from extract_functions import extract_footlive_notstarted

req = requests.get('http://www.footlive.com/')
print(req.text)

