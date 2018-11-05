'''######################################################
# '''
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
plc_tab = 1
rf_tab = 2
arm_tab = 3
###################################################


def enter_rtc_test_menu():
    testlib.enter_menu('rtc')
    testlib.inputStr('q\r\n', tab_index=arm_tab)
    testlib.inputStr('rtc\r\n', tab_index=arm_tab)


def get12_24():
    cmd_arm = 'rtc_set_time am 2016 7 22 10 20 50 0'
    cmd_dsp = 'rtc_get_time 0'
    testlib.inputStr(cmd_arm + '\r\n', arm_tab)
    testlib.sleep(100)
    testlib.runCase(
        cmd_dsp, passlist=['rtc time 2016.07.22 10:20:50'])

    cmd_arm = 'rtc_set_time 24h 2016 7 22 10 20 50 0'
    cmd_dsp = 'rtc_get_time 1'
    testlib.inputStr(cmd_arm + '\r\n', arm_tab)
    testlib.sleep(100)
    testlib.runCase(
        cmd_dsp, passlist=['rtc time 2016.07.22 10:20:50'])


def get12_24_2():
    for y in range(1900, 2100):
        cmd_arm = 'rtc_set_time am %d 7 22 10 20 50 0' % (y)
        cmd_dsp = 'rtc_get_time 0'
        testlib.inputStr(cmd_arm + '\r\n', arm_tab)
        testlib.sleep(100)
        testlib.runCase(
            cmd_dsp, passlist=['rtc time %d.07.22 10:20:50' % (y)])

        cmd_arm = 'rtc_set_time 24h %d 7 22 10 20 50 0' % (y)
        cmd_dsp = 'rtc_get_time 1'
        testlib.inputStr(cmd_arm + '\r\n', arm_tab)
        testlib.sleep(100)
        testlib.runCase(
            cmd_dsp, passlist=['rtc time %d.07.22 10:20:50' % (y)])


def int_test():
    arm_cmds = [
        'rtc_int_for_dsp 24h 2016 7 22 10 20 50 10 T',
        'rtc_int_for_dsp 24h 2016 7 22 10 20 50 10 S',
        'rtc_int_for_dsp 24h 2016 7 22 10 20 58 10 M',
        'rtc_int_for_dsp 24h 2016 7 22 10 59 58 10 H',
        'rtc_int_for_dsp 24h 2016 7 22 23 59 58 10 d',
        'rtc_int_for_dsp 24h 2016 7 31 23 59 58 10 m',
        'rtc_int_for_dsp 24h 2016 12 31 23 59 58 10 y',
    ]
    for arm_cmd in arm_cmds:
        testlib.inputStr('rtc_int_from_arm 0\r\n')
        testlib.inputStr('%s\r\n' % (arm_cmd), arm_tab)
        testlib.logTestPop('rtc_int_from_arm 0',
                           testlib.logTest2, ['pass'], ['fail'])
        testlib.inputStr('q\r\n', arm_tab)


def main():
    enter_rtc_test_menu()
    testcases = [
        get12_24,
        int_test,
    ]
    testlib.runCaseList(testcases * 1000,
                        logpath=testlib.GetFileNameAndExt(
                            __file__)[0] + '\\LOG\\',
                        filename=testlib.GetFileNameAndExt(__file__)[1])


if __name__ == '__builtin__':
    main()
