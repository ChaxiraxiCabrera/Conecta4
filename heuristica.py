from utils import *

# state -> ['__cmp__', '__doc__', '__init__', '__module__', '__repr__', 'board', 'moves', 'to_move', 'utility']
# max (1..7, 1..6) (columna, fila)


def memoize(f):
    memo = {}
    def helper(x):
        #key = (x.utility, x.to_move, frozenset(x.board.items()))
        key = tuple(x.board.items())
        if key not in memo:
            memo[key] = f(x)
        return memo[key]

    return helper


def legal_moves(state):
    "Legal moves are any square not yet taken."
    return [(x, y) for (x, y) in state.moves
            if y == 1 or (x, y - 1) in state.board]


def k_in_row(state, player, (delta_x, delta_y)):
    board = state.board
    weights_c = [1, 3, 9, 27, 9, 3, 1]
    weights_f = [729, 243, 81, 27, 9, 3, 1]
    h1 = 0
    h2 = 0
    for move in legal_moves(state):
        pos = (move[0] + delta_x, move[1] + delta_y)
        good = 0
        # Mientras sea una posicion legal calculamos su valor para un maximo de 3 posiciones
        while (pos in state.moves or board.get(pos) == player) and good < 3:
            # Si la posicion nos pertenece
            if board.get(pos) == player:
                # Si la ficha anterior es nuestra
                if (pos[0] - delta_x, pos[1] - delta_y) == player:
                    h1 += weights_c[pos[0] - 1] * weights_f[pos[1] - 1] * 2
                # Si la ficha anterior es un hueco
                else:
                    h1 += weights_c[pos[0] - 1] * weights_f[pos[1] - 1]
            # Si la posicion es un hueco
            elif pos in state.moves:
                # Si la ficha anterior es nuestra
                if (pos[0] - delta_x, pos[1] - delta_y) == player:
                    h1 += weights_c[pos[0] - 1] * weights_f[pos[1] - 1]
                # Si la ficha anterior es un hueco
                else:
                    h1 += weights_c[pos[0] - 1] * weights_f[pos[1] - 1] / 2
            # Actualizamos las posiciones
            pos = (pos[0] + delta_x, pos[1] + delta_y)
            good += 1
        # Si es un potencial 4 en raya aumentamos su valor
        if good == 3:
            h1 *= 2
        # Reiniciamos a la posicion original
        pos = (move[0] + delta_x, move[1] + delta_y)
        good = 0
        # Mientras sea una posicion legal calculamos su valor para un maximo de 3 posiciones
        while (pos in state.moves or board.get(pos) == player) and good < 3:
            # Si la posicion nos pertenece
            if board.get(pos) == player:
                # Si la ficha anterior es nuestra
                if (pos[0] + delta_x, pos[1] + delta_y) == player:
                    h2 += weights_c[pos[0] - 1] * weights_f[pos[1] - 1] * 2
                # Si la ficha anterior es un hueco
                else:
                    h2 += weights_c[pos[0] - 1] * weights_f[pos[1] - 1]
            # Si la posicion es un hueco
            elif pos in state.moves:
                # Si la ficha anterior es nuestra
                if (pos[0] + delta_x, pos[1] + delta_y) == player:
                    h2 += (weights_c[pos[0] - 1] * weights_f[pos[1] - 1])
                # Si la ficha anterior es un hueco
                else:
                    h2 += (weights_c[pos[0] - 1] * weights_f[pos[1] - 1]) / 2
            # Actualizamos las posiciones
            pos = (pos[0] - delta_x, pos[1] - delta_y)
            good += 1
        # Si es un potencial 4 en raya aumentamos su valor
        if good == 3:
            h2 *= 2
    return h1 + h2


#Calcula segun el jugador usando move
def compute_utility(state, player):
        Pk = 0
        Pk += k_in_row(state, player, (0, 1))
        Pk += k_in_row(state, player, (1, 0))
        Pk += k_in_row(state, player, (1, -1))
        Pk += k_in_row(state, player, (-1, 1))
        if player == 'X':
            contrincante = 'O'
        else:
            contrincante = 'X'
        Pk -= k_in_row(state, contrincante, (0, 1))
        Pk -= k_in_row(state, contrincante, (1, 0))
        Pk -= k_in_row(state, contrincante, (1, -1))
        Pk -= k_in_row(state, contrincante, (-1, 1))

        return Pk

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
        #calcula el valor heuristico para el jugador
        h = compute_utility(state, 'X')
        return h