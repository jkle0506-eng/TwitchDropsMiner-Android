# TwitchDropsMiner - Android Version

Automatický miner pre Twitch Drops na Android zariadenia.

## Funkcie

- ✅ Automatické sledovanie streamov pre získavanie dropov
- ✅ Podpora viacerých kampaní súčasne
- ✅ Automatické claimovanie dropov
- ✅ Notifikácie pri získaní dropu
- ✅ Prehľad inventára a kampaní
- ✅ Nastaviteľné priority hier
- ✅ Websocket pripojenie pre real-time updates
- ✅ Tmavý režim UI

## Požiadavky

### Pre zostavenie (Build)

- Linux (Ubuntu 20.04+ odporúčané) alebo WSL2 na Windows
- Python 3.9+
- Buildozer
- Android SDK a NDK (automaticky stiahne buildozer)
- Minimálne 8GB RAM
- Minimálne 20GB voľného miesta na disku

### Pre spustenie na Android

- Android 5.0 (API 21) alebo vyšší
- Minimálne 100MB voľného miesta
- Internetové pripojenie

## Inštalácia a zostavenie

### 1. Príprava prostredia (Linux/WSL2)

```bash
# Aktualizácia systému
sudo apt update
sudo apt upgrade -y

# Inštalácia závislostí
sudo apt install -y \
    python3-pip \
    python3-venv \
    git \
    zip \
    unzip \
    openjdk-17-jdk \
    autoconf \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    libffi-dev \
    libssl-dev \
    automake

# Nastavenie JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH=$PATH:$JAVA_HOME/bin
```

### 2. Inštalácia Buildozer

```bash
# Vytvorenie virtuálneho prostredia
python3 -m venv venv
source venv/bin/activate

# Inštalácia buildozer
pip install --upgrade pip
pip install buildozer
pip install cython==0.29.36

# Overenie inštalácie
buildozer --version
```

### 3. Príprava projektu

```bash
# Prejdite do priečinka projektu
cd TwitchDropsMiner_Android

# Inicializácia buildozer (ak ešte nie je buildozer.spec)
# buildozer init

# Prvé zostavenie (trvá 30-60 minút)
buildozer android debug
```

### 4. Zostavenie APK

```bash
# Debug verzia (pre testovanie)
buildozer android debug

# Release verzia (pre distribúciu)
buildozer android release

# APK súbor bude v priečinku: bin/
# Názov: twitchdropsminer-1.0.0-arm64-v8a-debug.apk
```

### 5. Inštalácia na zariadenie

#### Cez USB (ADB)

```bash
# Povoľte USB debugging na Android zariadení
# Nastavenia > O telefóne > Kliknite 7x na "Číslo zostavy"
# Nastavenia > Možnosti pre vývojárov > USB ladenie (zapnúť)

# Inštalácia cez ADB
sudo apt install -y adb
adb devices  # Overte, že zariadenie je pripojené
adb install bin/twitchdropsminer-1.0.0-arm64-v8a-debug.apk
```

#### Cez súbor

1. Skopírujte APK súbor z `bin/` priečinka na telefón
2. Otvorte súbor na telefóne
3. Povoľte inštaláciu z neznámych zdrojov (ak sa zobrazí)
4. Kliknite na "Inštalovať"

## Použitie

### 1. Prvé spustenie

1. Spustite aplikáciu "TwitchDropsMiner"
2. Zobrazí sa prihlasovacia obrazovka

### 2. Získanie OAuth tokenu

**Metóda 1: Twitch Token Generator (Odporúčané)**

1. Otvorte v prehliadači: https://twitchtokengenerator.com/
2. Kliknite na "Custom Scope Token"
3. Nevyberajte žiadne scopes (nechajte prázdne)
4. Kliknite "Generate Token"
5. Skopírujte vygenerovaný token (začína "oauth:")
6. Vložte token do aplikácie

**Metóda 2: Manuálne z cookies**

1. Prihláste sa na twitch.tv v prehliadači
2. Otvorte Developer Tools (F12)
3. Prejdite na Application/Storage > Cookies > https://twitch.tv
4. Nájdite cookie s názvom "auth-token"
5. Skopírujte hodnotu
6. Vložte do aplikácie

### 3. Spustenie miningu

1. Po prihlásení sa zobrazí hlavná obrazovka
2. Kliknite na "Start" pre spustenie miningu
3. Aplikácia automaticky:
   - Načíta dostupné kampane
   - Vyberie najlepší kanál
   - Začne sledovať a získavať drops
   - Automaticky claimne drops po dokončení

