#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
sys.path.append('../alyahmor')
import pyarabic.araby as araby
from pyarabic.arabrepr import arepr
import genelex
import aly_stem_noun_const as snc
import aly_stem_verb_const as svc
def main(args):

    generator = genelex.genelex()
    print ('NOUN_AFFIX_LIST='),
    noun_affixes = generator.generate_affix_list(word_type="noun", vocalized=False)
    print(arepr(noun_affixes).replace(',', ',\n'))
    
    print('VERB_AFFIX_LIST='),
    verb_affixes = generator.generate_affix_list(word_type="verb", vocalized=False)
    print(arepr(verb_affixes).replace(',', ',\n'))
    
    # print prefixes and affixes

    noun_prefixes, noun_suffixes = generator.generate_prefix_suffix_list(word_type="noun", vocalized=False)    
    print ('NOUN_PREFIX_LIST='),
    print(arepr(noun_prefixes).replace(',', ',\n'))
    print ('NOUN_SUFFIX_LIST='),
    print(arepr(noun_suffixes).replace(',', ',\n'))
    
    verb_prefixes, verb_suffixes = generator.generate_prefix_suffix_list(word_type="verb", vocalized=False)    

    print ('VERB_PREFIX_LIST='),
    print(arepr(verb_prefixes).replace(',', ',\n'))
    print ('VERB_SUFFIX_LIST='),
    print(arepr(verb_suffixes).replace(',', ',\n'))

    
    return 0
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
