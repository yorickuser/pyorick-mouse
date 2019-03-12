# idl_pyorick.py
# Functions for for event-driven programing, written by Hiroshi C. Ito. 2019

from pyorick import * 
from numpy import *
from subprocess import getoutput
import time



def calc_orilims(yo):
    yo.v.orilim=get_lim(yo,1,1)
    orilim2=get_lim(yo,1,2)
    orilim3=get_lim(yo,1,3)
    orilim4=get_lim(yo,1,4)
    yo.v.orilims = [orilim2,orilim3,orilim4]

def calc_orilim(yo):    
    yo.v.orilim=get_lim(yo,1,1)

def start_animation(yo):
    calc_orilims(yo)
    set_sys(yo,0,1)
    yo.c.animate(1)

def end_animation(yo):
    set_sys(yo,0,1)
    yo.c.animate(0)
    
def get_lim(yo,nwin,isys):
    buf_sys=yo.e.plsys()
    buf_win=yo.e.current_window()
    yo.c.window(nwin)
    yo.c.plsys(isys)
    olim=yo.e.limits()
    
    yo.c.window(buf_win)
    yo.c.plsys(buf_sys)
    return olim

def set_sys(yo,nwin,isys):
    yo.c.window(nwin)
    yo.c.plsys(isys)


def get_sys(yo):
    return yo.e.plsys(),yo.e.current_window()

def set_lim(yo,nwin,isys,lim0):
    buf_sys,buf_win=get_sys(yo)
    set_sys(yo,nwin,isys)
    yo.c.limits(lim0)    
    set_sys(yo,buf_win,buf_sys)

def reset_lim(yo,nwin,isys):
    buf_sys,buf_win=get_sys(yo)
    set_sys(yo,nwin,isys)
    yo.c.limits()    
    set_sys(yo,buf_win,buf_sys)


def push_but(yo,nwin,isys,olim):
    buf_sys,buf_win=get_sys(yo)
    set_sys(yo,nwin,isys)
    nlim=yo.e.limits()
    butt=0
    direx=0
    direy=0
    xs=olim[0]
    xe=olim[1]
    ys=olim[2]
    ye=olim[3]
    xs1=nlim[0]
    xe1=nlim[1]
    ys1=nlim[2]
    ye1=nlim[3]
    xpos=0.0;
    ypos=0.0
    zfac=1.0
    xpos=0.5*(xs+xe)
    ypos=0.5*(ys+ye)
    if (xe1-xs1)>1.1*(xe-xs) or (ye1-ys1>1.1*(ye-ys)):
        butt=2
        zfac=1.5
        xpos=((xs1+xe1)-zfac*(xs+xe))/(2.0*(1-zfac))
        ypos=((ys1+ye1)-zfac*(ys+ye))/(2.0*(1-zfac))

    if (xe1-xs1)<0.9*(xe-xs) or (ye1-ys1<0.9*(ye-ys)):
        butt=1
        zfac=1.0/1.5 
        xpos=((xs1+xe1)-zfac*(xs+xe))/(2.0*(1-zfac))
        ypos=((ys1+ye1)-zfac*(ys+ye))/(2.0*(1-zfac))

    direx=-1*((nlim[1]+nlim[0])-(olim[1]+olim[0]))/(olim[1]-olim[0])
    direy=-1*((nlim[3]+nlim[2])-(olim[3]+olim[2]))/(olim[3]-olim[2])
    set_sys(yo,buf_win,buf_sys)

    return [butt,direx,direy,xpos,ypos]


def control_rotation(yo,orilim2,orig,myexec):
    butt2=push_but(yo,1,2,orilim2)
    if(int(butt2[0])==1):
        if yo.v.flag_2d==0:
            print("rotation")
            set_lim(yo,1,2,orilim2)
            yo.c.redraw()
            
            yo.c.window(0)
            if(butt2[2]*butt2[2]<0.000001):
                yo.c.rot3_ho(0,0,butt2[1]*-1.0)
                print("about Z-axis")
            else:
                yo.c.rot3(butt2[2]*1.0,butt2[1]*-1.0)
                yo.c.redraw()
                set_sys(yo,1,1)
        else:
            yo.c.window(0)
            if butt2[2]>0:
                yo.c.scale(0.9)
            else:
                yo.c.scale(1.1)
            calc_orilims(yo)
            
            
    if(int(butt2[0])==2):
        if yo.v.flag_2d==0:
            print("reset rotation")
            set_lim(yo,1,2,orilim2)
            yo.c.redraw()
            yo.c.window(0)
            yo.c.restore3(orig)
            yo.c.redraw()
            set_sys(yo,1,1)
        else:
            print("reset scaling")
            yo.c.window(0)
            yo.c.limits()
            set_sys(yo,1,1)
            calc_orilims(yo)
            
            
