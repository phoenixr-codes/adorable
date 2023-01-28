import adorable
from adorable import color

def test_nocolor():
    adorable.use("NOCOLOR")
    RED = color.from_name("red")
    assert RED.fg("Hello") == "\x1b[mHello\x1b[0m"
    
