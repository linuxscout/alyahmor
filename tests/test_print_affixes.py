#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pprint
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
    pprint.pprint(noun_affixes)
    
    print('VERB_AFFIX_LIST='),
    verb_affixes = generator.generate_affix_list(word_type="verb", vocalized=False)
    pprint.pprint(verb_affixes)
    
    # print prefixes and affixes

    noun_prefixes, noun_suffixes = generator.generate_prefix_suffix_list(word_type="noun", vocalized=False)    
    print ('NOUN_PREFIX_LIST='),
    pprint.pprint(noun_prefixes)
    print ('NOUN_SUFFIX_LIST='),
    pprint.pprint(noun_suffixes)
    
    verb_prefixes, verb_suffixes = generator.generate_prefix_suffix_list(word_type="verb", vocalized=False)    

    print ('VERB_PREFIX_LIST='),
    pprint.pprint(verb_prefixes)
    print ('VERB_SUFFIX_LIST='),
    pprint.pprint(verb_suffixes)

    
    return 0
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
