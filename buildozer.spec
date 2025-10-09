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

# Závislosti (držíme sa stabilných verzií na Android)
# Pozn.: KivyMD a aiohttp sú vynechané kvôli častým build problémom. Pridáme neskôr, ak ich budeš potrebovať.
requirements = python3,kivy==2.2.1,requests,pillow,pyjnius,plyer,certifi

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

# Architektúry (najprv kompilujeme jednu – je rýchlejšie a stabilnejšie)
android.archs = arm64-v8a

# Voliteľné: názov balíka pre Android (ak chceš vlastný app id)
# package.domain a package.name spolu vytvoria: org.tdm.twitchdropsminer

# Voliteľné: ikona a špliechacia obrazovka (ak budeš mať súbory)
# icon.filename = assets/icon.png
# presplash.filename = assets/presplash.png

# Voliteľné: ďalšie optimalizácie
# android.prevent_scraping = True
# android.enable_androidx = True

[buildozer]
# Verbózne logy pre ľahšie debugovanie na Actions
log_level = 2
warn_on_root = 1

# Ukladanie logov buildozeru (pomôže pri debugovaní)
# storage_dir = .buildozer

# Voliteľné: force-ovať p4a verziu (zvyčajne netreba)
# p4a.branch = master
