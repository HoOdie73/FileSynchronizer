import re
import os

class pathGenerator:

    def getTargetDirPath(self, sourceDirPath, targetRoot, srcRoot):
        pattern = re.compile("(" + srcRoot + "/)(.*)")
        extendedPath = ''
        for m in re.finditer(pattern, sourceDirPath):
            extendedPath = m.group(2)
        return os.path.join(targetRoot, extendedPath).replace("\\", "/")
        # target = self.targetRoot + (self.srcRoot - sourceDirPath)

    def getSourceFilePath(self, sourceDirPath, srcfile):
        return os.path.join(sourceDirPath, srcfile).replace("\\", "/")

    def getTargetFilePath(self, targetDirPath, tgtFileName):
        return os.path.join(targetDirPath, tgtFileName).replace("\\", "/")