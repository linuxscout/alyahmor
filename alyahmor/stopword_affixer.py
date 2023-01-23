#!/usr/bin/python
# -*- coding=utf-8 -*-
# -------------------------------------------------------------------------
# Name:        stopword_affixer
# Purpose:     Arabic lexical analyser, provides feature for
# ~stemming arabic word as stopword
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     20-01-2023
# Copyright:   (c) Taha Zerrouki 2011
# Licence:     GPL
# -------------------------------------------------------------------------
"""
    Arabic stopword stemmer
"""
# from __future__ import absolute_import
import re
import sys
import pprint

sys.path.append('.')
import itertools
import pyarabic.araby as ar
import arabicstopwords.stopwords_classified
from arabicstopwords.stopwords_lexicon import stopwords_lexicon

try:
    import basic_affixer
    import aly_stem_stopword_const as SSC

except:
    import alyahmor.basic_affixer as basic_affixer
    import alyahmor.aly_stem_stopword_const as SSC


class stopword_affixer(basic_affixer.basic_affixer):
    def __init__(self, ):
        basic_affixer.basic_affixer.__init__(self, )

        self.procletics = SSC.COMP_PREFIX_LIST
        # ~ # get prefixes
        self.prefixes = []
        # get suffixes
        self.suffixes = SSC.CONJ_SUFFIX_LIST
        # get enclitics:
        self.enclitics = SSC.COMP_SUFFIX_LIST
        self.affixes = SSC.STOPWORDS_CONJUGATION_AFFIX
        self.clitics = SSC.COMP_STOPWORDS_AFFIXES

        # get only vocalized affixes
        # ~ self.procletics = [ p for p  in self.procletics if ar.is_vocalized(p)]
        # self.prefixes = [ p for p  in self.prefixes if ar.is_vocalized(p)]
        # ~ self.suffixes = [ p for p  in self.suffixes if ar.is_vocalized(p)]
        # ~ self.clitics = [ p for p  in self.clitics if ar.is_vocalized(p)]

        self.procletics_tags = SSC.COMP_PREFIX_LIST_TAGS
        # ~ # get prefixes
        self.prefixes_tags = []
        # get suffixes
        self.suffixes_tags = SSC.CONJ_SUFFIX_LIST_TAGS
        # get enclitics:
        self.enclitics_tags = SSC.COMP_SUFFIX_LIST_TAGS

        # New Configuration
        self.procletics = list(SSC.VOCALIZED_INDEX_COMP_PREFIX_LIST_TAGS.keys())
        # ~ # get prefixes
        self.prefixes = []
        # get suffixes
        self.suffixes = list(SSC.VOCALIZED_INDEX_CONJ_SUFFIX_LIST_TAGS.keys())
        # get enclitics:
        self.enclitics = list(SSC.VOCALIZED_INDEX_COMP_SUFFIX_LIST_TAGS.keys())

        self.procletics_tags = SSC.VOCALIZED_INDEX_COMP_PREFIX_LIST_TAGS
        # ~ # get prefixes
        self.prefixes_tags = []
        # get suffixes
        self.suffixes_tags = SSC.VOCALIZED_INDEX_CONJ_SUFFIX_LIST_TAGS
        # get enclitics:
        self.enclitics_tags = SSC.VOCALIZED_INDEX_COMP_SUFFIX_LIST_TAGS
        # ~ self.affixes_tags = SSC.STOPWORDS_CONJUGATION_AFFIX_TAGS
        # ~ self.clitics_tags = SSC.COMP_stopword_AFFIXES_TAGS

        # self.dictionary = arabicstopwords.stopwords_classified.STOPWORDS
        self.dictionary = stopwords_lexicon()

        # adjustement table
        self.ajustment_table = SSC.AJUSTMENT

    @staticmethod
    def get_stem_variants(stem, suffix_nm):
        """
        Generate the Stop stem variants according to the affixes.
        For example مدرستي = >مدرست+ي = > مدرسة +ي.
        Return a list of possible cases.
        @param stem: the input stem.
        @type stem: unicode.
        @param suffix_nm: suffix (no mark).
        @type suffix_nm: unicode.
        @return: list of stem variants.
        @rtype: list of unicode.
        """
        # some cases must have some correction
        # determinate the  suffix types
        # ~suffix = suffix_nm

        possible_stop_list = set([
            stem,
        ])

        if not suffix_nm or suffix_nm in (ar.YEH + ar.NOON,
                                          ar.WAW + ar.NOON):
            possible_stop = stem + ar.YEH
            possible_stop_list.add(possible_stop)
        if stem.endswith(ar.YEH):
            possible_stop = stem[:-1] + ar.ALEF_MAKSURA
            possible_stop_list.add(possible_stop)
        # to be validated
        validated_list = possible_stop_list
        return validated_list

    def get_suffix_variants(self, word, suffix, enclitic):
        """
        Get the suffix variant to be joined to the word.
        For example: word = مدرس, suffix = ة, encletic = ي.
        The suffix is converted to Teh.
        @param word: word found in dictionary.
        @type word: unicode.
        @param suffix: second level suffix.
        @type suffix: unicode.
        @param enclitic: first level suffix.
        @type enclitic: unicode.
        @return: variant of suffixes  (vocalized suffix and vocalized
        suffix without I'rab short mark).
        @rtype: (unicode, unicode)
        """
        enclitic_nm = ar.strip_tashkeel(enclitic)
        newsuffix = suffix  # default value
        word = ar.strip_lastharaka(word)
        # if the word ends by a haraka
        if not enclitic_nm and word[-1:] in (
                ar.ALEF_MAKSURA, ar.YEH,
                ar.ALEF) and ar.is_haraka(suffix):
            newsuffix = u""

        # gererate the suffix without I'rab short mark
        # here we lookup with given suffix because the new suffix is
        # changed and can be not found in table
        if u'متحرك' in self.suffixes_tags[suffix]['tags']:
            suffix_non_irab_mark = ar.strip_lastharaka(newsuffix)
        else:
            suffix_non_irab_mark = newsuffix

        return newsuffix, suffix_non_irab_mark

    @staticmethod
    def get_enclitic_variant(word, enclitic):
        """
        Get the enclitic variant to be joined to the word.
        For example: word = عن, suffix = , encletic = ني.
        The word and enclitic are geminated.
        @param word: word found in dictionary.
        @type word: unicode.
        @param enclitic: first level suffix.
        @type enclitic: unicode.
        @return: variant of suffixes  (vocalized suffix and vocalized
        suffix without I'rab short mark).
        @rtype: (unicode, unicode)
        """
        # enclitic_nm = ar.strip_tashkeel(enclitic)
        # newsuffix = suffix #default value
        # if the word ends by a haraka
        word_semi_voc = ar.strip_lastharaka(word)
        word_nm = ar.strip_tashkeel(word)
        # الإدغام في النون والياء في مثل فيّ، إليّ، عنّا ، منّا
        if enclitic.startswith(ar.NOON) and word_semi_voc.endswith(ar.NOON + ar.SUKUN):
            enclitic = enclitic[1:] + ar.SHADDA
            # ~ print "xxxxxxxxxxx--1"
        elif enclitic.startswith(ar.KASRA + ar.YEH) and word_semi_voc.endswith(ar.YEH):
            enclitic = ar.SHADDA + ar.FATHA
        elif enclitic.startswith(ar.KASRA + ar.YEH) and word_semi_voc.endswith(ar.ALEF_MAKSURA):
            #TODO: fix case سوى in ajust vocalization
            if not word_nm.endswith(ar.WAW+ar.ALEF_MAKSURA):
                enclitic = ar.SHADDA + ar.FATHA
            # ~ print "xxxxxxxxxxx--2"
        elif enclitic.startswith(ar.KASRA + ar.YEH) and word_semi_voc.endswith(ar.YEH + ar.SHADDA):
            enclitic = ""
            # ~ print "xxxxxxxxxxx--2"
        # return a tuple
        enclitic_non_irab_mark = enclitic
        return enclitic, enclitic_non_irab_mark

    @staticmethod
    def get_word_variant(word, proclitic, suffix):
        """
        Get the word variant to be joined to the suffix.
        For example: word = مدرسة, suffix = ي. The word is converted to مدرست.
        @param word: word found in dictionary.
        @type word: unicode.
        @param suffix: suffix ( firts or second level).
        @type suffix: unicode.
        @return: variant of word.
        @rtype: unicode.
        """
        word_stem = ar.strip_lastharaka(word)
        word_stem_nm = ar.strip_tashkeel(word)
        suffix_nm = ar.strip_tashkeel(suffix)
        proc_nm = ar.strip_tashkeel(proclitic)

        # حالة الكلمات التي تبدأ بألف لام التعريف
        if word_stem.startswith(ar.ALEF + ar.LAM + ar.LAM) and proc_nm.endswith(ar.LAM):
            word_stem = word_stem[2:]
        if word_stem.startswith(ar.ALEF + ar.LAM + ar.SUKUN + ar.LAM) and proc_nm.endswith(ar.LAM):
            word_stem = word_stem[3:]

        elif word_stem.startswith(ar.ALEF + ar.LAM) and proc_nm.endswith(ar.LAM):
            word_stem = word_stem[1:]

        # الاسم المؤنث بالتاء المروبطة نحذفها قبل اللاحقات مثل ات وية
        if suffix_nm != "" and word_stem.endswith(ar.TEH_MARBUTA):
            word_stem = word_stem[:-1] + ar.TEH
        # تحويل الألف المقصورة إلى ياء في مثل إلى => إليك
        if word_stem.endswith(ar.ALEF_MAKSURA) and suffix_nm:
            # if ar.strip_tashkeel(word_stem) == u"سوى":
            if word_stem_nm.endswith(ar.WAW+ar.ALEF_MAKSURA):
                word_stem = word_stem[:-1] + ar.ALEF
            else:
                word_stem = word_stem[:-1] + ar.YEH + ar.SUKUN
        # تحويل الهمزة حسب موقعها
        elif word_stem.endswith(ar.HAMZA) and suffix_nm:
            if suffix.startswith(ar.DAMMA):
                word_stem = word_stem[:-1] + ar.WAW_HAMZA
            elif suffix.startswith(ar.KASRA):
                word_stem = word_stem[:-1] + ar.YEH_HAMZA
            elif ar.KAF in proc_nm or ar.BEH in proc_nm:
                word_stem = word_stem[:-1] + ar.YEH_HAMZA

        # this option is not used with stop words, because most of them are not inflected مبني
        # if the word ends by a haraka strip the haraka if the suffix is not null
        if suffix and suffix[0] in ar.HARAKAT:
            word_stem = ar.strip_lastharaka(word_stem)

        # الإدغام في النون والياء في مثل فيّ، إليّ، عنّا ، منّا
        if suffix.startswith(ar.NOON) and word.endswith(ar.NOON + ar.SUKUN):
            word_stem = ar.strip_lastharaka(word_stem)
        elif suffix.startswith(ar.KASRA + ar.YEH) and word.endswith(
                ar.YEH + ar.SUKUN):
            word_stem = ar.strip_lastharaka(word_stem)

        return word_stem

    def vocalize(self, stop, proclitic, suffix, enclitic):
        """
        Join the  stop and its affixes, and get the vocalized form
        @param stop: stop found in dictionary.
        @type stop: unicode.
        @param proclitic: first level prefix.
        @type proclitic: unicode.

        @param suffix: second level suffix.
        @type suffix: unicode.
        @param enclitic: first level suffix.
        @type enclitic: unicode.
        @return: vocalized word.
        @rtype: unicode.
        """
        word_tuple_list = []

        suffix_voc = suffix  # CONJ_SUFFIX_LIST_TAGS[suffix]["vocalized"][0]

        # procletic can have manu vocalization (case of lam in arabic
        # proclitic_voc = self.procletics_tags[proclitic]["vocalized"][0]
        # enclitic can have many vocalization in arabic
        # like heh => عليهِ سواهُ
        # in this stage we consider only one,
        # the second situation is ajusted by vocalize_ajust
        # enclitic_voc = self.enclitics_tags[enclitic]["vocalized"][0]
        for proclitic_voc in self.procletics_tags.get(proclitic, {}).get("vocalized", proclitic):
            for enclitic_voc in self.enclitics_tags.get(enclitic, {}).get("vocalized", enclitic):
                enclitic_voc, encl_voc_non_inflect = self.get_enclitic_variant(stop,
                                                                               enclitic_voc)
                # generate the word variant for some words witch ends by special
                # letters like Alef_maksura, or hamza,
                # the variant is influed by the suffix harakat,
                # for example إلي +ك = إلى+ك

                stop = self.get_word_variant(stop, proclitic_voc, suffix + enclitic)
                # generate the suffix variant. if the suffix is removed for some letters like
                # Alef Maqsura and Yeh
                # for example
                suffix_voc, suffix_non_irab_mark = self.get_suffix_variants(
                    stop, suffix_voc, enclitic_voc)

                # generate the suffix variant. if the suffix is Yeh or Noon for geminating
                # for example عنّي = عن+ني
                # enclitic_voc = self.get_enclitic_variant(stop, enclitic_voc)

                # generate the non vacalized end word: the vocalized word
                # without the I3rab Mark
                # if the suffix is a short haraka
                word_non_irab_mark = ''.join(
                    [proclitic_voc, stop, suffix_non_irab_mark, enclitic_voc])

                word_vocalized = ''.join([proclitic_voc, stop, suffix_voc, enclitic_voc])

                # used for spelling purposes
                segmented = '-'.join([proclitic_voc, stop, suffix_voc, enclitic_voc])
                segmented = ar.strip_tashkeel(segmented)
                # adjust vocalization
                word_non_irab_mark = self.ajust_vocalization(word_non_irab_mark)
                word_vocalized = self.ajust_vocalization(word_vocalized)
                word_tuple_list.append((word_vocalized, word_non_irab_mark, segmented))
        return word_tuple_list

    @staticmethod
    def verify_affix(word, list_seg, affix_list):
        """
        Verify possible affixes in the resulted segments according
        to the given affixes list.
        @param word: the input word.
        @type word: unicode.
        @param list_seg: list of word segments indexes (numbers).
        @type list_seg: list of pairs.
        @return: list of acceped segments.
        @rtype: list of pairs.
        """
        return [
            s for s in list_seg
            if '-'.join([word[:s[0]], word[s[1]:]]) in affix_list
        ]

    @staticmethod
    def validate_tags(stop_tuple, affix_tags, procletic, encletic_nm):
        """
        Test if the given word from dictionary is compabilbe with affixes tags.
        @param stop_tuple: the input word attributes given from dictionary.
        @type stop_tuple: dict.
        @param affix_tags: a list of tags given by affixes.
        @type affix_tags:list.
        @param procletic: first level prefix vocalized.
        @type procletic: unicode.
        @param encletic_nm: first level suffix vocalized.
        @type encletic_nm: unicode.
        @return: if the tags are compaatible.
        @rtype: Boolean.
        """
        # procletic = ar.strip_tashkeel(procletic)
        # ~ encletic = encletic_nm
        # ~ suffix = suffix_nm
        if isinstance(affix_tags, str):
            affix_tags = affix_tags.split(":")
        if u"عطف" in affix_tags and not stop_tuple['has_conjuction']:
            return False
        if u"تعريف" in affix_tags and not stop_tuple['has_definition']:
            return False
        if u"تعريف" in affix_tags and stop_tuple['is_defined']:
            return False
        if u"مجرور" in affix_tags and not stop_tuple['is_inflected']:
            return False
        if u"مرفوع" in affix_tags and not stop_tuple['is_inflected']:
            return False
        # ~preposition
        if u'جر' in affix_tags and stop_tuple['is_inflected'] and not u"مجرور" in affix_tags:
            return False
        if u'جر' in affix_tags and not stop_tuple['has_preposition']:
            return False
        if u"متحرك" in affix_tags and not stop_tuple['is_inflected']:
            return False

        if u"مضاف" in affix_tags and not stop_tuple['has_pronoun']:
            return False
        if u"مضاف" in affix_tags and stop_tuple['is_defined']:
            return False
        # حين تكون الأداة متحركة فهي تقبل الاتصال بياء المتكلم مباشرة
        if encletic_nm == ar.YEH and not stop_tuple['is_inflected']:
            return False
        # noon wiqaya نون الوقاية
        # حين تكون الأداة غير متحركة فهي تلزم  الاتصال بنون الوقاية قبل ياء المتكلم مباشرة
        if u"وقاية" in affix_tags and (stop_tuple['is_inflected']
                                       or stop_tuple['word'].endswith(ar.YEH)):
            return False
        if u"وقاية" in affix_tags and "فعل" not in stop_tuple['type_word']:
            return False
            # ~interrog
        if u"استفهام" in affix_tags and not stop_tuple['has_interrog']:
            return False
            # ~conjugation
            # ~qasam

        if u"قسم" in affix_tags and not stop_tuple['has_qasam']:
            return False
            # ~
            # ~defined
            # ~is_inflected
            # ~tanwin
        if u"تنوين" in affix_tags and not stop_tuple['tanwin']:
            return False
            # ~action
            # ~object_type
            # ~need
        return True

    def ajust_vocalization(self, vocalized):
        """
        ajust vocalization
        Temporary function
        @param vocalized: vocalized word.
        @type vocalized: unicode.
        @return: ajusted vocalized word.
        @rtype: unicode.
        """
        ajusted = self.ajustment_table.get(vocalized, vocalized)

        return ajusted

    def get_form(self, word, proc, pref="", suff="", enc="", tags=""):
        """ generate stopword form """
        newword_list = []
        if self.is_valid_clitics(proc, enc):
            if self.check_clitic_affix(proc, enc, suff):
                if not tags:
                    tags = self.get_tags(word, proc, suff, enc)
                # validate stopwords forms agnaist classified stopwords dictionary
                newword_list = self.vocalize(word, proc, suff, enc)
                if newword_list:
                    newword_list = [list(x) for x in newword_list]
                    for word_tuple in newword_list:
                        word_tuple.append(tags)
        return newword_list


    def generate_forms(self, word, stop_tuple_list=None):
        """ generate all possible affixes
        We can genearte stopwords based on stop_tuple_list
        preprared to generate all forms according to a csv file.
        If stop_tuple_list = None: the current library use arabicstopwords library.
        """
        # get procletics
        stopword_forms = []
        # ~ word = u"قَصْدٌ"
        # lookup for each vocalized word in a the dictionary
        # if the word exist in stopword dictionary,
        # and has many vocalized forms,
        # get all forms for each vocalized word
        word_nm = ar.strip_tashkeel(word)
        if not stop_tuple_list:
            stop_tuple_list = self.dictionary.get_stopwordtuples(word_nm, lemma=True)

        # if the input word are not vocalized, get all vocalized forms from dictionary
        # if there the word is vocalized are many tuples
        # filter all vocalized like words
        if word != word_nm and len(stop_tuple_list) > 1:
            stop_tuple_list = [sp for sp in stop_tuple_list
                               if ar.vocalizedlike(sp.get("vocalized", word), word)]
        for stop_tuple in stop_tuple_list:
            vocalized_word = stop_tuple.get("vocalized", word)
            for element in itertools.product(self.procletics, self.suffixes, self.enclitics):
                proc = element[0]
                suff = element[1]
                enc = element[2]
                # if a proceletic has manycalized from
                # pass,
                # because those vocalizations already exist in the list
                # print(vocalized_word, "-".join([proc, suff, enc]))

                # proc_tags = self.procletics_tags.get(proc, {})
                # if len(proc_tags.get("vocalized", [])) > 1:
                #     continue
                # if a enceletic has many vocalized from
                # pass,
                # because those vocalizations already exist in the list
                # enc_tags = self.enclitics_tags.get(enc, {})
                # if len(enc_tags.get("vocalized", [])) > 1:
                #     continue
                # ~ affix = u"-".join([proc, enc])
                tags = self.get_tags(vocalized_word, proc, suff, enc)

                # validate stopwords forms agnaist classified stopwords dictionary
                if False: #DEBUG
                # if True: #DEBUG
                    affix =  "-".join([proc, suff, enc])
                    affix_nm =  ar.strip_tashkeel(affix)
                    print("\t".join([vocalized_word,affix, affix_nm,tags,
                                     str(self.validate_tags(stop_tuple, tags, proc, enc))]))
                if self.validate_tags(stop_tuple, tags, proc, enc):
                    # print(vocalized_word, "-".join([proc, suff, enc]),tags, self.validate_tags(stop_tuple, tags, proc, enc))
                    # print(stop_tuple)
                    newword_list = self.get_form(vocalized_word, proc, "", suff, enc, tags)
                    # print(newword_list)
                    if newword_list:
                        stopword_forms.extend(newword_list)
                    # else:
                    #     print("Error")
        # remove empty lists:
        stopword_forms = [sp for sp in stopword_forms if sp]
        return stopword_forms

    def get_tags(self, word, procletic, suffix, enclitic):
        """
        Get affixes tags
        
        """
        taglist = []
        # add procletic tags
        proclitic_tags = self.procletics_tags.get(procletic, {}).get('tags', ())
        taglist.extend(proclitic_tags)
        enclitic_tags = self.enclitics_tags.get(enclitic, {}).get('tags', ())
        taglist.extend(enclitic_tags)
        # in stopwords there is no prefix
        suffix_tags = self.suffixes_tags.get(suffix, {}).get('tags', ())
        taglist.extend(suffix_tags)
        # add suffix tags
        # add enclitic tags
        # ~ return "tags"
        # remove empy tags
        taglist = [t for t in taglist if t]
        return ":".join(taglist)

    def generate_by_affixes(self, word, affixes=[]):
        """ generate all possible word forms by given affixes"""
        # get procletics
        stopword_forms = []
        # ~ word = u"قَصْدٌ"
        proc = affixes[0]
        # ~ pref = affixes[1]
        suff = affixes[2]
        enc = affixes[3]
        # test if affixes are in affixes list
        # ~ print(proc not in self.procletics,suff not in self.suffixes , enc not in self.enclitics)
        # ~ print(proc, suff, enc)

        if (proc not in self.procletics or suff not in self.suffixes or enc not in self.enclitics):
            return [("Zerrouki", "taha")]
        stopword_forms = self.get_form(word, proc, "", suff, enc)
        # ~ print(stopword_forms)
        return stopword_forms

    def generate_affix_list(self, vocalized=True):
        """ generate all affixes """
        word = u"قصد"
        # generate all possible word forms
        stopword_forms = self.generate_forms(word)
        # remove diacritics
        if not vocalized:
            list_affixes = [ar.strip_tashkeel(d[0]) for d in stopword_forms]
        else:
            list_affixes = [d[0] for d in stopword_forms]
        # remove duplicated
        list_affixes = list(set(list_affixes))
        # remove stem and get only affixes
        list_affixes = [x.replace(word, '-') for x in list_affixes]

        return list_affixes

    def check_clitic_affix(self, proclitic_nm, enclitic, suffix):
        """
        Verify if proaffixes (sytaxic affixes) are compatable
        with affixes ( conjugation)
        @param proclitic_nm: first level prefix.
        @type proclitic_nm: unicode.
        @param enclitic: first level suffix.
        @type enclitic: unicode.
        @param suffix: second level suffix.
        @type suffix: unicode.
        @return: compatible.
        @rtype: True/False.
        """

        # return True
        # get proclitics and enclitics tags
        proclitic_tags = self.procletics_tags.get(proclitic_nm, {}).get('tags', ())
        enclitic_tags = self.enclitics_tags.get(enclitic, {}).get('tags', ())
        # in stopwords there is no prefix
        suffix_tags = self.suffixes_tags.get(suffix, {}).get('tags', ())
        # in some cases the suffixes have more cases
        # add this cases to suffix tags
        suffix_tags += self.suffixes_tags.get(suffix, {}).get("cases", ())
        # المقيمو الصلاة
        # المقيمي الصلاة

        # ~ if u"تعريف" in proclitic_tags and u"مضاف" in suffix_tags and \
        # ~ u'مضاف' not in enclitic_tags:
        # ~ return False

        if u"تعريف" in proclitic_tags and u"تنوين" in suffix_tags:
            return False
        elif u"تعريف" in proclitic_tags and u"إضافة" in suffix_tags:
            return False

        # ~ elif u"تعريف" in proclitic_tags and suffix == ar.YEH and u"مضاف"  in suffix_tags and \
        # ~ enclitic:
        # ~ return False

        # الجر  في حالات الاسم المعرفة بال أو الإضافة إلى ضمير أو مضاف إليه
        # مما يعني لا يمكن تطبيقها هنا
        # بل في حالة التحليل النحوي
        elif u"مضاف" in enclitic_tags and u"تنوين" in suffix_tags:
            return False
        elif u"مضاف" in enclitic_tags and u"لايضاف" in suffix_tags:
            return False
        # This case is not suitable to stopwords
        elif u"جر" in proclitic_tags and u"مرفوع" in suffix_tags:
            return False
        elif u"جر" in proclitic_tags and u"منصوب" in suffix_tags:
            return False
        elif enclitic.startswith(ar.YEH) and suffix.endswith(ar.DAMMA):
            return False


        # ستعمل في حالة كسر هاء الضمير في الجر

        # elif  bool(u"لايجر" in enclitic_tags) and  bool(u"مجرور" in \
        # suffix_tags) :
        #    self.cache_affixes_verification[affix] = False
        # elif  bool(u"مجرور" in enclitic_tags) and  not bool(u"مجرور" in \
        # suffix_tags) :
        #    self.cache_affixes_verification[affix] = False
        else:
            return True

        return True
