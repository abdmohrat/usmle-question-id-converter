# UWorld AMBOSS COMLEX - Question ID Converter for Anki
# Author: abdmohrat
# Version: 1.4.0

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
            "last_selected_bank": "UWorld",
            "custom_patterns": {},
            "conversion_history": []
        }
        mw.addonManager.writeConfig(__name__, config)
    # Ensure last_selected_bank exists for older configs
    if "last_selected_bank" not in config:
        config["last_selected_bank"] = "UWorld"
        mw.addonManager.writeConfig(__name__, config)
    return config

def save_config(config):
    """Save addon configuration"""
    mw.addonManager.writeConfig(__name__, config)

def clean_and_extract_ids(text, bank="UWorld"):
    """
    Extract IDs from text with support for multiple formats:
    - Comma-separated: 1234, 5678, 9012
    - Space-separated: 1234 5678 9012
    - Newline-separated: one ID per line
    - Tab-separated: 1234\t5678\t9012
    - Mixed formats
    
    For AMBOSS, supports alphanumeric IDs with hyphens and underscores:
    - -aaDMQ, 0jae_4, 3_0SLi
    """
    # Replace all separators (comma, space, tab, newline) with a single separator
    text = re.sub(r'[,\s\t\n]+', ',', text)
    
    # Split by comma and extract IDs based on bank type
    ids = []
    for item in text.split(','):
        item = item.strip()
        if not item:
            continue
            
        if bank == "AMBOSS":
            # AMBOSS: Keep alphanumeric, hyphens, and underscores
            clean_id = re.sub(r'[^a-zA-Z0-9\-_]', '', item)
        else:
            # UWorld, COMLEX: Only digits
            clean_id = re.sub(r'\D', '', item)
        
        if clean_id:  # Only add if we have a valid ID
            ids.append(clean_id)
    
    return ids

def get_tag_pattern(step_type, bank="UWorld", custom_patterns=None):
    """
    Get the tag pattern for a specific step type and question bank
    Supports custom patterns defined by user
    
    Banks: UWorld, AMBOSS, COMLEX
    """
    # Check for custom patterns first
    pattern_key = f"{bank}_{step_type}"
    if custom_patterns and pattern_key in custom_patterns:
        return custom_patterns[pattern_key]
    
    # Default patterns by bank
    if bank == "AMBOSS":
        if step_type == "Step1":
            return "tag:#AK_Step1_v12::#AMBOSS::{ID}"
        elif step_type == "Step2":
            return "tag:#AK_Step2_v12::#AMBOSS::{ID}"
        else:
            # Step 3 not supported for AMBOSS
            return None
    
    elif bank == "COMLEX":
        if step_type == "Step1":
            return "tag:#AK_Step1_v12::#UWorld::COMLEX::{ID}"
        elif step_type == "Step2":
            return "tag:#AK_Step2_v12::#UWorld::COMLEX::{ID}"
        else:
            # Step 3 not supported for COMLEX
            return None
    
    else:  # UWorld (default)
        if step_type == "Step1":
            return "tag:#AK_Step1_v12::#UWorld::Step::{ID}"
        elif step_type == "Step3":
            return "tag:#AK_Step3_v12::#UWorld::{ID}"
        else:  # Step2 (default)
            return "tag:#AK_Step2_v12::#UWorld::Step::{ID}"

def convert_ids_to_tags(ids_text, step_type="Step2", bank="UWorld", custom_patterns=None):
    """
    Convert IDs to Anki search format with custom pattern support
    Supports multiple question banks: UWorld, AMBOSS, COMLEX
    """
    # Extract and clean IDs from text (bank-aware)
    ids = clean_and_extract_ids(ids_text, bank)
    
    if not ids:
        return ""
    
    # Get the tag pattern for this step and bank
    tag_pattern = get_tag_pattern(step_type, bank, custom_patterns)
    
    if tag_pattern is None:
        return ""
    
    # Convert each ID to the tag format
    tag_queries = []
    for id in ids:
        # Replace {ID} placeholder with actual ID
        tag_query = tag_pattern.replace("{ID}", id)
        tag_queries.append(tag_query)
    
    # Join with OR
    return ' OR '.join(tag_queries)

