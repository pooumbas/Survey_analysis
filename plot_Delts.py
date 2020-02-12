import numpy as np
import matplotlib.pyplot as plt
import json
import os
import numpy as np

def get_files(new_dir, surveys):
    all_files=os.listdir(new_dir)
    files=[]
    os.chdir(new_dir)
    print()
    for ii in all_files:
        file_name, file_ext=os.path.splitext(ii)
        if file_ext=='.json' and ii in surveys:
            files.append(ii)
    file_input(files)

def file_input(files):
    num=0
    for ii in files:
        num+=1
        get_delts(ii)
def get_delts(file):
    delts=[]
    count=0
    counts=[]
    device=''
    with open (file) as r:
        for ii in r:
            a=json.loads(ii)
            eps=a['LeInput']['DeltaTime']
            delts.append(eps)
            count+=1
            counts.append(count)
            device=a['LeInput']['EpRequest']['Device']['OS']
    print(device)
    plot_delts(delts, counts, count, device)
def get_metrics(delts):
    STD=np.std(delts)
    Mean=np.mean(delts)
    return (STD, Mean)
def plot_delts(delts, counts, count, device):
    metrics=get_metrics(delts)
    plt.scatter(counts, delts)
    # plt.legend('Stadard Dev: {}, Mean : {}' .format(metrics[0], metrics[1])
    plt.show()
    
    
    
