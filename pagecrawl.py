#!/usr/bin/env python
# -*- coding: utf-8 -*-

import romkan
import urllib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from BeautifulSoup import BeautifulStoneSoup
import re

def getMeaning( word):
    path = "http://tangorin.com/general/"+word

    source = urllib2.urlopen(path).read()
    if "Sorry, no results." in str(source):
        return ""
    soup = BeautifulStoneSoup(source)
    entry = soup.findAll(attrs={ "value" : "1" })
    definition = entry
    return re.sub('<[^<]+?>', '', str(definition[0]).replace("例文",""))

for x in range(5,6):
    path = "http://www.tanos.co.uk/jlpt/jlpt"+str(x)+"/vocab"
    print "Parsing "+path
    source = urllib2.urlopen(path).read()
    soup = BeautifulStoneSoup(source)
    table = soup.findAll('table')[1]
    words = table.findAll('tr')
    f = open('n'+str(x)+'.html', 'w')
    print >>f, '<h1> N'+str(x)+' Vocabulary List </h1>'
    print >>f , "<table class=\"tablepress tablepress-id-5 dataTable no-footer\" role=\"grid\" style=\"margin-left: 0px; width: 880px;\">"
    print >>f , "<thead>"
    print >>f , "<tr class=\"row-1 odd\" role=\"row\">"
    print >>f , "<th class=\"column-1\" tabindex=\"0\" aria-controls=\"tablepress-5\" rowspan=\"1\" colspan=\"1\" style=\"width: 79px;\" aria-label=\"Kanji\">Kanji</th>"
    print >>f , "<th class=\"column-2\" tabindex=\"0\" aria-controls=\"tablepress-5\" rowspan=\"1\" colspan=\"1\" style=\"width: 106px;\" aria-label=\"Hiragana\">Hiragana</th>"
    print >>f, "<th class=\"column-3\" tabindex=\"0\" aria-controls=\"tablepress-5\" rowspan=\"1\" colspan=\"1\" style=\"width: 195px;\" aria-label=\"Romaji\">Romaji</th>"
    print >>f, "<th class=\"column-4 \" tabindex=\"0\" aria-controls=\"tablepress-5\" rowspan=\"1\" colspan=\"1\" style=\"width: 400px;\" aria-label=\"Meaning\">Meaning</th></tr>"
    print >>f ,"</thead>"
    print "Total Words to Parse = " + str(len(words))
    for word in words:
        splitWord = word.findAll('td')
        kanji = ""
        meaning = ""
        hiragana = ""
        romaji = ""
        i = 0;
        # print len(splitWord)
        for split in splitWord:
            cleanedWord = re.sub('<[^<]+?>', '', str(split));

            if i==0:
                # print >>f, cleanedWord

                kanji = cleanedWord

                    # meaning = getMeaning(cleanedWord,f)
                # print >>f, meaning
            if i==1:
                hiragana = cleanedWord
                if "（" in hiragana or "）" or "、" or "・" in hiragana:
                    hiragana = ""
                    kanji=""
            i = i+1
        if not(hiragana == "" and kanji == ""):
            print >>f, "<tr>"

            romaji = romkan.to_roma(hiragana.decode("utf-8"))

            if kanji =="":
                meaning = getMeaning(hiragana)
            else:
                meaning = getMeaning(kanji)

            print >>f, "<td>" + kanji + "</td>"
            print >>f, "<td>" + hiragana + "</td>"
            print >>f, "<td>" + romaji + "</td>"
            print >>f, "<td>" + meaning + "</td>"
            print >>f, "</tr>"

    print >>f , "</table>"

    f.close()
