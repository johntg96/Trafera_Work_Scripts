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
    return "Total # of unique SRO's scanned: " + str(num_units)

def menu():
    choice = input('\n1: Scan SRO\n2: Daily Stats\n3: Scan SRO No Stats\n4: Exit\n\n')

    if choice == "1":
        scan("stat_mode_ON")
    elif choice == "2":
        print(dailyStats())
        menu()
    elif choice == "3":
        scan("stat_mode_OFF")
    elif choice == "4":
        sys.exit(0)
    else:
        print("Invalid choice")
        menu()

def statMode(stat_mode):
    while True:
        print("Stat mode: " + stat_mode)
        switch_mode = input('Type "on" or "off" to switch stat mode.\n').upper()
        if switch_mode == "ON":
            return "stat_mode_ON"
        elif switch_mode == "OFF":
            return "stat_mode_OFF"
        else:
            print("incorrect input")
            continue

def scan(stat_mode):
    global sro_list
    raw_sro = input('\nScan SRO (' + stat_mode + '):\n\n').upper()
    raw_sro_list = split(raw_sro)

    #check if SRO has been scanned in using Colemak-Mod DH layout or not
    if raw_sro_list[0]+raw_sro_list[1]+raw_sro_list[2] == "RPY":
        mod_sro = raw_sro.replace('R', 'S').replace('P', 'R').replace('Y', 'O').replace('	','')
        if mod_sro not in sro_list and stat_mode == 'stat_mode_ON':
            sro_list.append(mod_sro)
        pyperclip.copy(mod_sro)
    elif raw_sro_list[0]+raw_sro_list[1]+raw_sro_list[2] == "SRO":
        if raw_sro not in sro_list and stat_mode == 'stat_mode_ON':
            sro_list.append(raw_sro)
        pyperclip.copy(raw_sro)
    elif raw_sro == 'MENU':
        menu()
    elif raw_sro == "DAILY":
        print(dailyStats())
        scan(stat_mode)
    elif raw_sro == 'MODE':
        stat_mode = statMode(stat_mode)
    elif raw_sro == 'EXIT':
        sys.exit(0)
    else:
        print("SRO not detected, try again.")
        scan(stat_mode)

    print('\n' + pyperclip.paste() + ' copied to clipboard')
    scan(stat_mode)

menu()