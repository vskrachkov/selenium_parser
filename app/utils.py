from contextlib import contextmanager							


class PlatformException(Exception):
    """Platform exception."""


@contextmanager
def virtualdisplay(on=False):
    if on:
        from pyvirtualdisplay import Display
        display = Display(visible=0, size=(800, 600))
        display.start()
        yield
        display.stop()
    else:
    	yield