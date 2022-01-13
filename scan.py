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
    choice = input("\n1: Scan SRO (with stats)\n2: No Statistic SRO Scan\n3: Delete SRO from List\n4: Daily Statistics\n5: Exit\n\n")

    if choice == "1":
        scan("stat_mode_ON")
    elif choice == "2":
        scan("stat_mode_OFF")
    elif choice == "3":
        scan("stat_mode_DELETE")
    elif choice == "4":
        print(dailyStats())
        menu()
    elif choice == "5":
        sys.exit(0)
    else:
        print("Invalid choice")
        menu()

def statMode(stat_mode):
    while True:
        print("Stat mode: " + stat_mode)
        switch_mode = input("1: stat_mode_ON\n2: stat_mode_OFF\n3: stat_mode_DELETE\n")
        if switch_mode == "1":
            return "stat_mode_ON"
        elif switch_mode == "2":
            return "stat_mode_OFF"
        elif switch_mode == "3":
            return "stat_mode_DELETE"
        else:
            print("incorrect input")
            continue

def scan(stat_mode):
    global sro_list
    raw_sro = input("\nScan SRO (" + stat_mode + "):\n\n").upper()
    raw_sro_list = split(raw_sro)

    #check if SRO has been scanned in using Colemak-Mod DH layout or not
    if raw_sro_list[0]+raw_sro_list[1]+raw_sro_list[2] == "RPY":
        if len(raw_sro_list) < 10:
            print("\nIncomplete SRO scanned. Please scan again.\n")
        else:
            mod_sro = raw_sro.replace('R', 'S').replace('P', 'R').replace('Y', 'O').replace('	','')
            if mod_sro not in sro_list and stat_mode == "stat_mode_ON":
                sro_list.append(mod_sro)
                pyperclip.copy(mod_sro)
                print("\n" + pyperclip.paste() + " copied to clipboard")
            elif mod_sro in sro_list and stat_mode == "stat_mode_DELETE":
                sro_list.remove(mod_sro)
                print(mod_sro + " deleted from daily list\n")
            elif mod_sro not in sro_list and stat_mode == "stat_mode_DELETE":
                print(mod_sro + " is not in daily SRO list\n")
            else:
                pyperclip.copy(mod_sro)
                print("\n" + pyperclip.paste() + " copied to clipboard but not added to daily list\n")
    elif raw_sro_list[0]+raw_sro_list[1]+raw_sro_list[2] == "SRO":
        if len(raw_sro_list) < 10:
            print("\nIncomplete SRO scanned. Please scan again.\n")
        else:
            if raw_sro not in sro_list and stat_mode == "stat_mode_ON":
                sro_list.append(raw_sro)
                pyperclip.copy(raw_sro)
                print("\n" + pyperclip.paste() + " copied to clipboard")
            elif raw_sro in sro_list and stat_mode == "stat_mode_DELETE":
                sro_list.remove(raw_sro)
                print(raw_sro + " deleted from daily list\n")
            elif raw_sro not in sro_list and stat_mode == "stat_mode_DELETE":
                print(raw_sro + " is not in daily SRO list\n")
            else:
                pyperclip.copy(raw_sro)
                print("\n" + pyperclip.paste() + " copied to clipboard but not added to daily list\n")
    elif raw_sro == "MENU":
        menu()
    elif raw_sro == "STATS":
        print(dailyStats())
    elif raw_sro == "MODE":
        stat_mode = statMode(stat_mode)
    elif raw_sro == "DELETE":
        stat_mode = "stat_mode_DELETE"
    elif raw_sro == "TURN ON":
        stat_mode = "stat_mode_ON"
    elif raw_sro == "TURN OFF":
        stat_mode = "stat_mode_OFF"
    elif raw_sro == "EXIT":
        sys.exit(0)
    else:
        print("SRO not detected, try again.")
        scan(stat_mode)
    
    scan(stat_mode)

menu()