# $language = "Python"
# $interface = "1.0"
from importlib import import_module
import sys, string
sys.path.append('.')
sys.dont_write_bytecode = True

loop_count_raw = crt.Dialog.Prompt("Enter a loop count for auto testing:", "Welcome to Columbus Auto Testing", "", False)

modules = [
    'test_rf_aes',
    'test_rf_dma',
    'test_rf_crc',
    #'test_rf_ecc',
    #'test_rf_ipc',
    'test_rf_qspi',
    #'test_rf_rtc',
    'test_rf_sha',
    #'test_rf_rfspi_loopback',
    'test_rf_spi_loopback_int',
    #'test_rf_spi',
    'test_rf_timer',
    'test_rf_wdt',
    'test_rf_saradc',
    #'test_rf_addac',
    'test_rf_prcm_reset',
    # 'test_rf_pll',
]

loop_count_int = string.atoi(loop_count_raw)

for i in range(loop_count_int):
    for module in modules:
        mo = import_module(module)
        reload(mo)
        mo.crt = crt
        mo.testlib.crt = crt
        mo.testlib.MSGPOP = False
        mo.testlib.log_file = 'result/rf_fail_%d.csv' % (i)
        mo.main()
