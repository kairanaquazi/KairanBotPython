from datetime import datetime as dt


class Logger:
    # handles normal requests
    def __init__(self, log=False):
        self.logname=log
        if not log:
            self.logname = "latest"
        self.file = open("locallog/logs/"+self.logname+".log", "w")

    def log(self, level, info, author=""):
        now = dt.now()
        text = "[" + level + "]: " + author + "@ " + str(now) + ":  " + info
        if author == "":
            text = "[" + level + "] @ " + str(now) + ":  " + info + "\n"
        self.file.write(text)
        self.file.close()
        self.file = open("locallog/logs/"+self.logname+".log", "a")

    def close(self):
        self.file.close()


class MimicLogger:
    # if logs are disabled, this has all the functions, but it does nothing
    def __init__(self, log=False):
        pass

    def log(self, level, info, author=""):
        pass

    def close(self):
        pass
