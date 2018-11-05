import sys
sys.path.append('.')
import testlib
reload(testlib)
testlib.init()
if __name__ == '__builtin__':
    testlib.crt = crt
    sys.dont_write_bytecode = True


def reset():
    for i in range(19):
        if i in [0, 4, 5, 14, 15, 16, 18]:
            continue
        cmd = 'reset %d' % (i)
        testlib.runCase(cmd)


def clock_gating():
    for i in range(17):
        if i in [0, 4, 5, 6, 7, 12, 14, 15, 16]:
            continue
        cmd = 'cg %d' % (i)
        testlib.runCase(cmd)


def enter_sys_test_menu():
    testlib.enter_menu('sys')


def main():
    enter_sys_test_menu()
    testcases = [
        reset,
        clock_gating,
    ]
    testlib.runCaseList(testcases,
                        logpath=testlib.GetFileNameAndExt(
                            __file__)[0] + '\\LOG\\',
                        filename=testlib.GetFileNameAndExt(__file__)[1])

if __name__ == '__builtin__':
    main()
