import numpy as np
import matplotlib.pyplot as plt
import json
import os

off=False
plot_path_global=None
view_plots=False

def get_plot_path():
    
    global off 
    global plot_path_global
    global view_plots
    
    if off==False:
        view=input('View Plots Now?  y/n: ')
        if view=='y':
            view_plots=True 
        print('Save Plots')
        plot_path=input('Enter Existing Path or Type current: ')
        plot_path=plot_path.strip(" ")
        if plot_path=='current':
            plot_path=os.getcwd()
        off=True
        print(off)
        plot_path_global=plot_path
    else:
        plot_path=plot_path_global
    return plot_path

def get_files(new_dir, surveys, x=None):
    all_files=os.listdir(new_dir)
    files=[]
    os.chdir(new_dir)
    print()
    for ii in all_files:
        file_name, file_ext=os.path.splitext(ii)
        if file_ext=='.json' and ii in surveys:
            files.append(ii)
    file_input(files, x)

def file_input(files, x):
    num=0
    if x==None:
        for ii in files:
            num+=1
            get_xy(ii,num)
            get_sensor_xy(ii,num)
    else:
        get_xy(files[x-1], x)
            

def get_xy(file,num):
    x=[]
    y=[]
    X1,Y1,X2,Y2=0,0,0,0
    interpolatedX=[]
    interpolatedY=[]
    switch=False
    delta=0
    deltacount=0
    with open (file) as r:
        for ii in r:
            a=json.loads(ii)
            ys=(-a['LeInput']["EpRequest"]["LocationEstimates"]["Client"]['Snapped']["Y"])
            xs=a['LeInput']["EpRequest"]["LocationEstimates"]["Client"]['Snapped']["X"]
            x1=a['StaticX']
            y1=(-a['StaticY'])
            if switch==True:
                delta+=a['LeInput']['DeltaTime']
                deltacount+=1
            if x1!=0 and y1!=0 and switch==False:
                X1=x1
                Y1=y1
                switch=True
            if switch==True and x1!=X1 or y1!=Y1:
                X2=x1
                Y2=y1
                if X2!=0:
                    interpolation=interpolate(X1,X2,Y1,Y2,delta)
                    interpolatedX.extend(interpolation[0])
                    interpolatedY.extend(interpolation[1])
                    delta=0
                    Y1=y1
                    X1=x1
            if xs!=0:
                x.append(xs)
            if ys!=0:
                y.append(ys)
        plot_xy(interpolatedX,interpolatedY,num, x,y )
        compare_error(interpolatedX, interpolatedY, x,y)
        
def get_sensor_xy(file,num):
    x=[]
    y=[]
    with open (file) as r:
        for ii in r:
            a=json.loads(ii)
            ys=(-a['LeInput']["EpRequest"]["LocEst"][3]['Point']["Y"])
            xs=a['LeInput']["EpRequest"]["LocEst"][3]['Point']["X"]
            if xs!=0:
                x.append(xs)
            if ys!=0:
                y.append(ys)
        plot_xy(x,y,num)
def compare_error(interx, intery, x,y):
    if len(x)==len(interx):
        print('Interpolated values are Equal')


def interpolate(X1,X2,Y1,Y2,delta):
    deltax=(X2-X1)
    deltay=(Y2-Y1)
    delta=int(delta/1000)
    X_array=[X1]
    Y_array=[Y1]
    index=0
    for ii in range(delta):
        nextx=X_array[index]+(deltax/delta)
        nexty=Y_array[index]+(deltay/delta)
        X_array.append(nextx)
        Y_array.append(nexty)
        index+=1
    X_array.append(X2)
    Y_array.append(Y2)
    returns=[X_array, Y_array]
    return returns

def check_overwrite(save_name):
    dirs=os.listdir()
    if save_name in dirs:
        return False
    return True


def plot_xy(x,y,num, xe=None,ye=None):
    plot_path=get_plot_path()
    if xe!=None:
        name='Particle'+str(num)
        plt.title('Particle vs. Actual X,Y')
        plt.scatter(xe,(ye),label='Snapped Particle Filter')
        plt.scatter(x,(y),label='Actual Path')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()
        save_name='{}/{}.png'.format(plot_path,name)
        if check_overwrite(name+".png")==True:
            print('Saving PF Plots to {}...'.format(plot_path))
            plt.savefig(save_name)
        else:
            print('Saving PF Plots to {}...'.format(plot_path))
            file_name, file_ext=os.path.splitext(save_name)
            save_name=file_name+"0"+file_ext
            plt.savefig(save_name)
        if view_plots==True:
            plt.show()
        
    else:
        name='Sensor'+str(num)
        plt.title('Sensor X,Y')
        plt.scatter(x,(y),label='Sensors')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()
        save_name='{}/{}.png'.format(plot_path,name)
        if check_overwrite(name+".png")==True:
            print('Saving Sensor Plots to {}...'.format(plot_path))
            plt.savefig(save_name)
        else:
            print('Saving Sensor Plots to {}...'.format(plot_path))
            file_name, file_ext=os.path.splitext(save_name)
            save_name=file_name+"0"+file_ext
            plt.savefig(save_name)
        if view_plots==True:
            plt.show()
      
        
if __name__=='__main__':
    get_files()
