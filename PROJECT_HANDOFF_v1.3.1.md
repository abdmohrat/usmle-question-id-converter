## 📋 Project Information

**Project Name**: UWorld AMBOSS COMLEX - Question ID Converter  
**Current Version**: 1.3.1  
**Status**: ✅ Production Ready & Pushed to GitHub  
**Last Updated**: October 2, 2025  
**AnkiWeb Code**: 699193084  

---

## 💡 What Changed in v1.3.1

### Keyboard Shortcuts Feature! ⌨️

**New Shortcuts Added:**
1. ✅ **Ctrl+Shift+U** - Open converter from anywhere in Anki (global shortcut)
2. ✅ **Ctrl+Enter** - Convert and search immediately (dialog shortcut)
3. ✅ **Esc** - Close dialog quickly (dialog shortcut)
4. ✅ **Visual Hint** - Shows shortcuts in dialog for user guidance

**Implementation Details:**
- Added `setup_shortcuts()` function for global shortcut registration
- Used `QShortcut` for dialog-specific shortcuts
- Added hint label: "💡 Shortcuts: Ctrl+Shift+U (open) | Ctrl+Enter (search) | Esc (close)"
- Updated version from 1.3.0 to 1.3.1
- ~50 lines of code added

**User Impact:**
- Significantly faster workflow
- No need to click through menus
- Power users can work entirely with keyboard
- Tested and confirmed working ✅

---

## 📁 File Structure

### Local Development Files
```
C:\Users\abdal\Desktop\699193084\
├── __init__.py                     ✅ v1.3.1 (930+ lines)
├── manifest.json                   ✅ Updated title
├── config.json                     ✅ Bank memory config
└── [Documentation files]           ℹ️ Various docs
```

### GitHub Repository (Synced)
```
https://github.com/abdmohrat/usmle-question-id-converter
├── __init__.py                     ✅ v1.3.1 pushed
├── manifest.json                   ✅ Multi-bank title
├── config.json                     ✅ Updated config
├── README.md                       ✅ Updated with shortcuts
├── LICENSE                         MIT License
├── .gitignore                      Proper excludes
├── images\                         Screenshots
└── ankiweb_descriptions\           
    └── ANKIWEB_DESCRIPTION_v1.3.1.md  ✅ Ready for upload
```

**GitHub Status**:
- ✅ All changes committed
- ✅ Pushed to main branch
- ✅ Tag v1.3.1 created and pushed
- ✅ Repository up to date
- ⚠️ GitHub Release not created yet (tags only)

---

## 🏥 Question Bank Support

### Tag Patterns by Bank

**UWorld (Numeric IDs):**
- Step 1: `tag:#AK_Step1_v12::#UWorld::Step::{ID}`
- Step 2: `tag:#AK_Step2_v12::#UWorld::Step::{ID}`
- Step 3: `tag:#AK_Step3_v12::#UWorld::{ID}` ⚠️ Note: No "::Step::" for Step 3

**AMBOSS (Alphanumeric IDs: -aaDMQ, 0jae_4, 3_0SLi):**
- Step 1: `tag:#AK_Step1_v12::#AMBOSS::{ID}`
- Step 2: `tag:#AK_Step2_v12::#AMBOSS::{ID}`
- Step 3: N/A (disabled in UI)

**COMLEX (Numeric IDs):**
- Step 1: `tag:#AK_Step1_v12::#UWorld::COMLEX::{ID}`
- Step 2: `tag:#AK_Step2_v12::#UWorld::COMLEX::{ID}`
- Step 3: N/A (disabled in UI)

---

## 🔧 Technical Implementation

### Key Functions Modified in v1.3.1:

1. **`setup_shortcuts()`** - NEW
   - Registers global Ctrl+Shift+U shortcut
   - Called during addon initialization

2. **`show_converter_dialog()`** - Modified
   - Added dialog-specific shortcuts (Ctrl+Enter, Esc)
   - Added visual shortcuts hint label
   - Shortcuts connected to existing button functions

