from math import sqrt

G=6.67428*10**(-11)
M_sol=1.9890*10**30
M_tierra=5.97242*10**24

X=1.496*10**11
y=0
vx=0
vy=29.783*10**3
dt=3600*10**24
T_total=3.154*10**7
N_pasos=T_total/dt

xs=[]
ys=[]
velsx=[]
velsy=[]

def calcular_aceleracion(x,y):
    r=sqrt(x**2+y**2)
    a_mag=-1*G*M_sol*(1/(r**2))

    ax=a_mag*(x/r)
    ay=a_mag*(y/r)

    return ax,ay




