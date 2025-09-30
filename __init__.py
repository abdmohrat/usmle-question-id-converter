# USMLE Question ID Converter Addon for Anki
# Author: abdmohrat
# Version: 1.1.0

from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo, openLink
import re

# Configuration key for storing user preferences
CONFIG_KEY = "usmle_converter"

def get_config():
    """Get addon configuration with defaults"""
    config = mw.addonManager.getConfig(__name__)
    if config is None:
        config = {"last_selected_step": "Step2"}
        mw.addonManager.writeConfig(__name__, config)
    return config

def save_config(config):
    """Save addon configuration"""
    mw.addonManager.writeConfig(__name__, config)

def convert_ids_to_tags(ids_text, step_type="Step2"):
    """
    Convert comma-separated question IDs to Anki search format
    """
    # Remove any extra whitespace and split by comma
    ids = [id.strip() for id in ids_text.split(',') if id.strip()]
    
    # Define tag formats for different steps
    if step_type == "Step1":
        tag_prefix = "tag:#AK_Step1_v12::#UWorld::Step::"
    elif step_type == "Step3":
        tag_prefix = "tag:#AK_Step3_v12::#UWorld::"
    else:  # Step2 (default)
        tag_prefix = "tag:#AK_Step2_v12::#UWorld::Step::"
    
    # Convert each ID to the tag format
    tag_queries = []
    for id in ids:
        # Remove any non-numeric characters (just in case)
        clean_id = re.sub(r'\D', '', id)
        if clean_id:  # Only add if we have a valid ID
            tag_queries.append(f'{tag_prefix}{clean_id}')
    
    # Join with OR
    return ' OR '.join(tag_queries)

def show_converter_dialog():
    """
    Show the main converter dialog
    """
    dialog = QDialog(mw)
    dialog.setWindowTitle("USMLE Question ID Converter")
    dialog.setFixedSize(750, 450)
    
    layout = QVBoxLayout()
    
    # Instructions
    instructions = QLabel("""
    Paste your USMLE question IDs below (comma-separated):
    Example: 21656, 19263, 4466, 12477, 4288
    """)
    layout.addWidget(instructions)
    
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
    layout.addWidget(step_group)
    
    # Input text area
    input_text = QTextEdit()
    input_text.setPlaceholderText("Paste your question IDs here...")
    input_text.setMaximumHeight(100)
    layout.addWidget(input_text)
    
    # Output text area
    output_label = QLabel("Anki search query:")
    layout.addWidget(output_label)
    
    output_text = QTextEdit()
    output_text.setReadOnly(True)
    layout.addWidget(output_text)
    
    # Current selection display
    initial_step = "Step 1" if step1_radio.isChecked() else ("Step 3" if step3_radio.isChecked() else "Step 2")
    current_step_label = QLabel(f"Current selection: {initial_step} (remembered from last use)")
    current_step_label.setStyleSheet("color: blue; font-weight: bold;")
    layout.addWidget(current_step_label)
    
    # Buttons
    button_layout = QHBoxLayout()
    
    convert_btn = QPushButton("Convert")
    copy_btn = QPushButton("Copy to Clipboard")
    search_btn = QPushButton("Search in Anki")
    
    # Support button with Ko-fi style
    support_btn = QPushButton("☕ Buy Me a Coffee")
    support_btn.setStyleSheet("""
        QPushButton {
            background-color: #29abe0;
            color: white;
            font-weight: bold;
            border-radius: 5px;
            padding: 5px 10px;
            border: none;
        }
        QPushButton:hover {
            background-color: #1a8cb8;
        }
        QPushButton:pressed {
            background-color: #127096;
        }
    """)
    
    # Review button
    review_btn = QPushButton("⭐ Rate Addon")
    review_btn.setStyleSheet("""
        QPushButton {
            background-color: #ffa500;
            color: white;
            font-weight: bold;
            border-radius: 5px;
            padding: 5px 10px;
            border: none;
        }
        QPushButton:hover {
            background-color: #ff8c00;
        }
        QPushButton:pressed {
            background-color: #e67e00;
        }
    """)
    
    close_btn = QPushButton("Close")
    
    button_layout.addWidget(convert_btn)
    button_layout.addWidget(copy_btn)
    button_layout.addWidget(search_btn)
    button_layout.addWidget(support_btn)
    button_layout.addWidget(review_btn)
    button_layout.addWidget(close_btn)
    
    layout.addLayout(button_layout)
    dialog.setLayout(layout)
    
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
        ids = input_text.toPlainText().strip()
        if not ids:
            showInfo("Please enter some question IDs first.")
            return
        
        try:
            step_type = get_selected_step()
            converted = convert_ids_to_tags(ids, step_type)
            output_text.setPlainText(converted)
        except Exception as e:
            showInfo(f"Error converting IDs: {str(e)}")
    
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
        showInfo(f"Search query for {step} copied to clipboard!")
    
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
    
    def support_clicked():
        """Open Ko-fi support page"""
        openLink("https://ko-fi.com/abdmohrat")
    
    def review_clicked():
        """Open AnkiWeb review page"""
        openLink("https://ankiweb.net/shared/review/699193084")
    
    # Connect buttons
    convert_btn.clicked.connect(convert_clicked)
    copy_btn.clicked.connect(copy_clicked)
    search_btn.clicked.connect(search_clicked)
    support_btn.clicked.connect(support_clicked)
    review_btn.clicked.connect(review_clicked)
    close_btn.clicked.connect(close_clicked)
    
    # Connect radio buttons
    step1_radio.toggled.connect(update_step_label)
    step2_radio.toggled.connect(update_step_label)
    step3_radio.toggled.connect(update_step_label)
    
    # Auto-convert when text changes (with a small delay)
    def on_text_changed():
        QTimer.singleShot(500, convert_clicked)  # 500ms delay
    
    input_text.textChanged.connect(on_text_changed)
    
    dialog.show()

# Add menu item to Tools menu
def add_menu_item():
    action = QAction("USMLE Question ID Converter", mw)
    action.triggered.connect(show_converter_dialog)
    mw.form.menuTools.addAction(action)

# Initialize the addon
add_menu_item()