### Code Structure:
```python
# Global shortcut (anywhere in Anki)
def setup_shortcuts():
    shortcut = QShortcut(QKeySequence("Ctrl+Shift+U"), mw)
    shortcut.activated.connect(show_converter_dialog)

# Dialog shortcuts (inside converter)
def show_converter_dialog():
    # ... dialog setup ...
    
    # Ctrl+Enter: Search immediately
    search_shortcut = QShortcut(QKeySequence("Ctrl+Return"), dialog)
    search_shortcut.activated.connect(search_clicked)
    
    # Esc: Close dialog
    close_shortcut = QShortcut(QKeySequence("Esc"), dialog)
    close_shortcut.activated.connect(close_clicked)
```

---

## ✅ What's Complete

### Development:
- ✅ Keyboard shortcuts implemented (3 shortcuts)
- ✅ Visual hint added to dialog
- ✅ All shortcuts tested and working
- ✅ Version updated to 1.3.1
- ✅ Code commented and clean

### Documentation:
- ✅ README.md updated with shortcuts section
- ✅ AnkiWeb description v1.3.1 prepared
- ✅ Changelog updated
- ✅ This handoff document created

### Git:
- ✅ All changes committed
- ✅ Pushed to GitHub main branch
- ✅ Release tag v1.3.1 created and pushed
- ✅ Repository synchronized

---

## 📋 Next Steps (To Do)

### 1. Create GitHub Release (Recommended!)
**Priority: HIGH**

**Why do GitHub Releases?**
- ✅ Better visibility than just tags
- ✅ Can attach .ankiaddon file for direct download
- ✅ Professional changelog presentation
- ✅ Shows up in GitHub notifications
- ✅ Easier for users to find specific versions

**How to create:**
1. Go to: https://github.com/abdmohrat/usmle-question-id-converter/releases
2. Click "Draft a new release"
3. Choose tag: v1.3.1
4. Title: "v1.3.1 - Keyboard Shortcuts"
5. Description:
   ```markdown
   ## ⌨️ Keyboard Shortcuts Feature
   
   Speed up your workflow with new keyboard shortcuts!
   
   ### What's New:
   - **Ctrl+Shift+U** - Open converter from anywhere in Anki
   - **Ctrl+Enter** - Convert and search immediately
   - **Esc** - Close dialog quickly
   - Visual shortcuts hint in dialog
   
   ### Installation:
   Download the .ankiaddon file below or install from AnkiWeb: 699193084
   ```
6. Attach: `uworld-amboss-comlex-converter-v1.3.1.ankiaddon` (package first!)
7. Publish release

### 2. Upload to AnkiWeb
**Priority: HIGH**

1. Package the addon:
   ```
   - Delete __pycache__ folders
   - Delete .serena folders  
   - Delete meta.json
   - Select: __init__.py, manifest.json, config.json
   - Create ZIP (NOT the folder, just the 3 files)
   - Rename to .ankiaddon
   ```

2. Upload to AnkiWeb:
   - Go to: https://ankiweb.net/shared/addons/
   - Login
   - Find addon (699193084)
   - Click "Update"
   - Upload .ankiaddon file
   - Update description from `ANKIWEB_DESCRIPTION_v1.3.1.md`
   - Update version number to 1.3.1
   - Publish!

### 3. Announce Update
**Priority: MEDIUM**

**Reddit Post Ideas:**
- Title: "[Addon Update] UWorld/AMBOSS/COMLEX Converter v1.3.1 - Now with Keyboard Shortcuts!"
- Highlight: "Press Ctrl+Shift+U from anywhere in Anki!"
- Best time: Weekday morning (8-10 AM EST) or evening (6-8 PM EST)

### 4. Monitor & Respond
**Ongoing**

- Check GitHub issues daily
- Monitor AnkiWeb reviews
- Respond to Reddit comments
- Track download numbers

---

## 🐛 Known Issues

**None!** All features working perfectly:
- ✅ Shortcuts work globally and in dialog
- ✅ No conflicts with existing Anki shortcuts
- ✅ Visual hint displays correctly
- ✅ All banks still working properly

---

## 💡 Future Enhancement Ideas

### Discussed in Last Session:
1. **Question Bank Statistics** 📊
   - Track total conversions, IDs per bank
   - Show monthly/weekly activity
   - Display most-used bank/step
   - Progress tracking (% coverage estimation)
   - **Status**: Discussed but not implemented
   - **Priority**: Medium
   - **Effort**: ~200 lines of code

