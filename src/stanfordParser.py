"""
Please edit lines 13 & 14 with the path to JRE 1.8

Please also include the path to JRE 1.8 in your nltk/internals.py source code if it is not on your system by default.

nltk/internals.py line 62: _java_bin = '/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home/bin/java'

nltk/internals.py line 65: def config_java(bin=_java_bin ...
"""


import os
os.environ['JAVAHOME'] = '/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home/bin/java'
os.environ['JAVA_HOME'] = '/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home/bin/java'
os.environ['STANFORD_PARSER'] = 'lib'
os.environ['STANFORD_MODELS'] = 'lib'