'''######################################################
# '''
# $language = "Python"
# $interface = "1.0"
import sys
from time import localtime, time
sys.path.append('.')
import testlib
reload(testlib)
testlib.init()
if __name__ == '__builtin__':
    testlib.crt = crt
    sys.dont_write_bytecode = True
testlib.MSGPOP = False
###################################################
valuedict = {
    'timer_id': [0, 1, 2, 3],
    'trim_mode': [3, 2, 1, 0],
    # 'trim_val': [-128, -64, -1, 0, 1, 64, 127],
    'trim_val': [-128, -120, -100, -86, -64, -32, -16, -8, -4, -2, -1, 0, 1, 2, 4, 8, 16, 32, 64, 90, 100, 120, 127],
}
formatdict = {
    'timer_id': '%d',
    'trim_mode': '%d',
    'trim_val': '%d',
}
plc_tab = 1
rf_tab = 2
arm_tab = 3
###################################################


def enter_rtc_test_menu():
    testlib.enter_menu('rtc')


def set_get():
    cs = int((time() - int(time())) * 100)
    cmd_set = 'rtc_set_time 24h %d %d %d %d %d %d %d' % (
        localtime()[:6] + (int((time() - int(time())) * 100),))
    cmd_set = 'rtc_set_time 24h %d %d %d %d %d %d %d' % (
        localtime()[:6] + (cs,))
    cmd_get = 'rtc_get_time 12h'
    testlib.inputStr(cmd_set + '\r\n')
    testlib.runCase(cmd_get, passlist=[
                    'rtc time %d.%02d.%02d %02d:%02d:%02d' % localtime()[:6]])


def set12_24():
    cmd1 = 'rtc_set_time am 2016 7 12 7 21 23 00'
    testlib.runCase(
        cmd1, passlist=['rtc time 2016.07.12 07:21:23:00 am week=2'])

    cmd2 = 'rtc_set_time pm 2016 7 12 7 21 23 99'
    testlib.runCase(
        cmd2, passlist=['rtc time 2016.07.12 07:21:23:99 pm week=2'])

    cmd3 = 'rtc_set_time 24h 2016 7 12 7 21 23 00'
    testlib.runCase(cmd3, passlist=['rtc time 2016.07.12 07:21:23:00 week=2'])

    cmd4 = 'rtc_set_time 24h 2016 7 12 17 21 23 99'
    testlib.runCase(cmd4, passlist=['rtc time 2016.07.12 17:21:23:99 week=2'])


def boundry():
    testlib.runCase('rtc_set_time pm 1970 7 12 7 21 23 00', passlist=[
                    'rtc time 1970.07.12 07:21:23:00 pm week=0'])
    testlib.runCase('rtc_set_time am 2099 7 12 7 21 23 99', passlist=[
                    'rtc time 2099.07.12 07:21:23:99 am week=0'])
    testlib.runCase('rtc_set_time 24h 2016 1 12 19 21 23 00', passlist=[
                    'rtc time 2016.01.12 19:21:23:00 week=2'])
    testlib.runCase('rtc_set_time 24h 2016 12 12 19 21 23 00', passlist=[
                    'rtc time 2016.12.12 19:21:23:00 week=1'])
    testlib.runCase('rtc_set_time 24h 2016 7 1 19 21 23 00', passlist=[
                    'rtc time 2016.07.01 19:21:23:00 week=5'])
    testlib.runCase('rtc_set_time 24h 2016 7 31 19 21 23 00', passlist=[
                    'rtc time 2016.07.31 19:21:23:00 week=0'])
    testlib.runCase('rtc_set_time 24h 2016 7 12 0 21 23 00', passlist=[
                    'rtc time 2016.07.12 00:21:23:00 week=2'])
    testlib.runCase('rtc_set_time 24h 2016 7 12 23 21 23 00', passlist=[
                    'rtc time 2016.07.12 23:21:23:00 week=2'])
    testlib.runCase(' rtc_set_time 24h 2016 7 12 19 0 23 00', passlist=[
                    'rtc time 2016.07.12 19:00:23:00 week=2'])
    testlib.runCase('rtc_set_time 24h 2016 7 12 19 59 23 00', passlist=[
                    'rtc time 2016.07.12 19:59:23:00 week=2'])
    testlib.runCase('rtc_set_time 24h 2016 7 12 19 21 0 00', passlist=[
                    'rtc time 2016.07.12 19:21:00:00 week=2'])
    testlib.runCase('rtc_set_time 24h 2016 7 12 19 21 59 00', passlist=[
                    'rtc time 2016.07.12 19:21:59:00 week=2'])
    testlib.runCase('rtc_set_time 24h 2016 2 29 23 59 55 00', passlist=[
                    'rtc time 2016.02.29 23:59:55:00 week=1'])
    testlib.runCase('rtc_set_time 24h 2015 2 28 23 59 55 00', passlist=[
                    'rtc time 2015.02.28 23:59:55:00 week=6'])


