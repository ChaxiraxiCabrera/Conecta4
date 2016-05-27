from utils import *

# state -> ['__cmp__', '__doc__', '__init__', '__module__', '__repr__', 'board', 'moves', 'to_move', 'utility']
# max (1..7, 1..6) (columna, fila)


def memoize(f):
    memo = {}

    def helper(state):
        key = tuple(state.board.items())
        if key not in memo:
            memo[key] = f(state)
        return memo[key]

    return helper


def legal_moves(state):
    "Legal moves are any square not yet taken."
    return [(x, y) for (x, y) in state.moves
            if y == 1 or (x, y - 1) in state.board]


def calculate_weights(state, pos):
    # Con los pesos favorecemos jugar abajo y en el centro del tablero
    weights_c = [4, 8, 16, 32, 16, 8, 4]
    weights_f = [32, 16, 8, 4, 2, 1]
    # Es un hueco
    if pos in state.moves:
        result = weights_c[pos[0] - 1] * weights_f[pos[1] - 1] / 2
    # Es una ficha
    else:
        result = weights_c[pos[0] - 1] * weights_f[pos[1] - 1]
    return result


def calculate_delta(move, op, (delta_x, delta_y)):
    if op == '+':
        pos = (move[0] + delta_x, move[1] + delta_y)
    else:
        pos = (move[0] - delta_x, move[1] - delta_y)
    return pos


def k_in_row(state, player, op, (delta_x, delta_y)):
    board = state.board
    htotal = 0
    for move in legal_moves(state):
        pos = calculate_delta(move, op, (delta_x, delta_y))
        h = 0
        good = 0
        # Mientras sea una posicion legal calculamos su valor para un maximo de 3 desplazamientos
        while (pos in state.moves or board.get(pos) == player) and good < 3:
            # Si la posicion nos pertenece
            if board.get(pos) == player:
                h += calculate_weights(state, pos)
            # Si la posicion es un hueco
            elif pos in state.moves:
                h += calculate_weights(state, pos)
            # Actualizamos las posiciones
            pos = calculate_delta(move, op, (delta_x, delta_y))
            good += 1
        # Si es un potencial 4 en raya sumamos su valor heuristico
        if good == 3:
            htotal += h
    return htotal


# Calcula segun el jugador usando k_in_row
def compute_utility(state, player):
        pk = 0
        pk += k_in_row(state, player, '+', (0, 1))
        pk += k_in_row(state, player, '+', (1, 0))
        pk += k_in_row(state, player, '+', (1, -1))
        pk += k_in_row(state, player, '+', (-1, 1))
        pk += k_in_row(state, player, '-', (0, 1))
        pk += k_in_row(state, player, '-', (1, 0))
        pk += k_in_row(state, player, '-', (1, -1))
        pk += k_in_row(state, player, '-', (-1, 1))
        if player == 'X':
            contrincante = 'O'
        else:
            contrincante = 'X'
        pk -= k_in_row(state, contrincante, '+', (0, 1))
        pk -= k_in_row(state, contrincante, '+', (1, 0))
        pk -= k_in_row(state, contrincante, '+', (1, -1))
        pk -= k_in_row(state, contrincante, '+', (-1, 1))
        pk -= k_in_row(state, contrincante, '-', (0, 1))
        pk -= k_in_row(state, contrincante, '-', (1, 0))
        pk -= k_in_row(state, contrincante, '-', (1, -1))
        pk -= k_in_row(state, contrincante, '-', (-1, 1))
        return pk


@memoize
# FACIL: Retorna siempre 0
def h_0(state):
    if state.utility != 0:
        return state.utility * infinity
    else:
        return 0


@memoize
# MEDIO: Retorna valor aleatorio entre -100 y 100
def h_1(state):
    if state.utility != 0:
        return state.utility * infinity
    else:
        return random.randint(-100, 100)


@memoize
# DIFICIL: Cada posicion tiene un peso y buscamos potenciales 4 en raya
def h_2(state):
    if state.utility != 0:
        return state.utility * infinity
    else:
        # Calcula el valor heuristico para el jugador
        h = compute_utility(state, 'X')
        return h