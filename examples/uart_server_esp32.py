# Run a loop on an esp32 

from serialtalk import SerialTalk
from serialtalk.esp32 import Esp32UART

# Define your remote callable functions.
# Here a simple multiplication, returning a float
def mult(a, b):
    return a*b

# Set up serialtalk to talk through the Esp32UART. 
# It defaults to pins 18 and 19, which are connected to the SPIKE Prime
# So you can also remove all esp32UART keyword arguments.
st = SerialTalk(Esp32UART(port=1, baudrate=115200, rx_pin=18,tx_pin=19), debug=False)

# Alternatively you can import from auto
from serialtalk.auto import SerialTalk
st = SerialTalk()

# Register our multiplication function, 
# and tell serial talk to format the result as a float
# all struct formats are supported. (https://docs.python.org/3/library/struct.html)
st.add_command(mult, "f")

# Now wait for our function to be called remotely.
# A remote device would execute st.call("mult", "ff", 5.9, 94.0)
# And the result should be: (multack, 554.6)
st.loop()