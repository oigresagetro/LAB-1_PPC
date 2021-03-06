#include <iostream>
#include <vector>
#include <omp.h>
#include <time.h>

#define F1 400 //Cantidad de filas de la matriz, divisible entre 8 y 16 
#define	C1 100 //Cantidad de columnas de la matriz.
#define F2 100
#define C2 400
using namespace std;

int main() {

	srand(time(NULL));
	int thread_count = 0;
	int max_threads = omp_get_max_threads();
	int num;
	int suma = 0;
	int contador = 0;
	double wtime = 0;

	while (thread_count < 1) {
		cout << "Ingrese la cantidad de hilos: " << "max: " << max_threads << endl;
		cin >> thread_count;
	}

	int m1[F1][C1];
	int m2[F2][C2];
	int result[F1][C2];
	if (F1 == C2) {
		//Inicializacion de la primera matriz A con valores aleatorios.
		for (int fila = 0; fila < F1; ++fila) {
			for (int columna = 0; columna < C1; ++columna) {
				num = 1 + rand() % 100;  // limInferior + rand() % (limSuperior + 1 - limInferior) 1-100
				m1[fila][columna] = num;
			}
		}

		//Inicializacion de la segunda matriz B con valores aleatorios.
		for (int fila = 0; fila < F2; ++fila) {
			for (int columna = 0; columna < C2; ++columna) {
				num = 1 + rand() % 100;  // limInferior + rand() % (limSuperior + 1 - limInferior) 1-100
				m2[fila][columna] = num;
			}
		}
		wtime = omp_get_wtime();
		//Multiplicacion AxB

#	pragma omp_set_nested(1)
#	pragma omp parallel for num_threads(thread_count) \
	firstprivate(suma)
		for (int fila = 0; fila < F1; ++fila) {
			for (int columna = 0; columna < C2; ++columna) {
				for (int k = 0; k < C1; ++k) {
					suma += (m1[fila][k] * m2[k][columna]);
				}
				result[fila][columna] = suma;
				suma = 0;
			}
		}
		wtime = omp_get_wtime() - wtime;
		cout << "TIEMPO DE DURACION: " << wtime << " segundos." << endl;

		/*
		for (int fila = 0; fila < F1; ++fila) {
			for (int columna = 0; columna < C1; ++columna) {
				cout << m1[fila][columna] << " ";
			}
			cout << endl;
		}

		for (int fila = 0; fila < F2; ++fila) {
			for (int columna = 0; columna < C2; ++columna) {
				cout << m2[fila][columna] << " ";
			}
			cout << endl;
		}

		//Imprimir matriz resultante
		for (int fila = 0; fila < F1; ++fila) {
			for (int columna = 0; columna < C2; ++columna) {
				cout << result[fila][columna] << " ";
			}
			cout << endl;
		}
		*/
		
	}
	else {
		cout << "Las dimensiones de ambas matrices no calzan para la multiplicacion. Modificar los define." << endl;
	}

	cin.ignore();
	cin.ignore();
	return 0;
}
