class AppException(Exception):
    def __init__(
        self,
        code: int,
        mess: str,
    ):
        self.code = code
        self.mess = mess

        super().__init__(mess)