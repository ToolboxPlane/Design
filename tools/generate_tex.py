import json
import sys


def main():
    if len(sys.argv) != 3:
        print(f"Usage {sys.argv[0]} in.json out.tex")
        exit(1)

    in_json = sys.argv[1]
    out_tex = sys.argv[2]

    with open(in_json, "r") as in_file:
        contents = "\n".join(in_file.readlines())
        root = json.loads(contents)

    with open(out_tex, "w") as out_file:
        out_file.write(f"\\group{{{root['title']}}}{{{root['id']}}}\n\n")

        for req in root["requirements"]:
            if req["type"] == "requirement":
                out_file.write(f"\\req{{{req['id']}}}{{{req['title']}}}\n"
                               f"{{{req['descr']}}}\n"
                               f"{{\n")
                for parent in req["parent"]:
                    out_file.write(f"\\parent{{{parent}}} ")
                out_file.write(f"}}\n"
                               f"{{{req['partition']}}}\n\n")
            else:
                out_file.write(f"\\dd{{{req['id']}}}{{{req['title']}}}\n"
                               f"{{{req['descr']}}}\n"
                               f"{{{req['reason']}}}\n\n")


if __name__=="__main__":
    main()