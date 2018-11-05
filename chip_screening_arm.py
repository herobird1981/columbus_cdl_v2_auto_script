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
    'timer_id': [i for i in range(8)],

}
formatdict = {
    'timer_id': '%d',

}

arm_tab = 3
plc_tab = 1
rf_tab = 2

Dblk = random.randint(0, 0x7ff)
###################################################


def blk_inc(num=1):
    global Dblk
    if Dblk + num < 0x7f0:
        Dblk = Dblk + num
    else:
        Dblk = 0


def twins(cmd_slave, cmd_master):  # function for spi1&spi2 master/slave test
    testlib.runCase(cmd_slave, passlist=[''])
    testlib.sleep(500)
    testlib.runCase('q', passlist=['Columbus'])
    testlib.sleep(500)
    testlib.runCase('spi2', passlist=[''])
    testlib.sleep(500)
    testlib.runCase(cmd_master)
    testlib.sleep(500)
    testlib.runCase('q', passlist=['Columbus'])
    testlib.sleep(500)
    testlib.runCase('spi1', passlist=[''])


def i2c2i2c(echo_cmd, transfer_cmd, auto=True, passstr='pass'):
    testlib.inputStr('q\r\n')
    testlib.inputStr('i2c1\r\n')
    testlib.inputStr(echo_cmd + '\r\n')
    testlib.sleep(500)
    testlib.inputStr('q\r\n')
    testlib.inputStr('i2c2\r\n')
    if auto:
        testlib.runCase(transfer_cmd, passlist=[passstr], failstr='$$$$$$$$$$')
    else:
        testlib.inputStr(transfer_cmd + '\r\n')
    testlib.sleep(500)


def test_timer():
    testlib.enter_menu('timer')
    cmd1 = 'timer_start_stop timer_id'  # test timer start & stop
    testlib.runAllCombo(cmd1, valuedict, formatdict)
    testlib.sleep(500)
    cmd2 = 'timer_int timer_id 2'  # test interrupt for each timer ID.
    testlib.runAllCombo(cmd2, valuedict, formatdict)


def test_wdt():
    testlib.enter_menu('watch dog timer')
    cmd1 = 'wdt_int'  # test interrupt for watch dog timer.
    testlib.runCase(cmd1)
    testlib.sleep(500)
    cmd4 = 'wdt_start_stop'
    testlib.runCase(cmd4)


def test_rtc():
    testlib.enter_menu('rtc')
    cmd1 = 'rtc_int 24h 2016 12 31 23 59 10 1 S'
    testlib.runCase(cmd1)


def test_dma0():
    testlib.enter_menu('dmac0')
    # test memory to memory for each channel.
    for i in (random.randint(0, 7),):
        cmd1 = 'dma_m2m %d 0x41000000 0x42000000 2048' % i
        testlib.runCase(cmd1)
    testlib.sleep(500)
    cmd2 = 'dma_int 0 1 2 3 4 5 6 7'
    testlib.runCase(cmd2)


def test_dma1():
    testlib.enter_menu('dmac1')
    # test memory to memory for each channel.
    for i in (random.randint(0, 7),):
        cmd1 = 'dma_m2m %d 0x41000000 0x42000000 2048' % i
        testlib.runCase(cmd1)
    testlib.sleep(500)
    cmd2 = 'dma_int 0 1 2 3 4 5 6 7'
    testlib.runCase(cmd2)


def test_dma2():
    testlib.enter_menu('dmac2')
    # test memory to memory for each channel.
    for i in (random.randint(0, 7),):
        cmd1 = 'dma_m2m %d 0x41000000 0x42000000 2048' % i
        testlib.runCase(cmd1)
    testlib.sleep(500)
    cmd2 = 'dma_int 0 1 2 3 4 5 6 7'  # test interrupt for each channel.
    testlib.runCase(cmd2)


def test_gpio():
    banda = 'a 31'
    bandb = 'b 31'
    bandc = 'd 0'
    bandd = 'd 1'
    testlib.enter_menu('gpio')
    testlib.runCase('gpio_output %s 1' % (banda), passlist=[
        'pass or fail'], failstr='$$$$')
    testlib.runCase('gpio_input %s 1' % (bandb))
    testlib.runCase('gpio_output %s 0' % (banda), passlist=[
        'pass or fail'], failstr='$$$$')
    testlib.runCase('gpio_input %s 0' % (bandb))

    testlib.runCase('gpio_output %s 1' % (bandc), passlist=[
        'pass or fail'], failstr='$$$$')
    testlib.runCase('gpio_input %s 1' % (bandd))
    testlib.runCase('gpio_output %s 0' % (bandc), passlist=[
        'pass or fail'], failstr='$$$$')
    testlib.runCase('gpio_input %s 0' % (bandd))


