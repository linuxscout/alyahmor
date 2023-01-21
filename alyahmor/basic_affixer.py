#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------
# Name:        basic_affixer
# Purpose:     Arabic lexical analyser, provides feature for
#  stemming arabic word as verb/nouns/stopwords
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     31-10-2011
# Copyright:   (c) Taha Zerrouki 2011
# Licence:     GPL
#-----------------------------------------------------------------------
"""
    Arabic verb stemmer
"""
import pyarabic.araby as araby
import itertools
class basic_affixer:
    def __init__(self, ):
        self.procletics = []
        #~ # get prefixes
        self.prefixes = []
        # get suffixes
        self.suffixes = []
        # get enclitics:
        self.enclitics = []
        
        self.affixes = []
        self.clitics = []
        
    def is_valid_affix(self, prefix, suffix):
        
        return  u"-".join([prefix, suffix]) in self.affixes
            
    def is_valid_clitics(self, proclitic, enclitic):
        #~ return True
        
        proclitic = araby.strip_tashkeel(proclitic)
        enclitic = araby.strip_tashkeel(enclitic)
        return  u"-".join([proclitic, enclitic]) in self.clitics
    
    #~ @staticmethod
    #~ def check_clitic_affix(proclitic, enclitic, affix):        
        #~ return check_clitic_affix(proclitic, enclitic, affix)

    def vocalize(self,verb, proclitic, enclitic):
        """
        Join the  verb and its affixes, and get the vocalized form
        @param verb: verb found in dictionary.
        @type verb: unicode.
        @param proclitic: first level prefix.
        @type proclitic: unicode.
        @param enclitic: first level suffix.
        @type enclitic: unicode.
        @return: (vocalized word, semivocalized).
        @rtype: (unicode, unicode).
        """
        vocalized = u"".join([proclitic, verb, enclitic])
        semivocalized = vocalized
        return (vocalized, semivocalized)
    def generate_forms(self, word):
        """ generate all possible affixes"""
        # get procletics

        verb_forms =[]
        for element in itertools.product(self.procletics,  self.prefixes, self.suffixes, self.enclitics):
            proc = element[0]
            pref = element[1]
            suff = element[2]
            enc = element[3]
            newword = self.get_form(word, proc, pref, suff, enc)
            if newword:
                verb_forms.append(newword)
        return verb_forms
        
    def get_form(self, word, proc, pref, suff, enc):
        """ generate the possible affixes"""
        # get procletics

        #~ word = u"قصد"
        newword = u""
        if self.is_valid_affix(pref, suff):
            if self.check_clitic_affix(proc, enc, pref+'-'+suff):
                #~ print(arepr(element))
                conj = u"".join([pref, word,suff])
                newword = self.vocalize(conj, proc,  enc)
        return newword
        

    def generate_affix_list(self, vocalized=True):
        """ generate all affixes """
        word = u"قصد"    
        # generate all possible word forms
        forms = self.generate_forms(word)
        # remove diacritics
        if not vocalized :
            list_affixes = [ araby.strip_tashkeel(d[0]) for d in forms]
        else:
            list_affixes = [d[0] for d in forms]
        # remove duplicated
        list_affixes = list(set(list_affixes))
        # remove stem and get only affixes
        # those variants are used to represent verb vocalizations when conjugation
        variants = [u'قَصَد', u'قْصَد', u"قصد"]
        for word in variants:
            list_affixes = [ x.replace(word,'-') for x in list_affixes]
         
        return list_affixes
    

        
