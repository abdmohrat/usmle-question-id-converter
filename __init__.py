# USMLE Question ID Converter Addon for Anki
# Author: abdmohrat
# Version: 1.0.3

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
    dialog.setFixedSize(750, 500)
    
    # Main layout
    main_layout = QHBoxLayout()
    
    # Left side - main content
    left_layout = QVBoxLayout()
    
    # Right side - support buttons
    right_layout = QVBoxLayout()
    right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    
    # Support buttons in top right
    support_btn = QPushButton("☕ Buy Me\na Coffee")
    support_btn.setFixedSize(90, 60)
    support_btn.setStyleSheet("""
        QPushButton {
            background-color: #29abe0;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 8px;
            font-size: 11px;
        }
        QPushButton:hover {
            background-color: #1a8fc4;
        }
    """)
    
    review_btn = QPushButton("⭐ Rate\nAddon")
    review_btn.setFixedSize(90, 60)
    review_btn.setStyleSheet("""
        QPushButton {
            background-color: #f39c12;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 8px;
            font-size: 11px;
        }
        QPushButton:hover {
            background-color: #e67e22;
        }
    """)
    
    right_layout.addWidget(support_btn)
    right_layout.addSpacing(10)
    right_layout.addWidget(review_btn)
    right_layout.addStretch()
    
    # Instructions
    instructions = QLabel("""
    Paste your USMLE question IDs below (comma-separated):
    Example: 21656, 19263, 4466, 12477, 4288
    """)
    left_layout.addWidget(instructions)
    
    # Step selection
    step_group = QGroupBox("Select USMLE Step:")
    step_layout = QHBoxLayout()
    
    step1_radio = QRadioButton("Step 1")
    step2_radio = QRadioButton("Step 2")
    
    # Load saved preference
    config = get_config()
    last_step = config.get("last_selected_step", "Step2")
    if last_step == "Step1":
        step1_radio.setChecked(True)
    else:
        step2_radio.setChecked(True)
    
    step_layout.addWidget(step1_radio)
    step_layout.addWidget(step2_radio)
    step_group.setLayout(step_layout)
    left_layout.addWidget(step_group)
    
    # Input text area
    input_text = QTextEdit()
    input_text.setPlaceholderText("Paste your question IDs here...")
    input_text.setMaximumHeight(100)
    left_layout.addWidget(input_text)
    
    # Output text area
    output_label = QLabel("Anki search query:")
    left_layout.addWidget(output_label)
    
    output_text = QTextEdit()
    output_text.setReadOnly(True)
    left_layout.addWidget(output_text)
    
    # Current selection display
    initial_step = "Step 1" if step1_radio.isChecked() else "Step 2"
    current_step_label = QLabel(f"Current selection: {initial_step} (remembered from last use)")
    current_step_label.setStyleSheet("color: blue; font-weight: bold;")
    left_layout.addWidget(current_step_label)
    
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
    
    left_layout.addLayout(button_layout)
    
    # Combine left and right layouts
    main_layout.addLayout(left_layout)
    main_layout.addLayout(right_layout)
    dialog.setLayout(main_layout)
    
    def get_selected_step():
        return "Step1" if step1_radio.isChecked() else "Step2"
    
    def save_step_preference():
        """Save the current step selection"""
        config = get_config()
        config["last_selected_step"] = get_selected_step()
        save_config(config)
    
    def update_step_label():
        step = "Step 1" if step1_radio.isChecked() else "Step 2"
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
        step = "Step 1" if step1_radio.isChecked() else "Step 2"
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