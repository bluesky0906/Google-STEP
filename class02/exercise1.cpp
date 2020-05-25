#include <bits/stdc++.h>
#include <sys/time.h>
using namespace std;
string PATH = "data/ex01_cpp.txt";
int N_OF_TRIALS = 30;

// n=200までを30回ずつ繰り返し、平均をとったデータをPATHに出力

double get_time()
{
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return tv.tv_sec + tv.tv_usec * 1e-6;
}

float matrix_multi(int n)
{
    vector<vector<double>> a(n, vector<double>(n, 0)); // Matrix A
    vector<vector<double>> b(n, vector<double>(n, 0)); // Matrix B
    vector<vector<double>> c(n, vector<double>(n, 0)); // Matrix C

    // Initialize the matrices to some values.
    int i, j, k;
    for (i = 0; i < n; i++)
    {
        for (j = 0; j < n; j++)
        {
            a.at(i).at(j) = i * n + j; // A[i][j]
            b.at(i).at(j) = j * n + i; // B[i][j]
            c.at(i).at(j) = 0;         // C[i][j]
        }
    }

    double begin = get_time();

    for (i = 0; i < n; i++)
    {
        for (j = 0; j < n; j++)
        {
            for (k = 0; k < n; k++)
            {
                c.at(i).at(j) += a.at(i).at(k) * b.at(k).at(j);
            }
        }
    }

    double end = get_time();

    return end - begin;
}

int main()
{
    vector<double> results;
    ofstream outputfile(PATH);

    for (int i = 2; i <= 200; i++)
    {
        double sum = 0;
        for (int j = 0; j < N_OF_TRIALS; j++)
        {
            sum += matrix_multi(i);
        }
        double result = sum / N_OF_TRIALS;
        outputfile << i << "\t" << scientific << result << endl;
    }

    return 0;
}