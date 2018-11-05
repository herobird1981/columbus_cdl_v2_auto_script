# $language = "Python"
# $interface = "1.0"
import sys
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
            cmd_get = 'ipc_get_msg  0 %d' % (i)
            cmd_set = 'ipc_set_msg 1 %d %d' % (i, j)
            testlib.inputStr(cmd_get + '\r\n', arm_tab)
            testlib.runCase(cmd_set, passlist=[
                            '100 pass, 0 fail'], failstr='$$$$$$$')

            cmd_get = 'ipc_get_msg 0 %d' % (i)
            cmd_set = 'ipc_set_msg 0 %d %d' % (i, j)
            testlib.inputStr(cmd_get + '\r\n', plc_tab)
            testlib.runCase(cmd_set, passlist=[
                            '100 pass, 0 fail'], failstr='$$$$$$$')


def Get_Message():
    for j in testlen:
        for i in range(0, 16):
            cmd_get = 'ipc_get_msg  1 %d' % (i)
            cmd_set = 'ipc_set_msg 0 %d %d' % (i, j)
            testlib.inputStr(cmd_set + '\r\n', arm_tab)
            testlib.runCase(cmd_get, passlist=[
                            '100 pass, 0 fail'], failstr='$$$$$$$')

            cmd_get = 'ipc_get_msg 0 %d' % (i)
            cmd_set = 'ipc_set_msg 0 %d %d' % (i, j)
            testlib.inputStr(cmd_set + '\r\n', plc_tab)
            testlib.runCase(cmd_get, passlist=[
                            '100 pass, 0 fail'], failstr='$$$$$$$')


def Free_Timer():
    run = 'ipc_free_time'
    testlib.runCase('ipc_free_time 0', tab_index=arm_tab)
    testlib.runCase(run, passlist=['test pass'])
    testlib.runCase('ipc_free_time 1', tab_index=arm_tab)
    testlib.runCase(run, passlist=['test pass'])


def Interrpt_Test():
    testlib.inputStr('ipc_int 1\r\n')
    testlib.runCase('ipc_set_msg 0 0 1024', passlist=[
                    '100 pass, 0 fail'], failstr='$$$$$$', tab_index=arm_tab)
    testlib.inputStr('q\r\n')

    testlib.inputStr('ipc_int 0\r\n')
    testlib.runCase('ipc_set_msg 0 0 1024', passlist=[
                    '100 pass, 0 fail'], failstr='$$$$$$', tab_index=plc_tab)
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

