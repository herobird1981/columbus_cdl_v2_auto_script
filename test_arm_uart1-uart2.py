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
# Precondition: need to connect UART1 to UART2, tx to rx, rts to cts
# port before testing.
valuedict = {
    # 'dma': [1],
    'dma': [0, 1],
    # 'baudrate': [300, 1200, 9600, 115200, 460800],
    'baudrate': [9600, 115200, 460800],
    # 'highbaud': [3686400],
    'highbaud': [921600, 1843200, 3686400],
    'parity': ['n', 'e', 'o'],
    'data_bits': [5, 6, 7, 8],
    'stop_bits': [1, 2],
    'flow_ctl': [0, 1],
    'length': [32, 1024],
    'pattern': [0xaa]
}
formatdict = {
    'dma': '%d',
    'baudrate': '%d',
    'highbaud': '%d',
    'parity': '%c',
    'data_bits': '%d',
    'stop_bits': '%d',
    'flow_ctl': '%d',
    'length': '%d',
    'pattern': '0x%x',
}
loop = 3
###################################################


def uart2uart(echo_cmd, transfer_cmd):
    testlib.inputStr('q\r\n')
    testlib.inputStr('uart1\r\n')
    testlib.sleep(100)
    testlib.inputStr(echo_cmd + '\r\n')
    testlib.sleep(500)
    testlib.inputStr('q\r\n')
    testlib.inputStr('uart2\r\n')
    testlib.sleep(100)
    testlib.runCase(transfer_cmd, failstr='test fail', timeout=120)
    testlib.sleep(500)


def high_baud():
    para_str = 'dma highbaud parity data_bits stop_bits flow_ctl'
    para_comb_list = testlib.combine(
        para_str, valuedict, formatdict, onlypara=True)
    for i in para_comb_list:
        uart2uart('uart_echo ' + i, 'uart_transfer ' + i + ' %d' % (loop))


def low_baud():
    loop = 1
    para_str = 'dma baudrate parity data_bits stop_bits flow_ctl'
    para_comb_list = testlib.combine(
        para_str, valuedict, formatdict, onlypara=True)
    for i in para_comb_list:
        uart2uart('uart_echo ' + i, 'uart_transfer ' + i + ' %d' % (loop))


def dma_high_baud():
    para_str = '1 highbaud parity data_bits stop_bits flow_ctl length'
    para_comb_list = testlib.combine(
        para_str, valuedict, formatdict, onlypara=True)
    for i in para_comb_list:
        uart2uart('uart_dma_block_echo ' + i,
                  'uart_dma_block ' + i + ' %d' % (loop))
    testlib.inputStr('uart_cleanup\r\n')
    testlib.sleep(100)


def dma_low_baud():
    loop = 1
    para_str = '1 baudrate parity data_bits stop_bits flow_ctl length'
    para_comb_list = testlib.combine(
        para_str, valuedict, formatdict, onlypara=True)
    for i in para_comb_list:
        uart2uart('uart_dma_block_echo ' + i,
                  'uart_dma_block ' + i + ' %d' % (loop))
    testlib.inputStr('uart_cleanup\r\n')
    testlib.sleep(100)


def main():
    testcases = [
        high_baud,
        low_baud,
        dma_high_baud,
        dma_low_baud,
    ]

    testlib.runCaseList(testcases,
                        logpath=testlib.GetFileNameAndExt(
                            __file__)[0] + '\\LOG\\',
                        filename=testlib.GetFileNameAndExt(__file__)[1])


if __name__ == '__builtin__':
    main()

