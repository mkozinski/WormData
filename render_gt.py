import numpy as np
import re

def volInds(swcCoords,scale,volDims,offset,downsampling):
    x=int((swcCoords[volDims[0]]*scale[0]+offset[0])*downsampling[0])
    y=int((swcCoords[volDims[1]]*scale[1]+offset[1])*downsampling[1])
    z=int((swcCoords[volDims[2]]*scale[2]+offset[2])*downsampling[2])
    return x,y,z

def traceLine(lbl,begPoint,endPoint):
    # endPoint and begPoint should be np.arrays
    # lbl is an np.array to which the line is rendered
    d=endPoint-begPoint
    s=begPoint
    mi=np.argmax(np.fabs(d))
    coef=d/d[mi]
    sz=np.array(lbl.shape)
    numsteps=int(abs(d[mi]))+1
    step=int(d[mi]/abs(d[mi]))
    for t in range(0,numsteps):
        pos=np.fabs(s+coef*t*step)
        if np.all(pos<=sz) and np.all(pos>=0):
            #print(pos)
            lbl[tuple(pos.astype(np.int))]=1
        else:
            print("reqested point",pos,"but the volume size is",sz)
    return lbl

def renderSWC2volume(swcfname, volumeDims, volCL, scale, offset, downsampling):
    '''
      swcfname      name of the swc file
      volumeDims    one-dimensional array;
                    volumeDims[1] is index of volCL dimension corresponding to X
                    volumeDims[2] is index of volCL dimension corresp to Y
                    volumeDims[3] is index of volCL dimension corresp to Z
                    X,Y,Z are as interpreted in the CWS format
      volCL         np array into which we will render ground truth centerlines
    '''
    distthresh=40
    nodes=dict()
    for a in open(swcfname):
        if (re.match('\s*\#',a)!=None):
            print("commment line", a)
            continue
        b=a.split()
        c=map(lambda x: float(x), b)
        d=list(c)
        nodes[int(d[0])]=d
        #print(d)
    for k in nodes :
        n=nodes[k]
        x,y,z= volInds(n,scale,volumeDims, offset, downsampling)
        parent=nodes.get(int(n[6]),None)
        #print(n)
        if parent!=None :
            #print(n,parent)
            xp,yp,zp=volInds(parent,scale,volumeDims, offset, downsampling)
            #print(x,y,z,volCL.shape)
            #print(xp,yp,zp,volCL.shape)
            if (x!=xp or y!=yp or z!=zp) and ((abs(x-xp)+abs(y-yp)+abs(z-zp))<distthresh):
                #print("line: ({},{},{})-({},{},{})".format(xp,yp,zp,x,y,z))
                traceLine(volCL,np.array([xp,yp,zp]),np.array([x,y,z]))


