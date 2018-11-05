# $language = "Python"
# $interface = "1.0"
import sys
import random
sys.path.append('.')
import testlib
reload(testlib)
testlib.init()
if __name__ == '__builtin__':
    testlib.crt = crt
    sys.dont_write_bytecode = True
###################################################


def enter_crc_test_menu():
    testlib.enter_menu('crc')


def crc16_cal():
    for i in range(100):
        length = random.randint(0, 10000)
        cmd = 'crc16_cal %d' % length
        testlib.runCase2(cmd, passlist=['XMODEM test pass', 'CCITT test pass'])


def crc32_cal():
    for i in range(100):
        length = random.randint(0, 10000)
        cmd = 'crc32_cal %d' % length
        testlib.runCase2(cmd, passlist=['Reflect test pass'])


def crc16_robust():
    testlib.inputStr('crc16_robust\r\n')
    testlib.sleep(30000)
    testlib.runCase2('q', passlist=['terminate', 'failed 0', 'cmd:>'], faillist=['$$$$$$'])


def crc32_ref_robust():
    testlib.inputStr('crc32_ref_robust\r\n')
    testlib.sleep(30000)
    testlib.runCase2('q', passlist=['terminate', 'failed 0', 'cmd:>'], faillist=['$$$$$$'])


def main():
    enter_crc_test_menu()
    testcases = [crc16_cal,
                 crc32_cal,
                 crc16_robust,
                 crc32_ref_robust,
                 ]
    testlib.runCaseList(testcases,
                        logpath=testlib.GetFileNameAndExt(
                            __file__)[0] + '\\LOG\\',
                        filename=testlib.GetFileNameAndExt(__file__)[1])


if __name__ == '__builtin__':
    main()
