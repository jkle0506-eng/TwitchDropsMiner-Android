# TwitchDropsMiner Android - Kompletný návod na inštaláciu

Tento návod vás prevedie celým procesom od prípravy prostredia až po inštaláciu aplikácie na vašom Android zariadení.

## Obsah

1. [Príprava systému](#1-príprava-systému)
2. [Inštalácia závislostí](#2-inštalácia-závislostí)
3. [Zostavenie aplikácie](#3-zostavenie-aplikácie)
4. [Inštalácia na zariadenie](#4-inštalácia-na-zariadenie)
5. [Prvé spustenie](#5-prvé-spustenie)
6. [Riešenie problémov](#6-riešenie-problémov)

---

## 1. Príprava systému

### Požiadavky

- **Operačný systém**: Linux (Ubuntu 20.04+) alebo Windows s WSL2
- **RAM**: Minimálne 8GB (odporúčané 16GB)
- **Disk**: Minimálne 20GB voľného miesta
- **Internet**: Stabilné pripojenie (prvé zostavenie stiahne ~2-3GB)

### Pre Windows používateľov - Inštalácia WSL2

```powershell
# Otvorte PowerShell ako administrátor

# Povoľte WSL
wsl --install

# Reštartujte počítač

# Po reštarte nainštalujte Ubuntu
wsl --install -d Ubuntu-22.04

# Spustite Ubuntu
wsl
```

### Pre Linux používateľov

Pokračujte priamo na ďalší krok.

---

## 2. Inštalácia závislostí

### Krok 2.1: Aktualizácia systému

```bash
sudo apt update
sudo apt upgrade -y
```

### Krok 2.2: Inštalácia základných nástrojov

```bash
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    zip \
    unzip \
    wget \
    curl
```

### Krok 2.3: Inštalácia Java Development Kit

```bash
# Inštalácia OpenJDK 17
sudo apt install -y openjdk-17-jdk

# Nastavenie JAVA_HOME
echo 'export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64' >> ~/.bashrc
echo 'export PATH=$PATH:$JAVA_HOME/bin' >> ~/.bashrc
source ~/.bashrc

# Overenie inštalácie
java -version
```

Výstup by mal byť podobný:
```
openjdk version "17.0.x" ...
```

### Krok 2.4: Inštalácia build nástrojov

```bash
sudo apt install -y \
    autoconf \
    automake \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    libffi-dev \
    libssl-dev \
    build-essential \
    ccache \
    libsqlite3-dev \
    libreadline-dev \
    libbz2-dev \
    libgdbm-dev \
    libgdbm-compat-dev \
    liblzma-dev \
    uuid-dev
```

### Krok 2.5: Inštalácia Android nástrojov (ADB)

```bash
sudo apt install -y adb

# Overenie inštalácie
adb version
```

### Krok 2.6: Vytvorenie virtuálneho prostredia

```bash
# Vytvorte priečinok pre projekt
mkdir -p ~/android-projects
cd ~/android-projects

# Vytvorte virtuálne prostredie
python3 -m venv buildozer-env

# Aktivujte virtuálne prostredie
source buildozer-env/bin/activate

# Váš prompt by sa mal zmeniť na:
# (buildozer-env) user@host:~/android-projects$
```

### Krok 2.7: Inštalácia Buildozer

```bash
# Aktualizujte pip
pip install --upgrade pip setuptools wheel

# Inštalujte Buildozer a závislosti
pip install buildozer
pip install cython==0.29.36

# Overenie inštalácie
buildozer --version
```

Výstup by mal byť:
```
1.5.0
```

---

## 3. Zostavenie aplikácie

### Krok 3.1: Získanie zdrojového kódu

```bash
# Prejdite do priečinka projektu
cd ~/android-projects

# Skopírujte priečinok TwitchDropsMiner_Android sem
# (predpokladáme, že ste ho už dostali)

cd TwitchDropsMiner_Android
```

### Krok 3.2: Overenie štruktúry projektu

```bash
ls -la
```

Mali by ste vidieť:
```
main.py
buildozer.spec
requirements.txt
core/
ui/
assets/
README.md
build.sh
install.sh
```

### Krok 3.3: Prvé zostavenie (Debug verzia)

**⚠️ DÔLEŽITÉ: Prvé zostavenie trvá 30-90 minút!**

```bash
# Aktivujte virtuálne prostredie (ak nie je aktívne)
source ~/android-projects/buildozer-env/bin/activate

# Spustite zostavenie
buildozer android debug
```

Buildozer automaticky:
1. Stiahne Android SDK (~1GB)
2. Stiahne Android NDK (~1GB)
3. Stiahne Python-for-Android
4. Skompiluje všetky závislosti
5. Vytvorí APK súbor

**Počas zostavenia:**
- Neukončujte proces
- Môžete vidieť rôzne warningy - to je normálne
- Ak sa zobrazí otázka o licencii SDK, napíšte `y` a stlačte Enter

### Krok 3.4: Overenie zostavenia

```bash
# Skontrolujte, či sa vytvoril APK
ls -lh bin/

# Mali by ste vidieť súbor podobný:
# twitchdropsminer-1.0.0-arm64-v8a-debug.apk
```

### Krok 3.5: Zostavenie Release verzie (voliteľné)

```bash
# Pre distribúciu použite release verziu
buildozer android release

# Release APK bude v bin/ s názvom:
# twitchdropsminer-1.0.0-arm64-v8a-release-unsigned.apk
```

---

## 4. Inštalácia na zariadenie

### Metóda A: Cez USB (Odporúčané)

#### Krok 4.1: Príprava Android zariadenia

1. **Povoľte Vývojárske možnosti:**
   - Otvorte **Nastavenia**
   - Prejdite na **O telefóne** (alebo **O zariadení**)
   - Nájdite **Číslo zostavy** (Build number)
   - Kliknite na neho **7-krát**
   - Zobrazí sa: "Ste teraz vývojár!"

2. **Povoľte USB ladenie:**
   - Vráťte sa do **Nastavenia**
   - Nájdite **Vývojárske možnosti** (Developer options)
   - Zapnite **USB ladenie** (USB debugging)

3. **Pripojte zariadenie k počítaču:**
   - Použite USB kábel
   - Na telefóne sa zobrazí dialóg "Povoliť USB ladenie?"
   - Zaškrtnite "Vždy povoliť z tohto počítača"
   - Kliknite **OK**

#### Krok 4.2: Overenie pripojenia

```bash
# Skontrolujte pripojené zariadenia
adb devices
```

Mali by ste vidieť:
```
List of devices attached
ABC123XYZ    device
```

Ak vidíte `unauthorized`, povoľte USB ladenie na telefóne.

#### Krok 4.3: Inštalácia APK

```bash
# Použite install skript
./install.sh

# Alebo manuálne:
adb install -r bin/twitchdropsminer-*.apk
```

Výstup:
```
Performing Streamed Install
Success
```

### Metóda B: Cez súbor (Bez USB)

#### Krok 4.1: Prenos APK na telefón

**Možnosť 1: Cez cloud (Google Drive, Dropbox, atď.)**
1. Nahrajte APK z `bin/` do cloudu
2. Stiahnite ho na telefóne

**Možnosť 2: Cez email**
1. Pošlite APK sebe na email
2. Otvorte email na telefóne a stiahnite prílohu

**Možnosť 3: Cez USB (len prenos súboru)**
1. Pripojte telefón k PC
2. Skopírujte APK do priečinka Downloads na telefóne

#### Krok 4.2: Inštalácia na telefóne

1. Otvorte **Správca súborov** (File Manager)
2. Nájdite stiahnutý APK súbor
3. Kliknite na neho
4. Ak sa zobrazí "Inštalácia blokovaná":
   - Kliknite na **Nastavenia**
   - Povoľte **Inštalovať neznáme aplikácie** pre Správcu súborov
   - Vráťte sa späť a skúste znova
5. Kliknite **Inštalovať**
6. Počkajte na dokončenie
7. Kliknite **Hotovo** alebo **Otvoriť**

---

## 5. Prvé spustenie

### Krok 5.1: Spustenie aplikácie

1. Nájdite ikonu **TwitchDropsMiner** v zozname aplikácií
2. Kliknite na ňu

### Krok 5.2: Získanie OAuth tokenu

**Metóda 1: Twitch Token Generator (Najjednoduchšie)**

1. Na počítači otvorte: https://twitchtokengenerator.com/
2. Kliknite na **"Custom Scope Token"**
3. **NEVYBERAJTE ŽIADNE SCOPES** (nechajte všetko prázdne)
4. Kliknite **"Generate Token!"**
5. Prihláste sa na Twitch (ak nie ste)
6. Autorizujte aplikáciu
7. Skopírujte vygenerovaný token (začína `oauth:`)
8. Pošlite si ho na telefón (email, poznámky, atď.)
9. V aplikácii vložte token do poľa
10. Kliknite **"Login"**

**Metóda 2: Z Twitch cookies (Pokročilé)**

1. Na počítači otvorte https://twitch.tv
2. Prihláste sa
3. Stlačte **F12** (Developer Tools)
4. Prejdite na záložku **Application** (alebo **Storage**)
5. V ľavom menu: **Cookies** > **https://www.twitch.tv**
6. Nájdite cookie s názvom **"auth-token"**
7. Skopírujte jeho hodnotu
8. Pridajte pred ňu `oauth:` (napr. `oauth:abc123xyz...`)
9. Vložte do aplikácie

### Krok 5.3: Prvé spustenie miningu

1. Po úspešnom prihlásení sa zobrazí hlavná obrazovka
2. Kliknite na **"Start"**
3. Aplikácia:
   - Načíta vaše kampane
   - Vyberie najlepší kanál
   - Začne mining

4. Sledujte progress na hlavnej obrazovke

### Krok 5.4: Kontrola inventára

1. Kliknite na **"Inventory"**
2. Uvidíte zoznam všetkých kampaní
3. Pre každú kampaň vidíte:
   - Názov kampane
   - Hru
   - Progress (koľko dropov ste získali)

---

## 6. Riešenie problémov

### Problém: Buildozer zlyhá pri zostavení

**Riešenie 1: Vyčistite cache**
```bash
buildozer android clean
rm -rf .buildozer
buildozer android debug
```

**Riešenie 2: Skontrolujte JAVA_HOME**
```bash
echo $JAVA_HOME
# Malo by byť: /usr/lib/jvm/java-17-openjdk-amd64

# Ak nie je nastavené:
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH=$PATH:$JAVA_HOME/bin
```

**Riešenie 3: Aktualizujte buildozer**
```bash
pip install --upgrade buildozer cython
```

### Problém: ADB nevidí zariadenie

**Riešenie 1: Reštartujte ADB server**
```bash
adb kill-server
adb start-server
adb devices
```

**Riešenie 2: Skontrolujte USB kábel**
- Použite originálny kábel
- Skúste iný USB port
- Skúste režim "File Transfer" namiesto "Charging only"

**Riešenie 3: Pravidlá udev (Linux)**
```bash
# Vytvorte udev pravidlo
sudo nano /etc/udev/rules.d/51-android.rules

# Pridajte (nahraďte XXXX vendor ID vášho telefónu):
SUBSYSTEM=="usb", ATTR{idVendor}=="XXXX", MODE="0666", GROUP="plugdev"

# Reštartujte udev
sudo udevadm control --reload-rules
sudo udevadm trigger
```

### Problém: Aplikácia crashuje pri spustení

**Riešenie 1: Skontrolujte logy**
```bash
# Pripojte telefón cez USB
adb logcat | grep python

# Alebo uložte logy do súboru
adb logcat > logcat.txt
```

**Riešenie 2: Reinstalujte aplikáciu**
```bash
adb uninstall com.twitchdropsminer.twitchdropsminer
adb install bin/twitchdropsminer-*.apk
```

**Riešenie 3: Vyčistite dáta aplikácie**
- Nastavenia > Aplikácie > TwitchDropsMiner
- Vymazať dáta
- Vymazať cache

### Problém: Mining nefunguje

**Kontrola 1: Overenie prihlásenia**
- Skontrolujte, či ste prihlásený
- Skúste sa odhlásiť a prihlásiť znova
- Overte token na twitchtokengenerator.com

**Kontrola 2: Kampane**
- Prejdite na https://twitch.tv/drops/campaigns
- Overte, že máte aktívne kampane
- Skontrolujte, či je váš účet prepojený s hrami

**Kontrola 3: Internet**
- Skontrolujte pripojenie
- Skúste reštartovať WiFi
- Overte, že aplikácia má povolený prístup k internetu

### Problém: Drops sa nezískavajú

**Riešenie 1: Manuálna kontrola**
- Otvorte https://twitch.tv/drops/inventory
- Skontrolujte, či sa progress zvyšuje
- Ak nie, problém je na strane Twitch

**Riešenie 2: Reštart miningu**
- Kliknite "Stop"
- Počkajte 5 sekúnd
- Kliknite "Start"

**Riešenie 3: Reštart aplikácie**
- Zatvorte aplikáciu úplne
- Vyčistite z nedávnych aplikácií
- Spustite znova

### Problém: Vysoká spotreba batérie

**Riešenie:**
1. Nastavenia > Batéria
2. Nájdite TwitchDropsMiner
3. Nastavte na "Neobmedzované" (Unrestricted)
4. Alebo použite mining len pri nabíjaní

### Problém: Aplikácia sa zastaví v pozadí

**Riešenie:**
1. Nastavenia > Aplikácie > TwitchDropsMiner
2. Batéria > Neobmedzované
3. Vypnite "Optimalizácia batérie"
4. Povoľte "Spustenie na pozadí"

---

## Dodatočné tipy

### Optimalizácia výkonu

1. **Povoľte režim vývojára:**
   - Nastavenia > O telefóne > 7x klik na Číslo zostavy
   - Vývojárske možnosti > Neponechávať aktivity
   - Vypnite túto možnosť

2. **Zakážte úsporu batérie:**
   - Nastavenia > Batéria > TwitchDropsMiner
   - Nastavte na "Neobmedzované"

3. **Pridajte do výnimiek:**
   - Nastavenia > Aplikácie > TwitchDropsMiner
   - Oprávnenia > Povoľte všetky

### Aktualizácia aplikácie

```bash
# Zostavte novú verziu
cd ~/android-projects/TwitchDropsMiner_Android
source ~/android-projects/buildozer-env/bin/activate
buildozer android debug

# Odinštalujte starú verziu
adb uninstall com.twitchdropsminer.twitchdropsminer

# Nainštalujte novú
adb install bin/twitchdropsminer-*.apk
```

### Zálohovanie nastavení

Nastavenia sú uložené v:
```
/data/data/com.twitchdropsminer.twitchdropsminer/files/.twitch_drops_android/
```

Pre zálohu:
```bash
adb pull /sdcard/Android/data/com.twitchdropsminer.twitchdropsminer/
```

---

## Kontakt a podpora

- **GitHub Issues**: Pre nahlásenie chýb
- **Discord**: Pre diskusiu a pomoc
- **Email**: Pre súkromné otázky

---

**Úspešné zostavenie a používanie! 🎉**
