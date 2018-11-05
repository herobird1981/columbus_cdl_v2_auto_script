import sys
from time import localtime
import random
sys.path.append('.')
import testlib
reload(testlib)
testlib.init()
if __name__ == '__builtin__':
    testlib.crt = crt
    sys.dont_write_bytecode = True


plc_tab = 1
rf_tab = 2
arm_tab = 3
epf_tab = 4

PON_num = 3


def setEPF():
    testlib.inputStr('epf\r\n', arm_tab)
    # testlib.runCase2('epf_test 0 1 255 260\r\n', passlist=[
    #     'pwd reg: 0x30000'], faillist=['@@@@@@@'], tab_index=arm_tab)
    testlib.inputStr('epf_test 0 1 255 260\r\n', arm_tab)
    testlib.sleep(100)
    testlib.inputStr('epf\r\n', plc_tab)
    testlib.inputStr('epf_int 0 1 100 210\r\n', plc_tab)
    testlib.sleep(100)
    # testlib.runCase2('epf_int 0 1 100 210\r\n', passlist=[
    #     'pwd reg: 0x30000'], faillist=['@@@@@@@'], tab_index=plc_tab)
    testlib.inputStr('epf\r\n', rf_tab)
    testlib.inputStr('epf_int 0 1 100 200 %d 96000\r\n' % (PON_num), rf_tab)
    # testlib.runCase2('epf_int 0 1 100 200 3 96000\r\n', passlist=[
    #     'pwd reg: 0x30004'], faillist=['@@@@@@@'], tab_index=rf_tab)


def randomPON():
    setEPF()
    testlib.sleep(500)

    testlib.inputStr('gpio_output b 31 0\r\n', epf_tab)
    for i in range(random.randint(0, PON_num)):
        testlib.logTestPop('', testlib.logTest2, [
                           'pon execute end'], ['@@@@@@@'], rf_tab)
    testlib.inputStr('gpio_output b 31 1\r\n', epf_tab)
    testlib.logTestPop('', testlib.logTest2, [
                       'Select the device to test :'], ['@@@@@@@'], rf_tab)

    testlib.sleep(500)


def epf_test():
    testlib.inputStr('q\r\n', plc_tab)
    testlib.inputStr('q\r\n', rf_tab)
    testlib.inputStr('q\r\n', arm_tab)

    testlib.inputStr('q\r\n', epf_tab)
    testlib.inputStr('gpio\r\n', epf_tab)
    testlib.inputStr('gpio_output b 31 1\r\n', epf_tab)

    for i in range(50000):
        randomPON()


def boot_from_arm():
    while True:
        testlib.logTestPop('', testlib.logTest2, [
            'Select the device to test :'], ['@@@@@@@'])
        testlib.inputStr('q\r\n')
        testlib.inputStr('ipc\r\n')
        testlib.inputStr('plcrf_boot_test 0x42000000 0x42100000\r\n')


def gpiod0():
    testlib.inputStr('gpio_output d 0 0\r\n')
    testlib.inputStr('gpio_output d 0 1\r\n')
    testlib.sleep(1000)


def waitforPON(num):
    for i in range(num):
        testlib.logTestPop('', testlib.logTest2, [
                           'pon execute end'], ['@@@@@@@'], rf_tab)


def get_delay_from_input(default_delay):
    return crt.Dialog.Prompt('Input epf delay(ms)',
                             title='Input epf delay(ms)', default=str(default_delay))


def clear_rf_hskp_done():
    testlib.inputStr('clear_rf_hskp_done_in_plc' + '\r\n', plc_tab)


def gpiod0_pull_epf():
    delay = get_delay_from_input(400)
    if not delay:
        return

    cmd_plc = 'epf_int 0 1 100 50'
    cmd_rf = ''
    cmd_arm = ''

    testlib.enter_menu('epf', plc_tab)
    testlib.enter_menu('epf', rf_tab)
    testlib.enter_menu('epf', arm_tab)

    # clear_rf_hskp_done()
    # testlib.sleep(500)

    testlib.inputStr(cmd_plc + '\r\n', plc_tab)
    testlib.inputStr(cmd_rf + '\r\n', rf_tab)
    testlib.inputStr(cmd_arm + '\r\n', arm_tab)
    testlib.sleep(500)

    testlib.inputStr('gpio_output d 0 0\r\n', epf_tab)
    testlib.sleep(int(delay))
    # waitforPON(3)
    testlib.inputStr('gpio_output d 0 1\r\n', epf_tab)


def main():
    testcases = [
        epf_test,
    ]
    testlib.runCaseList(testcases,
                        logpath=testlib.GetFileNameAndExt(
                            __file__)[0] + '\\LOG\\',
                        filename=testlib.GetFileNameAndExt(__file__)[1])


if __name__ == '__builtin__':
    main()
