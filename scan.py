import sys
import re
import pyperclip

print('|||||--Trafera Work Scripts--|||||')
def menu():
    choice = int(input('\n1: Scan SRO\n2: Exit\n\n'))

    if choice == 1:
        scan()
    elif choice == 2:
        sys.exit()
    else:
        print('Invalid choice')
        menu()

def scan():
    raw_sro = input('\nScan SRO:\n\n')
    if raw_sro == '~':
        sys.exit()
    else:
        legit_sro = raw_sro.replace('R', 'S').replace('r', 'S').replace('P', 'R').replace('p', 'R').replace('Y', 'O').replace('y', 'O').replace('	','')
        pyperclip.copy(legit_sro)
        print('\n"' + pyperclip.paste() + '" copied to clipboard!')
        scan()

menu()