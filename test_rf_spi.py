# $language = "Python"
# $interface = "1.0"
'''Precondition: Connect PLC & RF spi pin to pin before testing started.'''
'''Loop back test need to connect SPI rx to tx'''
import sys
sys.path.append('.')
import testlib
reload(testlib)
testlib.init()
if __name__ == '__builtin__':
    testlib.crt = crt
    sys.dont_write_bytecode = True
###################################################
APB_CLK = 120000000
# APB_CLK = 48000000
valuedict = {
    'dma': [0, 1],
    'speed': [APB_CLK / 60, APB_CLK / 6, APB_CLK / 5, APB_CLK / 4],
    # 'speed': [1000000, 4000000, 15000000, 37500000],
    'type': [0, 1],
    'phase': [0, 1, 2, 3],
    'cs': [0],
    'bus_width': [4, 5, 6, 7, 8, 15, 16, 31, 32],
    # 'bus_width': [i for i in range(4, 33)],
    'length': [1024],
}
formatdict = {
    'dma': '%d',
    'speed': '%d',
    'type': '%d',
    'phase': '%d',
    'cs': '%d',
    'bus_width': '%d',
    'length': '%d',
}
###################################################
plc_tab = 1
rf_tab = 2
arm_tab = 3
master_tab = rf_tab
slave_tab = plc_tab


def master_slave(cmd_master, cmd_slave):
    testlib.runCase(cmd_slave, passlist=[
                    'successfully'], tab_index=slave_tab)
    testlib.runCase(cmd_master, failstr='test fail')
    testlib.runCase(cmd_master, failstr='test fail')
    testlib.runCase(cmd_master, failstr='test fail')


def init():
    testlib.inputStr('q\r\n', master_tab)
    testlib.inputStr('spi1\r\n', master_tab)

    testlib.inputStr('q\r\n', slave_tab)
    testlib.inputStr('spi1\r\n', slave_tab)


def robust():
    robust_time = 20 * 1000
    for speed in valuedict['speed']:
        cmd_slave = 'spi_slave 1 %d 1 0 0 8' % (speed)
        cmd_master_list = [
            # 'spi_robust 0 %d 1 0 0 8' % (speed),
            'spi_robust 1 %d 1 0 0 8' % (speed),
            # 'spi_full_duplex_robust 0 %d 1 0 0 8' % (speed),
            'spi_full_duplex_robust 1 %d 1 0 0 8' % (speed),
        ]
        testlib.runCase(cmd_slave, passlist=['successfully'], tab_index=slave_tab)
        for cmd_master in cmd_master_list:
            testlib.inputStr(cmd_master + '\r\n')
            testlib.sleep(robust_time)
            testlib.runCase('q\r\n', passlist=['loop,total failed 0'], failstr='$$$$$$$$$')


def master_slave_all():
    para_format = 'speed type phase cs bus_width'
    paras = testlib.combine(para_format, valuedict, formatdict, onlypara=True)
    para_format2 = '1 dma length'
    para2list = [i.split() for i in testlib.combine(
        para_format2, valuedict, formatdict, onlypara=True)]
    for i in paras:
        for j in para2list:
            cmd_master = 'spi_master %d %s %d' % (int(j[1]), i, int(j[2]))
            cmd_slave = 'spi_slave %d %s' % (int(j[0]), i)
            master_slave(cmd_master, cmd_slave)


def spi_all_full_duplex():
    para_format = 'speed type phase cs bus_width'
    paras = testlib.combine(para_format, valuedict, formatdict, onlypara=True)
    para_format2 = '1 dma length'
    para2list = [i.split() for i in testlib.combine(
        para_format2, valuedict, formatdict, onlypara=True)]
    for i in paras:
        for j in para2list:
            cmd_full_duplex = 'spi_full_duplex %d %s %d' % (
                int(j[1]), i, int(j[2]))
            cmd_slave = 'spi_slave %d %s' % (int(j[0]), i)
            master_slave(cmd_full_duplex, cmd_slave)
###############################################


def main():
    init()
    testcases = [
        robust,
        master_slave_all,
        spi_all_full_duplex,
    ]
    testlib.runCaseList(testcases,
                        logpath=testlib.GetFileNameAndExt(
                            __file__)[0] + '\\LOG\\',
                        filename=testlib.GetFileNameAndExt(__file__)[1])


if __name__ == '__builtin__':
    main()

