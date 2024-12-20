from vt_ugcs.ugcs_lib.base.__Logger import LoggerBase


class Logger(LoggerBase):
    def __init__(self, target: str = 'main'):
        super().__init__(target)