def add_to_history(ids_text, step_type, bank, result_count):
    """Add conversion to history"""
    config = get_config()
    history = config.get("conversion_history", [])
    
    # Add new entry
    from datetime import datetime
    entry = {
        "timestamp": datetime.now().isoformat(),
        "bank": bank,
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
    dialog.setMinimumWidth(700)
    
    layout = QVBoxLayout()
    
    # Instructions
    instructions = QLabel("""
    Define custom tag patterns for your decks. Use {ID} as placeholder for question IDs.
    Patterns are organized by Question Bank and Step.
    
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
    
    # Pattern inputs organized by bank
    tabs = QTabWidget()
    
    # UWorld Tab
    uworld_widget = QWidget()
    uworld_layout = QFormLayout()
    
    uworld_step1 = QLineEdit(custom_patterns.get("UWorld_Step1", ""))
    uworld_step1.setPlaceholderText("tag:#AK_Step1_v12::#UWorld::Step::{ID}")
    uworld_layout.addRow("Step 1:", uworld_step1)
    
    uworld_step2 = QLineEdit(custom_patterns.get("UWorld_Step2", ""))
    uworld_step2.setPlaceholderText("tag:#AK_Step2_v12::#UWorld::Step::{ID}")
    uworld_layout.addRow("Step 2:", uworld_step2)
    
    uworld_step3 = QLineEdit(custom_patterns.get("UWorld_Step3", ""))
    uworld_step3.setPlaceholderText("tag:#AK_Step3_v12::#UWorld::{ID}")
    uworld_layout.addRow("Step 3:", uworld_step3)
    
    uworld_widget.setLayout(uworld_layout)
    tabs.addTab(uworld_widget, "UWorld")
    
    # AMBOSS Tab
    amboss_widget = QWidget()
    amboss_layout = QFormLayout()
    
    amboss_step1 = QLineEdit(custom_patterns.get("AMBOSS_Step1", ""))
    amboss_step1.setPlaceholderText("tag:#AK_Step1_v12::#AMBOSS::{ID}")
    amboss_layout.addRow("Step 1:", amboss_step1)
    
    amboss_step2 = QLineEdit(custom_patterns.get("AMBOSS_Step2", ""))
    amboss_step2.setPlaceholderText("tag:#AK_Step2_v12::#AMBOSS::{ID}")
    amboss_layout.addRow("Step 2:", amboss_step2)
    
    amboss_note = QLabel("Note: Step 3 not available for AMBOSS")
    amboss_note.setStyleSheet("color: gray; font-style: italic;")
    amboss_layout.addRow("", amboss_note)
    
    amboss_widget.setLayout(amboss_layout)
    tabs.addTab(amboss_widget, "AMBOSS")
    
    # COMLEX Tab
    comlex_widget = QWidget()
    comlex_layout = QFormLayout()
    
    comlex_step1 = QLineEdit(custom_patterns.get("COMLEX_Step1", ""))
    comlex_step1.setPlaceholderText("tag:#AK_Step1_v12::#UWorld::COMLEX::{ID}")
    comlex_layout.addRow("Step 1:", comlex_step1)
    
    comlex_step2 = QLineEdit(custom_patterns.get("COMLEX_Step2", ""))
    comlex_step2.setPlaceholderText("tag:#AK_Step2_v12::#UWorld::COMLEX::{ID}")
    comlex_layout.addRow("Step 2:", comlex_step2)
    
    comlex_note = QLabel("Note: Step 3 not available for COMLEX")
    comlex_note.setStyleSheet("color: gray; font-style: italic;")
    comlex_layout.addRow("", comlex_note)
    
    comlex_widget.setLayout(comlex_layout)
    tabs.addTab(comlex_widget, "COMLEX")
    
    layout.addWidget(tabs)
    
    # Test section
    test_group = QGroupBox("Test Pattern:")
    test_layout = QVBoxLayout()
    
    test_input = QLineEdit()
    test_input.setPlaceholderText("Enter test ID (e.g., 12345 for UWorld/COMLEX or -aaDMQ for AMBOSS)")
    test_layout.addWidget(test_input)
    
    test_result = QLabel("")
    test_result.setWordWrap(True)
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
    
    # Store all input fields
    all_inputs = {
        "UWorld_Step1": uworld_step1,
        "UWorld_Step2": uworld_step2,
        "UWorld_Step3": uworld_step3,
        "AMBOSS_Step1": amboss_step1,
        "AMBOSS_Step2": amboss_step2,
        "COMLEX_Step1": comlex_step1,
        "COMLEX_Step2": comlex_step2
    }
    
    def test_pattern():
        test_id = test_input.text().strip()
        if not test_id:
            test_result.setText("Enter a test ID to preview")
            return
        
        # Test patterns from current tab
        current_tab_name = tabs.tabText(tabs.currentIndex())
        results = []
        
        for key, input_field in all_inputs.items():
            if key.startswith(current_tab_name):
                pattern = input_field.text().strip()
                step = key.split('_')[1]
                
                if pattern:
                    result = pattern.replace("{ID}", test_id)
                    results.append(f"<b>{step}:</b> {result}")
                else:
                    # Show default pattern
                    default = get_tag_pattern(step, current_tab_name)
                    if default:
                        result = default.replace("{ID}", test_id)
                        results.append(f"<b>{step} (default):</b> {result}")
        
        if results:
            test_result.setText("<br>".join(results))
        else:
            test_result.setText("No patterns to test")
    
    def reset_patterns():
        for input_field in all_inputs.values():
            input_field.clear()
        test_result.setText("Patterns reset to defaults")
    
    def save_patterns():
        config = get_config()
        
        # Save only non-empty patterns
        new_patterns = {}
        for key, input_field in all_inputs.items():
            if input_field.text().strip():
                new_patterns[key] = input_field.text().strip()
        
        config["custom_patterns"] = new_patterns
        save_config(config)
        
        tooltip("Custom patterns saved!")
        dialog.accept()
    
    # Connect signals
    test_input.textChanged.connect(lambda: test_pattern())
    tabs.currentChanged.connect(lambda: test_pattern() if test_input.text().strip() else None)
    
    for input_field in all_inputs.values():
        input_field.textChanged.connect(lambda: test_pattern() if test_input.text().strip() else None)
    
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
    table.setColumnCount(5)
    table.setHorizontalHeaderLabels(["Time", "Bank", "Step", "IDs Preview", "Count"])
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
        table.setItem(i, 1, QTableWidgetItem(entry.get("bank", "UWorld")))  # Default to UWorld for old entries
        table.setItem(i, 2, QTableWidgetItem(entry["step"]))
        table.setItem(i, 3, QTableWidgetItem(entry["ids_preview"]))
        table.setItem(i, 4, QTableWidgetItem(str(entry["count"])))
    
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
    dialog.setWindowTitle("UWorld AMBOSS COMLEX - Question ID Converter")
    dialog.setFixedSize(850, 600)
    
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
    Paste your question IDs below (supports multiple formats):
    • UWorld/COMLEX: Comma, space, or newline separated numbers (e.g., 21656, 19263)
    • AMBOSS: Alphanumeric IDs with hyphens (e.g., -aaDMQ, 0jae_4, 3_0SLi)
    """)
    main_layout.addWidget(instructions)
    
    # Keyboard shortcuts hint
    shortcuts_hint = QLabel("💡 Shortcuts: Ctrl+Shift+U (open) | Ctrl+Enter (search) | Esc (close) | Auto-loads clipboard!")
    shortcuts_hint.setStyleSheet("color: gray; font-size: 10px; font-style: italic;")
    main_layout.addWidget(shortcuts_hint)
    
    # Question Bank selection
    bank_group = QGroupBox("Select Question Bank:")
    bank_layout = QHBoxLayout()
    
    uworld_radio = QRadioButton("UWorld")
    amboss_radio = QRadioButton("AMBOSS")
    comlex_radio = QRadioButton("COMLEX")
    
    # Load saved preference
    config = get_config()
    last_bank = config.get("last_selected_bank", "UWorld")
    if last_bank == "AMBOSS":
        amboss_radio.setChecked(True)
    elif last_bank == "COMLEX":
        comlex_radio.setChecked(True)
    else:
        uworld_radio.setChecked(True)
    
    bank_layout.addWidget(uworld_radio)
    bank_layout.addWidget(amboss_radio)
    bank_layout.addWidget(comlex_radio)
    bank_group.setLayout(bank_layout)
    main_layout.addWidget(bank_group)
    
    # Step selection
    step_group = QGroupBox("Select USMLE Step:")
    step_layout = QHBoxLayout()
    
    step1_radio = QRadioButton("Step 1")
    step2_radio = QRadioButton("Step 2")
    step3_radio = QRadioButton("Step 3")
    
    # Load saved preference
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
    
    # Auto-load from clipboard if it contains potential IDs
    clipboard = QApplication.clipboard()
    clipboard_text = clipboard.text().strip()
    
    if clipboard_text:
        # Check if clipboard might contain question IDs
        # Look for numbers or alphanumeric patterns
        has_numbers = bool(re.search(r'\d+', clipboard_text))
        has_amboss_pattern = bool(re.search(r'[a-zA-Z0-9\-_]{4,}', clipboard_text))
        
        # If clipboard looks like it might contain IDs, auto-load it
        if has_numbers or has_amboss_pattern:
            # Only auto-load if it's not too long (prevent pasting entire documents)
            if len(clipboard_text) < 5000:  # Max 5000 characters
                input_text.setPlainText(clipboard_text)
                # Show tooltip to let user know
                QTimer.singleShot(100, lambda: tooltip("📋 Clipboard content auto-loaded!", period=2000))
    
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
    def get_bank_name():
        if uworld_radio.isChecked():
            return "UWorld"
        elif amboss_radio.isChecked():
            return "AMBOSS"
        else:
            return "COMLEX"
    
    def get_step_name():
        if step1_radio.isChecked():
            return "Step 1"
        elif step3_radio.isChecked():
            return "Step 3"
        else:
            return "Step 2"
    
    current_step_label = QLabel(f"Current selection: {get_bank_name()} - {get_step_name()}")
    current_step_label.setStyleSheet("color: blue; font-weight: bold;")
    main_layout.addWidget(current_step_label)
    
    # Function to update Step 3 availability
    def update_step3_availability():
        bank = get_bank_name()
        if bank in ["AMBOSS", "COMLEX"]:
            # Disable Step 3 for AMBOSS and COMLEX
            step3_radio.setEnabled(False)
            step3_radio.setToolTip("Step 3 not available for " + bank)
            # If Step 3 was selected, switch to Step 2
            if step3_radio.isChecked():
                step2_radio.setChecked(True)
        else:
            # Enable Step 3 for UWorld
            step3_radio.setEnabled(True)
            step3_radio.setToolTip("")
    
    # Set initial Step 3 availability
    update_step3_availability()
    
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
    
    def get_selected_bank():
        if uworld_radio.isChecked():
            return "UWorld"
        elif amboss_radio.isChecked():
            return "AMBOSS"
        else:
            return "COMLEX"
    
    def save_preferences():
        """Save the current step and bank selection"""
        config = get_config()
        config["last_selected_step"] = get_selected_step()
        config["last_selected_bank"] = get_selected_bank()
        save_config(config)
    
    def update_labels():
        bank = get_bank_name()
        step = get_step_name()
        current_step_label.setText(f"Current selection: {bank} - {step}")
        # Save preferences when changed
        save_preferences()
        # Update Step 3 availability
        update_step3_availability()
        # Auto-convert when selection changes (only if text exists)
        if input_text.toPlainText().strip():
            convert_clicked(auto_convert=True)
    
    def convert_clicked(auto_convert=False):
        ids_text = input_text.toPlainText().strip()
        if not ids_text:
            # Only show popup if manually clicked (not auto-convert)
            if not auto_convert:
                showInfo("Please enter some question IDs first.")
            return
        
        try:
            step_type = get_selected_step()
            bank = get_selected_bank()
            config = get_config()
            custom_patterns = config.get("custom_patterns", {})
            
            # Convert using custom patterns if available
            converted = convert_ids_to_tags(ids_text, step_type, bank, custom_patterns)
            
            # Check if conversion failed (Step 3 not available or no valid IDs)
            if not converted:
                # Only show error for Step 3 unavailability if manually clicked
                if step_type == "Step3" and bank in ["AMBOSS", "COMLEX"] and not auto_convert:
                    showInfo(f"Step 3 is not available for {bank}. Please select Step 1 or Step 2.")
                # For invalid IDs during auto-convert, just clear output silently
                output_text.clear()
                stats_label.setText("No valid IDs found")
                stats_label.setStyleSheet("color: gray; font-style: italic;")
                return
            
            output_text.setPlainText(converted)
            
            # Update stats
            id_count = len(clean_and_extract_ids(ids_text, bank))
            if id_count > 0:
                stats_label.setText(f"✓ Converted {id_count} question ID(s)")
                stats_label.setStyleSheet("color: green; font-weight: bold;")
                
                # Add to history
                add_to_history(ids_text, step_type, bank, id_count)
            else:
                stats_label.setText("No valid IDs found")
                stats_label.setStyleSheet("color: gray; font-style: italic;")
            
        except Exception as e:
            # Only show error popup if manually clicked
            if not auto_convert:
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
        bank = get_bank_name()
        step = get_step_name()
        tooltip(f"Search query for {bank} - {step} copied to clipboard!")
    
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
        # Save preferences when closing (just in case)
        save_preferences()
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
    
    # Auto-convert when text changes (with a small delay)
    def on_text_changed():
        # Update stats preview
        text = input_text.toPlainText().strip()
        if text:
            bank = get_selected_bank()
            id_count = len(clean_and_extract_ids(text, bank))
            stats_label.setText(f"Found {id_count} ID(s) - auto-converting...")
            stats_label.setStyleSheet("color: gray; font-style: italic;")
            QTimer.singleShot(500, lambda: convert_clicked(auto_convert=True))  # 500ms delay
        else:
            # Clear output when input is empty
            output_text.clear()
            stats_label.setText("Ready to convert")
            stats_label.setStyleSheet("color: gray; font-style: italic;")
    
    input_text.textChanged.connect(on_text_changed)
    
    # Connect bank radio buttons
    uworld_radio.toggled.connect(update_labels)
    amboss_radio.toggled.connect(update_labels)
    comlex_radio.toggled.connect(update_labels)
    
    # Connect step radio buttons
    step1_radio.toggled.connect(update_labels)
    step2_radio.toggled.connect(update_labels)
    step3_radio.toggled.connect(update_labels)
    
    # Setup dialog keyboard shortcuts
    # Ctrl+Enter: Convert and search immediately
    search_shortcut = QShortcut(QKeySequence("Ctrl+Return"), dialog)
    search_shortcut.activated.connect(search_clicked)
    
    # Esc: Close dialog (already handled by Qt, but making it explicit)
    close_shortcut = QShortcut(QKeySequence("Esc"), dialog)
    close_shortcut.activated.connect(close_clicked)
    
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
    action = menu.addAction("📋 Copy Question ID(s)")
    action.triggered.connect(lambda: extract_question_ids(browser, selected_cards))

def extract_question_ids(browser: Browser, card_ids):
    """Extract UWorld/AMBOSS/COMLEX question IDs from selected cards"""
    if not card_ids:
        return
    
    extracted_ids = {
        "UWorld": [],
        "AMBOSS": [],
        "COMLEX": []
    }
    
    for card_id in card_ids:
        card = mw.col.get_card(card_id)
        note = card.note()
        
        # Search for IDs in tags
        for tag in note.tags:
            # UWorld pattern: #AK_Step[123]_v##::#UWorld::Step::12345
            uworld_match = re.search(r'#AK_Step[123]_v\d+::#UWorld::Step::(\d+)', tag)
            if uworld_match:
                question_id = uworld_match.group(1)
                if question_id not in extracted_ids["UWorld"]:
                    extracted_ids["UWorld"].append(question_id)
                continue
            
            # UWorld Step 3 pattern: #AK_Step3_v##::#UWorld::98765
            uworld_step3_match = re.search(r'#AK_Step3_v\d+::#UWorld::(\d+)', tag)
            if uworld_step3_match:
                question_id = uworld_step3_match.group(1)
                if question_id not in extracted_ids["UWorld"]:
                    extracted_ids["UWorld"].append(question_id)
                continue
            
            # AMBOSS pattern: #AK_Step[12]_v##::#AMBOSS::-aaDMQ
            amboss_match = re.search(r'#AK_Step[12]_v\d+::#AMBOSS::([a-zA-Z0-9\-_]+)', tag)
            if amboss_match:
                question_id = amboss_match.group(1)
                if question_id not in extracted_ids["AMBOSS"]:
                    extracted_ids["AMBOSS"].append(question_id)
                continue
            
            # COMLEX pattern: #AK_Step[12]_v##::#UWorld::COMLEX::106228
            comlex_match = re.search(r'#AK_Step[12]_v\d+::#UWorld::COMLEX::(\d+)', tag)
            if comlex_match:
                question_id = comlex_match.group(1)
                if question_id not in extracted_ids["COMLEX"]:
                    extracted_ids["COMLEX"].append(question_id)
                continue
    
    # Build result message
    all_ids = []
    result_parts = []
    
    for bank, ids in extracted_ids.items():
        if ids:
            all_ids.extend(ids)
            result_parts.append(f"{bank}: {len(ids)}")
    
    if all_ids:
        # Copy all IDs to clipboard (separated by commas)
        id_text = ", ".join(all_ids)
        clipboard = QApplication.clipboard()
        clipboard.setText(id_text)
        
        count = len(all_ids)
        banks_info = " (" + ", ".join(result_parts) + ")"
        if count == 1:
            tooltip(f"Copied question ID: {id_text}")
        else:
            tooltip(f"Copied {count} question IDs{banks_info} to clipboard!")
    else:
        tooltip("No question IDs found in selected card(s)")

# Add menu item to Tools menu
def add_menu_item():
    action = QAction("UWorld AMBOSS COMLEX - Question ID Converter", mw)
    action.triggered.connect(show_converter_dialog)
    mw.form.menuTools.addAction(action)

def setup_shortcuts():
    """Setup global keyboard shortcuts"""
    # Global shortcut: Ctrl+Shift+U to open converter
    shortcut = QShortcut(QKeySequence("Ctrl+Shift+U"), mw)
    shortcut.activated.connect(show_converter_dialog)

# Initialize the addon
add_menu_item()
setup_shortcuts()

# Add browser context menu hook
gui_hooks.browser_will_show_context_menu.append(on_browser_context_menu)
