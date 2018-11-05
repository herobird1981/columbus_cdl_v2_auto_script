import os
from time import strftime
#################################################
#get parameter combination                      #
#################################################

# Replace parameter name with format
vparalist = []


def replacestr(oldstr, newdict):
    oldlist = oldstr.split()
    newstr = ''
    for key in oldlist:
        if key in newdict:
            newstr = newstr + ' ' + newdict[key]
        else:
            newstr = newstr + ' ' + key
    return newstr

# Return a final cmd list with all parameters combination
# cmd               cmd string descriped with  command name and parameter name
# valuedict             paraname:paravalue
# formatdict            paraname:paraformat


def combine(cmd, valuedict, formatdict, onlypara=False):
    cmbinelist = []
    paranamelist = []
    if onlypara:
        paranamelist_raw = cmd.split()
    else:
        paranamelist_raw = cmd.split()[1:]
    for paraname in paranamelist_raw:
        if paraname in valuedict:
            paranamelist.append(paraname)
    cmdformat = replacestr(cmd, formatdict)
    getallpara(valuedict, cmbinelist, cmdformat, paranamelist)
    return cmbinelist

# Get parameter combination
# valuedict         paraname:paravalue
# combinelist       save all parameter combination
# cmdformat         cmd string format
# paranamelist      parameter name list


def getallpara(valuedict, cmbinelist, cmdformat, paranamelist):
    global vparalist
    key = paranamelist[0]
    for i in valuedict[key]:
        vparalist.append(i)
        paranamesub = paranamelist[1:]
        if not paranamesub:
            cmbinelist.append(cmdformat % tuple(vparalist))
            vparalist = vparalist[:-1]
        else:
            getallpara(valuedict, cmbinelist, cmdformat, paranamesub)
    vparalist = vparalist[:-1]
##########################################################################


def GetFileNameAndExt(filename):
    (filepath, tempfilename) = os.path.split(filename)
    (shotname, extension) = os.path.splitext(tempfilename)
    return filepath, shotname, extension

##########################################################################
# Run test
##########################################################################


timeoutdef = 60
crt = None
MSGPOP = True
# if CANCEL set True, inputStr(), sleep() and logTest2()will not work
CANCEL = False
log_file = 'result/tmp.csv'


def init():
    global MSGPOP, CANCEL
    MSGPOP = True
    CANCEL = False


def stringTestInListOrder(log, passlist):
    startIndex = 0
    for passstr in passlist[:-1]:
        findIndex = log.find(passstr, startIndex)
        if findIndex == -1:
            return passstr
        startIndex = findIndex + len(passstr)


def logTest(passlist, failstr, tab_index=0, timeout=timeoutdef):
    faillist = [failstr]
    return logTest2(passlist, faillist, tab_index, timeout)[0]


def logTest2(passlist, faillist, tab_index=0, timeout=timeoutdef):
    if CANCEL:
        return True, 'pass'
    if tab_index:
        tab = crt.GetTab(tab_index)
    else:
        tab = crt
    list_to_wait = passlist[-1:] + faillist
    text = tab.Screen.ReadString(list_to_wait, timeout)
    index = tab.Screen.MatchIndex
    if index in range(2, len(list_to_wait) + 1):
        return False, 'FAIL : ' + list_to_wait[index - 1]
    elif index == 0:
        return False, 'TIMEOUT'
    elif index == 1:
        passstr = stringTestInListOrder(text, passlist)
        if passstr:
            return False, 'MISSING : ' + passstr
        return True, 'PASS'


# def logTestPop(cmd, passlist, faillist, tab_index=0, timeout=timeoutdef):
#     result = logTest2(passlist, faillist, tab_index, timeout)
#     if not result[0]:
#         global crt, MSGPOP, CANCEL
#         if MSGPOP:
#             ok = crt.Dialog.MessageBox(
#                 "%s\n%s\nContinue?\nYes--continue\nNo--ignore all fail\nCancel--Pause script" % (cmd, result[1]), "Fail detected", 32 | 3)
#             if ok == 2:
#                 if crt.Session.Logging:
#                     crt.Session.Log(False)
#                     crt.Session.LogFileName = ''
#                 CANCEL = True
#             elif ok == 7:
#                 MSGPOP = False
#         pass

