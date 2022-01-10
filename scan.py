import sys
import re
import time
import pyperclip

print('''
           __________                                 
         .'----------`.                              
         | .--------. |                             
         | |10010101| |       __________              
         | |01011010| |      /__________\             
.--------| `--------' |------|    --=-- |-------------.
|        `----,-.-----'      |o ======  |             | 
|       ______|_|_______     |__________|             | 
|      /  ############  \                             | 
|     /  ##############  \   TRAFERA WORK SCRIPT      | 
|     ^^^^^^^^^^^^^^^^^^^^   c. 2022 John Garrison    | 
+-----------------------------------------------------+
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 
''')

sro_list = []

def split(word):
    return [char for char in word]

def dailyStats():
    print(sro_list)
    num_units = len(sro_list)
    return "Total # of SRO's scanned: " + str(num_units)

def menu():
    choice = int(input('\n1: Scan SRO\n2: Daily Stats\n3: Exit\n\n'))

    if choice == 1:
        scan()
    elif choice == 2:
        print(dailyStats())
    elif choice == 3:
        sys.exit(0)
    else:
        print('Invalid choice')
        menu()

def scan():
    global sro_list
    raw_sro = input('\nScan SRO:\n\n')
    raw_sro.upper()
    raw_sro_list = split(raw_sro)

    #check if SRO has been scanned in using Colemak-Mod DH layout or not
    if raw_sro_list[0]+raw_sro_list[1]+raw_sro_list[2] == "RPY":
        mod_sro = raw_sro.replace('R', 'S').replace('P', 'R').replace('Y', 'O').replace('	','')
        sro_list.append(mod_sro)
        pyperclip.copy(mod_sro)
    elif raw_sro_list[0]+raw_sro_list[1]+raw_sro_list[2] == "SRO":
        sro_list.append(raw_sro)
        pyperclip.copy(raw_sro)
    elif raw_sro == 'menu':
        menu()
    elif raw_sro == "daily":
        print(dailyStats())
        scan()
    elif raw_sro == 'exit':
        sys.exit(0)
    else:
        print("SRO not detected, try again.")
        scan()

    print('\n' + pyperclip.paste() + ' copied to clipboard')
    scan()

menu()