#!/usr/bin/env python

from lxml.html import fromstring
import requests
import os

search_url = 'https://teamtreehouse.com/library/q:'
#headers = {'Cookie': ''}
headers = {}

def get_request(url):
    response = requests.get(url)
    etree = fromstring(response.text)
    etree.make_links_absolute(response.url)
    return response.url, etree

def get_session(url):
    response = requests.Session().get(url, headers=headers)
    etree = fromstring(response.text)
    etree.make_links_absolute(response.url)
    return response.url, etree

def main():
    if headers == {}:
	cookie = raw_input('I need the cookie Treehouse gives you after you\'ve logged in.\nFor help finding the cookie view README.\nEnter the cookie now: ')
	headers = {'Cookie': cookie}
    query = raw_input('What would you like to search for?\nEnter now: ')
    #print('This is what you wanted to search for: %s' % query)
    #print('This is what you wanted to search for: '+query+'!')
    url, etree = get_request(search_url+query)

    counter = 0
    for course in etree.xpath(".//div[@data-featurette]/ul//a[@class='card-box']/@href"):
	print(counter, course)
	counter+=1

    selection = raw_input('Enter the number beside course you want: ')
    chosen = etree.xpath(".//div[@data-featurette]/ul//a[@class='card-box']/@href")[int(selection)]
    #print('You chose: %s' % chosen)
    #print('This is what you wanted to search for: '+query+'!')
    url, etree = get_request(chosen+'/stages')
    #response = requests.get('https://teamtreehouse.com/library/'+'github-basics'+'/stages')
    #etree = fromstring(response.text)
    #etree.make_links_absolute(response.url)

    asking = raw_input('Do you want to download every video or be asked for each video?\nEnter "ask" to be asked: ')
    where = raw_input('Where do you want the video saved?\nEnter a directory: ')
    while not os.path.exists(where):
	where = raw_input('That directory isn\'t accessible!\nEnter a directory: ')
    directory = where+'/' if where[-1] != '/' else where
    print('This is where the videos will be saved: '+directory)

    for elem in etree.xpath(".//a"):
	for text in elem.xpath("./p/text()"):
	    if text.replace(':', '').isdigit():
		for vid_link in elem.xpath("./@href"):
		    if asking == 'ask':
			print(vid_link)
			question = raw_input('Do you want to download this video?\nEnter "y" if you do: ')
			if question != 'y':
			    continue
		    print('Starting download...\n'+vid_link)
		    vid_url, vid_etree = get_session(vid_link)
		    video = requests.get(vid_etree.xpath(".//video/source/@src")[0], stream=True)
		    with open(directory+video.url.split("/")[-1].split("?")[0].split(".")[0]+'_'+vid_url.split('/')[-1]+'.'+video.url.split("/")[-1].split("?")[0].split(".")[1], 'wb') as file:
			for chunk in video.iter_content():
			    if chunk:
				file.write(chunk)
		    print('Downloaded '+video.url.split("/")[-1].split("?")[0])

if __name__ == "__main__":
    main()
