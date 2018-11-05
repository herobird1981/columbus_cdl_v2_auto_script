import sys
sys.path.append('.')
import testlib
reload(testlib)
testlib.init()
# testlib.MSGPOP = False
if __name__ == '__builtin__':
    testlib.crt = crt
    sys.dont_write_bytecode = True

###################################################


def adc_dma():
    cmd = 'adc_dma'
    testlib.runCase2(cmd, passlist=[
                     'please judge pass or fail'], faillist=['$$$$$$$'])


def adc_int():
    cmd = 'adc_int'
    testlib.runCase2(cmd)


def init():
    testlib.enter_menu('addac')


def dac_pio():
    cmd = 'dac_pio'
    testlib.runCase2(cmd, passlist=[
                     'please judge pass or fail'], faillist=['$$$$$$$'])
    testlib.sleep(2000)


def dac_dma():
    cmd = 'dac_pio'
    testlib.runCase2(cmd, passlist=[
                     'please judge pass or fail'], faillist=['$$$$$$$'])


def dac_int():
    cmd = 'dac_int'
    testlib.runCase2(cmd)


###############################################


def main():
    init()
    testcases = [
        adc_dma,
        adc_int,
        dac_pio,
        dac_dma,
        dac_int,
    ]
    testlib.runCaseList(testcases,
                        logpath=testlib.GetFileNameAndExt(
                            __file__)[0] + '\\LOG\\',
                        filename=testlib.GetFileNameAndExt(__file__)[1])

if __name__ == '__builtin__':
    main()
