#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  genAffixes.py
#  
#  Copyright 2019 zerrouki <zerrouki@majd4>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#
from __future__ import absolute_import
import itertools
from pyarabic.arabrepr import arepr
import pyarabic.araby as araby
try:
    from . import noun_affixer
    from . import verb_affixer
except:
    import noun_affixer
    import verb_affixer    
class genelex:
    
    def __init__(self,):
        self.verb_vocalizer = verb_affixer.verb_affixer()        
        self.noun_vocalizer = noun_affixer.noun_affixer()        
        pass
    def generate_by_affixes(self, word, word_type="noun", affixes =[], vocalized=True,):
        """
        Generate forms fo a given word with specified affixes
        
        @param word: the input word
        @type word: unicode
        @param type: (noun, verb, stop word): the default is "noun"
        @type type: unicode
        @param affixes: if the result must be vocalized or not, default is True
        @type affixes: boolean
        @param vocalized: if the result must be vocalized or not, default is True
        @type vocalized: boolean
        @return : all vocalized forms of input word
        @rtype:  tuple list, list or dict 
        """
        wtype = word_type
        if wtype=="noun":
            forms = self.noun_vocalizer.generate_by_affixes(word, affixes)        
        elif wtype=="verb":
            forms = self.verb_vocalizer.generate_by_affixes(word, affixes)        

        else:
            forms = self.noun_vocalizer.generate_by_affixes(word, affixes) 
        if vocalized:
            return self.get_vocalized_forms(forms)
        else:
            return self.get_unvocalized_forms(forms)

    def generate_forms(self, word, word_type="noun", vocalized=True, indexed=False, affixes =[]):
        """
        Generate forms fo a given word
        
        @param word: the input word
        @type word: unicode
        @param type: (noun, verb, stop word): the default is "noun"
        @type type: unicode
        @param vocalized: if the result must be vocalized or not, default is True
        @type vocalized: boolean
        @param indexed: the forms diplayed as dictionary with unvocalized forms as keys, and for 
        each key, we give all possible vocalization
        @type indexed: boolean, default False
        @return : all vocalized forms of input word
        @rtype:  tuple list, list or dict 
        """
        wtype = word_type
        if wtype=="noun":
            forms = self.generate_noun_forms(word)        
        elif wtype=="verb":
            forms = self.generate_verb_forms(word)            

        else:
            forms = self.generate_noun_forms(word)
        if not indexed:
            if vocalized:
                return self.get_vocalized_forms(forms)
            else:
                return self.get_unvocalized_forms(forms)
        else:
            return self.get_vocalized_forms_dict(forms)

    def generate_forms(self, word, word_type="noun", vocalized=True, indexed=False):
        """
        Generate forms fo a given word
        
        @param word: the input word
        @type word: unicode
        @param type: (noun, verb, stop word): the default is "noun"
        @type type: unicode
        @param vocalized: if the result must be vocalized or not, default is True
        @type vocalized: boolean
        @param indexed: the forms diplayed as dictionary with unvocalized forms as keys, and for 
        each key, we give all possible vocalization
        @type indexed: boolean, default False
        @return : all vocalized forms of input word
        @rtype:  tuple list, list or dict 
        """
        wtype = word_type
        if wtype=="noun":
            forms = self.generate_noun_forms(word)        
        elif wtype=="verb":
            forms = self.generate_verb_forms(word)            

        else:
            forms = self.generate_noun_forms(word)
        if not indexed:
            if vocalized:
                return self.get_vocalized_forms(forms)
            else:
                return self.get_unvocalized_forms(forms)
        else:
            return self.get_vocalized_forms_dict(forms)
            
    def separate(self, affix_list):
        """ return prefixes and suffixes from an affix list"""
        prefixes = []
        suffixes = []
        for affix in affix_list:
            affs = affix.split('-')
            if len(affs) >= 2:
                pref = affs[0]
                suff = affs[1]
            prefixes.append(pref)
            suffixes.append(suff)
        # remove duplicated
        prefixes = list(set(prefixes))
        prefixes.sort()
        suffixes = list(set(suffixes))
        suffixes.sort()
        return prefixes, suffixes
        
    def generate_affix_list(self, word_type="noun", vocalized=True, indexed= False):
        """
        generate affix list for a word type, it can be vocalized or not,
        and can be indexed by unvocalized affixes,
        or get it separated as prefixes and suffixes
        """
        wtype= word_type
        if wtype=="noun":
            affix_list=  self.generate_noun_affix_list()
        elif wtype=="verb":
            affix_list=  self.generate_verb_affix_list()            
        else:
            affix_list=  self.generate_noun_affix_list()            


        if not indexed:
            if vocalized:
                return affix_list
            else:
                return self.get_unvocalized_affix_list(affix_list)
        else:
            return self.get_vocalized_affixes_dict(affix_list)
    def generate_prefix_suffix_list(self, word_type="noun", vocalized=True, indexed= False):
        affix_list = self.generate_affix_list(word_type, vocalized, indexed)
        # we want here prefixes and suffixes separatly
        return self.separate(affix_list)
        
        
    def generate_noun_forms(self, word):
        """ generate all possible affixes"""
        # get procletics
        return self.noun_vocalizer.generate_forms(word)
        
    def generate_noun_affix_list(self,):
        """ generate all affixes """
        return self.noun_vocalizer.generate_affix_list()
        
    def generate_verb_forms(self, word):
        """ generate all possible affixes"""
        return self.verb_vocalizer.generate_forms(word)        

    def generate_verb_affix_list(self, ):
        """ generate all affixes """
        return self.verb_vocalizer.generate_affix_list()
        
    def generate_verb_affix_list(self, ):
        """ generate all affixes """
        return self.verb_vocalizer.generate_affix_list()
        
    def get_unvocalized_forms(self, forms = []):
        """ display unvocalized forms"""
        if not forms:
            return []
        else:
            unvoc_forms = [araby.strip_tashkeel(t[0]) for t in forms]
        unvoc_forms = list(set(unvoc_forms))
        unvoc_forms.sort()
        return unvoc_forms        
    def get_vocalized_forms(self, forms = []):
        """ display vocalized forms"""
        if not forms:
            return []
        else:
            voc_forms = [t[0] for t in forms]
        voc_forms = list(set(voc_forms))
        voc_forms.sort()
        return voc_forms 


        
    def get_vocalized_forms_dict(self, forms = []):
        """ display vocalized forms in a dict"""
        forms_dict = {}
        if forms:
            for form in forms:
                unvoc = araby.strip_tashkeel(form[0])
                if unvoc in forms_dict:
                    forms_dict[unvoc].append(form[0])
                else:
                   forms_dict[unvoc] = [form[0],]
        for key in forms_dict:
            forms_dict[key].sort()
            forms_dict[key] = list(set(forms_dict[key]))
        return forms_dict 
        
    def get_unvocalized_affix_list(self, forms=[]):
        """ display vocalized forms"""
        if not forms:
            return []
        voc_forms = [araby.strip_tashkeel(t) for t in forms]
        voc_forms = list(set(voc_forms))
        voc_forms.sort()
        return voc_forms
        
    def get_vocalized_affixes_dict(self, forms = []):
        """ display vocalized affixes in a dict"""
        forms_dict = {}
        if forms:
            for form in forms:
                unvoc = araby.strip_tashkeel(form)
                if unvoc in forms_dict:
                    forms_dict[unvoc].append(form)
                else:
                   forms_dict[unvoc] = [form,]
        for key in forms_dict:
            if len(forms_dict[key])>=2:
                forms_dict[key].sort()
                forms_dict[key] = list(set(forms_dict[key]))
        return forms_dict 
    
def main(args):
    word = u"قَصْدٌ"
    generator = genelex()
    noun_forms = generator.generate_noun_forms(word)
    #~ print(arepr(noun_forms).replace('),', '),\n'))
    #~ print('************verb*****')
    word = u"قصد"    
    verb_forms =generator.generate_verb_forms(word)
    #~ print(arepr(verb_forms).replace('),', '),\n'))
    #~ print(arepr(verb_forms).replace('],', '],\n'))
    
    print ('NOUN_AFFIX_LIST=')
    noun_affixes = generator.generate_noun_affix_list()
    print(repr(noun_affixes).replace(',', ',\n'))
    
    print('VERB_AFFIX_LIST=')
    verb_affixes = generator.generate_verb_affix_list()
    print(repr(verb_affixes).replace(',', ',\n'))

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