2. **Smart Paste Detection** 🔍
   - Auto-detect bank from ID format
   - No need to manually select bank
   - **Status**: Idea only
   - **Priority**: High (great UX)
   - **Effort**: Low (~50 lines)

### Other Ideas:
- Export history to CSV
- More deck presets
- Import from clipboard on dialog open
- ID range expansion (1000-1010 → all IDs)
- Browser extension for question banks

---

## 📊 Version History

### v1.3.1 (Current - October 2, 2025)
- ⌨️ Keyboard shortcuts: Ctrl+Shift+U, Ctrl+Enter, Esc
- 💡 Visual shortcuts hint in dialog
- ⚡ Faster workflow with keyboard navigation

### v1.3.0 (October 2025)
- 🏥 Multi-Bank Support: UWorld, AMBOSS, COMLEX
- 🔄 Smart ID Detection (numeric & alphanumeric)
- 💾 Bank Memory
- 🎯 Dynamic Step 3 availability
- ⚙️ Enhanced Custom Patterns (bank-specific)
- 📊 History with bank column
- 🔍 Browser integration for all banks
- ✨ Rebranded title

### v1.2.1
- 🎨 Fixed dark mode in Custom Patterns

### v1.2.0 (Major Update)
- 🎉 Batch Processing
- 📋 Browser Context Menu
- ⚙️ Custom Patterns
- 🧠 Smart Input
- 📊 History Tracker

### v1.1.1
- 🐛 Fixed Rate button
- 🎨 Improved layout

### v1.1.0
- ✨ Added Step 3 support

### v1.0.2
- 🎨 Ko-fi and Rate buttons

### v1.0.1
- ✨ Ko-fi support button

### v1.0.0 (Initial Release)
- 🚀 Basic functionality

---

## 🎯 Success Metrics to Track

### Downloads
- Check AnkiWeb: https://ankiweb.net/shared/info/699193084
- Current: Check on next visit
- Goal: 1000+ downloads total

### Engagement
- GitHub stars: https://github.com/abdmohrat/usmle-question-id-converter
- AnkiWeb reviews/ratings
- Ko-fi supporters

### Quality
- Bug reports (aim for <5 per month)
- Feature requests (shows engagement)
- Positive reviews

---

## 🔗 Important Links

