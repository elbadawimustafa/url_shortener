# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 15:40:47 2018

@author: Mustafa
UrlShortener class: handles generating the code to shorten the url
"""


class UrlShortener:
    #constructor is a dictionary containing urls as keys and and id a variable
    def __init__(self, url2id):
        self.url2id = url2id

        
    #we want to start with id = 100, this is to enable the get_code function to generate a mixed character/number url code
        if url2id == {}:
            id = 100
        elif max(url2id.values()) < 100:
            id = 100
        else:
            id = int(max(url2id.values())+1)
        
        self.id = id
    
    def shorten_url(self, url):
        #if the url is already in the dictionary then return the original code
        if url in self.url2id:
            id = self.url2id[url]
            url_code = self.get_code(id)
        #if not then use the get_code method to a shortener code for the url
        else:
            self.url2id[url] = self.id
            url_code = self.get_code(self.id)
            self.id += 1
        
        return str(url_code)
    
    def get_code(self, id):
        #characters to use in making the url
        chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        #number of characters is the base i.e. 62
        base = len(chars)
        #needed to convert numerical id to a mixed characters code
        conList = []
        
        #now convert the numerical id to a mixed code
        while id > 0:
            val = id % base
            conList.append(chars[int(val)]  )
            #end the while loop when id is a multiple of 62
            id = id // base
        #the loop returns integers in desc order, reverse to select list elements in ascending order    
        return "".join(conList[::-1])

