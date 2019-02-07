#!/usr/bin/python
# -*- coding = utf-8 -*-
from __future__ import absolute_import

import argparse
import sys
import sys
sys.path.append('..')
import pyarabic.araby as araby
from pyarabic.arabrepr import arepr
import alyahmor.genelex

def grabargs():
    parser = argparse.ArgumentParser(description='Test Qalsadi Analex.')
    # add file name to import and filename to export
    
    parser.add_argument("-f", dest="filename", required=True,
    help="input file to convert", metavar="FILE")
    
    parser.add_argument("-o", dest="outfile", nargs='?', 
    help="Output file to convert", metavar="OUT_FILE")
    
    parser.add_argument("--all", type=bool, nargs='?',
                        const=True, 
                        help="")
    args = parser.parse_args()
    return args
    
sys.path.append('../qalsadi')

import pandas as pd

def main(args):
    args = grabargs()
    filename = args.filename
    outfile = args.outfile
    try:
        myfile=open(filename)
    except:
        print("Can't Open file %s"%filename)
        sys.exit()
    lines = myfile.readlines()
    debug=True;
    limit=500
    generator = alyahmor.genelex.genelex()
    #~ words = araby.tokenize(text)
    tuple_list = [l.decode('utf8').strip().split('\t') for l in lines]
    for word, wtype in tuple_list:
        if wtype == "noun":
            print('************Noun*****')
            list_forms = generator.generate_noun_forms(word)
            #~ print(arepr(noun_forms).replace('),', '),\n').replace('],', '],\n'))
            unv_forms = generator.get_unvocalized_forms(list_forms)
            #~ print(u"\n".join((unv_forms)).encode('utf8'))
            voc_forms = generator.get_vocalized_forms(list_forms)
            #~ print(u"\n".join((voc_forms)).encode('utf8')) 
            voc_forms_dict = generator.get_vocalized_forms_dict(list_forms)
            print(arepr(voc_forms_dict).replace('],', '],\n'))

        if wtype == "verb":
            print('************verb*****')
            list_forms =generator.generate_verb_forms(word)
            #~ print(arepr(verb_forms).replace('),', '),\n').replace('],', '],\n'))
            unv_forms = generator.get_unvocalized_forms(list_forms)
            #~ print(u"\n".join((unv_forms)).encode('utf8'))
            voc_forms = generator.get_vocalized_forms(list_forms)
            #~ print(u"\n".join((voc_forms)).encode('utf8'))
            voc_forms_dict = generator.get_vocalized_forms_dict(list_forms[:10])
            print(arepr(voc_forms_dict).replace('],', '],\n'))

            
            

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
