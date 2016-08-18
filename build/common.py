import errno
import json
import os
import shutil
import urllib2

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
            
def make_dirs(folders_list):
    print 'making directories'
    for f in folders_list:
        make_sure_path_exists(f)
        print 'paths exist'

def copy(src, dest):
    print 'copy', src, dest
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)
        
def copytree(src, dst, symlinks=False, ignore=None):
    print 'copytree', src, dst
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)
            
def clean(folders_list):
    for f in folders_list:
        print 'removing', f
        shutil.rmtree(f)

def is_number(s):
    try:
        float(s)
        return True
    except:
        return False

def format_num(x):
    if x == int(x):
        return int(x)
    else:
        return x

def download_file_from(url, dest):
    print 'downloading to', dest
    response = urllib2.urlopen(url)
    with open(dest, 'w') as f:
        f.write(response.read())

def open_json(src):
    with open(src, 'r') as f:
        return json.loads(f.read())

def write_json(data, dest):
    with open(dest, 'w') as f:
        f.write(json.dumps(data, indent=1, sort_keys=True))
        
def subset(KEYS, bigdict):
    output = {k: bigdict[k] for k in KEYS if k in bigdict and bigdict[k]}
    return output