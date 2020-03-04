file='mist_sdkmist_sdk_logs.log'

data={"add-sensor":[], "send return":[], "basic":[],"send":[],"dr":[],}


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
    last=0
    for ii in listo:
        for key in data:
            if ii==key:
                decimal = get_decimal(listo, ii)
                if ii=='basic:':
                    last=0
                    value=decimal
                    last=value
                else:
                    value = decimal - last
                    last = decimal
                append_dict(value, key)
                break
            print(last)
def append_dict(value, key):
    data[key].append(value)

def adding_frame(ii, decimal):
    if ii=='basic':
        last=0
    else:
        last=decimal
    return last


def get_decimal(listo,ii):
    dex = len(listo) - 1
    decimal = listo[dex]
    decimal_dex=len(decimal)-2
    decimal=float(decimal[:decimal_dex])
    return decimal

if __name__=="__main__":
    initiate()
    print(data['dr'])





