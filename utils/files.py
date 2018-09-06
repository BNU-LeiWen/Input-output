#!/usr/bin/env python
import os

def makeifnotexist(path):
    if not os.path.isdir(path):
        os.makedirs(path)

