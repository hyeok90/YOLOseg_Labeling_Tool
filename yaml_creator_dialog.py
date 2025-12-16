from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QDialogButtonBox, 
    QFileDialog, QPushButton, QGroupBox, QTextEdit, QMessageBox
)
import yaml
import os

class YamlCreatorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create Dataset YAML")
        self.setMinimumWidth(500)
        self.layout = QVBoxLayout(self)

        self.form_layout = QFormLayout()

        # Train path
        self.train_path_edit = QLineEdit()
        self.train_path_edit.setPlaceholderText("Select training images folder...")
        self.train_browse = QPushButton("Browse...")
        self.train_browse.clicked.connect(lambda: self.browse_folder(self.train_path_edit))
        self.form_layout.addRow("Train Images:", self.train_browse)
        self.form_layout.addRow("", self.train_path_edit)

        # Val path
        self.val_path_edit = QLineEdit()
        self.val_path_edit.setPlaceholderText("Select validation images folder...")
        self.val_browse = QPushButton("Browse...")
        self.val_browse.clicked.connect(lambda: self.browse_folder(self.val_path_edit))
        self.form_layout.addRow("Val Images:", self.val_browse)
        self.form_layout.addRow("", self.val_path_edit)

        # Classes
        self.classes_edit = QTextEdit()
        self.classes_edit.setPlaceholderText("Enter class names, one per line.\nExample:\ncat\ndog\ncar")
        self.form_layout.addRow("Classes:", self.classes_edit)

        self.layout.addLayout(self.form_layout)

        # Buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.save_yaml)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

    def browse_folder(self, line_edit):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder:
            line_edit.setText(folder)

    def save_yaml(self):
        train_path = self.train_path_edit.text().strip()
        val_path = self.val_path_edit.text().strip()
        classes_text = self.classes_edit.toPlainText().strip()

        if not train_path or not val_path or not classes_text:
            QMessageBox.warning(self, "Missing Information", "Please fill in all fields.")
            return

        class_names = [line.strip() for line in classes_text.split('\n') if line.strip()]
        names_dict = {i: name for i, name in enumerate(class_names)}

        data = {
            'train': train_path,
            'val': val_path,
            'names': names_dict
        }

        save_path, _ = QFileDialog.getSaveFileName(self, "Save YAML File", "", "YAML Files (*.yaml)")
        if save_path:
            try:
                with open(save_path, 'w') as f:
                    yaml.dump(data, f, sort_keys=False)
                
                QMessageBox.information(self, "Success", f"YAML file saved to:\n{save_path}")
                self.created_file_path = save_path
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save YAML file:\n{e}")
    
    def get_created_file_path(self):
        return getattr(self, 'created_file_path', None)
