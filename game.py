import json
import math
import os
import time
import multiprocessing
from typing import Callable
import cv2
import numpy as np
import win32con
import win32gui
import win32ui
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QMessageBox

from keyboard import send, press, release, write
from mouse import *
from pointers import Pointers

altar = [
    {"xY": [400, 65]},
    {"xY": [373, 81]},
    {"xY": [354, 111]},
    {"xY": [336, 138]},
    {"xY": [323, 171]},
    {"xY": [285, 169]},
    {"xY": [252, 159]},
    {"xY": [226, 165]},
    {"xY": [195, 164]},
    {"xY": [148, 164]},  # casinha dos aborigne
    {"xY": [120, 145]},  # as vezes trava 118, 136
    {"xY": [108, 99]},
    {"xY": [80, 57]},  # casinha poison rattan
    {"xY": [102, 28]},
    {"xY": [127, -6]},
    {"xY": [147, -54]},  # anterior  brejo
    {"xY": [174, -98]},  # depois do brejo 174, -93
    {"xY": [223, -98]},  # 214, -98 onde trava nos skull
    {"xY": [232, -65]},
    {"xY": [250, -47]},
    {"xY": [276, -72]},
    {"xY": [307, -79]},
    {"xY": [338, -44]},
    {"xY": [354, -1]},
    {"xY": [330, 35]},
    {"xY": [295, 49]},  # entrada do altar
    {"xY": [258, 49]},
    {"xY": [259, 79]},
    {"xY": [222, 80]},
    {"xY": [190, 80]},
    {"xY": [189, 44]},  # escada 1
    # {"xY": [199,45]}, # meio da escada
    {"xY": [204, 45]},
    {"xY": [201, 22]},
    {"xY": [210, 22]},
    {"xY": [244, 22]},
    {"xY": [242, 45]},
    {"xY": [225, 45]},
    {"xY": [219, 45]}
]

gun_withc = [
    {"xY": [185, -406], "via": [915, 116]},
    {"xY": [165, -406], "via": [910, 116]},
    {"xY": [125, -406], "via": [905, 116]},
    {"xY": [105, -406], "via": [900, 116]}
]

blaze = [
    {"xY": [185, -406], "via": [915, 116]},
    {"xY": [165, -406], "via": [910, 116]},
    {"xY": [125, -406], "via": [905, 116]},
    {"xY": [105, -406], "via": [900, 116]},
    {"xY": [80, -406], "via": [895, 116]},
]

blaze_2 = [
    {"xY": [80, -406], "via": [895, 116]},
]

cords_team = {
    "yourself": [0, 0],
    "member_1": [0, 0],
    "member_2": [0, 0],
    "member_3": [0, 0],
    "member_4": [0, 0],
}

cords_move = {
    "stop": [0, 0],
    "right": [0, 0],
    "left": [0, 0],
    "up": [0, 0],
    "down": [0, 0],
    "minimize": [0, 0],
    "mouse_reset": [0, 0],
}

cords_game = {
    "deleter_ok": [0, 0],
    "jackstraw_ok": [0, 0],
    "revive_ok": [0, 0],
    "loot": [0, 0],
    "pickup": [0, 0],
    "reset_view": [0, 0],
    "world_map": [0, 0]
}

cords_bc = {
    "surrounds": [0, 0],
    "surr_input": [0, 0],
    "first_link": [0, 0],
    "rich_man": [0, 0],
    "rich_sell": [0, 0],
    "initial_slot": [0, 0],
    "ok_confirm": [0, 0],
    "sell_button": [0, 0],
    "purchase": [0, 0],
    "buy_charm": [0, 0],
    "buy_item": [0, 0],
    "fairy_teleport": [0, 0],
    "din_woods": [0, 0],
    "block_list": [0, 0],
    "team_name": [0, 0],
    "team_up": [0, 0],
    "photo": [0, 0],
    "leave_team": [0, 0],
    "team_info": [0, 0],
    "team_join": [0, 0],
    "skull": [0, 0],
    "skull_enter": [0, 0],
    "altar_npc": [0, 0],
    "altar_enter": [0, 0],
    "npc_leave": [0, 0],
    "exit": [0, 0],
    "treasure_box": [0, 0],
    "pick_up": [0, 0],
    "center_screen": [0, 0]

}


def set_coords_by_resolution(resolution):
    """Configura as coordenadas globais com base na resolução."""
    global cords_team, cords_move, cords_game

    if resolution == "800*600":
        cords_move.update({
            "stop": [695, 115],
            "right": [696, 115],
            "left": [694, 115],
            "up": [695, 114],
            "down": [695, 116],
            "minimize": [771, 127],
            "mouse_reset": [679, 180],
        })

        cords_team.update({
            "yourself": [45, 45],
            "member_1": [30, 210],
            "member_2": [30, 285],
            "member_3": [30, 365],
            "member_4": [30, 445],
        })

        cords_game.update({
            "deleter_ok": [327, 249],
            "jackstraw_ok": [325, 251],
            "revive_ok": [404, 384],
            "loot": [400, 300],
            "pickup": [450, 476],
            "reset_view": [643, 58],
            "world_map": [542, 23]
        })

    elif resolution == "1024*768":
        cords_move.update({
            "stop": [919, 115],
            "right": [920, 115],
            "left": [918, 115],
            "up": [919, 114],
            "down": [919, 116],
            "minimize": [995, 126],
            "mouse_reset": [900, 182],
        })

        cords_team.update({
            "yourself": [45, 45],
            "member_1": [30, 210],
            "member_2": [30, 285],
            "member_3": [30, 365],
            "member_4": [30, 445],
        })

        cords_game.update({
            "deleter_ok": [439, 335],
            "jackstraw_ok": [439, 336],
            "revive_ok": [515, 469],
            "loot": [505, 390],
            "pickup": [447, 479],
            "reset_view": [866, 58],
            "world_map": [654, 105]
        })

        cords_bc.update({
            "surrounds": [975, 58],
            "surr_input": [590, 540],
            "first_link": [299, 261],
            "rich_man": [345, 258],  # 240, 327
            "rich_sell": [271, 429],
            "initial_slot": [450, 327],
            "ok_confirm": [439, 333],
            "sell_button": [478, 713],
            "purchase": [282, 395],
            "buy_charm": [194, 327],
            "buy_item": [182, 712],
            "fairy_teleport": [466, 361],
            "din_woods": [299, 590],
            "block_list": [705, 192],
            "team_name": [571, 253],
            "team_up": [603, 323],
            "photo": [46, 49],
            "leave_team": [88, 98],
            "team_info": [15, 494],
            "team_join": [437, 335],
            "skull": [470, 405],
            "skull_enter": [258, 364],
            "altar_npc": [370, 380],  # 380, 320
            "altar_enter": [308, 336],
            "npc_leave": [513, 302],
            "exit": [301, 364],
            "treasure_box": [520, 269],
            "pick_up": [450, 478],
            "center_screen": [510, 370]
        })

    elif resolution == "1280*720":
        cords_move.update({
            "stop": [1175, 115],
            "right": [1176, 115],
            "left": [1174, 115],
            "up": [1175, 114],
            "down": [1175, 116],
            "minimize": [1253, 128],
            "mouse_reset": [1158, 182],
        })

        cords_team.update({
            "yourself": [45, 45],
            "member_1": [30, 210],
            "member_2": [30, 285],
            "member_3": [30, 365],
            "member_4": [30, 445],
        })

        cords_game.update({
            "deleter_ok": [567, 311],
            "jackstraw_ok": [567, 311],
            "revive_ok": [643, 445],
            "loot": [631, 363],
            "pickup": [447, 479],
            "reset_view": [1123, 59],
            "world_map": [786, 83]

        })

    elif resolution == "1280*800":
        cords_move.update({
            "stop": [1175, 115],
            "right": [1176, 115],
            "left": [1174, 115],
            "up": [1175, 114],
            "down": [1175, 116],
            "minimize": [1253, 128],
            "mouse_reset": [1158, 182],
        })

        cords_team.update({
            "yourself": [45, 45],
            "member_1": [30, 210],
            "member_2": [30, 285],
            "member_3": [30, 365],
            "member_4": [30, 445],
        })

        cords_game.update({
            "deleter_ok": [568, 350],
            "jackstraw_ok": [565, 351],
            "revive_ok": [643, 484],
            "loot": [640, 402],
            "pickup": [447, 479],
            "reset_view": [1124, 58],
            "world_map": [787, 120]
        })

    elif resolution == "1920*1080":
        cords_move.update({
            "stop": [1815, 115],
            "right": [1816, 115],
            "left": [1814, 115],
            "up": [1815, 114],
            "down": [1815, 116],
            "minimize": [1891, 128],
            "mouse_reset": [1798, 182],
        })

        cords_team.update({
            "yourself": [45, 45],
            "member_1": [25, 205],
            "member_2": [25, 285],
            "member_3": [25, 365],
            "member_4": [25, 445],
        })

        cords_game.update({
            "deleter_ok": [887, 480],
            "jackstraw_ok": [888, 483],
            "revive_ok": [964, 614],
            "loot": [960, 533],
            "pickup": [447, 479],
            "reset_view": [1761, 58],
            "world_map": [1106, 253]
        })

    else:
        raise ValueError(f"Resolução não suportada: {resolution}")


def start_game_process(config, stop_event):
    """Executa o loop de jogo em um subprocesso, verificando o sinal de parada."""
    set_coords_by_resolution(config.resolution)

    while not stop_event.is_set():
        try:
            if config.char_type == "BC Farm":
                if config.member_reseter == "ON":
                    reseter(config)
                else:
                    bc(config)
            else:
                bot(config)

            # Pequeno yield para não sobrecarregar CPU
            stop_event.wait(0.1)

        except Exception as e:
            print(f"Erro no subprocesso PID={config.pid}: {e}")

            # Se for erro crítico, para imediatamente
            if isinstance(e, (SystemExit, KeyboardInterrupt, MemoryError)):
                print(f"Erro crítico no PID={config.pid}: {type(e).__name__}. Encerrando processo.")
                break

            # Para outros erros, pausa antes de continuar
            print(f"Pausando processo PID={config.pid} por 500ms antes de tentar novamente...")
            if stop_event.wait(0.5):  # 500ms pause com possibilidade de interrupção
                print(f"Processo PID={config.pid} foi interrompido durante pausa.")
                break


def bc_set_info(config, name, current_runs, new_gold):

    # Opção 1: Formatação simples com separadores
    new_title = f"{name} - Runs: {current_runs} - Gold Gained: {new_gold}"

    try:
        win32gui.SetWindowText(config.hwnd, new_title)
        return True
    except Exception as e:
        print(f"Erro ao alterar título da janela: {e}")
        return False


