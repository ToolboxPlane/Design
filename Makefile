REQ_JSONS := $(shell find chapters/02_requirements -name '*.json')
REQ_TEXS := $(subst json,tex,${REQ_JSONS})

all: main.pdf

main.pdf: *.tex chapters/*/*.tex system.eps fcs.eps requirements.eps $(REQ_TEXS)
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
	rm -rf *.pdf $(REQ_TEXS)