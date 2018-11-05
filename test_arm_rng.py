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
#############################################
valuedict = {
    'ev_mode': [0, 1, 2],
    'kat_sel': [0, 1],
    'kat_vec': [0, 1],
    'int_bit': [0, 4]
}
formatdict = {
    'ev_mode': '%d',
    'kat_sel': '%d',
    'kat_vec': '%d',
    'int_bit': '%d',
}


def qualitytest(cmd):
    testlib.inputStr(cmd + '\r\n')
    q = testlib.getStrBetween('diff with pi = ', ' x 10^(-6)', timeout=60)
    if int(q) < 1000:
        if int(q) == 0:
            return False, 'TIMEOUT'
        else:
            return True, 'pass'
    else:
        return False, 'diff whth pi bigger than 10^(-3)'


def enter_qspi_test_menu():
    testlib.enter_menu('dwc_trng')


def trng_kat():
    cmd = 'trng_kat kat_sel kat_vec'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def trng_quality():
    for ev in valuedict['ev_mode']:
        cmd = 'trng_quality %d' % (ev)
        testlib.logTestPop(cmd, qualitytest, cmd)


def trng_int():
    cmd = 'trng_int int_bit'
    testlib.runAllCombo(cmd, valuedict, formatdict)


###############################################


def main():
    testcases = [
        enter_qspi_test_menu,
        trng_quality,
        trng_kat,
        trng_int,
    ]
    testlib.runCaseList(testcases, logpath=testlib.GetFileNameAndExt(
        __file__)[0] + '\\LOG\\',
        filename=testlib.GetFileNameAndExt(__file__)[1])


if __name__ == '__builtin__':
    main()
