# $language = "Python"
# $interface = "1.0"
from importlib import import_module
import sys, string
sys.path.append('.')
sys.dont_write_bytecode = True

loop_count_raw = crt.Dialog.Prompt("Enter a loop count for auto testing:", "Welcome to Columbus Auto Testing", "", False)

modules = [
    'test_arm_aes',
    'test_arm_bburam',
    'test_arm_crc',
    'test_arm_ddr',
    'test_arm_dma0',
    'test_arm_dma1',
    'test_arm_dma2',
    'test_arm_ecc',
    'test_arm_i2c',
    #'test_arm_ipc',
    'test_arm_mmc0',
    'test_arm_mmc1',
    'test_arm_rng',
    'test_arm_nand',
    'test_arm_qspi',
    #'test_arm_rtc',
    'test_arm_usbhost',
    'test_arm_sha',
    'test_arm_spi',
    'test_arm_timer',
    'test_arm_uart1-uart2',
    'test_arm_uart1-uart2_int',
    'test_arm_uart3_loopback_int',
    'test_arm_wdt',
    'test_arm_prcm_reset',
    # 'test_arm_pll',
]

loop_count_int = string.atoi(loop_count_raw)

for i in range(loop_count_int):
    for module in modules:
        mo = import_module(module)
        reload(mo)
        mo.crt = crt
        mo.testlib.crt = crt
        mo.testlib.MSGPOP = False
        mo.testlib.log_file = 'result/arm_fail_%d.csv' % (i)
        mo.main()
