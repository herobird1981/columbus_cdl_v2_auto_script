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
# Precondition: need to connect TX&RX pins, connect CTS/RTS pins of UART
# port before testing.
valuedict = {
    'dma': [0, 1],
    'baudrate': [1200, 115200, 460800, 1843200, 3686400],
    # 'baudrate': [300, 1200, 9600, 115200, 460800, 921600, 1843200, 3686400],
    'parity': ['n', 'e', 'o'],
    'data_bits': [5, 6, 7, 8],
    'stop_bits': [1, 2],
    'flow_ctl': [0, 1],
    'length': [10],
    'pattern': [0xaa]
}
formatdict = {
    'dma': '%d',
    'baudrate': '%d',
    'parity': '%c',
    'data_bits': '%d',
    'stop_bits': '%d',
    'flow_ctl': '%d',
    'length': '%d',
    'pattern': '0x%x',
}
###################################################


def enter_uart1_test_menu():
    testlib.enter_menu('uart1')
    testlib.sleep(100)

def enter_uart2_test_menu():
    testlib.enter_menu('uart2')
    testlib.sleep(100)

def enter_uart3_test_menu():
    testlib.enter_menu('uart3')
    testlib.sleep(100)


def uart_internal_loopback():
    cmd = 'uart_loopback dma baudrate parity data_bits stop_bits flow_ctl length pattern'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def uart_external_loopback():
    cmd = 'uart_external_loopback dma baudrate parity data_bits stop_bits flow_ctl length pattern'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def uart_int():
    cmds = [
        'uart_int 0 115200 n 8 1 0 tx',
        'uart_int 0 115200 n 8 1 0 rx 1 0',
        'uart_int 0 115200 n 8 1 0 rx 1 1',
        'uart_int 0 115200 n 8 1 0 rx 16 0',
        'uart_int 0 115200 n 8 1 0 rx 16 15',
        'uart_int 0 115200 n 8 1 0 rx 16 16',
        'uart_int 0 115200 n 8 1 0 rx 32 31',
        'uart_int 0 115200 n 8 1 0 rx 32 32',
        'uart_int 0 115200 n 8 1 0 rx 62 61',
        'uart_int 0 115200 n 8 1 0 rx 62 62',
        'uart_int 1 115200 n 8 1 0 tx',
        'uart_int 1 115200 n 8 1 0 rx 1 0',
        'uart_int 1 115200 n 8 1 0 rx 1 1',
        'uart_int 1 115200 n 8 1 0 rx 16 0',
        'uart_int 1 115200 n 8 1 0 rx 16 15',
        'uart_int 1 115200 n 8 1 0 rx 16 16',
        'uart_int 1 115200 n 8 1 0 rx 32 31',
        'uart_int 1 115200 n 8 1 0 rx 32 32',
        'uart_int 1 115200 n 8 1 0 rx 62 61',
        'uart_int 1 115200 n 8 1 0 rx 62 62',
    ]
    for cmd in cmds:
        paras = cmd.split()
        if paras[-1] == 'tx':
            testlib.runCase(cmd)
        else:
            if paras[-1] == '0':
                testlib.runCase(
                    cmd, passlist=['uart_int: test fail'], failstr='$$$$$$$')
            elif int(paras[-1]) < int(paras[-2]):
                testlib.runCase(cmd, passlist=['character timeout int', 'pass'])
            else:
                testlib.runCase2(cmd, passlist=['receive data available int', 'pass'])


def main():
    testcases = [
        enter_uart3_test_menu,
        uart_internal_loopback,
        uart_external_loopback,
        uart_int,
    ]
    testlib.runCaseList(testcases,
                        logpath=testlib.GetFileNameAndExt(
                            __file__)[0] + '\\LOG\\',
                        filename=testlib.GetFileNameAndExt(__file__)[1])

if __name__ == '__builtin__':
    main()

