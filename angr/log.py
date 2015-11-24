import logging

_original_emit = logging.StreamHandler.emit

class Loggers(object):
    def __init__(self, default_level=logging.INFO):
        """
        A dumb and simple way to aggregate all loggers in a convenient way
        """
        # All loggers are an attr of self for tab completion in iPython
        # (with . replaced with _)
        self._loggerdict = logging.Logger.manager.loggerDict
        for name, logger in self._loggerdict.iteritems():
            attr = name.replace('.', '_')
            setattr(self, attr, logger)

        fmt='%(levelname)-7s | %(asctime)-23s | %(name)-8s | %(message)s'

        # The default level is INFO
        logging.basicConfig(format=fmt, level=default_level)
        logging.StreamHandler.emit = self._emit_wrap

    def setall(self, level):
        for name in self._loggerdict.keys():
            logging.getLogger(name).setLevel(level)

    @staticmethod
    def _emit_wrap(*args, **kwargs):
        #import ipdb; ipdb.set_trace()
        record = args[1]
        color = hash(record.name) % 8 + 30
        try:
            record.name = ("\x1b[%dm" % color) + record.name + "\x1b[0m"
        except Exception:
            pass

        try:
            record.msg = ("\x1b[%dm" % color) + record.msg + "\x1b[0m"
        except Exception:
            pass
        _original_emit(*args, **kwargs)


