# USMLE Question ID Converter

[![AnkiWeb](https://img.shields.io/badge/AnkiWeb-699193084-blue)](https://ankiweb.net/shared/info/699193084)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.2.1-green)](https://github.com/abdmohrat/usmle-question-id-converter/releases)
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/abdmohrat)

Convert USMLE question IDs to Anki search queries instantly! Perfect for medical students using UWorld question banks with the **AnKing_v12 deck** from AnkiHub.

## 📺 Demo Video

https://github.com/user-attachments/assets/147e24bd-d391-4760-a06a-459201630bf5

**Complete workflow:** Copy question IDs from USMLEPREPS → Paste in addon → Search in Anki!

## 🎉 What's New in v1.2.1

### Major Update with 5 New Features!

- 🎉 **Batch Processing** - Load question IDs from text/CSV files
- 📋 **Quick Actions** - Right-click cards in Anki Browser to extract question IDs
- ⚙️ **Custom Patterns** - Define your own tag patterns for any deck structure
- 🧠 **Smart Input** - Accepts IDs in any format (comma, space, newline, tab)
- 📊 **History Tracker** - View your last 20 conversions with timestamps
- 🎨 **Dark Mode Support** - Perfect visibility in both light and dark themes

## 🚀 Features

### Core Features
- ✅ **Step 1, Step 2 & Step 3 Support** - Choose between USMLE Step 1, Step 2, or Step 3 tags
- ✅ **Smart Memory** - Remembers your last step selection  
- ✅ **Auto-conversion** - Converts IDs as you type
- ✅ **Multiple Actions** - Copy to clipboard or search directly in Anki
- ✅ **Clean Interface** - Simple, intuitive design
- ✅ **Error Handling** - Filters out invalid characters automatically

### New in v1.2.0+
- 📁 **File Import** - Load IDs from .txt or .csv files for batch processing
- 🎯 **Browser Context Menu** - Right-click on UWorld cards to extract question IDs
- ⚙️ **Custom Tag Patterns** - Use with any deck, not just AnKing_v12!
- 🔄 **Flexible Input** - Paste IDs in any format: comma, space, newline, or tab-separated
- 📊 **Conversion History** - Track your last 20 conversions with dates and counts
- 📈 **Live Stats** - See ID count in real-time as you type
- ✨ **Enhanced UI** - Larger dialog (850x550) with better visual feedback

## 📸 Screenshots

### Main Interface
![Main Interface](images/main-interface.png)
*Convert multiple question IDs at once - auto-conversion as you type*

### Search Results in Anki
![Anki Browser Results](images/anki-browser-results.png)
*One-click search opens Anki browser with your target questions*

## ⚠️ Requirements

- **Anki Version**: 2.1.66 or later
- **Deck**: Works with [AnKing_v12 deck](https://www.ankihub.net/) by default
- **Custom Decks**: Configure your own tag patterns for any deck!

## 📥 Installation

### Install from AnkiWeb
1. Open Anki → **Tools** → **Add-ons** → **Get Add-ons**
2. Paste this code: **699193084**
3. Restart Anki

## 🔧 Usage

### Quick Start with USMLEPREPS

1. **In USMLEPREPS**: 
   - Go to "My Tests"
   - Click the 3-dot menu (⋮) on your test
   - Select "Share Test"
   - Click "Copy All IDs"

2. **In Anki**:
   - Open: Tools → USMLE Question ID Converter
   - Select your step (Step 1, 2, or 3)
   - Paste the IDs (Ctrl+V / Cmd+V) - any format works!
   - Click "Search in Anki"
   - Done! 🎉

### Manual Usage

1. **Open the converter**: Tools → USMLE Question ID Converter
2. **Select your step**: Choose Step 1, Step 2, or Step 3 (saved for next time)
3. **Input IDs** (choose one):
   - Paste directly (comma, space, or newline-separated)
   - Click "📁 Load from File" to import from .txt or .csv
4. **Get results**: Copy the search query or search directly in Anki

### New Features Guide

#### 📁 Batch Processing
1. Create a text file with your IDs (any format)
2. Click "📁 Load from File"
3. Select your file
4. IDs automatically load and convert!

#### 📋 Extract IDs from Cards
1. Open Anki Browser
2. Select UWorld cards
3. Right-click → "📋 Copy UWorld Question ID(s)"
4. IDs copied to clipboard!

#### ⚙️ Custom Tag Patterns
1. Click "⚙️ Custom Patterns"
2. Define your pattern: `tag:#MyDeck::#UWorld::{ID}`
3. Test with sample ID
4. Save and use with any deck!

#### 📊 View History
1. Click "📊 History"
2. See all your past conversions
3. Review timestamps and counts
4. Clear history anytime

### Input Format Examples

The addon now accepts **any format**:

```
Comma-separated:    21656, 19263, 4466
Space-separated:    21656 19263 4466
Newline-separated:  21656
                    19263
                    4466
Tab-separated:      21656	19263	4466
Mixed format:       21656, 19263
                    4466
                    12477    4288
```

All formats work perfectly! 🎉

### Output Examples

**Step 2 Output:**
```
tag:#AK_Step2_v12::#UWorld::Step::21656 OR tag:#AK_Step2_v12::#UWorld::Step::19263 OR tag:#AK_Step2_v12::#UWorld::Step::4466
```

**Step 3 Output:**
```
tag:#AK_Step3_v12::#UWorld::21656 OR tag:#AK_Step3_v12::#UWorld::19263 OR tag:#AK_Step3_v12::#UWorld::4466
```

**Custom Pattern Output** (example):
```
tag:#MyDeck::Q21656 OR tag:#MyDeck::Q19263 OR tag:#MyDeck::Q4466
```

## 🎯 Perfect For

- Medical students using the **AnKing_v12** deck
- **USMLEPREPS** users who want quick Anki integration
- **UWorld** question bank Users
- **Step 1, Step 2, and Step 3** preparation
- **Custom decks** with personalized tag patterns
- **Batch processing** weekly review lists
- Quick access to specific question cards in Anki

## 🐛 Bug Reports & Feature Requests

Found a bug or have a suggestion? Please [open an issue](https://github.com/abdmohrat/usmle-question-id-converter/issues)!

## 📝 Changelog

### v1.2.1 (Latest - October 2025)
- 🎨 Fixed Custom Patterns test result visibility in dark mode
- ✨ Test result box now adapts to Anki's theme automatically

### v1.2.0 (Major Update - October 2025)
- 🎉 **Batch Processing**: Load question IDs from text/CSV files
- 📋 **Quick Actions**: Right-click cards in browser to extract question IDs
- ⚙️ **Custom Patterns**: Define your own tag patterns for any deck
- 🧠 **Smart Input**: Accepts IDs in any format (comma, space, newline, tab)
- 📊 **History Tracker**: View your last 20 conversions with timestamps
- ✨ **Better UI**: Live ID counter, status messages, improved layout
- 🚀 **Dialog Size**: Increased to 850x550 for better workflow
- 💾 **New Config**: Stores custom patterns and conversion history

### v1.1.1
- 🐛 Fixed Rate Addon button not opening review page
- 🎨 Moved support buttons to top-right corner for better layout
- 📏 Increased button widths to prevent text cutoff
- 📐 Improved dialog size (800x480) for better spacing

### v1.1.0
- ✨ Added Step 3 support
- 🎯 Now supports all three USMLE steps
- 💾 Remembers Step 3 selection

### v1.0.2
- 🎨 Redesigned support button: "☕ Buy Me a Coffee"
- ⭐ Added "Rate Addon" button
- ✨ Beautiful hover and press effects on buttons
- 🐛 Fixed support button not opening browser

### v1.0.1
- ✨ Added Ko-fi support button
- 🎨 Improved dialog layout
- 💙 Support development directly from addon

### v1.0.0 (Initial Release)
- 🚀 Convert question IDs to Anki search queries
- ⚡ Support for Step 1 and Step 2
- 💾 Memory feature for step selection
- ⌨️ Auto-conversion as you type
- 📋 Copy to clipboard functionality
- 🔍 Direct Anki search integration

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Feel free to:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 💝 Support

If this addon helped you with your USMLE studies, consider:
- ⭐ **Starring this repository**
- 📝 **[Rating it on AnkiWeb](https://ankiweb.net/shared/review/699193084)**
- ☕ **[Buying me a coffee](https://ko-fi.com/abdmohrat)** to support development
- 🐛 **Reporting bugs or suggesting features**
- 📢 **Sharing with fellow medical students**

## 🙏 Acknowledgments

Thanks to:
- The AnKing team for their amazing AnKing_v12 deck
- The medical student community for feedback and support

---

*Made with ❤️ for the medical student community*

**Happy Studying! 📚🩺**
