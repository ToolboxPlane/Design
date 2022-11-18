import re

contents = "\n".join(open("requirements/system-ll.tex", "r").readlines())

reqs = re.findall(r"\\req\s*{([0-9]+)}\s*{(.+)}\s*{([\sa-zA-Z0-9.${}\\]+)}\s*{(.+)}\s*{(.+)}", contents)

component_hls = dict()

for id, title, descr, parents, partition in reqs:
    if partition not in component_hls:
        component_hls[partition] = list()
    
    component_hls[partition].append((len(component_hls[partition])+1, title, descr, f"Sys-LL-REQ-{id}"))

for name, reqs in component_hls.items():
    file = open(f"requirements/{name.lower()}-hl.tex", "w")
    for id, title, descr, parent in reqs:
        file.write(f"\\req\n\t{{{id}}}{{{title}}}\n"
                    f"\t{{{descr}}}\n"
                    f"\t{{\\parent{{{parent}}}}}\n\n")

print(component_hls)