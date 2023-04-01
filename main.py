import cv2
import numpy as np
import math
import os
import time
import random


dt = 0.012
Gr = 10
Mass = 1
Kl = 1
hs=10



img_size = (1024, 1024)  # 图像尺寸
bg_color = (255, 255, 255)  # 背景色为白色
radius = 10  # 原点半径
color = (0, 0, 255)  # 原点颜色为蓝色
thickness = -1  # 填充圆形
delay = 1  # 帧率


class node:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = None
        self.a = None
        self.s = None
        self.d = None
        self.ox = self.x
        self.oy = self.y
        # self.ow = self.w
        # self.oa = self.a
        # self.os = self.s
        # self.od = self.d
        self.v = [0, 0]
        self.keep = 0

    def updata(self):
        self.ox = self.x
        self.oy = self.y
        # self.ow = self.w
        # self.oa = self.a
        # self.os = self.s
        # self.od = self.d

    def move(self):
        if self.keep == 2:
            self.x += 0
            self.y += 0
            self.updata()
        else:
            vx = self.v[0]
            vy = self.v[1]
            self.x += vx * dt
            self.y += vy * dt
            self.updata()


def GetvL(Node1, Node2):
    lx = Node2.ox - Node1.x
    ly = Node2.oy - Node1.y
    L = math.sqrt(lx * lx + ly * ly)
    return [lx, ly], L


def GetForce(Node1, Node2):
    if Node2 == None:
        return [0, 0]
    tmp = GetvL(Node1, Node2)
    if tmp[1] > 1.05*hs:
        F = Kl * tmp[1] *1.2
    else:
        if tmp[1] < 0.95*hs:
            F = -Kl * tmp[1]
        else:
            F = 0
    x = tmp[0][0]
    y = tmp[0][1]
    vF = [x * F / math.sqrt(x * x + y * y), y * F / math.sqrt(x * x + y * y)]
    # print(vF)
    return vF


def sumVec(V1, V2):
    V1[0] = V1[0] + V2[0]
    V1[1] = V1[1] + V2[1]
    # return [x, y]


def GetA(Force, Mass):
    return [Force[0] / Mass, Force[1] / Mass]


def GetV(A, ov):
    # print("ov",ov)
    vx = ov[0] + A[0] * dt
    vy = ov[1] + A[1] * dt
    # print([vx,vy])
    u = 0.05
    r = 1 - u
    # 能量损耗
    vx = vx * r
    vy = vy * r
    if math.fabs(vx) < 0.001:
        vx = 0
    if math.fabs(vy) < 0.001:
        vy = 0
    return [vx, vy]


def sim(Node, noise):
    sumF = [0, 0]
    # sumVec(sumF, GetForce(Node, Node.w))
    # sumVec(sumF, GetForce(Node, Node.a))
    sumVec(sumF, GetForce(Node, Node.s))
    sumVec(sumF, GetForce(Node, Node.d))
    G = [0 + np.random.normal(noise, noise), Mass * Gr + np.random.normal(noise, noise)]
    sumVec(sumF, G)
    # print("sumF", sumF)
    # 求得合力
    ap = GetA(sumF, Mass)
    # rint("ap", ap)p
    Node.v = GetV(ap, Node.v)
    # print("Node.v",Node.v)
    Node.move()
    # print("[x,y]:", Node.x, Node.y)


def CreateFabricLine(x, y):
    node_list = [node() for i in range(x * y)]
    # print(len(node_list))
    for i in range(x):
        for j in range(y):
            index = (j) * x + i
            # print(i, j, index)
            node_list[index].x = hs * i + 50
            node_list[index].y = hs * j + 5
            # if i<10 and j>10:
            #     node_list[index].keep=1
            # print('-')

    # 第一行 asd
    # 左上角sd
    node_list[0].w = None
    node_list[0].a = None
    node_list[0].s = node_list[x]
    node_list[0].d = node_list[1]
    node_list[0].keep = 1
    # 右上角as
    node_list[x - 1].w = None
    node_list[x - 1].a = node_list[x - 1 - 1]
    node_list[x - 1].s = node_list[x - 1 + x]
    node_list[x - 1].d = None
    node_list[x - 1].keep = 1
    for i in range(1, x - 1):
        node_list[i].keep = 1
        node_list[i].w = None
        node_list[i].a = node_list[i - 1]
        node_list[i].s = node_list[i + x]
        node_list[i].d = node_list[i + 1]
    # 最后一行 wad
    # 左下角wd
    node_list[x * (y - 1)].w = node_list[x * (y - 1) - x]
    node_list[x * (y - 1)].a = None
    node_list[x * (y - 1)].s = None
    node_list[x * (y - 1)].d = node_list[x * (y - 1) + 1]
    # 右下角wa
    node_list[x * y - 1].w = node_list[x * y - 1 - x]
    node_list[x * y - 1].a = node_list[x * y - 2]
    node_list[x * y - 1].s = None
    node_list[x * y - 1].d = None
    for i in range(x * (y - 1) + 1, x * y - 1):
        node_list[i].w = node_list[i - x]
        node_list[i].a = node_list[i - 1]
        node_list[i].s = None
        node_list[i].d = node_list[i + 1]
    # 两侧
    for i in range(1, y - 1):
        # 左wsd
        index = x * i
        # print(index)
        node_list[index].w = node_list[index - x]
        node_list[index].a = None
        node_list[index].s = node_list[index + x]
        node_list[index].d = node_list[index + 1]

        # 右was
        index = x * (i + 1) - 1
        node_list[index].w = node_list[index - x]
        node_list[index].a = node_list[index - 1]
        node_list[index].s = node_list[index + x]
        node_list[index].d = None
    # 中间部分
    for i in range(1, x - 1):
        for j in range(1, y - 1):
            index = (j) * x + i
            node_list[index].w = node_list[index - x]
            node_list[index].a = node_list[index - 1]
            node_list[index].s = node_list[index + x]
            node_list[index].d = node_list[index + 1]

    return node_list


