import numpy
import time
from tqdm import tqdm

PATH = 'data/ex01_python.txt'
N_OF_TRIALS = 30

# n=200までを30回ずつ繰り返し、平均をとったデータをPATHに出力


def matrix_multi(n: int) -> float:
    a = numpy.zeros((n, n))  # Matrix A
    b = numpy.zeros((n, n))  # Matrix B
    c = numpy.zeros((n, n))  # Matrix C

    # Initialize the matrices to some values.
    for i in range(n):
        for j in range(n):
            a[i, j] = i * n + j
            b[i, j] = j * n + i
            c[i, j] = 0

    begin = time.time()

    for i in range(n):
        for j in range(n):
            for k in range(n):
                c[i, j] += a[i][k] * b[k][j]

    end = time.time()
    time_result = end - begin
    # print("time: %.6f sec" % time_result)
    return time_result


if __name__ == '__main__':
    results = []
    # progress bar
    bar = tqdm(total=200)
    # 説明文を追加
    bar.set_description('Progress rate')
    for i in range(2, 201):
        sum = 0.0
        for j in range(N_OF_TRIALS):
            sum += matrix_multi(i)
        # 進捗を設定
        bar.update(1)
        results.append(f'{i}\t{sum/N_OF_TRIALS:e}')

    # esults_str = [format(f, 'e') for f in results]
    with open(PATH, mode='w') as f:
        f.write('\n'.join(results))
