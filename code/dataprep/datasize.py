# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 09:32:16 2017

@author: christoffer
"""
import os
import numpy as np
from bs4 import BeautifulSoup

xml = ""
xmlfile = '../../../benchmarkdata/pascalvoc/2012/Annotations/2007_000423.xml'
#xmlfile = '../../../benchmarkdata/pascalvoc/2012/Annotations/2008_003969.xml'

# All xml in dir
path = '../../../benchmarkdata/pascalvoc/2012/Annotations/'
allbbox = []
fileno = 0
for filename in os.listdir(path):
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
    for i  in range(0, len(bndboxlst)):
        bbox = bndboxlst[i]
        bbox = bbox.contents
        xminlst.append(np.float(bbox[1].get_text()))
        yminlst.append(np.float(bbox[3].get_text()))
        xmaxlst.append(np.float(bbox[5].get_text()))
        ymaxlst.append(np.float(bbox[7].get_text()))
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
     

    for i in range(0, len(bboxarealst)):
        allbbox.append(bboxarealst[i])     
    
    fileno += 1
    if fileno % 100 == 0:
        print("Parsed {} files".format(fileno))
