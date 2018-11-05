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


def enter_wdt_test_menu():
    testlib.enter_menu('watch dog timer')


def wdt_start_stop():
    cmd = 'wdt_start_stop'
    testlib.runCase(cmd)


def wdt_reload():
    vals = [0x10000000, 0x20000000]
    for i in vals:
        cmd_start = 'wdt_reload start 0x%x' % (i)
        testlib.runCase(cmd_start)
        cmd_restart = 'wdt_reload restart 0x%x' % (i)
        testlib.runCase(cmd_restart)


def wdt_fly():
    cmd = 'wdt_fly'
    testlib.runCase(cmd)


def wdt_int():
    cmd = 'wdt_int'
    testlib.runCase(cmd)
##########################################################################


def main():
    testcases = [
        enter_wdt_test_menu,
        wdt_start_stop,
        wdt_reload,
        wdt_fly,
        wdt_int,
    ]
    testlib.runCaseList(testcases,
                        logpath=testlib.GetFileNameAndExt(
                            __file__)[0] + '\\LOG\\',
                        filename=testlib.GetFileNameAndExt(__file__)[1])

if __name__ == '__builtin__':
    main()

