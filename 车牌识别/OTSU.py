
import cv2 as cv2
import os
import numpy as np
#  大律法详解 ：
# 假设前景点数占图像比例为w0，平均灰度为u0（计算每个像素点的个数个比例然后用期望的公式就可以求出来）
# 背景点数占图像的比例为w1 ,平均灰度为u1 ，
#则图像的总平均灰度为 u=w0*i0+w1*u1
#前景和背景图像总的方差为g=w0(u0-u)*(u0-u)+w1*(u1-u)*(u1-u)=w1*w2*(u1-u0)**2
class OTSU:
    def readDir(self,param=True):
        path="tenCar"
        pathDir=os.listdir(path)
        for alldir in pathDir:
            image=path+"/"+alldir
            image=cv2.imread(image).astype(np.float)
            img=0.2126*image[...,2]+0.7152*image[:,:,1]+0.0722*image[:,:,0]
            img=img.astype(np.uint8)
            self.calThreshold(img,alldir)
    def calThreshold(self,img,path):
        max_sigma=0
        max_t=0
        H,W=img.shape
        for _t in range(1,255):
            v0=img[np.where(img<_t)]
            m0=np.mean(v0) if len(v0)>0 else 0
            w0=len(v0)/(H*W)
            v1=img[np.where(img>=_t)]
            m1=np.mean(v1) if len(v1)>0 else 0
            w1=len(v1)/(H*W)
            sigma=w0*w1*((m0-m1)**2)
            if sigma>max_sigma:
                max_sigma=sigma
                max_t=_t
        img[img<max_t]=0
        img[img>=max_t]=255
        print("大律法找到的分割点分别为")
        print(max_t)
        cv2.imwrite("./ostuCar/"+path,img)
if __name__ == '__main__':
    otsu=OTSU()
    #otsu.readDir()
    img=cv2.imread("tenCar/5.jpg")
    img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    otsu.calThreshold(img,"otsu.jpg")