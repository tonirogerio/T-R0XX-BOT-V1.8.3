import ctypes
from ctypes.wintypes import HWND, UINT, WPARAM, LPARAM

# Constantes das mensagens
WM_SETCURSOR = 0x0020
WM_MOUSEMOVE = 0x0200
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202
WM_RBUTTONDOWN = 0x0204
WM_RBUTTONUP = 0x0205

HTCLIENT = 1  # Hit-test no cliente da janela
MK_LBUTTON = 0x0001  # Botão esquerdo pressionado
MK_RBUTTON = 0x0002  # Botão direito pressionado

# Carregando a biblioteca user32.dll
user32 = ctypes.windll.user32

# Função para criar o LPARAM com as coordenadas
def make_lparam(x: int, y: int) -> LPARAM:
    return LPARAM(y << 16 | x & 0xFFFF)

# Funções para cliques de mouse usando PostMessage
def left(hwnd: int, x: int, y: int):
    """Simula um clique com o botão esquerdo do mouse usando PostMessage."""
    # Sequência exata observada no Spy++:
    # 1. WM_MOUSEMOVE com fwKeys:0000
    user32.PostMessageW(HWND(hwnd), WM_MOUSEMOVE, WPARAM(0), make_lparam(x, y))
    # 2. WM_LBUTTONDOWN com fwKeys:MK_LBUTTON
    user32.PostMessageW(HWND(hwnd), WM_LBUTTONDOWN, WPARAM(MK_LBUTTON), make_lparam(x, y))
    # 3. WM_LBUTTONUP com fwKeys:0000
    user32.PostMessageW(HWND(hwnd), WM_LBUTTONUP, WPARAM(0), make_lparam(x, y))

def right(hwnd: int, x: int, y: int):
    """Simula um clique com o botão direito do mouse usando PostMessage."""
    # Sequência similar para botão direito
    user32.PostMessageW(HWND(hwnd), WM_MOUSEMOVE, WPARAM(0), make_lparam(x, y))
    user32.PostMessageW(HWND(hwnd), WM_RBUTTONDOWN, WPARAM(MK_RBUTTON), make_lparam(x, y))
    user32.PostMessageW(HWND(hwnd), WM_RBUTTONUP, WPARAM(0), make_lparam(x, y))


def kright(hwnd: int, x: int, y: int):
    """Simula um clique com o botão direito do mouse."""
    user32.SendMessageW(HWND(hwnd), WM_SETCURSOR, WPARAM(hwnd), LPARAM(HTCLIENT | (WM_MOUSEMOVE << 16)))
    user32.SendMessageW(HWND(hwnd), WM_MOUSEMOVE, WPARAM(0), make_lparam(x, y))
    user32.SendMessageW(HWND(hwnd), WM_RBUTTONDOWN, WPARAM(MK_RBUTTON), make_lparam(x, y))
    user32.SendMessageW(HWND(hwnd), WM_RBUTTONUP, WPARAM(0), make_lparam(x, y))

def kleft(hwnd: int, x: int, y: int):
    """Simula um clique com o botão esquerdo do mouse."""
    user32.SendMessageW(HWND(hwnd), WM_SETCURSOR, WPARAM(hwnd), LPARAM(HTCLIENT | (WM_MOUSEMOVE << 16)))
    user32.SendMessageW(HWND(hwnd), WM_MOUSEMOVE, WPARAM(0), make_lparam(x, y))
    user32.SendMessageW(HWND(hwnd), WM_LBUTTONDOWN, WPARAM(MK_LBUTTON), make_lparam(x, y))
    user32.SendMessageW(HWND(hwnd), WM_LBUTTONUP, WPARAM(0), make_lparam(x, y))

# função para cliques duplos
def double_left(hwnd: int, x: int, y: int):
    """Simula um clique duplo com o botão esquerdo do mouse usando PostMessage."""
    # Sequência exata observada no Spy++:
    # 1. WM_MOUSEMOVE com fwKeys:0000
    user32.PostMessageW(HWND(hwnd), WM_MOUSEMOVE, WPARAM(0), make_lparam(x, y))
    # 2. WM_LBUTTONDOWN com fwKeys:MK_LBUTTON
    user32.PostMessageW(HWND(hwnd), WM_LBUTTONDOWN, WPARAM(MK_LBUTTON), make_lparam(x, y))
    # 3. WM_LBUTTONUP com fwKeys:0000
    user32.PostMessageW(HWND(hwnd), WM_LBUTTONUP, WPARAM(0), make_lparam(x, y))
    # 4. WM_MOUSEMOVE com fwKeys:0000
    user32.PostMessageW(HWND(hwnd), WM_MOUSEMOVE, WPARAM(0), make_lparam(x, y))
    # 5. WM_LBUTTONDOWN com fwKeys:MK_LBUTTON
    user32.PostMessageW(HWND(hwnd), WM_LBUTTONDOWN, WPARAM(MK_LBUTTON), make_lparam(x, y))
    # 6. WM_LBUTTONUP com fwKeys:0000
    user32.PostMessageW(HWND(hwnd), WM_LBUTTONUP, WPARAM(0), make_lparam(x, y))

