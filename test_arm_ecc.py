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

}
formatdict = {

}
###################################################
tmo = 600


def enter_ecc_test_menu():
    testlib.enter_menu('ecc')


def ecc_test_basic():
    cmd = 'ecc_test_basic'
    testlib.runCase(cmd, timeout=tmo)


def ecc_test_sign_verify():
    cmd = 'ecc_test_sign_verify'
    testlib.runCase(cmd, timeout=tmo)


def ecc_test_shamir():
    cmd = 'ecc_test_shamir'
    testlib.runCase(cmd, timeout=tmo)


def main():
    enter_ecc_test_menu()
    testcases = [ecc_test_basic,
                 ecc_test_sign_verify,
                 ecc_test_shamir,
                 ]
    testlib.runCaseList(testcases,
                        logpath=testlib.GetFileNameAndExt(__file__)[0] + '\\LOG\\',
                        filename=testlib.GetFileNameAndExt(__file__)[1])

if __name__ == '__builtin__':
    main()

