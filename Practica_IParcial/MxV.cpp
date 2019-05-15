#include <iostream>
#include <omp.h>
#include <time.h>
#include <vector>
using namespace std;

#define MAX_SIZE_F 160
#define	MAX_SIZE_C 160
#define MAX_SIZE_V 160


int main() {

	srand(time(NULL));
	int matriz[MAX_SIZE_F][MAX_SIZE_C];
	int v[MAX_SIZE_V];
	vector<int> result;
	result.resize(MAX_SIZE_F); //A= 4X8 * V = 8X1 => R = 4X1

	int num;
	int suma = 0;
	int num_threads = 0;
	int max_num_threads = omp_get_max_threads();

	while (num_threads < 1) {
		cout << "Ingrese la cantidad de threads:\n Cantidad maxima: "<< max_num_threads << endl;
		cin >> num_threads;
	}

	for (int fila = 0; fila < MAX_SIZE_F; ++fila) {
		for (int columna = 0; columna < MAX_SIZE_C; ++columna) {
			num = 1 + rand() % (100);
			matriz[fila][columna] = num;
			cout << num << " ";
		}
		cout << endl;
	}
	cout << "\n\n";

	for (int i = 0; i < MAX_SIZE_V; ++i) {
		num = 1 + rand() % (100);
		v[i] = num;
		cout << num << " ";
	}
	cout << endl;

	//Multiplicacion de matrix por vector
	if (MAX_SIZE_C == MAX_SIZE_V) {

#	pragma omp parallel for num_threads(num_threads) \
	firstprivate(suma)
		for (int fila = 0; fila < MAX_SIZE_F; ++fila) {
			for (int columna = 0; columna < MAX_SIZE_C; ++columna) {
				suma += (matriz[fila][columna] * v[columna]);
			}
#	pragma omp critical 
			{
				cout << "Thread: " << omp_get_thread_num() << "Reportando la suma: " << suma << endl;
				result[fila] = suma;
			}
			suma = 0;
		}
	}
	

	for (int i = 0; i < MAX_SIZE_V; ++i) {
		cout << result[i] << endl;
	}

	cin.ignore();
	cin.ignore();

	return 0;
}
