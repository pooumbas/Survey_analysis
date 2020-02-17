import os
import time as tm
import shutil
import Dev_plot as sp

homedir = os.path.expanduser("~")
path=('{}/Survey_analysis/Data/'.format(homedir))
time=tm.time()
def get_files(time):
    epsilon=10000
    os.chdir('{}/Downloads'.format(homedir))
    surveys=[]
    size=input('Input Survey Count: ')
    while True:
        os.chdir('{}/Downloads'.format(homedir))
        dirs=os.listdir()
        for ii in dirs:
            file_name, file_extension= os.path.splitext(ii)
            if file_extension=='.json' and len(surveys)<int(size):
                download_time=os.stat(ii).st_mtime
                delta=time-download_time
                if delta<epsilon and ii not in surveys:
                    surveys.append(ii)
            if len(surveys)==int(size):
                move_files(surveys)
                surveys.clear()
                size=input('Input Survey Count: ')
                break
        tm.sleep(1)
def move_files(surveys, path=path):
      os.chdir('{}/Downloads'.format(homedir))
      temp=path
      print('Moving{}'.format(surveys))
      print('Current Path: {}' .format(path))
      for ii in surveys:
          print(path+ii)
          os.rename(ii, path + ii)
      sp.get_files(temp, surveys)
def new_dir():
    new_path=input('Enter a New Path')
    new_path=new_path.strip(" ")
    os.mkdir(new_path)
    shutil.copy('{}/survey_plotter.py'.format(homedir), '{}/survey_plotter.py'.format(new_path))
    return new_path

if __name__=='__main__':
      get_files(time)
