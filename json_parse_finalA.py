import re
import csv
import json
from bs4 import CData
from geotext import GeoText
from bs4 import BeautifulSoup

# a counter to ensure that loops only execute as needed could also be a bool
var = 0

# this json output is from an MySQL export of crawler.db 
loaded_json = json.load(open("sites.json"))

# splits out json fields
for x in loaded_json:	
	domain = x['domain']  	
	site = x['url']
	data = x['content']		
	
	# puts content json field into a bs object	
	soup = BeautifulSoup(data, 'html.parser')
	
	# puts soup into GeoText object	
	places = GeoText(data)
		
	# removes script and style tags	
	for script in soup(["script", "style"]):
    		# keep from looping gratuitously 
    		if var < 2:
			script.extract()

	# removes CDATA scripts
	for cd in soup.findAll(text=True):
			if isinstance(cd, CData):
				cd.replaceWith('')	
				# the loop made it here so increment counter by 1
				var += 1

	# still need to get rid of other pesky scripts
	   
	# location block    
	# gets country information - lots of false positives here
	for p in places.country_mentions: 
    		country = []
    		country.append(p)
    	
    # gets city information - fales positives?
    	for c in places.cities:
    			city = []
    			city.append(c)    
	
	# gets image URLs from each page
	for image in soup.findAll("img"):
			images_URL = []
			images_URL.append(image)
											
	# extracts all text 					
	text = soup.get_text(strip=True)
	
	# removes commas in the text that may confuse a csv
	text = text.replace(",", " ")
		
	# removes lines and spaces, then rejoins all the text
	lines = (line.strip() for line in text.splitlines())
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	text = '\n'.join(chunk for chunk in chunks if chunk)
	
	# gets dates from each page 
	for year in range(1950,2050): 
    		if text.count(str(year)):
    			dates_info = []
    			dates_info.append(year)
	
	# for debugging, how many times is the loop running?
	print var 
		
	# each field put into an object for writing to their own column			
	rows = (str(domain.encode('utf8')) , str(site.encode('utf8')) , str(images_URL).strip('[]'), str(dates_info).strip('[]'), str(country).strip('[]'), str(city).strip('[]'), str(text.encode('utf8')))

	#writes text only content to file for key word corpus
	#outF = open("myOutFile.txt", "a")
	#outF.writelines(str(rows)) + '\n')

	#write content to csv file NEED TO REMOVE , FROM TEXT
	outF = open("text.csv", "a")
	outF.writelines(str(rows).strip('()') + '\n')


