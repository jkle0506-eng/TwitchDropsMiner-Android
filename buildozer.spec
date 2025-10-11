[app]
# (Základné informácie o aplikácii)
title = TwitchDropsMiner
package.name = twitchdropsminer
package.domain = org.example
source.dir = .
source.include_exts = py,kv,png,jpg,json,txt,ico
version = 0.1.0
# Vstupný súbor (entrypoint)
entrypoint = main.py

# Názov vrstvy GUI (kivy) - len ak používaš .kv súbory
# kv = myapp.kv

# Knižnice požadované pre app. Uprav podľa svojho requirements.txt.
# Pin verzie tam, kde vieš že sú kompatibilné.
requirements = python3,kivy==2.1.0,requests,websockets,pyotp

# Orientácia a správanie
orientation = portrait
fullscreen = 0
presplash.filename =
icon.filename = %(source.dir)s/icon.png

# Zmenšovanie veľkosti (voliteľné)
# android.arch = armeabi-v7a, arm64-v8a

# Log level: 1=debug, 2=info, 3=warning, 4=error
log_level = 2
# Výstupné súbory sa budú ukladať do bin/ (default)

# -----------------------------------------------------------------
# Android specifics
# -----------------------------------------------------------------
# Android API (musí byť nainštalovaný v SDK cez sdkmanager)
android.api = 31
android.minapi = 21
# doporučené NDK pre p4a: 21b (veľa p4a receptov očakáva NDK r21)
android.ndk = 21b
android.ndk_api = 21
# architektúry ktoré chceš podporovať
android.arch = armeabi-v7a, arm64-v8a
# bootstrap (štandardne sdl2)
android.bootstrap = sdl2

# permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# cesta k SDK v CI — v workflow sme nastavili ANDROID_SDK_ROOT = /usr/local/lib/android/sdk
[buildozer]
warn_on_root = 1
android.sdk_path = /usr/local/lib/android/sdk

# -----------------------------------------------------------------
# Extra paddings / packaging (voliteľné)
# -----------------------------------------------------------------
# (Príklady, ak potrebuješ pridať natívne knižnice alebo manifest úpravy)
# android.add_src = src/android
# android.add_libs_armeabi_v7a = libs/armeabi-v7a/libexample.so
# android.manifest_intent_filters = <intent-filter> ... </intent-filter>
