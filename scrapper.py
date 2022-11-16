import requests
from bs4 import BeautifulSoup
import json


def get_video_info(json_video_data):
	jVideo = {
		"id" : json_video_data["videoDetails"]["videoId"],
		"titre" : json_video_data["videoDetails"]["title"],
		"auteur" : json_video_data["videoDetails"]["author"],
	}

	return jVideo


def get_video_description(json_video_data, jVideo):
	json_desc = json_video_data["engagementPanels"][2]["engagementPanelSectionListRenderer"]["content"]["structuredDescriptionContentRenderer"]["items"][1]["expandableVideoDescriptionBodyRenderer"]["descriptionBodyText"]["runs"]
	print(json_desc[0])
	print(jVideo)
	jVideo["description"] = json_desc[0]

	jTab = []
	for json_line in json_desc:
		if (json_line.get("navigationEndpoint") != None):
			jTab.append({ "url" : "https://www.youtube.com"+json_line["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"] })

	jVideo["url_list"] = jTab

	print(jVideo)
	return jVideo


def get_video_likes(json_video_data, jVideo):
	jVideo["j'aimes"] = json_video_data["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"][0]["videoPrimaryInfoRenderer"]["videoActions"]["menuRenderer"]["topLevelButtons"][0]["segmentedLikeDislikeButtonRenderer"]["likeButton"]["toggleButtonRenderer"]["defaultText"]["accessibility"]["accessibilityData"]["label"].split("\u00a0")[0]


	return jVideo

def create_output(jVideo):
	output = open("output.json", "w")

	dictionary_res = { "video_list": [] }
	dictionary_res["video_list"].append(jVideo)
	json_res = json.dumps(dictionary_res, indent=4)

	output.write(json_res)

	output.close()



#header = "{\"video_list\": []}"
#json_res = json.loads(header)
#json_res["video_list"].append(jVideo)

headers= {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}
URL = "https://www.youtube.com/watch?v=fmsoym8I-3o"
#URL = "https://www.youtube.com/watch?v=U3tmOXUkLb4"
page = requests.get(URL, headers=headers)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find("body", dir="ltr")
res_string = str(results)

#ff = open("demofile2.txt", "w")
#ff.write(res_string)
#ff.close()

rescut = res_string.split("var ytInitialPlayerResponse = ")
rescut2 = rescut[1].split(";</script>")

rescut3 = rescut2[2].split("var ytInitialData = ")

#fff = open("demofile3.txt", "w")
#fff.write(rescut3[1])
#fff.close()

r = json.loads(rescut2[0])
r2 = json.loads(rescut3[1])

f2 = open("demofile3.json", "w")
f2.write(json.dumps(r2, indent=4))
f2.close()

jVideo = get_video_info(r)
jVideo = get_video_likes(r2, jVideo)
jVideo = get_video_description(r2, jVideo)
create_output(jVideo)