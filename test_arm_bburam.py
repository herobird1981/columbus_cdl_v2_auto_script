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
tmo = 30
bram_size = 1024
bram_test_step = 16


def enter_bram_test_menu():
    testlib.enter_menu('bburam')


def bram_write():
    for i in range(0, bram_size, bram_test_step):
        cmd = 'bram_write_buf %d %d 0x%x' % (i, bram_test_step, i)
        testlib.runCase(cmd, passlist=['cmd:>'])


def bram_read():
    passlog = ['BBU RAM Read Result as below:']
    read_size = bram_size
    bram_content = ''
    for i in range(0, read_size, bram_test_step):
        for j in range(0, bram_test_step):
            bram_content += '%x  ' % (i & 0xff)
        bram_content += '\r\n'
    passlog += ['Total %d bytes displayed' % read_size]
    cmd = 'bram_read_buf 0 %d' % read_size
    testlib.runCase(cmd, passlist=passlog)


def bram_data_comp():
    cmp_size = bram_size
    cmd = 'bram_write_buf 0 %d 0x55\r\n' % cmp_size
    testlib.inputStr(cmd)
    cmd = 'bram_data_comp %d 0x55' % cmp_size
    testlib.runCase(cmd, passlist=['test pass'])


##########################################################################
def main():
    enter_bram_test_menu()
    testcases = [
        bram_write,
        bram_read,
        bram_data_comp,
    ]
    testlib.runCaseList(testcases,
                        logpath=testlib.GetFileNameAndExt(
                            __file__)[0] + '\\LOG\\',
                        filename=testlib.GetFileNameAndExt(__file__)[1])

if __name__ == '__builtin__':
    main()
