# Alyahmor اليحمور
Arabic flexionnal morphology generator

## Description
The Alyahmor produce a word form from (prefix, lemma, suffix).
It has many functionalities:
- Generate word forms from given word and affixes
- Generate all word forms by adding verbal or nominal affixes according to word type
- Generate all affixes combination for verbs or nouns which can be used in morphology analysis.


#### Developpers: 
 Taha Zerrouki: http://tahadz.com
    taha dot zerrouki at gmail dot com

Features |   value
---------|---------------------------------------------------------------------------------
Authors  | [Authors.md](https://github.com/linuxscout/alyahmor/master/AUTHORS.md)
Release  | 0.1 
License  |[GPL](https://github.com/linuxscout/alyahmor/master/LICENSE)
Tracker  |[linuxscout/alyahmor/Issues](https://github.com/linuxscout/alyahmor/issues)
Accounts  |[@Twitter](https://twitter.com/linuxscout) 
<!-- Website  |[https://pypi.python.org/pypi/alyahmor](https://pypi.python.org/pypi/alyahmor)-->
<!--Doc  |[package Documentaion](http://pythonhosted.org/alyahmor/)
Source  |[Github](http://github.com/linuxscout/alyahmor)-->
<!--Download  |[sourceforge](http://alyahmor.sourceforge.net)-->
<!-- Feedbacks  |[Comments](http://tahadz.com/alyahmor/contact) -->




## Citation
If you would cite it in academic work, can you use this citation
```
T. Zerrouki‏, Alyahmor, Arabic mophological  generator Library for python.,  https://pypi.python.org/pypi/alyahmor/, 2019
```
or in bibtex format
```bibtex
@misc{zerrouki2019alyahmor,
  title={alyahmor, Arabic mophological generator Library for python.},
  author={Zerrouki, Taha},
  url={https://pypi.python.org/pypi/alyahmor},
  year={2019}
}
```
## Applications
* Text Stemming
* Morphology analysis 
* Text Classification and categorization
* Spellchecking


## Features  مزايا
 - Arabic word Light Stemming.
* Features:
	- Generate word forms from given word and affixes
	- Generate all word forms by adding verbal or nominal affixes according to word type
	- Generate all affixes combination for verbs or nouns which can be used in morphology analysis.


 


## Installation
```
pip install alyahmor
```    
### Requirements
``` 
pip install -r requirements.txt 
```
 - libQutrub: Qutrub verb conjugation library: http://pypi.pyton/LibQutrub
 - PyArabic: Arabic language tools library   : http://pypi.pyton/pyarabic
 - Arramooz-pysqlite : Arabic dictionary


## أصل التسمية

**اليَحْمُور،** وهو الحسن بن المعالي الباقلاني أبو علي النحوي الحلي  شيخ العربية في زمانه في بغداد من تلامذة أبي البقاء العكبري ت ٦٣٧هـ

وكتب بخطه كثيراً من الأدب واللغة وسائر الفنون، وكان له همةٌ عالية، وحرصٌ شديد؛ وتحصيل الفوائد مع علو سنه، وضعف بصره، وكثرة محفوظه، وصدقه، وثقته، وتواضعه، وكرم أخلاقه.

وانتقل آخر عمره إلى مذهب الشافعي، **وانتهت إليه رياسة النحو.** مولده سنة ثمان وستين وخمسمائة، وتوفي سنة سبع وثلاثين وستمائة.
[المزيد عن اليحمور ](doc/alyahmor.md)
  
Usage
=====




## Example 




### Generate words forms

It joins word with affixes with suitable correction
for example

بال+كتاب +ين => بالكتابين
ب+أبناء+ه => بأبنائه

#### Nouns
To generate all forms of the word كتاب as noun use 
``` python
>>> import alyahmor.genelex
>>> generator = alyahmor.genelex.genelex()
>>> word = u"كِتِاب"
>>> noun_forms = generator.generate_forms( word, word_type="noun")
>>>noun_forms
[u'آلْكِتَاب', u'آلْكِتَابا', u'آلْكِتَابات', u'آلْكِتَابان', u'آلْكِتَابة', u'آلْكِتَابتان', u'آلْكِتَابتين', u'آلْكِتَابون', u'آلْكِتَابي', u'آلْكِتَابيات'
....]

```
#### Verbs
To generate all forms of the word كتاب as verb, use 
``` python
>>> import alyahmor.genelex
>>> generator = alyahmor.genelex.genelex()
>>> word = u"استعمل"
>>> verb_forms = generator.generate_forms( word, word_type="verb")
>>>verb_forms
[u'أَأَسْتَعْمِلَ', u'أَأَسْتَعْمِلَكَ', u'أَأَسْتَعْمِلَكُمَا', u'أَأَسْتَعْمِلَكُمْ', u'أَأَسْتَعْمِلَكُنَّ', u'أَأَسْتَعْمِلَنَا', u'أَأَسْتَعْمِلَنِي', u'أَأَسْتَعْمِلَنَّ', u'أَأَسْتَعْمِلَنَّكَ', u'أَأَسْتَعْمِلَنَّكُمَا', 

....]
```

#### Generate non vocalized forms
To generate all forms of the word كتاب as noun without vocalization  use 
``` python
>>> import alyahmor.genelex
>>> generator = alyahmor.genelex.genelex()
>>> word = u"كِتِاب"
>>> noun_forms = generator.generate_forms( word, word_type="noun", vocalized=False)
>>>noun_forms
[u'آلكتاب', u'آلكتابا', u'آلكتابات', u'آلكتابان', u'آلكتابة', u'آلكتابتان', u'آلكتابتين', u'آلكتابون', u'آلكتابي', u'آلكتابيات',
....]

```
#### Generate a dictionary of  vocalized forms indexed by unvocalized form
To generate all forms of the word كتاب as noun as a dict of grouped all vocalized forms by unvocalized form  use 
``` python
>>> import alyahmor.genelex
>>> generator = alyahmor.genelex.genelex()
>>> word = u"كِتِاب"
>>> noun_forms = generator.generate_forms( word, word_type="noun", indexed=True)
>>>noun_forms
{u'أككتابة': [u'أكَكِتَِابَةِ', u'أكَكِتَِابَةٍ'],
 u'أوككتابة': [u'أَوَكَكِتَِابَةِ', u'أَوَكَكِتَِابَةٍ'],
 u'وكتابياتهم': [u'وَكِتَِابياتهِمْ', u'وَكِتَِابِيَاتُهُمْ', u'وَكِتَِابِيَاتِهِمْ', u'وَكِتَِابِيَاتُهِمْ', u'وَكِتَِابياتهُمْ'],
 u'وكتابياتهن': [u'وَكِتَِابياتهِنَّ', u'وَكِتَِابياتهُنَّ', u'وَكِتَِابِيَاتِهِنَّ', u'وَكِتَِابِيَاتُهِنَّ', u'وَكِتَِابِيَاتُهُنَّ'],
 u'وللكتابات': [u'وَلِلْكِتَِابَاتِ', u'وَلِلْكِتَِابات'],
 u'أبكتابتكن': [u'أَبِكِتَِابَتِكُنَّ'],
 u'أبكتابتكم': [u'أَبِكِتَِابَتِكُمْ'],
 u'أكتابياتهن': [u'أَكِتَِابياتهِنَّ', u'أَكِتَِابِيَاتِهِنَّ', u'أَكِتَِابياتهُنَّ', u'أَكِتَِابِيَاتُهُنَّ', u'أَكِتَِابِيَاتُهِنَّ'],
 u'فكتاباتهم': [u'فَكِتَِاباتهِمْ', u'فَكِتَِابَاتُهُمْ', u'فَكِتَِابَاتُهِمْ', u'فَكِتَِاباتهُمْ', u'فَكِتَِابَاتِهِمْ'],
 u'بكتابياتكن': [u'بِكِتَِابِيَاتِكُنَّ', u'بِكِتَِابياتكُنَّ'],
....
}

```
### Generate affixes lists
Alyahmor generate affixes listes for verbs and nouns
```python
>>> verb_affix =generator.generate_affix_list(word_type="verb", vocalized=True)
>>>verb_affix
[u'أَفَسَت-يننِي', u'أَ-ونَا', u'ي-ونكَ', u'فَلَ-تاكَ', u'وَلََن-هُنَّ', u'أَت-وننَا', u'وَ-اكُنَّ', u'ن-ننَا', u'وَت-وهَا', u'أَي-نهُمَا', ....]

>>> noun_affix =generator.generate_affix_list(word_type="noun", vocalized=True)
>>> noun_affix
[u'أكَ-ياتكَ', u'فَ-ِيَاتِكُمَا', u'أكَ-ياتكِ', u'أَوَكَ-ِينَا', u'أَلِ-ِيِّهِنَّ', u'أَفَ-َكُمَا', u'أَفَ-ِيَّتِهِمْ', u'أَفَكَ-ياتهُمْ', u'فَبِ-ِيِّكُمْ', u'وَلِ-ِيَّتِهَا', ....]

```

Generate Unvocalized affixes 
```python
>>> noun_affix =generator.generate_affix_list(word_type="noun", vocalized=False)
>>> noun_affix
[u'-', u'-ا', u'-ات', u'-اتك', u'-اتكم', u'-اتكما', u'-اتكن', u'-اتنا', u'-اته', u'-اتها', ...]

```


### Files

* file/directory    category    description 

tests/samples/dataset.csv	A list of verified affixes

## Featured Posts


