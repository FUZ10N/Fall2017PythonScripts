#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#AUTHOR: FUZ10N
#DATE: FALL 2017

#Please note that to run without errors, the path to writing the returned & gathered output needs to be customized based on your own Computer.
#Note that the bs4 library returns occasional parsing errors when running on a Windows 8 environment. The script performs flawless on Windows 10 and Linux (Tested at least on latest Kali distro). 
#Ensure that all file paths are updated for script to save files properly.


#First necessary python libraries for the script to run as designed are imported. 

from os import system as call
import sys
import urllib2	 
import codecs
import datetime
import re

#Try and except is placed around the importing of the requests, bs4, and tweepy libraries as they do not come installed with Python 2.7 on windows. The path to pip may need to be altered to perform the download and install of the libraries. Additionally, pip may need to be installed first, if the version of Python is <= 2.7.9. 
try:
	import requests
	from bs4 import BeautifulSoup
	import tweepy
except ImportError:
	print "[ - ]  Please install the 'requests' and 'bs4' and the 'tweepy' module using pip as it appears it is not installed."
	print "[ - ]  Use the following command without quotations in your command prompt to do so."
	print "[ - ]  'C:\\Python27\\Scripts\\pip.exe install requests' and 'C:\\Python27\\Scripts\\pip.exe install bs4' and 'C:\\Python27\\Scripts\\pip.exe install tweepy"
	print "[ - ]  Note: You may also need to download 'pip' if it has not been installed on this system. Please google 'pip install python' for more information and instructions."
	sys.exit(1)
	
#The main menu function for our script is defined utilizing a while loop to keep script running despite any inproper user input. 
def menu():
	
	menuselection = 0
	while menuselection == 0:
		print "[ - - - Open Source News Intel V1.0 - - - ]"
		print "[ + ]  Please enter a valid option '1' through '7' and press enter to continue..."
		print "[ + ]  1. News Search (Russian Language)"
		print "[ + ]  2. News Search (English Language)"
		print "[ + ]  3. Twitter Search (Russian Language)"
		print "[ + ]  4. Twitter Search (English Language)"
		print "[ + ]  5. News & Twitter Search (Russian Language)"
		print "[ + ]  6. News & Twitter Search (English Language)"
		print "[ - ]  7. EXIT"
		selection = raw_input("Option: ")

		if selection == "1":
			news_search_Russian()
			menuselection = "99"
			
		if selection == "2":
			news_search_English()
			menuselection = "99"
			
		if selection == "3":
			twitter_Russian()
			menuselection = "99"
			
		if selection == "4":
			twitter_English()
			menuselection = "99"
			
		if selection == "5":
			news_search_Russian()
			twitter_Russian()
			menuselection = "99"
			
		if selection == "6":
			news_search_English()
			twitter_English()
			menuselection = "99"
		
		if selection == "7":
			print "Exiting..."
			sys.exit(1)
			menuselection = "99"
			
		if selection != "1" and selection != "2" and selection != "3" and selection != "4" and selection != "5" and selection !="6":
			call('cls')
			print "[ - ]  ERROR. Incorrect option selected, please try again."


			
def news_search_Russian():	
	
#Despite it's title, the script is only able to handle ASCII characters as input. While output is in Russian, python 2.7 has trouble working with non ASCII characters. 

