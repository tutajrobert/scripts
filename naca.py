import matplotlib.pyplot as plt
import numpy as np
import math

def func(x, m, p, c):
	if (x >= 0) and (x < p*c):
		return m * (x / (p**2)) * (2*p - (x/c))
	elif (x >= p*c) and (x <= c):
		return m * ((c - x) / ((1-p)**2)) * (1 + (x/c) - (2*p))

def dif(x, m, p, c):
	if (x >= 0) and (x < p*c):
		return math.atan(((2*m) / p**2) * (p - (x/c)))
	elif (x >= p*c) and (x <= c):
		return math.atan(((2*m) / ((1-p)**2)) * (p - (x/c)))

def distr(x, t):
	return (t / 0.2) * ((0.2969 * (x**(0.5))) - (0.1260 * x) - (0.3516 * (x**2)) + (0.2843 * (x**3)) - (0.1015 * (x**4)))

def centers(before_x, after_x, before_y, after_y):
	x = (after_x + before_x) / 2.0
	y = (after_y + before_y) / 2.0
	r = math.sqrt((after_x - before_x)**2 + (after_y - before_y)**2)
	n0 = before_y - after_y
	n1 = after_x - before_x
	return [x, y, r, n0, n1]

def colors(value, max):
	color = ["#7B1713", "#B80000", "#F34700", "#FC8408", "#FFB500", "#FFE600"]
	return color[int(round((value / max) * 5, 0))]

def rotation(x, y, ang, chord):
	x_rot = ((x - (chord / 2.0)) * math.cos((ang * math.pi)/180.0)) - y * math.sin((ang * math.pi)/180.0)
	y_rot = ((x - (chord / 2.0)) * math.sin((ang * math.pi)/180.0)) + y * math.cos((ang * math.pi)/180.0)
	return [x_rot, y_rot]

m = 0.02 #maximum camber 
p = 0.4 #location of maximum camber
c = 1.0 #chord
t = 0.15 #thickness
v = 1.5111e-5
points = 40
scale = 1.0

u = 15.111 #velocity
ang = -5 #angle of attack
	
ux = u * math.cos((ang * math.pi)/180.0)
uy = u * math.sin((ang * math.pi)/180.0)

X = []
for i in range(0, points):
	X.append((c / float(points - 1)) * i)

camber = [func(x, m, p, c) for x in X]
y_up = [func(x, m, p, c) + (distr(x, t) * math.cos(dif(x, m, p, c))) for x in X]
x_up = [x - (distr(x, t) * math.sin(dif(x, m, p, c))) for x in X]
y_down = [func(x, m, p, c) - ((distr(x, t) * math.cos(dif(x, m, p, c)))) for x in X]
x_down = [x + (distr(x, t) * math.sin(dif(x, m, p, c))) for x in X]

x_up_rot = []
y_up_rot = []
x_down_rot = []
y_down_rot = []

for i in range(0, len(x_up)):
	y = y_up[i]
	x = x_up[i]
	coord = rotation(x, y, ang, c)
	y = coord[1]
	x = coord[0]
	x_up_rot.append((c / 2.0) + x)
	y_up_rot.append(y)

	y = y_down[i]
	x = x_down[i]
	coord = rotation(x, y, ang, c)
	y = coord[1]
	x = coord[0]
	x_down_rot.append((c / 2.0) + x)
	y_down_rot.append(y)

x_down_rev = [x for x in x_down]
x_down_rev.reverse()
x_down_rev.pop(-1)
x_all = x_down_rev + x_up

y_down_rev = [y for y in y_down]
y_down_rev.reverse()
y_down_rev.pop(-1)
y_all = y_down_rev + y_up

centers_x = []
centers_y = []
normals0 = []
normals1 = []
lengths = []
n_lengths = []

for i in range(0, len(x_all) - 1):
	sol = centers(x_all[i], x_all[i+1], y_all[i], y_all[i+1])
	centers_x.append(sol[0])
	centers_y.append(sol[1])
	lengths.append(1)
	n_lengths.append(sol[2])
	normals0.append(sol[3] * scale)
	normals1.append(sol[4] * scale)

a_matrix = []
b_matrix = []

