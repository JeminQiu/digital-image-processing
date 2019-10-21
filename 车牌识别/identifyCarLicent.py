import numpy as np
import math
import cv2
import os
class CarLicent:
    imgOfLicent=[]
    wave=[]
    begin=0
    end=0
    #调整最小正方形的四个点的顺序
    def findVertices(self,box):
        # 获取四个顶点坐标
        boxTemp = []
        #四个点的顺序为上下左右
        box = box[np.lexsort(box[:, ::-1].T)] # 按第一列排序
        if box[1][1] > box[0][1]:
            boxTemp.append(box[0])
            boxTemp.append(box[1])
        else:
            boxTemp.append(box[0])
            boxTemp.append(box[1])
        if box[2][1] > box[3][1]:
            boxTemp.append(box[3])
            boxTemp.append(box[2])
        else:
            boxTemp.append(box[2])
            boxTemp.append(box[3])
        return boxTemp
    #旋转图片
    def rotate(selg,img, pt1, pt2, pt3, pt4, newImagePath):
        withRect = math.sqrt((pt4[0] - pt1[0]) ** 2 + (pt4[1] - pt1[1]) ** 2)  # 矩形框的宽度
        angle = math.asin((pt4[0] - pt1[0]) / withRect) * (180 / math.pi)  # 矩形框旋转角度
        if pt4[1] > pt1[1]:
            print("顺时针旋转")
            angle = -angle
        else:print("逆时针旋转")
        height = img.shape[0]  # 原始图像高度
        width = img.shape[1]  # 原始图像宽度
        # 获得图像绕某一点的旋转矩阵
        print(angle)
        rotateMat = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)  # 按angle角度旋转图像
        heightNew = int(
            width * math.fabs(math.sin(math.radians(angle))) + height * math.fabs(math.cos(math.radians(angle))))
        widthNew = int(
            height * math.fabs(math.sin(math.radians(angle))) + width * math.fabs(math.cos(math.radians(angle))))
        rotateMat[0, 2] += (widthNew - width) / 2
        rotateMat[1, 2] += (heightNew - height) / 2
        imgRotation = cv2.warpAffine(img, rotateMat, (widthNew, heightNew), borderValue=(255, 255, 255))
        # 旋转后图像的四点坐标
        [[pt1[0]], [pt1[1]]] = np.dot(rotateMat, np.array([[pt1[0]], [pt1[1]], [1]]))
        [[pt3[0]], [pt3[1]]] = np.dot(rotateMat, np.array([[pt3[0]], [pt3[1]], [1]]))
        [[pt2[0]], [pt2[1]]] = np.dot(rotateMat, np.array([[pt2[0]], [pt2[1]], [1]]))
        [[pt4[0]], [pt4[1]]] = np.dot(rotateMat, np.array([[pt4[0]], [pt4[1]], [1]]))
        # 处理反转的情况
        if pt2[1] > pt4[1]: pt2[1], pt4[1] = pt4[1], pt2[1]
        if pt1[0] > pt3[0]:pt1[0], pt3[0] = pt3[0], pt1[0]
        x1 = min((pt1[0], pt2[0], pt3[0], pt4[0]))
        x2 = max((pt1[0], pt2[0], pt3[0], pt4[0]))
        y1 = min((pt1[1], pt2[1], pt3[1], pt4[1]))
        y2 = max((pt1[1], pt2[1], pt3[1], pt4[1]))
        imgOut = imgRotation[int(y1):int(y2)+5, int(x1):int(x2)]
       # cv2.imshow("imgCut", imgOut)
       # cv2.waitKey(0)
       # cv2.destroyAllWindows()
        return imgOut  # rotated image
    def predict(self,path):
        self.imgOfLicent.clear()
        img = cv2.imread(path, cv2.COLOR_RGB2GRAY)
        # 将原图做个备份
        sourceImage = img.copy()
        # 高斯模糊滤波器对图像进行模糊处理
        img = cv2.GaussianBlur(img, (3, 3), 0)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        Matrix = np.ones((15, 15), np.uint8)
        img_opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, Matrix)
        img = cv2.addWeighted(img, 1, img_opening, -1, 0)

        kernelY = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 5))
        img = cv2.erode(img, kernelY, anchor=(-1, -1), iterations=1)
        # canny边缘检测
        _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        cv2.imshow('OSTU', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        kernelX = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 1))
        img = cv2.dilate(img, kernelX, anchor=(-1, -1), iterations=1)
        img = cv2.Canny(img, 100, 200)
        cv2.imshow('Canny', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Matrix = np.ones((4, 19), np.uint8)
        # img_edge1 = cv2.morphologyEx(img, cv2.MORPH_CLOSE, Matrix)
        # img_edge1 = cv2.morphologyEx(img_edge1, cv2.MORPH_OPEN, Matrix)
        # img_edge1 = cv2.morphologyEx(img_edge1, cv2.MORPH_OPEN, Matrix)
        # img_edge2 = cv2.morphologyEx(img_edge1, cv2.MORPH_OPEN, Matrix)
        # cv2.imshow('img_edg2', img_edge2)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # # 指定核大小，如果效果不佳，可以试着将核调大
        # kernelX = cv2.getStructuringElement(cv2.MORPH_RECT, (16, 1))
        # kernelY = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 10))
        # img_edge2 = cv2.erode(img_edge2, kernelX, anchor=(-1, -1), iterations=1)
        # img_edge2=cv2.erode(img_edge2,kernelY,anchor=(-1, -1), iterations=4)
        # img_edge2 = cv2.dilate(img_edge2, kernelX, anchor=(-1, -1), iterations=4)
        # cv2.imshow('img_edg2', img_edge2)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # 指定核大小，如果效果不佳，可以试着将核调大
        kernelX = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 1))
        kernelY = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 20))
        # 对图像进行膨胀腐蚀处理
        img = cv2.dilate(img, kernelX, anchor=(-1, -1), iterations=2)
        img = cv2.erode(img, kernelX, anchor=(-1, -1), iterations=4)
        img = cv2.dilate(img, kernelX, anchor=(-1, -1), iterations=2)
        img = cv2.erode(img, kernelY, anchor=(-1, -1), iterations=1)
        img = cv2.dilate(img, kernelY, anchor=(-1, -1), iterations=2)
        kernelX = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 1))
        img = cv2.erode(img, kernelX, anchor=(-1, -1), iterations=1)
        # 再对图像进行模糊处理
        img = cv2.medianBlur(img, 15)
        img = cv2.medianBlur(img, 15)
        cv2.imshow('sourceImage', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return sourceImage,img
    #统计每一行非0像素点的个素
    def findWave(self,img):
        self.rate=[]
        height, width = img.shape
        rate = []
        img2 = img.astype(np.uint8)
        for i in range(0,height):
            temp = img2[i]
            rate.append(sum(temp[np.where(temp != 0)]) / 255)
            #当两行的非零像素点的和的差值超过5时就认为是突变点,保存下来
            if len(rate)>1 and abs(rate[-1]-rate[-2])>=5:
                if (len(self.wave)>=1 and abs(i-self.wave[-1])<10):
                    continue
                self.wave.append(i) #存储所有非零像素点的和突变的位置
    #查找车牌位置
    def findClient(self,img,path):
        #+20的原因是扩大区别,防止车牌不完整
        self.begin = self.wave[len(self.wave)-1]+20
        for i in range(len(self.wave)-2,-1,-1):
            #-50,即向上扩大查找车牌的范围,因为本身车牌内部也为存在很多
            #突变点,确保车牌完整,同时减少查找的次数
            self.end=self.wave[i]-50
            img2=img[self.end:self.begin,:]
            sourseImg=self.sourceImage[self.end:self.begin,:]
            #车牌的区域至少大于20
            if abs(self.end-self.begin)<20:
                continue
            #找到车牌就直接退出
            if(self.findRectangle(img2,sourseImg,path)):
                break
    def findRectangle(self,img,sourseImg,path):
        kernelX = cv2.getStructuringElement(cv2.MORPH_RECT, (35, 1))
        kernelY = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 20))
        # 对图像进行膨胀腐蚀处理
        img = cv2.dilate(img, kernelX, anchor=(-1, -1), iterations=2)
        img = cv2.erode(img, kernelX, anchor=(-1, -1), iterations=4)
        img = cv2.dilate(img, kernelX, anchor=(-1, -1), iterations=2)

        img = cv2.erode(img, kernelY, anchor=(-1, -1), iterations=1)
        img = cv2.dilate(img, kernelY, anchor=(-1, -1), iterations=2)
        kernelY = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 15))
        img = cv2.erode(img, kernelY, anchor=(-1, -1), iterations=1)
        # 再对图像进行模糊处理
        img = cv2.medianBlur(img, 15)
        img = cv2.medianBlur(img, 15)
        if(self.fixPosition(sourseImg,img,path)):
            return True
        return  False


    def predictByPixel(self,path):
        self.imgOfLicent.clear()
        img = cv2.imread(path, cv2.COLOR_RGB2GRAY)
        self.sourceImage = img.copy()   #备份图像
        # 高斯模糊滤波器对图像进行模糊处理
        img = cv2.GaussianBlur(img, (3, 3), 0)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
       # img = cv2.equalizeHist(img)   #直方图均衡化
        Matrix = np.ones((15, 15), np.uint8)
        img_opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, Matrix)
        img = cv2.addWeighted(img, 1, img_opening, -1, 0)

        _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        #消除一些孤立的边缘线然后再检测车牌边缘
        kernelY = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 10))
        img2 = cv2.erode(img, kernelY, anchor=(-1, -1), iterations=1)
        self.img = cv2.Canny(img2, 100,200)
        img=cv2.Canny(img,100,200)
        # cv2.imshow("Canny", img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return img
    #定位车牌的位置
    def fixPosition(self,sourceImage,img,savePath):
        contours, hier = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # RETR_EXTERNAL 只检测外轮廓，并且保存轮廓上所有的点
        # RETR_LIST 检测所有轮廓，不建立等级关系，并且保存轮廓上的拐点信息
        num = []
        for i in range(len(contours)):
            # # 用红色表示有旋转角度的矩形框架
            # rect = cv2.minAreaRect(cnt)
            # box = cv2.cv.BoxPoints(rect)
            # box = np.int0(box)
            # cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
            # cv2.imwrite('contours.png', img)
            x_min = np.min(contours[i][:, :, 0])
            x_max = np.max(contours[i][:, :, 0])
            y_min = np.min(contours[i][:, :, 1])
            y_max = np.max(contours[i][:, :, 1])
            det_x = x_max - x_min
            det_y = y_max - y_min
            if (det_x / det_y >=2.6) and (det_x / det_y < 5.2):
                det_y_max = det_y
                det_x_max = det_x
                num.append(i)  # 存储所有可能的框
        if len(num)==0:
            return False
        for i in num:
            points = np.array(contours[i][:, 0])
            rect = cv2.minAreaRect(points)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            #在原图像上面画出框来
            lpImage = cv2.drawContours(sourceImage.copy(), [box], -1, (0, 0, 255), 3)
            cv2.imshow("IpImage",lpImage)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            box = self.findVertices(box)  # 四个点的顺序为上下左右
            imageCut=self.rotate(sourceImage, box[1], box[2], box[3], box[0],newImagePath=savePath)
            cv2.imwrite(savePath[0:14]+str(i)+savePath[14:],imageCut)
           #  cv2.imshow("CLIENT",imageCut)
           #  cv2.waitKey(0)
           #  cv2.destroyAllWindows()
        return True
if __name__ == '__main__':
    dirpath="tenCar"
    maindir=os.listdir("tenCar")
    a=CarLicent()
    for i in maindir:
        path=dirpath+"/"+i
        img = a.predictByPixel(path)
        path = "tenCarClient"+ "/" + i
        a.findWave(a.img)
        a.findClient(img,path)
    #
    # a=CarLicent()
    # path="tenCar/2.jpg"
    # img=a.predictByPixel(path)
    # path="tenCarClient/car5123.bmp"
    # a.findWave(a.img)
    # a.findClient(img,path)
# path = dirpath + "/" + i
# sourseImg, img = a.predict(path)
# path = "tenCarClient" + "/" + i
# a.fixPosition(sourseImg, img, path)