#A try and except is used if an error occurs while scraping data or if non-ASCII characters are entered as a 'keyword'. 	
	try:
		Keywords = raw_input('Please Enter A Keyword to Search News Sites (English Only): ') #Only a single keyword is accepted
		ria_news = 'https://ria.ru/search/?query='+Keywords
		riapage = urllib2.urlopen(ria_news)
		newspage = BeautifulSoup(riapage, 'html.parser')
		ria_results = newspage.find_all('span', attrs={'class': 'b-list__item-title'})
		headlinesria = [title.text for title in ria_results] #Returns only the text data -- no other coding, etc. for all items in the list. 
		#BeautifulSoup is used to parse the html data returned from the called page. The find_all command looks through the html source code and finds all occurrences of returned results (Headlines above, dates, summaries, and links below) based on the specified HTML/CSS code. 
		
		#datetime library is used to pull the time from the user's computer. This feature allows for multiple searches to occur without writing over previoulsy returned data and for easy tracking of when searches occured for any comparative purposes. 
		
		now = datetime.datetime.now()
		filename = now.strftime("%Y-%m-%d-%H %M") #datetime module is utilized to pull current time/date for organizational purposes and unique filenaming. 
		File = codecs.open("C:\\Path-To-Save-File\\RNS-"+filename+".txt", "w", "utf-8") #Change file path
		#Codecs is called to help write output in the cyrillic alphabet. 
		
		File.write("News Search (Russian Language)"+"\r\n"+"Keyword Searched: "+Keywords+"\r\n"+"Date & Time of Search: ")
		File.write(now.strftime("%Y-%m-%d %H:%M"))
		File.write("\r\n"+"\r\n"+"Articles from RIA Novosti:"+"\r\n"+"\r\n")
			
		#Returns the date the articles were published. 
		ria_resultsdate = newspage.find_all('div', attrs={'class': 'b-list__item-date'})
		ria_dates = [date.text for date in ria_resultsdate]
		
		#Returns a brief summary of the article as found on the search results page. 
		ria_summary = newspage.find_all('div', attrs={'class': 'b-list__item-announce'})
		ria_summaries = [summary.text for summary in ria_summary]
		
		links = []
		
		#A reg expression is used to pull all URLS with '.html' -- which was unique to the RIA News page.
		for link in newspage.findAll('a', attrs={'href': re.compile(".html")}):
			links.append(link.get('href')) #Results are appended to the empty list "links" 
	
		ria_links = [x for x in links if "doc" not in x] #Since other URLS were returned that did not correspond to the news articles found in the search results, all urls that contained 'doc' in a path, etc. were removed from the list.
		ria_links2 = ria_links[1:21] #Unique to RIA, each pulled list had 1 link at the top and 3 at the bottom of the list that did not correspond to the search results. This code creates a new list of links that only contains those we need for the news articles. 
		
		#Writes and formats data neatly in a text document -- also able to open and view neatly in microsoft word. 
		for a, b, c, d in zip(headlinesria,ria_dates,ria_links2,ria_summaries):
			File.write("Headline: "+a+"\r\n"+"Date Published: "+b+"\r\n"+"URL: http://ria.ru"+str(c)+"\r\n"+"Summary: "+d+"\r\n"+"\r\n")

	
		
		
		bbc_news = 'http://www.bbc.com/russian/search/?q='+Keywords
		bbcpage = urllib2.urlopen(bbc_news)
		newspagebbc = BeautifulSoup(bbcpage, 'html.parser')
		bbc_results = newspagebbc.find_all('a', attrs={'class': 'hard-news-unit__headline-link'})
		headlinesbbc = [title.text for title in bbc_results]
		File.write("\r\n"+"--"*70+"\r\n"+"\r\n"+"\r\n"+"Articles from BBC News Russian Service:"+"\r\n"+"\r\n")
		
		bbc_resultsdate = newspagebbc.find_all('div', attrs={'class': 'date date--v2'})
		bbc_dates = [date.text for date in bbc_resultsdate]
		
		bbc_summary = newspagebbc.find_all('p', attrs={'class': 'hard-news-unit__summary'})
		bbc_summaries = [summary.text for summary in bbc_summary]
		
		linksbbc = []
		
		for link in newspagebbc.findAll('a', attrs={'href': re.compile("www.bbc.co.uk/russian/")}): #Unique reg expression used for BBC site to weed out unneeded links. 
			linksbbc.append(link.get('href'))
	
		for d, e, f, g in zip(headlinesbbc,bbc_dates,linksbbc,bbc_summaries):
			File.write("Headline: "+d+"\r\n"+"Date Published: "+e+"\r\n"+"URL: "+f+"\r\n"+"Summary: "+g+"\r\n"+"\r\n")
			
		Read = raw_input("[ + ] Articles Scraped Successfully --- Press Enter to Exit: ")	
	except TypeError:	
		call ('cls')
		print "[ - ] Error Scraping Headline"
		menu()
	except urllib2.URLError:
		call ('cls')
		print "[ - ] Error: Please Enter Only a Single Keyword"
		menu()

	

