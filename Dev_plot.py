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
            off = True
    plot_path = os.getcwd()
    return plot_path

def get_files(new_dir, surveys, x=None):
    all_files=os.listdir(new_dir)
    files=[]
    os.chdir(new_dir)
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
    one_secx=[]
    one_secy=[]
    switch=False
    delta=0
    one_sec=True
    switch2=False
    with open (file) as r:
        for ii in r:
            a=json.loads(ii)
            ys=(-a['LeInput']["EpRequest"]["LocationEstimates"]["Client"]['Snapped']["Y"])
            xs=a['LeInput']["EpRequest"]["LocationEstimates"]["Client"]['Snapped']["X"]
            secx=a['LeInput']['EpRequest']["LocEst"][2]['Point']['X']
            secy=a['LeInput']['EpRequest']["LocEst"][2]['Point']['Y']
            x1=a['StaticX']
            y1=(-a['StaticY'])
            if switch == True:
                delta += 1
            if x1!=0 and y1!=0 and switch==False:
                X1=x1
                Y1=y1
                switch=True
            if switch==True and x1!=X1 or y1!=Y1:
                X2=x1
                Y2=y1
                if X2!=0:
                    if switch2==False:
                        interpolation=interpolate(X1,X2,Y1,Y2,delta, switch2)
                        switch2=True
                    else:
                        interpolation = interpolate(X1, X2, Y1, Y2, delta, switch2)
                    interpolatedX.extend(interpolation[0])
                    interpolatedY.extend(interpolation[1])
                    check_points(interpolatedX,interpolatedY, x,y)
                    delta=0
                    Y1=y1
                    X1=x1
            if switch==True and xs!=0:
                x.append(xs)
                y.append(ys)
                one_secx.append(secx)
                one_secy.append(-secy)
        x,y=fix_arrays(interpolatedX,interpolatedY, x,y)
        plot_xy(interpolatedX,interpolatedY,num, x,y )
        check_points(interpolatedX,interpolatedY, x,y)
        plot_xy(interpolatedX,interpolatedY,num, one_secx, one_secy, one_sec)
        save_metrics(interpolatedX,interpolatedY,one_secx, one_secy,  x,y)

def save_metrics(interx, intery, onex, oney, pfx, pfy):
    second_mean, second_STD, three_meter_one=get_error(interx, intery, onex, oney)
    pfmean, pfSTD, three_meter_PF =get_error(interx, intery, pfx, pfy)
    metrics=['One Second Mean Error:', 'One Second STDV Error:', 'One Second Estimates > 3 Meter Error:', 'Particle Filter Mean:', 'Particle Filter STDV:','Particle Filter Estimates > 3 Meter Error:']
    metrics2=[ second_mean, second_STD,three_meter_one, pfmean, pfSTD,three_meter_PF]
    print('Saving Metrics To metrics.txt...')
    with open ('metrics.txt', 'w') as w:
        w.write('__________Error Metrics__________' + '\n' +'\n')
        index=0
        for ii in range(len(metrics)):
            w.write(str(metrics[index])+ " " + str(metrics2[index]) + '\n')
            index+=1

def get_error(interx,intery,measured_x, measured_y):
    index=0
    Error_array=[]
    for ii in range(len(interx)):
        leg1=abs(measured_x[index]-interx[index])
        leg2=abs(measured_y[index]-intery[index])
        diff=np.sqrt((leg1**2)+(leg2**2))
        Error_array.append(diff)
        index+=1
    count=0
    for ii in Error_array:
        if ii>3:
            count+=1
    return (np.mean(Error_array), np.std(Error_array), count)

def fix_arrays(interx, intery, x,y):
    if len(interx)==x:
        return (x,y)
    diff=len(x)-len(interx)
    end_index=len(x)-diff
    return (x[:end_index],y[:end_index])
        
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

def check_points(interx, intery, x,y):
    print(len(x))
    print(str(len(interx))+"interx")
    if len(x)==len(interx):
        print('Interpolated values are Equal')
    delta=abs(len(interx)-len(x))
    if delta<2:
        print('Interx Delta less than Two')

def fix_delta(delta):
    test=delta-int(delta)
    if test<.5:
        return (int(delta)-1)
    return int(delta)
       
def interpolate(X1,X2,Y1,Y2,delta, switch2):
    if switch2==False:
        delta=delta-3
    else:
        delta=delta-2
    deltax=(X2-X1)
    deltay=(Y2-Y1)
    X_array=[X1]
    Y_array=[Y1]
    index=0
    print(delta)
    for ii in range(delta):
        nextx=X_array[index]+(deltax/delta)
        nexty=Y_array[index]+(deltay/delta)
        X_array.append(nextx)
        Y_array.append(nexty)
        index+=1
    print(X_array)
    X_array.append(X2)
    Y_array.append(Y2)
    returns=[X_array, Y_array]
    return returns

def check_overwrite(save_name):
    dirs=os.listdir()
    if save_name in dirs:
        return False
    return True

def plot_xy(x,y,num, xe=None,ye=None, one_sec=False):
    plot_path=get_plot_path()
    if xe!=None and one_sec!=True:
        name='Particle'+str(num)
        plt.title('Particle vs. Actual X,Y')
        plt.scatter(xe,(ye),label='Snapped Particle Filter')
        plt.scatter(x,(y),label='Actual Path')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()
        save_name='{}/{}.png'.format(plot_path,name)
        boo=check_overwrite(name+".png")
        save_fig(boo, plot_path, save_name)
        if view_plots==True:
            plt.show()
        
    elif xe==None:
        name='Sensor'+str(num)
        plt.title('Sensor X,Y')
        plt.scatter(x,(y),label='Sensors')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()
        save_name='{}/{}.png'.format(plot_path,name)
        boo=check_overwrite(name+".png")
        save_fig(boo, plot_path, save_name)
        if view_plots==True:
            plt.show()
    else:
        name='One_Second'+str(num)
        boo=check_overwrite(name+".png")
        save_name='{}/{}.png'.format(plot_path,name)
        save_fig(boo,plot_path, save_name)
        plt.scatter(x,y,)
        plt.scatter(xe,ye)
        plt.title('One Second Estimate X,Y')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.show()

def check_overwrite(save_name):
    dirs=os.listdir()
    if save_name in dirs:
        return False
    return True

def save_fig(boo,plot_path, save_name):
    if boo==True:
        print('Saving Sensor Plots to {}...'.format(plot_path))
        print(plot_path)
        plt.savefig(save_name)
    else:
        print('Saving Sensor Plots to {}...'.format(plot_path))
        file_name, file_ext=os.path.splitext(save_name)
        save_name=file_name+"0"+file_ext
        plt.savefig(save_name)
        
if __name__=='__main__':
     get_files()
