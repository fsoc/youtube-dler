#!/usr/bin/python
import subprocess, os, os.path, re
from pathlib import PurePath

commandDir = '/home/anon/proj/ytdler/testcommands/'
dlDir = '/home/anon/proj/ytdler/'

def scanFolder():
    for item in os.listdir(commandDir):
        if os.path.isfile(item) and item.endswith('.txt'):
            print('handling ' + item)
            try:
                handleFile(item)
                rename(item, 'ok')
            except Exception as e:
                print(e)
                rename(item, 'fail')

def rename(filename, suffix):
    os.chdir(commandDir)
    os.rename(filename, filename + '.' + suffix)


def handleFile(file):
    first = True
    path = '/tmp'
    with open(commandDir+file) as f:
        for line in f:
            line = line.rstrip()
            if first:
                first = False
                path = appendslash(line)
                validateFirst(line)
                handleFirstLine(line)
            else:
                validateUrl(line)
                handleLine(line, path)

def appendslash(path):
    if path.endswith('/'):
        return path
    else:
        return path + '/'

def validateFirst(path):
    if not re.fullmatch('[a-zA-z0-9\.\/]+', path):
        raise Exception("bad whitelist path:" + path)
    if re.match('\.\.', path):
        raise Exception("bad dot dot path:" + path)
    # handle symlinks, and ..
    child = os.path.realpath(dlDir + path)
    parent = os.path.realpath(dlDir)
    if os.path.commonpath([parent]) != os.path.commonpath([parent, child]):
        raise Exception("bad path:" + child)
    
def validateUrl(url):
    if not re.fullmatch('''((?:(?<=[^a-zA-Z0-9]){0,}(?:(?:https?\:\/\/){0,1}(?:[a-zA-Z0-9\%]{1,}\:[a-zA-Z0-9\%]{1,}[@]){,1})(?:(?:\w{1,}\.{1}){1,5}(?:(?:[a-zA-Z]){1,})|(?:[a-zA-Z]{1,}\/[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\:[0-9]{1,4}){1})){1}(?:(?:(?:\/{0,1}(?:[a-zA-Z0-9\-\_\=\-]){1,})*)(?:[?][a-zA-Z0-9\=\%\&\_\-]{1,}){0,1})(?:\.(?:[a-zA-Z0-9]){0,}){0,1})''', url):
        raise Exception("malformed url")

def handleFirstLine(path):
    os.chdir(dlDir)
    print(subprocess.run(['mkdir', '-p', path], text=True, capture_output=True))
    os.chdir(dlDir+path)

def handleLine(url, path):
    print(url)
    print(subprocess.run(['youtube-dl', '--no-part', '-q', url], text=True, capture_output=True))
    
scanFolder()
