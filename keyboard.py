import ctypes
from ctypes.wintypes import HWND, WPARAM, LPARAM
import win32api
import win32con

# Constantes de mensagens para eventos de teclado
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101

# Mapeamento de teclas para Virtual-Key Codes (VK) - CORRIGIDO
VK_CODES = {
    **{str(i): 0x30 + i for i in range(10)},  # Teclas numéricas 0-9
    **{chr(i): i for i in range(0x41, 0x5A + 1)},  # Letras A-Z
    # CORREÇÃO: Mapeamento correto das teclas F1-F12
    "F1": 0x70,   # VK_F1
    "F2": 0x71,   # VK_F2
    "F3": 0x72,   # VK_F3
    "F4": 0x73,   # VK_F4
    "F5": 0x74,   # VK_F5
    "F6": 0x75,   # VK_F6
    "F7": 0x76,   # VK_F7
    "F8": 0x77,   # VK_F8
    "F9": 0x78,   # VK_F9
    "F10": 0x79,  # VK_F10
    "F11": 0x7A,  # VK_F11
    "F12": 0x7B,  # VK_F12
    "ALT": 0x12,
    "SHIFT": 0x10,
    "CTRL": 0x11,
    "ENTER": 0x0D,
    "BACKSPACE": 0x08,
    "SPACE": 0x20,
    "TAB": 0x09,
    "ESC": 0x1B,
    "EMPTY": None,  # Tecla vazia que não envia nada
    "NULL": None,   # Alternativa
    "": None
}

# Carregar a biblioteca user32.dll
user32 = ctypes.windll.user32

def send(hwnd: int, command: str):
    """Envia uma tecla (press + release) para a janela especificada"""
    vk_code = VK_CODES.get(command.upper())
    if vk_code is None and command.upper() not in VK_CODES:
        raise ValueError(f"Tecla '{command}' não é suportada ou inválida.")
    
    # Se for uma tecla "vazia" (EMPTY/NULL), não faz nada
    if vk_code is None:
        return
    
    # Envia as mensagens WM_KEYDOWN e WM_KEYUP
    user32.SendMessageW(HWND(hwnd), WM_KEYDOWN, WPARAM(vk_code), LPARAM(0))
    user32.SendMessageW(HWND(hwnd), WM_KEYUP, WPARAM(vk_code), LPARAM(0))

def press(hwnd: int, command: str):
    """Pressiona uma tecla (apenas WM_KEYDOWN)"""
    vk_code = VK_CODES.get(command.upper())
    if vk_code is None and command.upper() not in VK_CODES:
        raise ValueError(f"Tecla '{command}' não é suportada ou inválida.")
    
    # Se for uma tecla "vazia" (EMPTY/NULL), não faz nada
    if vk_code is None:
        return
    
    # Envia a mensagem WM_KEYDOWN
    user32.SendMessageW(HWND(hwnd), WM_KEYDOWN, WPARAM(vk_code), LPARAM(0))

def release(hwnd: int, command: str):
    """Libera uma tecla (apenas WM_KEYUP)"""
    vk_code = VK_CODES.get(command.upper())
    if vk_code is None and command.upper() not in VK_CODES:
        raise ValueError(f"Tecla '{command}' não é suportada ou inválida.")
    
    # Se for uma tecla "vazia" (EMPTY/NULL), não faz nada
    if vk_code is None:
        return
    
    # Envia a mensagem WM_KEYUP
    user32.SendMessageW(HWND(hwnd), WM_KEYUP, WPARAM(vk_code), LPARAM(0))

def write(hwnd: int, text: str):
    """Escreve um texto caractere por caractere"""
    for char in text:
        win32api.SendMessage(hwnd, win32con.WM_CHAR, ord(char), 0)