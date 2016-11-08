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
from elasticsearch.helpers import bulk

TUBESCRAPER_INDEX = 'youtube_termscraper'
TUBESCRAPER_LOGS  = 'youtube_termlog'
TERMFILE          = 'terms.txt'
USE_BUFFER        = True
ELASTIC_TIMEOUT   = 60

client = elasticsearch.Elasticsearch( timeout=ELASTIC_TIMEOUT)
now = lambda: datetime.datetime.now().isoformat()


def resume(terms, ignore_logs=False):
    progress = {'Videos_touched':0,'Videos_added':0,'Comments_touched':0,'Comments_added':0}
    for nterm, term in enumerate(terms):
        if not ignore_logs: 
            searchpage = last_state(term)
        else:
            searchpage = None 
        try: vids = client.search(TUBESCRAPER_INDEX,'video',{'filter':{'term':{'TERM_MATCH':term}},
                    'sort':{'RETRIEVED':'desc'}})['hits']['hits']
        except elasticsearch.exceptions.NotFoundError:
            vids = []
        if len(vids):
            lv = vids[0]
        else:
            lv = {}
        for nvideo, video in enumerate(search(term, expand=True, captions='en', nextPageToken=searchpage)):
            video['TERM_MATCH'] = term
            video['RETRIEVED']  = now()
            vidres = client.index(TUBESCRAPER_INDEX, doc_type='video', id=video['id'], body=video)
            if vidres.get('created',False)==True:
                progress['Videos_added']+=1
            elif lv and video['id']!=lv['_source']['id']: continue
            progress['Videos_touched'] += 1
            ncomment = 0
            combuffer = []
            for ncomment, comment in enumerate(get_comments(video)):
                progress['Comments_touched'] +=1
                if USE_BUFFER : 
                    comment['_id'] = comment['id']
                    comment['_index'] = TUBESCRAPER_INDEX
                    comment['_type']  = 'comment'
                    combuffer.append(comment)
                    continue
                comres = client.index(TUBESCRAPER_INDEX, doc_type='comment', id=comment['id'], body=comment)
                if comres.get('created',False)==True:
                    progress['Comments_added'] += 1

                n = now()
                print("{n} at term {nterm} ({term}) - video {nvideo} - comment {ncomment}".format(**locals()))
                for k,v in progress.items():
                    print("{k:20}: {v:10}".format(**locals()))
            if combuffer:
                n = now()
                bulk(client,combuffer)
                print("{n} at term {nterm} ({term}) - video {nvideo} - comment {ncomment}".format(**locals()))
                for k,v in progress.items():
                    print("{k:20}: {v:10}".format(**locals()))

            log = dict(at=now(),term=term,nterm=nterm, page=video.get('PAGE',''), ncomments=ncomment,progress=progress)
            client.index(TUBESCRAPER_LOGS,doc_type='log', body=log)

def last_state(term):
    try:
        last = client.search(TUBESCRAPER_LOGS, 
            body={'filter':{'term':{'TERM_MATCH':term}} ,'sort':{'at':'desc'}}).get('hits',{}).get('hits',[])
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
    
            
            
