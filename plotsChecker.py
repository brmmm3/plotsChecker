#!/usr/bin/python3

if __name__ == "__main__":
    import os
    import sys
    from colorama import init, Fore, Style
    BRIGHTRED = Style.BRIGHT + Fore.RED
    BRIGHTGREEN = Style.BRIGHT + Fore.GREEN
    BRIGHTBLUE = Style.BRIGHT + Fore.BLUE
    BRIGHTYELLOW = Style.BRIGHT + Fore.YELLOW
    init()
    if len(sys.argv) < 2:
        print(BRIGHTGREEN + "BURST plots checker (version 1.0)\nChecking and validation plots for BURST")
        print("Translated into Python from Blago's C++ version which is only for Windows.")
        print(BRIGHTBLUE + "Usage: %s [PATH1] [PATH2] ..." % sys.argv[0])
        print(Fore.GREEN + "Example: %s /media/data/plots" + Style.RESET_ALL)
        sys.exit(1)
    nonceSize = 4096 * 64
    for plotsDirName in sys.argv[1:]:
        for fileName in os.listdir(plotsDirName):
            pathName = os.path.join(plotsDirName, fileName)
            # Ignore directories and invalid file names
            if os.path.isdir(pathName) or (fileName.count("_") != 3) or "." in fileName:
                continue
            key, nonce, nonces, stagger = [ int(x) for x in fileName.split("_") ]
            fileSize = os.path.getsize(pathName)
            if fileSize == nonces * nonceSize:
                print(BRIGHTGREEN + "OK %s" % pathName + Style.RESET_ALL)
                continue
            if nonces == stagger:
                print(BRIGHTRED + "INVALID (replot) %s" % pathName + Style.RESET_ALL)
                continue
            newNonces = int(fileSize / nonceSize / stagger) * stagger
            newPathName = os.path.join(plotsDirName, "%d_%d_%d_%d" % (key, nonce, newNonces, stagger))
            try:
                os.rename(pathName, newPathName)
                print(BRIGHTYELLOW + "File %s renamed to %s" % (pathName, newPathName) + Style.RESET_ALL)
            except Exception as exc:
                print(BRIGHTRED + "FAILED renaming file: %s\n" % pathName + exc + Style.RESET_ALL)
                continue
            newFileSize = newNonces * nonceSize
            if fileSize != newFileSize:
                try:
                    os.truncate(newPathName, newFileSize)
                    print(BRIGHTBLUE + "TRUNCATED %s to %d bytes" % (newPathName, newFileSize) + Style.RESET_ALL)
                except:
                    print(BRIGHTRED + "FAILED truncating file: %s\n" % newPathName + exc + Style.RESET_ALL)

