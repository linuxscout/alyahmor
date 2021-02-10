#!/usr/bin/python
# -*- coding = utf-8 -*-
#-----------------------------------------------------------------------
# Name:        verb_affixer
# Purpose:     Arabic lexical analyser, provides feature for
#  stemming arabic word as verb
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
from __future__ import absolute_import
import itertools
import pyarabic.araby as ar
try:
    import basic_affixer
    import aly_stem_verb_const as SVC    
except:
    import alyahmor.basic_affixer as basic_affixer
    import alyahmor.aly_stem_verb_const as SVC
import libqutrub.classverb
def verify_affix(word, list_seg, affix_list):
    """
    Verify possible affixes in the resulted segments
    according to the given affixes list.
    @param word: the input word.
    @type word: unicode.
    @param list_seg: list of word segments indexes (numbers).
    @type list_seg: list of pairs.
    @return: list of acceped segments.
    @rtype: list of pairs.
    """
    #~ for s in list_seg:
    #~ print "affix", '-'.join([word[:s[0]],word[s[0]:s[1]], word[s[1]:]])
    return [s for s in list_seg
        if '-'.join([word[:s[0]], word[s[1]:]]) in affix_list ]

def check_clitic_tense(proclitic, enclitic, tense, pronoun,
                         transitive):
    """
    test if the given tenses are compatible with proclitics
    """
    # proaffix key
    comp_key = u":".join(
        [proclitic, enclitic, tense, pronoun,
         str(transitive)])
    # إذا كان الزمن مجهولا لا يرتبط مع الفعل اللازم
    if not transitive and tense in SVC.qutrubVerbConst.TablePassiveTense:
        return False
    if not proclitic and not enclitic:
        return True
    # The passive tenses have no enclitics
    #ﻷزمنة المجهولة ليس لها ضمائر متصلة في محل نصب مفعول به
    #لأنّ مفعولها يصبح نائبا عن الفاعل

    if enclitic and tense in SVC.qutrubVerbConst.TablePassiveTense:
        return False

    #~ elif enclitic and think_trans and pronoun
    # لا سابقة
    # أو سابقة ، والزمن مسموح لها
    # لا لاحقة
    #أو زمن مسموح لتلك اللاحقة
    elif ((not proclitic
           or tense in SVC.EXTERNAL_PREFIX_TABLE.get(proclitic, ''))
          and (not enclitic
               or pronoun in SVC.EXTERNAL_SUFFIX_TABLE.get(enclitic, ''))):
        return True

    else:
        return False

def check_clitic_affix(proclitic, enclitic, affix):
    """
    Verify if proaffixes (sytaxic affixes) are compatable with affixes
    (conjugation)
    @param proclitic: first level prefix.
    @type proclitic: unicode.
    @param enclitic: first level suffix.
    @type enclitic: unicode.
    @param affix: second level affix.
    @type affix: unicode.
    @return: compatible.
    @rtype: True/False.
    """
    # proaffix key
    #~ comp_key = u":".join([proclitic, enclitic, affix])
    #~ if comp_key in self.compatibility_cache:
        #~ return self.compatibility_cache[comp_key]
    if not proclitic and not enclitic:
        return True
    else:
        proclitic_compatible = False
        if not proclitic:
            proclitic_compatible = True
        elif proclitic in SVC.EXTERNAL_PREFIX_TABLE:
            #~ elif SVC.EXTERNAL_PREFIX_TABLE.has_key(proclitic):
            if affix == '-':
                proclitic_compatible = True
            else:
                for item in SVC.TABLE_AFFIX.get(affix, []):
                    #the tense item[0]
                    if item[0] in SVC.EXTERNAL_PREFIX_TABLE.get(
                            proclitic, ''):
                        proclitic_compatible = True
                        break
                else:
                    proclitic_compatible = False
        if proclitic_compatible:
            if not enclitic:
                #~ self.compatibility_cache[comp_key] = True
                return True
            elif enclitic in SVC.EXTERNAL_SUFFIX_TABLE:
                #~ elif SVC.EXTERNAL_SUFFIX_TABLE.has_key(enclitic):
                if affix == '-':
                    #~ self.compatibility_cache[comp_key] = True
                    return True
                else:
                    for item in SVC.TABLE_AFFIX.get(affix, []):
                        #the tense item[0]
                        if item[1] in SVC.EXTERNAL_SUFFIX_TABLE.get(
                                enclitic, ''):
                            #~ return True
                            break
                    else:
                        #~ self.compatibility_cache[comp_key] = False
                        return False
                    #~ self.compatibility_cache[comp_key] = True
                    return True
    #~ self.compatibility_cache[comp_key] = False
    return False

