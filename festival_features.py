import os
import logging
import numpy as np
import struct 
from matplotlib import pyplot as pp

festival_path = '/Users/hamid/Code/festival/festival/'

class Festival_features():
    def __init__(self, lname, feats_file=None):
        self.read_list(lname)
        if feats_file:
            self.read_list_header(hname)
    def read_list(self, lname):
        chars = ['^', '-', '+', '=', '@', '_', '/', ':', '&', '#', '$', '!', ';', '|']

        inx=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        
        ls = []
        cnt =0
        f= open(lname)
        for line in f:
            line = line[:-1]
            line=line.replace('L-', 'L*')
            for c in chars:
                line=line.replace(c, ',')
            vals=line.split(',')
            for j in inx:
                vals.remove(j)
            ls.append(vals)
            cnt += 1
        ls_np = np.zeros((len(ls), len(ls[0])), 'object')
        i=0
        for ln in ls:
            j=0
            for o in ln: 
                ls_np[i,j] = o
                j+=1
            i+=1
            
        self.cats = [0,1,2,3,4, 7,8, 10,11, 25, 29,31,39, 47]
        ordinals = range(ls_np.shape[1])
        dims = []
        dicts = []
        for i in cats:
            ordinals.remove(i)
            dims.append(len(np.unique(ls_np[:, i])))
            if 'x' in ls_np[:, i]:
                dims[-1] -= 1
            unq = np.unique(ls_np[:, i])
            unq = unq.tolist()
            if 'x' in unq:
                unq.remove('x')
            unq=np.array(unq)
            d = {}
            for j in range(len(unq)):
                d[unq[j]] = j
            dicts.append(d)
        dimension = sum(dims) + len(ordinals)
        one_hot_data = np.zeros((ls_np.shape[0],dimension), dtype=int)
        cnt = 0
        for i in ordinals:
            if ls_np[:, i] is 'x':
                one_hot_data[:, cnt] = 0
            else:
                one_hot_data[:, cnt] = np.int(ls_np[:, i])
            cnt += 1
        for i in range(len(cats)):
            one_hot_data[:, cnt:cnt+dims[i]] = 0
            one_hot_data[:, cnt+dicts[ls_np[:,cats[i]]]] = 1
            cnt += dims[i]
            
        return ls_np
    def _convert_line_to_array(self, line):
        pass
    def read_list_header(self, hname):
        f= open(hname)
        cats = []
        for line in f:
            line = line[:-1]
            if line.startswith('#  '):
                prev_name = line
            if line.startswith('    printf ') and len(line) > len('    printf "@"')+1:
                cats.append(prev_name)
        pass    
            
    def convert_utt(self):
        pass
    def convert_dur(self):
        pass
    
def Festival_fx(text):
    """ 
    generate contextual features from a given tesxt string
    input: text (string)
    output: feature file name (string)
    """
    # generate .utt 
    os.system("echo -e '(load (path-append libdir \"init.scm\"))\n(utt.save (SynthText \""+text+"\") \"hts_scripts/tmp/tmp.utt\")' > hts_scripts/tmp/tmp.scp")
    os.system(festival_path+'bin/festival --script hts_scripts/tmp/tmp.scp')
    os.system('rm '+hts_scripts_path+'tmp/tmp.scp')
    # generate features from .utt
    os.system(festival_path + 'examples/dumpfeats \\ \
	-eval     '+hts_scripts_path+'extra_feats.scm \\ \
	-relation Segment \\ \
	-feats    '+hts_scripts_path+'label.feats \\ \
	-output   '+hts_scripts_path+'tmp/tmp.feat \\ \
	'+hts_scripts_path+'tmp/tmp.utt')

    # generate .lab (contextual features) from features computed from the previous step
    os.system('awk -f '+hts_scripts_path+'label-full.awk '+hts_scripts_path+'tmp/tmp.feat > '+hts_scripts_path+'tmp/tmp.full.lab')
    os.system('awk -f '+hts_scripts_path+'label-mono.awk '+hts_scripts_path+'tmp/tmp.feat > '+hts_scripts_path+'tmp/tmp.mono.lab')
    os.system('rm -f '+hts_scripts_path+'tmp/tmp.feat')

    return hts_scripts_path+'tmp/tmp.full.lab'


hname = '/Users/hamid/Code/hts/HTS-demo_CMU-ARCTIC-SLT2/data/scripts/label-full.awk'
lname = '/Users/hamid/Code/hts/HTS-demo_CMU-ARCTIC-SLT2/data/lists/full.list'

Festival_features(lname, hname)