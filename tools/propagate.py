import sys
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom


def main():
    if len(sys.argv) != 3:
        print(f"Usage {sys.argv[0]} in.xml out_dir/")
        exit(1)

    in_xml = sys.argv[1]
    out_dir = sys.argv[2]

    tree = ET.parse(in_xml)
    root = tree.getroot()

    sorted_reqs = dict()

    module_id = root.attrib["id"]

    for req in root:
        type = req.tag
        id = req.attrib["id"]
        title = req.find("title").text
        descr = req.find("description").text

        if type == "requirement":
            id = f"{module_id}-REQ-{id}"
            
            partition = req.find("partition")
            assert partition is not None
            partition = partition.text

            req_tuple = (title, descr, id)
            if partition not in sorted_reqs:
                sorted_reqs[partition] = [req_tuple]
            else:
                sorted_reqs[partition].append(req_tuple) 

    for partition, reqs in sorted_reqs.items():
        new_root = ET.Element("module", title=f"{partition} High-Level", id=f"{partition.lower()}-hl")
        for id, (title, descr, parent_id) in enumerate(reqs):
            req_root = ET.SubElement(new_root, "requirement", id=str(id+1))
            ET.SubElement(req_root, "title").text = title
            ET.SubElement(req_root, "description").text = descr
            parents = ET.SubElement(req_root, "parents")
            ET.SubElement(parents, "parent").text = parent_id
            ET.SubElement(req_root, "partition").text = partition

        rough_string = ET.tostring(new_root, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        text = reparsed.toprettyxml(indent="    ")
        with open(f"{out_dir}/{partition}-hl.xml", "w") as out_file:
            out_file.write(text)




if __name__=="__main__":
    main()