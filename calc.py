import picoease as raw
from time import sleep_ms

read = raw.read
write = raw.write
init = raw.init

er0 = 0x0000

def halt() -> None:
    global er0
    global pc
    print("halt")
    raw.pwrite(0x0D, 0x08)
    er0 = raw.pread(0x04)

def resume() -> None:
    print("resume")
    print(er0)
    raw.run(0x0000 | ((er0 >> 8) & 0xFF), 0x0100 | (er0 & 0xFF))
    raw.pwrite(0x0D, 0x00)
    raw.run(0xFE0F, 0xFE8F)

def connect() -> None:
    raw.connect()
    halt()