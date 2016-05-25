import games
import heuristica

# game = games.TicTacToe(h=3,v=3,k=3)
game = games.ConnectFour()

state = game.initial

# Valores iniciales
player = 'none'
dificultad1 = 'heuristica'
dificultad2 = 'human'
jugadas = 0
prof = 4

#Seleccion del jugador que empieza
while player == 'none':
    entrada = raw_input("Empieza maquina (X) o humano(O):")
    if entrada == 'x' or entrada == 'X':
        player = entrada
        state.to_move = 'X'
    elif entrada == 'o' or entrada == 'O':
        player = entrada
        state.to_move = 'O'
    else:
        print "Entrada no valida"

#Seleccion dificultad
while dificultad1 == 'heuristica':
    print "Seleccion de dificultad de la maquina: "
    entrada = raw_input("1: Facil 2: Medio 3: Dificil ")
    if entrada == '1':
        dificultad1 = "h_0", heuristica.h_0
    elif entrada == '2':
        dificultad1 = "h_1", heuristica.h_1
    elif entrada == '3':
        dificultad1 = "h_2", heuristica.h_2
    else:
        print "Entrada no valida"

while True:
    print "Jugador a mover:", state.to_move
    game.display(state)
     # HUMANO
    if state.to_move == 'O' and dificultad2 == 'human':
        coor_str = raw_input("Movimiento: ")
        coor = int(str(coor_str).strip())
        x = coor
        while (x <= 0) or (x >= 8) and coor.isdigit():
            print "Fuera del rango 1-7"
            coor_str = raw_input("Movimiento: ")
            coor = int(str(coor_str).strip())
            x = coor
        y = -1
        legal_moves = game.legal_moves(state)
        for lm in legal_moves:
            if lm[0] == x:
                y = lm[1]
        state = game.make_move((x, y), state)
        state.to_move = 'X'
        jugadas += 1
        # Cada 20 jugadas aumentamos la profundidad de busqueda
        if jugadas % 20 == 0:
            prof += 2
        print "Profundidad:", prof
        print "Dificultad:", dificultad1[0]

        #MAQUINA
    else:
        print "Thinking..."
        move = games.alphabeta_search(state, game, d=prof, cutoff_test=None, eval_fn=dificultad1[1])
        state = game.make_move(move, state)
        player = 'O'
        jugadas += 1
        # Cada 20 jugadas aumentamos la profundidad de busqueda
        if jugadas % 20 == 0:
            prof += 2
        print "Profundidad:", prof
        print "Dificultad:", dificultad1[0]
        print "-------------------"
        #Juego acabado
    if game.terminal_test(state):
        game.display(state)
        print "Final de la partida"
        if state.utility == 0:
            print "Partida empatada"
        else:
            if state.to_move == 'O':
                print "Gana el jugador: X"
            else:
                print "Gana el jugador: O"
        break
