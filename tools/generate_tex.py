import sys
import xml.etree.ElementTree as ET


def main():
    if len(sys.argv) != 3:
        print(f"Usage {sys.argv[0]} in.json out.tex")
        exit(1)

    in_xml = sys.argv[1]
    out_tex = sys.argv[2]

    tree = ET.parse(in_xml)
    root = tree.getroot()

    with open(out_tex, "w") as out_file:
        title = root.attrib["title"]
        id = root.attrib["id"]
        out_file.write(f"\\group{{{title}}}{{{id}}}\n\n")

        for req in root:
            id = req.attrib["id"]
            type = req.attrib["type"]
            title = req.find("title").text
            descr = req.find("description").text

            if type == "requirement":
                out_file.write(f"\\req{{{id}}}{{{title}}}\n"
                               f"{{{descr}}}\n"
                               f"{{")
                parents = req.find("parents")
                if parents is not None:
                    for parent in parents:
                        out_file.write(f"\\parent{{{parent.text}}} ")
                
                partition = req.find("partition")
                partition = partition.text if partition is not None else ""
                out_file.write(f"}}\n"
                               f"{{{partition}}}\n\n")
            else:
                print(id, req.tag)
                reason = req.find('reason').text
                out_file.write(f"\\dd{{{id}}}{{{title}}}\n"
                               f"{{{descr}}}\n"
                               f"{{{reason}}}\n\n")


if __name__=="__main__":
    main()