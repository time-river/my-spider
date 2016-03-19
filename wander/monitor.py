#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pickle
import subprocess
import time

def setup():
    subs = [subprocess.Popen(['python3.5', 'proxyrequest.py'])]
    subs.append(subprocess.Popen(['python3.5', 'proxyclaw.py']))
    subs.append(subprocess.Popen(['python3.5', 'proxyfilter.py']))
    subs.append(subprocess.Popen(['python3.5', 'proxyverify.py']))
    for sub in subs:
        sub.wait()
    endure = subprocess.Popen(['python3.5', 'proxymonitor.py'])
    while True:
        time.sleep(600)
        
        
if __name__ == "__main__":
    setup()