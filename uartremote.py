# Backward compatibility with UartRemote scripts
try:
    from .serialtalk.auto import SerialTalk
except ImportError:
    from serialtalk.auto import SerialTalk

class UartRemote(SerialTalk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)