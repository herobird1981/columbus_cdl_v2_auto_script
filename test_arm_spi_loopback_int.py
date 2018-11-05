# $language = "Python"
# $interface = "1.0"
'''Precondition: Connect SPI1 rx to SPI1 tx, SPI2 rx to SPI2 tx'''
'''If your want to test loopback ,connect spi tx to rx'''
import sys
sys.path.append('.')
import testlib
reload(testlib)
testlib.init()
if __name__ == '__builtin__':
    testlib.crt = crt
    sys.dont_write_bytecode = True

valuedict = {
    'dma_mode': [0, 1],
    'speed': [1000000, 10000000, 20000000, 30000000, 37500000],
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


def enter_spi2_test_menu():
    testlib.enter_menu('spi2')


def spi_loopback():
    cmd = 'spi_loopback dma_mode speed type phase cs bus_width length'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def spi_int():
    cmds = [
        'spi_int tx',
        'spi_int rx 1 0',
        'spi_int rx 1 1',
        'spi_int rx 1 2',
        'spi_int rx 4 0',
        'spi_int rx 4 3',
        'spi_int rx 4 4',
        'spi_int rx 4 5',
        'spi_int rx 8 0',
        'spi_int rx 8 7',
        'spi_int rx 8 8',
        'spi_int rx 8 9',
        'spi_int rx 16 0',
        'spi_int rx 16 15',
        'spi_int rx 16 16',
        'spi_int rx 16 17',
        'spi_int rx 16 31',
        'spi_int rx 16 32',
        'spi_int rx 16 33',
    ]
    for cmd in cmds:
        paras = cmd.split()
        if paras[-1] == 'tx':
            testlib.runCase(cmd)
        else:
            if int(paras[-1]) < int(paras[-2]):
                testlib.runCase(
                    cmd, passlist=['spi_int: test fail'], failstr='$$$$$$$')
            elif int(paras[-1]) >= int(paras[-2]) and int(paras[-1]) < 32:
                testlib.runCase(cmd, passlist=['status=0xc3'])
            elif int(paras[-1]) == 32:
                testlib.runCase(cmd, passlist=['status=0xe3'])
            else:
                testlib.runCase(cmd, passlist=['status=0xeb'])


###############################################


def main():
    testcases = [
        enter_spi1_test_menu,
        spi_loopback,
        spi_int,
        # enter_spi2_test_menu,
        # spi_loopback,
        # spi_int,
    ]
    testlib.runCaseList(testcases, logpath=testlib.GetFileNameAndExt(
        __file__)[0] + '\\LOG\\',
        filename=testlib.GetFileNameAndExt(__file__)[1])


if __name__ == '__builtin__':
    main()