def control_color(yo,orilim4,orig,myexec):
    butt4=push_but(yo,1,4,orilim4)
    if(int(butt4[0])>0):
        set_lim(yo,1,4,orilim4)
        set_sys(yo,0,1)
    
        if(int(butt4[0])==1):
            print("sys4 button1")
            yo.c.idl_change_pal(1)
        if(int(butt4[0])==2):
            print("sys4 button2")
            yo.c.idl_change_pal(-1)
            
        set_sys(yo,1,4)
        yo("palname_cur=pals(idl_pal_id);pal,palname_cur;")
        
        yo.c.fma()
        plot_control(yo)
        
        
def frame_out(yo,t):
    if yo.v.flag_frame_out==1:
        if(t%yo.v.frame_interval==0):
            tt=yo.v.frame_count
            yo.v.bb="%s%d%d%d%d%s" % ('frame',tt%10000/1000,tt%1000/100,tt%100/10,tt%10,'.png')
            yo("png2,bb")
            yo.v.frame_count = tt+1
            print(yo.v.bb)
            
def movie_encode(filename="movie_out.mp4"):
    print('encoding...')
    
    check = getoutput("ffmpeg -y  -i frame%04d.png -b:v 1000000  -vcodec libx264 -qscale 0 "+filename)
    print(check);
    print("output movie file:")
    print(filename)


def plot_control_rotation(yo):
    set_sys(yo,1,2)
    yo("plg,[-1,1],[0,0],color=\"fg\";plg,[0,0],[-1,1],color=\"fg\";limits;")
    ##yo.c.plt("Rotation",0.27,0.77,orient=1,tosys=0,color="fg",justify="RH",height=16)
    yo.c.plt("Rotation",0.36,0.81,tosys=0,height=14,color="fg",justify="CH")

def plot_control_color(yo):
    set_sys(yo,1,4)
  
    x, y = mgrid[-1:1:2j, -1:1:240j]  
    yo("plfp,[char([200,200,200])],3*[-1,-1,1,1],3*[-1,1,1,-1],[4]")
    yo.c.plf(y,y,x)
    yo.c.plg([-1,1,1,-1],[1,1,-1,-1], closed=1,marks=0,color="fg",width=1,type=1)

    yo.c.limits(-1.5,1.5,-1.1,1.1)    
    yo.c.plt("Palette",0.49,0.82,tosys=0,height=14,color="fg",justify="CC")
    yo.c.plt(yo.v.pals[yo.v.idl_pal_id-1],0.49,0.65,tosys=0,height=14,color="fg",justify="CC")


def plot_control_command(yo):
    set_sys(yo,1,3)
    if(yo.v.command_mode==0):

        yo("plfp,[char([240,240,200])],10*[-1,-1,1,1],10*[-1,1,1,-1],[4];limits,-1,1,-1,1;")
        yo.c.plt("Command",0.487,0.725-0.18,orient=1,tosys=0,height=14,color="blue",justify="CH")
    else:
        yo("plfp,[char([200,0,0])],10*[-1,-1,1,1],10*[-1,1,1,-1],[4];limits,-1,1,-1,1;")
        yo.c.plt("Command mode",0.487,0.725-0.18,orient=1,tosys=0,height=14,color="white",justify="CH")
     

    if(yo.v.flag_frame_out==1):    
        yo.c.plt("Frame-out ON",0.52,0.72-0.18,orient=1,tosys=0,color="red",justify="CH",height=12)   
    else:
        yo.c.plt("Frame-out OFF",0.52,0.72-0.18,orient=1,tosys=0,color="black",justify="CH",height=12)   

      
def plot_control_run(yo):    
    set_sys(yo,1,1)

    yo("plfp,[char([240,240,200])],5*[-1,-1,1,1],5*[-1,1,1,-1],[4];");
    if(yo.v.stop==0):
        
        yo.c.plt("Stop",0.36,0.55,height=18,tosys=0,justify="CH",color="red")
  
        time.sleep(0.0001)
       
    else:
        yo.c.plt("Start: left\n End: right",0.36,0.55,height=18,tosys=0,justify="CH",color="blue")
  
        time.sleep(0.0001)


