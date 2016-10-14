#!/bin/python
'''
crawls the youtube search results for terms specified in terms.txt (one per line). 

usage:

controtube.py [starterm] [searchpage] 

starterm   = the term to resume search
searchpage = the last unfinished search page 

Requires a running elasticsearch instance on port 9200!

'''

from youtube import *
import json
import elasticsearch
import datetime
import sys
import os

CONTROTUBE_INDEX = 'youtube_termscraper'
CONTROTUBE_LOGS  = 'youtube_termlog'
TERMFILE         = 'terms.txt'

client = elasticsearch.Elasticsearch()
now = lambda: datetime.datetime.now().isoformat()


def resume(terms, ignore_logs=False):
	progress = {'Videos_touched':0,'Videos_added':0,'Comments_touched':0,'Comments_added':0}
	for nterm, term in enumerate(terms):
		if not ignore_logs: 
			searchpage = last_state(term)
		else:
			searchpage = None 
		for nvideo, video in enumerate(search(term, expand=True, nextPageToken=searchpage)):
			video['TERM_MATCH'] = term
			video['caption_en'] = get_caption(video, language='en')
			vidres = client.index(CONTROTUBE_INDEX, doc_type='video', id=video['id'], body=video)
			if vidres.get('created',False)==True:
				progress['Videos_added']+=1
			progress['Videos_touched'] += 1
			for ncomment, comment in enumerate(get_comments(video)):
				comres = client.index(CONTROTUBE_INDEX, doc_type='comment', id=comment['id'], body=comment)
				if comres.get('created',False)==True:
					progress['Comments_added'] += 1
				progress['Comments_touched'] +=1
				n = now()
				print("{n} at term {nterm} ({term}) - video {nvideo} - comment {ncomment}".format(**locals()))
				for k,v in progress.items():
					print("{k:20}: {v:10}".format(**locals()))
			log = dict(at=now(),term=term,nterm=nterm, page=video.get('PAGE',''), ncomments=comment,progress=progress)
		client.index(CONTROTUBE_LOGS,doc_type='log', body=log)

def last_state(term):
	try:
		last = client.search(CONTROTUBE_LOGS, 
			body={'filter':{'term':{'term':term}} ,'sort':{'at':'desc'}}).get('hits',{}).get('hits',[])
	except elasticsearch.exceptions.NotFoundError: 
		return None
	if len(last)>0:
		searchpage = last[0]['_source']['page']
		print('resumable at {startterm}, {searchpage}'.format(**locals()))
	else:
		searchpage=None
	return searchpage

def get_terms_CLI():
	if TERMFILE in os.listdir('.'):
		terms = [term.strip() for term in open('terms.txt').readlines() if term.strip()]
	else:
		terms = [term.strip() for term in input("Please list terms separated by ',': ").split(',')]
		with open(TERMFILE,'w') as f:
			for term in terms:
				f.write(term+'\n')
	return terms


if __name__=='__main__':
	terms = get_terms_CLI()
	resume(terms)
	
			
			
