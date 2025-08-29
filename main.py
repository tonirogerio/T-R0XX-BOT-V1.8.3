import multiprocessing
import os
import sys
import json
import time
import webbrowser
import win32con
from PIL import ImageGrab
from _ctypes import byref
from pynput import keyboard
import psutil
import win32gui
import win32process
from PyQt6.QtGui import QFont, QIcon, QAction
from PyQt6.QtWidgets import (QGroupBox, QSpinBox, QRadioButton, QTabWidget,
    QApplication, QMainWindow, QMenuBar, QMenu,
    QVBoxLayout, QHBoxLayout, QStackedWidget, QWidget,
    QLabel, QListWidget, QPushButton, QSpacerItem, QSizePolicy, QProgressBar, QCheckBox, QLineEdit, QSlider, QComboBox,
    QInputDialog, QMessageBox, QListView, QScrollBar, QSystemTrayIcon
)
from PyQt6.QtCore import Qt, QTimer, QSize
from mouse import *
import ctypes
from ctypes import windll, Structure, c_long
from game import Game
from pointers import Pointers
from help import Help


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.start_style = """
                        QPushButton {
                            /* Background color of the button */
                            /*background-color: #4CAF50; /* Green */
                            /*color: Black; /* Text color */
                            max-width: 71px; /* Button width */
                            max-height: 20px; /* Button height */
                            border: 2px solid #696969; /* Border color */
                            border-radius: 5px; /* Rounded corners */
                            padding: 2px 2px; /* Padding for better spacing */
                            font-size: 14px; /* Font size */
                            font-weight: bold; /* Font weight */
                            text-align: center; /* Align text in the center */
                            text-decoration: none; /* Remove underline */
                        }

                        QPushButton:hover {
                            /* Style when the mouse hovers over the button */
                            background-color: #66CDAA; /* Slightly darker green */
                            border-color: #696969; /* Match border color with background */
                        }

                        QPushButton:pressed {
                            /* Style when the button is pressed */
                            background-color: #3CB371; /* Even darker green */
                            border-color: #696969; /* Match border color */
                            color: #d4d4d4; /* Change text color */
                        }"""

        self.stop_style = """
            QPushButton {                                                                  
                /* Background color of the button */                                                           
                /*background-color: #4CAF50; /* Green */                                                       
                /*color: Black; /* Text color */                                                               
                max-width: 71px; /* Button width */                                                            
                max-height: 20px; /* Button height */                                                          
                border: 2px solid #696969; /* Border color */                                                  
                border-radius: 5px; /* Rounded corners */                                                      
                padding: 2px 2px; /* Padding for better spacing */                                             
                font-size: 14px; /* Font size */                                                               
                font-weight: bold; /* Font weight */                                                           
                text-align: center; /* Align text in the center */                                             
                text-decoration: none; /* Remove underline */                                                  
            }                                                                                                  
                                                                                                               
            QPushButton:hover {                                                            
                /* Style when the mouse hovers over the button */                                              
                background-color: #DC143C; /* Slightly darker green */                                         
                border-color: #696969; /* Match border color with background */                                
            }                                                                                                  
                                                                                                               
            QPushButton:pressed {                                                          
                /* Style when the button is pressed */                                                         
                background-color: #FF6347; /* Even darker green */                                             
                border-color: #696969; /* Match border color */                                                
                color: #d4d4d4; /* Change text color */                                                        
            }"""

        self.update_style = """
            QPushButton {                                                                
                /* Background color of the button */                                                             
                /*background-color: #4CAF50; /* Green */                                                         
                /*color: Black; /* Text color */                                                                 
                max-width: 160px; /* Button width */                                                              
                max-height: 20px; /* Button height */                                                            
                border: 2px solid #696969; /* Border color */                                                    
                border-radius: 5px; /* Rounded corners */                                                        
                padding: 2px 2px; /* Padding for better spacing */                                               
                font-size: 14px; /* Font size */                                                                 
                font-weight: bold; /* Font weight */                                                             
                text-align: center; /* Align text in the center */                                               
                text-decoration: none; /* Remove underline */                                                    
            }                                                                                                    
                                                                                 
            QPushButton:hover {                                                                                  
                /* Style when the mouse hovers over the button */                                                
                background-color: #00BFFF; /* Slightly darker green */                                           
                border-color: #696969; /* Match border color with background */                                  
            }                                                                                                    
                                                                                 
            QPushButton:pressed {                                                                                
                /* Style when the button is pressed */                                                           
                background-color: #87CEEB; /* Even darker green */                                               
                border-color: #696969; /* Match border color */                                                  
                color: #d4d4d4; /* Change text color */                                                          
            }"""

        self.menu_style = """
            QMenuBar {

                font-size: 12px;
                margin: 0;
                min-height: 25px;
                max-height: 25px;
            }
            QMenuBar::item {
                background: transparent;
                text-align: center;
            }
            QMenuBar::item:selected {
                background: #4a6fa5;
            }
            QMenu {
                background-color: #2e3b4e;
                border: 1px solid #4a6fa5;
            }
            QMenu::item {
                background-color: transparent;
                color: #ffffff;
                margin: 1px 0;
                font-size: 12px;
                text-align: center;
            }
            QMenu::item:selected {
                background-color: #4a6fa5;
                color: #ffffff;
            }
        """

        self.side_button_style = """
                        QPushButton {
                            /* Background color of the button */
                            /*background-color: #4CAF50; /* Green */
                            /*color: Black; /* Text color */
                            min-width: 80px; /* Button width */
                            max-height: 30px; /* Button height */
                            border: 2px solid #696969; /* Border color */
                            border-radius: 5px; /* Rounded corners */
                            padding: 2px 2px; /* Padding for better spacing */
                            font-size: 14px; /* Font size */
                            font-weight: bold; /* Font weight */
                            text-align: center; /* Align text in the center */
                            /*text-decoration: none; /* Remove underline */
                        }

                        QPushButton:hover {
                            /* Style when the mouse hovers over the button */
                            background-color: #415fa1; /* Slightly darker green */
                            border-color: #696969; /* Match border color with background */
                        }

                        QPushButton:pressed {
                            /* Style when the button is pressed */
                            background-color: #F4A460; /* Even darker green */
                            border-color: #696969; /* Match border color */
                            color: #d4d4d4; /* Change text color */
                        }"""

        self.donate_style = """
                        QPushButton {
                            /* Background color of the button */
                            background-color: #cda672; /* Green */
                            color: Black; /* Text color */
                            max-width: 120px; /* Button width */
                            max-height: 40px; /* Button height */
                            border: 2px solid #696969; /* Border color */
                            border-radius: 4px; /* Rounded corners */
                            padding: 2px 2px; /* Padding for better spacing */
                            font-size: 14px; /* Font size */
                            font-weight: bold; /* Font weight */
                            text-align: center; /* Align text in the center */
                            text-decoration: none; /* Remove underline */
                        }

                        QPushButton:hover {
                            /* Style when the mouse hovers over the button */
                            background-color: #36cbe9; /* Slightly darker green */
                            border-color: #696969; /* Match border color with background */
                        }

                        QPushButton:pressed {
                            /* Style when the button is pressed */
                            background-color: #F4A460; /* Even darker green */
                            border-color: #696969; /* Match border color */
                            color: #d4d4d4; /* Change text color */
                        }
        """

        self.unlock = False
        self.game = Game()

        self.setWindowTitle("T-R0XX Bot V1.8.3")
        self.setWindowIcon(QIcon(resource_path("bot.ico")))
        self.setIconSize(QSize(256, 256))
        #self.setGeometry(100, 100, 800, 200)
        self.setFixedSize(850, 600)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowMaximizeButtonHint)
        self._start_pos = None
        self.selected_pid = None  # PID do processo selecionado
        self.character_pid_map = {}  # Dicionário para mapear nomes a PIDs

        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Menu Bar
        # self.create_menu_bar()

        # Layouts
        main_layout = QVBoxLayout(self.central_widget)
        body_layout = QHBoxLayout()

        self.create_side_menu(body_layout)
        self.create_central_area(body_layout)
        self.create_right_list(body_layout)

        main_layout.addLayout(body_layout)
        self.create_footer(main_layout)

        # Load window data on startup
        self.load_window_data()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._start_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self._start_pos:
            self.move(event.globalPosition().toPoint() - self._start_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._start_pos = None
            event.accept()

    def create_menu_bar(self):
        # Cria a barra de menus
        menu_bar = QMenuBar(self)
        menu_bar.setStyleSheet(self.menu_style)
        self.setMenuBar(menu_bar)

        # Adiciona botões ao menu bar com espaçamento
        menu_layout = QHBoxLayout()
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setSpacing(2)

        menu_widget = QWidget()
        menu_widget.setLayout(menu_layout)
        menu_bar.setCornerWidget(menu_widget, Qt.Corner.TopRightCorner)

    def open_url(self, url):
        webbrowser.open(url)

    def create_side_menu(self, parent_layout):
        side_menu = QVBoxLayout()

        # Buttons
        self.home_button = QPushButton("Home")
        self.home_button.setStyleSheet(self.side_button_style)
        self.keys_button = QPushButton("Keys")
        self.keys_button.setStyleSheet(self.side_button_style)
        self.sell_button = QPushButton("Auto Sell")
        self.sell_button.setStyleSheet(self.side_button_style)
        self.bc_button = QPushButton("BC Farm")
        self.bc_button.setStyleSheet(self.side_button_style)
        self.help_button = QPushButton("Help")
        self.help_button.setStyleSheet(self.side_button_style)

        self.website_button = QPushButton("Website")
        self.website_button.setStyleSheet(self.side_button_style)
        # self.website_button.setIcon(QIcon(resource_path("chrome.ico")))
        self.website_button.clicked.connect(lambda: self.open_url("tonyrogerio.com.br"))

        self.youtube_button = QPushButton("YouTube")
        self.youtube_button.setStyleSheet(self.side_button_style)
        # self.youtube_button.setIcon(QIcon(resource_path("youtube.ico")))
        self.youtube_button.clicked.connect(lambda: self.open_url("https://www.youtube.com/@tonyr0xx/videos"))

        self.donate_button = QPushButton("Donate")
        self.donate_button.setStyleSheet(self.donate_style)
        # self.donate_button.setIcon(QIcon(resource_path("donate.ico")))
        self.donate_button.clicked.connect(lambda: self.open_url("tonyrogerio.com.br/donations"))

        # Button actions
        self.home_button.clicked.connect(lambda: self.central_area.setCurrentIndex(0))  # Home no índice 0
        self.keys_button.clicked.connect(lambda: self.central_area.setCurrentIndex(1))  # Keys no índice 1
        self.sell_button.clicked.connect(lambda: self.central_area.setCurrentIndex(2))  # Sell no índice 2
        self.bc_button.clicked.connect(lambda: self.central_area.setCurrentIndex(3))
        self.help_button.clicked.connect(lambda: self.central_area.setCurrentIndex(4))


        # Add buttons to layout
        side_menu.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        side_menu.addWidget(self.home_button)
        side_menu.addWidget(self.keys_button)
        side_menu.addWidget(self.sell_button)
        side_menu.addWidget(self.bc_button)
        side_menu.addWidget(self.help_button)
        side_menu.addWidget(self.website_button)
        side_menu.addWidget(self.youtube_button)
        side_menu.addWidget(self.donate_button)
        side_menu.addStretch()

        parent_layout.addLayout(side_menu)

    def create_central_area(self, parent_layout):
        self.central_area = QStackedWidget()
        parent_layout.addWidget(self.central_area)

        # Adiciona todas as páginas, incluindo Home com valores iniciais
        self.home_page = Home(self, pid=None)  # Inicializa sem PID
        self.keys_page = Keys(self)  # Página Keys
        self.sell_page = Sell(self)  # Página Sell
        self.bc_page = BC(self)
        self.help_page = Help(self)  # Página Help

        # Conecta a instância de Sell à Home
        self.home_page.sell = self.sell_page
        self.home_page.bc = self.bc_page

        self.central_area.addWidget(self.home_page)  # Página Home no índice 0
        self.central_area.addWidget(self.keys_page)  # Página Keys no índice 1
        self.central_area.addWidget(self.sell_page)  # Página Sell no índice 2
        self.central_area.addWidget(self.bc_page)
        self.central_area.addWidget(self.help_page)

    def create_right_list(self, parent_layout):
        self.right_layout_list = QVBoxLayout()

        # Update button
        self.update_button = QPushButton("Update")
        self.update_button.setStyleSheet(self.update_style)
        self.update_button.setMaximumWidth(76)
        self.update_button.setMinimumWidth(76)
        self.update_button.clicked.connect(self.update_list)

        # List widget
        self.right_list = QListWidget()
        self.right_list.setMaximumWidth(180)
        self.right_list.setMinimumWidth(180)

        self.right_list.setStyleSheet("font-weight: bold; font-size: 18px; font-family: Consolas")
        self.right_list.itemClicked.connect(self.on_character_selected)  # Conecta o evento de clique
        self.right_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.right_list.customContextMenuRequested.connect(self.show_context_menu)

        # Add widgets to layout
        self.right_layout_list.addWidget(self.right_list)

        self.right_list_buttons_layout = QHBoxLayout()
        self.right_list_buttons_layout.addWidget(self.home_page.save_button)
        self.right_list_buttons_layout.addWidget(self.update_button)

        self.right_layout_list.addLayout(self.right_list_buttons_layout)

        parent_layout.addLayout(self.right_layout_list)

    def show_context_menu(self, pos):
        context_menu = QMenu(self)
        copy_action = QAction("Copy Name", self)
        copy_action.triggered.connect(self.copy_selected_item)
        context_menu.addAction(copy_action)
        context_menu.exec(self.right_list.mapToGlobal(pos))

    def copy_selected_item(self):
        selected_item = self.right_list.currentItem()
        if selected_item:
            clipboard = QApplication.clipboard()
            clipboard.setText(selected_item.text())

    def create_footer(self, main_layout):
        footer_layout = QHBoxLayout()

        # Footer text
        self.footer = QLabel("")
        self.footer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Start/Stop buttons
        self.start_button = QPushButton("Start")
        self.start_button.setFixedWidth(87)
        self.start_button.setStyleSheet(self.start_style)
        self.start_button.clicked.connect(self.start)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setFixedWidth(87)
        self.stop_button.setStyleSheet(self.stop_style)
        self.stop_button.clicked.connect(self.stop)

        # Footer button layout
        right_buttons_layout = QHBoxLayout()
        right_buttons_layout.addWidget(self.start_button)
        right_buttons_layout.addWidget(self.stop_button)

        footer_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        footer_layout.addWidget(self.footer)
        footer_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        footer_layout.addLayout(right_buttons_layout)

        main_layout.addLayout(footer_layout)

    def find_window_by_title(self):
        hwnds = []
        processes = []
        self.character_pid_map.clear()  # Limpa o mapeamento antes de atualizar

        # Step 1: Find processes with the name "client.exe"
        for proc in psutil.process_iter(['name', 'pid']):
            if proc.info['name'] and proc.info['name'].lower() == "client.exe":
                processes.append(proc.info['pid'])  # Armazena o PID do processo encontrado

        if not processes:
            print("Nenhum processo 'client.exe' encontrado.")
            return

        # Step 2: Find visible windows for these processes
        def enum_callback(hwnd, lparam):
            if win32gui.IsWindowVisible(hwnd):
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                if pid in processes:
                    hwnds.append({'hwnd': hwnd, 'pid': pid, 'name': win32gui.GetWindowText(hwnd)})

        win32gui.EnumWindows(enum_callback, None)

        if not hwnds:
            print("Nenhuma janela visível associada ao 'client.exe' encontrada.")
            return

        # Step 3: Retrieve the character name using Pointers
        for hwnd_entry in hwnds:
            try:
                pointer = Pointers(hwnd_entry['pid'])  # Inicializa o ponteiro para o processo
                char_name = pointer.get_char_name()  # Obtém o nome do personagem
                hwnd_entry['character_name'] = char_name

                # Atualiza o mapeamento de nomes para PIDs
                self.character_pid_map[char_name] = hwnd_entry['pid']
            except Exception as e:
                hwnd_entry['character_name'] = "Home"
                print(f"Erro ao acessar o processo {hwnd_entry['pid']}: {e}")

        # Step 4: Save the data to a JSON file
        with open('characters/hwnd.json', 'w') as file:
            json.dump(hwnds, file, indent=4)

        print("Dados das janelas e personagens salvos em 'hwnd.json'.")

    def set_names(self, client, pid, contains, new_title):
        """
        Modifica o título de uma janela específica com base no PID e no texto do título.

        :param client: Nome do processo (exemplo: "client.exe").
        :param pid: PID do processo da janela que será modificada.
        :param contains: Texto que deve estar no título da janela para ser alterado.
        :param new_title: Novo título a ser definido na janela.
        :return: Lista com os identificadores das janelas alteradas.
        """

        def enum_callback(hwnd, lista):
            if win32gui.IsWindowVisible(hwnd):  # Verifica se a janela está visível
                tittle = win32gui.GetWindowText(hwnd)
                if contains in tittle:  # Verifica se o título contém o texto esperado
                    _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
                    if window_pid == pid:  # Verifica se o PID corresponde ao esperado
                        for proc in psutil.process_iter(['pid', 'name']):
                            if proc.info['pid'] == pid and proc.info['name'].lower() == client.lower():
                                # Altera o título da janela
                                win32gui.SetWindowText(hwnd, new_title)
                                lista.append(hwnd)

        # Lista para armazenar as janelas que foram alteradas
        windows_changed = []
        win32gui.EnumWindows(enum_callback, windows_changed)
        return windows_changed

    def update_list(self):
        try:
            self.find_window_by_title()
            # Verifica se o atributo right_list já foi inicializado
            if hasattr(self, 'right_list'):
                self.load_window_data()
            else:
                # Se right_list ainda não existe, apenas salva os dados para uso posterior
                print("Lista será atualizada quando a interface estiver completamente inicializada.")
        except Exception as e:
            print(f"Erro ao atualizar lista: {e}")

    def load_window_data(self):
        """Load window data from JSON file and update the list."""
        try:
            with open('characters/hwnd.json', 'r') as file:
                hwnd_data = json.load(file)
                self.right_list.clear()
                for item in hwnd_data:
                    # Adicionar apenas o nome do personagem à lista
                    character_name = item.get('character_name', 'Home')
                    self.right_list.addItem(character_name)
        except FileNotFoundError:
            print("Arquivo hwnd.json não encontrado.")

    def on_character_selected(self, item):
        self.unlock = True
        """Evento chamado ao selecionar um personagem na lista."""
        self.character_name = item.text()
        if self.character_name in self.character_pid_map:
            selected_pid = self.character_pid_map[self.character_name]

            # Verifica se o processo ainda existe pelo PID
            if not psutil.pid_exists(selected_pid):
                print(f"Processo com PID {selected_pid} não encontrado. Atualizando lista.")
                # self.update_list()
                return

            # Atualiza o PID em todas as páginas
            self.home_page.update_pid(selected_pid)
            self.sell_page.update_pid(selected_pid)
            self.bc_page.update_pid(selected_pid)
            print(f"Personagem selecionado: {self.character_name}, PID: {selected_pid}")

            client = "client.exe"
            pid = selected_pid
            contains = "Talisman Online"
            new_tittle = self.character_name
            self.set_names(client, pid, contains, new_tittle)

            # Atualiza settings
            self.home_page.load_settings()

        else:
            print("Personagem não encontrado no mapeamento.")

    def start(self):
        if self.unlock:
            if not self.character_name:
                print("Erro: Nenhum personagem selecionado.")
                return
            target = self.character_name
            print("Current Target = ", target)
            self.home_page.save_settings()
            self.game.load_game(target)

    def stop(self):
        if self.unlock:
            target = self.character_name
            self.game.stop_game(target)


class Home(QWidget):

    def __init__(self, main_window, pid=None):
        super().__init__()

        self.sell = None  # Inicializado como None, será definido pela classe Main
        self.bc = None
        self.labels_style = """font-weight: bold; font-size: 14px; font-family: Consolas"""

        save_settings_style = """
            QPushButton {
                /* Background color of the button */
                /*background-color: #4CAF50; /* Green */
                /*color: Black; /* Text color */
                max-width: 120px; /* Button width */
                max-height: 20px; /* Button height */
                border: 2px solid #696969; /* Border color */
                border-radius: 5px; /* Rounded corners */
                padding: 2px 4px; /* Padding for better spacing */
                font-size: 14px; /* Font size */
                font-weight: bold; /* Font weight */
                text-align: center; /* Align text in the center */
                text-decoration: none; /* Remove underline */
            }

            QPushButton:hover {
                /* Style when the mouse hovers over the button */
                background-color: #008B8B; /* Slightly darker green */
                border-color: #696969; /* Match border color with background */
            }

            QPushButton:pressed {
                /* Style when the button is pressed */
                background-color: #3CB371; /* Even darker green */
                border-color: #696969; /* Match border color */
                color: #d4d4d4; /* Change text color */
            }"""

        self.button_style = """
                QPushButton {
                    /* Background color of the button */
                    /*background-color: #4CAF50; /* Green */
                    /*color: Black; /* Text color */
                    /*max-width: 120px; /* Button width */
                    /*max-height: 20px; /* Button height */
                    border: 2px solid #696969; /* Border color */
                    border-radius: 4px; /* Rounded corners */
                    padding: 2px 2px; /* Padding for better spacing */
                    font-size: 12px; /* Font size */
                    font-weight: bold; /* Font weight */
                    text-align: center; /* Align text in the center */
                    text-decoration: none; /* Remove underline */
                }

                QPushButton:hover {
                    /* Style when the mouse hovers over the button */
                    background-color: #415fa1; /* Slightly darker green */
                    border-color: #696969; /* Match border color with background */
                }

                QPushButton:pressed {
                    /* Style when the button is pressed */
                    background-color: #F4A460; /* Even darker green */
                    border-color: #696969; /* Match border color */
                    color: #d4d4d4; /* Change text color */
                }"""

        self.checkbox_style = """
            QCheckBox {
                font-family: Consolas;
                font-size: 16px;
                spacing: 4px;
            }

            QCheckBox::indicator {
                width: 24px;
                height: 24px;
            }

            QCheckBox::indicator:checked {
                image: url(Images/misc/check-on.svg);
            }

            QCheckBox::indicator:unchecked {
                image: url(Images/misc/check-off.svg);
            }
        """

        self.unlock = False
        self._image_create_active = False
        self._image_create_cancelled = False
        self.main_window = main_window
        self.pid = pid  # PID inicial (pode ser None)
        self.char_name = "Home"
        # Garantindo que a lista seja atualizada na inicialização
        if self.char_name == "Home" and not hasattr(main_window, '_list_updated'):
            main_window.update_list()
            main_window._list_updated = True
        self.pointers = None if pid is None else Pointers(pid)

        self.list_class = ["Stamina", "Mana", "Sin Lure/AOE", "Fairy Heal", "Fairy Attack", "Fairy ATK/HEAL", "BC Farm"]
        self.resolution_list = ["800*600", "1024*768", "1280*720", "1280*800", "1920*1080"]

        # Button to save settings
        self.save_button = QPushButton("Save")
        self.save_button.setFixedWidth(76)
        self.save_button.setStyleSheet(save_settings_style)
        self.save_button.clicked.connect(self.save_settings)

        # Button to load settings
        self.load_button = QPushButton("Load Settings")
        self.load_button.clicked.connect(self.load_settings)

        self.home_layout = QVBoxLayout(self)
        self.center_layout = QHBoxLayout()

        # Título da página
        self.title_label = QLabel(f"{self.char_name}")
        self.title_label.setStyleSheet("color: #FF4500; font-weight: bold; font-size: 24px; font-family: Consolas")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Barra de progresso para o HP
        self.hp_bar = QProgressBar(self)
        self.hp_bar.setMinimum(0)
        self.hp_bar.setMaximum(100)
        self.hp_bar.setValue(0)

        self.hp_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #363636;  /* Borda da barra */
                border-radius: 2px;         /* Bordas arredondadas */
                background: #1C1C1C;       /* Cor de fundo */
                font: bold 12px 'Consolas';   /* Fonte da barra */
                text-align: center;        /* Centraliza o texto */
                min-height: 15px;          /* Altura mínima da barra */
                max-height: 15px;
                max-width: 300px;
                min-width: 300px;
                
            }

            QProgressBar::chunk {
                background-color: #DC143C; /* Cor da parte preenchida */
                border-radius: 2px;        /* Bordas arredondadas na parte preenchida */
            }
        """)

        # Timer para atualização periódica
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_hp_bar)
        self.timer.start(100)  # Atualiza a cada 200ms

        # Select class
        self.char_class = QComboBox()
        self.char_class.setFixedHeight(18)
        self.char_class.addItems(self.list_class)
        self.char_class.setMaximumWidth(110)
        self.char_class.setMinimumWidth(110)
        self.char_class_tittle = QLabel("Char Script:")
        self.char_class_tittle.setStyleSheet(
            "color: #FF4500; font-weight: bold; font-size: 14px; font-family: Consolas")
        self.resolution = QComboBox()
        self.resolution.addItems(self.resolution_list)
        self.resolution.setFixedHeight(18)
        self.resolution.setMaximumWidth(100)
        self.resolution.setMinimumWidth(100)
        self.resolution_tittle = QLabel("Graphics:")
        self.resolution_tittle.setStyleSheet(
            "color: #FF4500; font-weight: bold; font-size: 14px; font-family: Consolas")

        # Add widgets to layout
        self.home_layout.addWidget(self.title_label)

        self.hp_bar_layout = QHBoxLayout()
        self.hp_bar_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.hp_bar_layout.addWidget(self.hp_bar)
        self.hp_bar_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.home_layout.addLayout(self.hp_bar_layout)

        self.h0 = QHBoxLayout()
        self.h0.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.h0.addWidget(self.char_class_tittle)
        self.h0.addWidget(self.char_class)
        self.h0.addWidget(self.resolution_tittle)
        self.h0.addWidget(self.resolution)
        self.h0.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        # self.h0.addWidget(self.save_button)
        self.home_layout.addLayout(self.h0)
        self.home_layout.addWidget(QLabel(""))

        # LEFT LAYOUT
        self.left_layout = QVBoxLayout()
        # Slider for LOW_HP
        self.low_hp_slider = QSlider(Qt.Orientation.Horizontal)
        self.low_hp_slider.setRange(10, 100)
        self.low_hp_slider.setValue(40)
        self.low_hp_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.low_hp_slider.setTickInterval(10)
        self.low_hp_slider.valueChanged.connect(self.update_low_hp_label)

        # Label for LOW_HP
        self.low_hp_label = QLabel(f"Low HP: {self.low_hp_slider.value():} % ")
        self.low_hp_label.setStyleSheet(self.labels_style)
        self.low_hp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Slider for LOW_MP
        self.low_mp_slider = QSlider(Qt.Orientation.Horizontal)
        self.low_mp_slider.setRange(10, 100)  # 0 to 100
        self.low_mp_slider.setValue(40)
        self.low_mp_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.low_mp_slider.setTickInterval(10)
        self.low_mp_slider.valueChanged.connect(self.update_low_mp_label)

        # Label for LOW_MP
        self.low_mp_label = QLabel(f"Low MP: {self.low_mp_slider.value()} % ")
        self.low_mp_label.setStyleSheet(self.labels_style)
        self.low_mp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Slider for BUFF_DELAY (in minutes)
        self.buff_delay_slider = QSlider(Qt.Orientation.Horizontal)
        self.buff_delay_slider.setRange(1, 30)  # 1 to 30 minutes
        self.buff_delay_slider.setValue(5)
        self.buff_delay_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.buff_delay_slider.setTickInterval(10)
        self.buff_delay_slider.valueChanged.connect(self.update_buff_delay_label)

        # Label for BUFF_DELAY
        self.buff_delay_label = QLabel(f"Buff Delay: {self.buff_delay_slider.value()} min")
        self.buff_delay_label.setStyleSheet(self.labels_style)
        self.buff_delay_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Slider for PET_FOOD_DELAY (in minutes)
        self.pet_food_delay_slider = QSlider(Qt.Orientation.Horizontal)
        self.pet_food_delay_slider.setRange(1, 50)  # 1 to 30 minutes
        self.pet_food_delay_slider.setValue(45)
        self.pet_food_delay_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.pet_food_delay_slider.setTickInterval(10)
        self.pet_food_delay_slider.valueChanged.connect(self.update_pet_food_delay_label)

        # Label for PET_FOOD_DELAY
        self.pet_food_delay_label = QLabel(f"Pet Food Delay: {self.pet_food_delay_slider.value()} min")
        self.pet_food_delay_label.setStyleSheet(self.labels_style)
        self.pet_food_delay_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Slider for DELETER_DELAY (in minutes)
        self.deleter_delay_slider = QSlider(Qt.Orientation.Horizontal)
        self.deleter_delay_slider.setRange(1, 60)
        self.deleter_delay_slider.setValue(20)
        self.deleter_delay_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.deleter_delay_slider.setTickInterval(10)
        self.deleter_delay_slider.valueChanged.connect(self.update_deleter_delay_label)

        # Label for DELETER_DELAY
        self.deleter_delay_label = QLabel(f"Deleter Delay: {self.deleter_delay_slider.value()} min")
        self.deleter_delay_label.setStyleSheet(self.labels_style)
        self.deleter_delay_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Slider for GET_BACK
        self.get_back_slider = QSlider(Qt.Orientation.Horizontal)
        self.get_back_slider.setRange(0, 50)
        self.get_back_slider.setValue(25)
        self.get_back_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.get_back_slider.setTickInterval(10)
        self.get_back_slider.valueChanged.connect(self.update_get_back_label)

        # Label for GET_BACK
        self.get_back_label = QLabel(f"Max Distance: {self.get_back_slider.value()} m")
        self.get_back_label.setStyleSheet(self.labels_style)
        self.get_back_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Checkbox for DELETER_BOT
        self.deleter_checkbox = QCheckBox("Delete Items")
        self.deleter_checkbox.setStyleSheet(self.checkbox_style)
        self.deleter_checkbox.setChecked(True)

        # Checkbox for GET_BACK (ON/OFF)
        self.get_back_checkbox = QCheckBox("Max Distance System")
        self.get_back_checkbox.setStyleSheet(self.checkbox_style)
        self.get_back_checkbox.setChecked(True)

        # Checkbox for revive ad back
        self.revive_back_checkbox = QCheckBox("Revive and Back")
        self.revive_back_checkbox.setStyleSheet(self.checkbox_style)
        self.revive_back_checkbox.setChecked(True)

        # Checkbox
        self.follow_leader_checkbox = QCheckBox("Fairy Follow Member")
        self.follow_leader_checkbox.setStyleSheet(self.checkbox_style)
        self.follow_leader_checkbox.setChecked(False)

        # Checkbox for debug_ap (ON/OFF)
        self.debug_ap_checkbox = QCheckBox("Debug Auto Pick")
        self.debug_ap_checkbox.setStyleSheet(self.checkbox_style)
        self.debug_ap_checkbox.setChecked(False)

        # checkbox for kill santa
        self.kill_santa = QCheckBox("Kill Santa Mushroom")
        self.kill_santa.setStyleSheet(self.checkbox_style)
        self.kill_santa.setChecked(False)

        # checkbox for mautopick mode
        self.autopick = QCheckBox("Auto Pick")
        self.autopick.setStyleSheet(self.checkbox_style)
        self.autopick.setChecked(False)
        # self.autopick.stateChanged.connect(self.show_autopick_message)

        # checkbox for sell items
        self.sell_items = QCheckBox("Sell Items")
        self.sell_items.setStyleSheet(self.checkbox_style)
        self.sell_items.setChecked(False)

        self.l1 = QHBoxLayout()  # LINHA 1
        self.l1.addWidget(self.low_hp_label)
        self.l1.addWidget(self.low_hp_slider)
        self.l2 = QHBoxLayout()  # LINHA 2
        self.l2.addWidget(self.low_mp_label)
        self.l2.addWidget(self.low_mp_slider)
        self.l3 = QHBoxLayout()
        self.l3.addWidget(self.pet_food_delay_label)
        self.l3.addWidget(self.pet_food_delay_slider)
        self.l4 = QHBoxLayout()
        self.l4.addWidget(self.buff_delay_label)
        self.l4.addWidget(self.buff_delay_slider)
        self.l5 = QHBoxLayout()
        self.l5.addWidget(self.deleter_delay_label)
        self.l5.addWidget(self.deleter_delay_slider)
        self.l6 = QHBoxLayout()
        self.l6.addWidget(self.get_back_label)
        self.l6.addWidget(self.get_back_slider)
        self.l7 = QHBoxLayout()
        # V1.5 removido
        self.l7.addWidget(QLabel(''))
        self.l8 = QHBoxLayout()
        self.l8.addWidget(self.deleter_checkbox)
        self.l8.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.l9 = QHBoxLayout()
        self.l9.addWidget(self.get_back_checkbox)
        self.l9.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.l10 = QHBoxLayout()
        self.l10.addWidget(self.follow_leader_checkbox)
        self.l10.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.l11 = QHBoxLayout()
        self.l11.addWidget(self.revive_back_checkbox)
        self.l11.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.l12 = QHBoxLayout()
        self.l12.addWidget(self.debug_ap_checkbox)
        self.l12.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.l13 = QHBoxLayout()
        self.l13.addWidget(self.kill_santa)
        self.l13.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.l14 = QHBoxLayout()
        self.l14.addWidget(self.autopick)
        self.l14.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.l15 = QHBoxLayout()
        self.l15.addWidget(self.sell_items)
        self.l15.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.left_layout.addLayout(self.l1)
        self.left_layout.addLayout(self.l2)
        self.left_layout.addLayout(self.l3)
        self.left_layout.addLayout(self.l4)
        self.left_layout.addLayout(self.l5)
        self.left_layout.addLayout(self.l6)
        self.left_layout.addLayout(self.l7)
        self.left_layout.addLayout(self.l8)
        self.left_layout.addLayout(self.l9)
        self.left_layout.addLayout(self.l10)  # follow leader
        self.left_layout.addLayout(self.l11)
        self.left_layout.addLayout(self.l12)  # debug_ap
        self.left_layout.addLayout(self.l13)
        self.left_layout.addLayout(self.l14)
        self.left_layout.addLayout(self.l15)
        self.center_layout.addLayout(self.left_layout)

        self.right_layout = QVBoxLayout()

        # Slider for LOW_HP_BATTLE
        self.low_hp_battle_slider = QSlider(Qt.Orientation.Horizontal)
        self.low_hp_battle_slider.setFixedWidth(120)
        self.low_hp_battle_slider.setRange(10, 99)
        self.low_hp_battle_slider.setValue(30)
        self.low_hp_battle_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.low_hp_battle_slider.setTickInterval(10)
        self.low_hp_battle_slider.valueChanged.connect(self.update_low_hp_battle_label)

        # Label for LOW_HP_BATTLE
        self.low_hp_battle_label = QLabel(f"Battle Low HP: {self.low_hp_battle_slider.value():} % ")
        self.low_hp_battle_label.setStyleSheet(self.labels_style)
        self.low_hp_battle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Slider for LOW_MP_BATTLE
        self.low_mp_battle_slider = QSlider(Qt.Orientation.Horizontal)
        self.low_mp_battle_slider.setFixedWidth(120)
        self.low_mp_battle_slider.setRange(10, 99)  # 0 to 100
        self.low_mp_battle_slider.setValue(30)
        self.low_mp_battle_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.low_mp_battle_slider.setTickInterval(10)
        self.low_mp_battle_slider.valueChanged.connect(self.update_low_mp_battle_label)

        # Label for LOW_MP_BATTLE
        self.low_mp_battle_label = QLabel(f"Battle Low MP: {self.low_mp_battle_slider.value()} % ")
        self.low_mp_battle_label.setStyleSheet(self.labels_style)
        self.low_mp_battle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Slider for lure time
        self.lure_time_slider = QSlider(Qt.Orientation.Horizontal)
        self.lure_time_slider.setFixedWidth(120)
        self.lure_time_slider.setRange(0, 15)
        self.lure_time_slider.setValue(0)
        self.lure_time_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.lure_time_slider.setTickInterval(1)
        self.lure_time_slider.valueChanged.connect(self.update_lure_time_label)

        # Label for lure time
        self.lure_time_label = QLabel(f"Set Respaw Time: {self.lure_time_slider.value()} sec")
        self.lure_time_label.setStyleSheet(self.labels_style)
        self.lure_time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.spot_farm_label = QLabel(f"Spot Farm:")
        self.spot_farm_label.setStyleSheet(self.labels_style)
        self.spot_farm_input = QLineEdit("")
        self.spot_farm_input.setMaximumWidth(110)
        self.spot_farm_input.setPlaceholderText("Back after revive")

        self.get_cords_button = QPushButton("Get Cords")
        self.get_cords_button.setStyleSheet(self.button_style)
        self.get_cords_button.setMaximumWidth(110)
        self.get_cords_button.setMinimumWidth(80)
        self.get_cords_button.clicked.connect(self.get_cords)

        # V1.5
        self.spot_test = QPushButton("Spot Farm Test")
        self.spot_test.setStyleSheet(self.button_style)
        self.spot_test.setMaximumWidth(110)
        self.spot_test.setMinimumWidth(110)
        self.spot_test.clicked.connect(self.spot_farm_test)

        self.get_image_button = QPushButton("Get Image")
        self.get_image_button.setStyleSheet(self.button_style)
        self.get_image_button.setMaximumWidth(110)
        self.get_image_button.setMinimumWidth(80)
        self.get_image_button.clicked.connect(self.image_create)
        self.get_image_input = QLineEdit("")
        self.get_image_input.setMaximumWidth(110)
        self.get_image_input.setMinimumWidth(110)
        self.get_image_input.setPlaceholderText("Image name")

        self.r1 = QHBoxLayout()
        self.r1.addWidget(self.low_hp_battle_label)
        self.r1.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.r1.addWidget(self.low_hp_battle_slider)
        self.r2 = QHBoxLayout()
        self.r2.addWidget(self.low_mp_battle_label)
        self.r2.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.r2.addWidget(self.low_mp_battle_slider)
        self.r2_1 = QHBoxLayout()
        self.r2_1.addWidget(self.lure_time_label)
        self.r2_1.addItem(QSpacerItem(1, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.r2_1.addWidget(self.lure_time_slider)
        self.r3 = QHBoxLayout()
        self.r3.addWidget(self.spot_farm_label)
        self.r3.addWidget(self.spot_farm_input)
        self.r5 = QHBoxLayout()
        self.r5.addWidget(self.get_cords_button)
        self.r5.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.r5.addWidget(self.spot_test)
        self.r6 = QHBoxLayout()
        self.r6.addWidget(self.get_image_button)
        self.r6.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.r6.addWidget(self.get_image_input)

        self.right_layout.addLayout(self.r1)
        self.right_layout.addLayout(self.r2)
        self.right_layout.addLayout(self.r2_1)
        self.right_layout.addLayout(self.r3)
        self.right_layout.addLayout(self.r5)
        self.right_layout.addLayout(self.r6)
        self.right_layout.addItem(QSpacerItem(20, 300, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.center_layout.addLayout(self.right_layout)

        self.home_layout.addLayout(self.center_layout)

        # Espaçador final
        # self.home_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.setLayout(self.home_layout)

    # Função para calcular porcentagem de HP
    def hp_bar_percentage(self):
        try:
            max_hp = Pointers(self.pid).get_max_hp()
            current_hp = Pointers(self.pid).get_hp()

            # Verifica se max_hp é válido para evitar divisão por zero
            if max_hp <= 0:
                return 0

            percentage = (current_hp / max_hp) * 100
            rounded_percentage = round(percentage, 2)

            # Garante que o percentual esteja no intervalo esperado
            if rounded_percentage < 0 or rounded_percentage > 100:
                return 0

            return rounded_percentage
        except Exception as e:
            # Log do erro (se necessário)
            # print(f"Erro ao calcular HP: {e}")
            return 0

    # Método para atualizar a barra de HP
    def update_hp_bar(self):
        if self.pid is not None:
            percentage = self.hp_bar_percentage()
            self.hp_bar.setValue(int(percentage))
            self.hp_bar.setFormat(f"{percentage:.2f}% HP")

        else:
            self.hp_bar.setValue(0)
            self.hp_bar.setFormat("0% HP")

    def update_low_hp_label(self):
        self.low_hp_label.setText(f"Low HP: {self.low_hp_slider.value():} % ")

    def update_low_mp_label(self):
        self.low_mp_label.setText(f"Low MP: {self.low_mp_slider.value()} % ")

    def update_low_hp_battle_label(self):
        self.low_hp_battle_label.setText(f"Battle Low HP: {self.low_hp_battle_slider.value():} % ")

    def update_low_mp_battle_label(self):
        self.low_mp_battle_label.setText(f"Battle Low MP: {self.low_mp_battle_slider.value()} % ")

    def update_lure_time_label(self):
        self.lure_time_label.setText(f"Set Respaw Time: {self.lure_time_slider.value()} sec")

    """def show_autopick_message(self, state):
        if state == Qt.CheckState.Checked.value:
            # Criar ícone de bandeja do sistema
            tray_icon = QSystemTrayIcon(self)
            tray_icon.setIcon(self.windowIcon())
            
            # Configurar e exibir a notificação
            tray_icon.setVisible(True)
            tray_icon.showMessage(
                "Auto Pick - Information!",
                "To use the Auto Pick system, enable Lock The View in: Esc/Graphics/Lock The View",
                QSystemTrayIcon.MessageIcon.Information,
                6000  # Duração de 2 segundos
            )
            
            # Configurar um timer para esconder o ícone após a notificação
            QTimer.singleShot(5000, lambda: tray_icon.setVisible(False))"""

    def update_get_back_label(self):
        self.get_back_label.setText(f"Max Distance: {self.get_back_slider.value()} m")

    def update_buff_delay_label(self):
        self.buff_delay_label.setText(f"Buff Delay: {self.buff_delay_slider.value()} min")

    def update_pet_food_delay_label(self):
        self.pet_food_delay_label.setText(f"Pet Food Delay: {self.pet_food_delay_slider.value()} min")

    def update_deleter_delay_label(self):
        self.deleter_delay_label.setText(f"Deleter Delay: {self.deleter_delay_slider.value()} min")

    def image_create(self):
        """Captura a posição do mouse e salva uma área como imagem BMP."""
        if self._image_create_active:
            print("Image capture is already underway.")
            self.main_window.footer.setText("Image capture is already underway.")
            QApplication.processEvents()
            return

        self._image_create_active = True
        self._image_create_cancelled = False

        try:
            image_name = self.get_image_input.text()

            if not image_name.strip():
                print("Canceled operation or invalid entry.")
                self.get_image_input.setPlaceholderText("type image name")
                QApplication.processEvents()
                return

            image_name = image_name.strip()
            file_path = os.path.join("Images", "DELETE", f"{image_name}.bmp")
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            def on_press(key):
                """Handler para o pressionamento de teclas."""
                try:
                    if self._image_create_cancelled:
                        print("Image capture has been canceled.")
                        self.main_window.footer.setText("Image capture has been canceled.")
                        return False

                    if key == keyboard.Key.esc:
                        pt = POINT()
                        windll.user32.GetCursorPos(byref(pt))
                        mouse_x, mouse_y = pt.x, pt.y

                        # Tamanho fixo da captura
                        capture_size = 16
                        start_x = max(mouse_x - capture_size // 2, 0)
                        start_y = max(mouse_y - capture_size // 2, 0)
                        end_x = start_x + capture_size
                        end_y = start_y + capture_size

                        # Validação das coordenadas e captura da imagem
                        try:
                            bbox = (start_x, start_y, end_x, end_y)
                            img = ImageGrab.grab(bbox=bbox)
                            img.save(file_path, format="BMP")
                            print(f"Saved: {file_path}")
                            self.main_window.footer.setText(f"Saved: {file_path}")
                        except Exception as e:
                            print(f"Error: {e}")
                            self.main_window.footer.setText("Error.")

                        return False  # Encerra o listener
                except Exception as e:
                    print(f"Error: {e}")
                    return False  # Encerra o listener

            print("Move the mouse to the desired location and press ESC to capture the image.")
            self.main_window.footer.setText(
                "Move the mouse to the desired location and press ESC to capture the image.")
            QApplication.processEvents()

            # Criação e gerenciamento do listener de forma segura
            with keyboard.Listener(on_press=on_press) as listener:
                listener.join()  # Aguarda até que o listener seja encerrado

        except Exception as e:
            print(f"Image capture error: {e}")

        finally:
            self._image_create_active = False
            print("Finished image capture.")
            self.main_window.footer.setText("")
            self.get_image_input.setPlaceholderText("Image name")

    def cancel_image_create(self):
        """Cancela a captura de imagem."""
        if self._image_create_active:
            self._image_create_cancelled = True
            self.main_window.footer.setText("Image capture has been canceled.")
            QApplication.processEvents()
            print("Image capture has been canceled.")

    def get_cords(self):
        """Captura a posição do mouse relativa à janela selecionada ao pressionar ESC."""
        if not self.pid:
            print("No window have been selected.")
            self.main_window.footer.setText("Select a window before capturing the coordinates.")
            QApplication.processEvents()
            return

        # Impede execução simultânea
        if getattr(self, "_spot_farm_active", False):
            print("The coordinate capture is already underway.")
            self.main_window.footer.setText("The coordinate capture is already underway.")
            QApplication.processEvents()
            return

        self._get_cords_active = True
        self._get_cords_cancelled = False

        try:
            # Obtém o identificador da janela (HWND) pelo PID
            hwnd = None

            def enum_callback(handle, _):
                _, process_pid = win32process.GetWindowThreadProcessId(handle)
                if process_pid == self.pid and win32gui.IsWindowVisible(handle):
                    nonlocal hwnd
                    hwnd = handle

            win32gui.EnumWindows(enum_callback, None)

            if not hwnd:
                print("The selected window could not be found.")
                self.main_window.footer.setText("The selected window could not be found.")
                QApplication.processEvents()
                self._get_cords_active = False
                return

            print(f"Janela selecionada (HWND): {hwnd}")

            # Obtém as coordenadas do cliente da janela
            client_pos = win32gui.ClientToScreen(hwnd, (0, 0))
            client_x, client_y = client_pos

            def on_press(key):
                try:
                    if self._get_cords_cancelled:
                        print("Coordinate capture has been canceled.")
                        return False

                    if key == keyboard.Key.esc:
                        pt = POINT()
                        windll.user32.GetCursorPos(ctypes.byref(pt))
                        mouse_x, mouse_y = pt.x, pt.y

                        # Calcula a posição relativa
                        relative_x = mouse_x - client_x
                        relative_y = mouse_y - client_y

                        # Validação dos valores capturados
                        if isinstance(relative_x, int) and isinstance(relative_y, int):
                            # Atualiza o campo de entrada
                            # self.get_cords_input.setText(f"{relative_x},{relative_y}")
                            self.spot_farm_input.setText(f"{relative_x},{relative_y}")  # V1.5
                            print(f"Coordenadas relativas capturadas: {relative_x},{relative_y}")
                        else:
                            print("Erro: Coordenadas capturadas são inválidas.")
                            self.main_window.footer.setText("Error when capturing coordinates.")
                            return False

                        self.main_window.footer.setText("")
                        QApplication.processEvents()
                        return False  # Encerra o listener
                except Exception as e:
                    print(f"Erro no listener de teclado: {e}")
                    self.main_window.footer.setText("Error when capturing coordinates.")
                    QApplication.processEvents()
                    return False  # Garante que o listener será encerrado

            self.main_window.footer.setText(
                "Move the mouse to the desired location and press ESC to capture the coordinates."
            )
            QApplication.processEvents()

            # Criação e gerenciamento do listener de forma segura
            listener = keyboard.Listener(on_press=on_press)
            listener.start()
            listener.wait()  # Aguarda até que o listener seja encerrado

        except Exception as e:
            print(f"Erro ao capturar posição relativa: {e}")
            self.main_window.footer.setText("Error when capturing coordinates.")
            QApplication.processEvents()

        finally:
            self._get_cords_active = False
            print("Captura de coordenadas finalizada.")

    def cancel_get_cords(self):
        """Cancela a captura de coordenadas."""
        if getattr(self, "_get_cords_active", False):
            self._get_cords_cancelled = True
            self.main_window.footer.setText("Captura de coordenadas cancelada.")
            QApplication.processEvents()
            print("Captura de coordenadas foi cancelada.")

    def cords_test_l(self):
        try:
            # Abrir e ler o arquivo JSON
            file_name = f"characters/{self.char_name}.json"
            with open(file_name, "r") as file:
                hwnd_data = json.load(file)

            # Verificar se o JSON contém o `CHAR_NAME` esperado
            if hwnd_data.get("CHAR_NAME") == self.char_name:
                hwnd = hwnd_data["HWND"]
                spot = hwnd_data["CORDS"]  # Exemplo: "59,83"

                # Separar as coordenadas
                spot_split = spot.split(",")  # ["59", "83"]
                xPos = int(spot_split[0])  # Converte o primeiro valor para inteiro
                yPos = int(spot_split[1])  # Converte o segundo valor para inteiro

                print(f"Character: {self.char_name}, HWND: {hwnd}, Spot: ({xPos}, {yPos})")

                # Realizar o clique no formato adequado
                time.sleep(0.1)
                left(hwnd, xPos, yPos)
                return hwnd
            else:
                # Caso o `CHAR_NAME` não corresponda
                print(f"No HWND found for character: {self.char_name}")
                return None

        except FileNotFoundError:
            print("Error: JSON file not found.")
        except json.JSONDecodeError:
            print("Error: JSON file is not properly formatted.")
        except KeyError as e:
            print(f"Error: Missing key in JSON: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def cords_test_r(self):
        try:
            # Abrir e ler o arquivo JSON
            file_name = f"characters/{self.char_name}.json"
            with open(file_name, "r") as file:
                hwnd_data = json.load(file)

            # Verificar se o JSON contém o `CHAR_NAME` esperado
            if hwnd_data.get("CHAR_NAME") == self.char_name:
                hwnd = hwnd_data["HWND"]
                spot = hwnd_data["CORDS"]  # Exemplo: "59,83"

                # Separar as coordenadas
                spot_split = spot.split(",")  # ["59", "83"]
                xPos = int(spot_split[0])  # Converte o primeiro valor para inteiro
                yPos = int(spot_split[1])  # Converte o segundo valor para inteiro

                print(f"Character: {self.char_name}, HWND: {hwnd}, Spot: ({xPos}, {yPos})")

                # Realizar o clique no formato adequado
                time.sleep(0.1)
                right(hwnd, xPos, yPos)
                return hwnd
            else:
                # Caso o `CHAR_NAME` não corresponda
                print(f"No HWND found for character: {self.char_name}")
                return None

        except FileNotFoundError:
            print("Error: JSON file not found.")
        except json.JSONDecodeError:
            print("Error: JSON file is not properly formatted.")
        except KeyError as e:
            print(f"Error: Missing key in JSON: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    # V1.5
    def spot_farm_test(self):
        try:
            # Abrir e ler o arquivo JSON
            file_name = f"characters/{self.char_name}.json"
            with open(file_name, "r") as file:
                hwnd_data = json.load(file)

            # Verificar se o JSON contém o `CHAR_NAME` esperado
            if hwnd_data.get("CHAR_NAME") == self.char_name:
                hwnd = hwnd_data["HWND"]
                spot = hwnd_data["SPOT_FARM"]  # Exemplo: "59,83"

                # Separar as coordenadas
                spot_split = spot.split(",")  # ["59", "83"]
                xPos = int(spot_split[0])  # Converte o primeiro valor para inteiro
                yPos = int(spot_split[1])  # Converte o segundo valor para inteiro

                print(f"Character: {self.char_name}, HWND: {hwnd}, Spot: ({xPos}, {yPos})")

                # Realizar o clique no formato adequado
                time.sleep(0.1)
                right(hwnd, xPos - 20, yPos - 20)
                time.sleep(0.2)
                right(hwnd, xPos + 20, yPos + 20)
                time.sleep(0.2)
                right(hwnd, xPos, yPos)
                time.sleep(0.1)
                return hwnd
            else:
                # Caso o `CHAR_NAME` não corresponda
                print(f"No HWND found for character: {self.char_name}")
                return None

        except FileNotFoundError:
            print("Error: JSON file not found.")
        except json.JSONDecodeError:
            print("Error: JSON file is not properly formatted.")
        except KeyError as e:
            print(f"Error: Missing key in JSON: {e}")
        except Exception as e:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("Set (Spot Farm) coordinates and press (Save) before test.")
            msg.setDefaultButton(QMessageBox.StandardButton.Ok)
            msg.setStyleSheet("QLabel { font-size: 14px; }")
            msg.exec()
            print(f"An unexpected error occurred: {e}")

    def save_settings(self):
        if self.unlock:
            with open('characters/hwnd.json', 'r') as file:
                hwnd_data = json.load(file)

            # Loop through the JSON data to find the matching character_name
            for item in hwnd_data:
                if item["character_name"] == self.char_name:
                    hwnd = item["hwnd"]
                    pid = item["pid"]
            settings = {
                "CHAR_NAME": self.char_name,
                "CHAR_TYPE": self.char_class.currentText(),
                "HWND": hwnd,
                "PID": pid,
                "RESOLUTION": self.resolution.currentText(),
                "LOW_HP": self.low_hp_slider.value(),
                "LOW_MP": self.low_mp_slider.value(),
                "BATTLE_LOW_HP": self.low_hp_battle_slider.value(),
                "BATTLE_LOW_MP": self.low_mp_battle_slider.value(),
                "LURE_TIME": self.lure_time_slider.value(),
                "PET_FOOD_DELAY": self.pet_food_delay_slider.value(),
                "BUFF_DELAY": self.buff_delay_slider.value(),
                "DELETER_BOT": "ON" if self.deleter_checkbox.isChecked() else "OFF",
                "DELETER_DELAY": self.deleter_delay_slider.value(),
                "SPOT_FARM": self.spot_farm_input.text(),
                "GET_BACK": "ON" if self.get_back_checkbox.isChecked() else "OFF",
                "FOLLOW_LEADER": "ON" if self.follow_leader_checkbox.isChecked() else "OFF",
                "DISTANCE": self.get_back_slider.value(),
                "REVIVE_AND_BACK": "ON" if self.revive_back_checkbox.isChecked() else "OFF",
                "DEBUG_AP": "ON" if self.debug_ap_checkbox.isChecked() else "OFF",
                "AUTO_PICK": "ON" if self.autopick.isChecked() else "OFF",
                "SELL_ITEMS": "ON" if self.sell_items.isChecked() else "OFF",
                "KILL_SANTA": "ON" if self.kill_santa.isChecked() else "OFF",
                "NPC_NAME": self.sell.npc_name_input.text(),
                "NPC_COORDS": self.sell.npc_coords_input.text(),
                "USE_TELEPORT": "ON" if self.sell.return_charm_checkbox.isChecked() else "OFF",
                "TELEPORT": self.sell.return_charm_shortcut_input.text(),
                "USE_MOUNT": "ON" if self.sell.mount_checkbox.isChecked() else "OFF",
                "MAX_ITEMS": self.sell.max_items_slider.value(),
                "INITIAL_SLOT": self.sell.initial_slot_input.text(),
                "CITY_COORDS": self.sell.city_input.text(),
                "SELL_ITEM_COORDS": self.sell.sell_item_coords_input.text(),
                "SELL_NPC_COORDS": self.sell.npc_talk_input.text(),
                "SURROUNDS_COORDS": self.sell.surrounds_input.text(),
                "SURR_INPUT_COORDS": self.sell.surr_input_input.text(),
                "SURR_CLOSE_COORDS": self.sell.surr_close_input.text(),
                "FIRST_LINK_COORDS": self.sell.first_link_input.text(),
                "SELL_BUTTON_COORDS": self.sell.sell_button_input.text(),
                "TELEPORT_GUILD": self.bc.return_guild_input.text(),
                "TELEPORT_STONE": self.bc.return_stone_input.text(),
                "BUY_CHARM": "ON" if self.bc.buy_return_checkbox.isChecked() else "OFF",
                "USE_GUILD": "ON" if self.bc.guild_teleport_checkbox.isChecked() else "OFF",
                # "MEMBER_NAME": self.bc.member_name_input.text(),
                "MEMBER_RESETER": "ON" if self.bc.member_reseter.isChecked() else "OFF",
                "MEMBER_FARMER": "ON" if self.bc.member_farmer.isChecked() else "OFF",
                "RETURN_EVERY": self.bc.return_input.text(),
                "STANDART_ROUTE": "ON" if self.bc.standart_route.isChecked() else "OFF",
                "SAFE_ROUTE": "ON" if self.bc.safe_route.isChecked() else "OFF",
                "BC_STAMINA": "ON" if self.bc.stam.isChecked() else "OFF",
                "BC_MANA": "ON" if self.bc.man.isChecked() else "OFF",
                "BC_FAIRY": "ON" if self.bc.fair.isChecked() else "OFF",
                "USE_AOE": "ON" if self.bc.use_aoe.isChecked() else "OFF",
                "USE_AOE_UNTIL": self.bc.use_aoe_slider.value(),
                "STAMINA_COMBO": "ON" if self.bc.stam_combo_checkbox.isChecked() else "OFF",
                "COMBO": self.bc.stam_combo_slider.value(),
                "BC_ATK_1": self.bc.skill_1_input.text(),
                "BC_ATK_2": self.bc.skill_2_input.text(),
                "BC_ATK_3": self.bc.skill_3_input.text(),
                "BC_ATK_AOE": self.bc.skill_4_input.text(),
                "BREAK_SOUL": self.bc.skill_5_input.text(),
                "BC_ATK_COMBO": self.bc.stam_skill_combo_input.text(),
                "ATK_DELAY": self.bc.skill_delay_slider.value(),
                "BC_MOUNT": self.bc.mount_input.text(),
                "BC_MOUNT_SPEED": self.bc.mount_speed_input.text(),
                "BC_PET_FOOD": self.bc.pet_fo_input.text(),
                "BC_POT_HP": self.bc.pot_hp_input.text(),
                "BC_POT_MP": self.bc.pot_mp_input.text(),
                "BC_POT_HP_BATTLE": self.bc.pot_hp_battle_input.text(),
                "BC_POT_MP_BATTLE": self.bc.pot_mp_battle_input.text(),
                "BC_SIT": self.bc.pot_sit_input.text(),
                "BC_WIZZ_SUPER": self.bc.wizz_super_input.text(),
                "BC_HEALING_SPELL": self.bc.healing_input.text(),
                "BC_LOW_HP": self.bc.bc_low_hp_slider.value(),
                "BC_LOW_MP": self.bc.bc_low_mp_slider.value(),
                "BC_BATTLE_LOW_HP": self.bc.bc_low_hp_battle_slider.value(),
                "BC_BATTLE_LOW_MP": self.bc.bc_low_mp_battle_slider.value(),
                "PICK_BOX": "ON" if self.bc.treasure_box.isChecked() else "OFF",
                "MANUAL_PICK": "ON" if self.bc.manual_pick.isChecked() else "OFF",
            }
            try:
                file_name = f"characters/{self.char_name}.json"

                with open(file_name, "w") as json_file:
                    json.dump(settings, json_file, indent=4)
                print("Settings saved.")
            except Exception as e:
                print(f"Error saving settings: {e}")

    def load_settings(self):
        try:
            file_name = f"characters/{self.char_name}.json"

            with open(file_name, "r") as json_file:
                settings = json.load(json_file)
                self.char_class.setCurrentText(settings["CHAR_TYPE"])
                self.resolution.setCurrentText(settings["RESOLUTION"])
                self.low_hp_slider.setValue(int(settings["LOW_HP"]))
                self.low_mp_slider.setValue(int(settings["LOW_MP"]))
                self.low_hp_battle_slider.setValue(int(settings["BATTLE_LOW_HP"]))
                self.low_mp_battle_slider.setValue(int(settings["BATTLE_LOW_MP"]))
                self.lure_time_slider.setValue(int(settings["LURE_TIME"]))
                self.pet_food_delay_slider.setValue(settings["PET_FOOD_DELAY"])
                self.buff_delay_slider.setValue(settings["BUFF_DELAY"])
                self.deleter_checkbox.setChecked(settings["DELETER_BOT"] == "ON")
                self.deleter_delay_slider.setValue(settings["DELETER_DELAY"])
                self.spot_farm_input.setText(settings["SPOT_FARM"])
                self.get_back_checkbox.setChecked(settings["GET_BACK"] == "ON")
                self.follow_leader_checkbox.setChecked(settings["FOLLOW_LEADER"] == "ON")
                self.get_back_slider.setValue(settings["DISTANCE"])
                self.revive_back_checkbox.setChecked(settings["REVIVE_AND_BACK"] == "ON")
                self.debug_ap_checkbox.setChecked(settings["DEBUG_AP"] == "ON")
                self.autopick.setChecked(settings["AUTO_PICK"] == "ON")
                self.sell_items.setChecked(settings["SELL_ITEMS"] == "ON")
                self.kill_santa.setChecked(settings["KILL_SANTA"] == "ON")
                self.sell.npc_name_input.setText(settings["NPC_NAME"])
                self.sell.npc_coords_input.setText(settings["NPC_COORDS"])
                self.sell.return_charm_checkbox.setChecked(settings["USE_TELEPORT"] == "ON")
                self.sell.return_charm_shortcut_input.setText(settings["TELEPORT"])
                self.sell.mount_checkbox.setChecked(settings["USE_MOUNT"] == "ON")
                self.sell.max_items_slider.setValue(settings["MAX_ITEMS"])
                self.sell.initial_slot_input.setText(settings["INITIAL_SLOT"])
                self.sell.city_input.setText(settings["CITY_COORDS"])
                self.sell.sell_item_coords_input.setText(settings["SELL_ITEM_COORDS"])
                self.sell.npc_talk_input.setText(settings["SELL_NPC_COORDS"])
                self.sell.surrounds_input.setText(settings["SURROUNDS_COORDS"])
                self.sell.surr_input_input.setText(settings["SURR_INPUT_COORDS"])
                self.sell.surr_close_input.setText(settings["SURR_CLOSE_COORDS"])
                self.sell.first_link_input.setText(settings["FIRST_LINK_COORDS"])
                self.sell.sell_button_input.setText(settings["SELL_BUTTON_COORDS"])
                self.bc.return_guild_input.setText(settings["TELEPORT_GUILD"])
                self.bc.return_stone_input.setText(settings["TELEPORT_STONE"])
                self.bc.buy_return_checkbox.setChecked(settings["BUY_CHARM"] == "ON")
                self.bc.guild_teleport_checkbox.setChecked(settings["USE_GUILD"] == "ON")
                # self.bc.member_name_input.setText(settings["MEMBER_NAME"])
                self.bc.member_reseter.setChecked(settings["MEMBER_RESETER"] == "ON")
                self.bc.member_farmer.setChecked(settings["MEMBER_FARMER"] == "ON")
                self.bc.return_input.setText(settings["RETURN_EVERY"])
                self.bc.standart_route.setChecked(settings["STANDART_ROUTE"] == "ON")
                self.bc.safe_route.setChecked(settings["SAFE_ROUTE"] == "ON")
                self.bc.stam.setChecked(settings["BC_STAMINA"] == "ON")
                self.bc.man.setChecked(settings["BC_MANA"] == "ON")
                self.bc.fair.setChecked(settings["BC_FAIRY"] == "ON")
                self.bc.use_aoe.setChecked(settings["USE_AOE"] == "ON")
                self.bc.use_aoe_slider.setValue(int(settings["USE_AOE_UNTIL"]))
                self.bc.stam_combo_checkbox.setChecked(settings["STAMINA_COMBO"] == "ON")
                self.bc.stam_combo_slider.setValue(int(settings["COMBO"]))
                self.bc.skill_1_input.setText(settings["BC_ATK_1"])
                self.bc.skill_2_input.setText(settings["BC_ATK_2"])
                self.bc.skill_3_input.setText(settings["BC_ATK_3"])
                self.bc.skill_4_input.setText(settings["BC_ATK_AOE"])
                self.bc.skill_5_input.setText(settings["BREAK_SOUL"])
                self.bc.stam_skill_combo_input.setText(settings["BC_ATK_COMBO"])
                self.bc.skill_delay_slider.setValue(int(settings["ATK_DELAY"]))
                self.bc.mount_input.setText(settings["BC_MOUNT"])
                self.bc.mount_speed_input.setText(settings["BC_MOUNT_SPEED"])
                self.bc.pet_fo_input.setText(settings["BC_PET_FOOD"])
                self.bc.pot_hp_input.setText(settings["BC_POT_HP"])
                self.bc.pot_mp_input.setText(settings["BC_POT_MP"])
                self.bc.pot_hp_battle_input.setText(settings["BC_POT_HP_BATTLE"])
                self.bc.pot_mp_battle_input.setText(settings["BC_POT_MP_BATTLE"])
                self.bc.pot_sit_input.setText(settings["BC_SIT"])
                self.bc.wizz_super_input.setText(settings["BC_WIZZ_SUPER"])
                self.bc.healing_input.setText(settings["BC_HEALING_SPELL"])
                self.bc.bc_low_hp_slider.setValue(int(settings["BC_LOW_HP"]))
                self.bc.bc_low_mp_slider.setValue(int(settings["BC_LOW_MP"]))
                self.bc.bc_low_hp_battle_slider.setValue(int(settings["BC_BATTLE_LOW_HP"]))
                self.bc.bc_low_mp_battle_slider.setValue(int(settings["BC_BATTLE_LOW_MP"]))
                self.bc.treasure_box.setChecked(settings["PICK_BOX"] == "ON")
                self.bc.manual_pick.setChecked(settings["MANUAL_PICK"] == "ON")

                print("Settings loaded.")
        except Exception as e:
            print(f"Error loading settings for {self.char_name}: {e}") # Adicionado para depuração
            import traceback # Adicionado para depuração
            traceback.print_exc() # Adicionado para depuração
            print(f"Saving new settings for {self.char_name}.")
            self.save_settings()

    def update_pid(self, pid):
        self.unlock = True
        """Atualiza o PID e o nome do personagem dinamicamente."""
        self.pid = pid
        self.pointers = Pointers(self.pid)

        self.char_name = self.pointers.get_char_name()
        self.title_label.setText(f"{self.char_name}")


class Sell(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.home = Home(main_window)
        self.char_name = "Home"
        self.pid = None
        self.pointers = None
        self.unlock = False

        self.checkbox_style = """
                    QCheckBox {
                        font-family: Consolas;
                        font-size: 16px;
                        spacing: 2px;
                    }

                    QCheckBox::indicator {
                        width: 20px;
                        height: 20px;
                    }

                    QCheckBox::indicator:checked {
                        image: url(Images/misc/check-on.svg);
                    }

                    QCheckBox::indicator:unchecked {
                        image: url(Images/misc/check-off.svg);
                    }
                """

        self.button_style = """
                QPushButton {
                    /* Background color of the button */
                    /*background-color: #4CAF50; /* Green */
                    /*color: Black; /* Text color */
                    /*max-width: 120px; /* Button width */
                    /*max-height: 20px; /* Button height */
                    border: 2px solid #696969; /* Border color */
                    border-radius: 4px; /* Rounded corners */
                    padding: 2px 2px; /* Padding for better spacing */
                    font-size: 12px; /* Font size */
                    font-weight: bold; /* Font weight */
                    text-align: center; /* Align text in the center */
                    text-decoration: none; /* Remove underline */
                }

                QPushButton:hover {
                    /* Style when the mouse hovers over the button */
                    background-color: #415fa1; /* Slightly darker green */
                    border-color: #696969; /* Match border color with background */
                }

                QPushButton:pressed {
                    /* Style when the button is pressed */
                    background-color: #F4A460; /* Even darker green */
                    border-color: #696969; /* Match border color */
                    color: #d4d4d4; /* Change text color */
                }"""

        # Layout principal
        self.sell_layout = QVBoxLayout(self)

        # Título
        self.title_label = QLabel(f"Sell Settings for {self.char_name}")
        self.title_label.setStyleSheet("color: #F04500; font-weight: bold; font-size: 24px; font-family: Consolas")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.get_npc_info = QPushButton("Get NPC Info")
        self.get_npc_info.setStyleSheet(self.button_style)
        self.get_npc_info.setFixedWidth(100)
        self.get_npc_info.clicked.connect(self.npc_info)

        # Input para nome do NPC
        self.npc_name_label = QLabel("Name:")
        self.npc_name_label.setStyleSheet("font-weight: bold; font-size: 14px; font-family: Consolas")
        self.npc_name_input = QLineEdit("Npc Name Here")
        self.npc_name_input.setStyleSheet("font-size: 14px; font-family: Consolas")
        self.npc_name_input.setFixedWidth(200)
        self.npc_name_input.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Input para coordenadas do NPC
        self.npc_coords_label = QLabel("Coords:")
        self.npc_coords_label.setStyleSheet("font-weight: bold; font-size: 14px; font-family: Consolas")
        self.npc_coords_input = QLineEdit("0,0")
        self.npc_coords_input.setStyleSheet("font-size: 14px; font-family: Consolas")
        self.npc_coords_input.setFixedWidth(100)
        self.npc_coords_input.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Layout horizontal para o input de coordenadas
        self.npc_info_layout = QHBoxLayout()
        #self.npc_info_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.npc_info_layout.addWidget(self.get_npc_info)
        self.npc_info_layout.addWidget(self.npc_name_label)
        self.npc_info_layout.addWidget(self.npc_name_input)
        self.npc_info_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.npc_info_layout.addWidget(self.npc_coords_label)
        self.npc_info_layout.addWidget(self.npc_coords_input)
        self.npc_info_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Layout para o return charm
        self.return_charm_layout = QHBoxLayout()
        # self.return_charm_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.return_charm_label = QLabel("Teleport Stone/Return Charm.")
        self.return_charm_label.setStyleSheet("font-weight: bold; font-size: 16px; font-family: Consolas")
        self.return_charm_checkbox = QCheckBox()
        self.return_charm_checkbox.setStyleSheet(self.checkbox_style)
        # self.return_charm_checkbox.setFixedSize(30, 30)
        self.return_charm_shortcut_label = QLabel("Shortcut:")
        self.return_charm_shortcut_label.setStyleSheet("font-weight: bold; font-size: 16px; font-family: Consolas")
        self.return_charm_shortcut_input = QLineEdit("F9")
        self.return_charm_shortcut_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.return_charm_shortcut_input.setFixedSize(60, 24)
        self.return_charm_shortcut_input.setStyleSheet("font-size: 18px; font-family: Consolas")
        self.return_charm_layout.addWidget(self.return_charm_checkbox)
        self.return_charm_layout.addWidget(self.return_charm_label)
        self.return_charm_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.return_charm_layout.addWidget(self.return_charm_shortcut_label)
        self.return_charm_layout.addWidget(self.return_charm_shortcut_input)
        self.return_charm_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Layout para Use Mount
        self.mount_layout = QHBoxLayout()
        self.mount_checkbox = QCheckBox()
        self.mount_checkbox.setStyleSheet(self.checkbox_style)
        self.mount_label = QLabel("Use Mount.")
        self.mount_label.setStyleSheet("font-weight: bold; font-size: 16px; font-family: Consolas")
        self.mount_layout.addWidget(self.mount_checkbox)
        self.mount_layout.addWidget(self.mount_label)
        self.mount_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Layout para Config
        self.config_layout = QVBoxLayout()

        # max items
        self.max_items_slider = QSlider(Qt.Orientation.Horizontal)
        self.max_items_slider.setRange(1, 60)
        self.max_items_slider.setValue(30)
        self.max_items_slider.setFixedWidth(150)
        self.max_items_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.max_items_slider.setTickInterval(1)
        self.max_items_slider.valueChanged.connect(self.update_max_items_label)
        self.max_items_label = QLabel(f"Set Bag Max items: {self.max_items_slider.value():}")
        self.max_items_label.setStyleSheet("font-weight: bold; font-size: 16px; font-family: Consolas;")

        # Botão único de Get Coords
        self.get_coords_button = QPushButton("Get Coords")
        self.get_coords_button.setStyleSheet(self.button_style)
        self.get_coords_button.setFixedSize(90, 24)

        # INITIAL SLOT
        self.initial_slot_label = QLabel("Initial Slot:")
        self.initial_slot_label.setStyleSheet("font-weight: bold; font-size: 16px; font-family: Consolas;")
        self.initial_slot_input = QLineEdit("0,0")
        self.initial_slot_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.initial_slot_input.setFixedSize(90, 24)
        self.initial_slot_input.setStyleSheet("font-size: 18px; font-family: Consolas")

        # npc coords
        self.npc_talk_label = QLabel("Npc Talk:")
        self.npc_talk_label.setStyleSheet("font-weight: bold; font-size: 16px; font-family: Consolas;")
        self.npc_talk_input = QLineEdit("0,0")
        self.npc_talk_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.npc_talk_input.setFixedSize(90, 24)
        self.npc_talk_input.setStyleSheet("font-size: 18px; font-family: Consolas")

        # sell item npc coords
        self.sell_item_coords_label = QLabel("Sell Item:")
        self.sell_item_coords_label.setStyleSheet("font-weight: bold; font-size: 16px; font-family: Consolas;")
        self.sell_item_coords_input = QLineEdit("0,0")
        self.sell_item_coords_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sell_item_coords_input.setFixedSize(90, 24)
        self.sell_item_coords_input.setStyleSheet("font-size: 18px; font-family: Consolas")

        # city coords
        self.city_label = QLabel("Back to City:")
        self.city_label.setStyleSheet("font-weight: bold; font-size: 16px; font-family: Consolas;")
        self.city_input = QLineEdit("0,0")
        self.city_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.city_input.setFixedSize(90, 24)
        self.city_input.setStyleSheet("font-size: 18px; font-family: Consolas")

        # surrounds coords
        self.surrounds_label = QLabel("Surrounds:")
        self.surrounds_label.setStyleSheet("font-weight: bold; font-size: 16px; font-family: Consolas;")
        self.surrounds_input = QLineEdit("0,0")
        self.surrounds_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.surrounds_input.setFixedSize(90, 24)
        self.surrounds_input.setStyleSheet("font-size: 18px; font-family: Consolas")

        # surr input coords
        self.surr_input_label = QLabel("Surr Input:")
        self.surr_input_label.setStyleSheet("font-weight: bold; font-size: 16px; font-family: Consolas;")
        self.surr_input_input = QLineEdit("0,0")
        self.surr_input_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.surr_input_input.setFixedSize(90, 24)
        self.surr_input_input.setStyleSheet("font-size: 18px; font-family: Consolas")

        # surr close coords
        self.surr_close_label = QLabel("Surr Close:")
        self.surr_close_label.setStyleSheet("font-weight: bold; font-size: 16px; font-family: Consolas;")
        self.surr_close_input = QLineEdit("0,0")
        self.surr_close_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.surr_close_input.setFixedSize(90, 24)
        self.surr_close_input.setStyleSheet("font-size: 18px; font-family: Consolas")

        # first link coords
        self.first_link_label = QLabel("First Link:")
        self.first_link_label.setStyleSheet("font-weight: bold; font-size: 16px; font-family: Consolas;")
        self.first_link_input = QLineEdit("0,0")
        self.first_link_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.first_link_input.setFixedSize(90, 24)
        self.first_link_input.setStyleSheet("font-size: 18px; font-family: Consolas")

        # sell button coords
        self.sell_button_label = QLabel("Sell Button:")
        self.sell_button_label.setStyleSheet("font-weight: bold; font-size: 16px; font-family: Consolas;")
        self.sell_button_input = QLineEdit("0,0")
        self.sell_button_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sell_button_input.setFixedSize(90, 24)
        self.sell_button_input.setStyleSheet("font-size: 18px; font-family: Consolas")

        # Save sell settings for current char
        self.save_sell_button = QPushButton("Save Settings")
        self.save_sell_button.setStyleSheet(self.button_style)
        self.save_sell_button.setMaximumWidth(100)
        self.save_sell_button.setMinimumWidth(100)
        self.save_sell_button.clicked.connect(self.save_sell_settings)

        self.l1 = QHBoxLayout()
        self.l1.addWidget(self.max_items_label)
        self.l1.addWidget(self.max_items_slider)
        self.l1.addItem(QSpacerItem(150, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.l2 = QHBoxLayout()
        self.l2.addWidget(self.npc_talk_label)
        self.l2.addWidget(self.npc_talk_input)
        self.l2.addItem(QSpacerItem(200, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.l3 = QHBoxLayout()
        self.l3.addWidget(self.sell_item_coords_label)
        self.l3.addWidget(self.sell_item_coords_input)
        self.l3.addItem(QSpacerItem(200, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.l4 = QHBoxLayout()
        self.l4.addWidget(self.initial_slot_label)
        self.l4.addWidget(self.initial_slot_input)
        self.l4.addItem(QSpacerItem(200, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.l5 = QHBoxLayout()
        self.l5.addWidget(self.city_label)
        self.l5.addWidget(self.city_input)
        self.l5.addItem(QSpacerItem(200, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.l7 = QHBoxLayout()
        self.l7.addWidget(self.surrounds_label)
        self.l7.addWidget(self.surrounds_input)
        self.l7.addItem(QSpacerItem(200, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.l8 = QHBoxLayout()
        self.l8.addWidget(self.surr_input_label)
        self.l8.addWidget(self.surr_input_input)
        self.l8.addItem(QSpacerItem(200, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.l9 = QHBoxLayout()
        self.l9.addWidget(self.surr_close_label)
        self.l9.addWidget(self.surr_close_input)
        self.l9.addItem(QSpacerItem(200, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.l10 = QHBoxLayout()
        self.l10.addWidget(self.first_link_label)
        self.l10.addWidget(self.first_link_input)
        self.l10.addItem(QSpacerItem(200, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.l11 = QHBoxLayout()
        self.l11.addWidget(self.sell_button_label)
        self.l11.addWidget(self.sell_button_input)
        self.l11.addItem(QSpacerItem(200, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Layout para o botão Get Coords
        self.coords_layout = QHBoxLayout()
        self.coords_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        self.coords_layout.addWidget(self.get_coords_button)
        self.coords_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.l6 = QHBoxLayout()
        self.l6.addItem(QSpacerItem(120, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        # self.l6.addWidget(self.save_sell_button)
        # self.l6.addItem(QSpacerItem(138, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        self.l6.addWidget(self.get_coords_button)
        self.l6.addItem(QSpacerItem(78, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.config_layout.addLayout(self.l1)
        self.config_layout.addLayout(self.l7)  # Surrounds
        self.config_layout.addLayout(self.l8)  # Surr Input
        self.config_layout.addLayout(self.l10) # First Link
        self.config_layout.addLayout(self.l9)  # Surr Close
        self.config_layout.addLayout(self.l2)  # Npc Talk
        self.config_layout.addLayout(self.l3)  # Sell Item
        self.config_layout.addLayout(self.l4)  # Initial Slot
        self.config_layout.addLayout(self.l11) # Sell Button
        self.config_layout.addLayout(self.l5)  # Back to City
        self.config_layout.addLayout(self.l6)  # Save Settings e Get Coords

        # Conectar o botão Get Coords ao método que detecta o campo focado
        self.get_coords_button.clicked.connect(self.get_coords_for_focused_input)

        # Armazenar referência do último campo focado
        self.focused_input = None

        # Conectar eventos de foco dos campos de entrada
        self.initial_slot_input.focusInEvent = lambda e: self.set_focused_input('slot')
        self.npc_talk_input.focusInEvent = lambda e: self.set_focused_input('npc_talk')
        self.sell_item_coords_input.focusInEvent = lambda e: self.set_focused_input('sell_item')
        self.city_input.focusInEvent = lambda e: self.set_focused_input('city')
        self.surrounds_input.focusInEvent = lambda e: self.set_focused_input('surrounds')
        self.surr_input_input.focusInEvent = lambda e: self.set_focused_input('surr_input')
        self.surr_close_input.focusInEvent = lambda e: self.set_focused_input('surr_close')
        self.first_link_input.focusInEvent = lambda e: self.set_focused_input('first_link')
        self.sell_button_input.focusInEvent = lambda e: self.set_focused_input('sell_button')


        self.sell_layout.addWidget(self.title_label)
        self.sell_layout.addItem(QSpacerItem(20, 50, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        self.sell_layout.addLayout(self.npc_info_layout)
        self.sell_layout.addLayout(self.return_charm_layout)
        self.sell_layout.addLayout(self.mount_layout)
        self.sell_layout.addLayout(self.config_layout)
        self.sell_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def save_sell_settings(self):
        # Salvar as configurações de venda
        if self.unlock:
            # Chama a função save_settings da instância principal de Home
            # Acessa a instância de Home através do main_window
            self.main_window.home_page.save_settings()

    def update_pid(self, pid):
        self.unlock = True
        """Atualiza o PID e o nome do personagem dinamicamente."""
        self.pid = pid
        self.pointers = Pointers(self.pid)

    def update_low_hp_label(self):
        self.low_hp_label.setText(f"Low HP: {self.low_hp_slider.value():} % ")

    def update_low_mp_label(self):
        self.low_mp_label.setText(f"Low MP: {self.low_mp_slider.value()} % ")

    def update_low_hp_battle_label(self):
        self.low_hp_battle_label.setText(f"Battle Low HP: {self.low_hp_battle_slider.value():} % ")

    def update_low_mp_battle_label(self):
        self.low_mp_battle_label.setText(f"Battle Low MP: {self.low_mp_battle_slider.value()} % ")
        self.char_name = self.pointers.get_char_name()
        self.title_label.setText(f"Sell Settings for {self.char_name}")

    def npc_info(self):
        if self.pid == None:
            self.title_label.setText("Please select a character.")
            return

        pointer = Pointers(self.pid).get_sur_info()

        # Verifica se o retorno é um dicionário com as informações formatadas
        if isinstance(pointer, dict) and 'name' in pointer and 'coords' in pointer:
            # Atualiza os campos de texto com as informações do NPC
            self.npc_name_input.setText(pointer['name'])
            self.npc_coords_input.setText(pointer['coords'])

    def update_max_items_label(self):
        self.max_items_label.setText(f"Set Bag Max items: {self.max_items_slider.value():}")

    def get_coordinates(self, coord_type="slot"):
        """Captura a posição do mouse relativa à janela selecionada ao pressionar ESC.

        Args:
            coord_type (str): Tipo de coordenada a ser capturada ('slot' ou 'sell_item')
        """
        if not self.pid:
            print("No window have been selected.")
            self.main_window.footer.setText("Select a window before capturing the coordinates.")
            QApplication.processEvents()
            return

        # Impede execução simultânea
        if getattr(self, "_spot_farm_active", False):
            print("The coordinate capture is already underway.")
            self.main_window.footer.setText("The coordinate capture is already underway.")
            QApplication.processEvents()
            return

        # Define os atributos de controle com base no tipo de coordenada
        active_attr = f"_get_{coord_type}_coords_active"
        cancelled_attr = f"_get_{coord_type}_coords_cancelled"

        # Define o campo de entrada com base no tipo de coordenada
        if coord_type == "slot":
            input_field = self.initial_slot_input
        elif coord_type == "npc_talk":
            input_field = self.npc_talk_input
        elif coord_type == "city":
            input_field = self.city_input
        elif coord_type == "surrounds":
            input_field = self.surrounds_input
        elif coord_type == "surr_input":
            input_field = self.surr_input_input
        elif coord_type == "surr_close":
            input_field = self.surr_close_input
        elif coord_type == "first_link":
            input_field = self.first_link_input
        elif coord_type == "sell_button":
            input_field = self.sell_button_input
        else:  # sell_item
            input_field = self.sell_item_coords_input

        # Ativa o flag de captura
        setattr(self, active_attr, True)
        setattr(self, cancelled_attr, False)

        try:
            # Obtém o identificador da janela (HWND) pelo PID
            hwnd = None

            def enum_callback(handle, _):
                _, process_pid = win32process.GetWindowThreadProcessId(handle)
                if process_pid == self.pid and win32gui.IsWindowVisible(handle):
                    nonlocal hwnd
                    hwnd = handle

            win32gui.EnumWindows(enum_callback, None)

            if not hwnd:
                print("The selected window could not be found.")
                self.main_window.footer.setText("The selected window could not be found.")
                QApplication.processEvents()
                setattr(self, active_attr, False)
                return

            print(f"Janela selecionada (HWND): {hwnd}")

            # Obtém as coordenadas do cliente da janela
            client_pos = win32gui.ClientToScreen(hwnd, (0, 0))
            client_x, client_y = client_pos

            def on_press(key):
                try:
                    if getattr(self, cancelled_attr):
                        print("Coordinate capture has been canceled.")
                        return False

                    if key == keyboard.Key.esc:
                        pt = POINT()
                        windll.user32.GetCursorPos(ctypes.byref(pt))
                        mouse_x, mouse_y = pt.x, pt.y

                        # Calcula a posição relativa
                        relative_x = mouse_x - client_x
                        relative_y = mouse_y - client_y

                        # Validação dos valores capturados
                        if isinstance(relative_x, int) and isinstance(relative_y, int):
                            # Atualiza o campo de entrada
                            input_field.setText(f"{relative_x},{relative_y}")
                            print(f"Coordenadas relativas capturadas: {relative_x},{relative_y}")
                        else:
                            print("Erro: Coordenadas capturadas são inválidas.")
                            self.main_window.footer.setText("Error when capturing coordinates.")
                            return False

                        self.main_window.footer.setText("")
                        QApplication.processEvents()
                        return False  # Encerra o listener
                except Exception as e:
                    print(f"Erro no listener de teclado: {e}")
                    self.main_window.footer.setText("Error when capturing coordinates.")
                    QApplication.processEvents()
                    return False  # Garante que o listener será encerrado

            self.main_window.footer.setText(
                "Move the mouse to the desired location and press ESC to capture the coordinates."
            )
            QApplication.processEvents()

            # Criação e gerenciamento do listener de forma segura
            listener = keyboard.Listener(on_press=on_press)
            listener.start()
            listener.wait()  # Aguarda até que o listener seja encerrado

        except Exception as e:
            print(f"Erro ao capturar posição relativa: {e}")
            self.main_window.footer.setText("Error when capturing coordinates.")
            QApplication.processEvents()

        finally:
            setattr(self, active_attr, False)
            print("Captura de coordenadas finalizada.")

    def cancel_get_coordinates(self, coord_type="slot"):
        """Cancela a captura de coordenadas.

        Args:
            coord_type (str): Tipo de coordenada a ser cancelada ('slot' ou 'sell_item')
        """
        active_attr = f"_get_{coord_type}_coords_active"
        cancelled_attr = f"_get_{coord_type}_coords_cancelled"

        if getattr(self, active_attr, False):
            setattr(self, cancelled_attr, True)
            self.main_window.footer.setText("Captura de coordenadas cancelada.")
            QApplication.processEvents()
            print("Captura de coordenadas foi cancelada.")

    # Métodos de compatibilidade para manter a interface existente
    def set_focused_input(self, input_type):
        """Armazena qual campo de entrada está atualmente focado.

        Args:
            input_type (str): Tipo do campo de entrada ('slot', 'npc_talk', 'sell_item' ou 'city')
        """
        self.focused_input = input_type

    def get_coords_for_focused_input(self):
        """Captura coordenadas para o campo de entrada atualmente focado."""
        if self.focused_input:
            self.get_coordinates(self.focused_input)
        else:
            print("Nenhum campo selecionado. Clique em um campo de coordenadas primeiro.")
            self.main_window.footer.setText("Selecione um campo de coordenadas primeiro.")
            QApplication.processEvents()


class Keys(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Dicionário para armazenar os valores selecionados
        self.selected_keys = {
            "SKILL_1": "5",
            "SKILL_2": "2",
            "SKILL_3": "3",
            "SKILL_4": "1",
            "SKILL_5": "3",
            "SKILL_6": "4",
            "HEALING_SPELL": "F2",
            "CURE_SPELL": "F3",
            "SUN_NEEDLE": "F4",
            "SIN_LURE": "3",
            "SIN_AOE": "6",
            "SIN_STUN": "4",
            "NEXT_TARGET": "TAB",
            "HIDE_PLAYERS": "F12",
            "SELECT_YOURSELF": "F1",
            "INVENTORY": "I",
            "FRIENDS": "F",
            "MAP": "M",
            "FOLLOW": "P",
            "MOUNT": "SPACE",
            "SIT": "8",
            "PET_FOOD": "0",
            "BUFF_1": "9",
            "BUFF_2": "9",
            "POTION_HP": "F5",
            "POTION_MP": "F6",
            "BATTLE_POTION_HP": "F7",
            "BATTLE_POTION_MP": "F8"
        }

        self.load_keys()

        # Layout principal
        self.keys_layout = QVBoxLayout(self)

        # Título
        title = QLabel("Keys Settings for All")
        title.setStyleSheet("font-weight: bold; font-size: 22px; font-family: Consolas")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        color_info_layout = QHBoxLayout()
        color1 = QVBoxLayout()
        color2 = QVBoxLayout()

        t1 = QLabel("Used Above 45% HP target")
        t1.setStyleSheet("color: #9390DB; font-weight: bold; font-size: 14px; font-family: Consolas")
        t1b = QLabel("Ataca acima de 45% HP do target")
        t1b.setStyleSheet("color: #9390DB; font-weight: bold; font-size: 14px; font-family: Consolas")

        t2 = QLabel("Used Below 45% HP target")
        t2.setStyleSheet("color: #FF1493; font-weight: bold; font-size: 14px; font-family: Consolas")
        t2b = QLabel("Ataca abaixo de 45% HP do target")
        t2b.setStyleSheet("color: #FF1493; font-weight: bold; font-size: 14px; font-family: Consolas")

        color1.addWidget(t1)
        color1.addWidget(t1b)
        color2.addWidget(t2)
        color2.addWidget(t2b)

        color_info_layout.addLayout(color1)
        color_info_layout.addLayout(color2)

        self.keys_layout.addWidget(title)
        self.keys_layout.addItem(QSpacerItem(20, 30, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Layout para os rótulos e entradas
        self.inputs_layout = QHBoxLayout()
        self.label_column = QVBoxLayout()
        self.input_column = QVBoxLayout()
        self.label_column_2 = QVBoxLayout()
        self.input_column_2 = QVBoxLayout()

        # Dividindo as chaves nas 4 colunas
        keys_list = list(self.selected_keys.keys())
        num_keys = len(keys_list)
        keys_per_column = num_keys // 2

        # Distribuindo as chaves nas colunas sem repetição
        for i, key_name in enumerate(keys_list):
            label, input_field, label2, input_field2 = self.create_input(key_name)

            if i < keys_per_column:
                self.label_column.addWidget(label)
                self.input_column.addWidget(input_field)
            elif i < 2 * keys_per_column:
                self.label_column_2.addWidget(label2)
                self.input_column_2.addWidget(input_field2)
            # Se houver mais chaves, continue distribuindo nas colunas restantes
            elif i < 3 * keys_per_column:
                self.label_column.addWidget(label)
                self.input_column.addWidget(input_field)
            else:
                self.label_column_2.addWidget(label2)
                self.input_column_2.addWidget(input_field2)

        self.inputs_layout.addLayout(self.label_column)
        self.inputs_layout.addLayout(self.input_column)
        self.inputs_layout.addItem(QSpacerItem(80, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.inputs_layout.addLayout(self.label_column_2)
        self.inputs_layout.addLayout(self.input_column_2)
        # self.inputs_layout.addItem(QSpacerItem(20, 50, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # self.keys_layout.addItem(QSpacerItem(20, 50, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.keys_layout.addLayout(self.inputs_layout)
        self.keys_layout.addItem(QSpacerItem(20, 30, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.keys_layout.addLayout(color_info_layout)

    def create_color_label(self, text, color):
        """
        Cria um QLabel com a cor e texto especificados.
        """
        label = QLabel(text)
        label.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 16px; font-family: Consolas")
        return label

    def create_input(self, key_name):
        """
        Cria um QLabel e QLineEdit associados a uma chave.
        """
        label = QLabel(f"{key_name.capitalize().replace('_', ' ')}:")
        label.setFixedHeight(24)
        label.setStyleSheet(self.get_label_style(key_name))

        input_field = QLineEdit()
        input_field.setFixedHeight(24)
        input_field.setText(self.selected_keys[key_name])
        input_field.setMaximumWidth(70)
        input_field.textChanged.connect(lambda text, key=key_name: self.update_key_value(key, text))

        label2 = QLabel(f"{key_name.capitalize().replace('_', ' ')}:")
        label2.setFixedHeight(24)
        label2.setStyleSheet(self.get_label_style(key_name))

        input_field2 = QLineEdit()
        input_field2.setFixedHeight(24)
        input_field2.setText(self.selected_keys[key_name])
        input_field2.setMaximumWidth(70)
        input_field2.textChanged.connect(lambda text, key=key_name: self.update_key_value(key, text))

        return label, input_field, label2, input_field2

    def get_label_style(self, key_name):
        """
        Retorna o estilo apropriado para o QLabel baseado no nome da chave.
        """
        if key_name.startswith("SKILL_") and key_name in ["SKILL_1", "SKILL_2", "SKILL_3"]:
            return "color: #9390DB; font-weight: bold; font-size: 18px; font-family: Consolas"
        elif key_name.startswith("SKILL_") and key_name in ["SKILL_4", "SKILL_5", "SKILL_6"]:
            return "color: #FF1493; font-weight: bold; font-size: 18px; font-family: Consolas"
        elif key_name in ["HEALING_SPELL", "CURE_SPELL", "SUN_NEEDLE"]:
            return "color: #00FA9A; font-weight: bold; font-size: 18px; font-family: Consolas"
        elif key_name in ["SIN_LURE", "SIN_AOE", "SIN_STUN"]:
            return "color: #FF4500; font-weight: bold; font-size: 18px; font-family: Consolas"
        else:
            return "font-weight: bold; font-size: 18px; font-family: Consolas"

    def update_key_value(self, key, value):
        """
        Atualiza o valor da chave no dicionário quando o campo de texto é alterado.
        """
        self.selected_keys[key] = value
        self.save_keys()

    def save_keys(self):
        os.makedirs("characters", exist_ok=True)
        with open("characters/keys.json", "w") as json_file:
            json.dump(self.selected_keys, json_file, indent=4)

    def load_keys(self):
        os.makedirs("characters", exist_ok=True)
        if not os.path.exists("characters/keys.json"):
            self.save_keys()  # Cria o arquivo se ele não existir
        else:
            with open("characters/keys.json", "r") as json_file:
                self.selected_keys = json.load(json_file)


class BC(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.home = Home(main_window)
        self.char_name = "Home"
        self.pid = None
        self.pointers = None

        self.radio_style = """
                            QRadioButton {
                                font-family: Consolas;
                                font-size: 16px;
                                spacing: 2px;
                            }

                            QRadioButton::indicator {
                                width: 24px;
                                height: 24px;
                            }

                            QRadioButton::indicator:checked {
                                image: url(Images/misc/check-on.svg)
                            }

                            QRadioButton::indicator:unchecked {
                                image: url(Images/misc/check-off.svg);
                            }
                        """

        # Main layout
        main_layout = QVBoxLayout(self)

        self.bc_title = QLabel(f"Bewitcher Cave - Settings for {self.char_name}")
        self.bc_title.setStyleSheet("color: #cda672; font-weight: bold; font-size: 20px; font-family: Consolas")
        self.bc_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.tabs = QTabWidget()
        self.tab_1 = QWidget()
        self.tab_2 = QWidget()
        self.tab_3 = QWidget()

        # Layout da aba 1
        self.tab_1_layout = QVBoxLayout()

        # ------------------------ TEAM ------------------------
        self.team_label = QLabel("Team Mode")
        self.team_label.setStyleSheet("color: #cda672; font-weight: bold; font-size: 16px; font-family: Consolas")
        self.team_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.member_layout = QHBoxLayout()
        self.member_name_label = QLabel("Member Name")
        self.member_name_label.setStyleSheet("font-size: 16px; font-family: Consolas")
        self.member_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.member_name_input = QLineEdit()
        self.member_name_input.setText("Unknown")
        self.member_name_input.setStyleSheet("font-size: 16px; font-family: Consolas")
        self.member_name_input.setMinimumWidth(150)
        self.member_name_input.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.member_farmer = QCheckBox("Farm")
        self.member_farmer.setStyleSheet(self.home.checkbox_style)
        self.member_farmer.setChecked(True)

        self.member_reseter = QCheckBox("Reset")
        self.member_reseter.setStyleSheet(self.home.checkbox_style)

        # Conectar ambos os checkboxes
        self.member_farmer.toggled.connect(lambda checked: self.member_reseter.setChecked(False) if checked else None)
        self.member_reseter.toggled.connect(lambda checked: self.member_farmer.setChecked(False) if checked else None)
        self.member_reseter.toggled.connect(lambda: self.update_reseter())

        # self.member_layout.addWidget(self.member_name_label)
        # self.member_layout.addWidget(self.member_name_input)
        self.member_layout.addWidget(self.member_farmer)
        self.member_layout.addWidget(self.member_reseter)

        self.team_layout = QHBoxLayout()
        # self.team_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.team_layout.addLayout(self.member_layout)
        self.team_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.team_container = QWidget()
        self.team_container.setObjectName("teamContainer")
        self.team_container.setStyleSheet("""
            #teamContainer {
                border: 2px solid #444;
                border-radius: 8px;
                padding: 2px;
            }
        """)
        team_container_layout = QVBoxLayout(self.team_container)
        team_container_layout.addWidget(self.team_label)
        team_container_layout.addLayout(self.team_layout)

        # ------------------------ GENERAL ------------------------
        self.general_label = QLabel("General")
        self.general_label.setStyleSheet("color: #cda672; font-weight: bold; font-size: 16px; font-family: Consolas")
        self.general_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Linha 1: Return to Stone
        self.return_layout = QHBoxLayout()
        # self.return_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.return_label = QLabel("Return Every")
        self.return_label.setStyleSheet("font-size: 16px; font-family: Consolas")
        self.return_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.return_input = QLineEdit()
        self.return_input.setText("3")
        self.return_input.setFixedWidth(50)
        self.return_input.setFixedHeight(20)
        self.return_input.setStyleSheet("font-size: 16px; font-family: Consolas")
        self.return_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.runs_label = QLabel("Runs")
        self.runs_label.setStyleSheet("font-size: 16px; font-family: Consolas")
        self.runs_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.return_layout.addWidget(self.return_label)
        self.return_layout.addWidget(self.return_input)
        self.return_layout.addWidget(self.runs_label)
        self.return_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Buy return charm
        self.buy_return_layout = QHBoxLayout()
        # self.buy_return_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.buy_return_checkbox = QCheckBox("Buy Stone City Return Charm")
        self.buy_return_checkbox.setStyleSheet(self.home.checkbox_style)
        self.buy_return_layout.addWidget(self.buy_return_checkbox)
        self.buy_return_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Use Guild Teleport
        self.guild_teleport_layout = QHBoxLayout()
        # self.guild_teleport_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.guild_teleport_checkbox = QCheckBox("Use Guild Teleport (Primary if Enabled)")
        self.guild_teleport_checkbox.setStyleSheet(self.home.checkbox_style)
        self.guild_teleport_layout.addWidget(self.guild_teleport_checkbox)
        self.guild_teleport_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.general_container = QWidget()
        self.general_container.setObjectName("generalContainer")
        self.general_container.setStyleSheet("""
            #generalContainer {
                border: 2px solid #444;
                border-radius: 8px;
                padding: 2px;
            }
        """)
        general_container_layout = QVBoxLayout(self.general_container)
        general_container_layout.addWidget(self.general_label)
        general_container_layout.addLayout(self.return_layout)
        general_container_layout.addLayout(self.buy_return_layout)
        general_container_layout.addLayout(self.guild_teleport_layout)

         # ------------------------ Route ------------------------
        self.route_label = QLabel("Route")
        self.route_label.setStyleSheet("color: #cda672; font-weight: bold; font-size: 16px; font-family: Consolas")
        self.route_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.route_layout = QVBoxLayout()
        self.standart_route = QRadioButton("Standart Route (Straight to Boss)")
        self.standart_route.setStyleSheet(self.radio_style)
        self.standart_route.setChecked(True)

        self.safe_route = QRadioButton("Safe Route (Kill Gun Witches + Cure)")
        self.safe_route.setStyleSheet(self.radio_style)
        # se for a rota segura, desmarcar a rota padrão
        self.safe_route.toggled.connect(lambda: self.standart_route.setChecked(False))

        self.treasure_box = QCheckBox("Pick up Treasure Box")
        self.treasure_box.setStyleSheet(self.home.checkbox_style)

        self.manual_pick = QCheckBox("Auto Pick (Manual)")
        self.manual_pick.setStyleSheet(self.home.checkbox_style)

        self.route_layout.addWidget(self.route_label)
        self.route_layout.addWidget(self.standart_route)
        self.route_layout.addWidget(self.safe_route)
        self.route_layout.addWidget(self.treasure_box)
        self.route_layout.addWidget(self.manual_pick)

        self.route_container = QWidget()
        self.route_container.setObjectName("routeContainer")
        self.route_container.setStyleSheet("""
            #routeContainer {
                border: 2px solid #444;
                border-radius: 8px;
                padding: 2px;
            }
        """)
        route_container_layout = QVBoxLayout(self.route_container)
        route_container_layout.addLayout(self.route_layout)

        # ------------------------ Misc ------------------------
        self.misc_layout = QVBoxLayout()

        self.misc_label = QLabel("Scripts")
        self.misc_label.setStyleSheet("color: #cda672; font-weight: bold; font-size: 16px; font-family: Consolas")
        self.misc_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.aoe_layout = QHBoxLayout()
        self.use_aoe = QCheckBox("Use AOE until Mana is")
        self.use_aoe.setStyleSheet(self.home.checkbox_style)
        self.use_aoe_slider = QSlider(Qt.Orientation.Horizontal)
        self.use_aoe_slider.setRange(10, 100)
        self.use_aoe_slider.setValue(30)
        self.use_aoe_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.use_aoe_slider.setTickInterval(10)
        self.use_aoe_label = QLabel(f"{self.use_aoe_slider.value():} %")
        self.use_aoe_label.setStyleSheet("font-weight: bold; font-size: 16px; font-family: Consolas")
        self.use_aoe_slider.valueChanged.connect(self.update_use_aoe_label)
        self.aoe_layout.addWidget(self.use_aoe)
        self.aoe_layout.addWidget(self.use_aoe_slider)
        self.aoe_layout.addWidget(self.use_aoe_label)

        # Stamina combo
        self.stam_combo_layout = QHBoxLayout()
        self.stam_combo_checkbox = QCheckBox("Shovel Combo")
        self.stam_combo_checkbox.setStyleSheet(self.home.checkbox_style)
        self.stam_combo_slider = QSlider(Qt.Orientation.Horizontal)
        self.stam_combo_slider.setRange(1, 5)
        self.stam_combo_slider.setValue(3)
        self.stam_combo_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.stam_combo_slider.setTickInterval(1)
        self.stam_combo_label = QLabel(f"{self.stam_combo_slider.value():}")
        self.stam_combo_label.setStyleSheet("font-weight: bold; font-size: 16px; font-family: Consolas")
        self.stam_combo_slider.valueChanged.connect(self.update_stam_combo_label)
        self.stam_combo_layout.addWidget(self.stam_combo_checkbox)
        self.stam_combo_layout.addWidget(self.stam_combo_slider)
        self.stam_combo_layout.addWidget(self.stam_combo_label)

        # layout escolha de classe, stamina ou mana
        self.class_layout = QHBoxLayout()
        self.stam = QRadioButton("Stamina")
        self.stam.toggled.connect(lambda: self.toggle_mp_stam_bar())
        self.stam.toggled.connect(lambda: self.man.setChecked(False))
        self.stam.toggled.connect(lambda: self.fair.setChecked(False))
        self.stam.setStyleSheet(self.radio_style)

        self.man = QRadioButton("Mana")
        self.man.setStyleSheet(self.radio_style)
        self.man.toggled.connect(lambda: self.toggle_mp_stam_bar())
        self.man.toggled.connect(lambda: self.stam.setChecked(False))
        self.man.toggled.connect(lambda: self.fair.setChecked(False))

        self.fair = QRadioButton("Fairy")
        self.fair.setStyleSheet(self.radio_style)
        self.fair.toggled.connect(lambda: self.toggle_mp_stam_bar())
        self.fair.toggled.connect(lambda: self.stam.setChecked(False))
        self.fair.toggled.connect(lambda: self.man.setChecked(False))

        self.class_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.class_layout.addWidget(self.stam)
        self.class_layout.addWidget(self.man)
        self.class_layout.addWidget(self.fair)
        self.class_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.misc_layout.addWidget(self.misc_label)
        self.misc_layout.addLayout(self.class_layout)
        self.misc_layout.addLayout(self.aoe_layout)
        self.misc_layout.addLayout(self.stam_combo_layout)

        self.misc_container = QWidget()
        self.misc_container.setObjectName("miscContainer")
        self.misc_container.setStyleSheet("""
                    #miscContainer {
                        border: 2px solid #444;
                        border-radius: 8px;
                        padding: 2px;
                    }
                """)

        misc_container_layout = QVBoxLayout(self.misc_container)
        misc_container_layout.addLayout(self.misc_layout)

        # ------------------------ Finalizando aba ------------------------
        self.tab_1_layout.addWidget(self.team_container)
        self.tab_1_layout.addWidget(self.general_container)
        self.tab_1_layout.addWidget(self.route_container)
        self.tab_1_layout.addWidget(self.misc_container)
        # self.tab_1_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.tab_2_layout = QVBoxLayout()

        # ------------------------ SKILLS ------------------------
        self.skills_label = QLabel("Attack Skills")
        self.skills_label.setStyleSheet("color: #cda672; font-weight: bold; font-size: 16px; font-family: Consolas")
        self.skills_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.line_1_layout = QHBoxLayout()
        self.skill_1_label = QLabel("Attack 1  ")
        self.skill_1_label.setStyleSheet("font-size: 16px; font-family: Consolas")
        self.skill_1_input = QLineEdit()
        self.skill_1_input.setText("null")
        self.skill_1_input.setFixedWidth(50)
        self.skill_1_input.setFixedHeight(20)
        self.skill_1_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.skill_1_input.setStyleSheet("font-size: 16px; font-family: Consolas")

        self.stam_skill_combo_label = QLabel("Shovel Combo")
        self.stam_skill_combo_label.setStyleSheet("font-size: 16px; font-family: Consolas")
        self.stam_skill_combo_input = QLineEdit()
        self.stam_skill_combo_input.setText("null")
        self.stam_skill_combo_input.setFixedWidth(50)
        self.stam_skill_combo_input.setFixedHeight(20)
        self.stam_skill_combo_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stam_skill_combo_input.setStyleSheet("font-size: 16px; font-family: Consolas")

        self.line_1_layout.addWidget(self.skill_1_label)
        self.line_1_layout.addWidget(self.skill_1_input)
        self.line_1_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.line_1_layout.addWidget(self.stam_skill_combo_label)
        self.line_1_layout.addWidget(self.stam_skill_combo_input)
        self.line_1_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.line_2_layout = QHBoxLayout()
        self.skill_2_label = QLabel("Attack 2  ")
        self.skill_2_label.setStyleSheet("font-size: 16px; font-family: Consolas")
        self.skill_2_input = QLineEdit()
        self.skill_2_input.setText("null")
        self.skill_2_input.setFixedWidth(50)
        self.skill_2_input.setFixedHeight(20)
        self.skill_2_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.skill_2_input.setStyleSheet("font-size: 16px; font-family: Consolas")

        #self.cure_spell_label = QLabel("Cure Spell   ")
        #self.cure_spell_label.setStyleSheet("font-size: 16px; font-family: Consolas")
        #self.cure_spell_input = QLineEdit()
        #self.cure_spell_input.setFixedWidth(50)
        #self.cure_spell_input.setFixedHeight(20)
        #self.cure_spell_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #self.cure_spell_input.setStyleSheet("font-size: 16px; font-family: Consolas")

        self.line_2_layout.addWidget(self.skill_2_label)
        self.line_2_layout.addWidget(self.skill_2_input)
        self.line_2_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        #self.line_2_layout.addWidget(self.cure_spell_label)
        #self.line_2_layout.addWidget(self.cure_spell_input)
        #self.line_2_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))


        self.line_3_layout = QHBoxLayout()
        self.skill_3_label = QLabel("Attack 3  ")
        self.skill_3_label.setStyleSheet("font-size: 16px; font-family: Consolas")
        self.skill_3_input = QLineEdit()
        self.skill_3_input.setText("null")
        self.skill_3_input.setFixedWidth(50)
        self.skill_3_input.setFixedHeight(20)
        self.skill_3_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.skill_3_input.setStyleSheet("font-size: 16px; font-family: Consolas")

        self.skill_5_label = QLabel("Break Soul  ")
        self.skill_5_label.setStyleSheet("font-size: 16px; font-family: Consolas")
        self.skill_5_input = QLineEdit()
        self.skill_5_input.setText("null")
        self.skill_5_input.setFixedWidth(50)
        self.skill_5_input.setFixedHeight(20)
        self.skill_5_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.skill_5_input.setStyleSheet("font-size: 16px; font-family: Consolas")

        self.line_3_layout.addWidget(self.skill_3_label)
        self.line_3_layout.addWidget(self.skill_3_input)
        self.line_3_layout.addItem(QSpacerItem(90, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.line_3_layout.addWidget(self.skill_5_label)
        self.line_3_layout.addWidget(self.skill_5_input)
        self.line_3_layout.addItem(QSpacerItem(90, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.line_4_layout = QHBoxLayout()
        self.skill_4_label = QLabel("Mana Aoe    ")
        self.skill_4_label.setStyleSheet("font-size: 16px; font-family: Consolas")
        self.skill_4_input = QLineEdit()
        self.skill_4_input.setText("null")
        self.skill_4_input.setFixedWidth(50)
        self.skill_4_input.setFixedHeight(20)
        self.skill_4_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.skill_4_input.setStyleSheet("font-size: 16px; font-family: Consolas")

        self.line_2_layout.addWidget(self.skill_4_label)
        self.line_2_layout.addWidget(self.skill_4_input)
        self.line_2_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.line_5_layout = QHBoxLayout()
        self.skill_delay_slider = QSlider(Qt.Orientation.Horizontal)
        self.skill_delay_slider.setRange(2, 50)  # Representa 1.0 a 5.0 com passo de 0.1
        self.skill_delay_slider.setValue(10)  # 1.0 segundos
        self.skill_delay_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.skill_delay_slider.setTickInterval(10)  # Uma marca a cada 1.0 segundo (10 passos de 0.1)

        self.skill_delay_label = QLabel(f"Attacks Delay {self.skill_delay_slider.value() / 10:.1f}s")
        self.skill_delay_label.setStyleSheet("font-weight: bold; font-size: 16px; font-family: Consolas")

        self.skill_delay_slider.valueChanged.connect(self.update_skill_delay_label)

        self.line_5_layout.addWidget(self.skill_delay_label)
        self.line_5_layout.addWidget(self.skill_delay_slider)
        self.line_5_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.skills_container = QWidget()
        self.skills_container.setObjectName("skillsContainer")
        self.skills_container.setStyleSheet("""
                    #skillsContainer {
                        border: 2px solid #444;
                        border-radius: 8px;
                        padding: 2px;
                    }
                """)

        skills_container_layout = QVBoxLayout(self.skills_container)
        skills_container_layout.addWidget(self.skills_label)
        skills_container_layout.addLayout(self.line_1_layout)
        skills_container_layout.addLayout(self.line_2_layout)
        skills_container_layout.addLayout(self.line_3_layout)
        skills_container_layout.addLayout(self.line_4_layout)
        skills_container_layout.addLayout(self.line_5_layout)


        # ------------------------ GENERAL ------------------------
        self.gen_label = QLabel("General")
        self.gen_label.setStyleSheet("color: #cda672; font-weight: bold; font-size: 16px; font-family: Consolas")
        self.gen_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.gen_line_1_layout = QHBoxLayout()
        self.mount_label = QLabel("Mount       ")
        self.mount_label.setStyleSheet("font-size: 16px; font-family: Consolas")
        self.mount_input = QLineEdit()
        self.mount_input.setText("null")
        self.mount_input.setFixedWidth(50)
        self.mount_input.setFixedHeight(20)
        self.mount_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mount_input.setStyleSheet("font-size: 16px; font-family: Consolas")

        self.mount_speed_label = QLabel("Mount Speed ")
        self.mount_speed_label.setStyleSheet("font-size: 16px; font-family: Consolas")
        self.mount_speed_input = QLineEdit()
        self.mount_speed_input.setText("null")
        self.mount_speed_input.setFixedWidth(50)
        self.mount_speed_input.setFixedHeight(20)
        self.mount_speed_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mount_speed_input.setStyleSheet("font-size: 16px; font-family: Consolas")

        self.gen_line_1_layout.addWidget(self.mount_label)
        self.gen_line_1_layout.addWidget(self.mount_input)
        self.gen_line_1_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.gen_line_1_layout.addWidget(self.mount_speed_label)
        self.gen_line_1_layout.addWidget(self.mount_speed_input)
        self.gen_line_1_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.gen_line_2_layout = QHBoxLayout()
        self.return_stone_label = QLabel("Return Stone")
        self.return_stone_label.setStyleSheet("font-size: 16px; font-family: Consolas")
        self.return_stone_input = QLineEdit()
        self.return_stone_input.setText("null")
        self.return_stone_input.setFixedWidth(50)
        self.return_stone_input.setFixedHeight(20)
        self.return_stone_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.return_stone_input.setStyleSheet("font-size: 16px; font-family: Consolas")

        self.return_guild_label = QLabel("Return Guild")
        self.return_guild_label.setStyleSheet("font-size: 16px; font-family: Consolas")
        self.return_guild_input = QLineEdit()
        self.return_guild_input.setText("null")
        self.return_guild_input.setFixedWidth(50)
        self.return_guild_input.setFixedHeight(20)
        self.return_guild_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.return_guild_input.setStyleSheet("font-size: 16px; font-family: Consolas")

        self.gen_line_2_layout.addWidget(self.return_stone_label)
        self.gen_line_2_layout.addWidget(self.return_stone_input)
        self.gen_line_2_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.gen_line_2_layout.addWidget(self.return_guild_label)
        self.gen_line_2_layout.addWidget(self.return_guild_input)
        self.gen_line_2_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.gen_line_3_layout = QHBoxLayout()
        self.pet_fo_label = QLabel("Pet Food    ")
        self.pet_fo_label.setStyleSheet("font-size: 16px; font-family: Consolas")
        self.pet_fo_input = QLineEdit()
        self.pet_fo_input.setText("null")
        self.pet_fo_input.setFixedWidth(50)
        self.pet_fo_input.setFixedHeight(20)
        self.pet_fo_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pet_fo_input.setStyleSheet("font-size: 16px; font-family: Consolas")

        self.gen_line_3_layout.addWidget(self.pet_fo_label)
        self.gen_line_3_layout.addWidget(self.pet_fo_input)
        self.gen_line_3_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.gen_container = QWidget()
        self.gen_container.setObjectName("genContainer")
        self.gen_container.setStyleSheet("""
                    #genContainer {
                        border: 2px solid #444;
                        border-radius: 8px;
                        padding: 2px;
                    }
                """)

        gen_container_layout = QVBoxLayout(self.gen_container)
        gen_container_layout.addWidget(self.gen_label)
        gen_container_layout.addLayout(self.gen_line_1_layout)
        gen_container_layout.addLayout(self.gen_line_2_layout)
        gen_container_layout.addLayout(self.gen_line_3_layout)

        # ------------------------ POTIONS ------------------------
        self.potions_label = QLabel("Recover Skills")
        self.potions_label.setStyleSheet("color: #cda672; font-weight: bold; font-size: 16px; font-family: Consolas")
        self.potions_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.pot_line_1_layout = QHBoxLayout()
        self.pot_hp_label = QLabel("Potion HP    ")
        self.pot_hp_label.setStyleSheet("font-size: 16px; font-family: Consolas")
        self.pot_hp_input = QLineEdit()
        self.pot_hp_input.setText("null")
        self.pot_hp_input.setFixedWidth(50)
        self.pot_hp_input.setFixedHeight(20)
        self.pot_hp_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pot_hp_input.setStyleSheet("font-size: 16px; font-family: Consolas")

        self.pot_mp_label = QLabel("Potion MP ")
        self.pot_mp_label.setStyleSheet("font-size: 16px; font-family: Consolas")
        self.pot_mp_input = QLineEdit()
        self.pot_mp_input.setText("null")
        self.pot_mp_input.setFixedWidth(50)
        self.pot_mp_input.setFixedHeight(20)
        self.pot_mp_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pot_mp_input.setStyleSheet("font-size: 16px; font-family: Consolas")

        self.pot_line_1_layout.addWidget(self.pot_hp_label)
        self.pot_line_1_layout.addWidget(self.pot_hp_input)
        self.pot_line_1_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.pot_line_1_layout.addWidget(self.pot_mp_label)
        self.pot_line_1_layout.addWidget(self.pot_mp_input)
        self.pot_line_1_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.pot_line_2_layout = QHBoxLayout()
        self.pot_hp_battle_label = QLabel("Battle HP    ")
        self.pot_hp_battle_label.setStyleSheet("font-size: 16px; font-family: Consolas")
        self.pot_hp_battle_input = QLineEdit()
        self.pot_hp_battle_input.setText("null")
        self.pot_hp_battle_input.setFixedWidth(50)
        self.pot_hp_battle_input.setFixedHeight(20)
        self.pot_hp_battle_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pot_hp_battle_input.setStyleSheet("font-size: 16px; font-family: Consolas")

        self.pot_mp_battle_label = QLabel("Battle MP ")
        self.pot_mp_battle_label.setStyleSheet("font-size: 16px; font-family: Consolas")
        self.pot_mp_battle_input = QLineEdit()
        self.pot_mp_battle_input.setText("null")
        self.pot_mp_battle_input.setFixedWidth(50)
        self.pot_mp_battle_input.setFixedHeight(20)
        self.pot_mp_battle_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pot_mp_battle_input.setStyleSheet("font-size: 16px; font-family: Consolas")

        self.pot_line_2_layout.addWidget(self.pot_hp_battle_label)
        self.pot_line_2_layout.addWidget(self.pot_hp_battle_input)
        self.pot_line_2_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.pot_line_2_layout.addWidget(self.pot_mp_battle_label)
        self.pot_line_2_layout.addWidget(self.pot_mp_battle_input)
        self.pot_line_2_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.pot_line_3_layout = QHBoxLayout()
        self.pot_sit_label = QLabel("Sit          ")
        self.pot_sit_label.setStyleSheet("font-size: 16px; font-family: Consolas")
        self.pot_sit_input = QLineEdit()
        self.pot_sit_input.setText("null")
        self.pot_sit_input.setFixedWidth(50)
        self.pot_sit_input.setFixedHeight(20)
        self.pot_sit_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pot_sit_input.setStyleSheet("font-size: 16px; font-family: Consolas")

        self.wizz_super_label = QLabel("Wizz Super")
        self.wizz_super_label.setStyleSheet("font-size: 16px; font-family: Consolas")
        self.wizz_super_input = QLineEdit()
        self.wizz_super_input.setText("null")
        self.wizz_super_input.setFixedWidth(50)
        self.wizz_super_input.setFixedHeight(20)
        self.wizz_super_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.wizz_super_input.setStyleSheet("font-size: 16px; font-family: Consolas")

        self.pot_line_3_layout.addWidget(self.pot_sit_label)
        self.pot_line_3_layout.addWidget(self.pot_sit_input)
        self.pot_line_3_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.pot_line_3_layout.addWidget(self.wizz_super_label)
        self.pot_line_3_layout.addWidget(self.wizz_super_input)
        self.pot_line_3_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.pot_line_4_layout = QHBoxLayout()
        self.healing_label = QLabel("Healing Spell")
        self.healing_label.setStyleSheet("font-size: 16px; font-family: Consolas")
        self.healing_input = QLineEdit()
        self.healing_input.setText("null")
        self.healing_input.setFixedWidth(50)
        self.healing_input.setFixedHeight(20)
        self.healing_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.healing_input.setStyleSheet("font-size: 16px; font-family: Consolas")
        self.pot_line_4_layout.addItem(QSpacerItem(0, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.pot_line_4_layout.addWidget(self.healing_label)
        self.pot_line_4_layout.addWidget(self.healing_input)
        self.pot_line_4_layout.addItem(QSpacerItem(400, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.pot_container = QWidget()
        self.pot_container.setObjectName("potContainer")
        self.pot_container.setStyleSheet("""
                            #potContainer {
                                border: 2px solid #444;
                                border-radius: 8px;
                                padding: 2px;
                            }
                        """)

        pot_container_layout = QVBoxLayout(self.pot_container)
        pot_container_layout.addWidget(self.potions_label)
        pot_container_layout.addLayout(self.pot_line_1_layout)
        pot_container_layout.addLayout(self.pot_line_2_layout)
        pot_container_layout.addLayout(self.pot_line_3_layout)
        pot_container_layout.addLayout(self.pot_line_4_layout)

        # ------------------------ Finalizando aba 2------------------------
        self.tab_2_layout.addWidget(self.skills_container)
        self.tab_2_layout.addWidget(self.gen_container)
        self.tab_2_layout.addWidget(self.pot_container)

        self.tab_3_layout = QVBoxLayout()
        # ------------------------ Low hp, mp, battle hp, battle mp ------------------------
        self.stats_label = QLabel("Char Status")
        self.stats_label.setStyleSheet("color: #cda672; font-weight: bold; font-size: 16px; font-family: Consolas")
        self.stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Barra de progresso para o HP
        self.bc_hp_bar = QProgressBar(self)
        self.bc_hp_bar.setMinimum(0)
        self.bc_hp_bar.setMaximum(100)
        self.bc_hp_bar.setValue(0)

        self.bc_hp_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #363636;  /* Borda da barra */
                border-radius: 2px;         /* Bordas arredondadas */
                background: #1C1C1C;       /* Cor de fundo */
                font: bold 12px 'Consolas';   /* Fonte da barra */
                text-align: center;        /* Centraliza o texto */
                min-height: 15px;          /* Altura mínima da barra */
                max-height: 15px;
                max-width: 300px;
                min-width: 300px;
                
            }

            QProgressBar::chunk {
                background-color: #DC143C; /* Cor da parte preenchida */
                border-radius: 2px;        /* Bordas arredondadas na parte preenchida */
            }
        """)

        # Barra de progresso para o MP
        self.bc_mp_bar = QProgressBar(self)
        self.bc_mp_bar.setMinimum(0)
        self.bc_mp_bar.setMaximum(100)
        self.bc_mp_bar.setValue(0)

        self.bc_mp_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #363636;  /* Borda da barra */
                border-radius: 2px;         /* Bordas arredondadas */
                background: #1C1C1C;       /* Cor de fundo */
                font: bold 12px 'Consolas';   /* Fonte da barra */
                text-align: center;        /* Centraliza o texto */
                min-height: 15px;          /* Altura mínima da barra */
                max-height: 15px;
                max-width: 300px;
                min-width: 300px;
                
            }

            QProgressBar::chunk {
                background-color: #00a8f3; /* Cor da parte preenchida */
                border-radius: 2px;        /* Bordas arredondadas na parte preenchida */
            }
        """)

        self.hp_bar_layout = QHBoxLayout()
        self.hp_bar_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.hp_bar_layout.addWidget(self.bc_hp_bar)
        self.hp_bar_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.mp_bar_layout = QHBoxLayout()
        self.mp_bar_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.mp_bar_layout.addWidget(self.bc_mp_bar)
        self.mp_bar_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Timer para atualização periódica
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.bc_update_hp_bar)
        self.timer.timeout.connect(self.bc_update_mp_bar)
        self.timer.start(100)

        # Slider for LOW_HP
        self.stats_line_1_layout = QHBoxLayout()
        self.bc_low_hp_slider = QSlider(Qt.Orientation.Horizontal)
        self.bc_low_hp_slider.setRange(10, 100)
        self.bc_low_hp_slider.setValue(95)
        self.bc_low_hp_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.bc_low_hp_slider.setTickInterval(10)
        self.bc_low_hp_slider.valueChanged.connect(self.bc_update_low_hp_label)

        # Label for LOW_HP
        self.bc_low_hp_label = QLabel(f"HP: {self.bc_low_hp_slider.value():} % ")
        self.bc_low_hp_label.setStyleSheet("font-size: 16px; font-family: Consolas")
        self.bc_low_hp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stats_line_1_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.stats_line_1_layout.addWidget(self.bc_low_hp_label)
        self.stats_line_1_layout.addWidget(self.bc_low_hp_slider)
        self.stats_line_1_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Slider for LOW_MP
        self.stats_line_2_layout = QHBoxLayout()
        self.bc_low_mp_slider = QSlider(Qt.Orientation.Horizontal)
        self.bc_low_mp_slider.setRange(10, 100)  # 0 to 100
        self.bc_low_mp_slider.setValue(95)
        self.bc_low_mp_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.bc_low_mp_slider.setTickInterval(10)
        self.bc_low_mp_slider.valueChanged.connect(self.bc_update_low_mp_label)

        # Label for LOW_MP
        self.bc_low_mp_label = QLabel(f"MP: {self.bc_low_mp_slider.value()} % ")
        self.bc_low_mp_label.setStyleSheet("font-size: 16px; font-family: Consolas")
        self.bc_low_mp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stats_line_2_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.stats_line_2_layout.addWidget(self.bc_low_mp_label)
        self.stats_line_2_layout.addWidget(self.bc_low_mp_slider)
        self.stats_line_2_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Slider for LOW_HP_BATTLE
        self.stats_line_3_layout = QHBoxLayout()
        self.bc_low_hp_battle_slider = QSlider(Qt.Orientation.Horizontal)
        self.bc_low_hp_battle_slider.setFixedWidth(120)
        self.bc_low_hp_battle_slider.setRange(10, 99)
        self.bc_low_hp_battle_slider.setValue(30)
        self.bc_low_hp_battle_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.bc_low_hp_battle_slider.setTickInterval(10)
        self.bc_low_hp_battle_slider.valueChanged.connect(self.bc_update_low_hp_battle_label)

        # Label for LOW_HP_BATTLE
        self.bc_low_hp_battle_label = QLabel(f"Battle HP: {self.bc_low_hp_battle_slider.value():} % ")
        self.bc_low_hp_battle_label.setStyleSheet("font-size: 16px; font-family: Consolas")
        self.bc_low_hp_battle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stats_line_3_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.stats_line_3_layout.addWidget(self.bc_low_hp_battle_label)
        self.stats_line_3_layout.addWidget(self.bc_low_hp_battle_slider)
        self.stats_line_3_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Slider for LOW_MP_BATTLE
        self.stats_line_4_layout = QHBoxLayout()
        self.bc_low_mp_battle_slider = QSlider(Qt.Orientation.Horizontal)
        self.bc_low_mp_battle_slider.setFixedWidth(120)
        self.bc_low_mp_battle_slider.setRange(10, 99)  # 0 to 100
        self.bc_low_mp_battle_slider.setValue(30)
        self.bc_low_mp_battle_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.bc_low_mp_battle_slider.setTickInterval(10)
        self.bc_low_mp_battle_slider.valueChanged.connect(self.bc_update_low_mp_battle_label)

        # Label for LOW_MP_BATTLE
        self.bc_low_mp_battle_label = QLabel(f"Battle MP: {self.bc_low_mp_battle_slider.value()} % ")
        self.bc_low_mp_battle_label.setStyleSheet("font-size: 16px; font-family: Consolas")
        self.bc_low_mp_battle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stats_line_4_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.stats_line_4_layout.addWidget(self.bc_low_mp_battle_label)
        self.stats_line_4_layout.addWidget(self.bc_low_mp_battle_slider)
        self.stats_line_4_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.stats_container = QWidget()
        self.stats_container.setObjectName("statsContainer")
        self.stats_container.setStyleSheet("""
                                    #statsContainer {
                                        border: 2px solid #444;
                                        border-radius: 8px;
                                        padding: 2px;
                                    }
                                """)


        stats_container_layout = QVBoxLayout(self.stats_container)
        stats_container_layout.addWidget(self.stats_label)
        stats_container_layout.addLayout(self.hp_bar_layout)
        stats_container_layout.addLayout(self.mp_bar_layout)
        stats_container_layout.addLayout(self.stats_line_1_layout)
        stats_container_layout.addLayout(self.stats_line_2_layout)
        stats_container_layout.addLayout(self.stats_line_3_layout)
        stats_container_layout.addLayout(self.stats_line_4_layout)

        # ------------------------ BC STATUS ------------------------

        self.tab_3_layout.addWidget(self.stats_container)
        self.tab_3_layout.addItem(QSpacerItem(20, 200, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.tab_1.setLayout(self.tab_1_layout)
        self.tab_2.setLayout(self.tab_2_layout)
        self.tab_3.setLayout(self.tab_3_layout)

        self.tabs.addTab(self.tab_1, "Settings")
        self.tabs.addTab(self.tab_2, "Shortcuts")
        self.tabs.addTab(self.tab_3, "Stats")

        main_layout.addWidget(self.bc_title)
        main_layout.addWidget(self.tabs)

    def update_reseter(self):
        if self.member_reseter.isChecked():
            self.general_container.setDisabled(True)
            self.route_container.setDisabled(True)
            self.misc_container.setDisabled(True)
        else:
            self.general_container.setEnabled(True)
            self.route_container.setEnabled(True)
            self.misc_container.setEnabled(True)

    def update_use_aoe_label(self):
        self.use_aoe_label.setText(f"{self.use_aoe_slider.value():} %")
        self.use_aoe_label.setStyleSheet("font-weight: bold; font-size: 16px; font-family: Consolas")

    def update_stam_combo_label(self):
        self.stam_combo_label.setText(f"{self.stam_combo_slider.value():}")
        self.stam_combo_label.setStyleSheet("font-weight: bold; font-size: 16px; font-family: Consolas")

    def update_skill_delay_label(self, value):
        # Converte o valor inteiro para float dividindo por 10
        delay = value / 10.0
        self.skill_delay_label.setText(f"Attacks Delay {delay:.1f}s")

    def update_pid(self, pid):
        self.unlock = True
        """Atualiza o PID e o nome do personagem dinamicamente."""
        self.pid = pid
        self.pointers = Pointers(self.pid)

        self.char_name = self.pointers.get_char_name()
        self.bc_title.setText(f"Bewitcher Cave - Settings for {self.char_name}")

    def bc_update_low_hp_label(self):
        self.bc_low_hp_label.setText(f"HP: {self.bc_low_hp_slider.value():} % ")

    def bc_update_low_mp_label(self):
        self.bc_low_mp_label.setText(f"MP: {self.bc_low_mp_slider.value()} % ")

    def bc_update_low_hp_battle_label(self):
        self.bc_low_hp_battle_label.setText(f"Battle HP: {self.bc_low_hp_battle_slider.value():} % ")

    def bc_update_low_mp_battle_label(self):
        self.bc_low_mp_battle_label.setText(f"Battle MP: {self.bc_low_mp_battle_slider.value()} % ")

    # Método para atualizar a barra de HP
    def bc_update_hp_bar(self):
        if self.pid is not None:
            percentage = self.bc_hp_bar_percentage()
            self.bc_hp_bar.setValue(int(percentage))
            self.bc_hp_bar.setFormat(f"{percentage:.2f}% HP")

        else:
            self.bc_hp_bar.setValue(0)
            self.bc_hp_bar.setFormat("0% HP")

    # Método para atualizar a barra de MP
    def bc_update_mp_bar(self):
        if self.pid is not None:
            percentage = self.bc_mp_bar_percentage()
            self.bc_mp_bar.setValue(int(percentage))
            self.bc_mp_bar.setFormat(f"{percentage:.2f}% MP")

        else:
            self.bc_mp_bar.setValue(0)
            self.bc_mp_bar.setFormat("0% MP")

    def bc_hp_bar_percentage(self):
        try:
            max_hp = self.pointers.get_max_hp()
            current_hp = self.pointers.get_hp()

            # Verifica se max_hp é válido para evitar divisão por zero
            if max_hp <= 0:
                return 0

            percentage = (current_hp / max_hp) * 100
            rounded_percentage = round(percentage, 2)

            # Garante que o percentual esteja no intervalo esperado
            if rounded_percentage < 0 or rounded_percentage > 100:
                return 0

            return rounded_percentage
        except Exception as e:
            # Log do erro (se necessário)
            # print(f"Erro ao calcular HP: {e}")
            return 0

    def bc_mp_bar_percentage(self):
        try:

            mp = self.pointers.get_mana()
            max_mp = self.pointers.get_max_mana()

            # Verifica se max_hp é válido para evitar divisão por zero
            if max_mp <= 0:
                return 0

            percentage = (mp / max_mp) * 100
            rounded_percentage = round(percentage, 2)

            # Garante que o percentual esteja no intervalo esperado
            if rounded_percentage < 0 or rounded_percentage > 100:
                return 0

            return rounded_percentage
        except Exception as e:
            # Log do erro (se necessário)
            # print(f"Erro ao calcular MP: {e}")
            return 0


    def toggle_mp_stam_bar(self):
        if self.stam.isChecked():
            self.bc_mp_bar.hide()
            self.bc_low_mp_label.hide()
            self.bc_low_mp_slider.hide()
            self.bc_low_mp_battle_label.hide()
            self.bc_low_mp_battle_slider.hide()
            self.use_aoe.setChecked(False)
            self.use_aoe.setDisabled(True)
            self.use_aoe_slider.setDisabled(True)
            self.use_aoe_label.setDisabled(True)
        else:
            self.bc_mp_bar.show()
            self.bc_low_mp_label.show()
            self.bc_low_mp_slider.show()
            self.bc_low_mp_battle_label.show()
            self.bc_low_mp_battle_slider.show()
            self.use_aoe.setEnabled(True)
            self.use_aoe_slider.setEnabled(True)
            self.use_aoe_label.setEnabled(True)

        if self.man.isChecked() or self.fair.isChecked():
            if self.fair.isChecked():
                self.use_aoe.setChecked(False)
                self.use_aoe.setDisabled(True)
            self.stam_combo_checkbox.setChecked(False)
            self.stam_combo_checkbox.setDisabled(True)
            self.stam_combo_label.setDisabled(True)
            self.stam_combo_slider.setDisabled(True)
        else:
            self.stam_combo_checkbox.setEnabled(True)
            self.stam_combo_label.setEnabled(True)
            self.stam_combo_slider.setEnabled(True)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    with open(resource_path('style.qss'), 'r') as file:
        app.setStyleSheet(file.read())
    app.setStyle('Fusion')
    bot = Main()
    bot.show()
    sys.exit(app.exec())
