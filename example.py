import adorable

RED = adorable.color.from_hex(0x730005)
YELLOW = adorable.color.from_name("yellow")

ERROR = YELLOW.on(RED)
ERROR += adorable.BOLD

print(ERROR("an error occured"))

c = adorable.Color4bit.from_name("yellow")
#c |= adorable.Color8bit.from_name("red")

print(c.fg("Hello World"))


doc = "A {!r} Hello {} <red>W<b>or</b>ld</red>"
print(adorable.markup(
    doc,
    style = dict(
        b = adorable.BOLD,
        red = RED
    ),
    insert = adorable.insert(
        "<b>big</b>",
        "<b>escaped</b>"
    )
))

print(adorable.markup(
    "Hello {!e} <{abc!r}>mhh</RED>",
    adorable.filter_ansi(locals()),
    adorable.insert(
        "while",
        abc = "RED"
    )
))