def test_uart1():
    testlib.enter_menu('uart1')
    testlib.sleep(200)
    cmd1 = 'uart_external_loopback 1 115200 n 8 1 0 1024 0x55'
    testlib.runCase(cmd1)
    cmd2 = 'uart_external_loopback 1 3686400 n 8 1 1 1024 0x55'
    testlib.runCase(cmd2)


def test_uart2():
    testlib.enter_menu('uart2')
    testlib.sleep(200)
    cmd1 = 'uart_external_loopback 1 115200 n 8 1 0 1024 0x55'
    testlib.runCase(cmd1)
    cmd2 = 'uart_external_loopback 1 3686400 n 8 1 1 1024 0x55'
    testlib.runCase(cmd2)


def test_uart3():
    testlib.enter_menu('uart3')
    testlib.sleep(200)
    cmd1 = 'uart_external_loopback 1 115200 n 8 1 0 1024 0x55'
    testlib.runCase(cmd1)
    cmd2 = 'uart_external_loopback 1 3686400 n 8 1 1 1024 0x55'
    testlib.runCase(cmd2)


def test_i2c0():  # test i2c EEPROM on EVB.
    testlib.enter_menu('i2c0')
    cmd1 = 'i2c_real 0 100000 256 0xaa'
    testlib.runCase(cmd1)
    cmd2 = 'i2c_real 1 400000 256 0xaa'
    testlib.runCase(cmd2)


def test_i2c():  # test i2c master/slave between i2c1 & i2c2.
    i2c2i2c('i2c_slave 0x45 7b', 'i2c_master 0 100000 0x45 7b 512 0xaa')
    i2c2i2c('i2c_slave 0x45 7b', 'i2c_master 0 400000 0x45 7b 512 0xaa')


def test_qspi():
    testlib.enter_menu('spi0(qspi)')
    # test qspi read & write test.
    cmd1 = 'qspi_write 0 50000000 0 0 0 131072 0xaa'
    testlib.runCase(cmd1)
    cmd2 = 'qspi_mode 0 25000000 0 10 4 4 0xaa'
    testlib.runCase(cmd2)
    testlib.sleep(500)
    cmd2 = 'qspi_int 0 10000000 0 0'  # test qspi interrupt.
    testlib.runCase(cmd2)


def test_spi():
    testlib.enter_menu('spi1')
    cmd_slave = 'spi_slave 0 12000000 1 0 0 8'
    cmd_master = 'spi_master 0 12000000 1 0 0 8 512'
    twins(cmd_slave, cmd_master)
    testlib.sleep(500)
    cmd1 = 'spi_int tx'
    testlib.runCase(cmd1)


def test_sdmmc0():  # test micro SD card
    testlib.enter_menu('mmc/sdio 0')
    # test single block read & write test.
    cmd1 = 'mmc_single 0 25000000 1 0 10 0xaa55a5a5'
    testlib.runCase(cmd1)
    testlib.sleep(500)
    cmd1 = 'mmc_single 0 50000000 4 0 10 0xaa55a5a5'
    testlib.runCase(cmd1)
    cmd1 = 'mmc_single 0 12500000 8 0 10 0xaa55a5a5'
    testlib.runCase(cmd1)
    cmd2 = 'mmc_int 1 10000000 1'
    testlib.runCase(cmd2, failstr='test fail')


def test_sdmmc1():  # test micro SD card
    testlib.enter_menu('mmc/sdio 1')
    # test single block read & write test.
    cmd1 = 'mmc_single 0 25000000 1 0 10 0xaa55a5a5'
    testlib.runCase(cmd1)
    testlib.sleep(500)
    cmd1 = 'mmc_single 0 50000000 4 0 10 0xaa55a5a5'
    testlib.runCase(cmd1)
    cmd1 = 'mmc_single 0 12500000 8 0 10 0xaa55a5a5'
    testlib.runCase(cmd1)
    cmd2 = 'mmc_int 1 10000000 1'
    testlib.runCase(cmd2, failstr='test fail')


def test_nand():
    testlib.enter_menu('nandflash')
    cmd_write = 'nand_write 0 1 1 %d 0 0x55' % (Dblk)
    cmd_read_data = 'nand_read 0 1 1 %d 0 0' % (Dblk)
    cmd_read_oob = 'nand_read 0 1 1 %d 0 1' % (Dblk)
    testlib.runCase(cmd_write)
    testlib.runCase(cmd_read_data)
    testlib.runCase(cmd_read_oob)
    blk_inc()

    cmd_write = 'nand_write 0 1 1 %d 1 0x55' % (Dblk)
    cmd_read_data = 'nand_read 0 1 1 %d 1 0' % (Dblk)
    cmd_read_oob = 'nand_read 0 1 1 %d 1 1' % (Dblk)
    testlib.runCase(cmd_write)
    testlib.runCase(cmd_read_data)
    testlib.runCase(cmd_read_oob)
    blk_inc()