Node1 = node()
Node2 = node()
Node1.x = 30
Node1.y = 20
Node1.a = Node2
Node2.x = 20
Node2.y = 20

# node_list = [node() for i in range(100)]
# for i in range(10):
#     for j in range(10):
#         node_list[10*i+j].x = 20*i +100
#         node_list[10*i+j].y = 20*j +100
#
# for i in range(10):
#     node_list[i].keep=1


# print(GetvL(Node1, Node2))
# tmp = GetForce(Node1, Node2)
# print(tmp)
# print(sim(Node1))

# 创建窗口
# cv2.namedWindow("Animation")
# # 绘制动画
# # 帧数
# for i in range(10000):
#     # 创建一个空白图像
#     img = np.zeros((img_size[1], img_size[0], 3), dtype=np.uint8)
#     img[:, :] = bg_color
#     # 在图像上绘制
#     cv2.circle(img, (int(Node1.x), int(Node1.y)), 3, (0, 0, 255), -1)
#     cv2.circle(img, (int(Node2.x), int(Node2.y)), 3, (0, 255, 0), -1)
#     # 显示图像
#     cv2.imshow("Animation", img)
#     sim(Node1)
#     # 按下ESC键退出程序
#     if cv2.waitKey(delay) == 27:
#         break
# # 关闭窗口
# cv2.destroyAllWindows()
# # if __name__=='main':
#
# def showMap(tar):
#     node_list = tar
#     img = np.zeros((300, 400, 3), np.uint8)
#     for i in range(len(tar)):
#         cv2.circle(img, (node_list[i].x, node_list[i].y), 3, (0, 0, 255), -1)
#     cv2.imshow("image", img)
#     cv2.imwrite('image.jpg', img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()


# showMap(CreateFabricLine(10,5))

tar = CreateFabricLine(60, 30)
# tar[12]=None
# tar[4]=None
# 创建窗口
cv2.namedWindow("Animation")
# 绘制动画
# 帧数
for k in range(100000):
    # 创建一个空白图像
    img = np.zeros((img_size[1], img_size[0], 3), dtype=np.uint8)
    img[:, :] = bg_color
    # 在图像上绘制全部点
    # print(tar[14+15].v)
    for i in range(len(tar)):
        if tar[i] != None:
            # if tar[i].keep==1:
            #     c=(255, 0, 0)
            # else:
            #     c=(0, 0, 255)
            c = (0, 0, 255)
            cv2.circle(img, (int(tar[i].x), int(tar[i].y)), 1, c, -1)
            t = (int(tar[i].x), int(tar[i].y))
            if tar[i].w != None:
                w = (int(tar[i].w.x), int(tar[i].w.y))
                cv2.line(img, t, w, (100, 0, 0), 1, 4)
            if tar[i].a != None:
                a = (int(tar[i].a.x), int(tar[i].a.y))
                cv2.line(img, t, a, (0, 100, 0), 1, 4)
            if tar[i].s != None:
                s = (int(tar[i].s.x), int(tar[i].s.y))
                cv2.line(img, t, s, (100, 0, 100), 1, 4)
            if tar[i].d != None:
                d = (int(tar[i].d.x), int(tar[i].d.y))
                cv2.line(img, t, d, (0, 100, 100), 1, 4)

    # 显示图像
    cv2.imshow("Animation", img)
    # time.sleep(1)
    for i in range(len(tar)):
        if tar[i] != None:
            if k % 200 < 180:
                tmp=i%60
                sim(tar[i], (tmp/15)*0.9)
            else:
                sim(tar[i], 0)
    # 按下ESC键退出程序
    if cv2.waitKey(delay) == 27:
        break
# 关闭窗口
cv2.destroyAllWindows()
