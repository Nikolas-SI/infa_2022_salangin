#include <iostream>
#include <chrono>
#include <random>
#include <stdio.h>
#include <stdlib.h>

using namespace std;

int func_A(int a[], int key, int n) {
	for (int i = 0; i < n; i++) {
		if (a[i] == key) {
			if (i != 0) {
				int buf = a[i];
				a[i] = a[0];
				a[0] = buf;
			}
			return 1;
		}
	}
	return 0;
}

int func_B(int a[], int key, int n) {
	for (int i = 0; i < n; i++) {
		if (a[i] == key) {
			if (i != 0) {
				int buf = a[i];
				a[i] = a[i-1];
				a[i-1] = buf;
			}
			return 1;
		}
	}
	return 0;
}

int func_C(int a[], int key, int n, int b[]) {
	for (int i = 0; i < n; i++) {
		if (a[i] == key) {
			b[i] += 1;
			if (i != 0 && b[i] > b[i - 1]) {
				int buf = a[i];
				a[i] = a[i-1];
				a[i - 1] = buf;
			}
			return 1;
		}
	}
	return 0;
}



int main() {
	unsigned seed = 1001;
	default_random_engine rng(seed);

	for (int n = 100; n < 10000; n = n + 100) {
		/*выделение памяти*/
		int* a = (int*)calloc(n, sizeof(int));
		int* b = (int*)calloc(n, sizeof(int));

		for (int i = 0; i < n; i++) {
			a[i] = i;
		}
		for (int i = 0; i < n; i++) {
			b[i] = 0;
		}

		auto begin = chrono::steady_clock::now();
		for (unsigned cnt = 100000; cnt != 0; --cnt) {
			binomial_distribution<> dstr(n, 0.5);
			/*uniform_int_distribution<unsigned> dstr(0, n + 0.01*n);*/
			int key = dstr(rng);
			func_C(a, key, n, b);
		}
		auto end = chrono::steady_clock::now();
		auto time_span =
			chrono::duration_cast<std::chrono::microseconds>(end - begin);

		cout << time_span.count() / (10) << endl;
		/*стираем память*/
		free(a);
		free(b);
	}

}