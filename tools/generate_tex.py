import sys
import req_lib


def main():
    if len(sys.argv) != 3:
        print(f"Usage {sys.argv[0]} in.xml out.tex")
        exit(1)

    in_xml = sys.argv[1]
    out_tex = sys.argv[2]

    module = req_lib.Module(in_xml)

    with open(out_tex, "w") as out_file:
        out_file.write(f"\\section{{{module.title}}}\n\n")

        for req in module.reqs:
            out_file.write(f"\\req{{{req.id}}}{{{req.title}}}\n"
                            f"{{{req.descr}}}\n"
                            f"{{")
            for parent in req.parents:
                out_file.write(f"\\parent{{{parent}}} ")
            out_file.write("}")
            
            if req.partition is not None:
                out_file.write(f"{{{req.partition}}}\n\n")
            else:
                out_file.write("{}")
        for dd in module.dds:
            out_file.write(f"\\dd{{{dd.id}}}{{{dd.title}}}\n"
                            f"{{{dd.descr}}}\n"
                            f"{{{dd.reason}}}\n\n")


if __name__=="__main__":
    main()