# Reglas del juego:
# 	Objetivo: Obtener una puntuación mas alta que el crupier pero sin pasarse de 21.
#
# 	Reglas de la apuesta:
# 		Perdio: 	El crupier se queda con la apuesta.
# 		Gano: 		El jugador gana la mismacantidad que aposto.
# 		Blackjack:	El jugador gana 1.5 veses la cantidad que aposto.
# 		Empate:		El jugador conserva su apuesta. No pierde ni gana nada.
# 	Valores de las cartas:
#
# 		Cartas del 2 al 10: Tienen el valor indicado en la carta.
# 		J, Q, K: 			Valen por 10
# 		A: 					Vale por 1 o por 11 (el jugador elije)
#
# 	Estructura del juego:
#		Inicio: Al comienzo del juego el jugador y el crupier resiven 2 cartas.
# 			Las cartas del jugador estan boca arriba mientras que las del crupier hay una boca abajo y otra boca arriba
# 			La mejor jugada posible es un Blackjack. Pasa cuando el jugador o el crupier tiene un As y una carta que valga 10.
#			Si el jugador tiene un Blackjack gana automaticamente amenos que el crupier tambien lo tenga. En este caso es un empate y el jugador recupera su apuesta
# 			Si el crupier tiene un Blackjack el jugador pierde amenos que tambien tenga un Blackjack.
#		
#		El turno del jugador:
# 			El jugador puede mantener su mano o tomar mas cartas del deck asta que crea que su mano ya esta lo suficiente mente fuerte o sobre pase 21.
#			En caso de que el jugador sobre pase 21 pierde automaticamente
# 		
#		El turno del crupier:
#			Si el crupier tiene un Blackjack todos los jugadores pierden exepto los que tambien tengan un Blackjack.
#			En caso de que el crupier no tenga un Blackjack el toma cartas del deck dependiendo del valor de su mano.
# 			El crupier debe tomar cartas si el valor de su mano es menor que 17 en caso contrario debe mantener su mano.
# 		
# 		Mostrar:
#			Si el crupier sobre pasa el valor de 21, el jugador gana.
#			Si el valor del jugador es mayor que el del crupier, el jugador gana.
#			Si el valor del jugador es menor que el del crupier, el jugador pierde.
#			Si el jugador tiene un Blackjack y el crupier no, el jugador gana.
#			Si el crupier tiene un Blackjack y el jugador no, el jugador pierde.

import random

class Deck(object):

        cartasCompletas = ["A ♡","2 ♡","3 ♡","4 ♡","5 ♡","6 ♡","7 ♡","8 ♡","9 ♡","10 ♡","J ♡","Q ♡","k ♡","A ♣","2 ♣","3 ♣","4 ♣","5 ♣","6 ♣","7 ♣","8 ♣","9 ♣","10 ♣","J ♣","Q ♣","k ♣","A ♠","2 ♠","3 ♠","4 ♠","5 ♠","6 ♠","7 ♠","8 ♠","9 ♠","10 ♠","J ♠","Q ♠","k ♠","A ♢","2 ♢","3 ♢","4 ♢","5 ♢","6 ♢","7 ♢","8 ♢","9 ♢","10 ♢","J ♢","Q ♢","k ♢"]

        def __init__(self):
		# Copia de las cartas
		self.resetearBaraja()

	def barajar(self):
		random.shuffle(self.cartas)

	def tomarCarta(self):
		lenCartas = len(self.cartas)
		randomNum = random.randint(0, lenCartas - 1)
		return self.cartas.pop(randomNum)

        def resetearBaraja(self):
		self.cartas = list(self.cartasCompletas)
		self.barajar()

	def __str__(self):
		return ", ".join(self.cartas)

class Jugador(object):
	def __init__(self,nombre, dinero=0):
		self.nombre = nombre
		self.dinero = dinero
		self.mano = []

	def manoInicial(self, deck):
		self.borrarMano()
		self.tomarCarta(deck)
		self.tomarCarta(deck)

	def tomarCarta(self, deck):
		self.mano.append(deck.tomarCarta())

	def borrarMano(self):
		self.mano = []

	def tieneAs(self):
		if "A ♡" in self.mano or "A ♣" in self.mano or "A ♠" in self.mano or "A ♢" in self.mano:
			return True
		return False

	def apostar(self, apuesta):
		if self.dinero >= apuesta:
			self.dinero -= apuesta
			return True
		else:
			return False

	def mostrarMano(self):
		s = ", ".join(["["+x+"]" for x in self.mano])
		base = "La mano de %s es %s y en total vale %i"
		baseConAs = "La mano de %s es %s y en total vale %i o %i"
		if self.tieneAs() and valorMano(self.mano, As=11) <= 21:
			print baseConAs%(self.nombre, s, valorMano(self.mano), valorMano(self.mano, As=11))
		else:
			print base%(self.nombre, s, valorMano(self.mano))

