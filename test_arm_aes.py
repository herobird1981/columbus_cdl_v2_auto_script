'''######################################################
# set OTP before test
# '''
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
valuedict = {
    'mode'		: [0, 1, 2],
    'keylen'	: [128, 256],
    'keymode'	: [0, 1, 2],
    'testlen'	: [0, 1024, 2048],
    'segments_len': [0, 1024, 2048],
    'noncelen'	: [7, 10, 13],
    'headerlen'	: [0, 1024, 8096],
    'maclen'	: [4, 8, 12, 16],
    'ivlen'		: [12],
    'example_no': [0, 1, 2, 3, 4, 5, 6, 7],
    'segments'	: [1, 2, 10],
}

formatdict = {
    'mode'		: '%d',
    'keylen'	: '%d',
    'keymode'	: '%d',
    'testlen'	: '%d',
    'segments_len'	: '%d',
    'noncelen'	: '%d',
    'headerlen'	: '%d',
    'maclen'	: '%d',
    'ivlen'		: '%d',
    'example_no': '%d',
    'segments'	: '%d',
}
###################################################
tmo = 200


def aes_report_case():
    cases = [
        'aes_ecb 0 128 0 0',
        'aes_ecb 0 128 0 1024',
        'aes_ecb 0 256 0 1024',
        'aes_ecb_multi 0 128 0 128 10',
        'aes_ecb_multi 0 256 0 128 10',
        'aes_cbc 0 128 0 1024',
        'aes_cbc 0 256 0 1024',
        'aes_cbc_multi 0 256 0 128 10',
        # 'aes_ctr 0 128 0 1024',
        # 'aes_ctr 0 256 0 1024',
        # 'aes_ctr_multi 0 256 0 128 10',
        'aes_ccm 0 128 0 7 32 8 1024',
        'aes_ccm 0 256 0 7 32 8 1024',
        'aes_ccm 0 256 0 10 512 6 1024',
        'aes_ccm_multi 0 128 0 7 32 8 128 10',
        'aes_ccm_star 0 0',
        'aes_ccm_star 1 1',
        'aes_ccm_star 2 1',
        'aes_ccm_star 3 2',
        'aes_ccm_star 4 1',
        'aes_ccm_star 5 2',
        'aes_ccm_star 6 1',
        'aes_ccm_star 7 0',
        'aes_gcm 0 128 0 12 128 12 1024',
        'aes_gcm 0 256 0 12 128 12 1024',
        'aes_gcm 0 256 0 12 512 14 1024',
        'aes_gcm_multi 0 128 0 12 128 12 128 10',
        'aes_cmac 0 128 0 4 1024',
        'aes_cmac 0 256 0 4 1024',
        'aes_cmac 0 256 0 16 1024',
        'aes_cmac_multi 0 128 0 4 128 10',
        'aes_ecb 0 256 1 1024',
        'aes_ecb 0 256 2 1024',
        'aes_cbc 0 256 1 1024',
        'aes_cbc 0 256 2 1024',
        # 'aes_ctr 0 256 1 1024',
        # 'aes_ctr 0 256 2 1024',
        'aes_ccm 0 256 1 7 32 8 1024',
        'aes_ccm 0 256 2 7 32 8 1024',
        'aes_gcm 0 256 1 12 128 13 1024',
        'aes_gcm 0 256 2 12 128 12 1024',
        'aes_cmac 0 256 1 4 1024',
        'aes_cmac 0 256 2 4 1024',
        'aes_ccm_multi 0 128 0 10 32 16 1024 100',
        'aes_gcm 0 128 0 12 0 14 1',
        'aes_gcm 0 128 0 12 0 14 0',
        'aes_gcm 0 128 0 12 0 16 1',
        'aes_gcm 0 128 0 12 0 16 0',
        'aes_gcm 0 256 0 12 0 14 1',
        'aes_gcm 0 256 0 12 0 14 0',
        'aes_gcm 0 256 0 12 0 16 1',
        'aes_gcm 0 256 0 12 0 16 0',
        'aes_cmac 0 128 0 16 0',
        'aes_cmac 0 256 0 16 0',
        'aes_cmac 0 256 0 16 13',
        'aes_cmac_multi 1 128 0 14 1024 10',
        'aes_cmac_multi 2 128 0 14 1024 10',
        'aes_cmac_multi 1 128 0 1 1 1',
        'aes_cmac_multi 1 128 0 0 1 1',
        'aes_cmac_multi 1 128 0 0 0 1',
        'aes_cmac_multi 1 128 0 0 0 0',
        'aes_cmac_multi 1 256 0 4 1024 10',
        'aes_cmac_multi 1 256 0 1 1 1',
        'aes_cmac_multi 1 256 0 0 1 1',
        'aes_cmac_multi 1 256 0 0 0 1',
        'aes_cmac_multi 1 256 0 0 0 0',
        'aes_cmac_multi 0 256 0 1 15 2',
    ]
    for i in cases:
        testlib.runCase(i, timeout=tmo)


def enter_aes_test_menu():
    testlib.enter_menu('aes')


