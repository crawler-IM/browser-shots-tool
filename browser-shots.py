import sys, os, time, shutil, re
from time import strftime as date
import datetime
from pyvirtualdisplay import Display
from selenium import webdriver
import selenium.webdriver.chrome.service as chrome_service
import subprocess
from multiprocessing import Process, Queue
import getopt


def usage():
 print '\n*********************************\n'
 print 'The script should be runned with only one option. To run it :\n    python browser-shots.py -f filePath \n'
 print '    python browser-shots.py -d directoryPath \n'
 print '*********************************\n'

def clean_it():
 to_be_removed = []
 if os.path.isdir('./marcalizer/out/bow/top/sift/100/1/'):
  to_be_removed.append('./marcalizer/out/bow/top/sift/100/1/')
 if os.path.isdir('./marcalizer/out/bow/top/sift/200/1/'):
  to_be_removed.append('./marcalizer/out/bow/top/sift/200/1/')
 if os.path.isdir('./marcalizer/out/sift/top/1/'):
  to_be_removed.append('./marcalizer/out/sift/top/1/')
 if os.path.isdir('./marcalizer/out/images/1/'):
  to_be_removed.append('./marcalizer/out/images/1/')
 if os.path.isdir('./marcalizer/in/images/1/'):
  to_be_removed.append('./marcalizer/in/images/1/')
 
 for r in to_be_removed:
  for f in os.listdir(r):
   os.remove(r + f)
 print 'all directories are cleaned'
 ts = date('%Y-%m-%d-%H:%M:%S')
 return ts

def split_it(l, j):
 if l:
  fp = open('./pairs/p-'+str(j),'a')
  fp.write(l[0])
  fp.write(l[1])
  l = l[:0] + l[1:]
  l = l[:0] + l[1:]
  j += 1
  split_it(l, j)

def take_remote_snapshot(host, opera, finput):
 print 'loading  in = ' + host + ' ; ' + opera
 list = open(finput, 'r').readlines()
 url1 = list[0]
 url2 = list[1]
 timestamp = date('%Y-%m-%d-%H-%M-%S')
 dir = './screenshots-tmp/' + os.path.basename(finput) + '-' + timestamp
 os.makedirs(dir)
 f = open(dir + '/' + os.path.basename(finput) + '-' + timestamp + '.txt', 'a')
 timestamp = date('%Y-%m-%d-%H-%M-%S')
 f.write('\n' + timestamp + ' taking snapshots')
 driver1 = webdriver.Remote(host, webdriver.DesiredCapabilities.FIREFOX)
 driver1.get(url1)
 driver2 = webdriver.Remote(opera, webdriver.DesiredCapabilities.OPERA)
 driver2.get(url2)
 format = '%Y-%m-%d-%H-%M-%S-%f'
 today = datetime.datetime.today()
 ts = (today.strftime(format))
 timestamp = date('%Y-%m-%d-%H-%M-%S')
 f.write('\n' + dir + '/ff36-' + ts + '.png' + ' ' + url1)
 f.write(dir + '/op12-' + ts + '.png' + ' ' + url2)
 driver1.get_screenshot_as_file(dir + '/ff36-' + ts + '.png')
 driver2.get_screenshot_as_file(dir + '/op12-' + ts + '.png')
 driver1.quit()
 driver2.quit()
 f.write(timestamp + ' snapshots taken')
 f.close()
 print 'snapshots taken'

def nothing():
 print '' 

def take_5_snapshots(host, opera, l_input, dir):
 print 'take_5_snapshots from : ' + str(host)
 p = Process(target=nothing, args=())
 print dir
 print len(l_input)
 lol = [l_input[i:i+5] for i in range(0, len(l_input), 5)]
 if len(lol) > 1:
  for list in lol:
   for f in list:
    f_path = str(dir) + '/' + str(f)
    print f_path
    if os.path.isfile(f_path):
     p = Process(target=take_remote_snapshot, args=(host, opera, f_path,))
     p.start()
   p.join()
 else:
  print 'a list of 5 pairs'
  for f in l_input:
   f_path = str(dir) + str(f)
   print f_path
   if os.path.isfile(f_path):
    p = Process(target=take_remote_snapshot, args=(host, opera, f_path,))
    p.start()


def marcalize_it():
 clean_it()
 log = open('./log/log.txt', 'a')
 rootdir = './screenshots-tmp/'
