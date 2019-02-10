#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
import pyarabic.araby as araby
from pyarabic.arabrepr import arepr
import alyahmor.genelex
def main(args):

    generator = alyahmor.genelex.genelex()
    print ('NOUN_AFFIX_LIST=')
    noun_affixes = generator.generate_affix_list(word_type="noun", vocalized=False)
    print(arepr(noun_affixes).replace(',', ',\n'))
    
    print('VERB_AFFIX_LIST=')
    verb_affixes = generator.generate_affix_list(word_type="verb", vocalized=False)
    print(arepr(verb_affixes).replace('],', '],\n'))
    print(arepr(verb_affixes).replace(',', ',\n'))
    return 0
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
