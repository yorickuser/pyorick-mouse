# pyorick_mouse_2d.py
# 2d demo program of idlp function, written by Hiroshi C. Ito. 2019
# execution command at console:
# python3 -i pyorick_mouse_2d.py


from idl_pyorick import *

def myexec(com):
    exec(com)
 
        
T=2000
dt=-0.02

yo=Yorick()
yo.c.include("~/Yorick/custom.i")
yo.c.win2()

idlp_init(yo,frame_interval=4,flag_animate=1,flag_frame_out=0,flag_auto_start=0,flag_2d=1,pal="br")

col_cont="green"
nlevs=15
x, y = mgrid[-3:3:64j, -3:3:64j]
z= sin(2*sqrt(x*x+y*y))+cos(x+y)
levs=linspace(-1.5,1.5,nlevs)

yo.c.window(0)
start_animation(yo)

for t in range(0,T):
    z= sin(2*sqrt(x*x+y*y)+0.02*t)+cos(x+y+0.013*t)
    levs=linspace(-1.5,1.5,nlevs)
    yo.c.window(0)
    yo.c.draw3_trigger()
    
    yo.c.fma;
    yo.c.plfc(z,y,x,levs=levs)
    yo.c.plc(z,y,x,color=col_cont,levs=levs)
    ##yo.c.limits(-3,3,-3,3)
    
    frame_out(yo,t)

    if(idlp(yo,0.0,t,myexec)):
        break

yo.c.window(0)
end_animation(yo)

##    movie_encode()
    
