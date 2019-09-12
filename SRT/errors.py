class SRTError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class SRTLoginError(SRTError):
    def __init__(self):
        super().__init__("Login failed, please check ID/PW")


class SRTResponseError(SRTError):
    def __init__(self, msg):
        super().__init__(msg)


class SRTDuplicateError(SRTResponseError):
    def __init__(self, msg):
        super().__init__(msg)


class SRTNotLoggedInError(SRTError):
    def __init__(self):
        super().__init__("Not logged in")
