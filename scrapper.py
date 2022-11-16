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

def find_engagementPanel(json_desc):
	i=0
	for json_line in json_desc:
		if (json_line["engagementPanelSectionListRenderer"]["content"].get("structuredDescriptionContentRenderer") == None):
			i=i+1
		else:
			return i


def find_segmentedButton(json_desc):
	i=0
	for json_line in json_desc:
		if (json_line.get("segmentedLikeDislikeButtonRenderer") == None):
			i=i+1
		else:
			return i


def get_video_description(json_video_data, jVideo):
	json_desc = json_video_data["engagementPanels"]

	i = find_engagementPanel(json_desc)

	json_desc = json_desc[i]["engagementPanelSectionListRenderer"]["content"]["structuredDescriptionContentRenderer"]["items"][1]["expandableVideoDescriptionBodyRenderer"]["descriptionBodyText"]["runs"]
	

	print(json_desc[0])
	print(jVideo)
	jVideo["description"] = json_desc[0]

	jTab = []
	for json_line in json_desc:
		if (json_line.get("navigationEndpoint") != None):
			temp_url = json_line["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"]

			if not("https://www.youtube.com" in temp_url):
				temp_url = "https://www.youtube.com"+temp_url

			jTab.append({ "url" : temp_url })

	jVideo["url_list"] = jTab

	print(jVideo)
	return jVideo


def get_video_likes(json_video_data, jVideo):
	json_desc = json_video_data["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"][0]["videoPrimaryInfoRenderer"]["videoActions"]["menuRenderer"]["topLevelButtons"]

	i = find_segmentedButton(json_desc)
	jVideo["j'aimes"]  = json_desc[i]["segmentedLikeDislikeButtonRenderer"]["likeButton"]["toggleButtonRenderer"]["defaultText"]["accessibility"]["accessibilityData"]["label"].split("\u00a0")[0]

	return jVideo

def create_output():
	dictionary_res = { "video_list": [] }

	return dictionary_res


def increment_output(jVideo, dictionary_res):
	dictionary_res["video_list"].append(jVideo)

	return dictionary_res


def finish_output(dictionary_res):
	output = open("output.json", "w")

	json_res = json.dumps(dictionary_res, indent=4)
	output.write(json_res)

	output.close()


def get_data(url):
	headers= {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}

	page = requests.get(url, headers=headers)

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

	return [r,r2]


def analyse_videos(list_video):
	res = create_output()

	for vid in list_video:
		url="https://www.youtube.com/watch?v="+vid
		print(url)
		data = get_data(url)
		jVideo = get_video_info(data[0])
		jVideo = get_video_likes(data[1], jVideo)
		jVideo = get_video_description(data[1], jVideo)

		res = increment_output(jVideo, res)

	finish_output(res)


def find_urls():
	inputs = open("input.json", "r")

	json_in = json.load(inputs)

	inputs.close()

	urls = []
	
	for u in json_in["videos_id"]:
		urls.append(u)

	return urls


def main():
	urls = find_urls()
	analyse_videos(urls)



main()