def news_search_English():	
	try:	
		Keywords = raw_input('Please Enter Keyword to Search News Sites (English Only): ')
		
		now = datetime.datetime.now()
		filename = now.strftime("%Y-%m-%d-%H %M")
		File = codecs.open("C:\\Path-To-Save-File\\ENS-"+filename+".txt", "w", "utf-8") #Change file path
		
		
		rfe_news = 'https://www.rferl.org/s?k='+Keywords
		rfepage = urllib2.urlopen(rfe_news)
		newspagerfe = BeautifulSoup(rfepage, 'html.parser')
		rfe_results = newspagerfe.find_all('span', attrs={'class': 'title'})
		headlinesrfe = [title.text for title in rfe_results]
		
		File.write("News Search (English Language)"+"\r\n"+"Keyword Searched: "+Keywords+"\r\n"+"Date & Time of Search: ")
		File.write(now.strftime("%Y-%m-%d %H:%M"))
		File.write("\r\n"+"\r\n"+"Articles from Radio Free Euriope:"+"\r\n"+"\r\n")
			
		rfe_resultsdate = newspagerfe.find_all('span', attrs={'class': 'date'})
		rfe_dates = [date.text for date in rfe_resultsdate]
		
		#The nameing conventions for RFE in the source code were very similar and intertwined, resulting in too much data being returned. This decompose method of BeautifulSoup will remove all unecessary html and data that we do not want in the summaries. 
		for span in newspagerfe.find_all("span", attrs={'class': 'date'}):
			span.decompose()
		for span in newspagerfe.find_all("span", attrs={'class': 'title'}):
			span.decompose()
			
			
		rfe_summary = newspagerfe.find_all('div', attrs={'class': 'content'})
		rfe_summaries = [summary.text for summary in rfe_summary]
		
		linksrfe = []
		
		for link in newspagerfe.findAll('a', attrs={'href': re.compile("/a/")}):
			linksrfe.append(link.get('href'))
			
		for a, b, c, d in zip(headlinesrfe,rfe_dates,linksrfe,rfe_summaries):
			File.write("Headline: "+a+"\r\n"+"Date Published: "+b+"\r\n"+"URL: https://www.rferl.org"+str(c)+"\r\n"+"Summary: "+d+"\r\n"+"\r\n")
		
		kyiv_news = 'https://www.kyivpost.com/?s='+Keywords
		kyivpage = urllib2.urlopen(kyiv_news)
		newspagekyiv = BeautifulSoup(kyivpage, 'html.parser')
		kyiv_results = newspagekyiv.find_all('h2', attrs={'class': 'title'})
		headlineskyiv = [title.text for title in kyiv_results]
		File.write("\r\n"+"--"*70+"\r\n"+"\r\n"+"\r\n"+"Articles from The Kyiv Post:"+"\r\n"+"\r\n")
		
		for h2 in newspagekyiv.find_all("h2", attrs={'class': 'title'}):
			h2.decompose() #Removes all unecessary 'h2' html headers to return only necessary data. 
	
		kyiv_resultsdate = newspagekyiv.find_all('div', attrs={'class': 'pe-desc'})
		kyiv_dates = [date.text for date in kyiv_resultsdate]
		kyiv_dates2 = [x.rstrip('\r\n') and x.strip('\r\n') for x in kyiv_dates] #Removes whitespace around dates.
		kyiv_dates3 = ["".join(x.split()) for x in kyiv_dates2] #Helped to remove the pagebreaks that were not removed by the .rstrip and .strip methods.
			
		linkskyiv = []
		
		for link in newspagekyiv.findAll('a', attrs={'href': re.compile("https://www.kyivpost.com/")}):
			linkskyiv.append(link.get('href'))	
		linkskyiv2 = linkskyiv[36:72] #This site contained a static number of URLS both before and after the search results were returned. This helped concentrate on only the links for the news articles we want. 
		del linkskyiv2[1::2] #This site included links to the author of each article that was returned in our list. This removes them (every other link) from the list. 
	
	
		for d, e, f in zip(headlineskyiv,kyiv_dates3,linkskyiv2):
			File.write("Headline: "+d+"\r\n"+"Date Published: "+e+"\r\n"+"URL: "+f+"\r\n"+"Summary: None"+"\r\n"+"\r\n")
			
		Read = raw_input("[ + ] Articles Scraped Successfully --- Press Enter to Exit: ")
			
	except TypeError:	
		call ('cls')
		print "[ - ] Error Scraping Headline"
		menu()
	except urllib2.URLError:
		call ('cls')
		print "[ - ] Error: Please Enter Only a Single Keyword"
		menu()
		


