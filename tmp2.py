'''######################################################
# '''
# $language = "Python"
# $interface = "1.0"
import sys
from time import localtime
sys.path.append('.')
import testlib
reload(testlib)
testlib.init()
if __name__ == '__builtin__':
    testlib.crt = crt
    sys.dont_write_bytecode = True
###################################################
plc_tab = 1
rf_tab = 2
arm_tab = 3


def enter_gpio_test_menu():
    testlib.enter_menu('gpio')


def pulse():
    # gpioe26 J162(9)
    # gpioa24 J151(9) J127
    pulse_width_u = 1000
    interval_m = 1
    # cmd = 'gpio_debounce a 25 1 1000 a 24 %d ' % (pulse_width_u)
    cmd = 'gpio_debounce e 25 1 1000 e 26 %d ' % (pulse_width_u)
    # cmd = 'gpio_debounce f 3 1 1000 f 2 %d ' % (pulse_width_u)
    while True:
        testlib.inputStr(cmd + '\r\n')
        testlib.sleep(interval_m)
        testlib.inputStr('q\r\n')


def arm_reset_dsp():
    testlib.enter_menu('sys')
    for i in range(1000):
        testlib.inputStr('reset 34\r\n')
        testlib.sleep(8000)
        testlib.inputStr('reset 35\r\n')
        testlib.sleep(8000)


def global_reset():
    testlib.inputStr('q\r\n')
    while True:
        testlib.inputStr('sys\r\n')

        testlib.runCase2('reset 36', passlist=[
            'Select the device to test :'], faillist=['@@@@@@@'])
        testlib.sleep(1000)


def arm_reset_plc():
    testlib.inputStr('q\r\n')
    testlib.inputStr('sys\r\n')
    while True:
        testlib.inputStr('reset 34\r\n')
        testlib.sleep(5000)


def arm_reset_rf():
    testlib.inputStr('q\r\n')
    while True:
        testlib.inputStr('sys\r\n')
        testlib.inputStr('reset 35\r\n')
        testlib.sleep(1000)


def rf_wdt():
    testlib.inputStr('q\r\n')
    while True:
        testlib.inputStr('watch dog timer\r\n')
        testlib.runCase2('wdt_reset 0x100 1\r\n', passlist=[
                         'Select the device to test :'])


def main():
    enter_gpio_test_menu()
    testcases = [
        # pulse,
        # arm_reset_dsp,
        rf_wdt,
        # arm_reset_plc,
    ]
    # testlib.runCaseList(testcases)
    # testlib.runCaseList(testcases,
    #                     logpath=testlib.GetFileNameAndExt(
    #                         __file__)[0] + '\\LOG\\',
    #                     filename=testlib.GetFileNameAndExt(__file__)[1])
    for tc in testcases:
        tc()

if __name__ == '__builtin__':
    main()
