#!/bin/bash
# Install script for TwitchDropsMiner Android

set -e

echo "=========================================="
echo "TwitchDropsMiner Android - Install Script"
echo "=========================================="
echo ""

# Check if adb is installed
if ! command -v adb &> /dev/null; then
    echo "❌ ADB is not installed!"
    echo "Install it with: sudo apt install adb"
    exit 1
fi

echo "✓ ADB found"

# Check for APK file
APK_FILE=$(ls bin/*.apk 2>/dev/null | head -n 1)

if [ -z "$APK_FILE" ]; then
    echo "❌ No APK file found in bin/"
    echo "Build the app first with: ./build.sh"
    exit 1
fi

echo "✓ APK found: $APK_FILE"
echo ""

# Check for connected devices
echo "Checking for connected devices..."
adb devices

DEVICE_COUNT=$(adb devices | grep -w "device" | wc -l)

if [ "$DEVICE_COUNT" -eq 0 ]; then
    echo "❌ No devices connected!"
    echo ""
    echo "Connect your device and enable USB debugging:"
    echo "  1. Go to Settings > About phone"
    echo "  2. Tap 'Build number' 7 times"
    echo "  3. Go to Settings > Developer options"
    echo "  4. Enable 'USB debugging'"
    exit 1
fi

echo "✓ Device connected"
echo ""

# Install APK
echo "📱 Installing APK..."
adb install -r "$APK_FILE"

echo ""
echo "=========================================="
echo "✅ Installation complete!"
echo "=========================================="
echo ""
echo "You can now launch TwitchDropsMiner on your device"
echo ""
