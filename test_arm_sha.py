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
    'len'	: [4, 64, 100, 128, 1000],
}
formatdict = {
    'len'	: '%d',
}
###################################################


def enter_sha_test_menu():
    testlib.enter_menu('sha')


def sha256():
    cmd = 'sha256 len'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def sha384():
    cmd = 'sha384 len'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def sha_int():
    cmd = 'sha_int'
    testlib.runCase(cmd)


def sha_robust():
    cmd = 'sha_robust'
    testlib.runCase(cmd)
    testlib.sleep(30000)
    testlib.runCase2('q', passlist=['test terminate', 'failed 0', 'cmd:>'], faillist=['$$$$$$$'])


def main():
    enter_sha_test_menu()
    testcases = [sha256,
                 sha384,
                 sha_int,
                 sha_robust
                 ]
    testlib.runCaseList(testcases,
                        logpath=testlib.GetFileNameAndExt(__file__)[0] + '\\LOG\\',
                        filename=testlib.GetFileNameAndExt(__file__)[1])


if __name__ == '__builtin__':
    main()
