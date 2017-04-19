from matplotlib import cm
import matplotlib.pyplot as plt
import numpy

nx = 11
ny = 11
time = 1
cfl = 0.01
dx = 1/(nx-1)
dy = 1/(ny-1)

dt = cfl * dx / 2

nt = int(time / dt)
nit = 3

rho = 1
nu = 1

Re = 1 / nu

print("nt", nt)
print("dt", dt)
print("Re", Re)

x = numpy.linspace(0, 1, nx)
y = numpy.linspace(0, 1, ny)
X, Y = numpy.meshgrid(x, y)

u = numpy.zeros((ny, nx))
v = numpy.zeros((ny, nx))
p = numpy.zeros((ny, nx)) 
b = numpy.zeros((ny, nx))

def buildUpB(b, rho, dt, u, v, dx, dy):
    b[1:-1,1:-1]=rho*(1/dt*((u[1:-1,2:]-u[1:-1,0:-2])/(2*dx)+(v[2:,1:-1]-v[0:-2,1:-1])/(2*dy))-\
                      ((u[1:-1,2:]-u[1:-1,0:-2])/(2*dx))**2-\
                      2*((u[2:,1:-1]-u[0:-2,1:-1])/(2*dy)*(v[1:-1,2:]-v[1:-1,0:-2])/(2*dx))-\
                      ((v[2:,1:-1]-v[0:-2,1:-1])/(2*dy))**2)
    return b

def presPoisson(p, dx, dy, b):
    pn = numpy.empty_like(p)
    pn = p.copy()    
    for q in range(nit):
        pn = p.copy()
        p[1:-1,1:-1] = ((pn[1:-1,2:]+pn[1:-1,0:-2])*dy**2+(pn[2:,1:-1]+pn[0:-2,1:-1])*dx**2)/\
                        (2*(dx**2+dy**2)) -\
                        dx**2*dy**2/(2*(dx**2+dy**2))*b[1:-1,1:-1]

        p[:,-1] =p[:,-2] ##dp/dy = 0 at x = 2
        p[0,0] = 0
        p[0,:] = p[1,:]  ##dp/dy = 0 at y = 0
        p[:,0]=p[:,1]    ##dp/dx = 0 at x = 0
        p[0,1:] = p[1,1:]
        #p[-1,:]=0        ##p = 0 at y = 2
        
    return p

def max_check(check, value):
    if check > value:
        return check
    else:
        return value

def residuals(new_mat, old_mat):
    max_value = 0
    for i in range(len(new_mat)):
        for j in range(len(new_mat[i])):
            max_value = max_check(new_mat[i][j] - old_mat[i][j], max_value)
    return(max_value)

def cavityFlow(nt, u, v, dt, dx, dy, p, rho, nu):
    un = numpy.empty_like(u)
    vn = numpy.empty_like(v)
    b = numpy.zeros((ny, nx))
    
    u_res = []
    v_res = []
    p_res = []
    
    for n in range(nt):

        un = u.copy()
        vn = v.copy()
        
        b = buildUpB(b, rho, dt, u, v, dx, dy)
        pn = numpy.empty_like(p)
        pn = p.copy()
        p = presPoisson(p, dx, dy, b)
        
        u[1:-1,1:-1] = un[1:-1,1:-1]-\
                        un[1:-1,1:-1]*dt/dx*(un[1:-1,1:-1]-un[1:-1,0:-2])-\
                        vn[1:-1,1:-1]*dt/dy*(un[1:-1,1:-1]-un[0:-2,1:-1])-\
                        dt/(2*rho*dx)*(p[1:-1,2:]-p[1:-1,0:-2])+\
                        nu*(dt/dx**2*(un[1:-1,2:]-2*un[1:-1,1:-1]+un[1:-1,0:-2])+\
                        dt/dy**2*(un[2:,1:-1]-2*un[1:-1,1:-1]+un[0:-2,1:-1]))

        v[1:-1,1:-1] = vn[1:-1,1:-1]-\
                        un[1:-1,1:-1]*dt/dx*(vn[1:-1,1:-1]-vn[1:-1,0:-2])-\
                        vn[1:-1,1:-1]*dt/dy*(vn[1:-1,1:-1]-vn[0:-2,1:-1])-\
                        dt/(2*rho*dy)*(p[2:,1:-1]-p[0:-2,1:-1])+\
                        nu*(dt/dx**2*(vn[1:-1,2:]-2*vn[1:-1,1:-1]+vn[1:-1,0:-2])+\
                        (dt/dy**2*(vn[2:,1:-1]-2*vn[1:-1,1:-1]+vn[0:-2,1:-1])))

        u[0,:] = 0
        u[:,0] = 0
        u[:,-1] = 0
        u[-1,:] = 1    #set velocity on cavity lid equal to 1
        v[0,:] = 0
        v[-1,:]=0
        v[:,0] = 0
        v[:,-1] = 0
        
        if n % int(nt / 10) == 0:
            print(n*10 / int(nt / 10))
        
        u_res.append(residuals(u, un))
        v_res.append(residuals(v, vn))
        p_res.append(residuals(p, pn))
        
    return u, v, p, u_res, v_res, p_res 

u, v, p, u_res, v_res, p_res = cavityFlow(nt, u, v, dt, dx, dy, p, rho, nu)

u_prof = u[: , int(len(u)/2)]
v_prof = v[int(len(v)/2), :]
xs = [i for i in range(len(u_prof))]
plt.plot(v_prof, xs)
plt.show()

"""
xs = [i for i in range(len(u_res))]
plt.plot(xs, u_res, label = "u")
plt.plot(xs, v_res, label = "v")
plt.plot(xs, p_res, label = "p")
plt.yscale("log")
plt.legend()
plt.show()
"""

"""
plt.streamplot(X, Y, u, v, color = u, linewidth = 1, cmap = plt.cm.jet)
plt.colorbar()

plt.show()
"""

"""
fig = plt.figure(figsize=(11,7), dpi=100)
plt.contourf(X,Y,p,alpha=0.5)    ###plnttong the pressure field as a contour
plt.colorbar()
plt.contour(X,Y,p)               ###plotting the pressure field outlines
plt.quiver(X[::2,::2],Y[::2,::2],u[::2,::2],v[::2,::2]) ##plotting velocity
plt.xlabel('X')
plt.ylabel('Y')
plt.show()
"""
