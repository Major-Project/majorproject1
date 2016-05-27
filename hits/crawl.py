#!/usr/bin/python
#matt garrett
#cse 417

#crawl is a python implementation of a simple wikipedia crawler to explore
#the wikipedia graph.  It is built on top of BeautifulSoup.

import sys
import urllib2
from bs4 import BeautifulSoup
import re

#the regex to match an internal wikipedia link
wikiLink = re.compile("^/wiki/[^:#]*$")

#accepts a target url of the form /wiki/HITS_algorithm or /wiki/Ferrari
#accepts a depth the current url is at
#accepts a depth to stop searching at
#accepts a list of lists of documents to append to
#accepts a corrisponding list of outbound links to append to
#accepts a list of problem urls to append to
#explores the target url, stopping at depth stop, storing all results
#in documents, outbound, and problems
def explore(url, depth, stop, documents, outbound, problems):
    if (url not in documents and depth < stop):
        print("adding = " + url + ", documents size = " + str(len(documents)))
        documents.append(url)
        outbound.append([])
        fullUrl = "http://en.wikipedia.org" + url
        
        #User-Agent must be set because wikipedia blocks crawlers
        request = urllib2.Request(fullUrl, headers={"User-Agent" : "Superman"})
        try:
            socket  = urllib2.urlopen(request)
            page    = socket.read()
            socket.close()
            
            #cuts off references section of the page
            page    = re.sub('id="References.*', '', page)
            soup    = BeautifulSoup(page)

            #this div is the article itself, it is what we want to search
            article = soup.find("div", {"id" : "mw-content-text"})
            index = documents.index(url)
            if article:
                for link in article.find_all("a", {"href" : wikiLink}):
                    if (link.get("href") not in documents):
                        explore(link.get("href"), depth + 1, stop, documents, outbound, problems)
                        outbound[index].append(link.get("href"))
            else:
                documents.pop()
                outbound.pop()
                problems.append(url)

        #didn't want to deal with exceptions breaking my code while
        #4 hours into crawling, this fixes that problem
        except IOError, (errno):
            print "HUGE ERROR MOVING ON"
            documents.pop()
            outbound.pop()

#accpets a list of documents and a corresponding list of lists of
#outbound urls, writes the adjacency list to the specified outFile
def dumpLists(documents, outbound, outFile):
    f = open(outFile, "w")
    for index, url in enumerate(documents):
        f.write(url + ":\n")
        for link in outbound[index]:
            f.write("   " + link + "\n")

#accepts a list of urls and writes them to sdtout
def dumpProblems(problems):
    print("Problems")
    for url in problems:
        print("   " + url)

#prints usage information for crawl
def showUsage():
    print("Crawl Usage:")
    print("   crawl targetUrl searchDepth outFile")
    print("Examples:")
    print("   crawl /wiki/HITS_algorithm 3 hits.dump")
    print("   crawl /wiki/Ferrari 5 ferrari.dump")

#yeah I'm used to java, learning python is weird
def main():
    if (len(sys.argv) < 4):
        showUsage()
    else:
        url = sys.argv[1]
        stop = int(sys.argv[2])
        outFile = sys.argv[3]
        documents = []
        outbound = []
        problems = []
        explore(url, 0, stop, documents, outbound, problems)
        print(outbound)
        print("====================================================")
        print(documents)
        dumpLists(documents, outbound, outFile)
        dumpProblems(problems)

main()
