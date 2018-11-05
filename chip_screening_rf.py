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
    'timer_id'		: [i for i in range(8)],

}
formatdict = {
    'timer_id'		: '%d',

}
###################################################
plc_tab = 1
rf_tab = 2
arm_tab = 3


def test_timer():
    cmd1 = 'q\r\n'
    cmd2 = 'timer\r\n'
    testlib.inputStr(cmd1)
    testlib.inputStr(cmd2)
    cmd3 = 'timer_start_stop timer_id'  # test timer start & stop
    testlib.runAllCombo(cmd3, valuedict, formatdict)
    testlib.sleep(500)
    cmd4 = 'timer_int timer_id 2'  # test interrupt for each timer ID.
    testlib.runAllCombo(cmd4, valuedict, formatdict)


def test_wdt():
    testlib.inputStr('q\r\n')
    testlib.inputStr('watch dog timer\r\n')
    testlib.sleep(100)
    cmd3 = 'wdt_int'  # test interrupt for watch dog timer.
    testlib.runCase(cmd3, passlist=['wdt_int: test pass'])


def test_rtc():
    cmd1 = 'q\r\n'
    cmd2 = 'rtc\r\n'
    testlib.inputStr(cmd1, rf_tab)
    testlib.inputStr(cmd2, rf_tab)

    testlib.inputStr(cmd1, arm_tab)
    testlib.inputStr(cmd2, arm_tab)

    arm_cmds = [
        'rtc_int_for_dsp 24h 2016 7 22 10 20 50 10 T',
    ]
    for arm_cmd in arm_cmds:
        testlib.inputStr('rtc_int_from_arm 0\r\n')
        testlib.inputStr('%s\r\n' % (arm_cmd), arm_tab)
        testlib.logTestPop('rtc_int_from_arm 0',
                           testlib.logTest2, ['pass'], ['fail'])
        testlib.inputStr('q\r\n', arm_tab)

    cmd_arm = 'rtc_set_time am 2016 7 22 10 20 50 0'
    cmd_dsp = 'rtc_get_time 0'
    testlib.inputStr(cmd_arm + '\r\n', arm_tab)
    testlib.sleep(100)
    testlib.runCase(
        cmd_dsp, passlist=['rtc time 2016.07.22 10:20:50'])

    cmd_arm = 'rtc_set_time 24h 2016 7 22 10 20 50 0'
    cmd_dsp = 'rtc_get_time 1'
    testlib.inputStr(cmd_arm + '\r\n', arm_tab)
    testlib.sleep(100)
    testlib.runCase(
        cmd_dsp, passlist=['rtc time 2016.07.22 10:20:50'])


def test_dma0():
    cmd1 = 'q\r\n'
    cmd2 = 'dmac0\r\n'
    testlib.inputStr(cmd1)
    testlib.inputStr(cmd2)
    startaddr = int(testlib.getStrBetween(
        'dram: start ', '; size'), 16)
    # test memory to memory for each channel.
    for i in range(random.randint(0, 7),):
        cmd = 'dma_m2m %d 0x%x 0x%x 0x800' % (i, startaddr, startaddr + 0x800)
        testlib.runCase(cmd)
    testlib.sleep(500)
    cmd3 = 'dma_int 0 1 2 3 4 5 6 7'
    testlib.runCase(cmd3)


def test_gpio():
    gpio1 = 'f 2'
    gpio2 = 'f 3'
    cmd1 = 'q\r\n'
    cmd2 = 'gpio\r\n'
    testlib.inputStr(cmd1)
    testlib.inputStr(cmd2)
    testlib.runCase('gpio_output %s 0' % (gpio1), passlist=[
                    'pass or fail'], failstr='$$$$')
    testlib.runCase('gpio_input %s 0' % (gpio2))

    testlib.runCase('gpio_output %s 1' % (gpio1), passlist=[
                    'pass or fail'], failstr='$$$$')
    testlib.runCase('gpio_input %s 1' % (gpio2))


