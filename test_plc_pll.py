import sys
sys.path.append('.')
import testlib
reload(testlib)
testlib.init()
if __name__ == '__builtin__':
    testlib.crt = crt
    sys.dont_write_bytecode = True



def pll_output_clock():
    freqm = [960, 900, 600, 500, 480, 240, 180, 120, 90, 60]
    for mh in freqm:
        cmd = 'plc_pll_freq %d' % (mh * 1000 * 1000)
        testlib.runCase(cmd)


def AHB_src_switch():
    srcs = [
        'plc_pll_ahb_div',
    ]
    for src in srcs:
        cmd = 'plc_ahb_src_switch %s' % (src)
        testlib.runCase(cmd)


def bus_AHB_divison():
    divs = range(2, 17, 2)  # only even
    # divs = [2, 4, 8, 16]  # only even
    for div in divs:
        cmd = 'plc_bus_rate_div plc_pll_ahb_div %d' % (div)
        testlib.runCase(cmd)


def bus_APB_divison():
    divs = range(1, 9)
    for div in divs:
        cmd = 'plc_bus_rate_div plc_apb %d' % (div)
        testlib.runCase(cmd)


def peripheral_div():
    divs = range(1, 33)
    for div in divs:
        cmd = 'plc_periph_rate_div plc_adc %d' % (div)
        testlib.runCase(cmd)


def enter_pll_test_menu():
    testlib.enter_menu('pll')


def main():
    enter_pll_test_menu()
    testcases = [
        pll_output_clock,
        AHB_src_switch,
        bus_AHB_divison,
        bus_APB_divison,
        peripheral_div,
    ]
    testlib.runCaseList(testcases,
                        logpath=testlib.GetFileNameAndExt(
                            __file__)[0] + '\\LOG\\',
                        filename=testlib.GetFileNameAndExt(__file__)[1])

if __name__ == '__builtin__':
    main()
