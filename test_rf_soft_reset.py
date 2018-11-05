# $language = "Python"
# $interface = "1.0"
'''Precondition: firstly download CDL bin to QSPI nor flash'''
import sys
sys.path.append('.')
import testlib
testlib.getCrt(crt)
###################################################
valuedict = {
			}
formatdict = {
		 	}
###################################################
def enter_sys_test_menu():
    testlib.enter_menu('sys') 

def do_rf_soft_reset():
	enter_sys_test_menu()
	cmd1 = 'reset 18\n'
	testlib.inputStr(cmd1)
	testlib.sleep(5000)

for i in range(10000):
	do_rf_soft_reset()