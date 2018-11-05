# $language = "Python"
# $interface = "1.0"
import sys
import random
sys.path.append('.')
import testlib
reload(testlib)
testlib.init()
if __name__ == '__builtin__':
    testlib.crt = crt
    sys.dont_write_bytecode = True
###################################################
AXI_CLK = 300000000
# AXI_CLK = 50000000
valuedict = {
    'speed'		: [9375000, 10000000, 20000000, 50000000],
    'speed_all': [int(AXI_CLK / div) for div in range(6, 33, 2)],
    'phase'		: [0, 3],
    'cs'		: [0],
    'read_bits'	: [1, 2, 4],
    'write_bits': [1, 4],
    'pattern'	: [0x5a],
    'ecc_mode': [0, 1]
}
formatdict = {
    'speed': '%d',
    'speed_all'		: '%d',
    'phase'		: '%d',
    'cs'		: '%d',
    'read_bits'	: '%d',
    'write_bits': '%d',
    'pattern'	: '0x%x',
    'ecc_mode'	: '%d',
}
###################################################
tmo = 100

Dblk = random.randint(0x21, 0x7ff)


def blk_inc(num=1):
    global Dblk
    if Dblk + num < 0x7f0:
        Dblk = Dblk + num
    else:
        Dblk = 0x21


def enter_qspi_test_menu():
    testlib.enter_menu('spi0(qspi)')


def qspi_probe():
    cmd = 'qspi_probe cs speed_all phase'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def qspi_erase():
    cmd = 'qspi_erase 0 10000000 0 %d' % (Dblk)
    testlib.runCase(cmd)
    cmd = 'qspi_erase_all 0 10000000 0'
    testlib.runCase(cmd)
    blk_inc()


def qspi_rwtest():
    cmd_write = 'qspi_write 0 10000000 0 %d 0 0x55' % (Dblk)
    cmd_read_data = 'qspi_read 0 10000000 0 %d 0 0' % (Dblk)
    cmd_read_oob = 'qspi_read 0 10000000 0 %d 0 1' % (Dblk)
    testlib.runCase(cmd_write)
    testlib.runCase(cmd_read_data)
    testlib.runCase(cmd_read_oob)
    blk_inc()
    cmd_write = 'qspi_write 0 10000000 0 %d 1 0x55' % (Dblk)
    cmd_read_data = 'qspi_read 0 10000000 0 %d 1 0' % (Dblk)
    cmd_read_oob = 'qspi_read 0 10000000 0 %d 1 1' % (Dblk)
    testlib.runCase(cmd_write)
    testlib.runCase(cmd_read_data)
    testlib.runCase(cmd_read_oob)
    blk_inc()


def qspi_bits_mode():
    modes = testlib.combine('write_bits read_bits',
                            valuedict, formatdict, onlypara=True)
    for paras in modes:
        cmd = 'qspi_mode 0 10000000 0 %d %s 0xaa' % (Dblk, paras)
        testlib.runCase(cmd)
        blk_inc()


def qspi_speed():
    speeds = valuedict['speed_all']
    for speed in speeds:
        cmd = 'qspi_write 0 %d 0 %d 1 0x55' % (speed, Dblk)
        testlib.runCase(cmd)
        blk_inc()


def qspi_bbt():
    testlib.runCase('qspi_erase_all 0 10000000 0')
    testlib.runCase('qspi_scan_bbt 0 10000000 0')

    testlib.runCase('qspi_mark_bb 0 10000000 0 %d' % (Dblk), passlist=[
                    'marked blk 0x%x as bad block in bbt' % (Dblk)])

    testlib.runCase('qspi_check_bb 0 10000000 0 %d' % (Dblk),
                    passlist=['blk 0x%x is bad' % (Dblk)])

    testlib.runCase('qspi_write_bbt 0 10000000 0')
    testlib.runCase('qspi_read_bbt 0 10000000 0')

    blk_inc()


def qspi_ecc():
    testlib.runCase('qspi_ecc_test 0 1000000 0 %d %d 0xaa' % (Dblk, Dblk + 2), timeout=120)
    blk_inc(3)


def qspi_int():
    cmd = 'qspi_int cs speed_all phase'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def qspi_all():
    cmd = 'qspi_write cs speed_all phase blk ecc_mode'
    combs = testlib.combine(cmd, valuedict, formatdict)
    for cmd in combs:
        cmd = cmd.replace('blk', '%d' % Dblk)
        testlib.runCase(cmd)
        blk_inc()
##########################################################################


def main():
    enter_qspi_test_menu()
    testcases = [
        qspi_probe,
        qspi_erase,
        qspi_rwtest,
        qspi_bits_mode,
        qspi_speed,
        qspi_bbt,
        qspi_ecc,
        qspi_int,
        qspi_all,
    ]
    testlib.runCaseList(testcases,
                        logpath=testlib.GetFileNameAndExt(
                            __file__)[0] + '\\LOG\\',
                        filename=testlib.GetFileNameAndExt(__file__)[1])

if __name__ == '__builtin__':
    main()
