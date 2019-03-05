from Exceptions.MissingDataException import MissingDataException
from jobs.base_class import base_class as _base
import json

class json_file(_base):

    def __init__(self, input, JSON):
        _base.__init__(self, "json")
        self.json_essentials = _base.getEssentials(self)
        self.input = input
        self.JSON = JSON

    def parseJson(self):
        try:
            obj = json.load(self.input)
            for data in self.json_essentials:
                if data not in obj:
                    raise MissingDataException("missing data in json file " + self.JSON + " " + data)

        except MissingDataException as error:
            print("Exception: " + error.args[0])
            return 0
        except:
            print("Exception: invalid json file " + self.JSON)
            return 0

        # Parsing json keys
        self.dicValues = {
            "source": obj["source"],
            "target": obj["target"],
            "log_path": obj["log_path"],
            "username": obj["username"],
            "job_name": obj["job_name"]
        }

        return self.dicValues