def log_write(filename, result):
    logpath = GetFileNameAndExt(filename)[0]
    if not os.path.exists(logpath):
        os.mkdir(logpath)
    try:
        fin = open(filename, 'a')
    except Exception:
        fin = open(filename, 'w')
    fin.write(result)
    fin.close()


def logTestPop(cmd, judge, *judgepara):
    result = judge(*judgepara)
    if not result[0]:
        global crt, MSGPOP, CANCEL
        if MSGPOP:
            ok = crt.Dialog.MessageBox(
                "%s\n%s\nContinue?\nYes--continue\nNo--ignore all fail\nCancel--Pause script" % (cmd, result[1]), "Fail detected", 32 | 3)
            if ok == 2:
                if crt.Session.Logging:
                    crt.Session.Log(False)
                    sleep(500)
                    crt.Session.LogFileName = ''
                CANCEL = True
            elif ok == 7:
                MSGPOP = False
        log_write(log_file, ','.join(
            [cmd, result[1], strftime('%Y%m%d-%H%M%S')]) + '\n')


def inputStr(cmd, tab_index=0):
    if CANCEL:
        return True
    if tab_index:
        tab = crt.GetTab(tab_index)
    else:
        tab = crt
    tab.Screen.Send(cmd)


def sleep(tmo):
    if CANCEL:
        return True
    crt.Sleep(tmo)


def reset(cmd, escapetime, passlist=['Columbus CDL test']):
    runCase(cmd, passlist=passlist, timeout=escapetime)
    inputStr('1\r\n')


def runCase(cmd, passlist=['pass'], failstr='fail', tab_index=0, timeout=timeoutdef):
    faillist = [failstr]
    runCase2(cmd, passlist, faillist, tab_index, timeout)


# def runCase2(cmd, passlist=['pass'], faillist=['fail'], tab_index=0, timeout=timeoutdef):
#     inputStr(cmd + '\r\n', tab_index)
#     logTestPop(cmd, passlist, faillist, tab_index, timeout)


def runCase2(cmd, passlist=['pass'], faillist=['fail'], tab_index=0, timeout=timeoutdef):
    inputStr(cmd + '\r\n', tab_index)
    logTestPop(cmd, logTest2, passlist, faillist, tab_index, timeout)


def getStrBetween(start, stop, timeout=1):
    text = crt.Screen.ReadString(stop, timeout)
    pre_index = text.index(start)
    return text[pre_index + len(start):]


def tabStr(tab_index, cmd):
    tab = crt.GetTab(tab_index)
    tab.Screen.Send(cmd)


def enter_menu(mid, tab_index=0):
    cmd1 = 'q\r\n'
    cmd2 = mid + '\r\n'
    if tab_index:
        inputStr(cmd1, tab_index)
        sleep(100)
        inputStr(cmd2, tab_index)
    else:
        inputStr(cmd1)
        sleep(100)
        inputStr(cmd2)


def runCaseList(testcases, logpath=None, filename=None):
    if crt.Session.Logging:
        crt.Session.Log(False)
    if logpath and filename:
        crt.Session.LogFileName = os.path.join(logpath, filename + '_' +
                                               strftime('%Y%m%d-%H%M%S') + '.log')
        # crt.Session.Log(True)
        crt.Session.LogUsingSessionOptions()
        crt.Session.LogFileName = ''
        for tc in testcases:
            tc()
        sleep(500)
        crt.Session.Log(False)
    else:
        for tc in testcases:
            tc()
    crt.Session.LogFileName = ''
#############################################################################
#
########################################################################


def runAll(allcombo, passlist, faillist, timeout):
    for cmd in allcombo:
        runCase2(cmd, passlist=passlist, faillist=faillist, timeout=timeout)
        sleep(100)


def runAllCombo(cmd, valuedict, formatdict, passlist=['pass'], faillist=['fail'], timeout=timeoutdef):
    combo = combine(cmd, valuedict, formatdict)
    runAll(combo, passlist, faillist, timeout)


if __name__ == '__builtin__':
    # allpara = combine(cmd, valuedict, formatdict)
    # print(len(allpara))
    runCase('uart_int 0 115200 n 8 1 0 rx 1 1', passlist=[
            'receive data available int', 'pass'])
