REQ_JSONS := $(shell find chapters/02_requirements -name '*.json')
REQ_TEXS := $(subst json,tex,${REQ_JSONS})
DOTS := $(shell find . -name '*.dot')
EPSS := $(subst dot,eps,${DOTS})
TEXS := $(shell find . -name '.tex')

all: main.pdf

main.pdf: $(TEXS) $(EPSS) $(REQ_TEXS)
	echo "${REQ_TEXS}"
	latexmk -pdf -d main.tex

%.tex: %.json
	python3 tools/generate_tex.py $< $@

%.eps: %.svg
	inkscape $< -E $@ --export-ignore-filters --export-ps-level=3

%.svg: %.dot
	dot -T svg -o $@ $<

clean:
	latexmk -C
	rm -rf *.pdf $(EPSS) $(REQ_TEXS)