# import cv2
# import numpy as np
#
# # 创建一个黑色的图像
# img = np.zeros((512, 512, 3), np.uint8)
#
# # 获取用户输入的坐标
# x = int(input("请输入横坐标："))
# y = int(input("请输入纵坐标："))
#
# # 在指定坐标处绘制圆
# cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
#
# # 显示图像
# cv2.imshow("image", img)
# cv2.imwrite('image.jpg', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

import cv2
import numpy as np

img_size = (640, 480)  # 图像尺寸
bg_color = (255, 255, 255)  # 背景色为白色
radius = 10  # 原点半径
color = (0, 0, 255)  # 原点颜色为蓝色
thickness = -1  # 填充圆形
delay = 500  # 帧率为20帧/秒，每帧显示50毫秒

def draw_circles(img, x, y):
    for i in range(len(x)):
        center = (int(x[i]), int(y[i]))
        cv2.circle(img, center, radius, color, thickness)

def main():
    # 读取数据
    x = np.loadtxt("x_data.txt")
    y = np.loadtxt("y_data.txt")

    # 创建窗口
    cv2.namedWindow("Animation")

    # 绘制动画
    for i in range(len(x)):
        # 创建一个空白图像
        img = np.zeros((img_size[1], img_size[0], 3), dtype=np.uint8)
        img[:, :] = bg_color

        # 在图像上绘制原点
        draw_circles(img, x[:i+1], y[:i+1])

        # 显示图像
        cv2.imshow("Animation", img)

        # 按下ESC键退出程序
        if cv2.waitKey(delay) == 27:
            break

    # 关闭窗口
    cv2.destroyAllWindows()

def main():
    # 读取数据
    x = np.loadtxt("x_data.txt")
    y = np.loadtxt("y_data.txt")

    # 创建窗口
    cv2.namedWindow("Animation")

    # 绘制动画
    for i in range(len(x)):
        # 创建一个空白图像
        img = np.zeros((img_size[1], img_size[0], 3), dtype=np.uint8)
        img[:, :] = bg_color

        # 在图像上绘制原点
        draw_circles(img, x[:i+1], y[:i+1])

        # 显示图像
        cv2.imshow("Animation", img)

        # 按下ESC键退出程序
        if cv2.waitKey(delay) == 27:
            break

    # 关闭窗口
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
