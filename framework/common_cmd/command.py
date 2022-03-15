# coding = utf-8
import sys


def CheckSysIsWin():
    my_os = sys.platform
    if my_os == 'win32':
        return True
    else:
        return False


def GetKillAdbCmd():
    if CheckSysIsWin():
        return 'taskkill -f /im adb.exe'
    else:
        return ''


def GetRootCmd():
    return 'adb root'


def GetAndroidLog():
    return 'adb logcat'


def GetDevices():
    return "adb devices"


def GetStopApp(package):
    return f'adb shell pm clear {package}'


def GetStartApp(activity):
    return f'adb shell am start -n {activity}'


def GetWindowPolicy():
    return 'adb shell dumpsys window policy'


def GetInstalledApp(package):
    return f'adb shell "pm list package |grep {package}"'


def GetAppStartActivity(package):
    '''
        android.intent.action.MAIN:
        ed54adc com.bnux.app.carcontrol/com.bnqc.carcontrolgx16.view.MainActivity filter c363634
        Action: "android.intent.action.MAIN"
          Category: "android.intent.category.LAUNCHER"
      bnux.vehicle.carcontrol.action.EXPERIENCE:
    '''
    return f'adb shell "dumpsys package {package} |grep action.MAIN -A 2"'


def GetInstallApk(apk_path):
    return f'adb install {apk_path}'
