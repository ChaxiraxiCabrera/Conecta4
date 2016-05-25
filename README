En el fichero heuristica.py se encuentra implementadas las diferentes heuristicas, una para cada dificultad.
Tambien se encuentra la implementacion de memoize usada por cada heuristica.
El fichero run.py se implemento de modo que pregunta que jugador empezara (X = maquina, O = humano),
y la dificultad de la maquina.
En games.py se añadio una clase para darle color al tablero.

heuristica.py
Para el nivel facil tenemos h0, la cual siempre devuelve 0.
Para el medio tenemos h1, que retorna un valor aletaorio entre 100 y -100
Para el dificil tenemos h2, usa el metodo compute_utility (que calcula el valor
de la heuristica), calcula el valor con el metodo move, cuenta los potenciales 4 en raya,
es decir, localiza el numero de piezas alineadas del jugador (mayor numero de piezas
alineadas, mayor valor) y le resta el numero de potenciales 4 en raya del contrario.
Ademas dependiendo de la posicion en la que se localicen las fichas se le asigna un peso,
dando mayor valor a las piezas mas abajo y centradas que al resto.