# $language = "Python"
# $interface = "1.0"
from importlib import import_module
import sys, string
sys.path.append('.')
sys.dont_write_bytecode = True

loop_count_raw = crt.Dialog.Prompt("Enter a loop count for auto testing:", "Welcome to Columbus Auto Testing", "", False)

modules = [
    'test_plc_aes',
    'test_plc_dma',
    #'test_plc_ecc',
    'test_plc_crc',
    #'test_plc_ipc',
    'test_plc_qspi',
    #'test_plc_rtc',
    'test_plc_sha',
    'test_plc_spi_loopback_int',
    #'test_plc_spi',
    'test_plc_timer',
    'test_plc_wdt',
    'test_plc_saradc',
    #'test_plc_addac',
    'test_plc_prcm_reset',
    # 'test_plc_pll',
]

loop_count_int = string.atoi(loop_count_raw)

for i in range(loop_count_int):
    for module in modules:
        mo = import_module(module)
        reload(mo)
        mo.crt = crt
        mo.testlib.crt = crt
        mo.testlib.MSGPOP = False
        mo.testlib.log_file = 'result/plc_fail_%d.csv' % (i)
        mo.main()
