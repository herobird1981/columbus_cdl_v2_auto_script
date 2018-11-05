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
###################################################
# connect i2c1 to i2c2 (data & clk)
###################################################
valuedict = {
    'dma': [0, 1],
    'speed': [100000, 400000],
    'addr': ['0x45 7b', '0x123 10b'],
    'length': [1, 6, 1024, 4095],
    'pattern': [0xaa]
}
formatdict = {
    'dma': '%d',
    'speed': '%d',
    'addr': '%s',
    'length': '%d',
    'pattern': '0x%x',
}

####################################################


def i2c2i2c(echo_cmd, transfer_cmd, auto=True, passstr='pass'):
    testlib.enter_menu('i2c1')
    testlib.sleep(200)
    testlib.inputStr(echo_cmd + '\r\n')
    testlib.sleep(500)
    testlib.enter_menu('i2c2')
    testlib.sleep(200)
    if auto:
        testlib.runCase(transfer_cmd, passlist=[passstr], failstr='$$$$$$$$$$')
    else:
        testlib.inputStr(transfer_cmd + '\r\n')
    testlib.sleep(500)

###########################################################


def basic_rw():
    i2c2i2c('i2c_slave 0x45 7b', 'i2c_master 0 100000 0x45 7b 1 0x55')
    i2c2i2c('i2c_slave 0x45 7b', 'i2c_master 0 100000 0x45 7b 1024 0x55')


def speed():
    i2c2i2c('i2c_slave 0x45 7b', 'i2c_master 0 100000 0x45 7b 512 0x55')
    i2c2i2c('i2c_slave 0x45 7b', 'i2c_master 0 400000 0x45 7b 512 0x55')


def bits():
    i2c2i2c('i2c_slave 0x123 10b', 'i2c_master 0 100000 0x123 10b 1 0x55')


def dma():
    i2c2i2c('i2c_slave 0x45 7b', 'i2c_master 1 100000 0x45 7b 512 0x55')


def interrupt():
    i2c2i2c('i2c_slave 0x45 7b', 'i2c_int_master 0x45 7b', auto=False)
    i2c2i2c('i2c_int_slave 0x45 7b', 'i2c_master2 0x45 7b')

def real():
    testlib.inputStr('q\r\n')
    testlib.inputStr('i2c0\r\n')
    testlib.runCase('i2c_real 0 100000 256 0x55')
    testlib.runCase('i2c_real 1 100000 256 0x55')


def different_addr():
    i2c2i2c('i2c_slave 100000 0x45 7b',
            'i2c_master 0 100000 0x55 7b 512 0x55', passstr='fail')


def robust():
    i2c2i2c('i2c_slave 0x45 7b', 'i2c_robust 0 100000 0x45 7b 0xaa', False)
    testlib.sleep(10000)
    testlib.runCase('q', passlist=['failed 0'], failstr='$$$$$$')

    i2c2i2c('i2c_slave 0x123 10b', 'i2c_robust 1 100000 0x123 10b 0xaa', False)
    testlib.sleep(10000)
    testlib.runCase('q', passlist=['failed 0'], failstr='$$$$$$')


def i2c_rw_all():
    para_format = 'dma speed addr length'
    paras = testlib.combine(para_format, valuedict, formatdict, onlypara=True)
    for para in paras:
        para_l = para.split()
        cmd_slave = 'i2c_slave %s %s' % (para_l[2], para_l[3])
        cmd_master = 'i2c_master %s' % (para)
        i2c2i2c(cmd_slave, cmd_master)


def robust_all():
    for addr in valuedict['addr']:
        cmd_slave = 'i2c_slave ' + addr
        for clk in valuedict['speed']:
            for dma_mode in valuedict['dma']:
                cmd_master = 'i2c_robust %d %d %s' % (dma_mode, clk, addr)
                i2c2i2c(cmd_slave, cmd_master, auto=False)
                testlib.sleep(10000)
                testlib.runCase('q', passlist=['failed 0'], failstr='$$$$$$')


def real_all():
    testlib.enter_menu('i2c0')
    cmd = 'i2c_real dma speed length'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def main():
    testcases = [
        basic_rw,
        speed,
        bits,
        dma,
        interrupt,
        # real,
        different_addr,
        robust,
        i2c_rw_all,
        robust_all,
        # real_all,
    ]

    testlib.runCaseList(testcases,
                        logpath=testlib.GetFileNameAndExt(
                            __file__)[0] + '\\LOG\\',
                        filename=testlib.GetFileNameAndExt(__file__)[1])
if __name__ == '__builtin__':
    main()

