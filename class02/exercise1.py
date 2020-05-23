import numpy, sys, time
PATH ='data/ex01_python.txt'

def matrix_multi(n: int) -> float:
    a = numpy.zeros((n, n)) # Matrix A
    b = numpy.zeros((n, n)) # Matrix B
    c = numpy.zeros((n, n)) # Matrix C

    # Initialize the matrices to some values.
    for i in range(n):
        for j in range(n):
            a[i, j] = i * n + j
            b[i, j] = j * n + i
            c[i, j] = 0

    begin = time.time()

    for i in range(n):
        for j in range(n):
            sum = 0
            for k in range(n):
                sum += a[i][k] * b[k][j]
            c[i,j] = sum

    end = time.time()
    time_result = end - begin
    #print("time: %.6f sec" % time_result)
    return time_result


if __name__ == '__main__':
    results = []
    for i in range(2,101):
        results.append(f'{i}\t{matrix_multi(i):e}')

    #results_str = [format(f, 'e') for f in results]
    with open(PATH, mode='w') as f:
        f.write('\n'.join(results))