for i in range(0, len(centers_x)):
	u1 = ux * centers_y[i]
	u2 = uy * centers_x[i]
	equation = []
	for j in range(0, len(centers_x) - 1):
		if (i == j and i != 0):
			equation.append(0.0)
		elif (i == j and i == 0):
			equation.append((-1) * (math.log(abs(math.sqrt((centers_x[i]**2) + (centers_y[i]**2)) - math.sqrt((centers_x[len(centers_x) - 1]**2) + (centers_y[len(centers_x) - 1]**2))))) * (lengths[i] / (2 * math.pi)))
		elif (j == 0 and i != (len(centers_x) - 1)) :
			equation.append(((math.log(abs(math.sqrt((centers_x[i]**2) + (centers_y[i]**2)) - math.sqrt((centers_x[j]**2) + (centers_y[j]**2))))) * (lengths[i] / (2 * math.pi))) - 
				((math.log(abs(math.sqrt((centers_x[i]**2) + (centers_y[i]**2)) - math.sqrt((centers_x[len(centers_x) - 1]**2) + (centers_y[len(centers_x) - 1]**2))))) * (lengths[i] / (2 * math.pi))))
		else:
			equation.append((math.log(abs(math.sqrt((centers_x[i]**2) + (centers_y[i]**2)) - math.sqrt((centers_x[j]**2) + (centers_y[j]**2))))) * (lengths[i] / (2 * math.pi)))

	equation.append(1)
	a_matrix.append(equation)

	b_matrix.append(u1 - u2)

a_matrix = np.array(a_matrix)
b_matrix = np.array(b_matrix)

x_matrix = np.linalg.solve(a_matrix, b_matrix)

gamma = []
for i in range(0, len(x_matrix) - 1):
	gamma.append(x_matrix[i] * lengths[i])

gamma.append((-1) * x_matrix[0] * lengths[-1])
gamma_all = sum(gamma)

Re = (u * c) / v
cl = round((-2 * gamma_all) / (c * u), 4)

print cl
print x_matrix

fig = plt.figure()
ax = fig.add_subplot(111)

plt.plot(X, camber)
plot_up = plt.plot(x_up, y_up)
plt.plot(x_down, y_down)
plt.grid()

if t*100 < 10:
	plt.title('NACA ' + str(int(m*100)) + str(int(p*10)) + "0" + str(int(t*100)) + '\n')
else:
	plt.title('NACA ' + str(int(m*100)) + str(int(p*10)) + str(int(t*100)) + '\n')
plt.xlim(0 - (0.1*c), c + (0.1*c))
plt.ylim(min(y_down) - (0.2*t), max(y_up) + (0.2*t))
plt.xlabel('chord')
plt.ylabel('chord %')
ax.set_aspect('equal', 'datalim')

plt.show()

#################################

fig = plt.figure()
ax = fig.add_subplot(111)

plt.plot(X, camber)
plot_up = plt.plot(x_up_rot, y_up_rot)
plt.plot(x_down_rot, y_down_rot)
plt.grid()

if t*100 < 10:
	plt.title('NACA ' + str(int(m*100)) + str(int(p*10)) + "0" + str(int(t*100)) + '\n')
else:
	plt.title('NACA ' + str(int(m*100)) + str(int(p*10)) + str(int(t*100)) + '\n')
plt.xlim(0 - (0.1*c), c + (0.1*c))
plt.ylim(min(y_down) - (0.2*t), max(y_up) + (0.2*t))
plt.xlabel('chord')
plt.ylabel('chord %')
ax.set_aspect('equal', 'datalim')

plt.show()

#################################

fig = plt.figure()
ax = fig.add_subplot(111)

plt.plot(X, camber)
plot_up = plt.plot(x_up, y_up)
plt.plot(x_down, y_down)
plt.grid()
 
for i in range(0, len(normals0)):
	plt.plot([centers_x[i], centers_x[i] + (normals0[i] * x_matrix[i])], [centers_y[i], centers_y[i] + (normals1[i] * x_matrix[i])], color = colors(abs(x_matrix[i]), max([max(x_matrix), abs(min(x_matrix))])), linewidth = 2.0)

if t*100 < 10:
	plt.title('NACA ' + str(int(m*100)) + str(int(p*10)) + "0" + str(int(t*100)) + '\n')
else:
	plt.title('NACA ' + str(int(m*100)) + str(int(p*10)) + str(int(t*100)) + '\n')
plt.xlim(0 - (0.1*c), c + (0.1*c))
plt.ylim(min(y_down) - (0.2*t), max(y_up) + (0.2*t))
plt.xlabel('chord')
plt.ylabel('chord %')
ax.set_aspect('equal', 'datalim')

plt.show()