# select folders of all pairs in rootdir
 l_folder = []
 for root, subFolders, files in os.walk(rootdir):
  for folder in subFolders:
   l_folder.append(rootdir + str(folder))
 for f in l_folder:
  pictures = os.listdir(f)
  if len(pictures) > 2:
   for pic in pictures:
    print f +'/'+pic
    if pic[-4:] in (".png"):
     shutil.copy(f +'/'+pic, './marcalizer/in/images/1/')
    else:
     os.system('cat ' + f + '/' + pic + ' >> ./log/marcalizer-log.txt ')
     print 'texte'
   shutil.move(f, './log/compared-pictures/')
   pics = os.listdir('./marcalizer/in/images/1/')
   for pi in pics:
    if pi[-4:] not in (".png"):
     pics.remove(pi)
   p1 = './marcalizer/in/images/1/' + str(pics[0])
   p2 = './marcalizer/in/images/1/' + str(pics[1])
   print str(date('%Y-%m-%d-%H-%M-%S')) + ' starts with : [' + str(p1) + '] , ' + '[' + str(p2) + ']'
   os.system('echo "\n" >> ./log/marcalizer-log.txt')
   os.system('date  >> ./log/marcalizer-log.txt')
   os.system('java -jar ./marcalizer/marcalizer.jar -snapshot1 ' + p1 + ' -snapshot2 ' + p2 + ' >> ./log/marcalizer-log.txt')
   os.system('date  >> ./log/marcalizer-log.txt')
   os.system('echo "-------------------------------------------\n" >> ./log/marcalizer-log.txt')
   clean_it()
  else:
   print 'no pictures in the folder'
   shutil.move(f, './log/compared-pictures/')
#end of marcalize-it


def main():
 node0 = "http://im1a10.internetmemory.org:5555/wd/hub"
 node1 = "http://im1a11.internetmemory.org:5555/wd/hub"
 node2 = "http://im1a12.internetmemory.org:5555/wd/hub"
 opera0 = "http://im1a10.internetmemory.org:5556/wd/hub"
 opera1 = "http://im1a11.internetmemory.org:5556/wd/hub"
 opera2 = "http://im1a12.internetmemory.org:5556/wd/hub"

 try:
  opts, args = getopt.getopt(sys.argv[1:], 'hf:d:', ['help', 'file=', 'directory='])
 except getopt.GetoptError as err:
  print('\nERROR:')
  print (err)
  usage()
  sys.exit()
#create all necessary folders
 if not os.path.exists('log'):
  os.makedirs('log')
 if not os.path.exists('log/compared-pictures'): 
  os.makedirs('log/compared-pictures')
 if not os.path.exists('./screenshots-tmp/'):
  os.makedirs('./screenshots-tmp/')
 if not os.path.exists('./pairs/'):
  os.makedirs('./pairs/')
#check options
 for o,a in opts:
  if o in ('-h', '--help'):
   usage()
  elif o in ('-f', '--file'):
   if os.path.isfile(a):
    f = open(a,'r')
    l = [l for l in f.readlines() if l.strip()]
    split_it(l, 1)
    f.close()
    print '\n the file is now divided to pairs in the directory "pairs" '
    print 'you can use the option "-d" of the script or type "-h" for help '
   else:
    print ('is not a file')
  elif o in ('-d', '--directory'):
   ts = date('%Y-%m-%d-%H:%M:%S')
   if os.path.isdir(a):
    print 'is a dir'
    listing = os.listdir(a)
    n = len(listing)
    print '~~~ ' + str(n) + ' ~~~'
    if (n <= 0):
     print 'capture in localhost'
     p = Process(target=take_5_snapshots(node0, listing, a), args=())
     p.start()
    if (n > 0):
     print 'capture in other nodes' 
     lol = [listing[i:i+(n/3+1)] for i in range(0, n, n/3+1)]
     iteration = 0
     for l in lol:
      print '\n' 
      if iteration == 0 :
       print 'node0 = ' + str(l)
       p0 = Process(target=take_5_snapshots, args=(node0, opera0, l, a,))
       p0.start()
      if iteration == 1 :
       print 'node1 = ' + str(l)
       p1 = Process(target=take_5_snapshots, args=(node1, opera1, l, a,))
       p1.start()
      if iteration == 2 :
       print 'node2 = ' + str(l)
       p2 = Process(target=take_5_snapshots, args=(node2, opera2, l, a,))
       p2.start()
      iteration += 1
   else:
    print 'is not a directory'
  else:
   print('ERROR')
   sys.exit(2)

 time.sleep(50)
 marcalize_it() 


if __name__ == "__main__":
    main()
