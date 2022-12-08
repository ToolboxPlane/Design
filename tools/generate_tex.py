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
            type = req["type"]
            id = req["id"]
            title = req["title"]
            descr = req["descr"]

            if req["type"] == "requirement":
                out_file.write(f"\\req{{{id}}}{{{title}}}\n"
                               f"{{{descr}}}\n"
                               f"{{\n")
                if "parent" in req:
                    for parent in req["parent"]:
                        out_file.write(f"\\parent{{{parent}}} ")
                
                partition = req["partition"] if "partition" in req else ""
                out_file.write(f"}}\n"
                               f"{{{partition}}}\n\n")
            else:
                reason = req['reason']
                out_file.write(f"\\dd{{{id}}}{{{title}}}\n"
                               f"{{{descr}}}\n"
                               f"{{{reason}}}\n\n")


if __name__=="__main__":
    main()