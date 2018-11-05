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


def single_mode_multiple_channel():
    cmd1 = 'adc_sm 0 2400000 0xff 0'
    testlib.runCase2(cmd1, passlist=['cmd:>'], faillist=['$$$$$$$'])
    cmd2 = 'adc_sm 0 2400000 0xff 1'
    testlib.inputStr(cmd2 + '\r\n')
    testlib.sleep(10000)
    testlib.runCase2('q', passlist=['please judge pass or fail'], faillist=['$$$$$$$'])


def init():
    testlib.enter_menu('saradc')


def continuous_mode_multiple_channel():
    cmd = 'adc_cm 0 2400000 0xff'
    testlib.runCase2(cmd, passlist=['please judge pass or fail'], faillist=['$$$$$$$'])


def saradc_int():
    for bit in range(10):
        cmd = 'adc_int %d' % (bit)
        testlib.runCase2(cmd)


###############################################


def main():
    init()
    testcases = [
        single_mode_multiple_channel,
        continuous_mode_multiple_channel,
        saradc_int,
    ]
    testlib.runCaseList(testcases,
                        logpath=testlib.GetFileNameAndExt(
                            __file__)[0] + '\\LOG\\',
                        filename=testlib.GetFileNameAndExt(__file__)[1])

if __name__ == '__builtin__':
    main()
