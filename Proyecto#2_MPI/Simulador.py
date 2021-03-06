#!/usr/bin/python3
import enum
import numpy as np	# para generar números al azar según distribución estándar
from Tortuga import Tortuga
from Contador import Contador
class Simulador:
	"""
	Representa al simulador de la arribada.
	"""
	
	## VARIABLES DE CLASE
	contadores_cuadrantes = []
	contadores_tv = []
	contadores_tpb = []
	sectores_playa = []
	marea = []
	comportamiento_tortugas = []
	tortugas = []
	transecto_berma = []
	transectos_verticales = []
	cuadrantes = []
	tics = 0			## cantidad total de tics a simular
	tic = 0				## tic actual
	conteo_tpb = 0 		## variable para el conteo basado en transecto paralelo
	conteo_tsv = 0		## variable para el conteo basado en transectos verticales
	conteo_cs = 0		## variable para el conteo basado en cuadrantes
	
	
	## MÉTODOS DE CLASE
	
	## EFE:Inicializa los sectores de playa con sp. 
	@classmethod
	def inicializar_playa(cls, sp):
		cls.sectores_playa = sp
		return
	
	## EFE: Inicializa los datos de la marea con la posición i de la lista mareas.
	@classmethod
	def inicializar_marea(cls, mareas, i): #solo vamos a usar la primera. i=0
		cls.marea = mareas[i]
		return
		
	## EFE: Inicializa la arribada con el comportamiento de las tortugas y la cantidad 
	## indicada por nt de tortugas a simular.
	@classmethod
	def inicializar_arribada(cls, comportamiento, nt):
	
		cls.comportamiento_tortugas = comportamiento
		marea = cls.marea[0]
		pendiente = (cls.marea[1] - cls.marea[0]) / cls.marea[2] 
		velocidad_promedio = cls.comportamiento_tortugas[0][6]
		desv_velocidad = cls.comportamiento_tortugas[0][7]
		cls.tortugas = Tortuga.crear_lista_tortugas(nt) # falta el comportamiento
		
		for tortuga in cls.tortugas:
			# CALCULO DEL TIEMPO DE DURACION POR ESTADO CAMAR - CAMUFLAR
			
			tiempos_estado = np.zeros(5)
		
		
			# CALCULO PARA LA POSICION INICIAL DE LA TORTUGA, SALIDA.
			
			tic_salida = np.random.logistic(0, cls.comportamiento_tortugas[0][8]) 
			tic_salida += 372 / 2   #Para ajustar la distribucion logistica.
			
			pos_x_tortuga = np.random.uniform(0, cls.transecto_berma[1][1])
			pos_y_salida = marea + (pendiente * tic_salida)
			
			pos_x_tortuga = int(pos_x_tortuga)
			pos_y_salida = int(pos_y_salida)
			pos_salida = pos_x_tortuga, pos_y_salida
			
			velocidad = np.random.normal(velocidad_promedio, desv_velocidad)
			
			# CALCULO DE LA POSICION Y FINAL DE LA TORTUGA (ANIDAMIENTO)
			proba = np.random.uniform(0,1) #Probabilidad de anidamiento en los diferentes sectores de la playa
			if(proba <= cls.comportamiento_tortugas[2][3]):
				i = Simulador.pos_playa(pos_x_tortuga)
				pos_y_anidacion = np.random.uniform(cls.sectores_playa[i][1]+21, cls.sectores_playa[i][1]+30)	
			else:	
				acumulado = cls.comportamiento_tortugas[2][0] + cls.comportamiento_tortugas[2][3]
				if(proba >= cls.comportamiento_tortugas[2][3] or proba <= acumulado): #17
					i = Simulador.pos_playa(pos_x_tortuga)
					pos_y_anidacion = np.random.uniform(cls.sectores_playa[i][1]+11, cls.sectores_playa[i][1]+20)
					#pos_y_anidacion = np.random.uniform(cls.sectores_playa[i][1]-10, cls.sectores_playa[i][1])
					
				else:
					acumulado2 = acumulado + cls.comportamiento_tortugas[2][2]
					if(proba >= acumulado or proba <= acumulado2): #24
						i = Simulador.pos_playa(pos_x_tortuga)
						pos_y_anidacion = np.random.uniform(cls.sectores_playa[i][1]-10, cls.sectores_playa[i][1])
						#pos_y_anidacion = np.random.uniform(cls.sectores_playa[i][1]+11, cls.sectores_playa[i][1]+20)
					else:		
						i = Simulador.pos_playa(pos_x_tortuga)
						pos_y_anidacion = np.random.uniform(cls.sectores_playa[i][1]+21, cls.sectores_playa[i][1]+30)
							
				
			pos_y_anidacion = int(pos_y_anidacion)
			pos_anidacion = pos_x_tortuga, pos_y_anidacion
			
			## Llena una lista con los tiempos de duracion de cada estado de la tortuga
			contador = 0
			while(contador < 9):
				pos = contador // 2
				t_promedio = cls.comportamiento_tortugas[1][contador]
				ds = cls.comportamiento_tortugas[1][contador+1] #desviacion
				tiempo = np.random.normal(t_promedio, ds)
				#por si da cero o negativo dependiendo de la desviacion y el promedio
				tiempo = np.absolute(np.ceil(tiempo))
				if tiempo == 0:
					tiempo = 1
				tiempos_estado[pos] = tiempo
				contador += 2
			
			
			#Asignaciones a cada tortuga.
			tortuga.asg_velocidad(velocidad)
			tortuga.asg_posicion(pos_salida)
			tortuga.asg_pos_anidacion(pos_anidacion)
			tortuga.asg_tic_salida(tic_salida)
			tortuga.asg_tiempos_estado(tiempos_estado)
			#print(tortuga.toJSON())
			
		return

	## EFE: Inicializa el transecto paralelo a la berma.
	@classmethod
	def inicializar_transecto_berma(cls, tb):
		cls.transecto_berma = tb
		marea_media = (cls.marea[1] + cls.marea[0]) / 2.0
		velocidad = 100.0 #100 mts por minuto (tic)
		cnt_contadores = cls.transecto_berma[0][0]
		for i in range(cnt_contadores):
			c = Contador()
			pos_x = 0
			pos_y = marea_media + cls.sectores_playa[0][1]
			posicion = pos_x, pos_y
			c.asg_posicion(posicion)
			c.asg_velocidad(velocidad)
			
			cls.contadores_tpb.append(c)			
		
		return
	
	## EFE: Inicializa los transectos verticales.
	@classmethod
	def inicializar_transectos_verticales(cls, tsv):
		cls.transectos_verticales = tsv
		largo_playa = 0
	
		for i in range(0, len(cls.sectores_playa)):
			largo_playa += cls.sectores_playa[i][0]
			
		cnt_contadores = cls.transectos_verticales[0][0]
		cnt_metros_por_contador = largo_playa // cnt_contadores
		marea_media = (cls.marea[1] + cls.marea[0]) / 2.0
		
		for i in range(1, cnt_contadores+1): # 1 - n
			pos_x = (cnt_metros_por_contador * i) - 1
			pos_x = int(pos_x)
			pos_y = marea_media + cls.sectores_playa[cls.pos_playa(pos_x)][1]
			pos_y = int(pos_y)
			posicion = pos_x, pos_y
			
			contador_i = Contador()
			contador_i.asg_tiempo_muestreo(cls.transectos_verticales[0][1])
			contador_i.asg_posicion(posicion)
			cls.contadores_tv.append(contador_i)
			
		
		return
	
	## EFE: Inicializa los cuadrantes.
	@classmethod
	def inicializar_cuadrantes(cls, cs):
		cls.cuadrantes = cs
		cnt_contadores = cls.cuadrantes[0][0]
		
		for i in range(0, cnt_contadores):
			contador_i = Contador()
			contador_i.asg_tiempo_muestreo(cls.cuadrantes[0][1])
			cls.contadores_cuadrantes.append(contador_i)
			
		return	
	
	
	@classmethod
	def simular(cls, total_tics):
		cls.tics = total_tics
		marea_media =  (cls.marea[1] + cls.marea[0]) / 2.0
		pendiente = (cls.marea[1] - cls.marea[0]) / cls.marea[2] 
		marea_actual = cls.marea[0]
		
		
		while(cls.tic < cls.tics): #Tic actual menor al total
			marea_actual += pendiente	#Aumento de la marea por tic
			
			for contador in cls.contadores_tpb:
				pos_contador = contador.obt_posicion()
				if( pos_contador[0] >= 0 or pos_contador[0] <= 1500 ):
					pos_x_contador = pos_contador[0]
					sector = Simulador.pos_playa(pos_x_contador)
					pos_y_contador = marea_media + cls.sectores_playa[sector][1]
					posicion = pos_x_contador, pos_y_contador
					contador.asg_posicion(posicion)
				pos_contador = contador.obt_posicion()
				if( pos_contador[0] < 0 or pos_contador[0] > 1500 ):
					contador.aumentar_tic()
					if( contador.obt_contador_tics() == cls.transecto_berma[0][1] ):
						if( pos_contador[0] > 1500 ):
							
							contador.cambiar_estado()
							contador.avanzar_izquierda()
							contador.avanzar()
						else:
							if( pos_contador[0] < 0 ):
								contador.cambiar_estado()
								contador.avanzar_derecha()
								contador.avanzar()
				else:
					contador.avanzar()
				#print(contador.obt_posicion())
								
			#Revision del estado de los contadores en los muestreos.
			for contador in cls.contadores_cuadrantes:
				contador.aumentar_tic()
				if (contador.obt_contador_tics() == contador.obt_tiempo_muestreo()):
					contador.cambiar_estado()
					
			for contador in cls.contadores_tv:
				contador.aumentar_tic()
				if (contador.obt_contador_tics() == contador.obt_tiempo_muestreo()):
					contador.cambiar_estado()
			
			
			if(cls.tic >= 170):
				for tortuga in cls.tortugas:
					#Salida de las tortugas.
					if(int(tortuga.obt_tic_salida()) == cls.tic and not tortuga.obt_salio()):
						tortuga.avanzar()
						tortuga._salio()
					
					#	CONTEO TPB
					for contador in cls.contadores_tpb:
						#if( not tortuga.obt_contada_en_tpb() ):
						pos_contador = contador.obt_posicion()
						pos_tortuga = tortuga.obt_posicion()
							
						pos_x_contador = pos_contador[0]
						pos_y_contador = pos_contador[1]
							
						pos_x_tortuga = pos_tortuga[0]
						pos_y_tortuga = pos_tortuga[1]
							
						if( pos_x_tortuga >= pos_x_contador ):	
							if( pos_x_tortuga <= (pos_x_contador + cls.transecto_berma[0][1]) ):
								if( pos_y_tortuga >= pos_y_contador ):
									if( pos_y_tortuga <= (pos_y_contador + 15) ):
										cls.conteo_tpb += 1
											
											#tortuga.contar_en_tpb()
					
					
					if(tortuga.obt_salio() and tortuga.obt_estado() == Tortuga.EstadoTortuga.vagar):
						tortuga.avanzar()
					
						
					if(tortuga.obt_posicion() == tortuga.obt_posicion_anidacion() and tortuga.obt_estado() is not Tortuga.EstadoTortuga.inactiva):
						estado = tortuga.estado_a_int(tortuga.obt_estado())
						proba = cls.comportamiento_tortugas[0][estado]
						tortuga.cambiar_estado(proba)
					Simulador.contar_en_cuadrantes(tortuga)
					#Conteo en transecto vertical.
					for contador in cls.contadores_tv:
						if( not tortuga.obt_contada_en_tv()):
							if(contador.obt_estado() == Contador.EstadoContador.contar):
								pos_tortuga = tortuga.obt_posicion()
								pos_contador = contador.obt_posicion()
								
								if(pos_tortuga[0] == (pos_contador[0] - 1) or pos_tortuga[0] == (pos_contador[0] + 1)):
									if(pos_tortuga[1] >= pos_contador[1]):
										cls.conteo_tsv += 1
										tortuga.contar_en_tv()
									
			
			cls.tic += 1
		
		return cls.conteo_tsv, cls.conteo_cs, cls.conteo_tpb
	
	
	@classmethod
	def contar_en_cuadrantes(cls, tortuga):
		if (not tortuga.obt_contada_en_c()):
			pos_actual = tortuga.obt_posicion()
			for i in range (0, len(cls.contadores_cuadrantes)):
				if(pos_actual[0] >= cls.cuadrantes[i + 1][0]):
					if(pos_actual[0] <= cls.cuadrantes[i + 1][2]):
						#Cumplio estar en rango x del cuadrante.
						if(pos_actual[1] >= cls.cuadrantes[i + 1][1]):
							if(pos_actual[1] <= cls.cuadrantes[i + 1][3]):
								#Cumplio estar en rango y del cuadrante.
								if(cls.contadores_cuadrantes[i].obt_estado() == Contador.EstadoContador.contar):
									cls.conteo_cs += 1
									tortuga.contar_en_c()
									
		return

	@classmethod
	def reiniciar(cls):
		cls.contadores_cuadrantes.clear()
		cls.contadores_tv.clear()
		cls.contadores_tpb.clear()	
		cls.tic = 0			
		cls.conteo_tpb = 0 		
		cls.conteo_tsv = 0	
		cls.conteo_cs = 0		
		return

	@classmethod
	def pos_playa(cls, pos_x_tortuga):
		indice = -1
		if(pos_x_tortuga <= 100):
			indice = 0
		elif(pos_x_tortuga <= 200):
			indice = 1
		elif(pos_x_tortuga <= 300):
			indice = 2
		elif(pos_x_tortuga <= 400):
			indice = 3
		elif(pos_x_tortuga <= 500):
			indice = 4
		elif(pos_x_tortuga <= 600):
			indice = 5
		elif(pos_x_tortuga <= 700):
			indice = 6
		elif(pos_x_tortuga <= 800):
			indice = 7
		elif(pos_x_tortuga <= 900):
			indice = 8
		elif(pos_x_tortuga <= 1000):
			indice = 9
		elif(pos_x_tortuga <= 1100):
			indice = 10
		elif(pos_x_tortuga <= 1200):
			indice = 11
		elif(pos_x_tortuga <= 1300):
			indice = 12
		elif(pos_x_tortuga <= 1400):
			indice = 13
		elif(pos_x_tortuga <= 1500):
			indice = 14
			
		return indice
	
	## DE ESTA CLASE SIMULADOR SÓLO EXISTIRÍA UNA INSTANCIA (SINGLETON).
## POR LO QUE NO SE INCLUYEN MÉTODOS DE INSTANCIA, SÓLO MÉTODOS DE CLASE.
