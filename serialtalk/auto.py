from .serialtalk import SerialTalk

class SerialTalk(SerialTalk):
    def __init__(self, *args, **kwargs):
        ## Platform detection and imports here
        super().__init__(*args, **kwargs)
