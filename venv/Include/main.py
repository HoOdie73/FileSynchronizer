import os
import workers
from jobs.json_file import json_file
from jobs.xml_file import xml_file
from threading import Thread

dirPath = input("enter directory absolute path:")
dirPath = dirPath.replace("\\", "/")
threads = []

def threadLauncher(keys):
    if not keys == 0:
        worker = workers.workers(keys)
        worker.daemon = True
        worker.start()

        threads.append(worker)

if os.path.isdir(dirPath):
    for FILE in os.listdir(dirPath):
        absPath = os.path.join(dirPath, FILE).replace("\\", "/")
        if os.path.isfile(absPath):
            if FILE.lower().endswith(".json"):
                with open(absPath, 'r') as input:
                    fileParser = json_file(input, FILE)
                    jsonKeys = fileParser.parseJson()
                    threadLauncher(jsonKeys)
            if FILE.lower().endswith(".xml"):
                fileParser = xml_file(absPath, FILE)
                xmlKeys = fileParser.parseXML()
                threadLauncher(xmlKeys)

    for thread in threads:
        thread.join()