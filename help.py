import json
import os
import sys

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QScrollArea, QFrame, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Help(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_language = 'pt'  # Começa em português
        self.help_data = self.load_help_data()
        self.init_ui()


    def load_help_data(self):
        try:
            help = resource_path('help.json')
            with open(help, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            print(f"Erro ao carregar help.json: {e}")
            return {}

    def init_ui(self):
        # Layout principal
        main_layout = QVBoxLayout(self)

        # Botão de alternar idioma
        language_layout = QHBoxLayout()
        self.language_button = QPushButton('English' if self.current_language == 'pt' else 'Português')
        self.language_button.setStyleSheet("""
            QPushButton {
                min-width: 100px;
                max-width: 100px;
                max-height: 30px;
                border: 2px solid #696969;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #415fa1;
                border-color: #696969;
            }
            QPushButton:pressed {
                background-color: #F4A460;
                border-color: #696969;
                color: #d4d4d4;
            }
        """)
        self.language_button.clicked.connect(self.toggle_language)
        language_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        language_layout.addWidget(self.language_button)
        language_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        main_layout.addLayout(language_layout)

        # Área de conteúdo com scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #4a6fa5;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)

        # Widget de conteúdo
        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

        self.update_content()

    def create_section(self, title, topics):
        section = QFrame()
        section.setStyleSheet("""
            QFrame {
                background-color: #585858;
                border-radius: 10px;
                margin: 5px;
                padding: 10px;
            }
        """)
        layout = QVBoxLayout(section)

        # Título da seção
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 18px;
                font-weight: bold;
                padding: 5px;
            }
        """)
        layout.addWidget(title_label)

        # Tópicos
        for topic in topics:
            topic_frame = QFrame()
            topic_frame.setStyleSheet("""
                QFrame {
                    background-color: #000000;
                    border-radius: 5px;
                    margin: 2px;
                    padding: 5px;
                }
            """)
            topic_layout = QVBoxLayout(topic_frame)

            # Título do tópico
            topic_title = QLabel(topic['title'])
            topic_title.setStyleSheet("""
                QLabel {
                    color: #ffffff;
                    font-size: 16px;
                    font-weight: bold;
                }
            """)
            topic_layout.addWidget(topic_title)

            # Conteúdo do tópico
            topic_content = QLabel(topic['content'])
            topic_content.setWordWrap(True)
            topic_content.setStyleSheet("""
                QLabel {
                    color: #d4d4d4;
                    font-size: 14px;
                    padding: 5px;
                }
            """)
            topic_layout.addWidget(topic_content)

            layout.addWidget(topic_frame)

        return section

    def update_content(self):
        # Limpa o layout atual
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Obtém os dados do idioma atual
        language_data = self.help_data.get(self.current_language, {})

        # Adiciona cada seção
        for section_key, section_data in language_data.items():
            section = self.create_section(
                section_data['title'],
                section_data['topics']
            )
            self.content_layout.addWidget(section)

        self.content_layout.addStretch()

    def toggle_language(self):
        self.current_language = 'en' if self.current_language == 'pt' else 'pt'
        self.language_button.setText('Português' if self.current_language == 'en' else 'English')
        self.update_content()