import xml.etree.ElementTree as ET

class ReqBase:
    def __init__(self, id : int, title : str, descr : str) -> None:
        self.id = id
        self.title = title 
        self.descr = descr

    def __init__(self, xml_req, module_id : str, req_type : str) -> None:
        self.id = f"{module_id}-{req_type}-{xml_req.attrib['id']}"
        self.title = xml_req.find("title").text
        self.descr = xml_req.find("description").text


class Requirement(ReqBase):
    def __init__(self, id : int, title : str, descr : str, parents : list, partition : str) -> None:
        super().__init__(id=id, title=title, descr=descr)
        self.parents = parents
        self.partition = partition

    def __init__(self, xml_req, module_id : str) -> None:
        super().__init__(xml_req=xml_req, module_id=module_id, req_type="REQ")
        parents = xml_req.find("parents")
        self.parents = []
        if parents is not None:
            for parent in parents:
                self.parents.append(parent.text)
        
        partition = xml_req.find("partition")
        self.partition = partition.text if (partition is not None) else None


class DesignDecision(ReqBase):
    def __init__(self, id : int, title : str, descr : str, reason : str) -> None:
        super().__init__(id=id, title=title, descr=descr)
        self.reason = reason
    
    def __init__(self, xml_req, module_id : str) -> None:
        super().__init__(xml_req=xml_req, module_id=module_id, req_type="DD")
        self.reason = xml_req.find('reason').text



class Module:
    def __init__(self, xml_file) -> None:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        self.title = root.attrib["title"]
        self.id = root.attrib["id"]
        self.reqs =[]
        self.dds = []

        for req in root:
            type = req.tag

            if type == "requirement":
                self.reqs.append(Requirement(req, module_id=self.id))
            else:
                self.dds.append(DesignDecision(req, module_id=self.id))
