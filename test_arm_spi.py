# $language = "Python"
# $interface = "1.0"
'''Precondition: Connect SPI1 & SPI2 with each other (4 pins: cs/clock/mosi/miso)'''
'''If your want to test loopback ,connect spi tx to rx'''
import sys
sys.path.append('.')
import testlib
reload(testlib)
testlib.init()
if __name__ == '__builtin__':
    testlib.crt = crt
    sys.dont_write_bytecode = True
# NO LOOPBACK & ROBUST
valuedict = {
    'dma_mode': [0, 1],
    'speed': [1000000, 10000000, 15000000],
    'phase': [0, 1, 2, 3],
    'type': [0, 1],
    'cs': [0],
    'bus_width': [4, 5, 6, 7, 8, 15, 16, 31, 32],
    'length': [4096],
    'pattern': [0x5a],
}
formatdict = {
    'dma_mode': '%d',
    'speed': '%d',
    'phase': '%d',
    'type': '%d',
    'cs': '%d',
    'bus_width': '%d',
    'length': '%d',
    'pattern': '0x%x',
}


def enter_spi1_test_menu():
    testlib.enter_menu('spi1')


def twins(cmd_master, cmd_slave):
    testlib.enter_menu('spi1')
    testlib.sleep(100)
    testlib.runCase(cmd_slave, passlist=[''])
    testlib.sleep(50)
    testlib.enter_menu('spi2')
    testlib.sleep(50)
    testlib.runCase(cmd_master)
    testlib.sleep(50)
    testlib.runCase(cmd_master)
    testlib.sleep(50)
    testlib.runCase(cmd_master)
    testlib.sleep(50)


def spi_robust():
    robust_time = 20 * 1000
    for speed in valuedict['speed']:
        cmd_slave = 'spi_slave 1 %d 1 0 0 8' % (speed)
        cmd_master_list = [
            'spi_robust 0 %d 1 0 0 8' % (speed),
            'spi_robust 1 %d 1 0 0 8' % (speed),
            'spi_full_duplex_robust 0 %d 1 0 0 8' % (speed),
            'spi_full_duplex_robust 1 %d 1 0 0 8' % (speed),
        ]
        testlib.runCase('q', passlist=['Columbus'])
        testlib.sleep(100)
        testlib.runCase('spi1', passlist=[''])
        testlib.runCase(cmd_slave, passlist=[''])
        testlib.sleep(50)
        testlib.runCase('q', passlist=['Columbus'])
        testlib.sleep(50)
        testlib.runCase('spi2', passlist=[''])
        testlib.sleep(50)
        for cmd_master in cmd_master_list:
            testlib.inputStr(cmd_master + '\r\n')
            testlib.sleep(robust_time)
            testlib.runCase('q', passlist=['loop,total failed 0'], failstr='$$$$$$')


def master_slave_all():
    para_format = 'speed type phase cs bus_width'
    paras = testlib.combine(para_format, valuedict, formatdict, onlypara=True)
    para_format2 = '1 dma_mode length'
    para2list = [i.split() for i in testlib.combine(
        para_format2, valuedict, formatdict, onlypara=True)]
    for i in paras:
        for j in para2list:
            cmd_master = 'spi_master %d %s %d' % (int(j[1]), i, int(j[2]))
            cmd_slave = 'spi_slave %d %s' % (int(j[0]), i)
            twins(cmd_master, cmd_slave)


def spi_all_full_duplex():
    para_format = 'speed type phase cs bus_width'
    paras = testlib.combine(para_format, valuedict, formatdict, onlypara=True)
    para_format2 = '1 dma_mode length'
    para2list = [i.split() for i in testlib.combine(
        para_format2, valuedict, formatdict, onlypara=True)]
    for i in paras:
        for j in para2list:
            cmd_full_duplex = 'spi_full_duplex %d %s %d' % (
                int(j[1]), i, int(j[2]))
            cmd_slave = 'spi_slave %d %s' % (int(j[0]), i)
            twins(cmd_full_duplex, cmd_slave)
###############################################


def main():
    testcases = [
        #spi_robust,
        master_slave_all,
        spi_all_full_duplex,
    ]
    testlib.runCaseList(testcases, logpath=testlib.GetFileNameAndExt(
        __file__)[0] + '\\LOG\\',
        filename=testlib.GetFileNameAndExt(__file__)[1])


if __name__ == '__builtin__':
    main()

