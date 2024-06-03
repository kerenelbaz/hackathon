import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox, QVBoxLayout, QHBoxLayout, 
    QCalendarWidget, QTimeEdit, QRadioButton, QPushButton, QTextEdit, QButtonGroup
)
from PyQt5.QtCore import QDate, QTime, QDateTime
import pandas as pd
import pandas as pd
from pedestrian import get_fasted_path_with_pedestrian
from car import get_fasted_path_with_car


class TransportationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Transportation App')
        self.setGeometry(100, 100, 700, 600)
        self.setStyleSheet("background-color: #f2f2f2;")

        layout = QVBoxLayout()

        # Source and Destination
        source_destination_layout = QHBoxLayout()
        source_layout = QVBoxLayout()
        source_label = QLabel('Source Station:')
        source_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        self.source_combo = QComboBox()
        self.source_combo.setStyleSheet("""
            QComboBox {
                font-size: 16px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: blue;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #007bff;
                color: white;
            }
            QComboBox::item {
                color: blue;
            }
        """)
        stations = [
            "Gadolinium", "Holmium", "Thallium", "Neodymium", "Thorium",
            "Technetium", "Ytterbium", "Tantalum", "Vanadium", "Neon",
            "Protactinium", "Erbium", "Xenon", "Francium", "Promethium",
            "Astatine", "Argon", "Lanthanum", "Mercury", "Lithium",
            "Sulfur", "Zirconium", "Radon", "Potassium", "Germanium",
            "Cerium", "Hydrogen", "Strontium", "Manganese", "Iron",
            "Krypton", "Arsenic", "Rhenium", "Antimony", "Fluorine",
            "Nitrogen", "Actinium", "Neptunium", "Oxygen", "Ruthenium",
            "Aluminum", "Helium", "Chromium", "Praseodymium", "Cesium",
            "Tellurium", "Lead", "Samarium", "Calcium", "Europium", "Platinum", "Radium",
            "Tin", "Carbon", "Tungsten", "Selenium", "Scandium",
            "Iridium", "Uranium", "Beryllium", "Americium", "Phosphorus",
            "Gallium", "Iodine", "Silicon", "Zinc", "Yttrium",
            "Thulium", "Copper", "Rhodium", "Curium", "Osmium",
            "Barium", "Molybdenum", "Cobalt", "Magnesium", "Silver",
            "Bismuth", "Polonium", "Chlorine", "Indium", "Plutonium",
            "Niobium", "Boron", "Rubidium", "Hafnium", "Bromine",
            "Nickel", "Lutetium", "Dysprosium", "Gold", "Terbium",
            "Palladium", "Sodium", "Cadmium", "Titanium"
        ]
        stations.sort()
        self.source_combo.addItems(stations)
        
        source_layout.addWidget(source_label)
        source_layout.addWidget(self.source_combo)
        
        destination_layout = QVBoxLayout()
        destination_label = QLabel('Destination Station:')
        destination_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.destination_combo = QComboBox()
        self.destination_combo.setStyleSheet("""
            QComboBox {
                font-size: 16px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: blue;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #007bff;
                color: white;
            }
            QComboBox::item {
                color: blue;
            }
        """)
        self.destination_combo.addItems(stations)
        destination_layout.addWidget(destination_label)
        destination_layout.addWidget(self.destination_combo)
        
        source_destination_layout.addLayout(source_layout)
        source_destination_layout.addLayout(destination_layout)
        layout.addLayout(source_destination_layout)

        # Date and Time
        date_time_layout = QVBoxLayout()
        date_layout = QHBoxLayout()
        date_label = QLabel('Date:')
        date_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.date_entry = QCalendarWidget()
        self.date_entry.setMinimumDate(QDate.currentDate())
        self.date_entry.setStyleSheet("font-size: 14px;")
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_entry)
        
        time_layout = QHBoxLayout()
        time_label = QLabel('Time:')
        time_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.time_entry = QTimeEdit()
        self.time_entry.setStyleSheet("font-size: 16px;")
        self.time_entry.setDisplayFormat('HH:mm')
        time_layout.addWidget(time_label)
        time_layout.addWidget(self.time_entry)
        
        date_time_layout.addLayout(date_layout)
        date_time_layout.addLayout(time_layout)
        layout.addLayout(date_time_layout)

        # Preference radio buttons
        preference_layout = QHBoxLayout()
        preference_label = QLabel('Preference:')
        preference_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.preference_group = QButtonGroup()

        self.greenest_path = QRadioButton('Greenest Path')
        self.greenest_path.setStyleSheet("font-size: 16px;")
        self.greenest_path.setChecked(True)
        self.preference_group.addButton(self.greenest_path)

        self.shortest_path_radio = QRadioButton('Fastest Path')
        self.shortest_path_radio.setStyleSheet("font-size: 16px;")
        self.preference_group.addButton(self.shortest_path_radio)

        # self.in_between_radio = QRadioButton('In Between')
        # self.in_between_radio.setStyleSheet("font-size: 16px;")
        # self.preference_group.addButton(self.in_between_radio)

        preference_layout.addWidget(preference_label)
        preference_layout.addWidget(self.greenest_path)
        # preference_layout.addWidget(self.in_between_radio)
        preference_layout.addWidget(self.shortest_path_radio)

        layout.addLayout(preference_layout)

        # Search button
        self.search_button = QPushButton('Search')
        self.search_button.setStyleSheet("font-size: 18px; font-weight: bold; background-color: #007bff; color: white;")
        self.search_button.clicked.connect(self.search)
        layout.addWidget(self.search_button)

        # Additional information textbox
        info_layout = QVBoxLayout()
        info_label = QLabel('Additional Information:')
        info_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.textbox = QTextEdit()
        self.textbox.setStyleSheet("font-size: 16px;")
        info_layout.addWidget(info_label)
        info_layout.addWidget(self.textbox)
        layout.addLayout(info_layout)

        self.setLayout(layout)

    def search(self):
        try:
            source = self.source_combo.currentText()
            destination = self.destination_combo.currentText()
            # selected_date = self.date_entry.selectedDate()
            # selected_time = self.time_entry.time()
            # current_date = QDate.currentDate()
            # current_time = QTime.currentTime()
            
            # selected_date_time = QDateTime(selected_date, selected_time)
            # current_date_time = QDateTime(current_date, current_time)

            # if selected_date_time < current_date_time:
            #     self.textbox.setText("Error: Selected date and time is in the past.")
            #     return
            
            # date_time_obj = selected_date_time.toString('yyyy-MM-dd HH:mm:ss')
            selected_date = self.date_entry.selectedDate().toString('yyyy-MM-dd')
            selected_time = self.time_entry.time().toString('HH:mm')
            date_time_obj = f"{selected_date} {selected_time}:00"

            preference = self.preference_group.checkedButton().text()

            print("Source Station:", source)
            print("Destination Station:", destination)
            print("Date and Time:", date_time_obj)
            print("Preference:", preference)
            
            data = pd.read_csv('data_clean.csv')
            if(preference == 'greenest_path'):
                result_route = get_fasted_path_with_pedestrian(data, source, destination, date_time_obj)
                print(result_route)

                # Display the result
                self.textbox.clear()
                self.textbox.append(f"Fastest route from {source} to {destination} starting at {date_time_obj}:\n")
                self.textbox.append("\n".join(result_route))
            else:
                result_route = get_fasted_path_with_car(data, source, destination, date_time_obj)
                print(result_route)

                # Display the result
                self.textbox.clear()
                self.textbox.append(f"Fastest route from {source} to {destination} starting at {date_time_obj}:\n")
                self.textbox.append("\n".join(result_route))


            # self.textbox.setText(result)
        except Exception as e:
            print("An error occurred:", e)
            self.textbox.setText(f"An error occurred: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TransportationApp()
    ex.show()
    sys.exit(app.exec_())
