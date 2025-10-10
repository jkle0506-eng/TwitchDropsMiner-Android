[app]
# Základné informácie o aplikácii
title = TwitchDropsMiner
package.name = twitchdropsminer
package.domain = org.tdm

# Zdrojový kód
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt

# Verzovanie
version = 1.0

# Závislosti (vrátime Kivy 2.2.1 s p4a master)
requirements = python3, kivy==2.2.1, requests, pillow, pyjnius==1.6.1, plyer, certifi

# Orientácia a zobrazenie
orientation = portrait
fullscreen = 0

# Android oprávnenia
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WAKE_LOCK

# Android SDK/NDK/API
android.api = 33
android.minapi = 21
android.ndk = 25b

# Buildozer/p4a nastavenia
android.private_storage = True
android.logcat_filters = *:S python:D
android.copy_libs = 1

# Architektúry (pre rýchlejší a stabilnejší build najprv len 64-bit ARM)
android.archs = arm64-v8a

# Použijeme najnovší p4a master branch (má lepšie patche pre Kivy 2.2.x)
p4a.branch = master

# Voliteľné: ikona a presplash (ak máš súbory v projekte)
# icon.filename = assets/icon.png
# presplash.filename = assets/presplash.png

# Voliteľné: ďalšie optimalizácie/kompat nastavenia
# android.enable_androidx = True
# android.allow_backup = False
# android.prevent_scraping = True

[buildozer]
# Verbózne logy pre ľahšie debugovanie na CI
log_level = 2
warn_on_root = 1

# Ukladanie build artefaktov (necháme default, Buildozer si vytvorí .buildozer)
# storage_dir = .buildozer
