import gfx, ssd1306, machine
from time import sleep

i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
graphics = gfx.GFX(128, 64, oled.pixel)
oled.text('Jeroen van Oorschot', 10, 10)
oled.show()
adc = machine.ADC(machine.Pin(39))
raw = 0
att = [machine.ADC.ATTN_0DB, machine.ADC.ATTN_2_5DB, machine.ADC.ATTN_6DB, machine.ADC.ATTN_11DB]
atti = 0
cal = [  # 100, 2000, 4000
    [0.75, 4.28, 7.95],
    [0.814, 5.52, 10.37],
    [1.09, 7.64, 14.35],
    [1.65, 13.73, 25.6], # actual 24.4 but very nonlinear at the end of this regime
]

while True:
    oled.fill(0)

    # raw = (raw + adc.read()) / 2.0
    raw = adc.read()
    if raw > 4000:
        if atti < 3:
            atti += 1
        else:
            oled.text('OVERVOLTAGE!', 0, 0)
    elif raw < 2000:
        if atti > 0:
            atti -= 1
        elif raw < 100:
            oled.text('Undervoltage', 0, 0)
    adc.atten(att[atti])
    if raw > 2000:
        val = (raw - 2000) * (cal[atti][2] - cal[atti][1]) / 2000.0 + cal[atti][1]
    else:
        val = (raw - 100) * (cal[atti][1] - cal[atti][0]) / 1900.0 + cal[atti][0]
    oled.text('{:.2f} V'.format(val, val), 0, 3 * 8)
    oled.text('{:.0f}'.format(raw), 0, 4 * 8)
    oled.text('{}: {:.1f}-{:.1f}V'.format(atti + 1, cal[atti][0], cal[atti][2]), 0, 6 * 8)
    graphics.fill_rect(10, 10, 128, 6)
    oled.show()
    sleep(0.2)
