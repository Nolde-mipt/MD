import random
import numpy as np
import matplotlib.pyplot as plt


def dist(i, j):
	pos_obr = coords[j, :]
	if coords[j, 0] - coords[i, 0] > L / 2:
		pos_obr[0] = pos_obr[0] - L
	elif coords[j, 0] - coords[i, 0] < - L / 2:
		pos_obr[0] = pos_obr[0] + L
	if coords[j, 1] - coords[i, 1] > L / 2:
		pos_obr[1] = pos_obr[1] - L
	elif coords[j, 1] - coords[i, 1] < - L / 2:
		pos_obr[1] = pos_obr[1] + L
	if coords[j, 2] - coords[i, 2] > L / 2:
		pos_obr[2] = pos_obr[2] - L
	elif coords[j, 2] - coords[i, 2] < - L / 2:
		pos_obr[2] = pos_obr[2] + L
	return (coords[i, 0] - pos_obr[0]) ** 2 + (coords[i, 1] - pos_obr[1]) ** 2 + (coords[i, 2] - pos_obr[2]) ** 2
def dist_and_dir(i, j):
	pos_obr = coords[j, :]
	if coords[j, 0] - coords[i, 0] > L / 2:
		pos_obr[0] = pos_obr[0] - L
	elif coords[j, 0] - coords[i, 0] < - L / 2:
		pos_obr[0] = pos_obr[0] + L
	if coords[j, 1] - coords[i, 1] > L / 2:
		pos_obr[1] = pos_obr[1] - L
	elif coords[j, 1] - coords[i, 1] < - L / 2:
		pos_obr[1] = pos_obr[1] + L
	if coords[j, 2] - coords[i, 2] > L / 2:
		pos_obr[2] = pos_obr[2] - L
	elif coords[j, 2] - coords[i, 2] < - L / 2:
		pos_obr[2] = pos_obr[2] + L
	delta_x = coords[i, 0] - pos_obr[0]
	delta_y = coords[i, 1] - pos_obr[1]
	delta_z = coords[i, 2] - pos_obr[2]
	dist_sqr = delta_x ** 2 + delta_y ** 2 + delta_z ** 2
	dist = dist_sqr ** (1 / 2)
	return [delta_x / dist,
		delta_y / dist,
		delta_z / dist,
		dist_sqr
			]


def placing():
	global coords, v
	coords = np.zeros((N, 3))
	v = np.zeros((N, 3))
	coords[0, 0] = random.uniform(0, L)
	coords[0, 1] = random.uniform(0, L)
	coords[0, 2] = random.uniform(0, L)
	for i in range(1, N):
		while True:
			distcheck = True
			coords[i, 0] = random.uniform(0, L)
			coords[i, 1] = random.uniform(0, L)
			coords[i, 2] = random.uniform(0, L)
			for j in range (0, i):
				if dist(i, j) <= 0.81:
					distcheck = False
			if distcheck:
				break
	print('placing_done')


def pot(i, j):
	a = dist(i, j)
	return 4 * (((1 / a)) ** 6 - ((1 / a) ** 3))


def force(i, j):
	a = dist(i, j)
	return 4 * (((1 / a) ** (7 / 2)) * 6 - ((1 / a) ** (13 / 2)) * 12)



print('введите число частиц')
N = int(input())
ro = 0.16
print('введите шаг времени')
T = float(input())
print('введите число итераций')
n = int(input())
V = N / ro
L = V ** (1 / 3)
print(L)
placing()
Energy = np.zeros((n, 3))
for i in range(N):
	for j in range(i):
		Energy[0, 0] += pot(i, j)
for step in range(1, n):
	for i in range(N):
		for j in range(i):
			f = force(i, j)
			d = dist_and_dir(i, j)
			for k in range(3):
				v[i, k] += f * d[k] * T
				v[j, k] -= f * d[k] * T
	sqr_v = v ** 2
	Energy[step, 1] = np.sum(sqr_v) / 2
	
	coords += v * T
	
	for i in range(N):
		for k in range(3):
			if coords[i, k] > L:
				coords[i, k] -= (coords[i,k] // L) * L
			elif coords[i, k] < 0:
				coords[i, k] += ((coords[i, k] // L) + 1) * L
		for j in range(i):
			Energy[step, 0] += pot(i, j)
Energy[:, 2] = Energy[:, 0] + Energy[:, 1]
print(Energy)

plotx = range(0, n)
ploty = Energy[:, 2]
plt.plot(plotx, ploty)
plt.show() 
