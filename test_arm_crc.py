# $language = "Python"
# $interface = "1.0"
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
    'dma'   	: [0, 1],
    'display' : [0, 1],
    'crc_mode': [0, 1],  #0: xmodem; 1: ccitt
    'length'	: [2, 4, 10, 23, 100, 10240],
}
formatdict = {
    'dma'		: '%d',
    'display':  '%d',
    'crc_mode': '%d',
    'length'	: '%d',
}
###################################################


def enter_crc_test_menu():
    testlib.enter_menu('crc')


def crc_xmodem():
    cmd = 'crc_xmodem dma length display'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def crc_multiple():
    cmd = 'crc_multiple dma crc_mode display'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def crc_ccitt():
    cmd = 'crc_ccitt dma length display'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def crc_robust():
    cmd1 = 'crc_robust 0'
    cmd2 = 'crc_robust 1'
    testlib.runCase(cmd1)
    testlib.sleep(30000)
    testlib.inputStr('q\r\n')
    testlib.runCase(cmd2)
    testlib.sleep(30000)
    testlib.inputStr('q\r\n')
    testlib.sleep(200)


def main():
    enter_crc_test_menu()
    testcases = [crc_xmodem,
                 crc_ccitt,
                 crc_multiple,
                 crc_robust,
                 ]
    testlib.runCaseList(testcases,
                        logpath=testlib.GetFileNameAndExt(__file__)[0] + '\\LOG\\',
                        filename=testlib.GetFileNameAndExt(__file__)[1])


if __name__ == '__builtin__':
    main()
