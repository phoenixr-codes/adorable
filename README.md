<p align="center">
  <h1 align="center">adorable</h1>
  <p align="center">
    Make the UI of your project <b>adorable</b>.
  </p>
</p>

Basic Usage
-----------

```python
import adorable
from adorable import color

RED = color.from_name("red")
print(RED.fg("Hello adorable World"))


BLUE = color.from_hex(0x0AF)
DARK = color.from_rgb((38, 38, 38))
col = BLUE.on(DARK)

adorable.printc("Hello", "World", style = col)

```


Links
-----

* [Documentation](https://phoenixr-codes.github.io/adorable)
* [Source Code](https://github.com/phoenixr-codes/adorable)
* [PyPI](https://pypi.org/project/adorable)