def update_gold(start_gold, current_gold):
    """
    Calcula e formata a diferença de gold

    :param start_gold: Valor inicial em copper
    :param current_gold: Valor atual em copper
    :return: String formatada da diferença (ex: "+10g 5s 20c" ou "-5g 10s 15c")
    """
    diff = current_gold - start_gold

    if diff >= 0:
        gold = diff // 10000
        silver = (diff // 100) % 100
        copper = diff % 100
        return f"+{gold}g {silver}s {copper}c"
    else:
        diff = abs(diff)
        gold = diff // 10000
        silver = (diff // 100) % 100
        copper = diff % 100
        return f"-{gold}g {silver}s {copper}c"


def reseter(config):
    while True:
        time.sleep(1)
        bc_team(config, "join")


def bc(config):
    run = 0
    current_runs = 0
    ptr = Pointers(config.pid)
    name = ptr.get_char_name()
    start_gold = ptr.get_gold()
    print(f"{name} {current_runs} {start_gold}")

    bc_set_info(config, name, current_runs, 0)

    # testes
    # bc_hide_players(config)
    # bc_go_to_din_woods(config)
    # bc_go_to_bc(config)
    # bc_enter(config)
    # bc_go_to_altar(config)
    # bc_enter_altar(config)
    # bc_kill_blaze(config)
    # time.sleep(20)
    # bc_leave(config)
    # time.sleep(20)

    # teste do sell
    # Pointers(config.pid).write_camera(380, 0, 40)
    # bc_hide_players(config)
    # bc_sell_items(config)
    # bc_show_players(config)

    cycle = CycleManager()

    print("Starting BC bot")
    cycle.add_cycle(bc_pet_food(config), 40, "Ciclo de Pet Food")
    cycle.add_cycle(bc_delete_items(config), 30, "Deleter")

    minimap_minimize(config)
    bc_mount(config, "dismount")
    bc_teleport(config)
    bc_mount(config, "mount")
    Pointers(config.pid).write_camera(380, 0, 40)

    bc_hide_players(config)
    bc_go_to_din_woods(config)
    bc_show_players(config)
    bc_go_to_bc(config)

    while True:
        if run == int(config.return_every):
            run = 0
            bc_mount(config, "dismount")
            bc_teleport(config)

            bc_mount(config, "mount")
            Pointers(config.pid).write_camera(380, 0, 40)

            bc_hide_players(config)
            bc_sell_items(config)
            bc_show_players(config)

            bc_hide_players(config)
            bc_go_to_din_woods(config)
            bc_show_players(config)

            bc_go_to_bc(config)

        # abre friend list
        # send(config.hwnd, config.friend_list)
        # time.sleep(1)
        friend_list_confirm(config, "open")

        surrounds_confirm(config, "close")
        time.sleep(0.5)

        bc_team(config, "send")

        # fecha friend list
        send(config.hwnd, config.friend_list)
        time.sleep(0.5)
        # confere se fechou friend list
        friend_list_confirm(config, "close")

        bc_hide_players(config)
        bc_enter(config)
        bc_show_players(config)

        bc_team(config, "leave")
        bc_cure_at_start(config)

        # confere se esta usando mount
        bc_mount(config, "mount")

        bc_go_to_altar(config)
        bc_enter_altar(config)

        # ir ao gun witchers se estiver ativado
        if config.safe_route == "ON":
            bc_gun_witchers(config)
            kill_gun_witchers(config)
            bc_cure(config)
            bc_go_to_blaze_2(config)
        else:
            bc_go_to_blaze(config)

        bc_kill_blaze(config)

        if config.manual_pick == "ON":
            print("Manual Pick")
            bc_manual_auto_pick(config)

        if config.treasure_box == "ON":
            bc_treasure_box(config)

        bc_use_courage(config)
        cycle.execute_cycles()

        run += 1
        time.sleep(0.2)
        current_runs += 1

        current_gold = ptr.get_gold()
        new_gold = update_gold(start_gold, current_gold)
        bc_set_info(config, name, current_runs, new_gold)

        if run < int(config.return_every):
            bc_leave(config)


def bc_sit(config):
    if not Pointers(config.pid).is_sitting():
        send(config.hwnd, config.bc_sit), time.sleep(0.5)


def bc_pet_food(config):
    def inner():
        time.sleep(1)
        print("Using Pet Food")
        send(config.hwnd, config.bc_pet_food)
        send(config.hwnd, config.bc_pet_food), time.sleep(0.2)

    return inner


# V1.8
def bc_mount(config, action):
    if action == "mount":
        if Pointers(config.pid).mount() == 0:
            print("Mounting...")
            send(config.hwnd, config.bc_mount)
            time.sleep(5)

    if action == "dismount":
        if Pointers(config.pid).mount() != 0:
            print("Dismounting...")
            send(config.hwnd, config.bc_mount)
            time.sleep(1)


def bc_hide_players(config):
    # print("Hiding players")
    press(config.hwnd, config.hide_players)


def bc_show_players(config):
    # print("Showing players")
    release(config.hwnd, config.hide_players)


def bc_talk_npc(config, x, y, max_attempts=10):
    if max_attempts <= 0:
        return

    offsets = [
        (0, 10),  # 10 pra cima
        (10, 0),  # 10 pra direita
        (0, -10),  # 10 pra baixo
        (-10, 0),  # 10 pra esquerda
    ]

    for offset_x, offset_y in offsets:
        right(config.hwnd, x + offset_x, y + offset_y)
        time.sleep(0.2)

        # Verifica se o pointer retornou true após o clique
        if Pointers(config.pid).get_dialog():
            time.sleep(0.2)
            break

    # Se após todos os cliques ainda não conseguiu dialog, tenta novamente
    if not Pointers(config.pid).get_dialog():
        return bc_talk_npc(config, x, y, max_attempts - 1)


def bc_talk_to_rich(config, x, y):
    richman = [156, -496]

    safe_spot_back(config, richman)

    offsets = [
        (0, 10),  # 10 pra cima
        (10, 0),  # 10 pra direita
        (0, -10),  # 10 pra baixo
        (-0, 0),  # 10 pra esquerda
    ]

    for offset_x, offset_y in offsets:
        right(config.hwnd, x + offset_x, y + offset_y)
        time.sleep(0.1)

    # Se após todos os cliques ainda não conseguiu dialog, tenta novamente
    if not Pointers(config.pid).get_dialog():
        return bc_talk_to_rich(config, x, y)


def bc_talk_fay(config, x, y):
    offsets = [
        (0, 10),  # 10 pra cima
        (10, 0),  # 10 pra direita
        (0, -10),  # 10 pra baixo
        (-10, 0),  # 10 pra esquerda
    ]

    for offset_x, offset_y in offsets:
        right(config.hwnd, x + offset_x, y + offset_y)
        time.sleep(0.2)

        # Verifica se o pointer retornou true após o clique
        if Pointers(config.pid).get_dialog():
            time.sleep(1.5)
            break

    # Se após todos os cliques ainda não conseguiu dialog, tenta novamente
    if not Pointers(config.pid).get_dialog():
        return bc_talk_fay(config, x, y)


def bc_teleport(config):
    if Pointers(config.pid).is_in_battle():
        bc_kill_blaze(config)

    guild = [241, -477]
    stone = [178, -515]
    send(config.hwnd, config.teleport_guild)
    time.sleep(3)
    x = Pointers(config.pid).get_x()
    y = Pointers(config.pid).get_y()
    print(f"Current = {x},{y}")

    if x != guild[0] or y != guild[1]:
        print("Teleporting to Stone")
        send(config.hwnd, config.teleport_stone)
        time.sleep(3)

        x = Pointers(config.pid).get_x()
        y = Pointers(config.pid).get_y()
        print(f"Current = {x},{y}")

        if x != stone[0] or y != stone[1]:
            print("Teleport error, trying again")
            return bc_teleport(config)


def bc_sell_items(config):
    left(config.hwnd, cords_bc["surrounds"][0], cords_bc["surrounds"][1])
    time.sleep(1)
    left(config.hwnd, cords_bc["surr_input"][0], cords_bc["surr_input"][1])
    time.sleep(0.5)
    write(config.hwnd, "Rich")
    time.sleep(0.5)
    left(config.hwnd, cords_bc["first_link"][0], cords_bc["first_link"][1])
    time.sleep(1)
    left(config.hwnd, cords_bc["surrounds"][0], cords_bc["surrounds"][1])
    time.sleep(1)

    # confirma se fechou surrounds e inventory
    surrounds_confirm(config, "close")
    inventory_confirm(config, "close")

    wait_while_moving(config)

    x = Pointers(config.pid).get_x()
    y = Pointers(config.pid).get_y()
    time.sleep(0.5)

    if x != 153 or y != -492:
        return bc_sell_items(config)

    bc_talk_to_rich(config, cords_bc["rich_man"][0], cords_bc["rich_man"][1])
    time.sleep(0.5)
    left(config.hwnd, cords_bc["rich_sell"][0], cords_bc["rich_sell"][1])
    time.sleep(0.5)
    for _ in range(24):
        left(config.hwnd, cords_bc["initial_slot"][0], cords_bc["initial_slot"][1])
        time.sleep(0.2)
        if Pointers(config.pid).confirm_box():
            time.sleep(0.2)
            left(config.hwnd, cords_bc["ok_confirm"][0], cords_bc["ok_confirm"][1])
            time.sleep(0.2)
    left(config.hwnd, cords_bc["sell_button"][0], cords_bc["sell_button"][1])
    time.sleep(0.5)

    bag_1 = Pointers(config.pid).bag_1_quantity()
    bag_2 = Pointers(config.pid).bag_2_quantity()
    items = bag_1 + bag_2
    print(f"Unsold items = {items}")
    if items > 20:
        bc_talk_to_rich(config, cords_bc["rich_man"][0], cords_bc["rich_man"][1])
        time.sleep(0.5)
        left(config.hwnd, cords_bc["rich_sell"][0], cords_bc["rich_sell"][1])
        time.sleep(0.5)
        for _ in range(24):
            left(config.hwnd, cords_bc["initial_slot"][0], cords_bc["initial_slot"][1])
            time.sleep(0.2)
            if Pointers(config.pid).confirm_box():
                time.sleep(0.2)
                left(config.hwnd, cords_bc["ok_confirm"][0], cords_bc["ok_confirm"][1])
                time.sleep(0.2)
        left(config.hwnd, cords_bc["sell_button"][0], cords_bc["sell_button"][1])
        time.sleep(0.5)

    if config.buy_charm == "ON":
        bc_talk_to_rich(config, cords_bc["rich_man"][0], cords_bc["rich_man"][1])
        time.sleep(0.5)
        left(config.hwnd, cords_bc["purchase"][0], cords_bc["purchase"][1])
        time.sleep(0.5)
        left(config.hwnd, cords_bc["buy_charm"][0], cords_bc["buy_charm"][1])
        time.sleep(0.5)
        left(config.hwnd, cords_bc["buy_item"][0], cords_bc["buy_item"][1])
        time.sleep(0.5)


def bc_go_to_din_woods(config):
    left(config.hwnd, cords_bc["surrounds"][0], cords_bc["surrounds"][1])
    time.sleep(1)
    left(config.hwnd, cords_bc["surr_input"][0], cords_bc["surr_input"][1])
    time.sleep(0.5)
    write(config.hwnd, "rans")
    left(config.hwnd, cords_bc["first_link"][0], cords_bc["first_link"][1])
    time.sleep(1)
    left(config.hwnd, cords_bc["surrounds"][0], cords_bc["surrounds"][1])
    time.sleep(0.5)

    # confirma se fechou surrounds
    surrounds_confirm(config, "close")

    wait_while_moving(config)

    # verifica se chegou na fada teleporte
    x = Pointers(config.pid).get_x()
    y = Pointers(config.pid).get_y()
    time.sleep(0.5)

    if x != 178 or y != -517:
        return bc_go_to_din_woods(config)

    # talk with fairy teleport
    bc_talk_fay(config, cords_bc["fairy_teleport"][0], cords_bc["fairy_teleport"][1])
    time.sleep(0.2)
    left(config.hwnd, cords_bc["din_woods"][0], cords_bc["din_woods"][1])
    time.sleep(1.5)

    woods = [1372, -417]
    location = Pointers(config.pid).get_location()
    location_2 = Pointers(config.pid).get_location_2()

    inX = Pointers(config.pid).get_x()
    inY = Pointers(config.pid).get_y()
    time.sleep(0.1)

    # verifica via location e X Y
    if location == "Ghost Din Woods" or location_2 == "Ghost Din Woods" or inX == woods[0] or inY == woods[1]:
        print("Teleported to Ghost Din Woods")
        time.sleep(0.2)
    else:
        if location == "Offline Account" or location_2 == "Offline Account" and inX == woods[0] or inY == woods[1]:
            print("Ghost Din Woods location pointer error, but x y is ok")
            time.sleep(0.2)
        else:
            print(f"Teleport fairy error, trying again {location} {location_2} {inX},{inY}")
            return bc_go_to_din_woods(config)


def bc_go_to_bc(config):
    left(config.hwnd, cords_bc["surrounds"][0], cords_bc["surrounds"][1])
    time.sleep(1)
    left(config.hwnd, cords_bc["surr_input"][0], cords_bc["surr_input"][1])
    time.sleep(0.5)
    write(config.hwnd, "ku")
    time.sleep(0.5)
    left(config.hwnd, cords_bc["first_link"][0], cords_bc["first_link"][1])
    time.sleep(1)
    wait_while_moving(config)

    entrance = [1395, -635]

    x = Pointers(config.pid).get_x()
    y = Pointers(config.pid).get_y()

    if x != entrance[0] or y != entrance[1]:
        left(config.hwnd, cords_bc["surr_input"][0], cords_bc["surr_input"][1])
        time.sleep(0.5)

        for _ in range(10):
            send(config.hwnd, "BACKSPACE")
        time.sleep(0.5)

        write(config.hwnd, "ku")
        time.sleep(0.5)

        left(config.hwnd, cords_bc["first_link"][0], cords_bc["first_link"][1])
        time.sleep(0.5)

        wait_while_moving(config)

        while x != entrance[0] or y != entrance[1]:
            left(config.hwnd, cords_bc["first_link"][0], cords_bc["first_link"][1])
            time.sleep(0.5)
            wait_while_moving(config)
            x = Pointers(config.pid).get_x()
            y = Pointers(config.pid).get_y()

            # verifica se esta morto
            if Pointers(config.pid).get_hp() == 0:
                left(config.hwnd, cords_bc["surrounds"][0], cords_bc["surrounds"][1])
                time.sleep(0.5)
                surrounds_confirm(config, "close")
                bc_dead(config)
                return bc(config)
    else:
        left(config.hwnd, cords_bc["surrounds"][0], cords_bc["surrounds"][1])
        time.sleep(0.5)

        # confirma se fechou surrounds
        surrounds_confirm(config, "close")


def bc_team(config, action, sent=0, max_attempts=5):
    if action == "send":
        left(config.hwnd, cords_bc["block_list"][0], cords_bc["block_list"][1])
        time.sleep(0.5)
        right(config.hwnd, cords_bc["team_name"][0], cords_bc["team_name"][1])
        time.sleep(0.2)
        left(config.hwnd, cords_bc["team_up"][0], cords_bc["team_up"][1])
        time.sleep(3)

        # verifica se esta em team
        if Pointers(config.pid).get_team_size() == 2:
            # print(f"Team formado após {sent + 1} tentativas")
            time.sleep(0.2)
        else:
            sent += 1
            # print(f"Tentativa {sent} falhou, tentando novamente...")
            if sent >= max_attempts:
                # print(f"Máximo de {max_attempts} tentativas atingido")
                sent = 0
                friend_list_confirm(config, "open")
            return bc_team(config, "send", sent)

        """# verifica nome do membro do team
        if Pointers(config.pid).team_name_1() != config.member_name:
            bc_team(config, "leave")
            bc_team(config, "send")"""

    if action == "leave":
        right(config.hwnd, cords_bc["photo"][0], cords_bc["photo"][1])
        time.sleep(1)
        left(config.hwnd, cords_bc["leave_team"][0], cords_bc["leave_team"][1])
        time.sleep(1.5)
        # verifica se saiu do team
        if Pointers(config.pid).get_team_size() == 0:
            print("Left team")
        else:
            return bc_team(config, "leave")

    if action == "join":
        left(config.hwnd, cords_bc["team_info"][0], cords_bc["team_info"][1])
        time.sleep(0.5)
        left(config.hwnd, cords_bc["team_join"][0], cords_bc["team_join"][1])
        time.sleep(0.5)


def bc_enter(config):
    # iMAGEM PARA VERIFICAR SE ENTROU
    img = "Images/misc/inside.bmp"
    img_2 = "Images/misc/inside_2.bmp"

    # Verifica se está morto
    if Pointers(config.pid).get_hp() == 0:
        bc_dead(config)
        return bc(config)

    # Configurações
    entrance = [1395, -635]
    entrance_2 = [
        {"xY": [1395, -635], "via": [0, 0]}
    ]

    # Verifica posição e move se necessário
    x = Pointers(config.pid).get_x()
    y = Pointers(config.pid).get_y()
    time.sleep(0.1)

    if x != entrance[0] or y != entrance[1]:
        # Verifica SE JA ESTA DENTRO DA CAVE ANTES DE POSICIONAR LÁ FORA, bug de ficar travado no canto dentro da cave.
        if find_image(config, img):
            print(f"Char ja esta dentro da cave (IMG).")
            return
        else:
            for coords in entrance_2:
                print("Reposicionando na entrada")
                if find_image(config, img):
                    print(f"Char ja esta dentro da cave (IMG 2).")
                    return
                else:
                    travel(config, coords["xY"], cords_move, 2)

    # Interage com NPC
    bc_talk_npc(config, cords_bc["skull"][0], cords_bc["skull"][1])
    time.sleep(0.3)
    left(config.hwnd, cords_bc["skull_enter"][0], cords_bc["skull_enter"][1])
    time.sleep(0.5)

    # Verifica imagem primeiro (mais confiável)
    if find_image(config, img):
        print(f"Entrou na cave, corfirmando...")
        time.sleep(0.5)
        if find_image(config, img_2):
            print(f"Char ja esta dentro da cave, confirmado.")
        return

    # Se não entrou, tenta novamente
    return bc_enter(config)


def wait_pos(config):
    """Aguarda até que a posição se estabilize por 3 verificações consecutivas"""
    pointers = Pointers(config.pid)
    count_spot = 0
    prev_x, prev_y = None, None

    while True:
        x = pointers.get_x()
        y = pointers.get_y()

        if prev_x == x and prev_y == y:
            count_spot += 1
            if count_spot >= 3:
                return
        else:
            count_spot = 0

        prev_x, prev_y = x, y
        time.sleep(0.2)  # wait(200) em Lua


def travel_normal(config, target_xy, cords_move, tolerance):
    # Função para movimentar personagem no mapa até coordenadas específicas
    pointers = Pointers(config.pid)

    while abs(pointers.get_x() - target_xy[0]) > tolerance or abs(pointers.get_y() - target_xy[1]) > tolerance:

        x = pointers.get_x()
        y = pointers.get_y()

        # Posição via (equivalente ao cords.move.stop em Lua)
        via = [cords_move["stop"][0], cords_move["stop"][1]]

        # Calcular reposicionamento necessário
        repos = [x - target_xy[0], y - target_xy[1]]

        # Verificar se precisa reposicionar (com tolerância)
        if abs(repos[0]) > tolerance or abs(repos[1]) > tolerance:
            # Eixo X
            if abs(repos[0]) > tolerance:
                via[0] = via[0] - repos[0]

            # Eixo Y
            if abs(repos[1]) > tolerance:
                via[1] = via[1] + repos[1]

            # Viajar (clique direito)
            right(config.hwnd, int(via[0]), int(via[1]))
            time.sleep(0.1)

            # Aguardar enquanto o personagem se move
            while True:
                time.sleep(0.1)  # wait(100)
                current_x = pointers.get_x()
                current_y = pointers.get_y()

                if current_x == x and current_y == y:
                    break

                x = current_x
                y = current_y

    # Resetar cursor (clique esquerdo)
    left(config.hwnd, cords_move["mouse_reset"][0], cords_move["mouse_reset"][1])
    time.sleep(0.1)  # wait(100)


def travel(config, target_xy, cords_move, tolerance, path_coords=None):
    pointers = Pointers(config.pid)
    max_attempts = 100  # Máximo de tentativas para evitar loop infinito
    attempt = 0
    stuck_counter = 0
    last_position = None
    circular_movement_count = 0  # Contador para movimentos circulares (mantido para compatibilidade)
    direct_movement_attempts = 0  # Contador para tentativas de movimento direto
    current_path_index = 0  # Índice da coordenada atual no caminho

    def get_effective_tolerance(current_target, is_final_target):

        if is_final_target and current_target == target_xy:
            return 0  # Tolerância zero para o destino final
        return tolerance  # Tolerância normal para coordenadas intermediárias

    def find_next_coordinate_in_path(current_pos, coords_list):

        if not coords_list:
            return None, -1

        # Encontrar a coordenada mais próxima da posição atual
        min_distance = float('inf')
        closest_index = 0

        for i, coord_dict in enumerate(coords_list):
            coord = coord_dict["xY"]
            distance = ((current_pos[0] - coord[0]) ** 2 + (current_pos[1] - coord[1]) ** 2) ** 0.5

            if distance < min_distance:
                min_distance = distance
                closest_index = i

        # Se está muito próximo de uma coordenada do caminho (< 15px), ir para a próxima
        if min_distance < 15 and closest_index < len(coords_list) - 1:
            next_index = closest_index + 1
            return coords_list[next_index]["xY"], next_index

        # Caso contrário, ir para a coordenada mais próxima
        return coords_list[closest_index]["xY"], closest_index

    def find_closest_coordinate(current_pos, coords_list, exclude_current=True, min_distance_threshold=15):

        if not coords_list:
            return None

        min_distance = float('inf')
        closest_coord = None

        for coord_dict in coords_list:
            coord = coord_dict["xY"]
            distance = ((current_pos[0] - coord[0]) ** 2 + (current_pos[1] - coord[1]) ** 2) ** 0.5

            # Se exclude_current está ativo, pular coordenadas muito próximas da atual
            if exclude_current and distance < min_distance_threshold:
                continue

            if distance < min_distance:
                min_distance = distance
                closest_coord = coord

        return closest_coord

    def try_direct_movement_to_next_path_coord(current_x, current_y):

        if not path_coords:
            return False

        # Encontrar próxima coordenada no caminho
        next_coord, next_index = find_next_coordinate_in_path((current_x, current_y), path_coords)

        if not next_coord:
            print("Não há próxima coordenada no caminho, tentando ir direto para o alvo")
            target_coord = target_xy
        else:
            print(
                f"Tentando movimento direto para próxima coordenada do caminho: [{next_coord[0]}, {next_coord[1]}] (índice {next_index})")
            target_coord = next_coord
            # Atualizar índice global
            nonlocal current_path_index
            current_path_index = next_index

        # Usar a mesma lógica de cálculo do movimento normal
        # Posição central do mapa (equivalente ao cords.move.stop)
        via = [cords_move["stop"][0], cords_move["stop"][1]]

        # Calcular o reposicionamento necessário (diferença atual vs coordenada de destino)
        repos = [current_x - target_coord[0], current_y - target_coord[1]]

        # Ajustar eixo X
        if abs(repos[0]) > tolerance:
            via[0] = via[0] - repos[0]

        # Ajustar eixo Y
        if abs(repos[1]) > tolerance:
            via[1] = via[1] + repos[1]

        print(
            f"Calculando movimento: Posição atual [{current_x}, {current_y}] -> Via [{via[0]}, {via[1]}] -> Destino [{target_coord[0]}, {target_coord[1]}]")

        # Executar movimento (clique direito na posição calculada)
        right(config.hwnd, int(via[0]), int(via[1]))
        time.sleep(2.0)  # Aguardar 2 segundos

        # Verificar se conseguiu se mover
        check_x = pointers.get_x()
        check_y = pointers.get_y()

        if check_x is not None and check_y is not None:
            distance_moved = ((check_x - current_x) ** 2 + (check_y - current_y) ** 2) ** 0.5

            if distance_moved > 4:
                print(f"Movimento direto bem-sucedido! Nova posição: [{check_x}, {check_y}]")
                return True
            else:
                print(f"Movimento direto falhou (distância: {distance_moved:.1f}px)")
                return False

        return False

    def get_current_target(current_x, current_y):

        if not path_coords:
            return target_xy, True

        # Se já está no destino final, retornar o destino
        distance_to_final = ((current_x - target_xy[0]) ** 2 + (current_y - target_xy[1]) ** 2) ** 0.5
        if distance_to_final <= 0:  # Usar tolerância 0 para verificar se já está no destino final
            return target_xy, True

        # Encontrar próxima coordenada no caminho
        next_coord, next_index = find_next_coordinate_in_path((current_x, current_y), path_coords)

        if next_coord:
            # Atualizar índice global
            nonlocal current_path_index
            current_path_index = next_index

            # Verificar se é a última coordenada do caminho
            is_last_coord = (next_index == len(path_coords) - 1)

            return next_coord, is_last_coord
        else:
            # Se não há próxima coordenada no caminho, ir para o destino final
            return target_xy, True

    def perform_unstuck_sequence(stuck_x, stuck_y):

        nonlocal direct_movement_attempts  # Declarar no início da função

        print(f"Personagem travado em [{stuck_x}, {stuck_y}], iniciando estratégias de destravamento...")

        # PRIMEIRA ESTRATÉGIA: Movimento direto para próxima coordenada do caminho
        if path_coords and direct_movement_attempts < 1:  # Máximo 3 tentativas de movimento direto
            direct_movement_attempts += 1
            print(f"Tentativa {direct_movement_attempts}/3 de movimento direto...")

            if try_direct_movement_to_next_path_coord(stuck_x, stuck_y):
                print("Destravamento por movimento direto bem-sucedido!")
                direct_movement_attempts = 0  # Reset contador após sucesso
                return True
            else:
                print(f"Movimento direto falhou (tentativa {direct_movement_attempts}/3)")

            # Se ainda tem tentativas de movimento direto, falhar para tentar novamente
            if direct_movement_attempts < 1:
                return False

        # SEGUNDA ESTRATÉGIA: Movimento circular (após esgotar tentativas diretas)
        print("Movimento direto esgotado ou não disponível, iniciando movimento circular...")
        direct_movement_attempts = 0  # Reset para próximas vezes

        # Salvar posição inicial do travamento
        stuck_position = (stuck_x, stuck_y)
        circular_radius = 10  # Raio inicial do movimento circular
        max_circular_attempts = 10  # Máximo de tentativas circulares

        print(f"Executando movimento circular para destravar...")

        # Loop com limite para destravar com movimento circular
        for circular_attempt in range(max_circular_attempts):
            print(f"Tentativa circular {circular_attempt + 1}/{max_circular_attempts} com raio {circular_radius}px...")

            # Posição central do movimento (cords_move["stop"])
            center_x = cords_move["stop"][0]
            center_y = cords_move["stop"][1]

            # Definir as 8 posições circulares com raio atual
            # Usando aproximação para diagonal (raio * 0.7 ≈ raio * 3/4)
            diagonal_offset = int(circular_radius * 0.7)
            circular_positions = [
                [center_x + circular_radius, center_y],  # Direita
                [center_x + diagonal_offset, center_y - diagonal_offset],  # Diagonal direita-cima
                [center_x, center_y - circular_radius],  # Cima
                [center_x - diagonal_offset, center_y - diagonal_offset],  # Diagonal esquerda-cima
                [center_x - circular_radius, center_y],  # Esquerda
                [center_x - diagonal_offset, center_y + diagonal_offset],  # Diagonal esquerda-baixo
                [center_x, center_y + circular_radius],  # Baixo
                [center_x + diagonal_offset, center_y + diagonal_offset],  # Diagonal direita-baixo
            ]

            # Executar movimento circular completo
            for pos in circular_positions:
                right(config.hwnd, int(pos[0]), int(pos[1]))
                time.sleep(0.1)  # Pequena pausa entre cada ponto do círculo

            # Após movimento circular, tentar ir para a próxima coordenada do caminho
            current_x_after = pointers.get_x()
            current_y_after = pointers.get_y()

            if current_x_after is not None and current_y_after is not None:
                # Determinar próximo alvo após destravamento
                next_target_after_circular, _ = get_current_target(current_x_after, current_y_after)

                print(
                    f"Movimento circular concluído, tentando ir para próxima coordenada: [{next_target_after_circular[0]}, {next_target_after_circular[1]}]...")
                right(config.hwnd, int(next_target_after_circular[0]), int(next_target_after_circular[1]))
                time.sleep(0.3)  # Aguardar um pouco mais para o movimento

            # Aguardar 3 segundos para dar tempo do personagem se mover
            print("Aguardando 3 segundos para o personagem se mover...")
            time.sleep(2.0)

            # Verificar posição atual após tentativa
            check_x = pointers.get_x()
            check_y = pointers.get_y()

            if check_x is not None and check_y is not None:
                # Calcular distância da posição travada original
                distance_moved = ((check_x - stuck_position[0]) ** 2 + (check_y - stuck_position[1]) ** 2) ** 0.5

                # Só considera destravado se moveu mais que 4px da posição original
                if distance_moved > 4:
                    print(
                        f"Destravado com movimento circular! Posição anterior: [{stuck_position[0]}, {stuck_position[1]}], Nova posição: [{check_x}, {check_y}], Distância: {distance_moved:.1f}px")
                    return True
                else:
                    # Ainda considerado travado se moveu menos que 10px
                    circular_radius += 2
                    print(
                        f"Movimento insuficiente ({distance_moved:.1f}px < 10px), ainda travado. Aumentando raio para {circular_radius}px")

                    # Limitar raio máximo para evitar sair muito da tela
                    if circular_radius > 25:
                        print("Raio máximo atingido, reiniciando com raio 4px...")
                        circular_radius = 10
            else:
                print("Erro ao verificar posição após movimento circular, tentando novamente...")
                time.sleep(0.2)

        print(f"Falha no destravamento após {max_circular_attempts} tentativas circulares")
        return False

    while attempt < max_attempts:
        try:
            # Obter posição atual
            x = pointers.get_x()
            y = pointers.get_y()

            # Verificar se pointer retornou valores válidos
            if x is None or y is None:
                print(f"Pointer falhou na tentativa {attempt + 1}, tentando novamente...")
                time.sleep(0.2)
                attempt += 1
                continue

            # Determinar alvo atual (pode ser uma coordenada do caminho ou o destino final)
            current_target, is_final_target = get_current_target(x, y)

            # Obter tolerância efetiva para o alvo atual
            effective_tolerance = get_effective_tolerance(current_target, is_final_target)

            # Verificar múltiplas vezes se realmente chegou ao alvo atual (anti-lag)
            arrival_confirmations = 0
            for _ in range(3):  # Verificar 3 vezes consecutivas
                test_x = pointers.get_x()
                test_y = pointers.get_y()

                if test_x is None or test_y is None:
                    break  # Pointer falhou, tentar novamente

                if abs(test_x - current_target[0]) <= effective_tolerance and abs(
                        test_y - current_target[1]) <= effective_tolerance:
                    arrival_confirmations += 1
                    time.sleep(0.05)  # Pequena pausa entre verificações
                else:
                    break

            # Se confirmou chegada 3 vezes consecutivas ao alvo atual
            if arrival_confirmations == 3:
                # Se chegou ao destino final OU à última coordenada do caminho, terminar
                if current_target == target_xy or is_final_target:
                    tolerance_msg = "tolerância ZERO" if effective_tolerance == 0 else f"tolerância {effective_tolerance}"
                    print(f"Destino alcançado com {tolerance_msg}: [{test_x}, {test_y}]")
                    return True  # SUCESSO - Destino final alcançado
                else:
                    # Chegou a uma coordenada intermediária do caminho, continuar para a próxima
                    print(f"Coordenada do caminho alcançada: [{test_x}, {test_y}], continuando...")
                    attempt += 1
                    continue

            # Detectar se está travado na mesma posição
            current_position = (x, y)
            if last_position == current_position:
                stuck_counter += 1
                if stuck_counter >= 5:  # Travado por 5 tentativas consecutivas

                    # Executar sequência de destravamento
                    if perform_unstuck_sequence(x, y):
                        # Destravamento bem-sucedido - resetar contadores e continuar loop principal
                        stuck_counter = 0
                        circular_movement_count = 0
                        direct_movement_attempts = 0
                        last_position = None  # Reset para forçar nova detecção de posição
                        print("Destravamento concluído, retornando ao loop principal...")
                        attempt += 1
                        continue  # Continuar o loop principal
                    else:
                        # Destravamento falhou - incrementar tentativa para evitar loop infinito
                        print("Destravamento falhou, continuando tentativas...")
                        attempt += 1
                        time.sleep(1.0)  # Aguardar um pouco antes da próxima tentativa
                        continue
            else:
                stuck_counter = 0
                circular_movement_count = 0  # Reset do contador quando não está mais travado
                direct_movement_attempts = 0  # Reset contador de movimento direto

            last_position = current_position

            # Verificar se já está no alvo atual (antes de tentar mover)
            if abs(x - current_target[0]) <= effective_tolerance and abs(y - current_target[1]) <= effective_tolerance:
                continue  # Vai para a verificação de confirmação no início do loop

            # Posição central do mapa (equivalente ao cords.move.stop)
            via = [cords_move["stop"][0], cords_move["stop"][1]]

            # Calcular o reposicionamento necessário (diferença atual vs alvo atual)
            repos = [x - current_target[0], y - current_target[1]]

            # Verificar se precisa reposicionar (fora da tolerância efetiva)
            if abs(repos[0]) > effective_tolerance or abs(repos[1]) > effective_tolerance:

                # Ajustar eixo X
                if abs(repos[0]) > effective_tolerance:
                    via[0] = via[0] - repos[0]

                # Ajustar eixo Y
                if abs(repos[1]) > effective_tolerance:
                    via[1] = via[1] + repos[1]

                # Executar movimento (clique direito na posição calculada)
                right(config.hwnd, int(via[0]), int(via[1]))
                time.sleep(0.1)

                # Aguardar o personagem se mover com timeout
                movement_timeout = 0
                max_wait_time = 50  # 5 segundos máximo
                initial_x, initial_y = x, y

                while movement_timeout < max_wait_time:
                    time.sleep(0.1)
                    movement_timeout += 1

                    try:
                        # Obter nova posição
                        current_x = pointers.get_x()
                        current_y = pointers.get_y()

                        # Verificar se pointer retornou valores válidos
                        if current_x is None or current_y is None:
                            continue

                        # Verificar se chegou ao alvo atual durante o movimento
                        if abs(current_x - current_target[0]) <= effective_tolerance and abs(
                                current_y - current_target[1]) <= effective_tolerance:
                            break

                        # Se parou de se mover (posição não mudou por 3 verificações)
                        if current_x == x and current_y == y:
                            stillness_count = 0
                            for _ in range(3):
                                time.sleep(0.1)
                                check_x = pointers.get_x()
                                check_y = pointers.get_y()
                                if check_x == current_x and check_y == current_y:
                                    stillness_count += 1
                                else:
                                    break

                            if stillness_count == 3:
                                break  # Realmente parou

                        # Atualizar posição para próxima verificação
                        x = current_x
                        y = current_y

                    except Exception as e:
                        print(f"Erro ao verificar movimento: {e}")
                        continue

            attempt += 1

            # Debug a cada 10 tentativas
            if attempt % 10 == 0:
                distance = ((x - current_target[0]) ** 2 + (y - current_target[1]) ** 2) ** 0.5
                target_type = "FINAL" if is_final_target else "CAMINHO"
                tolerance_info = f"tolerância {effective_tolerance}"
                print(
                    f"Tentativa {attempt}: Posição [{x}, {y}], Distância: {distance:.1f}, Alvo {target_type}: [{current_target[0]}, {current_target[1]}] ({tolerance_info})")

        except Exception as e:
            print(f"Erro na tentativa {attempt + 1}: {e}")
            time.sleep(0.2)
            attempt += 1
            continue

    # Verificação final - se chegou aqui, esgotou as tentativas
    try:
        final_x = pointers.get_x()
        final_y = pointers.get_y()

        if final_x is not None and final_y is not None:
            # Verificar se chegou ao destino final com tolerância ZERO
            final_distance_to_target = ((final_x - target_xy[0]) ** 2 + (final_y - target_xy[1]) ** 2) ** 0.5

            # Se tem caminho, verificar se está na última coordenada
            if path_coords:
                last_coord = path_coords[-1]["xY"]
                distance_to_last_coord = ((final_x - last_coord[0]) ** 2 + (final_y - last_coord[1]) ** 2) ** 0.5

                if final_distance_to_target == 0:  # Tolerância ZERO para destino final
                    print(f"Destino final alcançado com PRECISÃO EXATA: [{final_x}, {final_y}]")
                    return True
                elif distance_to_last_coord <= tolerance:
                    print(f"Última coordenada do caminho alcançada: [{final_x}, {final_y}]")
                    return True
                else:
                    print(
                        f"AVISO: Máximo de tentativas atingido. Distância final: {final_distance_to_target:.1f} (tolerância ZERO exigida)")
                    print(f"Distância para última coord do caminho: {distance_to_last_coord:.1f}")
                    print(f"Posição final: [{final_x}, {final_y}], Alvo: [{target_xy[0]}, {target_xy[1]}]")
                    return False
            else:
                if final_distance_to_target == 0:  # Tolerância ZERO para destino final
                    print(f"Destino final alcançado com PRECISÃO EXATA: [{final_x}, {final_y}]")
                    return True
                else:
                    print(
                        f"AVISO: Máximo de tentativas atingido. Distância final: {final_distance_to_target:.1f} (tolerância ZERO exigida)")
                    print(f"Posição final: [{final_x}, {final_y}], Alvo: [{target_xy[0]}, {target_xy[1]}]")
                    return False

        # Resetar cursor após chegar ao destino (ou falhar)
        # left(config.hwnd, cords_move["mouse_reset"][0], cords_move["mouse_reset"][1])
        time.sleep(0.1)
        return False

    except Exception as e:
        print(f"Erro na verificação final: {e}")
        # Mesmo com erro, tentar resetar o cursor
        try:
            # left(config.hwnd, cords_move["mouse_reset"][0], cords_move["mouse_reset"][1])
            time.sleep(0.1)
        except:
            pass
        return False


def bc_go_to_altar(config):
    send(config.hwnd, config.bc_mount_speed)
    send(config.hwnd, config.bc_mount_speed)

    for coords in altar:
        travel(config, coords["xY"], cords_move, 2, altar)


def bc_enter_altar(config):
    """Função para entrar no altar"""
    stair_path = [
        {"xY": [204, 45]},
        {"xY": [201, 22]},
        {"xY": [210, 22]},
        {"xY": [244, 22]},
        {"xY": [242, 45]},
        {"xY": [225, 45]},
        {"xY": [219, 45]}
    ]

    Pointers(config.pid).write_camera(380, 0, 30)
    time.sleep(0.2)

    entrance = [219, 45]

    x = Pointers(config.pid).get_x()
    y = Pointers(config.pid).get_y()
    time.sleep(0.5)

    if x != entrance[0] or y != entrance[1]:
        for coords in stair_path:
            travel(config, coords["xY"], cords_move, 2, stair_path)

    # talk with altar_npc
    bc_talk_npc(config, cords_bc["altar_npc"][0], cords_bc["altar_npc"][1])
    time.sleep(0.2)
    left(config.hwnd, cords_bc["altar_enter"][0], cords_bc["altar_enter"][1])
    time.sleep(1)


def bc_gun_witchers(config):
    for coords in gun_withc:
        # print(coords)
        travel_normal(config, coords["xY"], cords_move, 0)


def kill_gun_witchers(config):
    bc_mount(config, "dismount")

    guns = [101, -405]

    while Pointers(config.pid).is_in_battle():
        if Pointers(config.pid).mount() != 0:
            print("Dismounting...")
            send(config.hwnd, config.bc_mount)
            time.sleep(1)

        # mantem o personagem na cordenada dos gun witchers
        x = Pointers(config.pid).get_x()
        y = Pointers(config.pid).get_y()
        time.sleep(1)
        if x != guns[0] or y != guns[1]:
            safe_spot_back(config, guns)

        bc_battle_cure(config)

        if Pointers(config.pid).is_target_dead() and Pointers(config.pid).is_target_selected():
            send(config.hwnd, "ESC")
            time.sleep(0.5)

        if Pointers(config.pid).get_system_menu():
            send(config.hwnd, "ESC")
            time.sleep(0.5)

        if config.bc_stamina == "ON":
            if config.stamina_combo == "ON":
                if Pointers(config.pid).get_monk_combo() < config.combo:
                    send(config.hwnd, config.bc_atk_1)
                    time.sleep(config.atk_delay / 10.0)
                    send(config.hwnd, config.bc_atk_2)
                    time.sleep(config.atk_delay / 10.0)
                    send(config.hwnd, config.bc_atk_3)
                    time.sleep(config.atk_delay / 10.0)

                if Pointers(config.pid).get_monk_combo() >= config.combo:
                    send(config.hwnd, config.bc_atk_combo)
                    time.sleep(config.atk_delay / 10.0)
            else:
                send(config.hwnd, config.bc_atk_1)
                time.sleep(config.atk_delay / 10.0)
                send(config.hwnd, config.bc_atk_2)
                time.sleep(config.atk_delay / 10.0)
                send(config.hwnd, config.bc_atk_3)
                time.sleep(config.atk_delay / 10.0)

        if config.bc_mana == "ON":
            send(config.hwnd, config.bc_atk_1)
            time.sleep(config.atk_delay / 10.0)
            send(config.hwnd, config.bc_atk_2)
            time.sleep(config.atk_delay / 10.0)
            send(config.hwnd, config.bc_atk_3)
            time.sleep(config.atk_delay / 10.0)
            if config.use_aoe == "ON":
                if mp_percentage(config) >= config.use_aoe_until:
                    time.sleep(config.atk_delay / 10.0)
                    send(config.hwnd, config.bc_atk_aoe)

        if config.bc_fairy == "ON":
            send(config.hwnd, config.bc_atk_1)
            time.sleep(config.atk_delay / 10.0)
            send(config.hwnd, config.bc_atk_2)
            time.sleep(config.atk_delay / 10.0)
            send(config.hwnd, config.bc_atk_3)
            time.sleep(config.atk_delay / 10.0)

    if Pointers(config.pid).is_in_battle():
        return kill_gun_witchers(config)


def bc_battle_cure(config):
    low_hp_battle = config.bc_battle_low_hp
    low_mp_battle = config.bc_battle_low_mp

    hp_p = hp_percentage(config)
    mp_p = mp_percentage(config)

    if config.bc_stamina == "ON":
        if hp_p <= low_hp_battle:
            time.sleep(0.2)
            send(config.hwnd, config.bc_pot_hp_battle)

    if config.bc_mana == "ON":
        if hp_p <= low_hp_battle:
            time.sleep(0.2)
            send(config.hwnd, config.bc_pot_hp_battle)

        if mp_p <= low_mp_battle:
            time.sleep(0.2)
            send(config.hwnd, config.bc_pot_mp_battle)

    if config.bc_fairy == "ON":
        if hp_p <= low_hp_battle:
            send(config.hwnd, config.select_yourself)
            time.sleep(0.2)
            while Pointers(config.pid).get_hp() < Pointers(config.pid).get_max_hp() - 1500:
                send(config.hwnd, config.select_yourself)
                time.sleep(1)
                send(config.hwnd, config.bc_healing_spell)
                time.sleep(1)
            if mp_p <= low_mp_battle:
                time.sleep(0.2)
                send(config.hwnd, config.bc_pot_mp_battle)
            time.sleep(0.5)
            send(config.hwnd, config.next_target)


def bc_cure(config):
    low_hp = config.bc_low_hp
    low_mp = config.bc_low_mp

    hp_p = hp_percentage(config)
    mp_p = mp_percentage(config)

    guns = [101, -405]
    x = Pointers(config.pid).get_x()
    y = Pointers(config.pid).get_y()

    if hp_p <= low_hp:
        print("HP is Bellow the Percentage", low_hp, hp_p)
        if x != guns[0] or y != guns[1]:
            safe_spot_back(config, guns)

        if config.bc_fairy == "ON":
            send(config.hwnd, config.select_yourself)
            time.sleep(0.2)
            while Pointers(config.pid).get_hp() < Pointers(config.pid).get_max_hp() - 100:
                send(config.hwnd, config.select_yourself)
                time.sleep(1)
                send(config.hwnd, config.bc_healing_spell)
                time.sleep(1)

        bc_sit(config)
        time.sleep(1)

        if config.bc_stamina == "ON":
            send(config.hwnd, config.bc_pot_hp)
            time.sleep(1)
            bc_sit(config)

        if config.bc_mana == "ON":
            send(config.hwnd, config.bc_pot_hp)
            time.sleep(0.5)
            send(config.hwnd, config.bc_wizz_super)
            time.sleep(1)
            bc_sit(config)

        timer = QTimer()
        timer.setInterval(15000)
        timer.start()
        start_time = time.time()

        while Pointers(config.pid).get_hp() < Pointers(config.pid).get_max_hp() - 100:
            bc_sit(config)
            time.sleep(1)
            elapsed_time = time.time() - start_time
            if elapsed_time >= 15 and Pointers(config.pid).get_hp() < Pointers(config.pid).get_max_hp() - 100:
                send(config.hwnd, config.bc_pot_hp)
                print("Timer expired: sent potion command")
                start_time = time.time()  # Reseta o contador de tempo

    if mp_p <= low_mp:
        print("Mana is Bellow the Percentage", low_mp, mp_p)
        if x != guns[0] or y != guns[1]:
            safe_spot_back(config, guns)

        bc_sit(config)
        time.sleep(1)

        if config.bc_mana == "ON" or config.bc_fairy == "ON":
            send(config.hwnd, config.bc_pot_mp)
            time.sleep(1)
            bc_sit(config)

        timer = QTimer()
        timer.setInterval(15000)
        timer.start()
        start_time = time.time()

        while Pointers(config.pid).get_mana() < Pointers(config.pid).get_max_mana() - 100:
            bc_sit(config)
            time.sleep(1)
            elapsed_time = time.time() - start_time
            if elapsed_time >= 15 and Pointers(config.pid).get_mana() < Pointers(config.pid).get_max_mana() - 100:
                send(config.hwnd, config.bc_pot_mp)
                print("Timer expired: sent potion command")
                start_time = time.time()  # Reseta o contador de tempo


def bc_cure_at_start(config):
    low_hp = config.bc_low_hp
    hp_p = hp_percentage(config)

    if hp_p <= low_hp:
        print("HP is Bellow the Percentage", low_hp, hp_p)

        bc_mount(config, "dismount")
        time.sleep(2)

        if config.bc_fairy == "ON":
            send(config.hwnd, config.select_yourself)
            time.sleep(0.2)
            while Pointers(config.pid).get_hp() < Pointers(config.pid).get_max_hp() - 100:
                send(config.hwnd, config.select_yourself)
                time.sleep(1)
                send(config.hwnd, config.bc_healing_spell)
                time.sleep(1)

        if config.bc_stamina == "ON":
            send(config.hwnd, config.bc_pot_hp)
            time.sleep(1)
            bc_sit(config)

        if config.bc_mana == "ON":
            send(config.hwnd, config.bc_wizz_super)

        timer = QTimer()
        timer.setInterval(15000)
        timer.start()
        start_time = time.time()

        while Pointers(config.pid).get_hp() < Pointers(config.pid).get_max_hp() - 500:
            time.sleep(1)
            bc_sit(config)
            elapsed_time = time.time() - start_time
            if elapsed_time >= 15 and Pointers(config.pid).get_hp() < Pointers(config.pid).get_max_hp() - 500:
                send(config.hwnd, config.bc_pot_hp)
                print("Timer expired: sent potion command")
                start_time = time.time()  # Reseta o contador de tempo

        time.sleep(5)

        bc_mount(config, "mount")
        time.sleep(1)


def bc_go_to_blaze(config):
    for coords in blaze:
        # print(coords)
        travel_normal(config, coords["xY"], cords_move, 0)

    boss_pos_1 = [74, -394]
    boss_pos_2 = [74, -416]
    safe_spot_back(config, boss_pos_1)
    safe_spot_back(config, boss_pos_2)


def bc_go_to_blaze_2(config):
    bc_mount(config, "mount")
    time.sleep(1)
    for coords in blaze_2:
        # print(coords)
        travel_normal(config, coords["xY"], cords_move, 2)

    boss_pos_1 = [74, -394]
    boss_pos_2 = [74, -416]
    safe_spot_back(config, boss_pos_1)
    safe_spot_back(config, boss_pos_2)


def bc_kill_blaze(config):
    blaze = [70, -406]
    safe_spot_back(config, blaze)
    bc_mount(config, "dismount")
    stage = 0

    # mount_confirm(config, "dismount")

    send(config.hwnd, config.next_target)  # tab pra caso o pet estar selecionado

    while Pointers(config.pid).is_in_battle():

        if Pointers(config.pid).get_target_name() == "Blaze Skull Marshal":
            img = "Images/misc/stage1.bmp"
            if find_image(config, img):
                print("first stage")
            else:
                print("second stage")
                stage += 1

        if stage == 2:
            time.sleep(1)
            send(config.hwnd, config.break_soul)
            time.sleep(config.atk_delay / 10.0)
            print(stage)

        if Pointers(config.pid).get_target_name() == Pointers(config.pid).get_char_name():
            send(config.hwnd, config.next_target)

        if Pointers(config.pid).mount() != 0:
            print("Dismounting...")
            send(config.hwnd, config.bc_mount)
            time.sleep(1)

        x = Pointers(config.pid).get_x()
        y = Pointers(config.pid).get_y()
        time.sleep(1)
        if x != blaze[0] or y != blaze[1]:
            safe_spot_back(config, blaze)

        bc_battle_cure(config)

        if Pointers(config.pid).is_target_dead():
            send(config.hwnd, "TAB")
            time.sleep(0.2)

        if config.bc_stamina == "ON":
            if config.stamina_combo == "ON":
                if Pointers(config.pid).get_monk_combo() < config.combo:
                    send(config.hwnd, config.bc_atk_1)
                    time.sleep(config.atk_delay / 10.0)
                    send(config.hwnd, config.bc_atk_2)
                    time.sleep(config.atk_delay / 10.0)
                    send(config.hwnd, config.bc_atk_3)
                    time.sleep(config.atk_delay / 10.0)

                if Pointers(config.pid).get_monk_combo() >= config.combo:
                    send(config.hwnd, config.bc_atk_combo)
                    time.sleep(config.atk_delay / 10.0)
            else:
                send(config.hwnd, config.bc_atk_1)
                time.sleep(config.atk_delay / 10.0)
                send(config.hwnd, config.bc_atk_2)
                time.sleep(config.atk_delay / 10.0)
                send(config.hwnd, config.bc_atk_3)
                time.sleep(config.atk_delay / 10.0)

        if config.bc_mana == "ON":
            send(config.hwnd, config.bc_atk_1)
            time.sleep(config.atk_delay / 10.0)
            send(config.hwnd, config.bc_atk_2)
            time.sleep(config.atk_delay / 10.0)
            send(config.hwnd, config.bc_atk_3)
            time.sleep(config.atk_delay / 10.0)
            if config.use_aoe == "ON":
                if mp_percentage(config) >= config.use_aoe_until:
                    time.sleep(config.atk_delay / 10.0)
                    send(config.hwnd, config.bc_atk_aoe)

        if config.bc_fairy == "ON":
            send(config.hwnd, config.bc_atk_1)
            time.sleep(config.atk_delay / 10.0)
            send(config.hwnd, config.bc_atk_2)
            time.sleep(config.atk_delay / 10.0)
            send(config.hwnd, config.bc_atk_3)
            time.sleep(config.atk_delay / 10.0)


def bc_use_courage(config):
    # reseta o mouse para nao ficar aba de item aberta em cima da badge
    kleft(config.hwnd, cords_move["mouse_reset"][0], cords_move["mouse_reset"][1])
    time.sleep(0.5)

    send(config.hwnd, config.inventory)
    time.sleep(1)

    inventory_confirm(config, "open")

    time.sleep(1)

    # Captura o conteúdo da janela
    try:
        rect = win32gui.GetWindowRect(config.hwnd)
        width, height = rect[2] - rect[0], rect[3] - rect[1]

        hwnd_dc = win32gui.GetWindowDC(config.hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()
        save_bitmap = win32ui.CreateBitmap()
        save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
        save_dc.SelectObject(save_bitmap)

        save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)

        bmp_info = save_bitmap.GetInfo()
        bmp_str = save_bitmap.GetBitmapBits(True)
        img = np.frombuffer(bmp_str, dtype=np.uint8)
        img.shape = (bmp_info['bmHeight'], bmp_info['bmWidth'], 4)

        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(config.hwnd, hwnd_dc)
        win32gui.DeleteObject(save_bitmap.GetHandle())

        window_img = img[..., :3]

    except Exception as e:
        print(f"Erro ao capturar a janela: {e}")
        return

    # Carrega apenas a imagem específica do badge
    badge_path = "Images/misc/badge.bmp"
    time.sleep(0.5)
    badge_image = cv2.imread(badge_path, cv2.IMREAD_GRAYSCALE)

    if badge_image is None:
        print("Badge image not found.")
        send(config.hwnd, config.inventory)
        time.sleep(0.5)
        return

    # Procura o badge na janela
    window_gray = cv2.cvtColor(window_img, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(window_gray, badge_image, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val > 0.7:
        # Ajusta para descontar a barra de título
        SM_CYCAPTION = 4
        title_bar_height = ctypes.windll.user32.GetSystemMetrics(SM_CYCAPTION)
        badge_x = max_loc[0]
        badge_y = max_loc[1] - title_bar_height

        right(config.hwnd, badge_x, badge_y)
        print("Badge clicked successfully")
        time.sleep(0.5)
    else:
        print("Badge not found on screen")

    send(config.hwnd, config.inventory)
    time.sleep(1)

    inventory_confirm(config, "close")

    if Pointers(config.pid).is_in_battle():
        bc_kill_blaze(config)


def bc_leave(config):
    Pointers(config.pid).write_camera(380, 0, 40)

    if Pointers(config.pid).is_in_battle():
        bc_kill_blaze(config)

    time.sleep(0.5)

    bc_mount(config, "mount")

    npc = [82, -399]
    exit = [1395, -629]
    safe_spot_back(config, npc)
    inventory_confirm(config, "close")
    bc_talk_npc(config, cords_bc["npc_leave"][0], cords_bc["npc_leave"][1])
    time.sleep(0.2)
    left(config.hwnd, cords_bc["exit"][0], cords_bc["exit"][1])
    time.sleep(2)

    x = Pointers(config.pid).get_x()
    y = Pointers(config.pid).get_y()
    time.sleep(0.1)
    print(f"X = {x}, Y = {y}")

    if x == exit[0] or y == exit[1]:
        print("Leave success")

    if x == npc[0] or y == npc[1]:
        print("Leaving again")
        bc_leave(config)


def find_image(config, img_path):
    # Captura o conteúdo da janela
    try:
        rect = win32gui.GetWindowRect(config.hwnd)
        width, height = rect[2] - rect[0], rect[3] - rect[1]

        hwnd_dc = win32gui.GetWindowDC(config.hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()
        save_bitmap = win32ui.CreateBitmap()
        save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
        save_dc.SelectObject(save_bitmap)

        save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)

        bmp_info = save_bitmap.GetInfo()
        bmp_str = save_bitmap.GetBitmapBits(True)
        img = np.frombuffer(bmp_str, dtype=np.uint8)
        img.shape = (bmp_info['bmHeight'], bmp_info['bmWidth'], 4)

        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(config.hwnd, hwnd_dc)
        win32gui.DeleteObject(save_bitmap.GetHandle())

        window_img = img[..., :3]

    except Exception as e:
        print(f"Erro ao capturar a janela: {e}")
        return

    image_to_find = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    if image_to_find is None:
        print("image not found.")
    # Procura a imagem na janela
    window_gray = cv2.cvtColor(window_img, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(window_gray, image_to_find, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val > 0.9:
        return True
    else:
        return False
        return False

    # Procura a imagem na janela
    window_gray = cv2.cvtColor(window_img, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(window_gray, image_to_find, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val > 0.9:
        return True
    else:
        return False

    # Procura  na janela
    window_gray = cv2.cvtColor(window_img, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(window_gray, image_to_find, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val > 0.9:
        print("Image found successfully")
        time.sleep(0.2)
        return True
    else:
        print("Image not found on screen")
        time.sleep(0.2)
        return False


def surrounds_confirm(config, action):
    img = "Images/misc/surr.bmp"

    if action == "close":
        if find_image(config, img):
            print("Surrounds Opened, closing...")
            left(config.hwnd, cords_bc["surrounds"][0], cords_bc["surrounds"][1])
        else:
            print("Surrounds is closed.")

    if action == "open":
        if not find_image(config, img):
            print("Surrounds is closed, opening...")
            left(config.hwnd, cords_bc["surrounds"][0], cords_bc["surrounds"][1])
        else:
            print("Surrounds Opened.")


def friend_list_confirm(config, action):
    if action == "close":
        img = "Images/misc/block_list.bmp"
        if find_image(config, img):
            print("Friend List Opened, closing...")
            send(config.hwnd, config.friend_list)
        else:
            print("Friend List is closed.")

    if action == "open":
        img_friend = "Images/misc/friend_list.bmp"
        img_block = "Images/misc/block_list.bmp"

        if not find_image(config, img_block) or not find_image(config, img_friend):
            print("Friend List is closed, opening...")
            send(config.hwnd, config.friend_list)
            time.sleep(1)
            left(config.hwnd, cords_bc["block_list"][0], cords_bc["block_list"][1])

        if find_image(config, img_block):
            print("Friend List Opened.")


def mount_confirm(config, action):
    img = "Images/misc/mount.bmp"
    if action == "dismount":
        if find_image(config, img):
            print("Mounted, dismounting...")
            send(config.hwnd, config.mount)
            time.sleep(0.5)

    if action == "mount":
        if not find_image(config, img):
            print("Not Mounted, mounting...")
            send(config.hwnd, config.mount)
            time.sleep(5)


def inventory_confirm(config, action):
    img = "Images/misc/destroy-item.bmp"

    if action == "close":
        if find_image(config, img):
            print("Inventory Opened, closing...")
            send(config.hwnd, config.inventory)
        else:
            print("Inventory is closed.")

    if action == "open":
        if not find_image(config, img):
            print("Inventory is closed, opening...")
            send(config.hwnd, config.inventory)
        else:
            print("Inventory Opened.")


def bc_treasure_box(config):
    treasure_spot = [59, -402]

    Pointers(config.pid).write_camera(380, 270, 35)
    safe_spot_back(config, treasure_spot)

    kright(config.hwnd, cords_bc["treasure_box"][0], cords_bc["treasure_box"][1])
    time.sleep(6)

    kleft(config.hwnd, cords_bc["pick_up"][0], cords_bc["pick_up"][1])
    time.sleep(1)

    send(config.hwnd, config.next_target)

    while Pointers(config.pid).is_in_battle():

        if Pointers(config.pid).get_target_name() == Pointers(config.pid).get_char_name():
            send(config.hwnd, config.next_target)

        bc_battle_cure(config)

        if Pointers(config.pid).is_target_dead():
            send(config.hwnd, "TAB")
            time.sleep(0.2)

        if config.bc_stamina == "ON":
            if config.stamina_combo == "ON":
                if Pointers(config.pid).get_monk_combo() < config.combo:
                    send(config.hwnd, config.bc_atk_1)
                    time.sleep(config.atk_delay / 10.0)
                    send(config.hwnd, config.bc_atk_2)
                    time.sleep(config.atk_delay / 10.0)
                    send(config.hwnd, config.bc_atk_3)
                    time.sleep(config.atk_delay / 10.0)

                if Pointers(config.pid).get_monk_combo() >= config.combo:
                    send(config.hwnd, config.bc_atk_combo)
                    time.sleep(config.atk_delay / 10.0)
            else:
                send(config.hwnd, config.bc_atk_1)
                time.sleep(config.atk_delay / 10.0)
                send(config.hwnd, config.bc_atk_2)
                time.sleep(config.atk_delay / 10.0)
                send(config.hwnd, config.bc_atk_3)
                time.sleep(config.atk_delay / 10.0)

        if config.bc_mana == "ON":
            send(config.hwnd, config.bc_atk_1)
            time.sleep(config.atk_delay / 10.0)
            send(config.hwnd, config.bc_atk_2)
            time.sleep(config.atk_delay / 10.0)
            send(config.hwnd, config.bc_atk_3)
            time.sleep(config.atk_delay / 10.0)
            if config.use_aoe == "ON":
                if mp_percentage(config) >= config.use_aoe_until:
                    time.sleep(config.atk_delay / 10.0)
                    send(config.hwnd, config.bc_atk_aoe)

        if config.bc_fairy == "ON":
            send(config.hwnd, config.bc_atk_1)
            time.sleep(config.atk_delay / 10.0)
            send(config.hwnd, config.bc_atk_2)
            time.sleep(config.atk_delay / 10.0)
            send(config.hwnd, config.bc_atk_3)
            time.sleep(config.atk_delay / 10.0)


def bc_dead(config):
    if Pointers(config.pid).get_hp() == 0:
        print(f"Char {Pointers(config.pid).get_char_name()} is dead!")
        time.sleep(3)
        """Click on jackstraw"""
        left(config.hwnd, int(cords_game["jackstraw_ok"][0]), int(cords_game["jackstraw_ok"][1]))
        time.sleep(2)
        """Click on OK Revive Normal"""
        if Pointers(config.pid).get_hp() == 0:
            left(config.hwnd, int(cords_game["revive_ok"][0]), int(cords_game["revive_ok"][1]))
            time.sleep(2)

    if Pointers(config.pid).get_hp() == 0:
        return bc_dead(config)


def bc_delete_items(config):
    def inner():

        # Verifica se a mochila está aberta
        if not Pointers(config.pid).is_bag_open():
            print("Open bag")
            send(config.hwnd, config.inventory)
            time.sleep(0.5)
        else:
            print("Bag is open")
            time.sleep(0.5)

        def load_images(folder):
            """
            Carrega todas as imagens da pasta sem cache.
            """
            images = {}
            for filename in os.listdir(folder):
                full_path = os.path.join(folder, filename)
                image = cv2.imread(full_path, cv2.IMREAD_GRAYSCALE)
                if image is not None:
                    images[filename] = image
            return images

        def capture_window(hwnd):
            """
            Captura o conteúdo da janela especificada por hwnd, independentemente de sobreposições.
            """
            try:
                rect = win32gui.GetWindowRect(hwnd)
                width, height = rect[2] - rect[0], rect[3] - rect[1]

                hwnd_dc = win32gui.GetWindowDC(hwnd)
                mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
                save_dc = mfc_dc.CreateCompatibleDC()
                save_bitmap = win32ui.CreateBitmap()
                save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
                save_dc.SelectObject(save_bitmap)

                save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)

                bmp_info = save_bitmap.GetInfo()
                bmp_str = save_bitmap.GetBitmapBits(True)
                img = np.frombuffer(bmp_str, dtype=np.uint8)
                img.shape = (bmp_info['bmHeight'], bmp_info['bmWidth'], 4)

                save_dc.DeleteDC()
                mfc_dc.DeleteDC()
                win32gui.ReleaseDC(hwnd, hwnd_dc)
                win32gui.DeleteObject(save_bitmap.GetHandle())

                return img[..., :3]

            except Exception as e:
                print(f"Erro ao capturar a janela: {e}")
                raise

        def get_title_bar_height():
            """
            Obtém a altura da barra de título da janela usando a API do Windows.
            """
            SM_CYCAPTION = 4  # Constante para altura da barra de título
            return ctypes.windll.user32.GetSystemMetrics(SM_CYCAPTION)

        def find_image_in_window(target_image, hwnd):
            """
            Encontra uma imagem dentro da janela especificada pelo HWND,
            descontando a barra de título da janela.
            """
            title_bar_height = get_title_bar_height()

            # Capturar a imagem da janela
            window_img = capture_window(hwnd)
            window_gray = cv2.cvtColor(window_img, cv2.COLOR_BGR2GRAY)

            # Localizar a imagem na janela
            result = cv2.matchTemplate(window_gray, target_image, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            if max_val > 0.9:  # Ajuste o limiar conforme necessário
                adjusted_loc = (max_loc[0], max_loc[1] - title_bar_height)
                return adjusted_loc

            return None

        def find_items_in_window(item_images, hwnd):
            """
            Localiza itens em uma janela específica.
            """
            to_delete = []
            tolerance = 3  # Tolerância em pixels para coordenadas duplicadas

            window_img = capture_window(hwnd)
            window_gray = cv2.cvtColor(window_img, cv2.COLOR_BGR2GRAY)

            for offset in bag_offsets:
                x1, y1, width, height = offset

                bag_area = window_gray[y1:y1 + height, x1:x1 + width]

                for item_name, item_image in item_images.items():
                    result = cv2.matchTemplate(bag_area, item_image, cv2.TM_CCOEFF_NORMED)
                    threshold = 0.9
                    loc = np.where(result >= threshold)

                    for pt in zip(*loc[::-1]):
                        title_bar_height = get_title_bar_height()
                        global_x = x1 + pt[0]
                        global_y = y1 + pt[1] - title_bar_height

                        if not any(
                                abs(existing_x - global_x) <= tolerance and abs(existing_y - global_y) <= tolerance for
                                existing_x, existing_y in to_delete):
                            to_delete.append((global_x, global_y))

            return to_delete

        item_delete_path = "Images/BC_DELETE"
        item_images = load_images(item_delete_path)

        destroy_path = "Images/misc/destroy-item.bmp"
        destroy_image = cv2.imread(destroy_path, cv2.IMREAD_GRAYSCALE)
        coordinates = find_image_in_window(destroy_image, config.hwnd)

        if coordinates:
            destroy_x, destroy_y = coordinates

            bag_cords = [
                (destroy_x - 5, destroy_y - 200, destroy_x + 220, destroy_y - 15),
                (destroy_x + 250, destroy_y - 420, destroy_x + 490, destroy_y - 10),
            ]

            bag_offsets = [
                (destroy_x - 5, destroy_y - 200, destroy_x + 220, destroy_y - 15),
                (destroy_x + 250, destroy_y - 420, destroy_x + 490, destroy_y - 10),
            ]

            bag_images = []
            for x1, y1, x2, y2 in bag_cords:
                bag_img = capture_window(config.hwnd)[y1:y2, x1:x2]
                bag_images.append(bag_img)

            to_delete = find_items_in_window(item_images, config.hwnd)

            for item in to_delete:
                x, y = int(item[0]), int(item[1])

                left(config.hwnd, x, y)
                time.sleep(0.15)
                left(config.hwnd, destroy_x, destroy_y)
                time.sleep(0.15)
                left(config.hwnd, int(cords_game["deleter_ok"][0]), int(cords_game["deleter_ok"][1]))
                time.sleep(0.15)
        else:
            print("Destroy icon not found.")
        print("Close bag")
        send(config.hwnd, config.inventory)
        time.sleep(1)

    return inner


def bc_manual_auto_pick(config):
    for offset in range(20, 60, 20):
        right(config.hwnd, cords_bc["center_screen"][0] + offset, cords_bc["center_screen"][1])
        time.sleep(0.1)
        right(config.hwnd, cords_bc["center_screen"][0] - offset, cords_bc["center_screen"][1])
        time.sleep(0.1)
        right(config.hwnd, cords_bc["center_screen"][0], cords_bc["center_screen"][1] + offset)
        time.sleep(0.1)
        right(config.hwnd, cords_bc["center_screen"][0], cords_bc["center_screen"][1] - offset)
        time.sleep(0.1)

    left(config.hwnd, cords_bc["pick_up"][0], cords_bc["pick_up"][1])
    time.sleep(3)



def bot(config):
    global safe_spot, get_back_enable, heal_target_name, get_back_enable, sell_enable, next_cicle

    get_back_enable = 0
    sell_enable = 0
    next_cicle = 0

    x, y = Pointers(config.pid).get_x(), Pointers(config.pid).get_y()
    safe_spot = [x, y]
    print(f"Start  = {safe_spot}")

    manager = CycleManager()

    if config.deleter_bot == "ON":
        manager.add_cycle(deleter(config), config.deleter_delay, "Ciclo de Deleter")

    if config.get_back == "ON":
        minimap_minimize(config)

    if config.char_type == "Fairy Heal":
        manager.add_cycle(fairy_heal_buff_up(config), config.buff_delay, "Ciclo de Buff Fairy Heal")
    else:
        manager.add_cycle(buff_up(config), config.buff_delay, "Ciclo de Buff")

    manager.add_cycle(use_pet_food(config), config.pet_food_delay, "Ciclo de Pet Food")

    if config.char_type == "Fairy Attack":
        manager.add_cycle(fairy_attack_buff_up(config), config.buff_delay, "Ciclo de Buff Fairy Attack")

    if config.debug_ap == "ON":
        manager.add_cycle(debug_pet_ap(config), 3, "Debug Pet Ap")

    if config.get_back == "ON":
        get_back_enable = 1

    if config.char_type == "Fairy ATK/HEAL":
        manager.add_cycle(fairy_heal_buff_up(config), config.buff_delay, "Ciclo de Buff Fairy Heal")

    if config.autopick == "ON":
        press(config.hwnd, config.hide_players)

    while True:

        if config.get_back == "ON":
            check_distance(config, safe_spot)

        if config.sell_items == "ON":
            sell_items(config)

        if config.char_type == "Stamina":
            manager.execute_cycles()
            tab(config)
            kill(config)
            stamina_cure(config)
            dead(config)

        if config.char_type == "Mana":
            manager.execute_cycles()
            tab(config)
            kill(config)
            mana_cure(config)
            dead(config)

        if config.char_type == "Sin Lure/AOE":
            manager.execute_cycles()

            if config.autopick == "ON":
                config.autopick = "OFF"

            simitar_lure_kill(config)

        if config.char_type == "Fairy Heal":
            manager.execute_cycles()
            fairy_heal_follow(config)
            fairy_heal_cure(config)
            dead(config)
            sit(config)

        if config.char_type == "Fairy Attack":
            manager.execute_cycles()
            tab(config)
            kill(config)
            fairy_attack_cure(config)
            dead(config)

        if config.char_type == "Fairy ATK/HEAL":
            manager.execute_cycles()
            fairy_atk_heal_kill(config)
            fairy_attack_cure(config)
            fairy_heal_cure(config)
            dead(config)


# V1.6
# Procurar o monstro que esta no target
def search_monster(config):
    targetid = Pointers(config.pid).get_target_id()
    if targetid is None:
        print("Erro: ID do alvo não encontrado.")
        return None, None, None, None, None

    # Primeira chamada para search_id
    result = Pointers(config.pid).search_id()
    if result[0] is None or result[1] is None or result[2] is None:
        print(f"Erro: Falha ao buscar monstro. Tentando novamente...")
        # Tenta uma segunda vez antes de desistir
        result = Pointers(config.pid).search_id()
        if result[0] is None or result[1] is None or result[2] is None:
            print(f"Erro: Falha persistente ao buscar monstro.")
            return None, None, None, None, None

    monsterid = result  # Mantém compatibilidade com o código existente

    # Segunda chamada para search_id para obter as coordenadas e o ponteiro
    target_x, target_y, pointer = Pointers(config.pid).search_id()
    if target_x is None or target_y is None or pointer is None:
        print(f"Erro: Falha ao obter coordenadas do monstro.")
        return None, None, None, None, None

    return targetid, monsterid, target_x, target_y, pointer


# V1.6
# Pegar o loot
def get_loot(config):
    # print("Looting...")

    # Tenta clicar em um padrão circular mais amplo para pegar múltiplos loots
    for offset in range(20, 60, 20):
        right(config.hwnd, cords_game["loot"][0] + offset, cords_game["loot"][1])
        time.sleep(0.1)
        right(config.hwnd, cords_game["loot"][0] - offset, cords_game["loot"][1])
        time.sleep(0.1)
        right(config.hwnd, cords_game["loot"][0], cords_game["loot"][1] + offset)
        time.sleep(0.1)
        right(config.hwnd, cords_game["loot"][0], cords_game["loot"][1] - offset)
        time.sleep(0.1)

    left(config.hwnd, cords_game["pickup"][0], cords_game["pickup"][1])
    time.sleep(1)


# V1.6
# Retorna atual posição do personagem
def char_base(config):
    charposX = Pointers(config.pid).char_x()
    charposY = Pointers(config.pid).char_y()
    return charposX, charposY


# V1.6 
# Checa se realmente escreveu a posição do personagem no target
def check_wrote(config, pointer, new_x, new_y, target_x, target_y):
    time.sleep(0.5)
    if new_x == 0 or new_y == 0:
        print("Target not found")
        return
    else:
        if abs(new_x - target_x) >= 4 or abs(new_y - target_y) >= 4:
            print("Target not moved, moving again")
            print("New X: ", new_x, "New Y: ", new_y)
            print("Target X: ", target_x, "Target Y: ", target_y)
            charposX, charposY = char_base(config)
            _, _, target_x, target_y, pointer = search_monster(config)
            Pointers(config.pid).write_position(pointer, charposX, charposY)
            print("Target moved to new position: ", target_x, target_y)


# V1.6
def autopick(config):
    time.sleep(0.3)
    loot = Pointers(config.pid).is_loot()
    # print(f"Loot: ", loot)

    if loot > 0 and Pointers(config.pid).is_target_selected() and Pointers(config.pid).is_target_dead():
        # print(f"Loot Found: {loot} itens")
        _, _, target_x, target_y, pointer = search_monster(config)

        new_x = target_x
        new_y = target_y
        # print(f"Posição: X={new_x}, Y={new_y}")

        # Pega posição atual do personagem
        charposX, charposY = char_base(config)

        # Move o monstro atual para a posição do personagem
        Pointers(config.pid).write_position(pointer, charposX, charposY)
        time.sleep(0.5)
        Pointers(config.pid).write_position(pointer, charposX, charposY)
        time.sleep(0.5)
        Pointers(config.pid).write_position(pointer, charposX, charposY)

        # Pega o loot
        get_loot(config)


# V1.5
def mount_status(config, action):
    if action == "mount":
        if Pointers(config.pid).mount() == 0:
            print("Mounting...")
            send(config.hwnd, config.mount)
            time.sleep(5)

    if action == "dismount":
        print("Dismounting...")
        send(config.hwnd, config.mount)
        time.sleep(1)


def tab_santa(config):
    if config.kill_santa == "OFF":
        while True:
            if Pointers(config.pid).get_target_name() == "Santa Mushroom":
                send(config.hwnd, config.next_target)
            else:
                break


def debug_pet_ap(config):
    def inner():
        right(config.hwnd, cords_move["stop"][0] + 2, cords_move["stop"][1] + 2)
        time.sleep(1)
        right(config.hwnd, cords_move["stop"][0] - 2, cords_move["stop"][1] - 2)
        time.sleep(1)

    return inner


def fairy_attack_buff_up(config):
    def inner():
        send(config.hwnd, config.select_yourself), time.sleep(1)
        if Pointers(config.pid).get_target_name() != Pointers(config.pid).get_char_name():
            send(config.hwnd, config.select_yourself), time.sleep(1)
        send(config.hwnd, config.sun_needle), time.sleep(2)

    return inner


def fairy_attack_cure(config):
    if config.autopick == "ON" and config.follow_leader == "OFF":
        time.sleep(0.5)
        # print("Pegando loot antes da cura")
        autopick(config)

    low_hp = config.low_hp
    hp_p = hp_percentage(config)
    spell = 90

    if hp_p <= low_hp:
        print("HP is Bellow the Percentage", low_hp, hp_p)
        if Pointers(config.pid).is_in_battle():
            while not Pointers(config.pid).is_target_dead():
                kill(config)
            print("Waiting 2 seconds to leave battle")
            if Pointers(config.pid).is_target_selected() and Pointers(config.pid).is_target_dead():
                send(config.hwnd, "ESC")
            time.sleep(0.2)

        print("Healing Yourself")
        #send(config.hwnd, config.select_yourself), time.sleep(0.5)
        while Pointers(config.pid).get_hp() < Pointers(config.pid).get_max_hp() - 10:
            if Pointers(config.pid).get_target_name() != config.char_name:
                send(config.hwnd, config.select_yourself), time.sleep(0.5)
            send(config.hwnd, config.healing_spell)
            time.sleep(1)
            dead(config)
            # check_dc(config)
            time.sleep(1)

            if Pointers(config.pid).is_in_battle():
                print("Someone is hitting me!")
                time.sleep(0.2)
                send(config.hwnd, config.next_target)
                tab_santa(config)
                time.sleep(0.2)
                kill(config)
                if config.autopick == "ON" and config.follow_leader == "OFF":
                    time.sleep(0.5)
                    print("Pegando loot antes da cura")
                    autopick(config)
            dead(config)
            # print("Recovering HP")

    """MANA CURE SYSTEM"""
    low_mp = config.low_mp
    mp_p = mp_percentage(config)

    if mp_p <= low_mp:
        print("MP is Bellow the Percentage", low_mp, mp_p)
        if Pointers(config.pid).is_in_battle():
            while not Pointers(config.pid).is_target_dead():
                kill(config)
            print("Waiting 2 seconds to leave battle")
            time.sleep(0.2)

        if config.get_back == "ON" and Pointers(config.pid).get_team_size() >= 2:
            safe_spot_back(config, safe_spot)
            print("Safe Spot Back")

        print("Stting to recover MP")
        sit(config), time.sleep(2)
        send(config.hwnd, config.potion_mp)

        timer = QTimer()
        timer.setInterval(15000)
        timer.start()
        start_time = time.time()

        while Pointers(config.pid).get_mana() < Pointers(config.pid).get_max_mana() - 10:
            # check_dc(config)
            time.sleep(1)

            elapsed_time = time.time() - start_time
            if elapsed_time >= 15 and Pointers(config.pid).get_mana() < Pointers(config.pid).get_max_mana() - 10:
                send(config.hwnd, config.potion_mp)
                print("Timer expired: sent potion command")
                start_time = time.time()  # Reseta o contador de tempo

            if Pointers(config.pid).is_in_battle():
                print("Someone is hitting me!")
                kill(config)
                if config.autopick == "ON":
                    time.sleep(0.5)
                    print("Pegando loot antes da cura")
                    autopick(config)
            sit(config)
            # print("Recovering MP")

    if hp_p <= spell:
        send(config.hwnd, config.select_yourself), time.sleep(0.5)
        send(config.hwnd, config.cure_spell), time.sleep(0.5)


def fairy_heal_follow(config):
    if config.follow_leader == "ON":
        team_name_1 = Pointers(config.pid).team_name_1()
        #print(f"Following Team name 1{team_name_1}")

        if Pointers(config.pid).get_target_name() != team_name_1:
            kleft(config.hwnd, int(cords_team["member_1"][0]), int(cords_team["member_1"][1]))
            time.sleep(0.1)

        if not Pointers(config.pid).is_target_selected():
            kleft(config.hwnd, int(cords_team["member_1"][0]), int(cords_team["member_1"][1]))
            time.sleep(0.1)

        send(config.hwnd, config.follow)
        time.sleep(0.5)


def fairy_heal_cure(config):
    if config.autopick == "ON" and config.follow_leader == "OFF":
        time.sleep(0.5)
        # print("Pegando loot antes da cura")
        autopick(config)

    low_hp = config.low_hp
    hp_p = hp_percentage(config)

    def cure_member():
        if Pointers(config.pid).target_hp() <= target_hp_percentage(70):
            print("Using Healing Spell")
            while Pointers(config.pid).target_hp() < target_hp_percentage(90):
                send(config.hwnd, config.healing_spell)
                time.sleep(0.5)
                if not Pointers(config.pid).is_target_selected() or Pointers(config.pid).is_target_dead():
                    print("No target selected.")
                    send(config.hwnd, config.next_target)
            time.sleep(0.5)
            if config.follow_leader == "ON":
                if Pointers(config.pid).target_hp() <= target_hp_percentage(85):
                    print("Using Cure Spell")
                    send(config.hwnd, config.cure_spell)
                    time.sleep(1)

    def cure_yourself():
        if hp_p <= low_hp:
            while Pointers(config.pid).get_hp() < Pointers(config.pid).get_max_hp() - 10:
                send(config.hwnd, config.select_yourself), time.sleep(0.5)
                send(config.hwnd, config.healing_spell)
                time.sleep(0.5)

    def cure_spell():
        if Pointers(config.pid).get_team_size() > 1:
            kleft(config.hwnd, int(cords_team["member_1"][0]), int(cords_team["member_1"][1]))

            if Pointers(config.pid).target_hp() <= target_hp_percentage(85):
                time.sleep(0.1)
                send(config.hwnd, config.cure_spell)
                time.sleep(0.1)
                cure_yourself()
            time.sleep(0.5)
            cure_member()

        if Pointers(config.pid).get_team_size() > 2:
            kleft(config.hwnd, int(cords_team["member_2"][0]), int(cords_team["member_2"][1]))

            if Pointers(config.pid).target_hp() <= target_hp_percentage(85):
                time.sleep(0.1)
                send(config.hwnd, config.cure_spell)
                time.sleep(0.1)
                cure_yourself()
            time.sleep(0.5)
            cure_member()

        if Pointers(config.pid).get_team_size() > 3:
            kleft(config.hwnd, int(cords_team["member_3"][0]), int(cords_team["member_3"][1]))

            if Pointers(config.pid).target_hp() <= target_hp_percentage(85):
                time.sleep(0.1)
                send(config.hwnd, config.cure_spell)
                time.sleep(0.1)
                cure_yourself()
            time.sleep(0.5)
            cure_member()

        if Pointers(config.pid).get_team_size() > 4:
            kleft(config.hwnd, int(cords_team["member_4"][0]), int(cords_team["member_4"][1]))

            if Pointers(config.pid).target_hp() <= target_hp_percentage(85):
                time.sleep(0.1)
                send(config.hwnd, config.cure_spell)
                time.sleep(0.1)
                cure_yourself()
            time.sleep(0.5)
            cure_member()

    def cure_mana():
        low_mp = config.low_mp
        mp_p = mp_percentage(config)

        if mp_p <= low_mp:
            print("MP is Bellow the Percentage", low_mp, mp_p)
            if Pointers(config.pid).is_in_battle():
                while not Pointers(config.pid).is_target_dead():
                    kill(config)

            if Pointers(config.pid).is_target_selected() and Pointers(config.pid).is_target_dead():
                send(config.hwnd, "ESC")
            time.sleep(0.2)

            if config.get_back == "ON" and Pointers(config.pid).get_team_size() >= 2:
                safe_spot_back(config, safe_spot)
                print("Safe Spot Back")

            time.sleep(0.2)
            send(config.hwnd, config.potion_mp)
            dead(config)

            timer = QTimer()
            timer.setInterval(15000)
            timer.start()
            start_time = time.time()

            while Pointers(config.pid).get_mana() < Pointers(config.pid).get_max_mana() - 10:
                # check_dc(config)
                time.sleep(1)
                sit(config)

                elapsed_time = time.time() - start_time
                if elapsed_time >= 15 and Pointers(config.pid).get_mana() < Pointers(config.pid).get_max_mana() - 10:
                    send(config.hwnd, config.potion_mp)
                    print("Timer expired: sent potion command")
                    start_time = time.time()  # Reseta o contador de tempo

                if Pointers(config.pid).is_in_battle():
                    print("Someone is hitting me!")
                    return

                if Pointers(config.pid).is_target_selected() and Pointers(config.pid).is_target_dead():
                    send(config.hwnd, "ESC")
                time.sleep(0.2)

                sit(config)
                #print("Recovering MP")

    if config.follow_leader == "OFF":
        cure_spell()

    if config.follow_leader == "ON":
        if Pointers(config.pid).get_target_name() != Pointers(config.pid).team_name_1():
            left(config.hwnd, int(cords_team["member_1"][0]), int(cords_team["member_1"][1]))
            time.sleep(0.1)

        if not Pointers(config.pid).is_target_selected():
            left(config.hwnd, int(cords_team["member_1"][0]), int(cords_team["member_1"][1]))
            time.sleep(0.1)
        cure_member()
        cure_yourself()

    cure_mana()
    cure_yourself()


def fairy_heal_buff_up(config):
    def inner():
        send(config.hwnd, config.select_yourself), time.sleep(1)
        send(config.hwnd, config.sun_needle), time.sleep(2)
        if Pointers(config.pid).get_team_size() > 1:
            print("Buff Member 1")
            kleft(config.hwnd, int(cords_team["member_1"][0]), int(cords_team["member_1"][1]))
            send(config.hwnd, config.sun_needle), time.sleep(2)
        if Pointers(config.pid).get_team_size() > 2:
            print("Buff Member 2")
            kleft(config.hwnd, int(cords_team["member_2"][0]), int(cords_team["member_2"][1]))
            send(config.hwnd, config.sun_needle), time.sleep(2)
        if Pointers(config.pid).get_team_size() > 3:
            print("Buff Member 3")
            kleft(config.hwnd, int(cords_team["member_3"][0]), int(cords_team["member_3"][1]))
            send(config.hwnd, config.sun_needle), time.sleep(2)
        if Pointers(config.pid).get_team_size() > 4:
            print("Buff Member 4")
            kleft(config.hwnd, int(cords_team["member_4"][0]), int(cords_team["member_4"][1]))
            send(config.hwnd, config.sun_needle), time.sleep(2)

    return inner


def check_distance(config, xY):  # Adiciona um parâmetro de tolerância
    while True:
        get_x = Pointers(config.pid).get_x()
        get_y = Pointers(config.pid).get_y()
        # print(f"Posição inicial: {xY}, Posição atual: ({get_x}, {get_y})")

        # Calcula a distância do ponto inicial
        current_distance = math.sqrt((get_x - xY[0]) ** 2 + (get_y - xY[1]) ** 2)

        # Debug: Exibe a distância calculada e o limite
        # print(f"Distância atual: {current_distance:.2f} m, Limite: {config.distance} m")

        # Verifica se a distância ultrapassa o limite máximo
        if current_distance >= config.distance:  # Só reposiciona se for MAIOR
            # print(f"Distância {current_distance} excede o limite! Reposicionando...")
            if config.autopick == "ON":
                print("Pegando loot antes da reposição")
                autopick(config)
            safe_spot_back(config, xY)  # V1.5 removido voltar pelo mapa

        # Se a distância está dentro do limite, não faz nenhuma movimentação
        if current_distance <= config.distance:
            # print("Dentro do limite, sem movimentação.")
            time.sleep(0.1)
            return


def safe_spot_back(config, xY, tolerance=2):  # Adiciona um parâmetro de tolerância
    while True:
        # Atualiza continuamente a posição atual
        dead(config)

        get_x = Pointers(config.pid).get_x()
        get_y = Pointers(config.pid).get_y()
        time.sleep(0.1)
        # print(f"Primeiro {get_x} {get_y}")

        # Verifica se já está na posição correta com tolerância
        if abs(get_x - xY[0]) <= tolerance and abs(get_y - xY[1]) <= tolerance:
            #print("Chegou ao local seguro com tolerância!")
            break

        # Calcula a diferença entre a posição atual e o destino
        x, y = get_x, get_y
        via = [cords_move["stop"][0], cords_move["stop"][1]]
        repos = [x - xY[0], y - xY[1]]
        time.sleep(0.1)

        # Corrige a posição
        if repos[0] != 0 or repos[1] != 0:
            # Ajusta eixo X
            if repos[0] != 0:
                via[0] -= repos[0]
                time.sleep(0.1)
            # Ajusta eixo Y
            if repos[1] != 0:
                via[1] += repos[1]
                time.sleep(0.1)

            # Move o personagem
            right(config.hwnd, int(via[0]), int(via[1]))
            wait_while_moving(config)

    # Reseta o cursor após chegar no destino
    left(config.hwnd, int(cords_move["mouse_reset"][0]), int(cords_move["mouse_reset"][1]))
    time.sleep(0.1)


def wait_while_moving(config):
    countspot = 0
    prevX, prevY = None, None

    while True:
        # check_dc(config)
        x = Pointers(config.pid).get_x()
        y = Pointers(config.pid).get_y()
        # print(x, y)
        dead(config)
        if prevX == x and prevY == y:
            countspot += 1
            if countspot >= 4:
                time.sleep(0.1)
                break
        else:
            countspot = 0

        prevX, prevY = x, y
        time.sleep(0.2)


def buff_up(config):
    def inner():
        print("Using Buff")
        if config.char_type == "Stamina" or config.char_type == "Sin Lure/AOE":
            send(config.hwnd, config.buff_1), time.sleep(1)
            send(config.hwnd, config.buff_2), time.sleep(1)

        if config.char_type == "Mana":
            send(config.hwnd, config.select_yourself), time.sleep(1)
            send(config.hwnd, config.buff_1), time.sleep(1.5)
            send(config.hwnd, config.buff_2), time.sleep(1.5)

    return inner


def use_pet_food(config):
    def inner():
        time.sleep(1)
        print("Using Pet Food")
        send(config.hwnd, config.pet_food)
        send(config.hwnd, config.pet_food), time.sleep(0.2)

    return inner


def simitar_lure_kill(config):
    mobs = 0
    stickness = 0
    stuck_count = 0
    stuck = 30

    for _ in range(5):
        send(config.hwnd, "TAB")
        time.sleep(0.2)
        while Pointers(config.pid).target_hp() > 590:
            send(config.hwnd, config.simitar_lure), time.sleep(0.2)

            battle_cure(config)
            stamina_cure(config)
            dead(config)

            if stickness >= stuck:
                # print(f"Unstuck count: {stuck_count}:")
                if stuck_count == 3:
                    right(config.hwnd, cords_move["stop"][0] + 2, cords_move["stop"][1] + 2)
                    time.sleep(0.5)
                    right(config.hwnd, cords_move["stop"][0] - 2, cords_move["stop"][1] - 2)
                    time.sleep(0.5)
                    right(config.hwnd, cords_move["stop"][0] + 2, cords_move["stop"][1] - 2)
                    time.sleep(0.5)
                    right(config.hwnd, cords_move["stop"][0] - 2, cords_move["stop"][1] + 2)
                    time.sleep(0.5)
                    stuck_count = 0
                    send(config.hwnd, "TAB")
                else:
                    stuck_count = stuck_count + 1
                    send(config.hwnd, "TAB")
                    time.sleep(0.2)
                stickness = 0

            if Pointers(config.pid).target_hp_full() or not Pointers(config.pid).is_target_selected():
                # print(f"Sticness: {stickness}")
                # print(f"Stuck: {stuck}")
                stickness = stickness + 1

        mobs += 1
        # print(f"Lured mobs: {mobs}")
        stickness = 0

        if config.get_back == "ON":
            check_distance(config, safe_spot)

    while Pointers(config.pid).is_in_battle():
        send(config.hwnd, config.simitar_aoe), time.sleep(0.2)
        send(config.hwnd, config.simitar_lure), time.sleep(0.2)
        send(config.hwnd, config.simitar_stun), time.sleep(0.2)
        battle_cure(config)
        stamina_cure(config)
        dead(config)

    if config.lure_time >= 1:
        sit(config)
        time.sleep(config.lure_time)


def kill(config):
    stickness = 0
    stuck_count = 0
    stuck = 10

    if config.autopick == "ON":
        pointer = search_monster(config)

    while not Pointers(config.pid).is_target_dead():
        if Pointers(config.pid).target_hp() >= target_hp_percentage(45):
            send(config.hwnd, config.skill_1), time.sleep(0.2)
            send(config.hwnd, config.skill_2), time.sleep(0.2)
            send(config.hwnd, config.skill_3), time.sleep(0.2)
        else:
            send(config.hwnd, config.skill_4), time.sleep(0.2)
            send(config.hwnd, config.skill_5), time.sleep(0.2)
            send(config.hwnd, config.skill_6), time.sleep(0.2)

        if stickness >= stuck:
            print(f"Unstuck count: {stuck_count}:")
            if stuck_count == 3:
                # V1.5
                right(config.hwnd, cords_move["stop"][0] + 2, cords_move["stop"][1] + 2)
                time.sleep(0.5)
                right(config.hwnd, cords_move["stop"][0] - 2, cords_move["stop"][1] - 2)
                time.sleep(0.5)
                right(config.hwnd, cords_move["stop"][0] + 2, cords_move["stop"][1] - 2)
                time.sleep(0.5)
                right(config.hwnd, cords_move["stop"][0] - 2, cords_move["stop"][1] + 2)
                time.sleep(0.5)
                stuck_count = 0
                send(config.hwnd, config.next_target)
                tab_santa(config)
            else:
                stuck_count = stuck_count + 1
                send(config.hwnd, config.next_target)
                tab_santa(config)
                time.sleep(0.2)
            stickness = 0

        if Pointers(config.pid).target_hp_full() or not Pointers(config.pid).is_target_selected():
            # print(f"Sticness: {stickness}")
            # print(f"Stuck: {stuck}")
            stickness = stickness + 1

        if Pointers(config.pid).mount() != 0:
            send(config.hwnd, config.mount)
            time.sleep(1)  # V1.5

        dead(config)
        #check_distance(config, safe_spot)
        # check_dc(config)
        battle_cure(config)


def fairy_atk_heal_kill(config):  # ATUALIZAR IGUAL KILL
    stickness = 0
    stuck_count = 0
    stuck = 10

    if Pointers(config.pid).get_target_name() == Pointers(config.pid).get_char_name():
        send(config.hwnd, config.next_target)
        tab_santa(config)

    if Pointers(config.pid).get_team_size() > 1:
        while Pointers(config.pid).get_target_name() == Pointers(config.pid).team_name_1():
            send(config.hwnd, config.next_target)
            tab_santa(config)

    if Pointers(config.pid).get_team_size() > 2:
        while Pointers(config.pid).get_target_name() == Pointers(config.pid).team_name_2():
            send(config.hwnd, config.next_target)
            tab_santa(config)

    if Pointers(config.pid).get_team_size() > 3:
        while Pointers(config.pid).get_target_name() == Pointers(config.pid).team_name_3():
            send(config.hwnd, config.next_target)
            tab_santa(config)

    if Pointers(config.pid).get_team_size() > 4:
        while Pointers(config.pid).get_target_name() == Pointers(config.pid).team_name_4():
            send(config.hwnd, config.next_target)
            tab_santa(config)

    if config.autopick == "ON":
        pointer = search_monster(config)

    while not Pointers(config.pid).is_target_dead():

        if Pointers(config.pid).target_hp() >= target_hp_percentage(45):
            send(config.hwnd, config.skill_1), time.sleep(0.2)
            send(config.hwnd, config.skill_2), time.sleep(0.2)
            send(config.hwnd, config.skill_3), time.sleep(0.2)
        else:
            send(config.hwnd, config.skill_4), time.sleep(0.2)
            send(config.hwnd, config.skill_5), time.sleep(0.2)
            send(config.hwnd, config.skill_6), time.sleep(0.2)

        if stickness >= stuck:
            print(f"Unstuck count: {stuck_count}:")
            if stuck_count == 3:
                # V1.5
                right(config.hwnd, cords_move["stop"][0] + 2, cords_move["stop"][1] + 2)
                time.sleep(0.5)
                right(config.hwnd, cords_move["stop"][0] - 2, cords_move["stop"][1] - 2)
                time.sleep(0.5)
                right(config.hwnd, cords_move["stop"][0] + 2, cords_move["stop"][1] - 2)
                time.sleep(0.5)
                right(config.hwnd, cords_move["stop"][0] - 2, cords_move["stop"][1] + 2)
                time.sleep(0.5)
                stuck_count = 0
                send(config.hwnd, config.next_target)
                tab_santa(config)
            else:
                stuck_count = stuck_count + 1
                send(config.hwnd, config.next_target)
                tab_santa(config)
                time.sleep(0.2)
            stickness = 0

        if Pointers(config.pid).target_hp_full() or not Pointers(config.pid).is_target_selected():
            #print(f"Sticness: {stickness}")
            #print(f"Stuck: {stuck}")
            stickness = stickness + 1

        dead(config)
        battle_cure(config)
        #check_distance(config, safe_spot)
        # check_dc(config)


def check_dc(config):
    """
    Verifica se o server desconectou validando o estado do ponteiro por 5 segundos
    antes de encerrar o processo.
    """
    pointer = Pointers(config.pid)

    # Apenas verificar se inicialmente o ponteiro retorna 1
    if pointer.get_dc() == 1:
        consistent_dc = True

        for _ in range(20):  # Verifica por 20 segundos
            if pointer.get_dc() != 1:
                consistent_dc = False
                break
            time.sleep(1)  # Espera 1 segundo antes de verificar novamente

        if consistent_dc:  # Se foi consistente durante os 5 segundos
            print(f"Char {config.char_name} DC confirmado após validação.")
            g = Game()
            g.stop_events[config.char_name].set()
            g.stop_game(config.char_name)
        else:
            print(f"Falso positivo para {config.char_name}, processo não encerrado.")


def tab(config):
    # check_dc(config)
    if Pointers(config.pid).is_target_dead():
        send(config.hwnd, config.next_target)
        tab_santa(config)

    if not Pointers(config.pid).is_target_selected():
        send(config.hwnd, config.next_target)
        tab_santa(config)


def battle_cure(config):
    battle_low_hp = config.battle_low_hp
    hp_p = hp_percentage(config)

    battle_low_mp = config.battle_low_mp
    mp_p = mp_percentage(config)

    if hp_p <= battle_low_hp:
        # print("Using Battle Potion HP", battle_low_hp, hp_p)
        send(config.hwnd, config.battle_potion_hp)

    if mp_p <= battle_low_mp:
        # print("Using Battle Potion MP", battle_low_mp, mp_p)
        send(config.hwnd, config.battle_potion_mp)


def stamina_cure(config):
    if config.autopick == "ON":
        time.sleep(0.5)
        # print("Pegando loot antes da cura")
        autopick(config)

    low_hp = config.low_hp
    hp_p = hp_percentage(config)

    if hp_p <= low_hp:
        print("HP is Bellow the Percentage", low_hp, hp_p)
        if Pointers(config.pid).is_in_battle():
            while not Pointers(config.pid).is_target_dead():
                kill(config)
        if Pointers(config.pid).is_target_selected() and Pointers(config.pid).is_target_dead():
            send(config.hwnd, "ESC")
        time.sleep(0.2)

        if config.get_back == "ON" and Pointers(config.pid).get_team_size() >= 2:
            safe_spot_back(config, safe_spot)
            print("Safe Spot Back")

        send(config.hwnd, config.potion_hp)
        dead(config)

        timer = QTimer()
        timer.setInterval(15000)
        timer.start()
        start_time = time.time()

        while Pointers(config.pid).get_hp() < Pointers(config.pid).get_max_hp() - 10:
            # (config)
            sit(config)
            time.sleep(1)
            elapsed_time = time.time() - start_time
            if elapsed_time >= 15 and Pointers(config.pid).get_hp() < Pointers(config.pid).get_max_hp() - 10:
                send(config.hwnd, config.potion_hp)
                print("Timer expired: sent potion command")
                start_time = time.time()  # Reseta o contador de tempo
            if Pointers(config.pid).is_in_battle():
                print("Someone is hitting me!")
                if config.char_type == "Sin Lure/AOE":
                    send(config.hwnd, config.simitar_aoe), time.sleep(0.2)
                    send(config.hwnd, config.simitar_stun), time.sleep(0.2)
                kill(config)
                if config.autopick == "ON":
                    time.sleep(0.5)
                    print("Pegando loot antes da cura")
                    autopick(config)
            if Pointers(config.pid).is_target_selected() and Pointers(config.pid).is_target_dead():
                send(config.hwnd, "ESC")
            time.sleep(0.2)
            sit(config)
            dead(config)
            #print("Recovering HP")


def mana_cure(config):
    if config.autopick == "ON":
        time.sleep(0.5)
        print("Pegando loot antes da cura")
        autopick(config)

    low_hp = config.low_hp
    hp_p = hp_percentage(config)

    if hp_p <= low_hp:
        print("HP is Bellow the Percentage", low_hp, hp_p)
        if Pointers(config.pid).is_in_battle():
            while not Pointers(config.pid).is_target_dead():
                kill(config)

        if Pointers(config.pid).is_target_selected() and Pointers(config.pid).is_target_dead():
            send(config.hwnd, "ESC")
        time.sleep(0.2)

        if config.get_back == "ON" and Pointers(config.pid).get_team_size() >= 2:
            safe_spot_back(config, safe_spot)
            print("Safe Spot Back")

        time.sleep(0.2)
        send(config.hwnd, config.potion_hp)
        dead(config)

        timer = QTimer()
        timer.setInterval(15000)
        timer.start()
        start_time = time.time()

        while Pointers(config.pid).get_hp() < Pointers(config.pid).get_max_hp() - 10:
            # check_dc(config)
            time.sleep(1)
            sit(config)

            elapsed_time = time.time() - start_time
            if elapsed_time >= 15 and Pointers(config.pid).get_hp() < Pointers(config.pid).get_max_hp() - 10:
                send(config.hwnd, config.potion_hp)
                print("Timer expired: sent potion command")
                start_time = time.time()  # Reseta o contador de tempo
            if Pointers(config.pid).is_in_battle():
                print("Someone is hitting me!")
                kill(config)
                if config.autopick == "ON":
                    time.sleep(0.5)
                    print("Pegando loot antes da cura")
                    autopick(config)

            if Pointers(config.pid).is_target_selected() and Pointers(config.pid).is_target_dead():
                send(config.hwnd, "ESC")
            time.sleep(0.2)

            sit(config)
            dead(config)
            #print("Recovering HP")

    """MANA CURE SYSTEM"""
    low_mp = config.low_mp
    mp_p = mp_percentage(config)

    if mp_p <= low_mp:
        print("MP is Bellow the Percentage", low_mp, mp_p)
        if Pointers(config.pid).is_in_battle():
            while not Pointers(config.pid).is_target_dead():
                kill(config)

        if Pointers(config.pid).is_target_selected() and Pointers(config.pid).is_target_dead():
            send(config.hwnd, "ESC")
        time.sleep(0.2)

        if config.get_back == "ON" and Pointers(config.pid).get_team_size() >= 2:
            safe_spot_back(config, safe_spot)
            print("Safe Spot Back")

        time.sleep(0.2)
        send(config.hwnd, config.potion_mp)
        dead(config)

        timer = QTimer()
        timer.setInterval(15000)
        timer.start()
        start_time = time.time()

        while Pointers(config.pid).get_mana() < Pointers(config.pid).get_max_mana() - 10:
            # check_dc(config)
            time.sleep(1)
            sit(config)

            elapsed_time = time.time() - start_time
            if elapsed_time >= 15 and Pointers(config.pid).get_mana() < Pointers(config.pid).get_max_mana() - 10:
                send(config.hwnd, config.potion_mp)
                print("Timer expired: sent potion command")
                start_time = time.time()  # Reseta o contador de tempo

            if Pointers(config.pid).is_in_battle():
                print("Someone is hitting me!")
                kill(config)
                if config.autopick == "ON":
                    time.sleep(0.5)
                    print("Pegando loot antes da cura")
                    autopick(config)

            if Pointers(config.pid).is_target_selected() and Pointers(config.pid).is_target_dead():
                send(config.hwnd, "ESC")
            time.sleep(0.2)

            sit(config)
            #print("Recovering MP")


def hp_percentage(config):
    max_hp = Pointers(config.pid).get_max_hp()
    current_hp = Pointers(config.pid).get_hp()

    percentage = (current_hp / max_hp) * 100
    rounded_percentage = round(percentage, 2)
    return rounded_percentage


def mp_percentage(config):
    max_mp = Pointers(config.pid).get_max_mana()
    current_mp = Pointers(config.pid).get_mana()

    percentage = (current_mp / max_mp) * 100
    rounded_percentage = round(percentage, 2)
    return rounded_percentage


def target_hp_percentage(pct):
    hp_min = 460
    hp_max = 137
    return hp_min + hp_max * (pct / 100)


def sit(config):
    if not Pointers(config.pid).is_sitting():
        send(config.hwnd, config.sit), time.sleep(0.1)


def dead(config):
    if Pointers(config.pid).get_hp() == 0:

        if get_back_enable == 1:
            print("Setting Get Back OFF")
            config.get_back = "OFF"

        print(f"Char {Pointers(config.pid).get_char_name()} is dead!")
        time.sleep(3)
        """Click on jackstraw"""
        left(config.hwnd, int(cords_game["jackstraw_ok"][0]), int(cords_game["jackstraw_ok"][1]))
        time.sleep(2)
        """Click on OK Revive Normal"""
        if Pointers(config.pid).get_hp() == 0:
            left(config.hwnd, int(cords_game["revive_ok"][0]), int(cords_game["revive_ok"][1]))
            time.sleep(2)

        if config.revive_and_back == "ON":
            go_to_spot(config)


def go_to_spot(config):
    # V1.5
    mount_status(config, "mount")

    send(config.hwnd, config.map), time.sleep(1)

    if config.sell_items == "ON":
        city_map(config)

    coords = config.spot_farm.split(",")
    x = int(coords[0])
    y = int(coords[1])

    right(config.hwnd, x - 20, y - 20)
    time.sleep(0.2)
    right(config.hwnd, x + 20, y + 20)
    time.sleep(0.2)
    right(config.hwnd, x, y)
    time.sleep(1)
    send(config.hwnd, config.map), time.sleep(1)
    wait_until_farm_spot(config)


def wait_until_farm_spot(config):
    countspot = 0
    prevX, prevY = None, None

    while True:
        # check_dc(config)
        x = Pointers(config.pid).get_x()
        y = Pointers(config.pid).get_y()
        # print(x, y)
        dead(config)
        if prevX == x and prevY == y:
            countspot += 1
            if countspot >= 3:
                time.sleep(0.5)
                # V1.5 chegar no spot farm alterado para distancia
                check_return(config, safe_spot)
                print("Ready to start again !!!")
                mount_status(config, "dismount")

                if get_back_enable == 1 and config.get_back == "OFF":
                    print("Setting Get Back ON")
                    config.get_back = "ON"
                break
        else:
            countspot = 0

        prevX, prevY = x, y
        time.sleep(1)


def check_return(config, xY):
    get_x = Pointers(config.pid).get_x()
    get_y = Pointers(config.pid).get_y()

    current_distance = math.sqrt((get_x - xY[0]) ** 2 + (get_y - xY[1]) ** 2)

    if current_distance >= 80:
        print("Wrong Spot, trying again")
        go_to_spot(config)
    else:
        print("Near initial spot.")


def deleter(config):
    def inner():

        # Verifica se a mochila está aberta
        if not Pointers(config.pid).is_bag_open():
            print("Open bag")
            send(config.hwnd, config.inventory)
            time.sleep(0.5)
        else:
            print("Bag is open")
            time.sleep(0.5)

        def load_images(folder):
            """
            Carrega todas as imagens da pasta sem cache.
            """
            images = {}
            for filename in os.listdir(folder):
                full_path = os.path.join(folder, filename)
                image = cv2.imread(full_path, cv2.IMREAD_GRAYSCALE)
                if image is not None:
                    images[filename] = image
            return images

        def capture_window(hwnd):
            """
            Captura o conteúdo da janela especificada por hwnd, independentemente de sobreposições.
            """
            try:
                rect = win32gui.GetWindowRect(hwnd)
                width, height = rect[2] - rect[0], rect[3] - rect[1]

                hwnd_dc = win32gui.GetWindowDC(hwnd)
                mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
                save_dc = mfc_dc.CreateCompatibleDC()
                save_bitmap = win32ui.CreateBitmap()
                save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
                save_dc.SelectObject(save_bitmap)

                save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)

                bmp_info = save_bitmap.GetInfo()
                bmp_str = save_bitmap.GetBitmapBits(True)
                img = np.frombuffer(bmp_str, dtype=np.uint8)
                img.shape = (bmp_info['bmHeight'], bmp_info['bmWidth'], 4)

                save_dc.DeleteDC()
                mfc_dc.DeleteDC()
                win32gui.ReleaseDC(hwnd, hwnd_dc)
                win32gui.DeleteObject(save_bitmap.GetHandle())

                return img[..., :3]

            except Exception as e:
                print(f"Erro ao capturar a janela: {e}")
                raise

        def get_title_bar_height():
            """
            Obtém a altura da barra de título da janela usando a API do Windows.
            """
            SM_CYCAPTION = 4  # Constante para altura da barra de título
            return ctypes.windll.user32.GetSystemMetrics(SM_CYCAPTION)

        def find_image_in_window(target_image, hwnd):
            """
            Encontra uma imagem dentro da janela especificada pelo HWND,
            descontando a barra de título da janela.
            """
            title_bar_height = get_title_bar_height()

            # Capturar a imagem da janela
            window_img = capture_window(hwnd)
            window_gray = cv2.cvtColor(window_img, cv2.COLOR_BGR2GRAY)

            # Localizar a imagem na janela
            result = cv2.matchTemplate(window_gray, target_image, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            if max_val > 0.9:  # Ajuste o limiar conforme necessário
                adjusted_loc = (max_loc[0], max_loc[1] - title_bar_height)
                return adjusted_loc

            return None

        def find_items_in_window(item_images, hwnd):
            """
            Localiza itens em uma janela específica.
            """
            to_delete = []
            tolerance = 3  # Tolerância em pixels para coordenadas duplicadas

            window_img = capture_window(hwnd)
            window_gray = cv2.cvtColor(window_img, cv2.COLOR_BGR2GRAY)

            for offset in bag_offsets:
                x1, y1, width, height = offset

                bag_area = window_gray[y1:y1 + height, x1:x1 + width]

                for item_name, item_image in item_images.items():
                    result = cv2.matchTemplate(bag_area, item_image, cv2.TM_CCOEFF_NORMED)
                    threshold = 0.9
                    loc = np.where(result >= threshold)

                    for pt in zip(*loc[::-1]):
                        title_bar_height = get_title_bar_height()
                        global_x = x1 + pt[0]
                        global_y = y1 + pt[1] - title_bar_height

                        if not any(
                                abs(existing_x - global_x) <= tolerance and abs(existing_y - global_y) <= tolerance for
                                existing_x, existing_y in to_delete):
                            to_delete.append((global_x, global_y))

            return to_delete

        item_delete_path = "Images/DELETE"
        sell_item_path = "Images/SELL"

        if config.sell_items == "ON":
            item_images = load_images(sell_item_path)
        else:
            item_images = load_images(item_delete_path)

        destroy_path = "Images/misc/destroy-item.bmp"
        destroy_image = cv2.imread(destroy_path, cv2.IMREAD_GRAYSCALE)
        coordinates = find_image_in_window(destroy_image, config.hwnd)

        if coordinates:
            destroy_x, destroy_y = coordinates

            bag_cords = [
                (destroy_x - 5, destroy_y - 200, destroy_x + 220, destroy_y - 15),
                (destroy_x + 250, destroy_y - 420, destroy_x + 490, destroy_y - 10),
            ]

            bag_offsets = [
                (destroy_x - 5, destroy_y - 200, destroy_x + 220, destroy_y - 15),
                (destroy_x + 250, destroy_y - 420, destroy_x + 490, destroy_y - 10),
            ]

            bag_images = []
            for x1, y1, x2, y2 in bag_cords:
                bag_img = capture_window(config.hwnd)[y1:y2, x1:x2]
                bag_images.append(bag_img)

            to_delete = find_items_in_window(item_images, config.hwnd)

            """ok_button = config.deleter_ok.split(",")
            ok_buttonX = int(ok_button[0])
            ok_buttonY = int(ok_button[1])"""

            for item in to_delete:
                x, y = int(item[0]), int(item[1])

                left(config.hwnd, x, y)
                time.sleep(0.3)
                left(config.hwnd, destroy_x, destroy_y)
                time.sleep(0.3)
                left(config.hwnd, int(cords_game["deleter_ok"][0]), int(cords_game["deleter_ok"][1]))
                time.sleep(0.3)
        else:
            print("Destroy icon not found.")
        print("Close bag")
        send(config.hwnd, config.inventory)
        time.sleep(1)
        """if config.minimized_mode == "ON":
            hwnd = win32gui.FindWindow(None, config.char_name)
            if hwnd:
                placement = win32gui.GetWindowPlacement(hwnd)
                if not placement[1] == win32con.SW_SHOWMINIMIZED:  # SW_SHOWMINIMIZED é 2
                    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)  # Minimiza a janela"""

    return inner


def surrounds(config, action):
    if action == "open":
        x, y = map(int, config.surrounds_coords.split(','))
        click = [x, y]
        left(config.hwnd, click[0], click[1])
        time.sleep(0.5)

    if action == "close":
        x, y = map(int, config.surr_close_coords.split(','))
        click = [x, y]
        left(config.hwnd, click[0], click[1])
        time.sleep(0.5)


def check_pos(config, xY):
    get_x = Pointers(config.pid).get_x()
    get_y = Pointers(config.pid).get_y()

    x, y = map(int, xY.split(','))

    spot = [x, y]

    distance = math.sqrt((get_x - spot[0]) ** 2 + (get_y - spot[1]) ** 2)

    return distance


def go_to_npc(config, npc_name):
    # abrindo surrounds e indo ao npc de venda
    surrounds(config, "open")
    time.sleep(1)

    x, y = map(int, config.surr_input_coords.split(','))
    click = [x, y]
    left(config.hwnd, click[0], click[1])
    time.sleep(0.5)

    write(config.hwnd, npc_name)
    time.sleep(1)

    x, y = map(int, config.first_link_coords.split(','))
    click = [x, y]
    left(config.hwnd, click[0], click[1])
    time.sleep(1)

    surrounds(config, "close")
    time.sleep(1)

    wait_pos(config)
    check_pos(config, config.npc_coords)

    npc_distance = check_pos(config, config.npc_coords)
    if npc_distance >= 4:
        print("Char is far from npc")
        return go_to_npc(config, config.npc_name)
    else:
        print(" Char is near npc")


def reset_view(config):
    # print("Resetting view")
    left(config.hwnd, int(cords_game["reset_view"][0]), int(cords_game["reset_view"][1]))
    time.sleep(1)


def talk_npc(config, npc):
    print("Talking to npc")
    reset_view(config)

    x, y = map(int, npc.split(','))
    npc = [x, y]

    press(config.hwnd, config.hide_players)

    for offset in range(20, 60, 20):
        right(config.hwnd, npc[0] + offset, npc[1])
        time.sleep(0.1)
        right(config.hwnd, npc[0] - offset, npc[1])
        time.sleep(0.1)
        right(config.hwnd, npc[0], npc[1] + offset)
        time.sleep(0.1)
        right(config.hwnd, npc[0], npc[1] - offset)
        time.sleep(0.1)

    if config.autopick == "OFF":
        release(config.hwnd, config.hide_players)


def sell_item_to_npc(config):
    print("Selling items to npc")

    x, y = map(int, config.sell_item_coords.split(','))
    sell = [x, y]

    left(config.hwnd, sell[0], sell[1])
    time.sleep(1)

    x, y = map(int, config.initial_slot.split(','))
    initial_slot = [x, y]

    for _ in range(25):
        left(config.hwnd, initial_slot[0], initial_slot[1])
        time.sleep(0.1)

    x, y = map(int, config.sell_button_coords.split(','))
    click = [x, y]
    left(config.hwnd, click[0], click[1])

    time.sleep(1)


def city_map(config):
    left(config.hwnd, int(cords_game["world_map"][0]), int(cords_game["world_map"][1]))
    time.sleep(2)

    x, y = map(int, config.city_coords.split(','))
    city = [x, y]
    left(config.hwnd, city[0], city[1])
    time.sleep(1)


def sell_items(config):
    maxitemonbag = config.max_items
    bag_1 = Pointers(config.pid).bag_1_quantity()
    bag_2 = Pointers(config.pid).bag_2_quantity()

    # print(f"Bag 1: {bag_1}")
    # print(f"Bag 2: {bag_2}")

    if bag_1 + bag_2 >= maxitemonbag:
        print("Going to sell items")

        time.sleep(1)

        if config.use_teleport == "ON":
            print("Using teleport")
            send(config.hwnd, config.teleport), time.sleep(15)

        if config.use_mount == "ON":
            print("Using mount")
            send(config.hwnd, config.mount), time.sleep(5)

        go_to_npc(config, config.npc_name)

        # primeira venda
        talk_npc(config, config.sell_npc_coords)
        sell_item_to_npc(config)
        time.sleep(1)

        if config.max_items >= 20:
            # segunda venda
            talk_npc(config, config.sell_npc_coords)
            sell_item_to_npc(config)

        if config.max_items >= 50:
            # terceira venda
            talk_npc(config, config.sell_npc_coords)
            sell_item_to_npc(config)

        go_to_spot(config)


def minimap_minimize(config):
    for _ in range(5):
        left(config.hwnd, int(cords_move["minimize"][0]), int(cords_move["minimize"][1]))
        time.sleep(0.1)


class GameConfig:
    """Classe que encapsula as configurações e valores necessários para o jogo."""

    def __init__(self, resolution, char_name, hwnd, get_back, debug_ap, distance, inventory, char_type, pid, pet_food,
                 pet_food_delay, buff_1,
                 buff_2, skill_1, skill_2, potion_hp, potion_mp, battle_potion_hp, battle_potion_mp,
                 skill_3, skill_4, skill_5, skill_6, sit, select_yourself, low_hp, low_mp, battle_low_hp, battle_low_mp,
                 spot_farm, buff_delay, deleter_bot, deleter_delay, map,
                 follow, follow_leader, healing_spell, cure_spell, sun_needle, revive_and_back,
                 autopick, kill_santa, next_target, hide_players, mount, simitar_lure, simitar_aoe, simitar_stun,
                 lure_time,
                 npc_name, npc_coords, use_teleport, teleport, use_mount, max_items, initial_slot, sell_items,
                 sell_item_coords, sell_npc_coords, city_coords, surrounds_coords, surr_input_coords, surr_close_coords,
                 first_link_coords, sell_button_coords, teleport_guild, teleport_stone, member_reseter, member_farmer,
                 return_every,
                 buy_charm, use_guild, standart_route, safe_route, bc_stamina, bc_mana, bc_fairy, use_aoe,
                 use_aoe_until,
                 stamina_combo, combo, bc_atk_1, bc_atk_2, bc_atk_3, bc_atk_aoe, bc_atk_combo, atk_delay, bc_mount, bc_mount_speed,
                 bc_pet_food, bc_pot_hp, bc_pot_mp, bc_pot_hp_battle, bc_pot_mp_battle, bc_sit, bc_wizz_super,
                 bc_healing_spell,
                 bc_low_hp, bc_low_mp, bc_battle_low_hp, bc_battle_low_mp, friend_list, treasure_box, manual_pick, break_soul):
        self.hwnd = hwnd
        self.char_name = char_name
        self.resolution = resolution
        self.inventory = inventory
        self.char_type = char_type
        self.pid = pid
        self.spot_farm = spot_farm
        self.deleter_bot = deleter_bot
        self.deleter_delay = deleter_delay
        self.map = map
        self.pet_food = pet_food
        self.pet_food_delay = pet_food_delay
        self.buff_1 = buff_1
        self.buff_2 = buff_2
        self.skill_1 = skill_1
        self.skill_2 = skill_2
        self.skill_3 = skill_3
        self.skill_4 = skill_4
        self.skill_5 = skill_5
        self.skill_6 = skill_6
        self.potion_hp = potion_hp
        self.potion_mp = potion_mp
        self.battle_potion_hp = battle_potion_hp
        self.battle_potion_mp = battle_potion_mp
        self.sit = sit
        self.buff_delay = buff_delay
        self.select_yourself = select_yourself
        self.low_hp = low_hp
        self.low_mp = low_mp
        self.battle_low_hp = battle_low_hp
        self.battle_low_mp = battle_low_mp
        self.follow = follow
        self.follow_leader = follow_leader
        self.get_back = get_back
        self.distance = distance
        self.healing_spell = healing_spell
        self.cure_spell = cure_spell
        self.sun_needle = sun_needle
        self.revive_and_back = revive_and_back
        self.debug_ap = debug_ap
        self.kill_santa = kill_santa
        self.autopick = autopick
        self.next_target = next_target
        self.hide_players = hide_players
        self.mount = mount
        self.simitar_lure = simitar_lure
        self.simitar_aoe = simitar_aoe
        self.lure_time = lure_time
        self.simitar_stun = simitar_stun
        self.npc_name = npc_name
        self.npc_coords = npc_coords
        self.use_teleport = use_teleport
        self.teleport = teleport
        self.use_mount = use_mount
        self.max_items = max_items
        self.initial_slot = initial_slot
        self.sell_items = sell_items
        self.sell_item_coords = sell_item_coords
        self.sell_npc_coords = sell_npc_coords
        self.city_coords = city_coords
        self.surrounds_coords = surrounds_coords
        self.surr_input_coords = surr_input_coords
        self.surr_close_coords = surr_close_coords
        self.first_link_coords = first_link_coords
        self.sell_button_coords = sell_button_coords
        self.teleport_guild = teleport_guild
        self.teleport_stone = teleport_stone
        # self.member_name = member_name
        self.member_reseter = member_reseter
        self.member_farmer = member_farmer
        self.return_every = return_every
        self.buy_charm = buy_charm
        self.use_guild = use_guild
        self.standart_route = standart_route
        self.safe_route = safe_route
        self.bc_stamina = bc_stamina
        self.bc_mana = bc_mana
        self.bc_fairy = bc_fairy
        self.use_aoe = use_aoe
        self.use_aoe_until = use_aoe_until
        self.stamina_combo = stamina_combo
        self.combo = combo
        self.bc_atk_1 = bc_atk_1
        self.bc_atk_2 = bc_atk_2
        self.bc_atk_3 = bc_atk_3
        self.bc_atk_aoe = bc_atk_aoe
        self.bc_atk_combo = bc_atk_combo
        self.break_soul = break_soul
        self.atk_delay = atk_delay
        self.bc_mount = bc_mount
        self.bc_mount_speed = bc_mount_speed
        self.bc_pet_food = bc_pet_food
        self.bc_pot_hp = bc_pot_hp
        self.bc_pot_mp = bc_pot_mp
        self.bc_pot_hp_battle = bc_pot_hp_battle
        self.bc_pot_mp_battle = bc_pot_mp_battle
        self.bc_sit = bc_sit
        self.bc_wizz_super = bc_wizz_super
        self.bc_healing_spell = bc_healing_spell
        self.bc_low_hp = bc_low_hp
        self.bc_low_mp = bc_low_mp
        self.bc_battle_low_hp = bc_battle_low_hp
        self.bc_battle_low_mp = bc_battle_low_mp
        self.friend_list = friend_list
        self.treasure_box = treasure_box
        self.manual_pick = manual_pick

    def __repr__(self):
        return (
            f"GameConfig(resolution={self.resolution}, "
            f"hwnd={self.hwnd},char_name={self.char_name}, inventory={self.inventory}, char_type={self.char_type}, pid={self.pid}, pet_food={self.pet_food}, buff_1={self.buff_1}, buff_2={self.buff_2}"
            f"skill_1={self.skill_1}, skill_2={self.skill_2}, skill_3={self.skill_3}, skill_4={self.skill_4}, "
            f"skill_5={self.skill_5}, skill_6={self.skill_6}, sit={self.sit}, select_yourself={self.select_yourself}, "
            f"low_hp={self.low_hp}, low_mp={self.low_mp}, battle_low_hp={self.battle_low_hp}, battle_low_mp={self.battle_low_mp} spot_farm={self.spot_farm}, battle_potion_hp={self.battle_potion_hp}, battle_potion_mp={self.battle_potion_mp}, "
            f"deleter_delay={self.deleter_delay}, deleter_bot={self.deleter_bot}, map={self.map}, buff_delay={self.buff_delay},"
            f"pet_food_delay={self.pet_food_delay}, cords={self.cords}, "
            f"get_back={self.get_back}, distance={self.distance}, follow={self.follow}, healing_spell={self.healing_spell}, "
            f"cure_spell={self.cure_spell}, sun_needle={self.sun_needle}, follow_leader={self.follow_leader}, revive_and_back={self.revive_and_back},"
            f"potion_hp={self.potion_hp}, potion_mp={self.potion_mp}, debug_ap={self.debug_ap},"
            f"autopick={self.autopick}, kill_santa={self.kill_santa}, next_target={self.next_target}, mount={self.mount}, hide_players={self.hide_players},"
            f"simitar_lure={self.simitar_lure}, simitar_aoe={self.simitar_aoe}, lure_time={self.lure_time}, simitar_stun={self.simitar_stun},"
            f"npc_name={self.npc_name}, npc_coords={self.npc_coords}, use_teleport={self.use_teleport}, teleport={self.teleport},"
            f"use_mount={self.use_mount}, max_items={self.max_items}, initial_slot={self.initial_slot},"
            f"sell_items={self.sell_items}, sell_item_coords={self.sell_item_coords}, sell_npc_coords={self.sell_npc_coords},"
            f"city_coords={self.city_coords}, surrounds_coords={self.surrounds_coords}, "
            f"surr_input_coords={self.surr_input_coords}, surr_close_coords={self.surr_close_coords}, "
            f"first_link_coords={self.first_link_coords}, sell_button_coords={self.sell_button_coords},"
            f"teleport_guild={self.teleport_guild}, teleport_stone={self.teleport_stone},"
            f"member_reseter={self.member_reseter}, member_farmer={self.member_farmer}, return_every={self.return_every}, buy_charm={self.buy_charm}, use_guild={self.use_guild}"
            f"standart_route={self.standart_route}, safe_route={self.safe_route}, bc_stamina={self.bc_stamina}, bc_mana={self.bc_mana}"
            f"bc_fairy={self.bc_fairy}, use_aoe={self.use_aoe}, use_aoe_until={self.use_aoe_until}, stamina_combo={self.stamina_combo},"
            f"combo={self.combo}, atk_delay={self.atk_delay}, bc_atk_1={self.bc_atk_1}, bc_atk_2={self.bc_atk_2}, bc_atk_3={self.bc_atk_3}, bc_atk_aoe={self.bc_atk_aoe},"
            f"bc_atk_combo={self.bc_atk_combo}, bc_mount={self.bc_mount}, bc_mount_speed={self.bc_mount_speed}, bc_pet_food={self.bc_pet_food},"
            f"bc_pot_hp={self.bc_pot_hp}, bc_pot_mp={self.bc_pot_mp}, bc_pot_hp_battle={self.bc_pot_hp_battle}, bc_pot_mp_battle={self.bc_pot_mp_battle}, "
            f"bc_sit={self.bc_sit},bc_wizz_super={self.bc_wizz_super}, bc_healing_spell={self.bc_healing_spell}, bc_low_hp={self.bc_low_hp},"
            f"bc_low_mp={self.bc_low_mp}, bc_battle_low_hp={self.bc_battle_low_hp}, bc_battle_low_mp={self.bc_battle_low_mp}, friend_list={self.friend_list}, "
            f"treasure_box={self.treasure_box}, manual_pick={self.manual_pick}, break_soul={self.break_soul}")


class Game:
    def __init__(self):
        self.settings = {}
        self.keys = {}
        self.processes = {}
        self.stop_events = {}

    def set_settings(self, target):
        """Carrega as configurações do arquivo JSON do personagem."""
        file_name = f"characters/{target}.json"
        with open(file_name, "r") as json_file:
            self.settings[target] = json.load(json_file)

    def get_keys(self):
        """Carrega os atalhos de teclas do arquivo JSON."""
        with open("characters/keys.json", "r") as json_file:
            self.keys = json.load(json_file)

    def load_game(self, target):
        """Carrega os dados do personagem e inicializa o processo de jogo."""
        if target in self.processes and self.processes[target]:  # Verifica se já existe um processo ativo
            # Exibe uma QMessageBox perguntando se deseja reiniciar
            app = QApplication.instance() or QApplication([])  # Usa a instância existente ou cria uma nova
            reply = QMessageBox.question(
                None,
                "Processo em execução",
                f"Char {target} already running. Do you want to restart it?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                print(f"Processo para {target} mantido em execução.")
                return
            else:
                print(f"Reiniciando o processo para {target}...")
                self.stop_game(target)

        print(f"Carregando o jogo para o personagem {target}...")
        self.get_keys()
        self.set_settings(target)

        config = GameConfig(
            hwnd=self.settings[target]["HWND"],
            char_name=self.settings[target]["CHAR_NAME"],
            resolution=self.settings[target]["RESOLUTION"],
            inventory=self.keys["INVENTORY"],
            friend_list=self.keys["FRIENDS"],
            char_type=self.settings[target]["CHAR_TYPE"],
            pid=self.settings[target]["PID"],
            spot_farm=self.settings[target]["SPOT_FARM"],
            deleter_bot=self.settings[target]["DELETER_BOT"],
            deleter_delay=self.settings[target]["DELETER_DELAY"],
            low_hp=self.settings[target]["LOW_HP"],
            low_mp=self.settings[target]["LOW_MP"],
            battle_low_hp=self.settings[target]["BATTLE_LOW_HP"],
            battle_low_mp=self.settings[target]["BATTLE_LOW_MP"],
            pet_food=self.keys["PET_FOOD"],
            pet_food_delay=self.settings[target]["PET_FOOD_DELAY"],
            buff_1=self.keys["BUFF_1"],
            buff_2=self.keys["BUFF_2"],
            skill_1=self.keys["SKILL_1"],
            skill_2=self.keys["SKILL_2"],
            skill_3=self.keys["SKILL_3"],
            skill_4=self.keys["SKILL_4"],
            skill_5=self.keys["SKILL_5"],
            skill_6=self.keys["SKILL_6"],
            potion_hp=self.keys["POTION_HP"],
            potion_mp=self.keys["POTION_MP"],
            battle_potion_hp=self.keys["BATTLE_POTION_HP"],
            battle_potion_mp=self.keys["BATTLE_POTION_MP"],
            sit=self.keys["SIT"],
            select_yourself=self.keys["SELECT_YOURSELF"],
            buff_delay=self.settings[target]["BUFF_DELAY"],
            map=self.keys["MAP"],
            get_back=self.settings[target]["GET_BACK"],
            distance=self.settings[target]["DISTANCE"],
            follow=self.keys["FOLLOW"],
            follow_leader=self.settings[target]["FOLLOW_LEADER"],
            healing_spell=self.keys["HEALING_SPELL"],
            cure_spell=self.keys["CURE_SPELL"],
            sun_needle=self.keys["SUN_NEEDLE"],
            revive_and_back=self.settings[target]["REVIVE_AND_BACK"],
            debug_ap=self.settings[target]["DEBUG_AP"],
            autopick=self.settings[target]["AUTO_PICK"],
            kill_santa=self.settings[target]["KILL_SANTA"],
            next_target=self.keys["NEXT_TARGET"],
            hide_players=self.keys["HIDE_PLAYERS"],
            mount=self.keys["MOUNT"],
            simitar_lure=self.keys["SIN_LURE"],
            simitar_aoe=self.keys["SIN_AOE"],
            simitar_stun=self.keys["SIN_STUN"],
            lure_time=self.settings[target]["LURE_TIME"],
            npc_name=self.settings[target]['NPC_NAME'],
            npc_coords=self.settings[target]['NPC_COORDS'],
            use_teleport=self.settings[target]['USE_TELEPORT'],
            teleport=self.settings[target]['TELEPORT'],
            use_mount=self.settings[target]['USE_MOUNT'],
            max_items=self.settings[target]['MAX_ITEMS'],
            initial_slot=self.settings[target]['INITIAL_SLOT'],
            sell_items=self.settings[target]['SELL_ITEMS'],
            sell_item_coords=self.settings[target]['SELL_ITEM_COORDS'],
            sell_npc_coords=self.settings[target]['SELL_NPC_COORDS'],
            city_coords=self.settings[target]['CITY_COORDS'],
            surrounds_coords=self.settings[target]['SURROUNDS_COORDS'],
            surr_input_coords=self.settings[target]['SURR_INPUT_COORDS'],
            surr_close_coords=self.settings[target]['SURR_CLOSE_COORDS'],
            first_link_coords=self.settings[target]['FIRST_LINK_COORDS'],
            sell_button_coords=self.settings[target]['SELL_BUTTON_COORDS'],
            teleport_guild=self.settings[target]['TELEPORT_GUILD'],
            teleport_stone=self.settings[target]['TELEPORT_STONE'],
            # member_name=self.settings[target]['MEMBER_NAME'],
            member_reseter=self.settings[target]['MEMBER_RESETER'],
            member_farmer=self.settings[target]['MEMBER_FARMER'],
            return_every=self.settings[target]['RETURN_EVERY'],
            buy_charm=self.settings[target]['BUY_CHARM'],
            use_guild=self.settings[target]['USE_GUILD'],
            standart_route=self.settings[target]['STANDART_ROUTE'],
            safe_route=self.settings[target]['SAFE_ROUTE'],
            bc_stamina=self.settings[target]['BC_STAMINA'],
            bc_mana=self.settings[target]['BC_MANA'],
            bc_fairy=self.settings[target]['BC_FAIRY'],
            use_aoe=self.settings[target]['USE_AOE'],
            use_aoe_until=self.settings[target]['USE_AOE_UNTIL'],
            stamina_combo=self.settings[target]['STAMINA_COMBO'],
            combo=self.settings[target]['COMBO'],
            bc_atk_1=self.settings[target]['BC_ATK_1'],
            bc_atk_2=self.settings[target]['BC_ATK_2'],
            bc_atk_3=self.settings[target]['BC_ATK_3'],
            bc_atk_aoe=self.settings[target]['BC_ATK_AOE'],
            bc_atk_combo=self.settings[target]['BC_ATK_COMBO'],
            break_soul=self.settings[target]['BREAK_SOUL'],
            atk_delay=self.settings[target]['ATK_DELAY'],
            bc_mount=self.settings[target]['BC_MOUNT'],
            bc_mount_speed=self.settings[target]['BC_MOUNT_SPEED'],
            bc_pet_food=self.settings[target]['BC_PET_FOOD'],
            bc_pot_hp=self.settings[target]['BC_POT_HP'],
            bc_pot_mp=self.settings[target]['BC_POT_MP'],
            bc_pot_hp_battle=self.settings[target]['BC_POT_HP_BATTLE'],
            bc_pot_mp_battle=self.settings[target]['BC_POT_MP_BATTLE'],
            bc_sit=self.settings[target]['BC_SIT'],
            bc_wizz_super=self.settings[target]['BC_WIZZ_SUPER'],
            bc_healing_spell=self.settings[target]['BC_HEALING_SPELL'],
            bc_low_hp=self.settings[target]['BC_LOW_HP'],
            bc_low_mp=self.settings[target]['BC_LOW_MP'],
            bc_battle_low_hp=self.settings[target]['BC_BATTLE_LOW_HP'],
            bc_battle_low_mp=self.settings[target]['BC_BATTLE_LOW_MP'],
            treasure_box=self.settings[target]['PICK_BOX'],
            manual_pick=self.settings[target]['MANUAL_PICK']
        )

        # Criação do evento de parada
        stop_event = multiprocessing.Event()

        # Criação do processo, passando o objeto `GameConfig` e a flag de controle
        game_process = multiprocessing.Process(target=start_game_process, args=(config, stop_event))
        game_process.daemon = True  # O processo será encerrado quando o programa principal terminar
        game_process.start()

        # Armazenar o processo e o evento com base no target e pid
        if target not in self.processes:
            self.processes[target] = {}
            self.stop_events[target] = {}

        self.processes[target][game_process.pid] = game_process
        self.stop_events[target][game_process.pid] = stop_event

        # print(f"Processo iniciado para {target} (PID: {game_process.pid}).")
        # print(f"Processos: {self.processes}")

    def stop_game(self, target, pid=None):
        """Para o processo de jogo associado ao personagem e PID."""
        if target in self.processes:
            if pid is None:
                # print(f"Parando todos os processos para {target}...")
                # Para todos os processos associados ao target
                for pid, process in self.processes[target].items():
                    self._terminate_process(target, pid, process)
                del self.processes[target]
                del self.stop_events[target]
            elif pid in self.processes[target]:
                # print(f"Parando o processo {pid} para {target}...")
                # Para um processo específico pelo PID
                self._terminate_process(target, pid, self.processes[target][pid])
                del self.processes[target][pid]
                del self.stop_events[target][pid]
                if not self.processes[target]:  # Remove o target se não houver processos restantes
                    del self.processes[target]
                    del self.stop_events[target]
            else:
                print(f"PID {pid} não encontrado para o personagem {target}.")
        else:
            print(f"Personagem {target} não encontrado ou processo já encerrado.")

    def _terminate_process(self, target, pid, process):
        """Auxiliar para encerrar um processo."""
        self.stop_events[target][pid].set()
        process.terminate()  # Termina o processo
        process.join()  # Espera o processo terminar
        print(f"Processo {pid} para {target} encerrado.")


class CycleManager:
    def __init__(self):

        self.cycles = []

    def add_cycle(self, action: Callable, interval_minutes: float, name: str):
        interval_seconds = interval_minutes * 60  # Converte minutos para segundos
        self.cycles.append({
            "action": action,
            "interval": interval_seconds,
            "next_execution": time.time(),  # Executa imediatamente no início
            "name": name
        })

    def execute_cycles(self):
        current_time = time.time()
        for cycle in self.cycles:
            if current_time >= cycle["next_execution"]:
                print(f"Executando ciclo: {cycle['name']}...")
                try:
                    cycle["action"]()  # Executa a função associada ao ciclo
                except Exception as e:
                    print(f"Erro ao executar o ciclo '{cycle['name']}': {e}")
                cycle["next_execution"] = current_time + cycle["interval"]  # Atualiza o próximo tempo de execução


if __name__ == "__main__":
    print("Módulo Game carregado.")
