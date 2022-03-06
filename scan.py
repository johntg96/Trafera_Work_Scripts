import sys
import re
import datetime
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
sro_dict = {}

def split(word):
    return [char for char in word]

def calcAvg(timeframe):
    #appends each hour of the day to this list as they are worked.
    hours = []

    for hour in sro_dict:
        if hour[:2] not in hours:
            hours.append(hour[:2])

    if timeframe == "hour":
        hourly_avg = len(sro_dict.values()) / len(hours)
        return "Hours worked: " + str(len(hours)) + "\nHourly average: " + str(int(hourly_avg))

    elif timeframe == "morning":
        if '07' in hours and '12' in hours:
            morning_sros = []

            for sro in sro_dict.values():
                morning_sros.append(sro)

            morning_avg = len(sro_dict.values()) / 4.5
            morning_total = len(morning_sros)
            return "Morning average: " + str(int(morning_avg)) + " Morning total: " + str(morning_total)
        else:
            return "Morning hours not yet worked."
    elif timeframe == 'afternoon':
        if '12' in hours and '03' in hours:
            afternoon_sros = []

            for sro in sro_dict.values():
                afternoon_sros.append(sro)

            afternoon_avg = len(sro_dict.values()) / 3
            afternoon_total = len(afternoon_sros)
            return "Afternoon average: " + str(int(afternoon_avg)) + " Afternoon total: " + str(afternoon_total)
        else:
            return "Afternoon hours not yet worked."
    elif timeframe == "day":
        if '07' in hours and '03' in hours:
            day_avg = len(sro_dict.values()) / 7
            return "Day average " + str(int(day_avg))
        else:
            return "Full day not yet worked"

def dailyStats():
    return "Total # of unique SRO's scanned: " + str(len(sro_dict.values())) + "\n" + calcAvg('hour') + "\n" + calcAvg("morning") + "\n" + calcAvg("afternoon") + "\n" + calcAvg("day")

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
                sro_timestamp = datetime.datetime.now()
                sro_dict[sro_timestamp.strftime("%X")] = mod_sro
                pyperclip.copy(mod_sro)
                print(f"\n{pyperclip.paste()} copied to clipboard")
                print(sro_dict)
            elif mod_sro in sro_list and stat_mode == "stat_mode_DELETE":
                sro_list.remove(mod_sro)
                print(mod_sro + " deleted from daily list\n")
            elif mod_sro not in sro_list and stat_mode == "stat_mode_DELETE":
                print(f"{mod_sro} is not in daily SRO list\n")
            else:
                pyperclip.copy(mod_sro)
                print(f"\n{pyperclip.paste()} copied to clipboard but not added to daily list\n")
    elif raw_sro_list[0]+raw_sro_list[1]+raw_sro_list[2] == "SRO":
        if len(raw_sro_list) < 10:
            print("\nIncomplete SRO scanned. Please scan again.\n")
        else:
            if raw_sro not in sro_list and stat_mode == "stat_mode_ON":
                sro_list.append(raw_sro)
                pyperclip.copy(raw_sro)
                print(f"\n{pyperclip.paste()} copied to clipboard")
            elif raw_sro in sro_list and stat_mode == "stat_mode_DELETE":
                sro_list.remove(raw_sro)
                print(f"{raw_sro} deleted from daily list\n")
            elif raw_sro not in sro_list and stat_mode == "stat_mode_DELETE":
                print(f"{raw_sro} is not in daily SRO list\n")
            else:
                pyperclip.copy(raw_sro)
                print(f"\n{pyperclip.paste()} copied to clipboard but not added to daily list\n")
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