from openrgb import OpenRGBClient
from openrgb.utils import RGBColor, DeviceType

class colors:
    red = RGBColor(255, 0, 0)
    blue = RGBColor(52, 61, 235)
    yellow = RGBColor(235, 232, 52)
    purple = RGBColor(183, 52, 235)
    green = RGBColor(58, 235, 52)
    white = RGBColor(243, 237, 245)

class tachometer:    
    def overRev():
        client = OpenRGBClient('127.0.0.1', 6742, 'My client!')
        client.devices[0].clear()
        client.devices[0].zones[3].set_color(colors.red, fast=True)
        client.devices[0].zones[2].set_color(colors.red, fast=True)
    def engineIdle():
        client = OpenRGBClient('127.0.0.1', 6742, 'My client!')
        client.devices[0].clear()
        client.devices[0].zones[3].set_color(colors.green, fast=True)
        client.devices[0].zones[2].set_color(colors.green, fast=True)
    def optimalShift():
        client = OpenRGBClient('127.0.0.1', 6742, 'My client!')
        client.devices[0].clear()
        client.devices[0].zones[3].set_color(colors.blue, fast=True)
        client.devices[0].zones[2].set_color(colors.blue, fast=True)
    def Phase1():
        client = OpenRGBClient('127.0.0.1', 6742, 'My client!')
        client.devices[0].clear()
        client.devices[0].leds[22].set_color(colors.yellow, fast=True)
    def Phase2():
        client = OpenRGBClient('127.0.0.1', 6742, 'My client!')
        client.devices[0].clear()
        client.devices[0].leds[22].set_color(colors.yellow, fast=True)
        client.devices[0].leds[23].set_color(colors.yellow, fast=True)
    def Phase3():
        client = OpenRGBClient('127.0.0.1', 6742, 'My client!')
        client.devices[0].clear()
        client.devices[0].leds[22].set_color(colors.yellow, fast=True)
        client.devices[0].leds[23].set_color(colors.yellow, fast=True)
        client.devices[0].leds[24].set_color(colors.yellow, fast=True)
    def Phase4():
        client = OpenRGBClient('127.0.0.1', 6742, 'My client!')
        client.devices[0].clear()
        client.devices[0].leds[22].set_color(colors.yellow, fast=True)
        client.devices[0].leds[23].set_color(colors.yellow, fast=True)
        client.devices[0].leds[24].set_color(colors.yellow, fast=True)
        client.devices[0].leds[25].set_color(colors.yellow, fast=True)
    def Phase5():
        client = OpenRGBClient('127.0.0.1', 6742, 'My client!')
        client.devices[0].clear()
        client.devices[0].leds[22].set_color(colors.yellow, fast=True)
        client.devices[0].leds[23].set_color(colors.yellow, fast=True)
        client.devices[0].leds[24].set_color(colors.yellow, fast=True)
        client.devices[0].leds[25].set_color(colors.yellow, fast=True)
        client.devices[0].leds[26].set_color(colors.yellow, fast=True)
    def Phase6():
        client = OpenRGBClient('127.0.0.1', 6742, 'My client!')
        client.devices[0].clear()
        client.devices[0].leds[22].set_color(colors.yellow, fast=True)
        client.devices[0].leds[23].set_color(colors.yellow, fast=True)
        client.devices[0].leds[24].set_color(colors.yellow, fast=True)
        client.devices[0].leds[25].set_color(colors.yellow, fast=True)
        client.devices[0].leds[26].set_color(colors.yellow, fast=True)
        client.devices[0].leds[27].set_color(colors.yellow, fast=True)
    def Phase7():
        client = OpenRGBClient('127.0.0.1', 6742, 'My client!')
        client.devices[0].clear()
        client.devices[0].leds[22].set_color(colors.yellow, fast=True)
        client.devices[0].leds[23].set_color(colors.yellow, fast=True)
        client.devices[0].leds[24].set_color(colors.yellow, fast=True)
        client.devices[0].leds[25].set_color(colors.yellow, fast=True)
        client.devices[0].leds[26].set_color(colors.yellow, fast=True)
        client.devices[0].leds[27].set_color(colors.yellow, fast=True)
        client.devices[0].leds[28].set_color(colors.yellow, fast=True)
    def Phase8():
        client = OpenRGBClient('127.0.0.1', 6742, 'My client!')
        client.devices[0].clear()
        client.devices[0].leds[22].set_color(colors.yellow, fast=True)
        client.devices[0].leds[23].set_color(colors.yellow, fast=True)
        client.devices[0].leds[24].set_color(colors.yellow, fast=True)
        client.devices[0].leds[25].set_color(colors.yellow, fast=True)
        client.devices[0].leds[26].set_color(colors.yellow, fast=True)
        client.devices[0].leds[27].set_color(colors.yellow, fast=True)
        client.devices[0].leds[28].set_color(colors.yellow, fast=True)
        client.devices[0].leds[29].set_color(colors.yellow, fast=True)
    def Phase9():
        client = OpenRGBClient('127.0.0.1', 6742, 'My client!')
        client.devices[0].clear()
        client.devices[0].leds[22].set_color(colors.yellow, fast=True)
        client.devices[0].leds[23].set_color(colors.yellow, fast=True)
        client.devices[0].leds[24].set_color(colors.yellow, fast=True)
        client.devices[0].leds[25].set_color(colors.yellow, fast=True)
        client.devices[0].leds[26].set_color(colors.yellow, fast=True)
        client.devices[0].leds[27].set_color(colors.yellow, fast=True)
        client.devices[0].leds[28].set_color(colors.yellow, fast=True)
        client.devices[0].leds[29].set_color(colors.yellow, fast=True)
        client.devices[0].leds[30].set_color(colors.yellow, fast=True)
    def Phase10():
        client = OpenRGBClient('127.0.0.1', 6742, 'My client!')
        client.devices[0].clear()
        client.devices[0].leds[22].set_color(colors.yellow, fast=True)
        client.devices[0].leds[23].set_color(colors.yellow, fast=True)
        client.devices[0].leds[24].set_color(colors.yellow, fast=True)
        client.devices[0].leds[25].set_color(colors.yellow, fast=True)
        client.devices[0].leds[26].set_color(colors.yellow, fast=True)
        client.devices[0].leds[27].set_color(colors.yellow, fast=True)
        client.devices[0].leds[28].set_color(colors.yellow, fast=True)
        client.devices[0].leds[29].set_color(colors.yellow, fast=True)
        client.devices[0].leds[30].set_color(colors.yellow, fast=True)
        client.devices[0].leds[31].set_color(colors.yellow, fast=True)
    def Phase11():
        client = OpenRGBClient('127.0.0.1', 6742, 'My client!')
        client.devices[0].clear()
        client.devices[0].leds[22].set_color(colors.yellow, fast=True)
        client.devices[0].leds[23].set_color(colors.yellow, fast=True)
        client.devices[0].leds[24].set_color(colors.yellow, fast=True)
        client.devices[0].leds[25].set_color(colors.yellow, fast=True)
        client.devices[0].leds[26].set_color(colors.yellow, fast=True)
        client.devices[0].leds[27].set_color(colors.yellow, fast=True)
        client.devices[0].leds[28].set_color(colors.yellow, fast=True)
        client.devices[0].leds[29].set_color(colors.yellow, fast=True)
        client.devices[0].leds[30].set_color(colors.yellow, fast=True)
        client.devices[0].leds[31].set_color(colors.yellow, fast=True)
        client.devices[0].leds[32].set_color(colors.yellow, fast=True)
    def Phase12():
        client = OpenRGBClient('127.0.0.1', 6742, 'My client!')
        client.devices[0].clear()
        client.devices[0].leds[22].set_color(colors.yellow, fast=True)
        client.devices[0].leds[23].set_color(colors.yellow, fast=True)
        client.devices[0].leds[24].set_color(colors.yellow, fast=True)
        client.devices[0].leds[25].set_color(colors.yellow, fast=True)
        client.devices[0].leds[26].set_color(colors.yellow, fast=True)
        client.devices[0].leds[27].set_color(colors.yellow, fast=True)
        client.devices[0].leds[28].set_color(colors.yellow, fast=True)
        client.devices[0].leds[29].set_color(colors.yellow, fast=True)
        client.devices[0].leds[30].set_color(colors.yellow, fast=True)
        client.devices[0].leds[31].set_color(colors.yellow, fast=True)
        client.devices[0].leds[32].set_color(colors.yellow, fast=True)
        client.devices[0].leds[33].set_color(colors.yellow, fast=True)
    def Phase13():
        client = OpenRGBClient('127.0.0.1', 6742, 'My client!')
        client.devices[0].clear()
        client.devices[0].leds[22].set_color(colors.yellow, fast=True)
        client.devices[0].leds[23].set_color(colors.yellow, fast=True)
        client.devices[0].leds[24].set_color(colors.yellow, fast=True)
        client.devices[0].leds[25].set_color(colors.yellow, fast=True)
        client.devices[0].leds[26].set_color(colors.yellow, fast=True)
        client.devices[0].leds[27].set_color(colors.yellow, fast=True)
        client.devices[0].leds[28].set_color(colors.yellow, fast=True)
        client.devices[0].leds[29].set_color(colors.yellow, fast=True)
        client.devices[0].leds[30].set_color(colors.yellow, fast=True)
        client.devices[0].leds[31].set_color(colors.yellow, fast=True)
        client.devices[0].leds[32].set_color(colors.yellow, fast=True)
        client.devices[0].leds[33].set_color(colors.yellow, fast=True)
        client.devices[0].leds[34].set_color(colors.yellow, fast=True)
    def Phase14():
        client = OpenRGBClient('127.0.0.1', 6742, 'My client!')
        client.devices[0].clear()
        client.devices[0].leds[22].set_color(colors.yellow, fast=True)
        client.devices[0].leds[23].set_color(colors.yellow, fast=True)
        client.devices[0].leds[24].set_color(colors.yellow, fast=True)
        client.devices[0].leds[25].set_color(colors.yellow, fast=True)
        client.devices[0].leds[26].set_color(colors.yellow, fast=True)
        client.devices[0].leds[27].set_color(colors.yellow, fast=True)
        client.devices[0].leds[28].set_color(colors.yellow, fast=True)
        client.devices[0].leds[29].set_color(colors.yellow, fast=True)
        client.devices[0].leds[30].set_color(colors.yellow, fast=True)
        client.devices[0].leds[31].set_color(colors.yellow, fast=True)
        client.devices[0].leds[32].set_color(colors.yellow, fast=True)
        client.devices[0].leds[33].set_color(colors.yellow, fast=True)
        client.devices[0].leds[34].set_color(colors.yellow, fast=True)
        client.devices[0].leds[35].set_color(colors.yellow, fast=True)
    def Phase15():
        client = OpenRGBClient('127.0.0.1', 6742, 'My client!')
        client.devices[0].clear()
        client.devices[0].leds[22].set_color(colors.yellow, fast=True)
        client.devices[0].leds[23].set_color(colors.yellow, fast=True)
        client.devices[0].leds[24].set_color(colors.yellow, fast=True)
        client.devices[0].leds[25].set_color(colors.yellow, fast=True)
        client.devices[0].leds[26].set_color(colors.yellow, fast=True)
        client.devices[0].leds[27].set_color(colors.yellow, fast=True)
        client.devices[0].leds[28].set_color(colors.yellow, fast=True)
        client.devices[0].leds[29].set_color(colors.yellow, fast=True)
        client.devices[0].leds[30].set_color(colors.yellow, fast=True)
        client.devices[0].leds[31].set_color(colors.yellow, fast=True)
        client.devices[0].leds[32].set_color(colors.yellow, fast=True)
        client.devices[0].leds[33].set_color(colors.yellow, fast=True)
        client.devices[0].leds[34].set_color(colors.yellow, fast=True)
        client.devices[0].leds[35].set_color(colors.yellow, fast=True)
        client.devices[0].leds[36].set_color(colors.yellow, fast=True)
    def raceOff():
        client = OpenRGBClient('127.0.0.1', 6742, 'My client!')
        client.devices[0].clear()
        client.devices[0].leds[2].set_color(colors.red, fast=True)
        client.devices[0].leds[3].set_color(colors.blue, fast=True)
        client.devices[0].leds[4].set_color(colors.yellow, fast=True)
        client.devices[0].leds[5].set_color(colors.red, fast=True)
        client.devices[0].leds[6].set_color(colors.blue, fast=True)
        client.devices[0].leds[7].set_color(colors.yellow, fast=True)
        client.devices[0].leds[8].set_color(colors.red, fast=True)
        client.devices[0].leds[9].set_color(colors.blue, fast=True)
        client.devices[0].leds[10].set_color(colors.yellow, fast=True)
        client.devices[0].leds[11].set_color(colors.red, fast=True)
        client.devices[0].leds[12].set_color(colors.blue, fast=True)
        client.devices[0].leds[13].set_color(colors.yellow, fast=True)
        client.devices[0].leds[14].set_color(colors.red, fast=True)
        client.devices[0].leds[15].set_color(colors.blue, fast=True)
        client.devices[0].leds[16].set_color(colors.yellow, fast=True)
        client.devices[0].leds[17].set_color(colors.red, fast=True)
        client.devices[0].leds[18].set_color(colors.blue, fast=True)
        client.devices[0].leds[19].set_color(colors.yellow, fast=True)
        client.devices[0].leds[20].set_color(colors.red, fast=True)
        client.devices[0].leds[21].set_color(colors.blue, fast=True)
        client.devices[0].leds[22].set_color(colors.red, fast=True)
        client.devices[0].leds[23].set_color(colors.blue, fast=True)
        client.devices[0].leds[24].set_color(colors.yellow, fast=True)
        client.devices[0].leds[25].set_color(colors.red, fast=True)
        client.devices[0].leds[26].set_color(colors.blue, fast=True)
        client.devices[0].leds[27].set_color(colors.yellow, fast=True)
        client.devices[0].leds[28].set_color(colors.red, fast=True)
        client.devices[0].leds[29].set_color(colors.blue, fast=True)
        client.devices[0].leds[30].set_color(colors.yellow, fast=True)
        client.devices[0].leds[31].set_color(colors.red, fast=True)
        client.devices[0].leds[32].set_color(colors.blue, fast=True)
        client.devices[0].leds[33].set_color(colors.yellow, fast=True)
        client.devices[0].leds[34].set_color(colors.red, fast=True)
        client.devices[0].leds[35].set_color(colors.blue, fast=True)
        client.devices[0].leds[36].set_color(colors.yellow, fast=True)
        client.devices[0].leds[37].set_color(colors.red, fast=True)
        client.devices[0].leds[38].set_color(colors.blue, fast=True)
        client.devices[0].leds[39].set_color(colors.yellow, fast=True)
        client.devices[0].leds[40].set_color(colors.red, fast=True)
        client.devices[0].leds[41].set_color(colors.blue, fast=True)
        client.devices[0].leds[42].set_color(colors.yellow, fast=True)
        client.devices[0].leds[43].set_color(colors.red, fast=True)
        client.devices[0].leds[44].set_color(colors.blue, fast=True)
        client.devices[0].leds[45].set_color(colors.yellow, fast=True)
        client.devices[0].leds[46].set_color(colors.red, fast=True)
        client.devices[0].leds[47].set_color(colors.blue, fast=True)
        client.devices[0].leds[48].set_color(colors.yellow, fast=True)
        client.devices[0].leds[49].set_color(colors.red, fast=True)
        client.devices[0].leds[50].set_color(colors.blue, fast=True)
        client.devices[0].leds[51].set_color(colors.yellow, fast=True)
        client.devices[0].leds[52].set_color(colors.red, fast=True)
        client.devices[0].leds[53].set_color(colors.blue, fast=True)
    def unlit():
        client = OpenRGBClient('127.0.0.1', 6742, 'My client!')
        client.devices[0].clear()