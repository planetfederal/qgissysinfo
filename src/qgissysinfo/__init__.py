import systeminfo
import qgisinfo
import os

def info():
	_info = systeminfo.allSystemInfo()
	_info.update(qgisinfo.allQgisInfo())
	return _info

def _as_text(o, level = 0):
	if isinstance(o, basestring):
		return o
	elif isinstance(o, dict):
		s = ""
		for key,value in o.iteritems():
			s += key + os.linesep
			s += ("\t" * level)
			s += _as_text(value, level + 1)
		return s
	elif isinstance(o, list):
		s = ""
		for item in o:
			s += ("\t" * level)
			s += _as_text(item, level)
		return s

def info_as_text():	
	return _as_text(info())