import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# グラフに描画

# Pythonを読み込み
py_df = pd.read_table('data/ex01_python.txt', header = None)
print(py_df[1])
plt.plot(py_df[0], py_df[1], label='Python')

# C++を読み込み
cp_df = pd.read_table('data/ex01_cpp.txt', header = None)
plt.plot(cp_df[0], cp_df[1], label='C++')


plt.title('Time Complexity')
plt.xlabel('Dimension of Matrix')
plt.ylabel('Time Complexity (sec)')
plt.legend()
# plt.show()
plt.savefig('img/resuls.png')