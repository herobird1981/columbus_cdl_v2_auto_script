# $language = "Python"
# $interface = "1.0"
import sys
import string
sys.path.append('.')
import testlib
reload(testlib)
testlib.init()
if __name__ == '__builtin__':
    testlib.crt = crt
    sys.dont_write_bytecode = True
###################################################
plc_tab = 1
rf_tab = 2
arm_tab = 3
testlen = [1, 31, 64, 1024]


def counterTest(int_list, reverse=False):
    if not reverse:
        for i in range(len(int_list) - 1):
            if int_list[i] > int_list[i + 1]:
                return False
    else:
        for i in range(len(int_list) - 1):
            if int_list[i] < int_list[i + 1]:
                return False
    return True


def init():
    testlib.inputStr('q\r\n', plc_tab)
    testlib.inputStr('ipc\r\n', plc_tab)

    testlib.inputStr('q\r\n', arm_tab)
    testlib.inputStr('ipc\r\n', arm_tab)

    testlib.inputStr('q\r\n', rf_tab)
    testlib.inputStr('ipc\r\n', rf_tab)
##################################################


def Set_Message():
    for j in testlen:
        for i in range(0, 16):
            cmd_get = 'ipc_get_msg  1 %d' % (i)
            cmd_set = 'ipc_set_msg 1 %d %d' % (i, j)
            testlib.inputStr(cmd_get + '\r\n', plc_tab)
            testlib.runCase(cmd_set, passlist=[
                            '100 pass, 0 fail'], failstr='$$$$$$$')

            cmd_get = 'ipc_get_msg 1 %d' % (i)
            cmd_set = 'ipc_set_msg 0 %d %d' % (i, j)
            testlib.inputStr(cmd_get + '\r\n', rf_tab)
            testlib.runCase(cmd_set, passlist=[
                            '100 pass, 0 fail'], failstr='$$$$$$$')


def Get_Message():
    for j in testlen:
        for i in range(0, 16):
            cmd_get = 'ipc_get_msg  1 %d' % (i)
            cmd_set = 'ipc_set_msg 1 %d %d' % (i, j)
            testlib.inputStr(cmd_set + '\r\n', plc_tab)
            testlib.runCase(cmd_get, passlist=[
                            '100 pass, 0 fail'], failstr='$$$$$$$')

            cmd_get = 'ipc_get_msg 0 %d' % (i)
            cmd_set = 'ipc_set_msg 1 %d %d' % (i, j)
            testlib.inputStr(cmd_set + '\r\n', rf_tab)
            testlib.runCase(cmd_get, passlist=[
                            '100 pass, 0 fail'], failstr='$$$$$$$')


def Free_Timer():
    set_up = 'ipc_free_time 1'
    set_down = 'ipc_free_time 0'
    testlib.runCase(set_up, passlist=['mode:up', 'test pass'])
    testlib.runCase(set_down, passlist=['mode:down', 'test pass'])


def Interrpt_Test():
    for flag in range(8):
        testlib.inputStr('ipc_int 1 %d\r\n' % (flag))
        testlib.sleep(100)
        testlib.runCase('ipc_set_msg 1 %d 1024' % (flag), passlist=[
                        '100 pass, 0 fail'], failstr='$$$$$$', tab_index=plc_tab)
        testlib.inputStr('q\r\n')

        testlib.inputStr('ipc_int 0 %d\r\n' % (flag))
        testlib.sleep(100)
        testlib.runCase('ipc_set_msg 1 %d 1024' % (flag), passlist=[
                        '100 pass, 0 fail'], failstr='$$$$$$', tab_index=rf_tab)
        testlib.inputStr('q\r\n')


###############################################
def main():
    init()
    testcases = [
        Set_Message,
        Get_Message,
        Free_Timer,
        Interrpt_Test,
    ]
    testlib.runCaseList(testcases,
                        logpath=testlib.GetFileNameAndExt(__file__)[0] + '\\LOG\\',
                        filename=testlib.GetFileNameAndExt(__file__)[1])


if __name__ == '__builtin__':
    main()
