# USMLE Question ID Converter Addon for Anki
# Author: abdmohrat
# Version: 1.2.1

from aqt import mw, gui_hooks
from aqt.qt import *
from aqt.utils import showInfo, openLink, tooltip
from aqt.browser import Browser
import re
import json
import os

# Configuration key for storing user preferences
CONFIG_KEY = "usmle_converter"

def get_config():
    """Get addon configuration with defaults"""
    config = mw.addonManager.getConfig(__name__)
    if config is None:
        config = {
            "last_selected_step": "Step2",
            "custom_patterns": {},
            "conversion_history": []
        }
        mw.addonManager.writeConfig(__name__, config)
    return config

def save_config(config):
    """Save addon configuration"""
    mw.addonManager.writeConfig(__name__, config)

def clean_and_extract_ids(text):
    """
    Extract IDs from text with support for multiple formats:
    - Comma-separated: 1234, 5678, 9012
    - Space-separated: 1234 5678 9012
    - Newline-separated: one ID per line
    - Tab-separated: 1234\t5678\t9012
    - Mixed formats
    """
    # Replace all separators (comma, space, tab, newline) with a single separator
    # This handles all formats: "1,2,3", "1 2 3", "1\n2\n3", "1\t2\t3", or mixed
    text = re.sub(r'[,\s\t\n]+', ',', text)
    
    # Split by comma and extract only numeric parts
    ids = []
    for item in text.split(','):
        # Extract all digits from each item
        clean_id = re.sub(r'\D', '', item.strip())
        if clean_id:  # Only add if we have a valid ID
            ids.append(clean_id)
    
    return ids

def get_tag_pattern(step_type, custom_patterns=None):
    """
    Get the tag pattern for a specific step type
    Supports custom patterns defined by user
    """
    if custom_patterns and step_type in custom_patterns:
        return custom_patterns[step_type]
    
    # Default patterns
    if step_type == "Step1":
        return "tag:#AK_Step1_v12::#UWorld::Step::{ID}"
    elif step_type == "Step3":
        return "tag:#AK_Step3_v12::#UWorld::{ID}"
    else:  # Step2 (default)
        return "tag:#AK_Step2_v12::#UWorld::Step::{ID}"

def convert_ids_to_tags(ids_text, step_type="Step2", custom_patterns=None):
    """
    Convert IDs to Anki search format with custom pattern support
    """
    # Extract and clean IDs from text
    ids = clean_and_extract_ids(ids_text)
    
    if not ids:
        return ""
    
    # Get the tag pattern for this step
    tag_pattern = get_tag_pattern(step_type, custom_patterns)
    
    # Convert each ID to the tag format
    tag_queries = []
    for id in ids:
        # Replace {ID} placeholder with actual ID
        tag_query = tag_pattern.replace("{ID}", id)
        tag_queries.append(tag_query)
    
    # Join with OR
    return ' OR '.join(tag_queries)

def add_to_history(ids_text, step_type, result_count):
    """Add conversion to history"""
    config = get_config()
    history = config.get("conversion_history", [])
    
    # Add new entry
    from datetime import datetime
    entry = {
        "timestamp": datetime.now().isoformat(),
        "step": step_type,
        "ids_preview": ids_text[:50] + "..." if len(ids_text) > 50 else ids_text,
        "count": result_count
    }
    
    # Keep only last 20 entries
    history.insert(0, entry)
    if len(history) > 20:
        history = history[:20]
    
    config["conversion_history"] = history
    save_config(config)