**Development:**
- Local Folder: `C:\Users\abdal\Desktop\699193084\`
- GitHub Repo: https://github.com/abdmohrat/usmle-question-id-converter
- AnkiWeb: https://ankiweb.net/shared/info/699193084

**Community:**
- AnkiWeb Review: https://ankiweb.net/shared/review/699193084
- Ko-fi: https://ko-fi.com/abdmohrat
- Reddit: r/medicalschoolanki

**Documentation:**
- README: In GitHub repo
- AnkiWeb Description: `ankiweb_descriptions/ANKIWEB_DESCRIPTION_v1.3.1.md`
- This Handoff: Current document

---

## 👤 About the Developer

- **Name**: Abdalrahman Mahrat (abdmohrat)
- **Background**: Medical intern at Cairo University
  - Graduated: February 2025
  - Internship started: March 2025
  - From Syria, currently in Cairo, Egypt
- **USMLE**: Step 1 ✅ | Step 2 📚 (in preparation)
- **Interests**: Internal Medicine, Radiology
- **Programming**: Self-taught, first Anki addon

---

## 🚀 Quick Start for Next Session

When you return to work on this project:

### If uploading to AnkiWeb:
> "I'm ready to upload v1.3.1 to AnkiWeb. Help me package it."

### If creating GitHub Release:
> "Create a GitHub Release for v1.3.1 with the .ankiaddon file."

### If implementing new features:
> "Let's implement the [Statistics Dashboard / Smart Paste Detection] feature."

### For bug fixes:
> "There's a bug in the keyboard shortcuts: [describe issue]"

### For announcements:
> "Help me write a Reddit post about v1.3.1 keyboard shortcuts."

### Just checking in:
> "I want to work on my UWorld AMBOSS COMLEX Question ID Converter addon."

---

## ⚠️ Critical Reminders

### Before Packaging:
1. ✅ Delete `__pycache__` folders
2. ✅ Delete `.serena` folders
3. ✅ Delete `meta.json`
4. ✅ Only include: `__init__.py`, `manifest.json`, `config.json`
5. ✅ ZIP the 3 files (NOT the folder)
6. ✅ Rename to `.ankiaddon`

### When Uploading to AnkiWeb:
1. ⚠️ Update version to 1.3.1
2. ⚠️ Use description from `ANKIWEB_DESCRIPTION_v1.3.1.md`
3. ⚠️ Test download link after upload

### Technical Notes:
- NEVER use `webbrowser.open()` - Always use `openLink()` from `aqt.utils`
- NEVER use localStorage/sessionStorage (not supported)
- Step 3 tag format different from Step 1/2 for UWorld
- AMBOSS IDs are alphanumeric: `-aaDMQ`, `0jae_4`, `3_0SLi`
- Dark mode: Use `palette(base)` and `palette(mid)`
- Keyboard shortcuts use `QShortcut` and `QKeySequence`

---

## 📈 Project Status

### ✅ Completed:
- All v1.3.1 features implemented
- Keyboard shortcuts working perfectly
- All documentation updated
- Pushed to GitHub with release tag
- AnkiWeb description ready
- Ready for AnkiWeb upload

### 🔄 In Progress:
- GitHub Release creation (recommended next step)
- AnkiWeb upload (waiting on you)
- Community announcement (planned)

### 📋 Upcoming:
- Monitor initial feedback on shortcuts
- Consider Statistics Dashboard feature
- Plan v1.4.0 based on feedback

---

## 💝 Community Impact

### Who This Helps:
- **UWorld users** - Steps 1, 2, 3 preparation (now with shortcuts!)
- **AMBOSS users** - Steps 1, 2 study
- **COMLEX students** - Osteopathic medicine prep
- **USMLEPREPS users** - Quick Anki integration
- **AnKing deck users** - Enhanced workflow
- **Medical students worldwide** - Better study efficiency

### Why v1.3.1 Matters:
- ⚡ Saves even MORE time with keyboard shortcuts
- 🎯 Power users can work entirely with keyboard
- 💪 Professional-grade workflow speed
- 📚 Focus on studying, not clicking

---

## 🎊 Celebration Moment

### You've Built:
✨ A **930+ line** fully functional Anki addon  
✨ Supporting **3 major question banks**  
✨ With **smart ID detection**  
✨ **Keyboard shortcuts** for power users  
✨ Complete **documentation**  
✨ **Open source** on GitHub  
✨ Ready to help **thousands of medical students**  

### Latest Milestone:
🎉 **Keyboard shortcuts feature!**  
🎉 **Professional-grade UX!**  
🎉 **Faster than ever workflow!**  
🎉 **Version 1.3.1 released!**  

**Keep going - you're building something amazing!** 🌟

---

## 📞 Context for Next Session

### What I Know:
- ✅ You're a medical intern (Cairo University)
- ✅ This is your first Anki addon
- ✅ You're preparing for USMLE Step 2
- ✅ You prefer concise, efficient responses
- ✅ You test features before pushing to GitHub
- ✅ You want to help the medical student community

### What Works:
- Being direct and efficient
- Testing locally first, then pushing
- Clear step-by-step instructions
- Technical explanations when needed
- Celebrating milestones!

### Quick Phrases to Continue:
- "Let's package and upload v1.3.1"
- "Create a GitHub Release for v1.3.1"
- "Help me announce the keyboard shortcuts"
- "Implement the Statistics Dashboard"
- "There's a bug: [description]"
- "I got feedback: [feedback]"

---

<p align="center">
<strong>🚀 Project Status: v1.3.1 COMPLETE! 🚀</strong><br>
<i>Next steps: Create GitHub Release + Upload to AnkiWeb</i><br>
<br>
<strong>Version 1.3.1 ready to launch! ⌨️</strong><br>
<br>
Made with ❤️ by Abdalrahman Mahrat<br>
Medical Intern | Addon Developer | Step 2 Candidate
</p>

---

**End of Project Handoff v1.3.1**

*Last Updated: October 2, 2025*
*Current Version: 1.3.1*
*Status: Ready for GitHub Release + AnkiWeb Upload*
