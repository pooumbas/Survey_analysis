import os
import time as tm
import shutil
import plots as sp

homedir = os.path.expanduser("~")
path=('{}/desktop/new_surveys/'.format(homedir))
time=tm.time()
def get_files(time):
    epsilon=10000
    os.chdir('{}/downloads'.format(homedir))
    surveys=[]
    size=input('Input Survey Count: ')
    while True:
        os.chdir('{}/downloads'.format(homedir))
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
      os.chdir('{}/downloads'.format(homedir))
      temp=path
      print('Moving{}'.format(surveys))
      print('Current Path: {}' .format(path))
      new_path=input('Move Surveys to a New Path? y/n: ')
      if new_path=='y':
          path=new_dir()+"/"
          print(path)
      else:
          path=input('Enter Path or Type: current: ')
          path=path.strip(" ")
      if path=='current':
          path=temp
      else:
          path=path+'/'
      for ii in surveys:
          print(ii)
          os.rename(ii, path+ ii)
      sp.get_files(path, surveys) 
def new_dir():
    new_path=input('Enter a New Path')
    new_path=new_path.strip(" ")
    os.mkdir(new_path)
    shutil.copy('{}/survey_plotter.py'.format(homedir), '{}/survey_plotter.py'.format(new_path))
    return new_path

if __name__=='__main__':
      get_files(time)