def show_custom_pattern_dialog(parent):
    """Show dialog for configuring custom tag patterns"""
    dialog = QDialog(parent)
    dialog.setWindowTitle("Custom Tag Patterns")
    dialog.setMinimumWidth(600)
    
    layout = QVBoxLayout()
    
    # Instructions
    instructions = QLabel("""
    Define custom tag patterns for your decks. Use {ID} as placeholder for question IDs.
    
    Examples:
    - tag:#MyDeck::#UWorld::{ID}
    - tag:#CustomStep1::Question::{ID}
    - tag:UWorld_{ID}
    """)
    instructions.setWordWrap(True)
    layout.addWidget(instructions)
    
    # Load current config
    config = get_config()
    custom_patterns = config.get("custom_patterns", {})
    
    # Pattern inputs
    patterns_group = QGroupBox("Tag Patterns:")
    patterns_layout = QFormLayout()
    
    step1_input = QLineEdit(custom_patterns.get("Step1", ""))
    step1_input.setPlaceholderText("tag:#AK_Step1_v12::#UWorld::Step::{ID}")
    patterns_layout.addRow("Step 1:", step1_input)
    
    step2_input = QLineEdit(custom_patterns.get("Step2", ""))
    step2_input.setPlaceholderText("tag:#AK_Step2_v12::#UWorld::Step::{ID}")
    patterns_layout.addRow("Step 2:", step2_input)
    
    step3_input = QLineEdit(custom_patterns.get("Step3", ""))
    step3_input.setPlaceholderText("tag:#AK_Step3_v12::#UWorld::{ID}")
    patterns_layout.addRow("Step 3:", step3_input)
    
    patterns_group.setLayout(patterns_layout)
    layout.addWidget(patterns_group)
    
    # Test section
    test_group = QGroupBox("Test Pattern:")
    test_layout = QVBoxLayout()
    
    test_input = QLineEdit()
    test_input.setPlaceholderText("Enter test ID (e.g., 12345)")
    test_layout.addWidget(test_input)
    
    test_result = QLabel("")
    test_result.setWordWrap(True)
    # Theme-aware styling - works in both light and dark mode
    test_result.setStyleSheet("""
        QLabel {
            padding: 10px;
            border: 1px solid palette(mid);
            border-radius: 5px;
            background-color: palette(base);
        }
    """)
    test_layout.addWidget(test_result)
    
    test_group.setLayout(test_layout)
    layout.addWidget(test_group)
    
    # Buttons
    button_layout = QHBoxLayout()
    
    reset_btn = QPushButton("Reset to Defaults")
    save_btn = QPushButton("Save")
    cancel_btn = QPushButton("Cancel")
    
    button_layout.addWidget(reset_btn)
    button_layout.addStretch()
    button_layout.addWidget(save_btn)
    button_layout.addWidget(cancel_btn)
    
    layout.addLayout(button_layout)
    dialog.setLayout(layout)
    
    def test_pattern():
        test_id = test_input.text().strip()
        if not test_id:
            test_result.setText("Enter a test ID to preview")
            return
        
        # Test all three patterns
        results = []
        for step, input_field in [("Step1", step1_input), ("Step2", step2_input), ("Step3", step3_input)]:
            pattern = input_field.text().strip()
            if pattern:
                result = pattern.replace("{ID}", test_id)
                results.append(f"<b>{step}:</b> {result}")
            else:
                default = get_tag_pattern(step)
                result = default.replace("{ID}", test_id)
                results.append(f"<b>{step} (default):</b> {result}")
        
        test_result.setText("<br>".join(results))
    
    def reset_patterns():
        step1_input.clear()
        step2_input.clear()
        step3_input.clear()
        test_result.setText("Patterns reset to defaults")
    
    def save_patterns():
        config = get_config()
        
        # Save only non-empty patterns
        new_patterns = {}
        if step1_input.text().strip():
            new_patterns["Step1"] = step1_input.text().strip()
        if step2_input.text().strip():
            new_patterns["Step2"] = step2_input.text().strip()
        if step3_input.text().strip():
            new_patterns["Step3"] = step3_input.text().strip()
        
        config["custom_patterns"] = new_patterns
        save_config(config)
        
        tooltip("Custom patterns saved!")
        dialog.accept()
    
    # Connect signals
    test_input.textChanged.connect(lambda: test_pattern())
    step1_input.textChanged.connect(lambda: test_pattern() if test_input.text().strip() else None)
    step2_input.textChanged.connect(lambda: test_pattern() if test_input.text().strip() else None)
    step3_input.textChanged.connect(lambda: test_pattern() if test_input.text().strip() else None)
    
    reset_btn.clicked.connect(reset_patterns)
    save_btn.clicked.connect(save_patterns)
    cancel_btn.clicked.connect(dialog.reject)
    
    dialog.exec()

def load_ids_from_file():
    """Load question IDs from a text or CSV file"""
    file_path, _ = QFileDialog.getOpenFileName(
        None,
        "Select File with Question IDs",
        "",
        "Text Files (*.txt);;CSV Files (*.csv);;All Files (*.*)"
    )
    
    if not file_path:
        return None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        showInfo(f"Error reading file: {str(e)}")
        return None

