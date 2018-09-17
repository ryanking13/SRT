class SRTError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class UndefinedResponseError(SRTError):
    def __init__(self, msg):
        super(msg)