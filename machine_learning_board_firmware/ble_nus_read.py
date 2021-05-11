from bluepy.btle import Peripheral
import bluepy.btle as btle
import binascii
import struct

MyNUSUUID = "F0:B4:82:0D:EE:7F"

class MyDelegate(btle.DefaultDelegate):
    def __init__(self, params):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        print(data.decode(), flush=True, end='')

class SensorNUS(Peripheral):
    def __init__(self, addr):
        Peripheral.__init__(self, addr, addrType="random")
        self.result = 1

def main():
    nus = SensorNUS(MyNUSUUID)
    nus.setDelegate(MyDelegate(btle.DefaultDelegate))

    nus.writeCharacteristic(0x0010, struct.pack('<bb', 0x01, 0x00), True)

    while True:
        if nus.waitForNotifications(1.0):
            continue

        print( "wait...")

if __name__ == "__main__":
    main()
 
