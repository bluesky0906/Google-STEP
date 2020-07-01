#include <bits/stdc++.h>
#include <sys/time.h>
using namespace std;
string PATH = "data/ex01_cpp.txt";
int N_OF_TRIALS = 10;

double get_time()
{
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return tv.tv_sec + tv.tv_usec * 1e-6;
}

float matrix_multi(int n)
{
    double *a = (double *)malloc(n * n * sizeof(double)); // Matrix A
    double *b = (double *)malloc(n * n * sizeof(double)); // Matrix B
    double *c = (double *)malloc(n * n * sizeof(double)); // Matrix C

    // Initialize the matrices to some values.
    int i, j;
    for (i = 0; i < n; i++)
    {
        for (j = 0; j < n; j++)
        {
            a[i * n + j] = i * n + j; // A[i][j]
            b[i * n + j] = j * n + i; // B[i][j]
            c[i * n + j] = 0;         // C[i][j]
        }
    }

    double begin = get_time();

    // Write code to calculate C = A * B.
    int k;

    for (k = 0; k < n; k++)
    {
        for (i = 0; i < n; i++)

        {
            for (j = 0; j < n; j++)

            {
                c[i * n + j] += a[i * n + k] * b[k * n + j];
            }
        }
    }

    double end = get_time();
    free(a);
    free(b);
    free(c);
    return end - begin;
}

int main()
{
    int i = 1000;
    double sum = 0;
    for (int j = 0; j < N_OF_TRIALS; j++)
    {
        sum += matrix_multi(i);
    }
    double result = sum / N_OF_TRIALS;

    cout << fixed << result << endl;

    return 0;
}