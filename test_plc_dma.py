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


dram_addr1 = 0x3ffe7d20
dram_addr2 = dram_addr1 + 0x1400
share_ram1 = 0x61600000
share_ram2 = share_ram1 + 0x1400
sram_addr1 = 0x64000000
sram_addr2 = sram_addr1 + 0x1400
###################################################
valuedict = {
    'src_addr': [dram_addr1, share_ram1, sram_addr1],
    'dst_addr': [dram_addr2, share_ram2, sram_addr2],
    'ch': [0, 1, 2, 3, 4, 5, 6, 7],
    #'ch': [2, 4],
    # header 32bytes, tail 32bytes, total 16 words
    # 'trans_len': [0x100, 0x1f0],
    'trans_len': [0x1f0],
    'src_dst': [0, 1],
    'bus_width': [0, 1, 2],
    #'burst_size': [0, 1, 2, 3, 4, 5, 6, 7],
    'burst_size': [3, 4],
    'addr_update': [0, 1, 2],
    'display'	: [0],
}

formatdict = {
    'src_addr': '0x%x',
    'dst_addr': '0x%x',
    'ch': '%d',
    'trans_len'	: '0x%x',
    'src_dst': '%d',
    'bus_width': '%d',
    'burst_size': '%d',
    'addr_update': '%d',
    'display': '%d',
}
###################################################


def enter_dma0_test_menu():
    global valuedict
    testlib.enter_menu('dmac0')
    valuedict['src_addr'][0] = int(testlib.getStrBetween(
        'dram: start ', '; size'), 16)
    valuedict['dst_addr'][0] = valuedict['src_addr'][0] + 0x800


def m2m_transfer():
    cmd = 'dma_m2m ch src_addr dst_addr trans_len'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def m2m_cfg():
    cmd = 'dma_cfg ch trans_len src_dst bus_width burst_size addr_update'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def m2m_cfg2():
    cmd = 'dma_cfg2 ch trans_len src_addr bus_width burst_size addr_update dst_addr bus_width burst_size addr_update display'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def dma_int():
    cmd1 = 'dma_int 0'
    cmd2 = 'dma_int 0 1'
    cmd2 = 'dma_int 0 1 2'
    cmd3 = 'dma_int 0 1 2 3'
    cmd4 = 'dma_int 0 1 2 3 4 '
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
    cmd = 'dma_mc src_addr dst_addr ch ch'
    cmdlist = testlib.combine(cmd, valuedict, formatdict)
    for i in cmdlist:
        para = i.split()
        if para[3] != para[4]:
            testlib.runCase(i)
    testlib.runCase('dma_mc 0x%x 0x%x 0 1 2 3 4 5 6 7' %
                    (valuedict['src_addr'][0], valuedict['src_addr'][1]))


def multi_block():
    cmd = 'dma_mb ch src_addr dst_addr trans_len'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def robust():
    testlib.inputStr('dma_m2m_robust\r\n')
    testlib.sleep(60000)
    testlib.runCase2('q', passlist=['dma_m2m_robust: test pass'], faillist=['dma_m2m_robust: test fail'])
##########################################################################


def main():
    enter_dma0_test_menu()
    testcases = [
        m2m_transfer,
        m2m_cfg,
        m2m_cfg2,
        dma_int,
        multi_channel,
        multi_block,
        robust,
    ]
    testlib.runCaseList(testcases,
                        logpath=testlib.GetFileNameAndExt(
                            __file__)[0] + '\\LOG\\',
                        filename=testlib.GetFileNameAndExt(__file__)[1])

if __name__ == '__builtin__':
    main()