def aes_ecb():
    cmd = 'aes_ecb mode keylen keymode testlen'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def aes_cbc():
    cmd = 'aes_cbc mode keylen keymode testlen'
    testlib.runAllCombo(cmd, valuedict, formatdict)


# def aes_ctr():
#     cmd = 'aes_ctr mode keylen keymode testlen'
#     testlib.runAllCombo(cmd, valuedict, formatdict)


def aes_ccm():
    valuedict = {
        'mode': [0, 1, 2],
        'keylen': [128, 256],
        'keymode': [0, 1, 2],
        'testlen': [0, 1024, 2048],
        'noncelen': [7, 10, 13],
        'headerlen': [0, 1024, 8096],
        'maclen': [4, 6, 8, 10, 12, 14, 16],
        'ivlen': [12],
    }
    cmd = 'aes_ccm mode keylen keymode noncelen headerlen maclen testlen'
    testlib.runAllCombo(cmd, valuedict, formatdict, timeout=tmo)


def aes_ccm_fixdata():
    cmd = 'aes_ccm_fixdata'
    testlib.runCase(cmd)


def aes_gcm():
    valuedict = {
        'mode': [0,1, 2],
        'keylen': [128, 256],
        'keymode': [0, 1, 2],
        'testlen': [0, 1024, 2048],
        'headerlen': [0, 10, 128],
        'maclen': [12,13,14,15,16],
        'ivlen': [12],
    }
    cmd = 'aes_gcm mode keylen keymode ivlen headerlen maclen testlen'
    testlib.runAllCombo(cmd, valuedict, formatdict, timeout=tmo)


def aes_gcm_fixdata():
    cmd = 'aes_gcm_fixdata'
    testlib.runCase(cmd)


def aes_cmac():
    valuedict = {
        'mode': [0, 1, 2],
        'keylen': [128, 256],
        'keymode': [0, 1, 2],
        'testlen': [0, 13, 1024, 2048],
        'maclen': [0,1,2,3,4, 6, 8, 10, 13, 14, 16],
    }
    cmd = 'aes_cmac mode keylen keymode maclen testlen'
    testlib.runAllCombo(cmd, valuedict, formatdict, timeout=tmo)


def aes_ccm_star():
    cmd = 'aes_ccm_star example_no keymode'
    testlib.runAllCombo(cmd, valuedict, formatdict, timeout=tmo)


def aes_ecb_multi():
    cmd = 'aes_ecb_multi mode keylen keymode segments_len segments'
    testlib.runAllCombo(cmd, valuedict, formatdict)


def aes_cbc_multi():
    cmd = 'aes_cbc_multi mode keylen keymode segments_len segments'
    testlib.runAllCombo(cmd, valuedict, formatdict)


# def aes_ctr_multi():
#     cmd = 'aes_ctr_multi mode keylen keymode segments_len segments'
#     testlib.runAllCombo(cmd, valuedict, formatdict)


def aes_ccm_multi():
    valuedict = {
        'mode': [0,1, 2],
        'keylen': [128, 256],
        'keymode': [0, 1, 2],
        'segments_len': [0, 1024, 2048],
        'noncelen': [7, 10, 13],
        'headerlen': [0, 10, 128],
        'maclen': [4,6,8,10,12,14,16],
        'segments': [1, 2, 10],
    }
    cmd = 'aes_ccm_multi mode keylen keymode noncelen headerlen maclen segments_len segments'
    testlib.runAllCombo(cmd, valuedict, formatdict, timeout=tmo)


def aes_gcm_multi():
    valuedict = {
        'mode': [0,1, 2],
        'keylen': [128, 256],
        'keymode': [0, 1, 2],
        'segments_len': [0, 1024, 2048],
        'headerlen': [0, 10, 128],
        'maclen': [12,13,14,15,16],
        'ivlen': [12],
        'segments': [1, 2, 10],
    }
    cmd = 'aes_gcm_multi mode keylen keymode ivlen headerlen maclen segments_len segments'
    testlib.runAllCombo(cmd, valuedict, formatdict, timeout=tmo)


def aes_cmac_multi():
    cmd = 'aes_cmac_multi mode keylen keymode maclen segments_len segments'
    testlib.runAllCombo(cmd, valuedict, formatdict, timeout=tmo)


def main():
    enter_aes_test_menu()
    testcases = [
        aes_report_case,
        aes_ecb,
        aes_cbc,
        # aes_ctr,
        aes_ccm,
        aes_ccm_fixdata,
        aes_gcm,
        aes_gcm_fixdata,
        aes_cmac,
        aes_ccm_star,
        aes_ecb_multi,
        aes_cbc_multi,
        # aes_ctr_multi,
        aes_ccm_multi,
        aes_gcm_multi,
        aes_cmac_multi,
    ]
    testlib.runCaseList(testcases,
                        logpath=testlib.GetFileNameAndExt(
                            __file__)[0] + '\\LOG\\',
                        filename=testlib.GetFileNameAndExt(__file__)[1])

if __name__ == '__builtin__':
    main()
