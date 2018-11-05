# $language = "Python"
# $interface = "1.0"
'''Precondition: Connect SPI1 rx to SPI1 tx'''
'''If your want to test loopback ,connect spi tx to rx'''
import sys
sys.path.append('.')
import testlib
reload(testlib)
testlib.init()
if __name__ == '__builtin__':
    testlib.crt = crt
    sys.dont_write_bytecode = True

APB_CLK = 60000000
valuedict = {
    'dma': [0, 1],
    'speed': [APB_CLK / 60, APB_CLK / 6, APB_CLK / 5, APB_CLK / 4],
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


def enter_spi1_test_menu():
    testlib.enter_menu('spi2(rfspi)')


def spi_loopback():
    cmd = 'spi_loopback dma_mode speed type phase cs bus_width length'
    testlib.runAllCombo(cmd, valuedict, formatdict)

###############################################


def main():
    testcases = [
        enter_spi1_test_menu,
        spi_loopback,
    ]
    testlib.runCaseList(testcases, logpath=testlib.GetFileNameAndExt(
        __file__)[0] + '\\LOG\\',
        filename=testlib.GetFileNameAndExt(__file__)[1])


if __name__ == '__builtin__':
    main()

