import os
import yaml

dupcount = 0
def getmode():
    mode = '0'
    dynamicexclude = 'anyconnect-custom-data dynamic-split-exclude-domains'
    dynamicinclude = 'anyconnect-custom-data dynamic-split-include-domains'
    modeoptions = ['1', '2']
    # Get correct split tunnel mode
    while mode not in modeoptions:
        print('What type of split tunnel list are you building?')
        print('''
    [1] Dynamic Exclude
    [2] Dynamic Include
    [q] Quit
        ''')
        mode = input('Please enter a number to specify your split tunnel type: ').lower()
        if mode in modeoptions:
            break
        if mode == 'q':
            print('exiting..')
            exit()
        else:
            print(f'Invalid input.. Please make a valid selection or enter [q] to quit.')

    if mode == '1':
        mode = dynamicexclude
    if mode == '2':
        mode = dynamicinclude
    
    return mode

def getacver():
    acver = '0'
    acveroptions = ['1', '2']
    # Get AnyConnect Version
    while acver not in acveroptions:
        print('What version of AnyConnect do you have deployed?')
        print('''
    [1] AnyConnect 4.10 and Beyond
    [2] AnyConnect 4.9 and Earlier
    [q] Quit
        ''')
        acver = input('Please enter a number to specify your AnyConnect client version: ').lower()
        if acver in acveroptions:
            break
        if acver == 'q':
            print('exiting..')
            exit()
        else:
            print(f'Invalid input.. Please make a valid selection or enter [q] to quit.')

    if acver == '1':
        acver = 1
    if acver == '2':
        acver = 2
    
    return acver

def loadTXTtoList():
    txtFileasList = []
    txtFile = input('Input full path to *.txt file for import or [q] to quit: ')

    if txtFile == 'q':
        print('exiting...')
        exit()

    if not os.path.exists(txtFile):
        print(f'{txtFile} does not exist.')
        return 0

    if txtFile.split('.')[-1].lower() != 'txt':
        print(f'{txtFile} is not a .txt file.')
        return 0

    try:
        with open(txtFile, 'r') as f:
            for line in f:
                line = line.strip('\n')
                line = line.strip(' ')
                line = line.strip(',')
                txtFileasList.append(line)
            f.close()
        return txtFileasList
    
    except:
        print(f'Failed to load {txtFile}. Update file and try again.')

def loadYMLtoList():
    ymlFile = input('Input full path to *.yml file for import or [q] to quit: ')
    
    if ymlFile == 'q':
        print('exiting...')
        exit()

    if not os.path.exists(ymlFile):
        print(f'{ymlFile} does not exist.')
        return 0

    if ymlFile.split('.')[-1].lower() != 'yml':
        print(f'{ymlFile} is not a .yml file.')
        return 0

    try:
        with open(ymlFile, 'r') as f:
            ymlFileasList = yaml.safe_load(f)
        return ymlFileasList
    
    except:
        print(f'Failed to load {ymlFile}. Check formatting and try again.')
        return 0
    

def getdest():
    global dupcount
    inputoptions = ['1', '2', '3']
    urlinput = '0'
    
    while urlinput not in inputoptions:
        print('Please select an input option for the split tunnel destinations.')
        print('''
    [1] Paste in comma seperated values
    [2] Load a .txt file
    [3] Load a .yml file
    [q] Quit
        ''')
        urlinput = input('Please input a selection: ').lower()
        if urlinput in inputoptions:
            break
        if urlinput == 'q':
            print('exiting..')
            exit()
        else:
            print(f'Invalid input.. Please make a valid selection or enter [q] to quit.')

    if urlinput == '1':
        dest = ''

        while ',' not in dest:
            dest = input('Please input a single line of comma seperated values: ')
            if ',' in dest:
                dest = dest.split(',')
                break
            else:
                print('Invalid input detected. Please try again or enter [q] to quit.')

        for i in range(len(dest)):
            dest[i] = dest[i].strip()

        for i in dest:
            if len(i) < 1:
                dest.remove(i)
            if i == ',':
                dest.remove(i)

        while '' in dest:
            dest.remove('')

        if len(dest) <= 0:
            print('A valid comma seperated list was not provided.')
            getdest()

    if urlinput == '2':
        dest = 0

        while dest == 0:
            dest = loadTXTtoList()
            if dest == 'q':
                print('exiting...')
                exit()

    if urlinput == '3':
        dest = 0

        while dest == 0: 
            dest = loadYMLtoList()
            if dest == 'q':
                print('exiting...')
                exit()

    nodups = []

    for i in dest:
        if i not in nodups:
            nodups.append(i)
        else:
            dupcount += 1

    return nodups

def listbuilder(urllist, mode, listname):
    urlstring = ''
    defaultlen = len(mode) + len(listname) + 2
    currentlen = defaultlen

    # Add commas to every entry in url list
    for i in range(len(urllist)):
        urllist[i] += ','
   
    while len(urllist) >= 1:
        indexzero = urllist[0]
        if currentlen + len(indexzero) <= 420:
            currentlen += len(indexzero)
            urlstring += indexzero
            urllist.remove(indexzero)

        else:
            urlstring = urlstring[:-1]+'\n,'
            currentlen = defaultlen + 1

    return urlstring[:-1]

def main():
    # Get AnyConnect version
    acver = getacver()
    # Get dynamic split tunnel mode
    mode = getmode()
    # Get name of split tunnel list
    listname = input('Please input split tunnel list name: ').strip()
    # Get list of domains to be split tunneled
    dest = getdest()
    # Compile a string of domains with a line break everytime we hit a maximum of 420 characters per line.
    build = listbuilder(dest, mode, listname)

    # Use collected data to output actual config.
    print('-' * 20 + ' Begin Output ' + '-' * 20)
    if '\n' in build:
        buildlist = build.split('\n')
        for i in buildlist:
            
            if len(i) > 0:
                print(f'{mode} {listname} {i}')

    else:
        print(f'{mode} {listname} {build}')

    print('-' * 52)
    if dupcount > 0:
        print(f'[INFO] {dupcount} duplicate entries removed.')
    
    if len(build) > 5000:
        if acver == 2:
            print(f'[WARNING] Your dynamic-split-tunnel list is {len(build)} characters. In AnyConnect versions 4.9 and earlier the client limits you to 5000 characters. This limit occurs client side and truncates the dynamic-split-tunnel list to the first 5000 characters without warning.')

        if len(build) > 20000:
            print(f'[WARNING] Your dynamic-split-tunnel list is {len(build)} characters. In AnyConnect version 4.10 and beyond the client limits you to 20000 characters. This limit occurs client side and truncates the dynamic-split-tunnel list to the first 20000 characters without warning.')

if __name__ == '__main__':
    main()