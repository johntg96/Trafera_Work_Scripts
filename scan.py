import sys
import re
import datetime
import pyperclip
import csv

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

sro_dict = {}

def help():
    return '''
----------------------------Help-----------------------------------
-------------------------------------------------------------------
Commands:
menu     -> Open Menu
stats    -> Display statistics
list     -> Displays scanned SRO's with corresponding timestamps
save     -> Exports daily scanned SRO's to .csv file
mode     -> Change scan mode
turn on  -> Turns ON statistic tracking
turn off -> Turns OFF statistic tracking
delete   -> Turns on DELETE mode to remove scanned SRO's
exit     -> Exits"
-------------------------------------------------------------------
    '''

def split(word):
    return [char for char in word]

def calcAvg(timeframe):
    #appends each hour of the day to this list as they are worked when this function is called.
    hours = []

    for hour in sro_dict.values():
        if hour[:2] not in hours:
            hours.append(hour[:2])

    if timeframe == "hour":
        hourly_avg = len(sro_dict) / len(hours)
        return "Hours worked: " + str(len(hours)) + "\nHourly average: " + str(hourly_avg)

    elif timeframe == "morning":
        if '07' in hours and '12' in hours:
            morning_sros = []

            for sro in sro_dict:
                morning_sros.append(sro)

            morning_avg = len(sro_dict) / 4.5
            morning_total = len(morning_sros)
            return "Morning average: " + str(morning_avg) + " Morning total: " + str(morning_total)
        else:
            return "Morning hours not yet worked."
    elif timeframe == 'afternoon':
        if '12' in hours and '03' in hours:
            afternoon_sros = []

            for sro in sro_dict:
                afternoon_sros.append(sro)

            afternoon_avg = len(sro_dict) / 3
            afternoon_total = len(afternoon_sros)
            return "Afternoon average: " + str(afternoon_avg) + " Afternoon total: " + str(afternoon_total)
        else:
            return "Afternoon hours not yet worked."
    elif timeframe == "day":
        if '07' in hours and '03' in hours:
            day_avg = len(sro_dict) / 7
            export_choice = False

            while export_choice == False:
                choice = input("Full workday hours worked. Would you like to export today's daily scans? y/n:\n")

                if choice == "y":
                    print(exportDailyScans())
                    export_choice == True
                    return "Day average " + str(day_avg)
                elif export_choice == "n":
                    export_choice == True
                    return "Day average " + str(day_avg)
                else:
                    print("Invalid choice. Try again.\n")
        else:
            return "Full day not yet worked"

def dailyStats():
    if len(sro_dict) != 0:
        return "\nTotal # of unique SRO's scanned: " + str(len(sro_dict)) + "\n" + calcAvg('hour') + "\n" + calcAvg("morning") + "\n" + calcAvg("afternoon") + "\n" + calcAvg("day")
    else:
        return "\nNo SRO data available"

def menu():
    choice = input('''
----------Menu------------
--------------------------
1: Scan SRO (with stats)
2: No Statistic SRO Scan
3: Delete SRO from List
4: Daily Statistics
5: Export Scans
6: Help
7: Exit
--------------------------
choice: ''')

    if choice == "1":
        scan("stat_mode_ON")
    elif choice == "2":
        scan("stat_mode_OFF")
    elif choice == "3":
        scan("stat_mode_DELETE")
    elif choice == "4":
        print(dailyStats())
        input("Press any key to continue...")
        menu()
    elif choice == "5":
        print(exportDailyScans())
        input("Press any key to continue...")
        menu()
    elif choice == "6":
        print(help())
        input("Press any key to continue...")
        menu()
    elif choice == "7":
        sys.exit(0)
    else:
        print("Invalid choice")
        menu()

def exportDailyScans():
    if len(sro_dict) != 0:
        export_status = None
        while True:
            confirm = input("\nWould you like to export daily scans to .csv file? y/n:\n")
            if confirm == "y":
                date = datetime.datetime.now()
                filename = "scan_history_" + date.strftime("%m") + "_" + date.strftime("%d") + "_" + date.strftime("%y") + ".csv"
                fields = ["SRO", "Timestamp"]
                with open(filename, 'w+') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(fields)
                    csvwriter.writerows(sro_dict.items())

                export_status = f"\nExport complete. [Saved: {filename}]\n"
                break
            elif confirm == "n":
                export_status = "\nExport aborted.\n"
                break
            else:
                print("\nIncorrect input. Try again.\n")
                continue
        return export_status
    else:
        return "\nCannot export, no SRO's scanned with stat_mode_ON\n"