def test_usb0():
    testlib.enter_menu('usb0')
    cmd2 = 'usb_host_mass 0 0 100 10 0xaa'
    testlib.runCase(cmd2)


def test_usb1():
    testlib.enter_menu('usb1')
    cmd2 = 'usb_host_mass 0 0 100 10 0xaa'
    testlib.runCase(cmd2)


def test_otp():
    pass


def test_crc():
    testlib.enter_menu('crc')
    cmd1 = 'crc_robust 0'
    cmd2 = 'crc_robust 1'
    testlib.inputStr(cmd1 + '\r\n')
    testlib.sleep(5000)
    testlib.runCase('q\r\n', passlist=[
                    'test terminate'], failstr='failed 1')
    testlib.sleep(100)
    testlib.inputStr(cmd2 + '\r\n')
    testlib.sleep(5000)
    testlib.runCase('q\r\n', passlist=[
                    'test terminate'], failstr='failed 1')
    testlib.sleep(100)


def test_ecc():
    testlib.enter_menu('ecc')
    cmd1 = 'ecc_test_basic'
    testlib.runCase(cmd1, timeout=200)


def test_aes():
    testlib.enter_menu('aes')
    cmd1 = 'aes_ecb 0 256 0 512'
    testlib.runCase(cmd1)
    testlib.sleep(200)


def test_sha():
    testlib.enter_menu('sha')
    cmd1 = 'sha_robust'
    testlib.runCase(cmd1)
    testlib.sleep(8000)
    testlib.inputStr('q\r\n')


def test_ipc():
    testlib.inputStr('q\r\n', plc_tab)
    testlib.inputStr('ipc\r\n', plc_tab)

    testlib.inputStr('q\r\n', arm_tab)
    testlib.inputStr('ipc\r\n', arm_tab)

    testlib.inputStr('q\r\n', rf_tab)
    testlib.inputStr('ipc\r\n', rf_tab)
    for i in (random.randint(0, 15),):  # IPC flag test (0 ~ 15)
        cmd_get = 'ipc_get_msg 1 %d' % (i)
        cmd_set = 'ipc_set_msg 1 %d 1024' % (i)
        testlib.inputStr(cmd_get + '\r\n', tab_index=plc_tab)
        testlib.runCase(cmd_set, passlist=[
                        '100 pass, 0 fail'], failstr='$$$$$$$')
        cmd_get = 'ipc_get_msg 1 %d' % (i)
        cmd_set = 'ipc_set_msg 0 %d 1024' % (i)
        testlib.tabStr(rf_tab, cmd_get + '\r\n')
        testlib.runCase(cmd_set, passlist=[
                        '100 pass, 0 fail'], failstr='$$$$$$$')
    set_up = 'ipc_free_time 1'
    set_down = 'ipc_free_time 0'
    testlib.runCase(set_up, passlist=['mode:up', 'test pass'])
    testlib.runCase(set_down, passlist=['mode:down', 'test pass'])


def test_tamper():
    testlib.enter_menu('32')
    cmd1 = 'tamp_int 2 2 0'  # detect mode: IRQ_TYPE_EDGE_BOTH (switch6)
    testlib.runCase(cmd1)


def test_rng():
    testlib.enter_menu('dwc_trng')
    testlib.runCase2('trng_kat 1 1')


def test_bburam():
    testlib.enter_menu('bburam')
    cmp_size = 1024
    cmd = 'bram_write 0 %d 0x55\r\n' % cmp_size
    testlib.inputStr(cmd)
    cmd = 'bram_data_comp %d 0x55' % cmp_size
    testlib.runCase(cmd, passlist=['test pass'])


def test_lpddr():
    testlib.enter_menu('ddr')
    cmd = 'ddr_random_value_test 0x8000000'
    testlib.runCase(cmd)


def test_adc():
    testlib.enter_menu('adc')
    testlib.runCase2('adc_cm 0 200000 0xf', passlist=[
                     'cmd:>'], faillist=['$$$$$'])

##########################################################################


def main():
    testcases = [
        test_timer,
        test_wdt,
        test_rtc,
        test_dma0,
        test_dma1,
        test_dma2,
        test_gpio,
        test_uart1,
        test_uart2,
        test_uart3,
        test_i2c0,
        test_i2c,
        test_qspi,
        test_spi,
        test_sdmmc0,
        test_sdmmc1,
        test_nand,
        test_usb0,
        test_usb1,
        test_crc,
        test_ecc,
        test_aes,
        test_sha,
        test_ipc,
        test_rng,
        test_bburam,
        test_lpddr,
        test_adc,
    ]
    testlib.runCaseList(testcases,
                        logpath=testlib.GetFileNameAndExt(
                            __file__)[0] + '\\LOG\\',
                        filename=testlib.GetFileNameAndExt(__file__)[1])
main()
