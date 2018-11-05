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
    'dma'		: [0, 1],
    # 'speed'     : [25000000],
    'speed'		: [12500000, 25000000, 50000000],
    # 'bus_width' : [8],
    'bus_width'	: [1, 4, 8],
    'lba'			: [10],  # start block offset
    'blk_cnt'		: [10],
}
formatdict = {
    'dma'		: '%d',
    'speed'		: '%d',
    'bus_width'	: '%d',
    'lba'			: '%d',
    'blk_cnt'		: '%d',
}
###################################################
tmo = 60
lba = random.randint(0, 1900000)
cnt = 10


def blk_inc(num):
    global lba
    if lba < 1900000:
        lba = lba + num
    else:
        lba = 0


def enter_mmc0_test_menu():
    testlib.enter_menu('mmc/sdio 0')


def mmc_probe():
    cmd = 'mmc_probe dma speed bus_width'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def mmc_single():
    cmd = 'dma speed bus_width'
    paras = testlib.combine(cmd, valuedict, formatdict, onlypara=True)
    for p in paras:
        testlib.runCase('mmc_single %s %d %d' % (p, lba, cnt))
        blk_inc(1)


def mmc_multi():
    cmd = 'dma speed bus_width'
    paras = testlib.combine(cmd, valuedict, formatdict, onlypara=True)
    for p in paras:
        testlib.runCase('mmc_multi %s %d %d' % (p, lba, cnt))
        blk_inc(256)


def mmc_read():
    cmd = 'mmc_read dma speed bus_width lba blk_cnt'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def mmc_int():
    cmd = 'mmc_int dma speed bus_width'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def robust():
    cmd = 'dma_mode speed bus_width'
    paras = testlib.combine(cmd, valuedict, formatdict, onlypara=True)
    for p in paras:
        testlib.inputStr('mmc_multi_robust %s %d\r\n' % (p, lba))
        testlib.sleep(10000)
        testlib.runCase2('q', passlist=['test terminate', 'failed 0'], faillist=['$$$$$$'])
        blk_inc(256)


def main():
    enter_mmc0_test_menu()
    testcases = [
        mmc_probe,
        mmc_single,
        mmc_multi,
        mmc_read,
        mmc_int,
        robust,
    ]
    testlib.runCaseList(testcases,
                        logpath=testlib.GetFileNameAndExt(
                            __file__)[0] + '\\LOG\\',
                        filename=testlib.GetFileNameAndExt(__file__)[1])

if __name__ == '__builtin__':
    main()

