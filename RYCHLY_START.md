# TwitchDropsMiner Android - Rýchly štart

## 🎯 Čo som dostal?

Kompletne prepísanú Android verziu TwitchDropsMiner aplikácie s:

✅ **Plne funkčný kód** - Všetky moduly prepísané pre Android
✅ **Kivy/KivyMD UI** - Moderné Material Design rozhranie  
✅ **Asynchrónna architektúra** - Efektívne spracovanie
✅ **Websocket podpora** - Real-time updates
✅ **Automatické claimovanie** - Drops sa claimujú automaticky
✅ **Notifikácie** - Upozornenia pri získaní dropu
✅ **Kompletná dokumentácia** - Návody v slovenčine

## 📁 Štruktúra projektu

```
TwitchDropsMiner_Android/
├── main.py                    # Hlavný vstupný bod aplikácie
├── buildozer.spec             # Konfigurácia pre Android build
├── requirements.txt           # Python závislosti
├── README.md                  # Prehľad projektu (anglicky)
├── INSTALL_GUIDE.md          # Detailný návod (anglicky)
├── RYCHLY_START.md           # Tento súbor
├── build.sh                   # Skript na zostavenie APK
├── install.sh                 # Skript na inštaláciu na zariadenie
│
├── core/                      # Jadro aplikácie
│   ├── twitch_client.py      # Hlavný Twitch klient
│   ├── websocket_client.py   # WebSocket pripojenie
│   ├── inventory.py          # Správa dropov a kampaní
│   ├── channel.py            # Správa kanálov
│   ├── settings.py           # Nastavenia aplikácie
│   ├── utils.py              # Pomocné funkcie
│   ├── constants.py          # Konštanty a GQL operácie
│   └── exceptions.py         # Vlastné výnimky
│
├── ui/                        # Používateľské rozhranie
│   └── screens.py            # Všetky obrazovky (Home, Login, atď.)
│
└── assets/                    # Zdroje
    ├── images/               # Obrázky (ikony, atď.)
    └── lang/                 # Jazykové súbory
```

## 🚀 Ako začať (3 kroky)

### 1️⃣ Príprava (Linux/WSL2)

```bash
# Nainštalujte základné nástroje
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git openjdk-17-jdk

# Vytvorte virtuálne prostredie
python3 -m venv buildozer-env
source buildozer-env/bin/activate

# Nainštalujte buildozer
pip install buildozer cython==0.29.36
```

### 2️⃣ Zostavenie APK

```bash
# Prejdite do priečinka projektu
cd TwitchDropsMiner_Android

# Spustite build (trvá 30-60 minút pri prvom spustení)
./build.sh

# Alebo manuálne:
buildozer android debug
```

### 3️⃣ Inštalácia na telefón

**Cez USB:**
```bash
# Povoľte USB debugging na telefóne
# Nastavenia > O telefóne > 7x klik na "Číslo zostavy"
# Nastavenia > Vývojárske možnosti > USB ladenie (zapnúť)

# Pripojte telefón a nainštalujte
./install.sh
```

**Cez súbor:**
1. Skopírujte `bin/twitchdropsminer-*.apk` na telefón
2. Otvorte súbor na telefóne
3. Povoľte inštaláciu z neznámych zdrojov
4. Nainštalujte

## 📱 Prvé použitie

1. **Spustite aplikáciu** na telefóne
2. **Získajte OAuth token:**
   - Otvorte: https://twitchtokengenerator.com/
   - Kliknite "Custom Scope Token"
   - Nevyberajte žiadne scopes
   - Vygenerujte token
   - Skopírujte ho
3. **Prihláste sa** v aplikácii s tokenom
4. **Kliknite "Start"** a aplikácia začne mining

## 🎨 Funkcie aplikácie

### Hlavná obrazovka (Home)
- Aktuálny stav miningu
- Sledovaný kanál
- Progress aktuálneho dropu
- Tlačidlá Start/Stop

### Inventár (Inventory)
- Zoznam všetkých kampaní
- Progress každej kampane
- Počet získaných dropov

### Kanály (Channels)
- Zoznam sledovaných kanálov
- Stav kanálov (online/offline)

### Nastavenia (Settings)
- Automatické claimovanie
- Notifikácie
- Odhlásenie

### Logy (Logs)
- História udalostí
- Chybové hlásenia
- Debug informácie

## 🔧 Technické detaily

### Použité technológie
- **Kivy 2.3.0** - Cross-platform UI framework
- **KivyMD 1.2.0** - Material Design komponenty
- **aiohttp** - Asynchrónne HTTP requesty
- **asyncio** - Asynchrónne programovanie
- **Buildozer** - Android build nástroj

### Ako to funguje

1. **Prihlásenie:** Overenie OAuth tokenu cez Twitch API
2. **Načítanie kampaní:** Stiahnutie aktívnych drops kampaní
3. **Výber kanála:** Automatický výber najlepšieho kanála
4. **Mining:** Pravidelné posielanie "watch" eventov (každých 20s)
5. **Progress tracking:** WebSocket pripojenie pre real-time updates
6. **Claimovanie:** Automatické claimovanie dokončených dropov

### API Endpointy
- **GraphQL:** `https://gql.twitch.tv/gql`
- **WebSocket:** `wss://pubsub-edge.twitch.tv/v1`

## 📖 Dokumentácia

- **README.md** - Prehľad projektu, funkcie, základné použitie
- **INSTALL_GUIDE.md** - Detailný návod na inštaláciu krok za krokom
- **RYCHLY_START.md** - Tento súbor, rýchly prehľad

## ❓ Časté problémy

### Build zlyhá
```bash
buildozer android clean
rm -rf .buildozer
buildozer android debug
```

### ADB nevidí telefón
```bash
adb kill-server
adb start-server
adb devices
```

### Aplikácia crashuje
```bash
# Pozrite logy
adb logcat | grep python

# Reinstalujte
adb uninstall com.twitchdropsminer.twitchdropsminer
adb install bin/*.apk
```

### Mining nefunguje
- Skontrolujte OAuth token
- Overte kampane na twitch.tv/drops/campaigns
- Reštartujte mining (Stop > Start)

## 🎯 Čo ďalej?

### Odporúčané nastavenia na telefóne:
1. **Batéria:** Nastavte aplikáciu na "Neobmedzované"
2. **Pozadie:** Povoľte spustenie na pozadí
3. **Notifikácie:** Povoľte notifikácie

### Testovanie:
1. Spustite mining
2. Sledujte logy
3. Overte progress na twitch.tv/drops/inventory
4. Počkajte na prvý drop

### Vylepšenia (budúce):
- Background service (mining v pozadí)
- Viacero účtov
- Štatistiky
- Plánovač
- Widget

## 📞 Podpora

Ak máte problémy:
1. Prečítajte si **INSTALL_GUIDE.md**
2. Skontrolujte logy v aplikácii
3. Použite `adb logcat` pre detailné logy

## ✅ Checklist

- [ ] Nainštaloval som závislosti
- [ ] Zostavil som APK
- [ ] Nainštaloval som na telefón
- [ ] Získal som OAuth token
- [ ] Prihlásil som sa
- [ ] Spustil som mining
- [ ] Funguje to! 🎉

---

**Vytvorené s ❤️ pre Twitch komunitu**

*Verzia: 1.0.0 | Dátum: 2024*
