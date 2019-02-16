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
    
#~ sys.path.append('../qalsadi')

import pandas as pd
def test(tuple_list):
    generator = alyahmor.genelex.genelex()
    
    for word, wtype in tuple_list:
        print('************%s*****'%wtype)
        list_forms =generator.generate_forms(word, word_type=wtype)
        print(arepr(list_forms).replace('),', '),\n').replace('],', '],\n'))
        list_forms =generator.generate_forms(word, word_type=wtype, vocalized = False)
        print(arepr(list_forms).replace('),', '),\n').replace('],', '],\n'))
        list_forms =generator.generate_forms( word_type=wtype, indexed=True)
        print(arepr(list_forms).replace('),', '),\n').replace('],', '],\n'))
        list_forms =generator.generate_affix_list(word_type=wtype, indexed=True)
        print(arepr(list_forms).replace('),', '),\n').replace('],', '],\n'))
def test_affix():
    generator = alyahmor.genelex.genelex()
    word = u"قصد"
    wtype="verb"
    list_forms =generator.generate_affix_list(word_type=wtype, indexed=True)
    print(arepr(list_forms).replace('),', '),\n').replace('],', '],\n'))
    wtype="noun"
    list_forms =generator.generate_affix_list(word_type=wtype, indexed= True)
    print(arepr(list_forms).replace('),', '),\n').replace('],', '],\n'))
    
def generate_dataset_affix():
    generator = alyahmor.genelex.genelex()
    word = u"فَاعِل"
    wtype="noun"
    print('\t'.join(["affix", "word", "affix_nm", "word_nm", "type", "value"]))
    
    for word, wtype  in [(u"فَاعِل", "noun"), (u"فعل", "verb")]:
        list_forms =generator.generate_affix_list(word_type=wtype, vocalized=True)
        for affix in list_forms:
            unvoc = araby.strip_tashkeel(affix)
            word_voc = affix.replace('-', word)
            word_nm = araby.strip_tashkeel(word_voc)
            value = "ok"
            tuplex = [affix, word_voc, unvoc, word_nm, wtype, value]
            print(u'\t'.join(tuplex).encode('utf8'))
def generate_datatest_affix():
    generator = alyahmor.genelex.genelex()
    verb_forms =generator.generate_affix_list(word_type="verb", vocalized=True)
    noun_forms =generator.generate_affix_list(word_type="noun", vocalized=True)
    return noun_forms, verb_forms 

def read_dataset(filename):
    """ read dataset from file"""
    dataframe = None
    df = pd.read_csv(filename, encoding="utf8", delimiter="\t");
    return df
def metric_test(affix, wtype, value, noun_affix, verb_affix):
    """  Calculate TP, TN, FP, FN """
    # how to examin metrics
    # TP : calculted   is in _orginal
    # TN : calculted   is null and   _orginal is null
    # FP : calculted   is not null and   _orginal is null
    # FN : calculted   is incorrect and   _orginal is not null
    
    if value =="ok"  and ((wtype=="noun" and affix in noun_affix) 
    or (wtype=="verb" and affix  in verb_affix)):
        return "TP"    
    elif value =="ok"  and ((wtype=="noun" and affix not in noun_affix) 
    or (wtype=="verb" and affix not in verb_affix)    ):
            return "TN"
    elif value =="no"  and ((wtype=="noun" and affix in noun_affix) 
    or (wtype=="verb" and affix  in verb_affix)    ):
            return "FP"
    elif value =="no"  and ((wtype=="noun" and affix not in noun_affix) 
    or (wtype=="verb" and affix not in verb_affix)    ):
        return "FN"

    else:
        "NON"    
def eval_datatest(dataset):
    """
    test all
    """
    df = dataset
    generator = alyahmor.genelex.genelex()
    verb_affix =generator.generate_affix_list(word_type="verb", vocalized=True)
    noun_affix =generator.generate_affix_list(word_type="noun", vocalized=True)
    df['metric'] = df.apply(lambda row: metric_test(row["affix"],row["type"], row["value"], noun_affix, verb_affix), axis=1)
    TP = df[df.metric == "TP"]['affix'].count()
    TN = df[df.metric == "TN"]['affix'].count()
    FP = df[df.metric == "FP"]['affix'].count()
    FN = df[df.metric == "FN"]['affix'].count()
    
    verb_affix_unknown = [ aff for aff in verb_affix if aff in df[df.type == "verb"]['affix']]
    noun_affix_unknown = [ aff for aff in noun_affix if aff in df[df.type == "noun"]['affix']]
    print({'unkonwn noun affix': len(noun_affix_unknown),
            'unkonwn verb affix': len(verb_affix_unknown),
            })    
    print({'TP':TP,'TN':TN, 'FP':FP, 'FN':FN})
    print({'Accuracy': (TP+TN)*100.0/(TP+TN+FP+FN),
            'F1 score': 2*TP*100.0/(2*TP+FP+FN),
            'Recall': TP*100.0/(TP+FN),
            'Precision': TP*100.0/(TP+FP),
            })

    return df

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
    #~ words = araby.tokenize(text)
    tuple_list = [l.decode('utf8').strip().split('\t') for l in lines]
    #~ test(tuple_list)
    #~ test_affix()
    #~ generate_dataset_affix()
    # read dataset
    df = read_dataset("samples/dataset.csv")
    print(df.head())
    result = eval_datatest(df)
    df3 = result[(result.metric == "FP")|(result.metric == "TN")]
    df3.to_csv(outfile, encoding='utf8', sep='\t')
            

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
