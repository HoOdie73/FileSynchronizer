from Exceptions.MissingDataException import MissingDataException
from jobs.base_class import base_class as _base
from xml.dom import minidom

class xml_file(_base):

    def __init__(self, input, XML):
        _base.__init__(self, "xml")
        self.xml_essentials = _base.getEssentials(self)
        self.absPath = input
        self.XML = XML

    def parseXML(self):
        try:
            input = minidom.parse(self.absPath)
            for value in self.xml_essentials:
                v = input.getElementsByTagName(value)
                if len(v):
                    if (value == "source"):
                        srcRoot = v[0].firstChild.data
                        continue
                    if (value == "target"):
                        targetPath = v[0].firstChild.data
                        continue
                    if (value == "log_path"):
                        log = v[0].firstChild.data
                        continue
                    if (value == "username"):
                        user = v[0].firstChild.data
                        continue
                    if (value == "job_name"):
                        job = v[0].firstChild.data
                        continue

                raise MissingDataException("missing data in json file " + self.XML + " " + value)

        except MissingDataException as error:
            print("Exception: " + error.args[0])
            return 0
        except:
            print("Exception: invalid xml file " + self.XML)
            return 0

        self.dicValues = {
            "source": srcRoot,
            "target": targetPath,
            "log_path": log,
            "username": user,
            "job_name": job
        }

        return self.dicValues