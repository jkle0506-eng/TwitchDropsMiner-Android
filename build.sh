#!/bin/bash
# Build script for TwitchDropsMiner Android

set -e

echo "=========================================="
echo "TwitchDropsMiner Android - Build Script"
echo "=========================================="
echo ""

# Check if buildozer is installed
if ! command -v buildozer &> /dev/null; then
    echo "❌ Buildozer is not installed!"
    echo "Install it with: pip install buildozer"
    exit 1
fi

echo "✓ Buildozer found"

# Check if in virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Warning: Not in a virtual environment"
    echo "It's recommended to use a virtual environment"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Clean previous builds if requested
if [ "$1" == "clean" ]; then
    echo "🧹 Cleaning previous builds..."
    buildozer android clean
    rm -rf .buildozer
    echo "✓ Clean complete"
    echo ""
fi

# Build type
BUILD_TYPE="${1:-debug}"

if [ "$BUILD_TYPE" == "release" ]; then
    echo "🔨 Building RELEASE version..."
    buildozer android release
else
    echo "🔨 Building DEBUG version..."
    buildozer android debug
fi

echo ""
echo "=========================================="
echo "✅ Build complete!"
echo "=========================================="
echo ""
echo "APK location: bin/"
ls -lh bin/*.apk 2>/dev/null || echo "No APK found"
echo ""
echo "To install on device:"
echo "  adb install bin/*.apk"
echo ""
