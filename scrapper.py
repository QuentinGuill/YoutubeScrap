import requests
from bs4 import BeautifulSoup
import json

headers= {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}
URL = "https://www.youtube.com/watch?v=fmsoym8I-3o"
page = requests.get(URL, headers=headers)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find("body", dir="ltr")
res_string = str(results)
rescut = res_string.split("var ytInitialPlayerResponse = ")
rescut2 = rescut[1].split(";</script>")

r = json.loads(rescut2[0])

f = open("demofile2.json", "w")
f.write(json.dumps(r, indent=4))
f.close()

print(r["videoDetails"]["videoId"])
print(r["videoDetails"]["title"])
print(r["videoDetails"]["author"])
print(r["videoDetails"]["shortDescription"])
