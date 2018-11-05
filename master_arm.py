import sys
import os
import csv
from time import strftime
sys.dont_write_bytecode=True

global_board_number = crt.Dialog.Prompt("Enter Your Board ID:", "Welcome to Auto Tests", "#10", False)
#crt.Dialog.MessageBox("SecureCRT version is: " + str(__file__))

files=[
      ##'test_arm_adc.py',
      'test_arm_timer.py',
      'test_arm_wdt.py',
	    'test_arm_uart_all.py',
      'test_arm_dma_all.py',
      'test_arm_gpio.py',
      'test_arm_i2c.py',
      'test_arm_qspi.py',
      'test_arm_spi.py',
      'test_arm_nand.py',
	    'test_arm_ipc.py',
      'test_arm_mmc.py',
      'test_arm_trng.py',
      'test_arm_crc.py',
      'test_arm_aes.py',
      'test_arm_ecc.py',
      'test_arm_sha.py',
	    'test_arm_bburam.py',
      'test_arm_prcm_reset.py',
      ##'test_arm_lpddr.py',
      #'test_arm_prcm.py',
      'test_arm_usbhost.py'
       ]
menu=''
count=1

for str1 in files:
    menu = menu + str(count)+'. '+str1.split('.')[0] + '\n'
    count = count+1

menu = menu + str(count)+'. '+'Run all!' + '\n\nAlso you can give a range like 1-3\nPlease select correct option:' 
menu_option=1000
limits=[-1,-1]
while (menu_option > count or menu_option < 1) and limits[0]==-1:
    menu_select = crt.Dialog.Prompt(menu,"Select test module",str(count), False)
    if menu_select == '':
        crt.Dialog.MessageBox("Test item number(or range) is null!", "Error", BUTTON_OK)
        exit()
    if '-' in menu_select:
      try:
            limits_str=menu_select.split('-')
            limits[0]=int(limits_str[0])
            limits[1]=int(limits_str[1])
            menu_option=1000
      except:
            limits[0]=-1
            menu_option=1000
            pass
    else:
      try:
          menu_option= int(menu_select)
      except:
          menu_option=1000
loops=-1        
while loops<0 :    
    loops_str = crt.Dialog.Prompt("Choose number of cycles\nPress 0 to run forever","Enter Number of loops you want to perform:",  "0", False)
    loops = int(loops_str)
loop_counter=0
while loop_counter<loops or loops==0:
    if menu_option == count:
        for str1 in files:
            execfile(str1,globals())
    elif limits[0]>-1:
            for str1 in files[limits[0]-1:limits[1]]:
                  execfile(str1,globals())
    if menu_option<count:
        execfile(files[menu_option-1],globals())
    loop_counter=loop_counter+1

dir_path = os.path.join(os.path.split(__file__)[0]+ '\\LOG\\' + 'Board' + global_board_number + '\\')
a_path=os.path.join(dir_path + '\\'+strftime('analysis_ARM_%Y%m%d-%H%M%S') + '.csv')
a_file=open(a_path,'wb')
writer=csv.writer(a_file,delimiter=',')
count=0
for filename in os.listdir(dir_path):
    if filename.endswith(".csv"):
        if filename.startswith('analysis_'):
            continue
#        crt.Dialog.MessageBox(os.path.join(dir_path, filename))
        
        filepath=os.path.join(dir_path,filename)
        csv_file = open(filepath,'rb')
        reader=csv.reader(csv_file,delimiter=',')
        for row in reader:
            if row[0] !='PASS':
                writer.writerow([filename]+row)
                count=count+1
       
        csv_file.close()
        continue
a_file.close()
