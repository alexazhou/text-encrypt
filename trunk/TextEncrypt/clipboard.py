#!/usr/bin/env python
# -*- coding: utf-8 -*-
#clipboard.py
#Direction:clipboard support,need PYWIN32 installed
#2012-10-12 11:08:34 by zw zwholdu@gmail.com

import win32clipboard as clip
import win32con

def SetClip(clipStr):
    clip.OpenClipboard()
    clip.EmptyClipboard()
    clip.SetClipboardData(win32con.CF_UNICODETEXT,clipStr)
    clip.CloseClipboard()


def GetClip():
    clip.OpenClipboard()
    
    tempStr = ""
    if(clip.IsClipboardFormatAvailable(win32con.CF_UNICODETEXT)):
        tempStr = clip.GetClipboardData(win32con.CF_UNICODETEXT)
    
    clip.CloseClipboard()
    return tempStr


def main():
    print(GetClip())
    SetClip("zzz测试用123")



if __name__ == '__main__':
    main()
    input('Press Enter to exit')
else:
    print ('clipboard.py had been imported as a module')

