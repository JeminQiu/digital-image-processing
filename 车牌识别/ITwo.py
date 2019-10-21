import cv2 as cv2
import  numpy as np
#迭代阈值法分割图片
def iTwo(path):
    img=cv2.imread(path,cv2.COLOR_BGR2GRAY)
    img_gray = (cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)).astype(np.uint8)
    minPix=np.min(img_gray)
    maxPix=np.max(img_gray)
    half=(minPix+maxPix)//2
    temp=0
    _t=0
    for _t in range(10):
        w0=img_gray[np.where(img_gray<half)]
        w1=img_gray[np.where(img_gray>half)]
        meanW0=np.mean(w0)
        meanW1=np.mean(w1)
        half=(meanW0+meanW1)//2
        if _t>1 and half-temp<4:  #收敛则退出
            break
        temp=half
    print("迭代二分法迭代的次数和找到的分割点分别为")
    print(_t)   #输出运行的次数
    print(half) #输出找到的分割的像素点
    img_gray[img_gray<half]=0
    img_gray[img_gray>half]=255
    cv2.imshow("iTwo",img_gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
if __name__ == '__main__':
    iTwo('5.jpg')