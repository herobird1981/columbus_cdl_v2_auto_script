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
    'id': [i for i in range(8)],
}
formatdict = {
    'id'		: '%d',

}
###################################################


def enter_timer_test_menu():
    testlib.enter_menu('timer')


def timer_start_stop():
    cmd = 'timer_start_stop id'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def timer_reload():
    cmd = 'timer_reload id'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def timer_count_mode():
    cmd = 'timer_count_mode id'
    passlog = ['timer_count_mode: test pass']
    testlib.runAllCombo(cmd, valuedict, formatdict, passlog)


def timer_overflow():
    cmd = 'timer_overflow id'
    passlog = ['timer_overflow: test pass']
    testlib.runAllCombo(cmd, valuedict, formatdict, passlog)


def timer_reset():
    cmd = 'timer_reset id'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def timer_int():
    cmd = 'timer_int id 5'
    testlib.runAllCombo(cmd, valuedict, formatdict)
##########################################################################


def main():
    enter_timer_test_menu()
    testcases = [timer_start_stop,
                 timer_reload,
                 timer_count_mode,
                 timer_overflow,
                 timer_reset,
                 timer_int
                 ]
    testlib.runCaseList(testcases,
                        logpath=testlib.GetFileNameAndExt(
                            __file__)[0] + '\\LOG\\',
                        filename=testlib.GetFileNameAndExt(__file__)[1])
if __name__ == '__builtin__':
    main()
