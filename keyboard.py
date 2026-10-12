from . import calc
from . import screen
from .const import *

def init() -> None:
    calc.write(KB.IN_MASK, 0xFF)
    calc.write(KB.OUT_MASK, 0x80)

def pressed_any() -> bool:
    calc.write(KB.OUT, 0b111_1111)
    return calc.read(KB.IN) != 0xFF

def pressed(code: int) -> bool:
    x = (code & 0b11_1000) >> 3
    y = code & 0b00_0111
    calc.write(KB.OUT, 0b000_0001 << x)
    return not (calc.read(KB.IN) & (0b000_0001 << y))

def wait_for(code: int, show_icon: bool = True) -> None:
    if pressed(code): return
    if show_icon:
        screen.set_icon(SCR.ICON.PAUSE, SCR.COLOR.BLACK)
        screen.apply_icons()
    while not pressed(code): pass
    if show_icon:
        screen.set_icon(SCR.ICON.PAUSE, SCR.COLOR.WHITE)
        screen.apply_icons()

def wait(show_icon: bool = True) -> None:
    if pressed_any(): pass
    if show_icon:
        screen.set_icon(SCR.ICON.PAUSE, SCR.COLOR.BLACK)
        screen.apply_icons()
    while not pressed_any(): pass
    if show_icon:
        screen.set_icon(SCR.ICON.PAUSE, SCR.COLOR.WHITE)
        screen.apply_icons()

def get() -> int:
    for key in range(0b000_000, 0b111_111):
        if pressed(key): return key
    return -1

def get_next(show_icon: bool = True) -> int:
    if pressed_any():
        for key in range(0b000_000, 0b111_111):
            if pressed(key): return key
    k = -1
    if show_icon:
        screen.set_icon(SCR.ICON.PAUSE, SCR.COLOR.BLACK)
        screen.apply_icons()
    wait(show_icon=False)
    for key in range(0b000_000, 0b111_111):
        if pressed(key):
            k = key
            break
    if show_icon:
        screen.set_icon(SCR.ICON.PAUSE, SCR.COLOR.WHITE)
        screen.apply_icons()
    return k