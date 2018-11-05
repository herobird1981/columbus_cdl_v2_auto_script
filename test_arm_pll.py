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
    'bus': ['axi', 'ahb', 'apb0', 'apb1'],
    'bus_div': [2, 3, 4],
    'peripheral': ['sdmmc', 'nfc'],
    'peripheral_div': [1, 2, 4, 8, 16],
}
formatdict = {
    'bus': '%s',
    'bus_div': '%d',
    'peripheral': '%s',
    'peripheral_div': '%d',

}
###################################################


def pll_config():
    srcs = ['600000000 xtal 0']
    for src in srcs:
        cmd = 'pll_freq_src %s' % (src)
        testlib.runCase(cmd)


def clk_switch():
    testlib.runCase('arm_clk_switch arm_pll')


def bus_div():
    cmd = 'bus_rate_div bus bus_div'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def peripheral_div():
    cmd = 'periph_rate_div peripheral peripheral_div'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def enter_pll_test_menu():
    testlib.enter_menu('pll')


def main():
    enter_pll_test_menu()
    testcases = [
        pll_config,
        clk_switch,
        bus_div,
        peripheral_div,
    ]
    testlib.runCaseList(testcases,
                        logpath=testlib.GetFileNameAndExt(
                            __file__)[0] + '\\LOG\\',
                        filename=testlib.GetFileNameAndExt(__file__)[1])

if __name__ == '__builtin__':
    main()
