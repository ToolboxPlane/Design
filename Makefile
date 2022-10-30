all: main.pdf

main.pdf: main.tex 
	latexmk -pdf -d main.tex

%.pdf: %.dot
	dot -T pdf -o $@ $<

clean:
	latexmk -C
	rm -rf *.pdf