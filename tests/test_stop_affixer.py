import sys
from pprint import pprint
sys.path.append("../alyahmor")
import stopword_affixer
import verb_affixer
import noun_affixer
import genelex
generator = genelex.genelex()
affixer = stopword_affixer.stopword_affixer()
naffixer = noun_affixer.noun_affixer()
vaffixer = verb_affixer.verb_affixer()
x=affixer.vocalize("إِلَى","و","","ه")
print(x)
print("generate one form")
x = affixer.get_form("إِلَى","و","","","ه")
print(x)



print("generate all forms")
x = affixer.generate_forms("إلى")
#x = affixer.generate_forms("إِلَى")
pprint(x)

print("generate all forms")
x = affixer.generate_forms("أن")
pprint(x)

print("generate all forms AN")
x = affixer.generate_forms("أَنْ")
pprint(x)


print("generate all forms AN like")
x = affixer.generate_forms("أنْ")
pprint(x)

word = "إلى"
stop_forms = generator.generate_forms( word, word_type="stopword")
print(stop_forms)
print("-------Details-----------")
stop_forms = generator.generate_forms( word, word_type="stopword", details=True)
print(stop_forms)
