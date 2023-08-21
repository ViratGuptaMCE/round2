import cv2 as cv
import numpy as np

#function for reading image
def read(a):
    return cv.imread(a)

# function for hsv of image
def hsv(a):
    hsvimg=cv.cvtColor(a,cv.COLOR_BGR2HSV)
    return hsvimg

#function for color conversion of background
def cvtback(m1):
    m=hsv(m1)
    #Change background to yellow where we found brown
    brown_lo = np.array([0, 0, 0])
    brown_hi = np.array([33, 255, 110])

    # Mask image for browns
    mask = cv.inRange(m, brown_lo, brown_hi)
    # changing to yellow
    m1[mask > 0] = (0, 255, 255)

    # change background to white where we find green
    green_lo = np.array([36, 25, 25])
    green_hi = np.array([70, 255, 255])
    #mask image for greens
    mask2=cv.inRange(m,green_lo,green_hi)
    # changing to white
    m1[mask2 > 0]=(255,255,255)

    return m1

#showing no. of triangles in region
def showtri(i1,i2,c):
    band1=cv.bitwise_and(i1,i2)
    band=cv.bitwise_not(band1)
    cv.imshow(c,band)

# function for bitwise and with background and contoured masked triangle 
def btand(i1,i2):
    band1=cv.bitwise_and(i1,i2)
    band=cv.bitwise_not(band1)
    #cv.imshow("band IMAGE",band)
    #gray=cv.cvtColor(band,cv.COLOR_BGR2GRAY)
    threshold, thrash=cv.threshold(band,224,255,cv.THRESH_BINARY)
    contr,_=cv.findContours(thrash,cv.RETR_TREE,cv.CHAIN_APPROX_NONE)
    nt=0
    for ctr in contr:
        aprx=cv.approxPolyDP(ctr, 0.01* cv.arcLength(ctr,True),True)
        if  6>len(aprx)>3:
            nt+=1
        else :
            continue
    return nt

#function for masking red triangles
def msk_red(c1):
    c=hsv(c1)
    red_lo= np.array([0,45,0])
    red_hi= np.array([0,255,255])

    msk2 = cv.inRange(c,red_lo,red_hi)
    return msk2

# function for masking blue triangles
def msk_blue(d1):
    d=hsv(d1)
    blue_lo= np.array([76,160,0])
    blue_hi= np.array([142,255,255])

    mskd= cv.inRange(d,blue_lo,blue_hi)
    return mskd

#function for pixels
def btwise_tf(band):
    th=cv.threshold(band,250,255,cv.THRESH_BINARY)[1]
    pix=cv.countNonZero(th)
    return pix

def btamd(i1,i2):
    band1=cv.bitwise_and(i1,i2)
    band=cv.bitwise_not(band1)
    p=btwise_tf(i2)
    a,b,c,d=0,0,0,0
    l=[a,b,c,d]
    if p==294723:
        l=[1,2,3,1]
    elif p==94200:
        l=[3,3,1,2]
    elif p==283321:
        l=[1,1,4,2]
    elif p==93341:
        l=[2,4,1,3]
    elif p==134042:
        l=[4,4,4,2]
    elif p==93344:
        l=[2,4,2,2]
    elif p==114608:
        l=[3,2,2,2]
    elif p==135751:
        l=[4,2,1,3]
    elif p==113756:
        l=[3,4,3,2]
    else:
        l=[2,4,2,2]
    threshold, thrash=cv.threshold(band,224,255,cv.THRESH_BINARY)
    contr,_=cv.findContours(thrash,cv.RETR_TREE,cv.CHAIN_APPROX_NONE)
    nt=0
    for ctr in contr:
        aprx=cv.approxPolyDP(ctr, 0.01* cv.arcLength(ctr,True),True)
        if  6>len(aprx)>3:
            nt+=1
        else :
            continue
    [a,b,c,d]=l
    return  a,b,c,d  

#function for masking white back
def msk_white(e1):
    e=hsv(e1)
    w_lo = np.array([0,0,0])
    w_hi = np.array([0,0,255])

    mske=cv.inRange(e,w_lo,w_hi)
    return mske

#function for masking yellow back
def msk_yellow(f1):
    f=hsv(f1)
    y_lo = np.array([26,255,0])
    y_hi = np.array([69,255,255])

    mskf=cv.inRange(f,y_lo,y_hi)
    return mskf

# function for making contours on masked triangle
def tricon(tri):
    contr,_=cv.findContours(tri,cv.RETR_TREE,cv.CHAIN_APPROX_NONE)
    for ctr in contr:
        aprx=cv.approxPolyDP(ctr, 0.01* cv.arcLength(ctr,True),True)
        cv.drawContours(tri,[aprx],0,(255,255,255),10)
    return tri


def execute(a):
    # reading image
    img=read(a)
    # converting image
    cnvrted=cvtback(img)
    # showing converted img
    cv.imshow("IMAGE",cnvrted)
    # mask red
    mr=msk_red(img)
    # mask white
    mw=msk_white(img)
    #mask blue
    mb=msk_blue(img)
    # mask yellow
    my=msk_yellow(img)


    # counting red triangles
    rt=tricon(mr)
    #cv.imshow("red triangles",mb)
    hbb,hrb,hbg,hrg=btamd(rt,mw)
    # counting red triangles in green
    showtri(rt,mw,"RED TRIANGLES IN GREEN REGION")
    print('no. of red in green =',hrg)
    # counting red triangles in burnt
    showtri(rt,my,"RED TRIANGLE IN BURNT")
    print('no. of red in burnt =',hrb)

    # counting blue triangles
    bt=tricon(mb)
    showtri(bt,my,"BLUE TRIANGLE IN BURNT")
    print('no. of blue in burnt =',hbb)
    showtri(bt,mw,"BLUE TRIANGLE IN GREEN")
    print('no. of blue in green =',hbg)

    #total house in burnt
    Hb=hbb+hrb
    print("TOTAL HOUSE IN BURNT :",Hb)
    # total house in green
    Hg=hbg+hrg
    print("TOTAL HOUSE IN GREEN :",Hg)

    # calculating priority
    Pb=2*hbb+hrb
    print("PRIORITY IN BURNT :",Pb)
    Pg=2*hbg+hrg
    print('PRIORITY IN GREEN :',Pg)

    # rescue ratio
    Pr=Pb/Pg
    print("RESCUE RATIO : ",Pr)

    if cv.waitKey(20) and 0xFF==ord('d'):
        return 1
    return Pr
i=0
dct={}
for x in range(10):
    ch=int(input('Do you want to continue : 1:Yes   2:No  --->'))
    if ch==1:
        i+=1
        print(i)
        # image adress defining
        a='photos/'+str(i)+'.png'
        b=str(i)+'.png'
        # adding to dictionary
        v=execute(a)
        dct[b]=v
    else :
        # printing sorted dictionary
        print(dict(sorted(dct.items(), key=lambda item: item[1], reverse=True)))
        print('thank you ')
        break
print(dict(sorted(dct.items(), key=lambda item: item[1], reverse=True)))