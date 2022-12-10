import sys
import xml.etree.ElementTree as ET


def main():
    if len(sys.argv) != 3:
        print(f"Usage {sys.argv[0]} in.xml out.tex")
        exit(1)

    in_xml = sys.argv[1]
    out_tex = sys.argv[2]

    tree = ET.parse(in_xml)
    root = tree.getroot()

    req_ids = dict() 
    dd_ids= dict()

    with open(out_tex, "w") as out_file:
        module_title = root.attrib["title"]
        module_id = root.attrib["id"]
        out_file.write(f"\\section{{{module_title}}}\n\n")

        for req in root:
            type = req.tag
            id = req.attrib["id"]
            title = req.find("title").text
            descr = req.find("description").text

            ids = req_ids if type == "requirement" else dd_ids
            if id in ids:
                print(f"{in_xml}: ID {id} used by \"{ids[id]}\" and \"{title}\"")
                exit(1)
            ids[id] = title

            if type == "requirement":
                id = f"{module_id}-REQ-{id}"
                out_file.write(f"\\req{{{id}}}{{{title}}}\n"
                               f"{{{descr}}}\n"
                               f"{{")
                parents = req.find("parents")
                if parents is not None:
                    for parent in parents:
                        out_file.write(f"\\parent{{{parent.text}}} ")
                
                partition = req.find("partition")
                partition = partition.text if (partition is not None) else ""
                out_file.write(f"}}\n"
                               f"{{{partition}}}\n\n")
            else:
                id = f"{module_id}-DD-{id}"
                reason = req.find('reason').text
                out_file.write(f"\\dd{{{id}}}{{{title}}}\n"
                               f"{{{descr}}}\n"
                               f"{{{reason}}}\n\n")


if __name__=="__main__":
    main()