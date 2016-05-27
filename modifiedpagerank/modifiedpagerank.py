#!/usr/bin/python

import sys
import time
from sys import stdout
from math import sqrt
from math import pow

class Document:
    """Represents an HTML document"""
    def __init__(self, url):
        self.url = url
        self.outbound = []
        self.inbound = []
        self.outboundcount = 0
        self.inboundcount = 0
        self.pagerank = 0.25
        self.visibility = {}
        self.position = {}
        self.sumoutbound = 0
        self.depth = 0;

#accepts a hashmap of url to Document objects
#writes the Document objects to stdout in a reasonable fashion
def dumpDocuments(documents):
    for doc in documents:
        print documents[doc].url
        print "OUTBOUND:"
        for link in documents[doc].outbound:
            print "   " + documents[link.url].url
        print "INBOUND:"
        for link in documents[doc].inbound:
            print "   " + documents[link.url].url
        print
    print "number of documents = " + str(len(documents))

#accepts a hashmap of url to Document objects and an inputFileName
#reads the input file, creating Document objects and storing
#them in documents
def processDocuments(documents, inputFileName):
    print("reading from input file...")
    inputFile = open(inputFileName, "r")
    for line in inputFile:
        if line.find("   ") != 0:
            documents[line[:-2]] = (Document(line[:-2]))
        elif line[3:-9] not in documents:
        	documents[line[3:-9]] = (Document(line[3:-9]))

    inputFile = open(inputFileName, "r")
    count = 0
    for line in inputFile:
        if line.find("   ") != 0:
            current = documents[line[:-2]]
            count = count + 1

        elif line[3:-9] in documents:
            current.outbound.append(documents[line[3:-9]])
            current.outboundcount += 1
            current.visibility[line[3:-9]] = int(line[-2:-1])
            current.position[line[3:-9]] = int(line[-6:-5])
            current.sumoutbound = current.sumoutbound + (int(line[-2:-1]) * int(line[-6:-5]))
            documents[line[3:-9]].inbound.append(documents[current.url])
            documents[line[3:-9]].inboundcount += 1
            documents[line[3:-9]].depth = count

#accepts a hashmap of url to Document objects and an int iterations
#runs the pageRank algorithm on the Document objects for iterations number of times
def pageRank(documents, iterations):
    dump = 0.85
    for i in range(0, iterations):
        stdout.write(str(i + 1) + " out of " + str(iterations) + " iterations complete!\r")
        stdout.flush()
        for doc in documents:
            inboundpagerank = 0;
            for incomming in documents[doc].inbound:
            	if(incomming.sumoutbound != 0):
                	inboundpagerank += (incomming.pagerank * (float(incomming.visibility[doc] * incomming.position[doc])/incomming.sumoutbound))
                elif(incomming.outboundcount != 0):
                	inboundpagerank += (incomming.pagerank/incomming.outboundcount)
            documents[doc].pagerank = (1 - dump) + dump * (inboundpagerank)
    stdout.write("\n")

#accepts a hashmap of url to Documents object, and an output file name
#sorts and writes the Documents to the output file in a reasonable format
def printRanks(documents, outputFileName):
    print("writing to output file...")
    newList = sorted(documents, key=lambda doc: documents[doc].pagerank, reverse=True)
    rank = 1
    outputFile = open(outputFileName, "w")
    for url in newList:
        outputFile.write(str(rank) + "\t" + str(documents[url].pagerank) + " " + url + "\n")
        rank = rank + 1
    outputFile.close()

def showUsage():
    print("rank usage:")
    print("   rank inputFile outputFile iterations")
    print("Examples:")
    print("  python pagerank.py pagerank.dump out.txt 15") 

def main():
    if (len(sys.argv) < 4):
        showUsage()
    else:
        inputFileName  = sys.argv[1]
        outputFileName = sys.argv[2]
        iterations     = int(sys.argv[3])
        documents = {}
        processDocuments(documents, inputFileName)
        start_time = time.time()
        pageRank(documents, iterations)
        print("Time taken to execute is %s seconds" % (time.time() - start_time))
        printRanks(documents, outputFileName)
        print("done!")

main()
