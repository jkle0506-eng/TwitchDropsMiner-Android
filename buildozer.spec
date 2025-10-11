[app]
# (Základné informácie o aplikácii)
title = TwitchDropsMiner
package.name = twitchdropsminer
package.domain = org.example
source.dir = .
source.include_exts = py,kv,png,jpg,json,txt
version = 0.1
# Vstupný súbor (entrypoint)
entrypoint = main.py
# Pinnú verziu Kivy a ďalších knižníc — odporúčam zafixovať verzie pre reprodukovateľný build
requirements = python3,kivy==2.1.0,requests,websockets,pyotp
orientation = portrait
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png
# odstráni Kivy nastavenia v runtime (voliteľné)
android.use_kivy_settings = False
log_level = 2

# -----------------------------------------------------------------
# Android specifics
# -----------------------------------------------------------------
# Android API (musí byť nainštalovaný v SDK cez sdkmanager)
android.api = 31
android.minapi = 21
# odporúčané NDK pre p4a: 21b (veľa p4a receptov očakáva NDK r21)
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
