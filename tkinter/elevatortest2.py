# coding:utf-8

# *****************************************************************************
# 开发人员: @poros666 徐炳昌1850953
# 开发时间: 2020-5-5
# *****************************************************************************

import tkinter as tk
import tkinter.font as tkfont
from PIL import Image
import tkutils as tkui
import os


def _font(fname="微软雅黑", size=9, bold=tkfont.NORMAL):
    """
    设置字体
    :param fname: 字体种类
    :param size: 大小
    :param bold: 粗体与否，用tkfont.表示
    :return: 返回字体字典
    """
    ft = tkfont.Font(family=fname, size=size, weight=bold)
    return ft


def _ft(size=12, bold=False):
    """
    简单版字体设置
    :param size: 大小
    :param bold: 粗体与否，用tkfont.表示
    :return: 返回字体字典
    """
    if bold:
        return _font(size=size, bold=tkfont.BOLD)
    else:
        return _font(size=size, bold=tkfont.NORMAL)

# *****************************************************************************
# App类说明：应用程序主类，绘制GUI窗口，响应事件，完成ui更新
# 开发人员: @poros666 徐炳昌1850953
# 开发时间: 2020-5-5
# *****************************************************************************


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("%dx%d" % (1200, 950))           # 窗体尺寸
        tkui.center_window(self.root)                       # 将窗体移动到屏幕中央
        self.root.iconbitmap(None)       # 窗体图标
        self.root.title("Elevator")
        self.root.resizable(False, False)                   # 设置窗体不可改变大小
        self.root.protocol('WM_DELETE_WINDOW', self.close)  # 监听退出按键，弹出确认
        self.body()# 绘制窗体组件

    def body(self):
        """
        绘制主要窗体，将各个部分的frame pack起来
        :return: 无
        """
        frm_title = self.title()
        frm_title.pack(fill=tk.X)

        frm_main = self.main_body()
        frm_main.pack(expand=tk.YES, fill=tk.X)

        frm_ele = self.down()
        frm_ele.pack(fill=tk.X)

        frm_bottom = self.bottom()
        frm_bottom.pack(fill=tk.X)

    def title(self):
        """
        绘制标题栏
        :return:标题栏frame
        """
        def label(frame, text, size, bold=False):
            return tk.Label(frame, text=text, bg="#AEBFA0", fg="white", height=2, font=_ft(size, bold))
        def button(frame, text, command):
            return tk.Button(frame, text=text, bg="#9DA2AD", fg="white", command=command, font=_font())

        frame = tk.Frame(self.root, bg="#AEBFA0")

        button(frame, "收起提示", self.info_close_up).pack(side=tk.LEFT, padx=10)
        button(frame, "打开提示", self.info_show_down).pack(side=tk.LEFT, padx=100)
        label(frame, "", 12).pack(side=tk.LEFT, padx=0)
        label(frame, "电梯调度模拟器", 20).pack(side=tk.LEFT, padx=100)
        label(frame, "", 12).pack(side=tk.RIGHT, padx=20)
        label(frame, "制作者：徐炳昌1850953", 12).pack(side=tk.RIGHT, padx=20)
        #tkui.image_label(frame, "images\\user.png", 40, 40, False).pack(side=tk.RIGHT)

        return frame

    def bottom(self):
        """
        绘制底栏
        :return:=底栏frame
        """
        frame = tk.Frame(self.root, height=20, bg="#AEBFA0")
        frame.propagate(True)
        return frame

    def main_body(self):
        """
        绘制中央部分
        :return: 中央frame
        """
        frame = tk.Frame(self.root, name="frm_mainbody", bg="whitesmoke")

        self.main_info(frame).pack(fill=tk.X, padx=30, pady=15)
        for ele_num in range(1,6):
            tkui.v_seperator(frame, width=10).pack(side=tk.LEFT, fill=tk.Y)
            self.main_ele_part(frame, "ele%d_L" % ele_num).pack(side=tk.LEFT, fill=tk.Y)
            self.main_ele_part(frame, "ele%d_R" % ele_num).pack(side=tk.LEFT, fill=tk.Y)

        tkui.v_seperator(frame, width=5).pack(side=tk.LEFT, fill=tk.Y)
        self.main_right(frame).pack(side=tk.TOP, expand=tk.YES, fill=tk.X)
        tkui.v_seperator(frame, width=5).pack(side=tk.LEFT, fill=tk.Y)

        return frame

    def main_info(self, parent):
        """
        绘制中央部分的提示栏
        :param parent: 该frame的父控件
        :return: info frame
        """
        def label(frame, text, size=12):
            return tk.Label(frame, bg="white", fg="gray", text=text, font=_ft(size))
        def button(frame, text, command):
            return tk.Button(frame, text=text, width=5,
                             bg="whitesmoke", fg="gray", command=command, font=_font())
        frame = tk.Frame(parent, name="frm_maininfo", bg="white", height=100)
        self.main_info_middle(frame).pack(side=tk.LEFT)
        button(frame, "收起^", self.info_close_up).pack(side=tk.RIGHT, padx=10)
        frame.propagate(False)
        return frame

    def main_info_middle(self, parent):
        """
        绘制info的中间部分
        :param parent: 该frame的父控件
        :return: info mid frame
        """
        str1 = "中间左侧部分的五组按钮表示了对应的电梯内部的按钮，按下即表示该电梯内乘客想去哪一层。"
        str2 = "中间右侧部分表示复选框对应的楼层的上下等电梯按钮，按下白哦是电梯外乘客想上或下。"
        str3 = "下方五个方格对应五部电梯的显示屏，其显示该电梯当前楼层。"

        def label(frame, text):
            return tk.Label(frame, bg="white", fg="gray", text=text, font=_ft(12))

        frame = tk.Frame(parent, bg="white")

        label(frame, str1).pack(anchor=tk.W, padx=10)
        label(frame, str2).pack(anchor=tk.W, padx=10, pady=2)
        label(frame, str2).pack(anchor=tk.W, padx=10)

        return frame

    def main_ele_part(self, parent, frm_name):
        """
        绘制电梯内部件
        :param parent: 该frame的父控件
        :param frm_name: 该电梯部件的名字
        :return: ele frame
        """
        def label(frame, text, size=10, bold=True, bg="white"):
            return tk.Label(frame, text=text, bg=bg, font=_ft(size, bold))
        def button(frame, text, command):
            return tk.Button(frame, text=text, width=30,
                             bg="#9DA2AD", fg="white", command=command, font=_font())
        frame = tk.Frame(parent, name=frm_name, width=90, height=500, bg="white")
        if frm_name[-1]=="L":
            for i in range(1, 11):
                button(frame, "  %d  " % i, None).pack(anchor=tk.N, padx=8, pady=8)
            tkui.v_seperator(frame, width=5, bg="#AEBFA0").pack(side=tk.LEFT, fill=tk.Y)
            label(frame, frm_name[3] + "号电梯", bg="whitesmoke").pack(anchor=tk.W, expand=True, fill=tk.BOTH)
        else:
            for i in range(11, 21):
                button(frame, "  %d  " % i, None).pack(anchor=tk.N, padx=8, pady=8)

        frame.propagate(False)
        return frame

    def main_right(self, parent):
        """
        绘制右侧的框架，包含电梯外的操作区
        :param parent: 该frame的父控件
        :return: right frame
        """
        def label(frame, text, size=10, bold=False, fg="black"):
            return tk.Label(frame, text=text, bg="white", fg=fg, font=_ft(size, bold))

        def space(n):
            s = " "
            r = ""
            for i in range(n):
                r += s
            return r

        frame = tk.Frame(parent, width=200, bg="white")

        label(frame, "创建模型", 12, True).pack(anchor=tk.W, padx=20, pady=5)

        tkui.h_seperator(frame)

        f1 = tk.Frame(frame, bg="white")
        label(f1, space(8) + "模型类别:").pack(side=tk.LEFT, pady=5)
        label(f1, "图像分类").pack(side=tk.LEFT, padx=20)
        f1.pack(fill=tk.X)

        f2 = tk.Frame(frame, bg="white")
        label(f2, space(5) + "*", fg="red").pack(side=tk.LEFT, pady=5)
        label(f2, "模型名称:").pack(side=tk.LEFT)
        tk.Entry(f2, bg="white", font=_ft(10), width=25).pack(side=tk.LEFT, padx=20)
        f2.pack(fill=tk.X)

        f3 = tk.Frame(frame, bg="white")
        label(f3, space(5) + "*", fg="red").pack(side=tk.LEFT, pady=5)
        label(f3, "联系方式:").pack(side=tk.LEFT)
        tk.Entry(f3, bg="white", font=_ft(10), width=25).pack(side=tk.LEFT, padx=20)
        f3.pack(fill=tk.X)

        f4 = tk.Frame(frame, bg="white")
        label(f4, space(5) + "*", fg="red").pack(side=tk.LEFT, anchor=tk.N, pady=5)
        label(f4, "功能描述:").pack(side=tk.LEFT, anchor=tk.N, pady=5)
        tk.Text(f4, bg="white", font=_ft(10), height=10, width=40).pack(side=tk.LEFT, padx=20, pady=5)
        f4.pack(fill=tk.X)

        #ttk.Button(frame, text="下一步", width=12).pack(anchor=tk.W, padx=112, pady=5)

        return frame

    def down(self):
        """
        绘制底部的frame，包含电梯的显示屏
        :return: down frame
        """
        def label(frame, text, size=10, bold=False, bg="white"):
            return tk.Label(frame, text=text, bg=bg, font=_ft(size, bold))
        def button(frame, text, command):
            return tk.Button(frame, text=text, bg="#303030", fg="white", command=command, font=_font())

        frame = tk.Frame(self.root, height=180, width=200, bg="white")

        can1 = tk.Canvas(frame, width=200, height=200, bg="black")

        frame.propagate(False)
        return frame

    def info_close_up(self):
        """
        用于隐藏提示栏的函数
        :return: 无
        """
        frm1 = self.root.children["frm_mainbody"]
        frm2 = frm1.children["frm_maininfo"]
        frm2.pack_forget()

    def info_show_down(self):
        """
        用于显示提示栏的函数
        :return: 无
        """
        frm1 = self.root.children["frm_mainbody"]
        frm2 = frm1.children["frm_maininfo"]
        frm2.pack()

    def close(self):
        """
        用于在用户退出时确认
        :return: 无
        """
        if tkui.show_confirm("Confirm Exit?"):
            self.root.destroy()


if __name__ == "__main__":
    app = App()             # 实例化
    app.root.mainloop()     # 启动主循环