def control_command(yo,orilim3,orig,myexec):
    butt3=push_but(yo,1,3,orilim3)
    if(int(butt3[0])==2):
        ##print("sys3 button2")
        
        set_lim(yo,1,3,orilim3)
        if(yo.v.flag_frame_out==1):
            yo.v.flag_frame_out=0
            print("frame-out OFF")
        else:
            yo.v.flag_frame_out=1
            print("frame-out ON")
        plot_control(yo)
        
    if(int(butt3[0])==1):
        yo.c.animate(0)
        yo.v.command_mode=1
        plot_control(yo)
        ##print("sys3 button1")
        print("Enter command: ")
        set_sys(yo,0,1)
        
        while True:
            com=input("->> ")
            if com == "exit":
                print("Exited from command-input")
                yo.v.command_mode=0
                break
            else:
                try:
                    myexec(com)
                except NameError:
                    print('undefined name')
                except ZeroDivisionError:
                    print('division by zero')
                except:
                    print('something else went wrong')
       ## yo.v.command_mode=myexec()
                    
        plot_control(yo)
        if yo.v.flag_animate==1:
            yo.c.animate(1)



def plot_control(yo):
    orilim0=get_lim(yo,1,1)
    posx=yo.v.posx
    mixpp=yo.v.mixpal
    yo.c.window(1)
    yo.c.fma()   
    plot_control_command(yo)
    plot_control_color(yo)
    plot_control_rotation(yo)
    plot_control_run(yo)

    set_lim(yo,1,1,orilim0)
    yo.c.redraw() 
    set_sys(yo,0,1)

def idlp_init(yo,frame_interval=2,flag_animate=1,flag_frame_out=0,flag_auto_start=0,flag_2d=0,pal="sunrise"):
    yo.c.win2((200+60),(300+60),n=1,offset_h=-10,offset_w=-20,axis=7,div_ratio=0.75,div_ratio1=0.5,div_margin=40)
    yo.v.frame_interval=1
    yo.v.command_mode=0
    yo.v.flag_animate=1
    set_sys(yo,0,1)
    yo.c.pal(pal)
    set_sys(yo,1,3)
    yo.c.pal(pal)
    yo("idl_init_pal")
    yo.v.flag_frame_out=flag_frame_out
    yo.v.flag_auto_start=flag_auto_start
    yo.v.flag_2d=flag_2d
    yo.v.stop=1
    yo.v.frame_count=0
    plot_control(yo)
    time.sleep(0.05)





def idlp(yo,idl_sleep,t,myexec,control_funcs=0):
    orilim=yo.v.orilim
    orilims=yo.v.orilims
    if control_funcs==0:
        control_funcs=[control_rotation,control_command,control_color]
        
    flag_halt=0
    nfunc=len(control_funcs)
    if(idl_sleep>0):
        time.sleep(idl_sleep)

    set_sys(yo,0,1)
    rgb=yo.e.rgb_read()            
    orig=yo.e.save3()
    set_sys(yo,1,1)

    for ii in range(0,nfunc):
        control_funcs[ii](yo,orilims[ii],orig,myexec)


    set_sys(yo,1,1)
 
    
    rgb=yo.e.rgb_read()            
    butt=push_but(yo,1,1,orilim)
    if(butt[0]==2):
        set_sys(yo,0,1)
        yo.c.orient3()
    
    if (butt[0]==1 or (t==0 and yo.v.flag_auto_start==0)):
   
        orilim=get_lim(yo,1,1)
        print(yo.e.swrite(t,format="stop:%d"))
        yo.v.stop=1
        set_sys(yo,1,1)
        yo.c.fma();
        plot_control(yo)
        
        set_lim(yo,1,1,orilim)
    
        yo.c.window(0)
        yo.c.animate(0)
        ##time.sleep(0.01)
        yo.c.redraw()
        set_sys(yo,1,1)
        
        
        while (1):

            time.sleep(0.01)
            rgb=yo.e.rgb_read()            
            butt=push_but(yo,1,1,orilim)
            if(butt[0]==1):
                ##set_lim(yo,1,1,orilim)
                yo.c.window(0)
                if yo.v.flag_animate==1:
                    yo.c.animate(1)
                yo.c.window(1)
                yo.v.stop=0
                plot_control(yo)
          
                break

                
            for ii in range(0,nfunc):
                control_funcs[ii](yo,orilims[ii],orig,myexec)

            orilims=yo.v.orilims
          
            if(butt[0]==2):
                flag_halt=1
                orilim=get_lim(yo,1,1)
                break

        if(flag_halt==1):
            print("end")
            set_lim(yo,1,1,orilim)
            return 1
        else:
            set_lim(yo,1,1,orilim)
            calc_orilim(yo)
            return 0



