import json
import fnmatch
import shutil
import queue
import time
import os
import datetime
import pathGenerator
from threading import Thread
import threading

class workers(Thread):
    directories = queue.Queue()
    genPath = pathGenerator.pathGenerator()

    def __init__(self, obj):
        Thread.__init__(self)

        self.srcRoot = obj["source"]
        self.targetRoot = obj["target"]
        self.logger = obj["log_path"]
        self.user = obj["username"]
        self.job = obj["job_name"]

    def overrideExistingFile(self, targetDirPath, srcFilePath, tgtFilePath):
        os.remove(tgtFilePath)
        shutil.copy2(srcFilePath, targetDirPath)

    def copyNewFile(self, srcFilePath, targetDirPath):
        shutil.copy2(srcFilePath, targetDirPath)

    def createLog(self, tgtFilePath, targetDirPath, srcfile, newFile):
        if newFile:
            path = os.path.join(targetDirPath, srcfile).replace("\\", "/")
        else:
            path = tgtFilePath

        logData = {
            "job_name": self.job,
            "user": self.user,
            "Timestamp": datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
            "Message": "new file added " + path
        }
        return logData

    def run(self):
        print (threading.get_ident())
        self.directories.put(self.srcRoot)

        while not self.directories.empty():
            sourceDirPath = self.directories.get()
            targetDirPath = self.genPath.getTargetDirPath(sourceDirPath, self.targetRoot, self.srcRoot)

            # create directory if it doesn't exist
            if not os.path.exists(targetDirPath):
                os.makedirs(targetDirPath)

            # outerloop .. checking source files
            for srcfile in os.listdir(sourceDirPath):
                srcFilePath = self.genPath.getSourceFilePath(sourceDirPath, srcfile)

                if os.path.isdir(srcFilePath):
                    self.directories.put(srcFilePath)

                if os.path.isfile(srcFilePath):
                    nomatch = 1

                    # open log file to output results
                    if not os.path.exists(self.logger):
                        os.makedirs(self.logger)
                    logPath = os.path.join(self.logger, self.job + ".json").replace("//", "/")
                    with open(logPath, "a+") as log:
                        # innerloop .. checking target files
                        for tgtfile in os.listdir(targetDirPath):
                            tgtFilePath = self.genPath.getTargetFilePath(targetDirPath, tgtfile)

                            if fnmatch.fnmatch(srcfile.title(), tgtfile.title()):
                                nomatch = 0
                                if not os.path.getmtime(srcFilePath) == os.path.getmtime(tgtFilePath):
                                    self.overrideExistingFile(targetDirPath, srcFilePath, tgtFilePath)
                                    logData = self.createLog(tgtFilePath, targetDirPath, srcfile, False)
                                    json.dump(logData, log, sort_keys=True, indent=4)
                                    log.write("\n")
                                break

                        if nomatch:
                            self.copyNewFile(srcFilePath, targetDirPath)
                            logData = self.createLog(tgtFilePath, targetDirPath, srcfile, True)
                            json.dump(logData, log, sort_keys=True, indent=4)
                            log.write("\n")