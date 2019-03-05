class base_class:

    def __init__(self, job):
        self.job_type = job

    def getEssentials(self):
        return ["source", "target", "username", "log_path", "job_name"]
