#!/usr/bin/env python3

from lxml import etree 

#load file
tree = etree.parse("XML/traffic.xml")

#search xml
search = tree.xpath('/response/result/log/logs/entry/dst')

#number of matches
matches = len(search)

print("Found "+str(matches)+" matches")

i = 0

while i < matches:
    print(search[i].text)
    i = i+1
