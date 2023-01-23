import sys
from pprint import pprint
import arabicstopwords.arabicstopwords as stop
import stopwordsallforms07
from pyarabic import araby
sys.path.append("../alyahmor")


import genelex
from pprint import pprint
def get_stopword_features(lemma):
	"""
	@param lemma: stopword lemma
	@return: dict of feature value
	"""
	return stop.classed_STOPWORDS.get(lemma, [])


def get_forms(word):
	"""
	used to test new stopword list
	@param stopword:
	@return:
	"""
	return stopwordsallforms07.STOPWORDS_INDEX.get(word, [])

generator = genelex.genelex()
stop_lemmas = list(stop.classed_stopwords_list())

limit = 1000
#pprint(stop_lemmas[:limit])
# use non recognized to avoid
# stop_lemmas = ['حم', 'زمان', 'أجمع', 'هب', 'عسى', 'هن', 'هم', 'ارتد', 'هي', 'هو', 'تلكما', 'أولئكم', 'نحو', 'حسب', 'نحن', 'اللذين', 'أب', 'أخ', 'بدون', 'ذا', 'لعمر', 'لدى', 'ذه', 'ذي', 'أن', 'جعل', 'أولئك', 'هؤلاء', 'كل', 'لعل', 'إنا', 'خلال', 'راح', 'كأنما', 'استحال', 'أمسى', 'انبرى', 'أنتم', 'أنتن', 'أوشك', 'طفق', 'هناك', 'هاذين', 'سوف', 'هاتين', 'ليت', 'إلى', 'ابن', 'تين', 'أصبح', 'قد', 'شمال', 'ذلكما', 'حما', 'التي', 'أنا', 'مثل', 'هذين', 'حمو', 'حمي', 'هما', 'عند', 'ظل', 'خلف', 'تحول', 'هاته', 'هاتي', 'حوالى', 'تينك', 'أولاء', 'بعد', 'حين', 'قلما', 'تلكم', 'ذين', 'اللائي', 'خلا', 'حيث', 'صار', 'يمين', 'ذاك', 'ذات', 'اللواتي', 'معاذ', 'الذين', 'تحت', 'حاشا', 'أمام', 'أضحى', 'اللتيا', 'كلتا', 'بضع', 'انقلب', 'اللتين', 'تبدل', 'أولالك', 'اخلولق', 'حرى', 'عاد', 'سبحان', 'أقبل', 'الألاء', 'كاد', 'عن', 'كان', 'بين', 'الذي', 'أبو', 'أبي', 'هذا', 'ذينك', 'ابتدأ', 'ضمن', 'سوى', 'تانك', 'آض', 'فا', 'هذي', 'أبا', 'هذه', 'تجاه', 'رجع', 'عامة', 'لكن', 'أنشأ', 'شبه', 'فوق', 'اللاتي', 'إن', 'كأن', 'كليهما', 'كليكما', 'شرع', 'أعلى', 'طالما', 'مع', 'نفس', 'ذوي', 'ذوو', 'من', 'عدا', 'وراء', 'بات', 'على', 'علق', 'حار', 'أخي', 'أخو', 'قام', 'الألى', 'ذلكم', 'ذلكن', 'ذواتي', 'أخذ', 'ذلك', 'أخا', 'ويكأن', 'كرب', 'ذانك', 'هنالك', 'جميع', 'حول', 'تي', 'ته', 'في', 'عين', 'تلك', 'أنتما']

# stop_lemmas =  ["إِلَىَ", "سِوّى"]
# stop_lemmas =  ["أَنَّ",]
# stop_lemmas =  ["هذا",]
# stop_lemmas =  ["بعد",]

wrong_generation = {}
nb_diff_expected  = 0
nb_diff_generated = 0
for word in stop_lemmas[:limit]:
	stop_forms_vocalized = generator.generate_forms( word, word_type="stopword")
	stop_forms = list(set([araby.strip_tashkeel(form) for form in stop_forms_vocalized]))
	expected_forms = get_forms(word)
	# expected_forms = stop.stopword_forms(word)
	equal = len(stop_forms)==len(expected_forms)
	diff_expected  = [x for x in expected_forms if x not in stop_forms]
	diff_generated = [x for x in stop_forms if x not in expected_forms]
	if diff_expected or diff_generated:
		if diff_expected:  nb_diff_expected  += 1
		if diff_generated: nb_diff_generated += 1
		wrong_generation[word] = {
			"stop_forms":stop_forms,
			"stop_forms_vocalized":stop_forms_vocalized,
			"expected_forms":expected_forms,
			"stop_forms":stop_forms,
			"diff_expected":diff_expected,
			"diff_generated":diff_generated,
		}

print("********** Diff Generated *************")
print("********** Generate more cases than expected *************")
print("********** cases  %d *************"%nb_diff_generated)
for word in wrong_generation:
	if wrong_generation[word]["diff_generated"]:
		print("\t".join([word,
						 str(len(wrong_generation[word]["stop_forms"])),
						 str(len(wrong_generation[word]["expected_forms"])),
						 # str(equal),
						 ]
						))
		# wrong_generation.append(word)
		print("generated forms", wrong_generation[word]["stop_forms"])
		print("generated forms vocalized", wrong_generation[word]["stop_forms_vocalized"])
		print("expected forms", wrong_generation[word]["expected_forms"])
		print("diff  generated", wrong_generation[word]["diff_generated"])
print("********** Diff expected *************")
print("********** Generate less cases than expected *************")
print("********** cases  %d *************"%nb_diff_expected)

for word in wrong_generation:
	if wrong_generation[word]["diff_expected"]:
		print("\t".join([word,
						 str(len(wrong_generation[word]["stop_forms"])),
						 str(len(wrong_generation[word]["expected_forms"])),
						 # str(equal),
						 ]
						))
		# wrong_generation.append(word)
		print("generated forms", wrong_generation[word]["stop_forms"])
		print("generated forms vocalized", wrong_generation[word]["stop_forms_vocalized"])
		print("expected forms", wrong_generation[word]["expected_forms"])
		print("diff expected", wrong_generation[word]["diff_expected"])
print("wrong generation")
print(len(wrong_generation),"/", min(len(stop_lemmas), limit))
# print(wrong_generation)