def double_right(hwnd: int, x: int, y: int):
    """Simula um clique duplo com o botão direito do mouse usando PostMessage."""
    # Sequência similar para botão direito
    user32.PostMessageW(HWND(hwnd), WM_MOUSEMOVE, WPARAM(0), make_lparam(x, y)) # 1.
    user32.PostMessageW(HWND(hwnd), WM_RBUTTONDOWN, WPARAM(MK_RBUTTON), make_lparam(x, y)) # 2.
    user32.PostMessageW(HWND(hwnd), WM_RBUTTONUP, WPARAM(0), make_lparam(x, y)) # 3.
    user32.PostMessageW(HWND(hwnd), WM_MOUSEMOVE, WPARAM(0), make_lparam(x, y)) # 4.
    user32.PostMessageW(HWND(hwnd), WM_RBUTTONDOWN, WPARAM(MK_RBUTTON), make_lparam(x, y)) # 5.
    user32.PostMessageW(HWND(hwnd), WM_RBUTTONUP, WPARAM(0), make_lparam(x, y)) # 6.

def multiple_left_clicks(hwnd: int, x: int, y: int, count: int = 1):
    """
    Simula múltiplos cliques consecutivos, replicando exatamente o padrão do Spy++.

    Args:
        hwnd (int): Handle da janela alvo
        x (int): Coordenada X do clique
        y (int): Coordenada Y do clique
        count (int): Número de cliques a executar
    """
    for i in range(count):
        # Cada clique é precedido por WM_MOUSEMOVE
        user32.PostMessageW(HWND(hwnd), WM_MOUSEMOVE, WPARAM(0), make_lparam(x, y))
        user32.PostMessageW(HWND(hwnd), WM_LBUTTONDOWN, WPARAM(MK_LBUTTON), make_lparam(x, y))
        user32.PostMessageW(HWND(hwnd), WM_LBUTTONUP, WPARAM(0), make_lparam(x, y))

# Função para mover o mouse fisicamente (mantida do código original)
def move(hwnd: int, x: int, y: int):
    """
    Move fisicamente o cursor do mouse para uma posição específica dentro da janela alvo.

    Args:
        hwnd (int): Handle da janela onde o movimento será calculado.
        x (int): Coordenada X relativa à janela.
        y (int): Coordenada Y relativa à janela.
    """
    # Obter a posição absoluta da janela na tela
    rect = ctypes.wintypes.RECT()
    user32.GetWindowRect(HWND(hwnd), ctypes.byref(rect))
    window_x, window_y = rect.left, rect.top

    # Converter coordenadas relativas à janela em coordenadas absolutas
    absolute_x = window_x + x
    absolute_y = window_y + y

    # Mover o cursor fisicamente para as coordenadas absolutas
    user32.SetCursorPos(absolute_x, absolute_y)

# Função adicional - apenas mover cursor sem clique (usando PostMessage)
def move_cursor_message(hwnd: int, x: int, y: int):
    """Move o cursor virtualmente enviando apenas WM_MOUSEMOVE via PostMessage."""
    user32.PostMessageW(HWND(hwnd), WM_MOUSEMOVE, WPARAM(0), make_lparam(x, y))

"""
Exemplo de uso:

import mouse

# Handle da janela (substitua pelo handle correto)
hwnd = 0x002900AE  # Exemplo do log do Spy++
xPos, yPos = 996, 128

# Clique único
mouse.left(hwnd, xPos, yPos)

# Múltiplos cliques (como mostrado no Spy++)
mouse.multiple_left_clicks(hwnd, xPos, yPos, 3)

# Apenas mover cursor (PostMessage)
mouse.move_cursor_message(hwnd, xPos, yPos)

# Mover cursor fisicamente
mouse.move(hwnd, xPos, yPos)
"""