### 4. Navigácia

- **Home**: Hlavná obrazovka s aktuálnym stavom
- **Inventory**: Prehľad kampaní a dropov
- **Channels**: Zoznam sledovaných kanálov
- **Settings**: Nastavenia aplikácie
- **Logs**: História udalostí

### 5. Nastavenia

- **Auto Claim Drops**: Automatické claimovanie dropov
- **Notifications**: Notifikácie pri získaní dropu
- **Logout**: Odhlásenie z účtu

## Riešenie problémov

### Aplikácia sa nezostavia

```bash
# Vyčistite build cache
buildozer android clean

# Odstráňte .buildozer priečinok
rm -rf .buildozer

# Skúste znova
buildozer android debug
```

### Chyba pri inštalácii na zariadenie

- Skontrolujte, či máte povolenú inštaláciu z neznámych zdrojov
- Skúste odinštalovať starú verziu aplikácie
- Reštartujte zariadenie

### Aplikácia crashuje pri spustení

- Skontrolujte logy: `adb logcat | grep python`
- Overte, že máte správny OAuth token
- Skontrolujte internetové pripojenie

### Mining nefunguje

- Overte, že ste prihlásený
- Skontrolujte, či máte aktívne kampane
- Overte, že váš Twitch účet je prepojený s hrami
- Skontrolujte logy v aplikácii

### Drops sa nezískavajú

- Overte na twitch.tv/drops/inventory, či sa drops získavajú
- Skontrolujte, či je kanál online
- Overte, že kanál má zapnuté drops
- Reštartujte mining (Stop > Start)

## Technické detaily

### Architektúra

```
TwitchDropsMiner_Android/
├── main.py                 # Hlavný vstupný bod
├── core/                   # Jadro aplikácie
│   ├── twitch_client.py   # Twitch API klient
│   ├── websocket_client.py # WebSocket pripojenie
│   ├── inventory.py       # Správa dropov a kampaní
│   ├── channel.py         # Správa kanálov
│   ├── settings.py        # Nastavenia
│   ├── utils.py           # Pomocné funkcie
│   ├── constants.py       # Konštanty
│   └── exceptions.py      # Výnimky
├── ui/                    # Používateľské rozhranie
│   └── screens.py         # Kivy obrazovky
├── assets/                # Zdroje (obrázky, jazyky)
├── buildozer.spec         # Konfigurácia zostavenia
└── requirements.txt       # Python závislosti
```

### Použité technológie

- **Kivy**: Cross-platform UI framework
- **KivyMD**: Material Design komponenty
- **aiohttp**: Asynchrónne HTTP requesty
- **asyncio**: Asynchrónne programovanie
- **Buildozer**: Android build nástroj

### API Endpointy

- GraphQL: `https://gql.twitch.tv/gql`
- WebSocket: `wss://pubsub-edge.twitch.tv/v1`

## Bezpečnosť

- OAuth token je uložený lokálne v zariadení
- Komunikácia s Twitch API je šifrovaná (HTTPS/WSS)
- Aplikácia nepožaduje žiadne nebezpečné oprávnenia
- Nezbiera žiadne osobné údaje

## Licencia

Tento projekt je open-source a je poskytovaný "ako je" bez akejkoľvek záruky.

## Podpora

Pre problémy a otázky vytvorte issue na GitHub repozitári.

## Changelog

### v1.0.0 (2024)
- Prvé vydanie Android verzie
- Základné funkcie miningu
- UI s Material Design
- Podpora pre Android 5.0+

## Poznámky

- Aplikácia musí bežať na popredí alebo v pozadí pre získavanie dropov
- Odporúčame povoliť "Neobmedzovať batériu" pre aplikáciu
- Mining môže spotrebovať dáta (cca 10-50MB/hod)
- Aplikácia neemuluje sledovanie videa, len posiela watch eventy

## Budúce vylepšenia

- [ ] Podpora pre viacero účtov
- [ ] Plánovač (automatické spustenie/zastavenie)
- [ ] Štatistiky (získané drops, čas sledovania)
- [ ] Exportovanie logov
- [ ] Tmavý/svetlý režim prepínač
- [ ] Podpora pre viac jazykov
- [ ] Widget na domovskú obrazovku
- [ ] Background service (mining v pozadí)

---

**Vyrobené s ❤️ pre Twitch komunitu**
