


def PyQtShow():
    """Функция для написания GUI на PyQt6"""
    """"""
    print("Привет JSON Стетхом")


"""
```Python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QStackedWidget, QWidget, QLabel, QFrame, QTableWidget, QPushButton, QHeaderView, QTableWidgetItem
# from PyQt6.QtCore import Qt
import utils
import db


class Sidebar(QFrame):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setFixedWidth(150)
        self.setStyleSheet("""
            QFrame {
                background: black;
                color: white;
            }
            QPushButton {
                background: black;
                color: white;
                padding: 10px;
            }
            QPushButton:hover {
                background: grey;
            }
        """)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        passenger_button = QPushButton("Всего пассажирова")
        passenger_button.clicked.connect(lambda _:  self.parent.switch_window(0))
 
        flights_button = QPushButton("Всего рейсов")
        flights_button.clicked.connect(lambda _:  self.parent.switch_window(1))
        layout.addWidget(passenger_button)
        layout.addWidget(flights_button)
        layout.addStretch()

        self.setLayout(layout)
        
        
class MainWindow(QMainWindow):
    """Главное окно"""
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        utils.center_window(self) 
        self.setStyleSheet("""
            color: white;
        """)
        self.main_widget = QWidget()
        self.setWindowTitle("Автобусная остановка")
        layout = QHBoxLayout() 
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.content = QStackedWidget()
        self.content.addWidget(TotalFlightPassengers(self))
        self.content.addWidget(FlightsCount(self))
        
        self.content.setStyleSheet("""
            color: black;
            background: white;
        """)
        self.sidebar = Sidebar(self)
        layout.addWidget(self.sidebar)
        layout.addWidget(self.content)

        self.main_widget.setLayout(layout)
        self.setCentralWidget(self.main_widget)

    
    def switch_window(self, index):
        self.content.setCurrentIndex(index)


class TotalFlightPassengers(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.name = "Все рейсы"
        self.setWindowTitle("Все рейсы")
        main_layout = QVBoxLayout()
        label = QLabel("Total passengers")
        main_layout.addWidget(label)
        self.setLayout(main_layout)


class FlightsCount(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        layout = QVBoxLayout()


        update_table_flights=QPushButton("Обновить рейсы", self)
        update_table_flights.clicked.connect(self.update_flights_table)
        layout.addWidget(update_table_flights)

        self.flights_table = QTableWidget()
        self.flights_table.setColumnCount(2)
        self.flights_table.setHorizontalHeaderLabels(["Код рейса", "Количество рейсов"])
        self.header = self.flights_table.horizontalHeader()
        self.header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.flights_table)

        self.setLayout(layout)
        self.update_flights_table()

    def update_flights_table(self):
        try:
            flights = db.get_flights()
        
            self.flights_table.setRowCount(len(flights))

            for row_idx, flight in enumerate(flights):
                for col_idx, value in enumerate(flight):
                    item = QTableWidgetItem(str(value))
                    self.flights_table.setItem(row_idx, col_idx, item)
        except Exception as e:
            print(f"Ошибка при загрузке данных о рейсах: {e}")

    
    def cancel_main_window():
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

```

```SQL
-- SQLBook: Code
DROP DATABASE IF EXISTS exam;

CREATE DATABASE exam;
USE exam;

CREATE TABLE IF NOT EXISTS buses_marks (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    mark_name VARCHAR(255) NOT NULL UNIQUE
)

CREATE TABLE IF NOT EXISTS buses (
    id INTEGER PRIMARY KEY,
    gos_number VARCHAR(255) NOT NULL UNIQUE,
    mark_id INTEGER NOT NULL,
    capacity INTEGER NOT NULL,
    FOREIGN KEY (mark_id) REFERENCES buses_marks(id)
)


CREATE TABLE IF NOT EXISTS stations (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL
)


create TABLE IF NOT EXISTS flights (
    id INTEGER PRIMARY KEY,
    station_id  INTEGER NOT NULL UNIQUE,
    bus_id INTEGER NOT NULL UNIQUE,
    departure_time DATETIME NOT NULL,
    FOREIGN KEY (bus_id) REFERENCES buses(id),
    FOREIGN KEY (station_id) REFERENCES stations(id)
);


INSERT INTO buses_marks (mark_name) VALUES
('Mercedes-Benz'),
('Volvo'),
('MAN'),
('Scania'),
('sldfkj');

-- Заполнение таблицы buses
INSERT INTO buses (id, gos_number, mark_id, capacity) VALUES
(1, 'A123BC77', 1, 50),
(2, 'B456DE78', 2, 45),
(3, 'C789FG79', 3, 60),
(4, 'D321HI80', 4, 55),
(5, 'D321HI8099', 4, 100);

-- Заполнение таблицы stations
INSERT INTO stations (id, name) VALUES
(1, 'Central Station'),
(2, 'North Station'),
(3, 'South Station'),
(4, 'East Station'),
(5, 'East Stations'),
(6, 'East Stationss');

-- Заполнение таблицы flights
INSERT INTO flights (id, station_id, bus_id, departure_time) VALUES 
(1, 1, 1, '2024-12-22 08:00:00'),
(2, 2, 2, '2024-12-22 09:30:00'),
(3, 3, 3, '2024-12-22 11:00:00'),
(4, 4, 4, '2024-12-22 12:45:00');
(100, 6, 5, '2024-12-22 12:45:00');

CREATE VIEW total_flights as select COUNT(f.id) as total_amount, f.id from flights f join stations s on f.station_id = s.id group by f.id;
CREATE VIEW total_flights_capacity as select f.id, SUM(capacity) from flights f join buses b on f.bus_id = b.id GROUP BY f.id;
```

```python
    import mysql.connector

def create_conn():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="user",
            password="root",
            database="exam",
        )
        
        return conn if conn.is_connected() else None
    except Exception as err:
        print(err)
        print(f"Не получилось подключиться к баззе даннных")
        return None

def init_db():
    """Создание и заполнение таблиц тестовыми данными."""
    conn = create_conn()
    if conn is None:
        return
    
    cursor = conn.cursor()
    try:   
        # Заполнение таблиц тестовыми данными
        cursor.executemany(
            "INSERT INTO buses_marks (mark_name) VALUES (%s);",
            [("Mercedes",), ("Volvo",), ("MAN",)]
        )

        cursor.executemany(
            "INSERT INTO buses (gos_number, mark_id, capacity) VALUES (%s, %s, %s);",
            [
                ("AA1234BB", 1, 50),
                ("CC5678DD", 2, 60),
                ("EE9101FF", 3, 55)
            ]
        )

        cursor.executemany(
            "INSERT INTO stations (name) VALUES (%s);",
            [("Station A",), ("Station B",), ("Station C",)]
        )

        cursor.executemany(
            "INSERT INTO flights (station_id, bus_id, departure_time) VALUES (%s, %s, %s);",
            [
                (1, 1, "2024-12-22 10:00:00"),
                (2, 2, "2024-12-22 12:00:00"),
                (3, 3, "2024-12-22 14:00:00"),
                (1, 2, "2024-12-22 16:00:00"),
                (2, 3, "2024-12-22 18:00:00")
            ]
        )


        conn.commit()
        print("База данных инициализирована успешно.")
    except mysql.connector.Error as e:
        print(f"Ошибка при инициализации базы данных: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def get_flights():
    """Получение данных о рейсах из представления."""
    conn = create_conn()
    if conn is None:
        return []
    
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM total_flights_capacity;")
        flights = cursor.fetchall()
        return flights
    except mysql.connector.Error as e:
        print(f"Ошибка при получении данных о рейсах: {e}")
        return []
    finally:
        cursor.close()
        conn.close()
```


```text
    Вадим ничего не просил
    поэтому тут пусто
```
"""






