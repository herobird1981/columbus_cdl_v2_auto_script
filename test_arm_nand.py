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
valuedict = {
    'dma': [1],
    'cs': [0],
    'block_num': [10],
    'ecc_bit': [8],
    'ecc_mode': [0, 1],
    'pattern': [0xaa],
    'read_mode': [1],
    'mode': [0, 1, 2, 3, 4],
    'delay': [1],
    # 'delay': [0, 1, 2, 3],
}
formatdict = {
    'dma': '%d',
    'cs': '%d',
    'block_num': '%d',
    'ecc_bit': '%d',
    'ecc_mode': '%d',
    'pattern': '0x%x',
    'read_mode': '%d',
    'mode': '%d',
    'delay': '%d',
}
###################################################
tmo = 30

Dblk = random.randint(0x21, 0x7ff)


def blk_inc(num=1):
    global Dblk
    if Dblk + num < 0x7f0:
        Dblk = Dblk + num
    else:
        Dblk = 0x21


def enter_nand_test_menu():
    testlib.enter_menu('nandflash')


def nand_probe():
    cmd = 'nand_probe cs mode delay'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def nand_write_read():
    para_combs = testlib.combine(
        'cs mode delay blk ecc_mode', valuedict, formatdict, onlypara=True)
    for i in para_combs:
        i = i.replace('blk', str(Dblk))
        cmd_write = 'nand_write %s 0x55' % (i)
        cmd_read_data = 'nand_read %s 0' % (i)
        cmd_read_oob = 'nand_read %s 1' % (i)
        testlib.runCase(cmd_write)
        testlib.runCase(cmd_read_data)
        testlib.runCase(cmd_read_oob)
        blk_inc()


def nand_erase():
    cmd = 'nand_erase cs mode delay %d' % (Dblk)
    testlib.runAllCombo(cmd, valuedict, formatdict)
    cmd = 'nand_erase_all cs mode delay'
    testlib.runAllCombo(cmd, valuedict, formatdict)
    blk_inc()


def nand_ecc():
    para_combs = testlib.combine(
        'cs mode delay blk ecc_bit', valuedict, formatdict, onlypara=True)
    for i in para_combs:
        i = i.replace('blk', str(Dblk))
        cmd = 'nand_ecc %s' % (i)
        testlib.runCase2(cmd)
        blk_inc()


def nand_int():
    cmd = 'nand_int cs mode delay'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def nand_bbt():
    mode = random.randint(0, 4)
    delay = random.randint(0, 3)
    testlib.runCase('nand_erase_all 0 %d %d' % (mode, delay))
    testlib.runCase('nand_scan_bbt 0 %d %d' % (mode, delay))
    testlib.runCase('nand_mark_bb 0 %d %d %d' % (mode, delay, Dblk), passlist=[
                    'marked blk 0x%x as bad block in bbt' % (Dblk)])
    testlib.runCase('nand_check_bb 0 %d %d %d' % (mode, delay, Dblk),
                    passlist=['blk 0x%x is bad' % (Dblk)])
    testlib.runCase('nand_write_bbt 0 %d %d' % (mode, delay))
    testlib.runCase('nand_read_bbt 0 %d %d' % (mode, delay))
    blk_inc()

##########################################################################
def main():
    testcases = [
        enter_nand_test_menu,
        nand_probe,
        nand_erase,
        nand_write_read,
        nand_ecc,
        nand_int,
        nand_bbt,
    ]
    testlib.runCaseList(testcases,
                        logpath=testlib.GetFileNameAndExt(
                            __file__)[0] + '\\LOG\\',
                        filename=testlib.GetFileNameAndExt(__file__)[1])

if __name__ == '__builtin__':
    main()