def twitter_Russian():
	try:
		Keywords = raw_input('Please Enter A Keyword(s) to Search Twitter (English Only) *FOR BEST RESULTS SEARCH ONLY ONE KEYWORD*: ') #Using the twitter API, multiple keywords can be used per search, but searching only one for the russian language tweets is best to maximize results as cyrilic characters are not acceptable input. 
	#Authentication information needed to access Twitter's API
    #Substitue your own authentication information below
		CONSUMER_KEY = ''
		CONSUMER_SECRET = ''
		ACCESS_KEY = ''
		ACCESS_SECRET = ''
	
		twitterauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		twitterauth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	#Authenticates to twitter API
		twitterapi = tweepy.API(twitterauth)
		twitter_search_results = twitterapi.search(q=Keywords, lang='ru', result_type="recent") #Searches only russian language, recent tweets. 
	
		now = datetime.datetime.now()
		filename = now.strftime("%Y-%m-%d-%H %M")
		File = codecs.open("C:\\Path-To-Save-File\\RTWT-"+filename+".txt", "w", "utf-8") #Change file path
		
		
		File.write("--*Twitter Search (Russian Language)*--"+"\r\n"+"Top Matching Tweets (Recent)"+"\r\n"+"Keyword Searched: "+Keywords+"\r\n"+"Date & Time of Search: ")
		File.write(now.strftime("%Y-%m-%d %H:%M"))
		
			
		for tweet in twitter_search_results:
			File.write("\r\n"+"\r\n"+"TWEET: "+tweet.text+"\r\n"+"\r\n")
	
		print "[ + ] - Twitter Searched Successfully"
		Exit = raw_input("Press Enter to Exit: ")
		
	except TypeError:
		call ('cls')
		print "[ - ] Invalid Keyword Input. Only ASCII Characters are accetped. Please select your option and try again."
		
		menu()
		
def twitter_English():
	try:
		Keywords = raw_input('Please Enter A Keyword(s) to Search Twitter (English Only): ')
	
    #Authentication information needed to access Twitter's API
    #Substitue your own authentication information below
    
		CONSUMER_KEY = ''
		CONSUMER_SECRET = ''
		ACCESS_KEY = ''
		ACCESS_SECRET = ''
	
		twitterauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		twitterauth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	
		twitterapi = tweepy.API(twitterauth)
		twitter_search_results = twitterapi.search(q=Keywords, count=100, lang='en', result_type="recent") #Returns a max of 100 recent tweets in English only.
		
		now = datetime.datetime.now()
		filename = now.strftime("%Y-%m-%d-%H %M")
		File = codecs.open("C:\\Path-To-Save-File\\ETWT-"+filename+".txt", "w", "utf-8") #Change file path
		
		
		File.write("--*Twitter Search (English Language)*--"+"\r\n"+"Top Matching Tweets (Recent)"+"\r\n"+"Keyword Searched: "+Keywords+"\r\n"+"Date & Time of Search: ")
		File.write(now.strftime("%Y-%m-%d %H:%M"))
	
			
		for tweet in twitter_search_results:
			File.write("\r\n"+"\r\n"+"TWEET: "+tweet.text+"\r\n"+"\r\n")
		
		print "[ + ] - Twitter Searched Successfully"
		Exit = raw_input("Press Enter to Exit: ") 
		
	except TypeError:
		call ('cls')
		print "[ - ] Invalid Keyword Input. Only ASCII Characters are accepted. Please selection your option and try again."
		menu()
			

menu()
