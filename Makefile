all: main.pdf

main.pdf: *.tex chapters/*/*.tex system.eps fcs.eps requirements.eps
	latexmk -pdf -d main.tex

%.eps: %.svg
	inkscape $< -E $@ --export-ignore-filters --export-ps-level=3

%.svg: %.dot
	dot -T svg -o $@ $<

clean:
	latexmk -C
	rm -rf *.pdf