class verb_affixer(basic_affixer.basic_affixer):
    def __init__(self, ):
        basic_affixer.basic_affixer.__init__(self,)
        self.procletics = SVC.COMP_PREFIX_LIST
        #~ # get prefixes
        self.prefixes = SVC.CONJ_PREFIX_LIST
        # get suffixes
        self.suffixes = SVC.CONJ_SUFFIX_LIST
        # get enclitics:
        self.enclitics = SVC.COMP_SUFFIX_LIST
        
        self.affixes = SVC.VERBAL_CONJUGATION_AFFIX
        #~ self.clitics = SVC.CONJ_VER_AFFIXES
        # get only vocalized affixes
        #~ self.procletics = [ p for p  in self.procletics if ar.is_vocalized(p)]
        #~ self.prefixes = [ p for p  in self.prefixes if ar.is_vocalized(p)]
        #~ self.suffixes = [ p for p  in self.suffixes if ar.is_vocalized(p)]
        #~ self.clitics = [ p for p  in self.clitics if ar.is_vocalized(p)]
    @staticmethod
    def check_clitic_affix(proclitic, enclitic, affix):        
        return check_clitic_affix(proclitic, enclitic, affix)  
    @staticmethod
    def get_verb_variants(verb):
        """ return modified forms of input verb"""
        verb_list = []
        #cases like verb started with Alef madda, it can ءا or أأ
        if verb.startswith(ar.ALEF_MADDA):
            verb_list.append(ar.ALEF_HAMZA_ABOVE + ar.ALEF_HAMZA_ABOVE \
            +verb[1:])
            verb_list.append(ar.HAMZA + ar.ALEF + verb[1:])
        return verb_list
    @staticmethod
    def get_in_stem_variants(stem, enclitic):
        """ return modified forms of input stem"""
        list_stem = []
        if enclitic:
            if stem.endswith(ar.TEH + ar.MEEM + ar.WAW):
                list_stem.append(stem[:-1])
            elif stem.endswith(ar.WAW):
                list_stem.append(stem + ar.ALEF)
            elif stem.endswith(ar.ALEF):
                list_stem.append(stem[:-1] + ar.ALEF_MAKSURA)
        if stem.startswith(ar.ALEF_MADDA):
            # االبداية بألف مد
            list_stem.append(ar.ALEF_HAMZA_ABOVE + \
            ar.ALEF_HAMZA_ABOVE + stem[1:])
            list_stem.append(ar.HAMZA + ar.ALEF + stem[1:])
        return list_stem
    @staticmethod
    def get_enclitic_variant(word, enclitic):
        """
        Get the enclitic variant to be joined to the word.
        For example: word  =  أرجِهِ , enclitic = هُ.
        The enclitic  is convert to HEH+ KAsra.
        اعبارة في مثل أرجه وأخاه إلى يم الزينة
        @param word: word found in dictionary.
        @type word: unicode.
        @param enclitic: first level suffix vocalized.
        @type enclitic: unicode.
        @return: variant of enclitic.
        @rtype: unicode.
        """
        #if the word ends by a haraka
        if enclitic == ar.HEH+ar.DAMMA and (word.endswith(ar.KASRA)\
         or word.endswith(ar.YEH)):
            enclitic = ar.HEH + ar.KASRA
        return enclitic


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
        #~ print(verb.encode('utf8'))
        # لمعالجة حالة ألف التفريق
        if enclitic and verb.endswith(ar.WAW + ar.ALEF):
            verb = verb[:-1]
        # حالة مشَوْا
        if enclitic and verb.endswith(ar.WAW + ar.SUKUN + ar.ALEF):
            verb = verb[:-1]
        if enclitic and verb.endswith(ar.ALEF_MAKSURA):
            verb = verb[:-1] + ar.ALEF
        if enclitic and verb.endswith(ar.TEH+ar.DAMMA + ar.MEEM+ ar.SUKUN):
            verb  = verb[:-1] + ar.DAMMA + ar.WAW
        if enclitic and verb.endswith(ar.TEH+ar.DAMMA + ar.MEEM):
            verb += ar.DAMMA + ar.WAW
        word_tuple_list =[]
        #~ enclitic_voc = SVC.COMP_SUFFIX_LIST_TAGS[enclitic]["vocalized"][0]
        #~ enclitic_voc = self.get_enclitic_variant(verb, enclitic_voc)
        #~ proclitic_voc = SVC.COMP_PREFIX_LIST_TAGS[proclitic]["vocalized"][0]
        #suffix_voc = suffix #CONJ_SUFFIX_LIST_TAGS[suffix]["vocalized"][0]
            
        for proclitic_voc in SVC.COMP_PREFIX_LIST_TAGS.get(proclitic, {}).get("vocalized", ''):
            for enclitic_voc in SVC.COMP_SUFFIX_LIST_TAGS.get(enclitic, {}).get("vocalized", ''):
                enclitic_voc = self.get_enclitic_variant(verb, enclitic_voc)
                vocalized = ''.join([proclitic_voc, verb, enclitic_voc])
                semivocalized = ''.join(
            [proclitic_voc, ar.strip_lastharaka(verb), enclitic_voc])
                word_tuple_list.append((vocalized, semivocalized))
        return word_tuple_list
        
    def generate_forms(self, word):
        """ generate all possible affixes"""
        # get procletics

        #~ word = u"قصد"
        verb_forms =[]
        for element in itertools.product(self.procletics,  self.prefixes, self.suffixes, self.enclitics):
            proc = element[0]
            pref = element[1]
            suff = element[2]
            enc = element[3]
            
            newwordlist = self.get_form(word, proc, pref, suff, enc)
            if newwordlist:
                verb_forms.extend(newwordlist)
        return verb_forms

    def generate_by_affixes(self, word, affixes = []):
        """ generate all possible word forms by given affixes"""
        # get procletics
        verb_forms = []
        #~ word = u"قَصْدٌ"
        proc = affixes[0]
        pref = affixes[1]
        suff = affixes[2]
        enc = affixes[3]
        # test if affixes are in affixes list
        if (proc not in self.procletics or pref not in self.prefixes or  suff not in self.suffixes or enc not in self.enclitics):
            return []
        verb_forms = self.get_form(word, proc, pref,suff, enc)
        return verb_forms         
    
    def get_form(self, word, proc, pref, suff, enc):
        """ generate the possible affixes"""
        # get procletics

        #~ word = u"قصد"
        list_word = []
        newword = u""
        transitive = True
        
        future_type= ar.FATHA
        vbc = libqutrub.classverb.VerbClass(word, transitive,future_type)        
        if self.is_valid_affix(pref, suff):
            affix = pref+'-'+suff
            if self.check_clitic_affix(proc, enc, affix):
                #~ print(arepr(element))
                if affix in SVC.TABLE_AFFIX:
                    for pair in SVC.TABLE_AFFIX[affix]:
                        tense = pair[0]
                        pronoun = pair[1]
                        test = check_clitic_tense(proc, enc,
                                                         tense, pronoun, transitive)
                        if test:
                            conj_verb = vbc.conjugate_tense_for_pronoun(tense, pronoun)
                            newword_list = self.vocalize(conj_verb, proc,  enc)
                            list_word.extend(newword_list)
        return list_word
        

        
