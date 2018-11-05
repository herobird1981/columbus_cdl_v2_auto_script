import sys
sys.path.append('.')
import testlib
reload(testlib)
testlib.init()
if __name__ == '__builtin__':
    testlib.crt = crt
    sys.dont_write_bytecode = True


def pll_output_clock():
    freqm = [240, 180, 120, 90, 60]
    for mh in freqm:
        cmd = 'rf_pll_freq %d' % (mh * 1000 * 1000)
        testlib.runCase(cmd)


def AHB_src_switch():
    srcs = [
        'rf_pll',
    ]
    for src in srcs:
        cmd = 'rf_ahb_src_switch %s' % (src)
        testlib.runCase(cmd)


def bus_APB_divison():
    divs = range(1, 9)
    for div in divs:
        cmd = 'rf_bus_rate_div rf_apb %d' % (div)
        testlib.runCase(cmd)


def enter_pll_test_menu():
    testlib.enter_menu('pll')


def main():
    enter_pll_test_menu()
    testcases = [
        pll_output_clock,
        AHB_src_switch,
        bus_APB_divison,
    ]
    testlib.runCaseList(testcases,
                        logpath=testlib.GetFileNameAndExt(
                            __file__)[0] + '\\LOG\\',
                        filename=testlib.GetFileNameAndExt(__file__)[1])

if __name__ == '__builtin__':
    main()
