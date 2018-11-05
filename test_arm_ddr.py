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
    'test_size': [0x8000000],
}

formatdict = {
    'test_size': '0x%x',
}
###################################################
tmo = 30000


def enter_ddr_test_menu():
    testlib.enter_menu('ddr')

def ddr_dataline_probe():
    cmd1 = 'ddr_dataline_probe'
    testlib.runCase(cmd1)


def ddr_addrline_probe():
    cmd1 = 'ddr_addrline_probe test_size'
    testlib.runAllCombo(cmd1, valuedict, formatdict, timeout=tmo)


def ddr_random_value_test():
    cmd1 = 'ddr_random_value_test test_size'
    testlib.runAllCombo(cmd1, valuedict, formatdict, timeout=tmo)


def ddr_xor_cmp_test():
    cmd1 = 'ddr_xor_cmp_test test_size'
    testlib.runAllCombo(cmd1, valuedict, formatdict, timeout=tmo)


def ddr_sub_cmp_test():
    cmd1 = 'ddr_sub_cmp_test test_size'
    testlib.runAllCombo(cmd1, valuedict, formatdict, timeout=tmo)


def ddr_mul_cmp_test():
    cmd1 = 'ddr_mul_cmp_test test_size'
    testlib.runAllCombo(cmd1, valuedict, formatdict, timeout=tmo)


def ddr_div_cmp_test():
    cmd1 = 'ddr_div_cmp_test test_size'
    testlib.runAllCombo(cmd1, valuedict, formatdict, timeout=tmo)


def ddr_or_cmp_test():
    cmd1 = 'ddr_or_cmp_test test_size'
    testlib.runAllCombo(cmd1, valuedict, formatdict, timeout=tmo)


def ddr_and_cmp_test():
    cmd1 = 'ddr_and_cmp_test test_size'
    testlib.runAllCombo(cmd1, valuedict, formatdict, timeout=tmo)


def ddr_seqinc_cmp_test():
    cmd1 = 'ddr_seqinc_cmp_test test_size'
    testlib.runAllCombo(cmd1, valuedict, formatdict, timeout=tmo)


def ddr_solidbits_cmp_test():
    cmd1 = 'ddr_solidbits_cmp_test test_size'
    testlib.runAllCombo(cmd1, valuedict, formatdict, timeout=tmo)


def ddr_blockseq_cmp_test():
    cmd1 = 'ddr_blockseq_cmp_test test_size'
    testlib.runAllCombo(cmd1, valuedict, formatdict, timeout=tmo)


def ddr_chkboard_cmp_test():
    cmd1 = 'ddr_chkboard_cmp_test test_size'
    testlib.runAllCombo(cmd1, valuedict, formatdict, timeout=tmo)


def ddr_bitspread_cmp_test():
    cmd1 = 'ddr_bitspread_cmp_test test_size'
    testlib.runAllCombo(cmd1, valuedict, formatdict, timeout=tmo)


def ddr_bitflip_cmp_test():
    cmd1 = 'ddr_bitflip_cmp_test test_size'
    testlib.runAllCombo(cmd1, valuedict, formatdict, timeout=tmo)


def ddr_walkbits0_cmp_test():
    cmd1 = 'ddr_walkbits0_cmp_test test_size'
    testlib.runAllCombo(cmd1, valuedict, formatdict, timeout=tmo)


def ddr_walkbits1_cmp_test():
    cmd1 = 'ddr_walkbits1_cmp_test test_size'
    testlib.runAllCombo(cmd1, valuedict, formatdict, timeout=tmo)


def ddr_wide8bits_cmp_test():
    cmd1 = 'ddr_wide8bits_cmp_test test_size'
    testlib.runAllCombo(cmd1, valuedict, formatdict, timeout=tmo)


def ddr_wide16bits_cmp_test():
    cmd1 = 'ddr_wide16bits_cmp_test test_size'
    testlib.runAllCombo(cmd1, valuedict, formatdict, timeout=tmo)

##########################################################################


def main():
    enter_ddr_test_menu()
    testcases = [ddr_dataline_probe,
                 ddr_addrline_probe,
                 ddr_random_value_test,
                 ddr_xor_cmp_test,
                 ddr_sub_cmp_test,
                 ddr_mul_cmp_test,
                 ddr_div_cmp_test,
                 ddr_or_cmp_test,
                 ddr_and_cmp_test,
                 ddr_seqinc_cmp_test,
                 ddr_solidbits_cmp_test,
                 ddr_blockseq_cmp_test,
                 ddr_chkboard_cmp_test,
                 ddr_bitspread_cmp_test,
                 ddr_bitflip_cmp_test,
                 ddr_walkbits0_cmp_test,
                 ddr_walkbits1_cmp_test,
                 ddr_wide8bits_cmp_test,
                 ddr_wide16bits_cmp_test,
                 ]
    testlib.runCaseList(testcases,
                        logpath=testlib.GetFileNameAndExt(
                            __file__)[0] + '\\LOG\\',
                        filename=testlib.GetFileNameAndExt(__file__)[1])

if __name__ == '__builtin__':
    main()
