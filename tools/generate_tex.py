import sys
import req_lib


def main():
    if len(sys.argv) < 3:
        print(f"Usage {sys.argv[0]} in.xml out.tex other_modules.xml...")
        exit(1)

    in_xml = sys.argv[1]
    out_tex = sys.argv[2]
    other_modules = sys.argv[3:]
    other_modules = [req_lib.Module(file_name) for file_name in other_modules]

    def find_children(id):
        children = []
        for other_module in other_modules:
            for other_req in other_module.reqs:
                for parent in other_req.parents:
                    if parent == id:
                        children.append(other_req)
        return children

    def find_requirement(id):
        for other_module in other_modules:
            all = other_module.reqs + other_module.dds
            for other_req in all:
                if other_req.id == id:
                    return other_req
        return None

    module = req_lib.Module(in_xml)

    with open(out_tex, "w") as out_file:
        out_file.write(f"\\newpage\n\\section{{{module.title}}}\n\n")

        for req in module.reqs:
            out_file.write(f"\\req{{{req.id}}}{{{req.title}}}\n"
                            f"{{{req.descr}}}\n")
            if len(req.parents) == 0:
                out_file.write("{}")
            else:
                out_file.write("{\\begin{itemize}")
                for parent_id in req.parents:
                    parent = find_requirement(parent_id)
                    if parent is None:
                        print(f"{in_xml}: {req.id} parent {parent_id} does not exist")
                        exit(1)
                    out_file.write(f"\\item \\hyperref[{parent.id}]{{{parent.title}}} \n")
                out_file.write("\\end{itemize}}")
            
            if req.partition is not None:
                out_file.write(f"{{{req.partition}}}\n")
            else:
                out_file.write("{}\n")

            children = find_children(req.id)
            if len(children) == 0:
                out_file.write("{}")
            else:
                out_file.write("{\\begin{itemize}")
                for child in children:
                    out_file.write(f"\\item\\hyperref[{child.id}]{{{child.title}}} \n")
                out_file.write("\\end{itemize}}\n\n")
        for dd in module.dds:
            out_file.write(f"\\dd{{{dd.id}}}{{{dd.title}}}\n"
                            f"{{{dd.descr}}}\n"
                            f"{{{dd.reason}}}\n")
            children = find_children(req.id)
            if len(children) == 0:
                out_file.write("{}")
            else:
                out_file.write("{\\begin{itemize}")
                for child in children:
                    out_file.write(f"\\item\\hyperref[{child.id}]{{{child.title}}} \n")
                out_file.write("\\end{itemize}}\n\n")



if __name__=="__main__":
    main()