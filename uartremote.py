# Backward compatibility with UartRemote scripts

from serialtalk.auto import SerialTalk

class UartRemote(SerialTalk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)