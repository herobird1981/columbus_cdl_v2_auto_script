# $language = "Python"
# $interface = "1.0"
'''precondition:download cdl to flash, so cdl will be loaded after wdt reset'''
import sys
sys.path.append('.')
import testlib
reload(testlib)
testlib.init()
if __name__ == '__builtin__':
    testlib.crt = crt
    sys.dont_write_bytecode = True
###################################################
valuedict = {
    'dma': [0, 1],
    'cs': [0],
    'block_num': [10, 100],
    'repeat': [100, 300, 1000],
    'ecc_bit': [2, 4, 8, 16],
    'ecc_mode': [0, 1],
    'pattern': [0xaa],
    # To run 4 times tests for radomization purpose
    'patterns': [0xaa, 0x98, 0x67, 0xff],
    'read_mode': [0, 1]
}
formatdict = {
    'dma': '%d',
    'cs': '%d',
    'block_num': '%d',
    'repeat': '%d',
    'ecc_bit': '%d',
    'ecc_mode': '%d',
    'pattern': '0x%x',
    'patterns': '0x%x',
    'read_mode': '%d',
}


def enter_usb0_test_menu():
    testlib.enter_menu('usb0')


def enter_usb1_test_menu():
    testlib.enter_menu('usb1')


def usb_host_mass():
    cmd = 'usb_host_mass dma 0 100 repeat'
    testlib.runAllCombo(cmd, valuedict, formatdict, passlist=['test pass'], faillist=[
                        'usb_host_mass: test fail\r\nsrc/test_usb.c'], timeout=3600)


def usb_int():
    testlib.runCase('usb_int', passlist=['test pass'], timeout=1200)


def main():
    testcases = [
        enter_usb0_test_menu,
        usb_host_mass,
        usb_int,
        enter_usb1_test_menu,
        usb_host_mass,
        usb_int,
    ]
    testlib.runCaseList(testcases,
                        logpath=testlib.GetFileNameAndExt(
                            __file__)[0] + '\\LOG\\',
                        filename=testlib.GetFileNameAndExt(__file__)[1])

if __name__ == '__builtin__':
    main()