def show_history_dialog(parent):
    """Show conversion history"""
    config = get_config()
    history = config.get("conversion_history", [])
    
    if not history:
        showInfo("No conversion history yet.")
        return
    
    dialog = QDialog(parent)
    dialog.setWindowTitle("Conversion History")
    dialog.setMinimumSize(600, 400)
    
    layout = QVBoxLayout()
    
    # Create table
    table = QTableWidget()
    table.setColumnCount(4)
    table.setHorizontalHeaderLabels(["Time", "Step", "IDs Preview", "Count"])
    table.setRowCount(len(history))
    table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    
    # Populate table
    for i, entry in enumerate(history):
        # Parse timestamp
        from datetime import datetime
        try:
            dt = datetime.fromisoformat(entry["timestamp"])
            time_str = dt.strftime("%Y-%m-%d %H:%M")
        except:
            time_str = entry["timestamp"]
        
        table.setItem(i, 0, QTableWidgetItem(time_str))
        table.setItem(i, 1, QTableWidgetItem(entry["step"]))
        table.setItem(i, 2, QTableWidgetItem(entry["ids_preview"]))
        table.setItem(i, 3, QTableWidgetItem(str(entry["count"])))
    
    # Resize columns to content
    table.resizeColumnsToContents()
    
    layout.addWidget(table)
    
    # Buttons
    button_layout = QHBoxLayout()
    clear_btn = QPushButton("Clear History")
    close_btn = QPushButton("Close")
    
    button_layout.addWidget(clear_btn)
    button_layout.addStretch()
    button_layout.addWidget(close_btn)
    
    layout.addLayout(button_layout)
    dialog.setLayout(layout)
    
    def clear_history():
        reply = QMessageBox.question(
            dialog,
            "Clear History",
            "Are you sure you want to clear all conversion history?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            config = get_config()
            config["conversion_history"] = []
            save_config(config)
            dialog.accept()
            tooltip("History cleared!")
    
    clear_btn.clicked.connect(clear_history)
    close_btn.clicked.connect(dialog.accept)
    
    dialog.exec()

def show_converter_dialog():
    """
    Show the main converter dialog
    """
    dialog = QDialog(mw)
    dialog.setWindowTitle("USMLE Question ID Converter")
    dialog.setFixedSize(850, 550)
    
    # Main layout
    main_layout = QVBoxLayout()
    
    # Top bar with support buttons and new feature buttons
    top_bar = QHBoxLayout()
    
    # Left side - feature buttons
    history_btn = QPushButton("📊 History")
    history_btn.setToolTip("View conversion history")
    history_btn.clicked.connect(lambda: show_history_dialog(dialog))
    
    custom_pattern_btn = QPushButton("⚙️ Custom Patterns")
    custom_pattern_btn.setToolTip("Configure custom tag patterns")
    custom_pattern_btn.clicked.connect(lambda: show_custom_pattern_dialog(dialog))
    
    file_btn = QPushButton("📁 Load from File")
    file_btn.setToolTip("Load question IDs from a file")
    
    top_bar.addWidget(history_btn)
    top_bar.addWidget(custom_pattern_btn)
    top_bar.addWidget(file_btn)
    top_bar.addStretch()
    
    # Right side - support buttons
    support_btn = QPushButton("☕ Buy Me a Coffee")
    support_btn.setStyleSheet("""
        QPushButton {
            background-color: #29abe0;
            color: white;
            font-weight: bold;
            border-radius: 5px;
            padding: 6px 12px;
            border: none;
            font-size: 11px;
        }
        QPushButton:hover {
            background-color: #1a8cb8;
        }
        QPushButton:pressed {
            background-color: #127096;
        }
    """)
    support_btn.clicked.connect(lambda: openLink("https://ko-fi.com/abdmohrat"))
    
    # Review button
    review_btn = QPushButton("⭐ Rate Addon")
    review_btn.setStyleSheet("""
        QPushButton {
            background-color: #ffa500;
            color: white;
            font-weight: bold;
            border-radius: 5px;
            padding: 6px 12px;
            border: none;
            font-size: 11px;
        }
        QPushButton:hover {
            background-color: #ff8c00;
        }
        QPushButton:pressed {
            background-color: #e67e00;
        }
    """)
    review_btn.clicked.connect(lambda: openLink("https://ankiweb.net/shared/review/699193084"))
    
    top_bar.addWidget(support_btn)
    top_bar.addSpacing(10)
    top_bar.addWidget(review_btn)
    
    main_layout.addLayout(top_bar)
    main_layout.addSpacing(10)
    
    # Instructions
    instructions = QLabel("""
    Paste your USMLE question IDs below (supports multiple formats):
    • Comma-separated: 21656, 19263, 4466
    • Space-separated: 21656 19263 4466
    • One per line or any mix of formats
    """)
    main_layout.addWidget(instructions)
    
    # Step selection
    step_group = QGroupBox("Select USMLE Step:")
    step_layout = QHBoxLayout()
    
    step1_radio = QRadioButton("Step 1")
    step2_radio = QRadioButton("Step 2")
    step3_radio = QRadioButton("Step 3")
    
    # Load saved preference
    config = get_config()
    last_step = config.get("last_selected_step", "Step2")
    if last_step == "Step1":
        step1_radio.setChecked(True)
    elif last_step == "Step3":
        step3_radio.setChecked(True)
    else:
        step2_radio.setChecked(True)
    
    step_layout.addWidget(step1_radio)
    step_layout.addWidget(step2_radio)
    step_layout.addWidget(step3_radio)
    step_group.setLayout(step_layout)
    main_layout.addWidget(step_group)
    
    # Input text area
    input_text = QTextEdit()
    input_text.setPlaceholderText("Paste your question IDs here (any format: comma, space, or newline separated)...")
    input_text.setMaximumHeight(100)
    main_layout.addWidget(input_text)
    
    # Stats label
    stats_label = QLabel("Ready to convert")
    stats_label.setStyleSheet("color: gray; font-style: italic;")
    main_layout.addWidget(stats_label)
    
    # Output text area
    output_label = QLabel("Anki search query:")
    main_layout.addWidget(output_label)
    
    output_text = QTextEdit()
    output_text.setReadOnly(True)
    main_layout.addWidget(output_text)
    
    # Current selection display
    initial_step = "Step 1" if step1_radio.isChecked() else ("Step 3" if step3_radio.isChecked() else "Step 2")
    current_step_label = QLabel(f"Current selection: {initial_step} (remembered from last use)")
    current_step_label.setStyleSheet("color: blue; font-weight: bold;")
    main_layout.addWidget(current_step_label)
    
    # Bottom buttons
    button_layout = QHBoxLayout()
    
    convert_btn = QPushButton("Convert")
    copy_btn = QPushButton("Copy to Clipboard")
    search_btn = QPushButton("Search in Anki")
    close_btn = QPushButton("Close")
    
    button_layout.addWidget(convert_btn)
    button_layout.addWidget(copy_btn)
    button_layout.addWidget(search_btn)
    button_layout.addWidget(close_btn)
    
    main_layout.addLayout(button_layout)
    dialog.setLayout(main_layout)
    
    def get_selected_step():
        if step1_radio.isChecked():
            return "Step1"
        elif step3_radio.isChecked():
            return "Step3"
        else:
            return "Step2"
    
    def save_step_preference():
        """Save the current step selection"""
        config = get_config()
        config["last_selected_step"] = get_selected_step()
        save_config(config)
    
    def update_step_label():
        if step1_radio.isChecked():
            step = "Step 1"
        elif step3_radio.isChecked():
            step = "Step 3"
        else:
            step = "Step 2"
        current_step_label.setText(f"Current selection: {step}")
        # Save preference when changed
        save_step_preference()
        # Auto-convert when step changes
        if input_text.toPlainText().strip():
            convert_clicked()
    
    def convert_clicked():
        ids_text = input_text.toPlainText().strip()
        if not ids_text:
            showInfo("Please enter some question IDs first.")
            return
        
        try:
            step_type = get_selected_step()
            config = get_config()
            custom_patterns = config.get("custom_patterns", {})
            
            # Convert using custom patterns if available
            converted = convert_ids_to_tags(ids_text, step_type, custom_patterns)
            output_text.setPlainText(converted)
            
            # Update stats
            id_count = len(clean_and_extract_ids(ids_text))
            stats_label.setText(f"✓ Converted {id_count} question ID(s)")
            stats_label.setStyleSheet("color: green; font-weight: bold;")
            
            # Add to history
            add_to_history(ids_text, step_type, id_count)
            
        except Exception as e:
            showInfo(f"Error converting IDs: {str(e)}")
            stats_label.setText(f"✗ Error: {str(e)}")
            stats_label.setStyleSheet("color: red; font-weight: bold;")
    
    def copy_clicked():
        converted_text = output_text.toPlainText()
        if not converted_text:
            showInfo("Nothing to copy. Please convert some IDs first.")
            return
        
        clipboard = QApplication.clipboard()
        clipboard.setText(converted_text)
        if step1_radio.isChecked():
            step = "Step 1"
        elif step3_radio.isChecked():
            step = "Step 3"
        else:
            step = "Step 2"
        tooltip(f"Search query for {step} copied to clipboard!")
    
    def search_clicked():
        converted_text = output_text.toPlainText()
        if not converted_text:
            showInfo("Nothing to search. Please convert some IDs first.")
            return
        
        # Open the browser and set the search
        from aqt import dialogs
        browser = dialogs.open("Browser", mw)
        browser.form.searchEdit.lineEdit().setText(converted_text)
        browser.onSearchActivated()
        
        dialog.close()
    
    def close_clicked():
        # Save preference when closing (just in case)
        save_step_preference()
        dialog.close()
    
    def load_file_clicked():
        """Load IDs from file"""
        content = load_ids_from_file()
        if content:
            input_text.setPlainText(content)
            tooltip("File loaded! IDs ready to convert.")
    
    # Connect main action buttons
    convert_btn.clicked.connect(convert_clicked)
    copy_btn.clicked.connect(copy_clicked)
    search_btn.clicked.connect(search_clicked)
    close_btn.clicked.connect(close_clicked)
    file_btn.clicked.connect(load_file_clicked)
    
    # Connect radio buttons
    step1_radio.toggled.connect(update_step_label)
    step2_radio.toggled.connect(update_step_label)
    step3_radio.toggled.connect(update_step_label)
    
    # Auto-convert when text changes (with a small delay)
    def on_text_changed():
        # Update stats preview
        text = input_text.toPlainText().strip()
        if text:
            id_count = len(clean_and_extract_ids(text))
            stats_label.setText(f"Found {id_count} ID(s) - auto-converting...")
            stats_label.setStyleSheet("color: gray; font-style: italic;")
            QTimer.singleShot(500, convert_clicked)  # 500ms delay
        else:
            stats_label.setText("Ready to convert")
            stats_label.setStyleSheet("color: gray; font-style: italic;")
    
    input_text.textChanged.connect(on_text_changed)
    
    dialog.show()

# Context menu integration for Browser
def on_browser_context_menu(browser: Browser, menu: QMenu):
    """Add context menu option to get question ID from selected card"""
    selected_cards = browser.selectedCards()
    if not selected_cards:
        return
    
    # Add separator
    menu.addSeparator()
    
    # Add action to extract question IDs
    action = menu.addAction("📋 Copy UWorld Question ID(s)")
    action.triggered.connect(lambda: extract_question_ids(browser, selected_cards))

def extract_question_ids(browser: Browser, card_ids):
    """Extract UWorld question IDs from selected cards"""
    if not card_ids:
        return
    
    extracted_ids = []
    
    for card_id in card_ids:
        card = mw.col.get_card(card_id)
        note = card.note()
        
        # Search for UWorld ID in tags
        for tag in note.tags:
            # Match patterns like #AK_Step1_v12::#UWorld::Step::12345
            # or #AK_Step2_v12::#UWorld::Step::67890
            # or #AK_Step3_v12::#UWorld::98765
            match = re.search(r'#AK_Step[123]_v\d+::#UWorld::(?:Step::)?(\d+)', tag)
            if match:
                question_id = match.group(1)
                if question_id not in extracted_ids:
                    extracted_ids.append(question_id)
    
    if extracted_ids:
        # Copy to clipboard
        id_text = ", ".join(extracted_ids)
        clipboard = QApplication.clipboard()
        clipboard.setText(id_text)
        
        count = len(extracted_ids)
        if count == 1:
            tooltip(f"Copied question ID: {id_text}")
        else:
            tooltip(f"Copied {count} question IDs to clipboard!")
    else:
        tooltip("No UWorld question IDs found in selected card(s)")

# Add menu item to Tools menu
def add_menu_item():
    action = QAction("USMLE Question ID Converter", mw)
    action.triggered.connect(show_converter_dialog)
    mw.form.menuTools.addAction(action)

# Initialize the addon
add_menu_item()

# Add browser context menu hook
gui_hooks.browser_will_show_context_menu.append(on_browser_context_menu)
