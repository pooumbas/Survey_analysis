file='mist_sdkmist_sdk_logs.log'

data={"add-sensor":[], "send return":[], "basic":[],"send":[],"dr":[],}
last = []

def make_list(ii):
    if 'return' in ii:
        listo=ii.split(" ")
        listo[4:6]=[' '.join(listo[4:6])]
    else:
        listo=ii.split(" ")
    return listo



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
                decimal = (get_decimal(listo, ii))*10000
                decimal=int(decimal)
                if len(last)==0:
                    last.append(decimal)
                else:
                    if ii=='basic:':
                        value=(decimal)
                        last.append(value)
                    else:
                        index = len(last)-1
                        value = (decimal - last[index])
                        last.append(value)
                    append_dict(value, key)
                break


def append_dict(value, key):
    data[key].append(value)


def get_decimal(listo,ii):
    dex = len(listo) - 1
    decimal = listo[dex]
    decimal_dex=len(decimal)-2
    decimal=float(decimal[:decimal_dex])
    return decimal


if __name__=="__main__":
    initiate()
    print(data)
    print(last)





