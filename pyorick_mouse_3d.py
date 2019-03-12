# pyorick_mouse_3d.py
# 3d demo program of idlp function, written by Hiroshi C. Ito. 2019
# execution command at console:
# python3 -i pyorick_mouse_3d.py

from idl_pyorick import * 

def myexec(com):
    exec(com)


T=2000
dt=-0.02

yo=Yorick()
yo.c.include("~/Yorick/custom.i")

yo.c.win2()

idlp_init(yo,frame_interval=4,flag_animate=1,flag_frame_out=0,flag_auto_start=0,pal="br")

col_cont="red"
x, y = mgrid[-3:3:32j, -3:3:32j]
z= sin(2*sqrt(x*x+y*y))+cos(x+y)

yo.c.window(0)
yo.c.win3()
yo.c.setz3(20)

yo.c.plwf(z,y,x,shade=1,edges=1,ecolor="green",scale=1.5)

yo.c.orient3()
yo.c.limit3,-3,3,-3,3,-6,6;
yo.c.cage3(1)
yo.c.limits()
yo.c.scale(0.85)

start_animation(yo)

for t in range(0,T):
    z= sin(2*sqrt(x*x+y*y)+0.02*4*t)+cos(x+y+0.013*4*t)
     
    yo.c.window(0)
 
    yo.v.z=z
    yo.v.y=y
    yo.v.x=x
    yo("plwf,z,y,x,shade=1,edges=1,ecolor=green,scale=1.5;limit3,-3,3,-3,3,-6,6;")    
 
    frame_out(yo,t)

    if(idlp(yo,0.0,t,myexec)):
        break

yo.c.window(0)
end_animation(yo)

##    movie_encode()
    
