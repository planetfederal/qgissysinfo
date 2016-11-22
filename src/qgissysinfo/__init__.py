import systeminfo
import qgisinfo

def info():
	info = [systeminfo.systemInfo(),
			systeminfo.pythonInfo(),
			systeminfo.qtInfo(),
			qgisinfo.qgisMainInfo(),
			qgisinfo.qgisSettingsInfo(),
			qgisinfo.qgisPluginsInfo()]

	return "\n\n".join(info)