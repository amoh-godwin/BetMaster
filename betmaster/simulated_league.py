
import requests
import json

req = requests.get('https://lsc.fn.sportradar.com/common/en/Etc:UTC/gismo/sport_matches/1/2022-09-13')
conts = req.text

with open('13.txt', 'w') as fp:
    fp.write(conts)

print(json.loads(conts))
