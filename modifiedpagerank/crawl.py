#!/usr/bin/python
import sys
import urllib2
from bs4 import BeautifulSoup
import re

#the regex to match an internal wikipedia link
wikiLink = re.compile("^/wiki/[^:#]*$")

def explore(url, depth, stop, documents, outbound, problems,visibility,position):
    if (url not in documents and depth < stop):
        print("adding = " + url + ", documents size = " + str(len(documents)))
        documents.append(url)
        outbound.append([])
        visibility.append([])
        position.append([])
        boldocument = {}
        italicdocument = {}
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
            	for boldtag in article.find_all("b"):
            		for boldlink in boldtag.find_all("a"):
            			boldocument[boldlink.get("href")] = boldlink
                for italictag in article.find_all("i"):
                    for italiclink in italictag.find_all("a"):
                        italicdocument[italiclink.get("href")] = italiclink
            	alllinks = article.find_all("a",{"href" : wikiLink})
            	totallinks = len(alllinks)
                for count,link in enumerate(alllinks):
                    if (link.get("href") not in documents):
                    	visibility[index].append(1)
                    	if (link.get("href") in boldocument):
							visibility[index][-1] = 3
                        elif(link.get("href") in italicdocument):
                            visibility[index][-1] = 2
                        if(count < (totallinks/2)):
							position[index].append(2)
                        else:
							position[index].append(1)
                        explore(link.get("href"), depth + 1, stop, documents, outbound, problems, visibility,position)
                        outbound[index].append(link.get("href"))
			
            else:
                documents.pop()
                outbound.pop()
                problems.append(url)

        except IOError, (errno):
            print "HUGE ERROR MOVING ON"
            documents.pop()
            outbound.pop()

#accpets a list of documents and a corresponding list of lists of
#outbound urls, writes the adjacency list to the specified outFile
def dumpLists(documents, outbound, outFile,visibility,position): #avani
    f = open(outFile, "w")
    for index, url in enumerate(documents):
        f.write(url + ":\n") #avani
        boldlink = visibility[index]
        posvalue = position[index]
        for count, link in enumerate(outbound[index]):
            f.write("   " + link + "   " + str(posvalue[count]) + "   " + str(boldlink[count]) + "\n") #avani

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
    print("  python crawl.py /wiki/HITS_algorithm 3 pagerank.dump")
    print("  python crawl.py /wiki/Ferrari 5 pagerank.dump")

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
        vis = []
        position = []
        explore(url, 0, stop, documents, outbound, problems, vis, position) #avani
        dumpLists(documents, outbound, outFile, vis, position)
        #dumpProblems(problems)

main()
