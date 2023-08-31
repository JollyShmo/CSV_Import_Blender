###########################################################################################
#| [CSV Combiner Application]
#|
#| [Created by:] Jolly Joe
#| [GitHub:] https://github.com/JollyShmo
#| [Version:] 2.0.0
#|
#| [Description:] This script defines a GUI application for combining CSV files together.
#| License: MIT License
#|
#| [Note:] You are free to use and modify this script for your projects.
#| If you find it helpful, please consider giving credit to Jolly Joe and sharing it!
#|
###########################################################################################

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QListWidget, QFileDialog, QTableWidget, QTableWidgetItem, QProgressBar, QInputDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class CombineThread(QThread):
    progress_signal = pyqtSignal(int)
    finished = pyqtSignal(list, int)

    def __init__(self, selected_files):
        super().__init__()
        self.selected_files = selected_files

    def run(self):
        self.combined_data = []

        max_columns = 0
        for file_path in self.selected_files:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                max_columns = max(max_columns, len(lines[0].split(',')))

        total_lines = sum(len(open(file_path).readlines()) for file_path in self.selected_files)
        processed_lines = 0

        for idx, file_path in enumerate(self.selected_files):
            with open(file_path, 'r') as file:
                lines = file.readlines()

                if idx > 0:
                    lines = lines[1:]

                self.combined_data.extend(lines)
                processed_lines += len(lines)
                progress = (processed_lines / total_lines) * 100
                self.progress_signal.emit(int(progress))

        self.finished.emit(self.combined_data, max_columns)

class CSVCombinerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.selected_files = []
        self.combined_data = []

    def init_ui(self):
        self.setWindowTitle('CSV Combiner')
        self.setGeometry(100, 100, 700, 600)
        self.setWindowIcon(QIcon('icon.png'))
        self.setStyleSheet("background-color: #232323;")
        layout = QVBoxLayout()

        self.label = QLabel('Display .csv files to combine:')
        self.label.setStyleSheet("color: red; border: 2px solid black; border-radius: 10px; padding: 2px;")
        layout.addWidget(self.label)

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("background-color: lightgray; border: 2px solid lightgray; border-radius: 10px;")
        layout.addWidget(self.list_widget)

        button_width = 200
        button_height = 40        
        
        self.additional_window = QWidget()
        # Create a button to toggle the visibility of hello_label
        toggle_label_button = QPushButton('❔')
        toggle_label_button.setFixedSize(30, 30)
        toggle_label_button.setStyleSheet("background-color: lightblue; font-size: 16px; font: bold;")
        toggle_label_button.clicked.connect(self.toggle_hello_label)
        layout.addWidget(toggle_label_button)

        # Create a label widget
        hello_label = QLabel("1)Select Files: select all the files you want to combine\n(CTRL + click files) and press open).\n \n2)Combine Files: The first header of the first file will remain \n(all others skip the first row).\n \n3)Save As CSV: exports the combine file into one file.")
        hello_label.setStyleSheet("font-size: 18px; border: 2px dotted; border-radius: 25% solid; padding: 4px; background-color: lightblue;")

        # Create a additional layout for info
        additional_layout = QVBoxLayout()
        additional_layout.addWidget(hello_label)

        self.additional_window.setLayout(additional_layout)

        layout.addWidget(self.additional_window, alignment=Qt.AlignLeft)

        # Create a container widget to hold the entire layout
        container_widget = QWidget()
        container_widget.setLayout(layout)
        self.setCentralWidget(container_widget)
        self.select_button = QPushButton('Select Files')
        self.select_button.setFixedSize(button_width, button_height)
        self.select_button.setStyleSheet("background-color: green; font: bold; color: lightgreen; font-size: 20px; border: 4px solid lightgreen; border-radius: 15px 15px;")
        self.select_button.clicked.connect(self.select_files)
        layout.addWidget(self.select_button)

        self.combine_button = QPushButton('Combine Files')
        self.combine_button.setFixedSize(button_width, button_height)
        self.combine_button.setStyleSheet("background-color: lightblue; font: bold; color: teal; font-size: 20px; border: 4px dotted teal; border-radius: 15px 15px;")       
        self.combine_button.clicked.connect(self.combine_files)
        layout.addWidget(self.combine_button)

        self.export_button = QPushButton('Export CSV')
        self.export_button.setFixedSize(button_width, button_height)
        self.export_button.setStyleSheet("background-color: orange; font: bold; color: darkred; font-size: 20px; border: 4px solid; border-radius: 15px 15px;")       
        self.export_button.clicked.connect(self.export_csv)
        layout.addWidget(self.export_button)

        self.clear_button = QPushButton('Clear')
        self.clear_button.setFixedSize(100, 30)
        self.clear_button.setStyleSheet("background-color: red; font-size: 20px; border: 3px dashed pink; border-radius: 15px;")       
        self.clear_button.clicked.connect(self.clear_data)
        layout.addWidget(self.clear_button)
    
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar, alignment=Qt.AlignTop)
        self.progress_bar.hide()

        self.table_widget = QTableWidget()
        self.table_widget.setStyleSheet("background-color: lightblue; font: bold; font-size: 12px;")
        layout.addWidget(self.table_widget)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    def toggle_hello_label(self):
        self.additional_window.setVisible(not self.additional_window.isVisible())

        # Adjust the layout to ensure proper space allocation
        self.centralWidget().layout().invalidate()
        self.centralWidget().layout().activate()

    def select_files(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        files, _ = QFileDialog.getOpenFileNames(self, "Select .csv Files", "", "CSV Files (*.csv);;All Files (*)", options=options)

        if files:
            self.selected_files = files
            self.list_widget.clear()
            self.list_widget.addItems(files)
            self.list_widget.setStyleSheet("color: lightgreen; font-size: 14px; font: bold; border-radius: 10px;")

    def combine_files(self):
        self.progress_bar.show()
        self.progress_bar.setValue(0)

        self.combine_thread = CombineThread(self.selected_files)
        self.combine_thread.progress_signal.connect(self.update_progress_bar)
        self.combine_thread.finished.connect(self.display_combined_data)  # No need for arguments here
        self.combine_thread.start()

    def update_progress_bar(self, progress):
        self.progress_bar.setValue(progress)

    def display_combined_data(self, data, num_columns):
        self.progress_bar.hide()
        self.table_widget.clear()

        self.table_widget.setRowCount(len(data))
        self.table_widget.setColumnCount(num_columns)

        for i, line in enumerate(data):
            columns = line.strip().split(',')
            for j, column in enumerate(columns):
                item = QTableWidgetItem(column)
                self.table_widget.setItem(i, j, item)

    def export_csv(self):
        export_path, _ = QFileDialog.getSaveFileName(self, "Export as CSV", "", "CSV Files (*.csv);;All Files (*)")
        if export_path:
            with open(export_path, 'w') as file:
                for row in range(self.table_widget.rowCount()):
                    row_data = []
                    for col in range(self.table_widget.columnCount()):
                        item = self.table_widget.item(row, col)
                        if item is not None:
                            row_data.append(item.text())
                    file.write(','.join(row_data) + '\n')
                        
    def rename_button(self, button_input):
        new_name, ok = QInputDialog.getText(self, "Rename Button", "Enter a new name for the button:")
        if ok:
            for index, setting in enumerate(self.game_settings):
                if setting["button_input"] == button_input:
                    setting["button_input"].setText(new_name)
                    self.game_names[index] = new_name
                    return

    def clear_data(self):
        self.selected_files = []
        self.combined_data = []
        self.list_widget.clear()
        self.table_widget.clear()
        self.table_widget.clearContents()
        self.table_widget.setRowCount(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = CSVCombinerApp()
    window.show()
    sys.exit(app.exec_())





