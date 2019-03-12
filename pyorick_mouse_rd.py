# pyorick_mouse_rd.py
# 2d demo program (gray-scott reaction diffucion model) of idlp function,
# written by Hiroshi C. Ito. 2019
# execution command at console:
# python3 -i pyorick_mouse_rd.py

from idl_pyorick import *

def comloop():
    command_mode=1
    while True:
        com=input("->> ")
        if com == "exit":
            print("Exited from command-input")
            command_mode=0
            break
        else:
            try:
                exec(com)
            except NameError:
                print('undefined name')
            except ZeroDivisionError:
                print('division by zero')
            except:
                print('something else went wrong')
    return command_mode



yo=Yorick()
size = 100
gridx, gridy = meshgrid(linspace(0,1,size),linspace(0,1,size))
yo.v.size=size

dif_gridx, dif_gridy =meshgrid(linspace(0.3,2.0,size),linspace(0.3,2.0,size))

dt =0.2
ncal=100
count_interval=10
a = 0.023
b = 0.055


dif_rate_x = (8.0e-2)*dif_gridx
dif_rate_y = (4.6e-2)*dif_gridy

x=gridx*0+1.0
y=gridy*0+0.001
y[int(size/2),int(size/3)] = 0.5;
diffuse_mask=hstack((array([0]),array(range(size)),array([size-1])));

yo("x=array(1.0,size,size);y=array(0.001,size,size);y(size/2,size/3) = 0.5;diffuse_mask=grow(1,indgen(size),size);")
        
T=2000


yo.c.include("~/Yorick/custom.i")
yo.c.win2()

idlp_init(yo,frame_interval=4,flag_animate=1,flag_frame_out=0,flag_auto_start=0,flag_2d=1,pal="cr")

nlevs=20
levs=geomspace(0.05,0.6,nlevs)

yo.c.window(0)

yo.c.fma()
yo.c.plfc(y,gridy,gridx,levs=levs)
yo.c.xyt("Diffusion rate for x", "Diffusion rate for y")
yo.c.limits()


start_animation(yo)


for t in range(0,T):

    
    for k in range (1,ncal):
        diffuse_x=yo.v.diffuse_x
        diffuse_y=yo.v.diffuse_y
        diffuse_x=diff(x[:,diffuse_mask],n=2,axis=1)+diff(x[diffuse_mask,:],n=2,axis=0)

        diffuse_y=diff(y[:,diffuse_mask],n=2,axis=1)+diff(y[diffuse_mask,:],n=2,axis=0)
   
        x += dt*(-1.0*x*y*y + a*(1.0-x) +dif_rate_x*diffuse_x);
        y += dt*(x*y*y - (a+b)*y+dif_rate_y*diffuse_y);
    
    if t%count_interval==0:
        print(t*ncal)

    yo.c.window(0)
    yo.c.draw3_trigger()
        
    
    yo.c.plfc(y,gridy,gridx,levs=levs)

    yo.c.xyt("Diffusion rate for x", "Diffusion rate for y")
    yo.c.redraw()
    
    frame_out(yo,t)

    if(idlp(yo,0.0,t,comloop)):
        break

yo.c.window(0)
end_animation(yo)

##    movie_encode()
    
