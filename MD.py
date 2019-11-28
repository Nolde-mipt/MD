import random


random.seed(version = 2)


def dist(i, j) :
	pos_obr = [x[j], y[j], z[j]]
	if x[j] - x[i] > L / 2 :
		pos_obr[0] = pos_obr[0] - L
	elif x[j] - x[i] < - L / 2 :
		pos_obr[0] = pos_obr[0] + L
	if y[j] - y[i] > L / 2 :
		pos_obr[1] = pos_obr[1] - L
	elif y[j] - y[i] < - L / 2 :
		pos_obr[1] = pos_obr[1] + L
	if z[j] - z[i] > L / 2 :
		pos_obr[2] = pos_obr[2] - L
	elif z[j] - z[i] < - L / 2 :
		pos_obr[2] = pos_obr[2] + L
	return (x[i] - pos_obr[0]) ** 2 + (y[i] - pos_obr[1]) ** 2 + (z[i] - pos_obr[2]) ** 2
def dist_and_dir(i, j) :
	pos_obr = [x[j], y[j], z[j]]
	if x[j] - x[i] > L / 2 :
		pos_obr[0] = pos_obr[0] - L
	elif x[j] - x[i] < - L / 2 :
		pos_obr[0] = pos_obr[0] + L
	if y[j] - y[i] > L / 2 :
		pos_obr[1] = pos_obr[1] - L
	elif y[j] - y[i] < - L / 2 :
		pos_obr[1] = pos_obr[1] + L
	if z[j] - z[i] > L / 2 :
		pos_obr[2] = pos_obr[2] - L
	elif z[j] - z[i] < - L / 2 :
		pos_obr[2] = pos_obr[2] + L
	delta_x = x[i] - pos_obr[0]
	delta_y = y[i] - pos_obr[1]
	delta_z = z[i] - pos_obr[2]
	dist_sqr = delta_x ** 2 + delta_y ** 2 + delta_z ** 2
	return [delta_x / ((dist_sqr) ** (1 / 2)),
		delta_y / ((dist_sqr) ** (1 / 2)),
		delta_z / ((dist_sqr) ** (1 / 2)),
		dist_sqr]


def placing() :
	global x, vx, y, vy, z, vz
	x = [0] * N
	y = [0] * N
	z = [0] * N
	vx = [0] * N
	vy = [0] * N
	vz = [0] * N
	x[0] = random.uniform(0, L)
	y[0] = random.uniform(0, L)
	z[0] = random.uniform(0, L)
	for i in range(1, N):
		while True:
			distcheck = True
			x[i] = random.uniform(0, L)
			y[i] = random.uniform(0, L)
			z[i] = random.uniform(0, L)
			for j in range (0, i):
				if dist(i, j) <= 0.81 :
					distcheck = False
			if distcheck:
				break
	print('placing_done')


def pot(i, j) :
	return 4 * (((1 / dist(i, j)) ** 6 - ((1 / dist(i, j)) ** 3)))


def force(i, j) :
	return 4 * (((1 / dist_and_dir(i, j)[3]) ** 7 / 2) * 6 - ((1 / dist_and_dir(i, j)[3]) ** 13 / 2) * 12)



print('введите число частиц')
N = int(input())
ro = 0.03
print('введите шаг времени')
T = float(input())
print('введите число итераций')
n = int(input())
V = N / ro
print(V)
L = V ** (1 / 3)
print(L)
placing()
EnP = 0
EnK = 0
EnF = [0] * (n + 1)
for i in range(N):
	for j in range(i):
		EnP = EnP + pot(i, j)
EnF[0] = EnP
for step in range(1, n + 1):
	EnP = 0
	EnK = 0
	for i in range(N):
		for j in range(i):
			vx[i] = vx[i] + force(i, j) * dist_and_dir(i, j)[0] * T
			vx[j] = vx[j] - force(i, j) * dist_and_dir(i, j)[0] * T
			vy[i] = vy[i] + force(i, j) * dist_and_dir(i, j)[1] * T
			vy[j] = vy[j] - force(i, j) * dist_and_dir(i, j)[1] * T
			vz[i] = vz[i] + force(i, j) * dist_and_dir(i, j)[2] * T
			vz[j] = vz[j] - force(i, j) * dist_and_dir(i, j)[2] * T
		x[i] = x[i] + vx[i] * T
		y[i] = y[i] + vy[i] * T
		z[i] = z[i] + vz[i] * T
		EnK = EnK + (vx[i] ** 2 + vy[i] ** 2 + vz[i] ** 2) / 2
		for j in range(i):
			EnP = EnP + pot(i, j)
	for i in range(N):
		if x[i] > L :
			x[i] -= L
		elif x[i] < 0 :
			x[i] += L
		if y[i] > L :
			y[i] -= L
		elif y[i] < 0 :
			y[i] += L
		if z[i] > L :
			z[i] -= L
		elif z[i] < 0 :
			z[i] +=L
	EnF[step] = EnK + EnP
print(EnF)
for i in range(0, N, 100):
	print EnF[i]
