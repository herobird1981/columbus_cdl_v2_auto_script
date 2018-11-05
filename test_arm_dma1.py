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
valuedict = {
    'src_addr'  : [0x10000000, 0x41000000, 0xC2600000],
    'dst_addr'  : [0x10008000, 0x42000000, 0xC2604000],
    # 'ch'        : [0, 1, 2, 3, 4, 5, 6, 7],
    'ch'        : [0, 6],
    'trans_len' : [2048],
    'src_dst'   : [0, 1],
    'bus_width' : [0, 1, 2],
    # 'burst_size': [0, 1, 2, 3, 4, 5, 6, 7],
    'burst_size': [1, 4],
    'addr_update': [0, 1, 2],
    'display'   : [0],
}

formatdict = {
    'src_addr'	: '0x%x',
    'dst_addr'	: '0x%x',
    'ch'		: '%d',
    'trans_len'	: '%d',
    'src_dst'	: '%d',
    'bus_width'	: '%d',
    'burst_size'	: '%d',
    'addr_update'	: '%d',
    'display'	: '%d',
}
###################################################


def enter_dma1_test_menu():
    testlib.enter_menu('dmac1')


def m2m_transfer():
    cmd = 'dma_m2m ch src_addr dst_addr trans_len'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def m2m_cfg():
    cmd = 'dma_cfg ch trans_len src_dst bus_width burst_size addr_update'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def m2m_cfg2():
    cmd = 'dma_cfg2 ch trans_len src_addr bus_width burst_size addr_update dst_addr bus_width burst_size addr_update display'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def m2m_ch():
    for i in range(8):
        cmd = 'dma_m2m %d 0x41000000 0x42000000 2048' % i
        testlib.runCase(cmd)


def dma_int():
    cmd1 = 'dma_int 0'
    cmd2 = 'dma_int 0 1'
    cmd3 = 'dma_int 0 1 2 3'
    cmd4 = 'dma_int 0 1 2 3 4 5'
    cmd5 = 'dma_int 0 1 2 3 4 5 6'
    cmd6 = 'dma_int 0 1 2 3 4 5 6 7'
    testlib.runCase(cmd1)
    testlib.runCase(cmd2)
    testlib.runCase(cmd3)
    testlib.runCase(cmd4)
    testlib.runCase(cmd5)
    testlib.runCase(cmd6)


def multi_channel():
    cmd1 = 'dma_mc src_addr dst_addr ch ch'
    cmd2 = 'dma_mc 0x10000000 0x40000000 0 1 2 3'
    cmd3 = 'dma_mc 0x10000000 0x40000000 0 1 2 3 4 5 6 7'
    cmdlist = testlib.combine(cmd1, valuedict, formatdict)
    for i in cmdlist:
        para = i.split()
        if para[3] != para[4]:
            testlib.runCase(i)
    testlib.runCase(cmd2)
    testlib.runCase(cmd3)


def multi_block():
    cmd = 'dma_mb ch src_addr dst_addr trans_len'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def robust():
    testlib.inputStr('dma_m2m_robust\r\n')
    testlib.sleep(60000)
    testlib.runCase2('q', passlist=['dma_m2m_robust: test pass'], faillist=['dma_m2m_robust: test fail'])

##########################################################################


def main():
    testcases = [
        enter_dma1_test_menu,
        m2m_transfer,
        m2m_cfg,
        m2m_cfg2,
        m2m_ch,
        dma_int,
        multi_channel,
        multi_block,
        robust,
    ]
    testlib.runCaseList(testcases,
                        logpath=testlib.GetFileNameAndExt(__file__)[0] + '\\LOG\\',
                        filename=testlib.GetFileNameAndExt(__file__)[1])


if __name__ == '__builtin__':
    main()
