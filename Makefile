REQ_XMLS := $(shell find chapters/02_requirements -name '*.xml')
REQ_TEXS := $(subst xml,tex,${REQ_XMLS})
DOTS := $(shell find . -name '*.dot')
EPSS := $(subst dot,eps,${DOTS})
TEXS := $(shell find . -name '.tex')

all: main.pdf

main.pdf: $(TEXS) $(EPSS) $(REQ_TEXS)
	latexmk -pdf -d main.tex

main.html: $(TEXS) $(EPSS) $(REQ_TEXS)
	htlatex main.tex	

%.tex: %.xml
	python3 tools/generate_tex.py $< $@ $(REQ_XMLS)

%.eps: %.svg
	inkscape $< --export-eps $@ --export-ignore-filters --export-ps-level=3

%.svg: %.dot
	dot -T svg -o $@ $<

clean:
	latexmk -C
	rm -rf *.pdf $(EPSS) $(REQ_TEXS) $(shell cat .gitignore)