[app]
title = TwitchDropsMiner
package.name = twitchdropsminer
package.domain = org.tdm
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt
version = 1.0
requirements = python3,kivy==2.2.1,requests,pillow,pyjnius,plyer,certifi
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WAKE_LOCK
android.api = 33
android.minapi = 21
android.ndk = 25b
android.private_storage = True
android.logcat_filters = *:S python:D
android.copy_libs = 1
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
