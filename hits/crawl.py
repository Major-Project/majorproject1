
import sys
import urllib2
from bs4 import BeautifulSoup
import re

wikiLink = re.compile("^/wiki/[^:#]*$")

def explore(url, depth, stop, documents, outbound, problems):
    if (url not in documents and depth < stop):
        print("adding = " + url + ", documents size = " + str(len(documents)))
        documents.append(url)
        outbound.append([])
        fullUrl = "http://en.wikipedia.org" + url
        
        request = urllib2.Request(fullUrl, headers={"User-Agent" : "Superman"})
        try:
            socket  = urllib2.urlopen(request)
            page    = socket.read()
            socket.close()
            
            page    = re.sub('id="References.*', '', page)
            soup    = BeautifulSoup(page)

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

        except IOError, (errno):
            print "HUGE ERROR MOVING ON"
            documents.pop()
            outbound.pop()

def dumpLists(documents, outbound, outFile):
    f = open(outFile, "w")
    for index, url in enumerate(documents):
        f.write(url + ":\n")
        for link in outbound[index]:
            f.write("   " + link + "\n")

def dumpProblems(problems):
    print("Problems")
    for url in problems:
        print("   " + url)

def showUsage():
    print("Crawl Usage:")
    print("   crawl targetUrl searchDepth outFile")
    print("Examples:")
    print("   crawl /wiki/HITS_algorithm 3 hits.dump")
    print("   crawl /wiki/Ferrari 5 ferrari.dump")

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
