file='mist_sdkmist_sdk_logs.log'

data={"add-sensor":[], "send return":[], "basic":[],"send":[],"dr":[],}
last = []       
maxes={}
ep_req=0

def make_list(ii):
    if 'return' in ii:
        listo=ii.split(" ")
        listo[4:6]=[' '.join(listo[4:6])]
    else:
        listo=ii.split(" ")
    return listo



def get_data():
    initiate()
    find_max()
    print(maxes)
    


def initiate():
    with open (file) as logs:
        for ii in logs:
            if "benchmark" in ii:
                listo=make_list(ii)
                brute_list(listo)

def brute_list(listo):
    for ii in listo:
        for key in data:
            if ii==key:
                decimal = (get_decimal(listo, ii))
                sort_data(decimal,ii,key)
                break

def sort_data(decimal,ii,key):
    if len(last)==0:
        last.append(decimal)
    else:
        if ii=='basic':
            global ep_req
            ep_req+=1
            value=(decimal)
            last.append(decimal)
        else:
            index = len(last)-1
            value = (decimal - last[index])
            last.append(decimal)
        append_dict(value, key)



def append_dict(value, key):
    data[key].append(value)


def get_decimal(listo,ii):
    dex = len(listo) - 1
    decimal = listo[dex]
    decimal_dex=len(decimal)-2
    decimal=float(decimal[:decimal_dex])
    return decimal


def find_max():
    count=0
    for key in data:
        if key=='dr':
            for ii in data[key]:
                if ii>=.1:
                    count+=1
        maximum=max(data[key])
        maxes.update({key:maximum})
    print("{} EP_REQ's with >.1 Second Delay".format(count))
    print("{} EP_REQ's Total".format(ep_req))
        


if __name__=="__main__":
    get_data()
    






