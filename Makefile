#/usr/bin/sh
# Build alyahmor package

default: all
# Clean build files
clean:
	
backup: 
	
#create all files 
all: 

# Publish to github
publish:
	git push origin master 

md2rst:
	pandoc -s -r markdown -w rst README.md -o README.rst
md2html:
	pandoc -s -r markdown -w html README.md -o README.html

wheel:
	sudo python3 setup.py bdist_wheel
install:
	sudo python3 setup.py install
sdist:
	sudo python3 setup.py sdist
upload:
	echo "use twine upload dist/alyahmor-0.1-py2-none-any.whl"

doc:
	epydoc -v --config epydoc.conf
test:
	cd tests;python3 test_genelex.py -f samples/text.txt -o output/text.csv > output/text.out.txt
eval:
	cd tests;python3 test_genelex.py -c eval -f samples/text.txt -o output/text.csv > output/text.out.txt
testqrn:
	cd tests;python3 test_genelex.py -f samples/text.txt -o output/text.csv > output/text.out.txt
testaffix:
	cd tests;python3 test_print_affixes.py > output/affixes.text
teststops:
    # test stopwords generation based on arabicstopwords library
	cd tests;python3 test_stop_affixer_global.py> output/st.txt


