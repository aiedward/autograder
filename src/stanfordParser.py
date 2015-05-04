import os
os.environ['JAVAHOME'] = '/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home/bin/java'
os.environ['JAVA_HOME'] = '/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home/bin/java'
os.environ['STANFORD_PARSER'] = 'lib'
os.environ['STANFORD_MODELS'] = 'lib'

"""
Please also include the path to JRE 1.8 in your nltk/internals.py source code.

line 62: _java_bin = '/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home/bin/java'

line 65: def config_java(bin=_java_bin ...

"""
