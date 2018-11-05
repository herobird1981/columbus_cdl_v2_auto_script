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
AHB_CLK = 120000000
# AHB_CLK = 48000000
valuedict = {
    'dma'		: [0, 1],
    'speed': [1000000, 5000000, 10000000, 30000000],  # AHB_CLK=120M
    # 'speed': [24000000, 12000000, 1500000],  # AHB_CLK=48M
    'speed_all'		: [int(AHB_CLK / div) for div in range(4, 33, 2)],
    'phase'		: [0, 3],  # nor we got doesn't support phase 1 and 2
    'cs'			: [0],
    'read_bits': [1, 2, 4],
    'write_bits': [1, 4],
    'pattern'		: [0xa5],
}
formatdict = {
    'dma'		: '%d',
    'speed': '%d',
    'speed_all'		: '%d',
    'phase'		: '%d',
    'cs'		: '%d',
    'read_bits'	: '%d',
    'write_bits'	: '%d',
    'pattern'	: '0x%x',
}
###################################################
tmo = 200
Dblk = 0


def blk_inc():
    global Dblk
    if Dblk < 15:
        Dblk = Dblk + 1
    else:
        Dblk = 0


def enter_qspi_test_menu():
    testlib.enter_menu('spi0(qspi)')


def qspi_probe():
    cmd = 'qspi_probe cs speed_all phase'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def qspi_erase():
    cmd = 'qspi_blk_erase 0 10000000 0 %d' % (Dblk)
    testlib.runCase(cmd)
    cmd = 'qspi_chip_erase 0 10000000 0'
    testlib.runCase(cmd)
    blk_inc()


def qspi_rwtest():
    cmd_write = 'qspi_write 0 10000000 0 %d 0x55' % (Dblk)
    cmd_read_data = 'qspi_read 0 10000000 0 %d' % (Dblk)
    testlib.runCase(cmd_write)
    testlib.runCase(cmd_read_data)
    blk_inc()


def qspi_direct():
    cmd = 'qspi_direct 0 1000000 0 %d 0x55' % (Dblk)
    testlib.runCase(cmd, failstr='test fail')
    blk_inc()


def qspi_legacy():
    for blk in range(16):
        cmd = 'qspi_legacy 0 10000000 0 %d 0x55' % (blk)
        testlib.runCase(cmd)


def qspi_speed():
    speeds = valuedict['speed_all']
    # blks = range(Dblk, Dblk + len(speeds))
    # m = [(speeds[i], blks[i]) for i in range(len(speeds))]
    # for t in m:
    #     cmd = 'qspi_write 0 %d 0 %d 0x55' % (t[0], t[1])
    #     testlib.runCase(cmd)
    for speed in speeds:
        cmd = 'qspi_write 0 %d 0 %d 0x55' % (speed, Dblk)
        testlib.runCase(cmd)
        blk_inc()


def qspi_bits_mode():
    modes = testlib.combine('write_bits read_bits',
                            valuedict, formatdict, onlypara=True)
    for paras in modes:
        cmd = 'qspi_mode 0 10000000 0 %d %s 0xaa' % (Dblk, paras)
        testlib.runCase(cmd)
        blk_inc()


def qspi_int():
    cmd = 'qspi_int cs speed_all phase'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def main():
    enter_qspi_test_menu()
    testcases = [
        qspi_probe,
        qspi_erase,
        qspi_rwtest,
        qspi_speed,
        qspi_direct,
        qspi_legacy,
        qspi_bits_mode,
        qspi_int,
    ]
    testlib.runCaseList(testcases,
                        logpath=testlib.GetFileNameAndExt(
                            __file__)[0] + '\\LOG\\',
                        filename=testlib.GetFileNameAndExt(__file__)[1])

if __name__ == '__builtin__':
    main()
