import asyncio
from machine import Pin, PWM, ADC


async def main():
    await asyncio.gather(Bpm(), Seq(), Down(), Input())

async def Bpm():
    global pos
    while 1 == 1:
        for pos in range(8):
            led_bpm.value(1)
            await asyncio.sleep(bpm/2)
            led_bpm.value(0)
            await asyncio.sleep(bpm/2)

async def Seq():
    global xpos
    while 1 == 1:
        if pos == xpos:
            line = l[pos]
            line.duty_u16(65536)
            line = l[pos-1]
            if long != 1:
                line.duty_u16(0)
            else:
                ld = l[pos-2]
                ld.duty_u16(0)
            if pos == 7:
                xpos = 0
            else:
                xpos = pos + 1
            await asyncio.sleep_ms(1)
        await asyncio.sleep_ms(1)

async def Down():
    global ypos
    while 1 == 1:
        if pos == ypos:
            if long == 1:
                ld = l[pos-1]
                for duty in range(100000, -1, -release*1000):
                    ld.duty_u16(duty)
                    await asyncio.sleep(1/release/10000)
                ld.duty_u16(0)
            else:
                ld = l[pos]
                ld.duty_u16(100000)
                await asyncio.sleep((1/release)/2)
                for duty in range(100000, -1, -1000):
                    ld.duty_u16(duty)
                    await asyncio.sleep((1/release)/10000)
                ld.duty_u16(0)
        if pos == 7:
             ypos = 0
        else:
             ypos = pos + 1
        await asyncio.sleep_ms(1)

async def Input():
    global bpm
    global long
    global release
    while 1 == 1:
        if bt_long.value() == True:
            long = 1
        else:
            long = 0
        ivbpm = int(ADC(26).read_u16()/1000)
        bpm = 1/(lbpm[ivbpm]/60)
        ivrelease = int(ADC(27).read_u16()/1000)
        release = (ivrelease+1)
        await asyncio.sleep_ms(1)


#initialisation
release = 1
ivbpm = 1
lbpm = []
for ibpm in range(60, 260, 3):
    lbpm.append(ibpm)

long = 0
xpos = 0
ypos = 0
bpm = 0.5

bt_long = Pin(16, Pin.IN)

led_bpm = Pin(18, Pin.OUT)

frequency = 5000
l1 = PWM(15, freq=frequency)
l2 = PWM(14, freq=frequency)
l3 = PWM(13, freq=frequency)
l4 = PWM(12, freq=frequency)
l5 = PWM(11, freq=frequency)
l6 = PWM(10, freq=frequency)
l7 = PWM(9, freq=frequency)
l8 = PWM(8, freq=frequency)
l = [l1, l2, l3, l4, l5, l6, l7, l8]

#debut du progame
asyncio.run(main())