def test_qspi():
    cmd1 = 'q\r\n'
    cmd2 = 'spi0(qspi)\r\n'
    testlib.inputStr(cmd1)
    testlib.inputStr(cmd2)
    # test qspi read & write test.
    cmd3 = 'qspi_mode 0 25000000 0 10 4 4 0xaa'
    testlib.runCase(cmd3)
    testlib.sleep(500)
    cmd4 = 'qspi_int 0 12000000 0'  # test qspi interrupt.
    testlib.runCase(cmd4)


def test_spi():
    testlib.inputStr('q\r\n')
    testlib.inputStr('spi1\r\n')

    cmd = 'spi_loopback 0 12000000 1 0 0 8 16'
    testlib.runCase(cmd)

    cmd3 = 'spi_int tx'
    testlib.runCase(cmd3)


def test_rfspi():
    testlib.inputStr('q\r\n')
    testlib.inputStr('spi2(rfspi)\r\n')

    cmd = 'spi_loopback 0 12000000 1 0 0 8 16'
    testlib.runCase(cmd)


def test_crc():
    cmd1 = 'q\r\n'
    cmd2 = 'crc\r\n'
    testlib.inputStr(cmd1)
    testlib.inputStr(cmd2)
    cmd3 = 'crc16_cal %d'
    cmd4 = 'crc32_cal %d'
    for i in range(10):
        testlib.runCase(cmd3 % (random.randint(0x1, 0x400) * 4),
                        passlist=['CCITT test pass'])
        testlib.runCase(cmd4 % (random.randint(0x1, 0x400) * 4),
                        passlist=['Reflect test pass'])


def test_addac():
    testlib.enter_menu('addac')
    testlib.runCase('adc_int')
    testlib.runCase('dac_int')


def test_ecc():
    cmd1 = 'q\r\n'
    cmd2 = 'ecc\r\n'
    testlib.inputStr(cmd1)
    testlib.inputStr(cmd2)
    cmd3 = 'ecc_test_basic'
    testlib.runCase(cmd3)


def test_aes():
    cmd1 = 'q\r\n'
    cmd2 = 'aes\r\n'
    testlib.inputStr(cmd1)
    testlib.inputStr(cmd2)
    cmd3 = 'aes_ecb 0 256 0 816'
    testlib.runCase(cmd3, ['aes_ecb: test pass'])


def test_sha():
    cmd1 = 'q\r\n'
    cmd2 = 'sha\r\n'
    testlib.inputStr(cmd1)
    testlib.inputStr(cmd2)
    cmd3 = 'sha384 %d'
    cmd4 = 'sha256 %d'
    for i in range(100):
        testlib.runCase(cmd3 % (random.randint(0x1, 0x400) * 4),
                        passlist=['sha384: test pass'])
        testlib.runCase(cmd4 % (random.randint(0x1, 0x400) * 4),
                        passlist=['sha256: test pass'])


def test_ipc():
    testlib.inputStr('q\r\n', plc_tab)
    testlib.inputStr('ipc\r\n', plc_tab)

    testlib.inputStr('q\r\n', arm_tab)
    testlib.inputStr('ipc\r\n', arm_tab)

    testlib.inputStr('q\r\n', rf_tab)
    testlib.inputStr('ipc\r\n', rf_tab)

    run = 'ipc_free_time'
    testlib.runCase('ipc_free_time 0', tab_index=arm_tab)
    testlib.runCase(run, passlist=['test pass'])
    testlib.runCase('ipc_free_time 1', tab_index=arm_tab)
    testlib.runCase(run, passlist=['test pass'])


def test_pontimer():
    testlib.enter_menu('pontimer')
    testlib.runCase('ptimer_count_mode')

##########################################################################


def main():
    testcases = [
        test_timer,
        test_wdt,
        test_rtc,
        test_dma0,
        test_gpio,
        test_qspi,
        test_spi,
        test_crc,
        # test_addac,
        # test_ecc,
        test_aes,
        test_sha,
        test_ipc,
        test_pontimer,
    ]
    testlib.runCaseList(testcases,
                        logpath=testlib.GetFileNameAndExt(
                            __file__)[0] + '\\LOG\\',
                        filename=testlib.GetFileNameAndExt(__file__)[1])
main()