def statMode(stat_mode):
    while True:
        print("Stat mode: " + stat_mode)
        switch_mode = input("1: stat_mode_ON\n2: stat_mode_OFF\n3: stat_mode_DELETE\n")
        if switch_mode == "1":
            stat_mode = "stat_mode_ON"
            break
        elif switch_mode == "2":
            stat_mode = "stat_mode_OFF"
            break
        elif switch_mode == "3":
            stat_mode = "stat_mode_DELETE"
            break
        else:
            print("incorrect input")
            continue

    return stat_mode

def scan(stat_mode):
    raw_sro = input(f"\nScan SRO {stat_mode}:\n\n").upper()
    raw_sro_list = split(raw_sro)

    #check if SRO has been scanned in using Colemak-Mod DH layout or not
    if raw_sro_list[0]+raw_sro_list[1]+raw_sro_list[2] == "RPY":
        if len(raw_sro_list) < 10:
            print("\nIncomplete SRO scanned. Please scan again.\n")
        else:
            mod_sro = raw_sro.replace('R', 'S').replace('P', 'R').replace('Y', 'O').replace('	','')
            if mod_sro not in sro_dict.keys() and stat_mode == "stat_mode_ON":
                sro_timestamp = datetime.datetime.now()
                sro_dict[mod_sro] = sro_timestamp.strftime("%X")
                pyperclip.copy(mod_sro)
                print(f"\n{pyperclip.paste()} copied to clipboard")
            elif mod_sro in sro_dict.keys() and stat_mode == "stat_mode_DELETE":
                del sro_dict[mod_sro]
                print(mod_sro + " deleted\n")
            elif mod_sro not in sro_dict.keys() and stat_mode == "stat_mode_DELETE":
                print(f"{mod_sro} not found\n")
            else:
                pyperclip.copy(mod_sro)
                print(f"\n{pyperclip.paste()} copied to clipboard but not added to daily list\n")
    elif raw_sro_list[0]+raw_sro_list[1]+raw_sro_list[2] == "SRO":
        if len(raw_sro_list) < 10:
            print("\nIncomplete SRO scanned. Please scan again.\n")
        else:
            if raw_sro not in sro_dict.keys() and stat_mode == "stat_mode_ON":
                sro_timestamp = datetime.datetime.now()
                sro_dict[raw_sro] = sro_timestamp.strftime("%X")
                pyperclip.copy(raw_sro)
                print(f"\n{pyperclip.paste()} copied to clipboard")
            elif raw_sro in sro_dict.keys() and stat_mode == "stat_mode_DELETE":
                del sro_dict[raw_sro]
                print(f"{raw_sro} deleted\n")
            elif raw_sro not in sro_dict.keys() and stat_mode == "stat_mode_DELETE":
                print(f"{raw_sro} not found\n")
            else:
                pyperclip.copy(raw_sro)
                print(f"\n{pyperclip.paste()} copied to clipboard but not added to daily list\n")
    elif raw_sro == "MENU":
        menu()
    elif raw_sro == "STATS":
        print(dailyStats())
        input("Press any key to continue...")
    elif raw_sro == "MODE":
        stat_mode = statMode(stat_mode)
    elif raw_sro == "DELETE":
        stat_mode = "stat_mode_DELETE"
    elif raw_sro == "TURN ON":
        stat_mode = "stat_mode_ON"
    elif raw_sro == "TURN OFF":
        stat_mode = "stat_mode_OFF"
    elif raw_sro == "LIST":
        print(sro_dict)
        input("Press any key to continue...")
    elif raw_sro == "HELP":
        print(help())
        input("Press any key to continue...")
    elif raw_sro == "SAVE" or raw_sro == "EXPORT":
        print(exportDailyScans())
        input("Press any key to continue...")
    elif raw_sro == "EXIT":
        sys.exit(0)
    else:
        print("SRO not detected, try again.")
        scan(stat_mode)
    
    scan(stat_mode)

menu()