def alarm():
    testlib.runCase('rtc_alarm 24h 2016 12 31 23 59 10 00 S', passlist=[
        'SECOND'])
    testlib.runCase('rtc_alarm pm 2016 12 31 11 50 58 00 M', passlist=[
        'MINUTE'])
    testlib.runCase('rtc_alarm am 2016 12 31 8 59 58 00 H', passlist=[
        'HOUR'])
    testlib.runCase('rtc_alarm 24h 2016 12 20 23 59 58 00 d', passlist=[
        'DAY'])
    testlib.runCase('rtc_alarm 24h 2016 10 31 23 59 58 00 m', passlist=[
        'MONTH'])
    testlib.runCase('rtc_alarm 24h 2016 12 31 23 59 58 00 y', passlist=[
        'YEAR'])
    testlib.runCase('rtc_alarm 24h 2016 12 31 23 59 58 00 T', passlist=[
        '100THSEC'])


def alarm_mul():
    testlib.runCase('rtc_alarm_multi_mode 24h 2016 12 31 23 59 10 0 S',
                    passlist=['SECOND'])
    testlib.runCase('rtc_alarm_multi_mode 24h 2016 12 31 23 59 57 0 M',
                    passlist=['MINUTE'])
    testlib.runCase('rtc_alarm_multi_mode 24h 2016 12 31 23 59 57 0 H',
                    passlist=['HOUR'])
    testlib.runCase('rtc_alarm_multi_mode 24h 2016 12 31 23 59 57 0 d',
                    passlist=['DAY'])
    testlib.runCase('rtc_alarm_multi_mode 24h 2016 12 31 23 59 57 0 m',
                    passlist=['MONTH'])
    testlib.runCase('rtc_alarm_multi_mode 24h 2016 12 31 23 59 57 99 y',
                    passlist=['YEAR'])
    testlib.runCase('rtc_alarm_multi_mode 24h 2016 12 31 23 59 10 0 T',
                    passlist=['100THSEC'])
    testlib.runCase('rtc_alarm_multi_mode 24h 2016 12 31 23 59 57 0 ymdHMST',
                    passlist=['100THSEC', 'SECOND', 'MINUTE', 'HOUR', 'DAY', 'MONTH', 'YEAR'])


def int_test():
    testlib.inputStr('q\r\n', tab_index=plc_tab)
    testlib.inputStr('rtc\r\n', tab_index=plc_tab)
    testlib.inputStr('q\r\n', tab_index=rf_tab)
    testlib.inputStr('rtc\r\n', tab_index=rf_tab)

    testlib.runCase('rtc_int am 2016 12 31 11 59 10 S')

    testlib.inputStr('rtc_int_from_arm 0\r\n', tab_index=plc_tab)
    testlib.inputStr('rtc_int_for_dsp 24h 2016 7 22 10 20 50 S\r\n')
    testlib.logTest(passlist=['pass'], failstr='fail', tab_index=plc_tab)
    testlib.inputStr('q\r\n')

    testlib.inputStr('rtc_int_from_arm 0\r\n', tab_index=rf_tab)
    testlib.inputStr('rtc_int_for_dsp 24h 2016 7 22 10 20 50 S\r\n')
    testlib.logTest(passlist=['pass'], failstr='fail', tab_index=rf_tab)
    testlib.inputStr('q\r\n')


def rtc_calibrate():
    testlib.MSGPOP = False
    cmd = 'rtc_calibrate 0 trim_mode trim_val'
    testlib.runAllCombo(cmd, valuedict, formatdict, timeout=500)


def main():
    enter_rtc_test_menu()
    testcases = [
        set_get,
        set12_24,
        boundry,
        alarm,
        alarm_mul,
        # int_test,
        # rtc_calibrate,
    ]
    testlib.runCaseList(testcases,
                        logpath=testlib.GetFileNameAndExt(
                            __file__)[0] + '\\LOG\\',
                        filename=testlib.GetFileNameAndExt(__file__)[1])

if __name__ == '__builtin__':
    main()
