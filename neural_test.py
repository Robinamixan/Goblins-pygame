import numpy as np


np.set_printoptions(threshold=np.nan, precision=2, suppress=True)


# Сигмоида
def nonlin(x, deriv=False):
    if deriv:
        return x * (1 - x)
    return 1 / (1 + np.exp(-x))


l1 = 0
X = np.array([
    [0, 0, 3, 0],
    [0, 0, 0, 3],
    [0, 0, 3, 3],
    [3, 3, 3, 0],
    [3, 3, 0, 3],
    [3, 3, 0, 0],
    [0, 0, 0, 0],
    [2, 1, 1, 2],
    [0, 3, 3, 0]
              ])

y = np.array([
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 1, 1, 0],
    [1, 0, 0, 0],
    [0, 0, 0, 1],
    [1, 0, 0, 1],
    [0, 0, 0, 0],
    [0, 0, 1, 1],
    [1, 1, 0, 0],
])

input_amount = 4

examples_amount = 8

output_amount = 4

np.random.seed(1)

# # случайно инициализируем веса, в среднем - 0
# syn0 = 2 * np.random.random((input_amount, examples_amount)) - 1
# syn1 = 2 * np.random.random((examples_amount, output_amount)) - 1
#
# for j in range(60000):
#
#     # проходим вперёд по слоям 0, 1 и 2
#     l0 = X
#     l1 = nonlin(np.dot(l0, syn0))
#     l2 = nonlin(np.dot(l1, syn1))
#
#     # как сильно мы ошиблись относительно нужной величины?
#     l2_error = y - l2
#
#     # if (j % 10000) == 0:
#     #     print("Error:" + str(np.mean(np.abs(l2_error))))
#
#     # в какую сторону нужно двигаться?
#     # если мы были уверены в предсказании, то сильно менять его не надо
#     l2_delta = l2_error * nonlin(l2, deriv=True)
#
#     # как сильно значения l1 влияют на ошибки в l2?
#     l1_error = l2_delta.dot(syn1.T)
#
#     # в каком направлении нужно двигаться, чтобы прийти к l1?
#     # если мы были уверены в предсказании, то сильно менять его не надо
#     l1_delta = l1_error * nonlin(l1, deriv=True)
#
#     syn1 += l1.T.dot(l2_delta)
#     syn0 += l0.T.dot(l1_delta)
#
# print("Выходные данные после тренировки:")
# # print(l2)
#
# np.savetxt('syn0.txt', syn0)
# np.savetxt('syn1.txt', syn1)

syn0 = np.loadtxt('syn0.txt')
syn1 = np.loadtxt('syn1.txt')

C = [25, 12, 1, 2]

l0 = C
l1 = nonlin(np.dot(l0, syn0))
l2 = nonlin(np.dot(l1, syn1))
print("Выходные данные после тренировки:")

print(l2)
