# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 09:32:16 2017

@author: christoffer
"""
import os
import numpy as np
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

def plotHist(bboxlst, year):
    binwidth = 10000
    plt.hist(bboxlst, bins = range(np.int(min(bboxlst)), np.int(max(bboxlst))
                                    + binwidth, binwidth))
    plt.title(year + " trainval Bounding Box Area")
    plt.xlabel("Area")
    plt.ylabel("Frequency")
    plt.savefig('figs/data_' + year + '.pdf')

#xml = ""
#xmlfile = '../../../benchmarkdata/pascalvoc/2012/Annotations/2007_000423.xml'
#xmlfile = '../../../benchmarkdata/pascalvoc/2012/Annotations/2008_003969.xml'

# All xml in dir
year = '2007'
path = '../../../benchmarkdata/pascalvoc/' + year + '/Annotations/'
allbbox_id = []
allbbox = []
filenames = []
fileno = 0
#for y in range(0,1):
for filename in os.listdir(path):
    #filename = '2007_000423.xml'
    if not filename.endswith('.xml'): 
        continue
    fullname = os.path.join(path, filename)
        
    # Parse xml file
    with open(fullname) as f:
        xml = f.readlines()
    xml = ''.join([line.strip('\t') for line in xml])
        
    soup = BeautifulSoup(xml, "xml")
    obj = soup.find_all('object')
    soupLength = len(obj)
    
    
    bndboxlst = soup.find_all('bndbox')
    partlst = soup.find_all('part')
    
    # Extract all bboxes
    xminlst, yminlst, xmaxlst, ymaxlst, bboxarealst = ([] for i in range(5))
    bboxstrlst = []
    for i  in range(0, len(bndboxlst)):
        bbox = bndboxlst[i]
        bbox = bbox.contents
        tags = [tag.name for tag in bbox]
        
        #for j in range(0,len(bbox)):
        #    bboxstrlst.append(str(bbox[0].extract()))   
        tags = ['None' if v is None else v for v in tags]
        xminind = [q for q, s in enumerate(tags) if 'xmin' in s]
        yminind = [q for q, s in enumerate(tags) if 'ymin' in s]
        xmaxind = [q for q, s in enumerate(tags) if 'xmax' in s]
        ymaxind = [q for q, s in enumerate(tags) if 'ymax' in s]
        xmin = np.float(bbox[xminind[0]].get_text())
        ymin = np.float(bbox[yminind[0]].get_text())
        xmax = np.float(bbox[xmaxind[0]].get_text())
        ymax = np.float(bbox[ymaxind[0]].get_text())
        #xmin = np.float(''.join(c for c in bboxstrlst[xminind[0]] if c.isdigit()))    
        #ymin = np.float(''.join(c for c in bboxstrlst[ymindind[0]] if c.isdigit()))
        #max = np.float(''.join(c for c in bboxstrlst[xmaxind[0]] if c.isdigit()))
        #ymax = np.float(''.join(c for c in bboxstrlst[ymaxind[0]] if c.isdigit()))
    
        xminlst.append(xmin)
        yminlst.append(ymin)
        xmaxlst.append(xmax)
        ymaxlst.append(ymax)
        bboxarealst.append((ymaxlst[i]-yminlst[i]) * (xmaxlst[i]-xminlst[i]))
    
    # Extract bbox for parts                                                
    for i in range(0, len(partlst)):
        part = partlst[i].contents
        #if part[3].xmin is not None:
        #    print(i)
        try:
            pxmin = part[3].xmin.extract()    
            pymin = part[3].ymin.extract()    
            pxmax = part[3].xmax.extract()    
            pymax = part[3].ymax.extract()
            pxmin = str(pxmin)
            pymin = str(pymin)
            pxmax = str(pxmax)
            pymax = str(pymax)
            xmin = np.float(''.join(c for c in pxmin if c.isdigit()))    
            ymin = np.float(''.join(c for c in pymin if c.isdigit()))
            xmax = np.float(''.join(c for c in pxmax if c.isdigit()))
            ymax = np.float(''.join(c for c in pymax if c.isdigit()))
            partarea = (ymax - ymin) * (xmax - xmin)
            # Remove part bboxes
            if partarea in bboxarealst:
                bboxarealst.remove(partarea)
        except AttributeError:
            print("no value present")
     
    allbbox_id.append(filename)
    for i in range(0, len(bboxarealst)):
        allbbox_id.append(bboxarealst[i])    
        allbbox.append(bboxarealst[i])
        
    
    filenames.append(filename)
    fileno += 1
    if fileno % 100 == 0:
        print("Parsed {} files".format(fileno))

plotHist(allbbox, year) 