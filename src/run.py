from machine import Pin, I2C
import ssd1306
from collections import deque


ADDR_BUS = {
    "A0": Pin(4, Pin.OUT),
    "A1": Pin(3, Pin.OUT),
    "A2": Pin(2, Pin.OUT),
    "A3": Pin(1, Pin.OUT),
    "A4": Pin(0, Pin.OUT),
}

DATA_BUS = {
    "D0": Pin(6, Pin.OUT),
    "D1": Pin(7, Pin.OUT),
    "D2": Pin(8, Pin.OUT),
    "D3": Pin(9, Pin.OUT),
    "D4": Pin(13, Pin.OUT),
    "D5": Pin(12, Pin.OUT),
    "D6": Pin(11, Pin.OUT),
    "D7": Pin(10, Pin.OUT),
}

CS = Pin(18, Pin.OUT, Pin.PULL_UP)
RW = Pin(19, Pin.OUT, Pin.PULL_UP)

key_0 = Pin(14, Pin.IN, Pin.PULL_UP)
key_1 = Pin(15, Pin.IN, Pin.PULL_UP)
key_en = Pin(21, Pin.IN, Pin.PULL_UP)

i2c = I2C(0, sda=Pin(16), scl=Pin(17))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

ADDR_LEN = 5
DATA_LEN = 8

addr_reg = deque([], maxlen=ADDR_LEN)
data_reg = deque([], maxlen=DATA_LEN)


def setup():
    global addr_reg
    global data_reg


addr_callback = lambda key: addr_reg.append(key)
data_callback = lambda key: data_reg.append(key)


def send_gpio():
    CS.off()
    RW.off()

    ADDR_BUS["A0"].value(addr_reg[0])
    ADDR_BUS["A1"].value(addr_reg[1])
    ADDR_BUS["A2"].value(addr_reg[2])
    ADDR_BUS["A3"].value(addr_reg[3])
    ADDR_BUS["A4"].value(addr_reg[4])

    DATA_BUS["D0"].value(data_reg[0])
    DATA_BUS["D1"].value(data_reg[1])
    DATA_BUS["D2"].value(data_reg[2])
    DATA_BUS["D3"].value(data_reg[3])
    DATA_BUS["D4"].value(data_reg[4])
    DATA_BUS["D5"].value(data_reg[5])
    DATA_BUS["D6"].value(data_reg[6])
    DATA_BUS["D7"].value(data_reg[7])

    CS.on()
    RW.on()
    addr_reg.clear()
    data_reg.clear()


while True:
    while len(addr_reg) != ADDR_LEN and len(data_reg) != DATA_LEN:
        if len(addr_reg) != 5:
            if not key_0.value():
                addr_callback(0)
            if not key_1.value():
                addr_callback(1)
            display.text = f"A: {list(addr_reg)} | D: ________"
            continue

        if len(data_reg) != 8:
            if not key_0.value():
                data_callback(0)
            if not key_1.value():
                data_callback(1)
            display.text = f"A: {list(addr_reg)} | D: {list(data_reg)}"
            continue

    if not key_en.value():
        send_gpio()