class Juego(object):
	def __init__(self):
		self.deck = Deck()
		self.apuesta = 0

	def juego(self):
		self.setup()
		while self.jugador.dinero > 0:
			blackjack = self.inicio()
			if blackjack == 0:
				jugadorSobrePasa = self.turnoJugador()
				if jugadorSobrePasa == 0:
					crupierSobrePasa = self.turnoCrupier()
					if crupierSobrePasa == 0:
						ganador = self.mostrar()
						if ganador == 1:
							self.apuesta *= 2
							self.jugador.dinero += self.apuesta
							self.apuesta = 0
						elif ganador == 0:
							# Es un empate
							self.jugador.dinero += self.apuesta
							self.apuesta = 0
					else:
						self.apuesta *= 2
						self.jugador.dinero += self.apuesta
						self.apuesta = 0
			elif blackjack == 1:
				# El jugador hace blackjack
				self.apuesta *= 2.5
				self.jugador.dinero += self.apuesta
				self.apuesta = 0
			elif blackjack == 3:
                                # Es un empate
				self.jugador.dinero += self.apuesta
				self.apuesta = 0
		print "Te quedaste sin dinero. Perdiste :'("

	def setup(self):
		nombre = raw_input("Nombre del jugador: ")
		self.jugador = Jugador(nombre, 1000)
		self.crupier = Jugador("Crupier")

		print "%s tu saldo inicial es %i"%(nombre, 1000)

	def apostar(self):
		apuesta = 0
		while True:
			apuesta = None
			apuesta_str = raw_input("Tienes %i. ¿Cuanto deseas apostar? "%self.jugador.dinero)
			try:
				apuesta = int(apuesta_str)
			except ValueError:
				print "'%s' no es un numero valido" % apuesta_str
			if apuesta:
				if apuesta > 0:
					if self.jugador.apostar(apuesta):
						break
					else:
						print "No tienes suficiente dinero para hacer esa apuesta"
				else:
					print "La apuesta minima es 1"
		self.apuesta = apuesta

	def inicio(self):
		"""Devuelve 1 si el jugador gana con un Blackjack,
			devuelve 2 si el crupier gana con un Blackjack,
			devuelve 3 si es un empate con Blackjack,
			devuelve 0 si no hay Blackjack"""
		self.deck.resetearBaraja()

		self.jugador.manoInicial(self.deck)
		self.crupier.manoInicial(self.deck)

		self.apostar()

		if esBlackjack(self.jugador.mano):
			if esBlackjack(self.crupier.mano):
				print "Es un empate, ambos tienen un Blackjack"
				return 3
			else:
				print "El jugador gana, tiene un Blackjack"
				return 1
		elif esBlackjack(self.crupier.mano):
			print "El crupier gana con un Blackjack"
			return 2

		return 0

	def turnoJugador(self):
		"""Devuelve 1 si el jugador supera los 21 sino devuelve 0"""
		print "La mano del crupier es [%s]"%self.crupier.mano[1]
		self.jugador.mostrarMano()

		while True:
			if inputSi("Quieres tomar otra carta? "):
				self.jugador.tomarCarta(self.deck)

				self.jugador.mostrarMano()

				if valorMano(self.jugador.mano) > 21:
					print "Superaste los 21. Perdiste"
					return 1
			else:
				break

		return 0

	def turnoCrupier(self):
		"""Devuelve 1 si el crupier supera los 21"""
		while valorMano(self.crupier.mano) < 17:
			self.crupier.tomarCarta(self.deck)

		if valorMano(self.crupier.mano) > 21:
			print "El cupier supera los 21. El jugador gana"
			return 1
		return 0

	def mostrar(self):
		"""Devuelve 1 si el jugador gana.
			Devuelve 2 si el crupier gana.
			Devuelve 0 si es un empate"""

		self.jugador.mostrarMano()
		self.crupier.mostrarMano()
		if manoMayor(self.jugador.mano, self.crupier.mano) == 1:
			print "El jugador gana!"
			return 1
		elif manoMayor(self.jugador.mano, self.crupier.mano) == 2:
			print "El crupier gana."
			return 2
		else:
			print "Es un empate."
			return 0

def inputSi(msg):
	respuestasAfirmativas = ["s", "si"]
	respuestasNegativas = ["n", "no"]
	while True:
		respuesta = raw_input(msg)
		if respuesta.lower() in respuestasAfirmativas:
			return True
		elif respuesta.lower() in respuestasNegativas:
			return False
		else:
			print "'%s' no es una respuesta valida intenta con 'si' o 'no'"%respuesta

def esBlackjack(mano):
	if valorMano(mano, As=11) == 21:
		return True
	return False

def valorMano(mano, As=1):
	valor = 0
	for carta in mano:
		num = carta.split(" ")[0]
		if num == "A":
			valor += As
		elif num == "J" or num == "Q" or num == "k":
			valor += 10
		else:
			valor += int(num)

	return valor

def manoMayor(mano1, mano2):
	"""Devuelve 1 si la mano1 es mayor que la mano2.
		Devuelve 2 si la mano2 es mayor que la mano1
		Devuelve 0 si las dos manos valen lo mismo"""
	if valorMano(mano1, As=11) <= 21:
		valorMano1 = valorMano(mano1, As=11)
	else:
		valorMano1 = valorMano(mano1)

	if valorMano(mano2, As=11) <= 21:
		valorMano2 = valorMano(mano2, As=11)
	else:
		valorMano2 = valorMano(mano2)

	if valorMano1 == valorMano2:
		return 0
	elif valorMano1 > valorMano2:
		return 1
	elif valorMano1 < valorMano2:
		return 2

def main():
	juego = Juego()
	juego.juego()

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
                print "\nGracias por jugar. Vuelve cuando quieras!!"
