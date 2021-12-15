#!/usr/bin/python3

import datetime
import time
import requests
from bs4 import BeautifulSoup
import os
import errno
import csv
import sys

def grep_esdx():
#while True:
	try :
		with open('list_sta', newline = '') as sta:                                                                                          
			list_sta_reader = csv.reader(sta, delimiter='\t')
			for detilSta in list_sta_reader:
				#print(detilSta)
				#print(detilSta[1])

				filename = "repo/"+detilSta[0]+"/lastgrep_"+detilSta[0]+".txt"
				if not os.path.exists(os.path.dirname(filename)):
					try:
						os.makedirs(os.path.dirname(filename))
					except OSError as exc: # Guard against race condition
						if exc.errno != errno.EEXIST:
							raise
				try :
					last_grep = open("repo/"+detilSta[0]+"/lastgrep_"+detilSta[0]+".txt", "r")
					param_text_old = last_grep.read()
					last_grep.close()
				except :
					last_grep = open("repo/"+detilSta[0]+"/lastgrep_"+detilSta[0]+".txt", "x")
					last_grep = open("repo/"+detilSta[0]+"/lastgrep_"+detilSta[0]+".txt", "r")
					param_text_old = last_grep.read()
					last_grep.close()
				
				# Collect and parse first page
				page = requests.get(detilSta[1])
				#print(page)
				soup = BeautifulSoup(page.text, 'html.parser')
				#print(soup)

				param_text = soup.find("pre").find(text=True)
				#print(param_text)
				if param_text_old != param_text: 
					#appending (repo)
					repo = open("repo/"+detilSta[0]+"/repo_"+detilSta[0]+".txt", "a")
					repo.write(param_text)
					repo.close()
					stat = "Repo "+detilSta[0]+" tercolong"+" jam "+str(datetime.datetime.now())
					print(str(datetime.datetime.now()))

					#appending (nyolong.log)
					log = open("nyolong.log", "a")
					log.write("\n"+stat)
					log.close()

				#overwrite (last event)
				lastG = open("repo/"+detilSta[0]+"/lastgrep_"+detilSta[0]+".txt", "w")
				lastG.write(param_text)
				lastG.close()
			time.sleep(10)
	except :
		text_err = "Error bro "+" jam "+str(datetime.datetime.now())
		#appending (err.log)
		err = open("err.log", "a")
		err.write("\n"+text_err)
		err.close()
		#time.sleep(30)
		time.sleep(10)
		pass
	
if __name__ == '__main__':
	grep_esdx()
	os.execv(__file__, sys.argv)

