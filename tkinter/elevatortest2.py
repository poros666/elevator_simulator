# coding:utf-8

# *****************************************************************************
# 开发人员: @poros666 徐炳昌1850953
# 开发时间: 2020-5-6
# *****************************************************************************

import tkinter as tk
import tkinter.font as tkfont
from PIL import Image
import tkutils as tkui
import os
from tkinter import ttk


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
# 开发注释: 本文件里ele为elevator的缩写
# *****************************************************************************


class App:

    #floor_select_variable = tk.StringVar()

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("%dx%d" % (1250, 950))           # 窗体尺寸
        tkui.center_window(self.root)                       # 将窗体移动到屏幕中央
        self.root.iconbitmap(None)       # 窗体图标
        self.root.title("Elevator")
        self.root.resizable(False, False)                   # 设置窗体不可改变大小
        self.root.protocol('WM_DELETE_WINDOW', self._close)  # 监听退出按键，弹出确认
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

    # ****************************************************************************
    # 以下是界面布局所需的函数                                                        #
    # ****************************************************************************

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

        button(frame, "收起提示", self._info_close_up).pack(side=tk.LEFT, padx=10)
        button(frame, "打开提示", self._info_show_down).pack(side=tk.LEFT, padx=100)
        label(frame, "", 12).pack(side=tk.LEFT, padx=0)
        label(frame, "电梯调度模拟器", 20).pack(side=tk.LEFT, padx=100)
        label(frame, "", 12).pack(side=tk.RIGHT, padx=20)
        label(frame, "制作者：徐炳昌1850953", 12).pack(side=tk.RIGHT, padx=20)
        
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
        self.main_right(frame).pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
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
        button(frame, "收起^", self._info_close_up).pack(side=tk.RIGHT, padx=10)
        frame.propagate(False)
        
        return frame

    def main_info_middle(self, parent):
        """
        绘制info的中间部分
        :param parent: 该frame的父控件
        :return: info mid frame
        """
        str1 = "左侧部分的五组按钮表示了对应的电梯内部的按钮，按下即表示该电梯内乘客想去哪一层。"
        str2 = "右侧复选框选择对应的楼层，按上下等电梯按钮，就表示该层电梯外乘客想上或下。"
        str3 = "下方五个方格对应五部电梯的显示屏，其显示该电梯当前楼层以及上下方向。"

        def label(frame, text):
            return tk.Label(frame, bg="white", fg="gray", text=text, font=_ft(12))

        frame = tk.Frame(parent, bg="white")

        label(frame, str1).pack(anchor=tk.W, padx=10)
        label(frame, str2).pack(anchor=tk.W, padx=10, pady=2)
        label(frame, str3).pack(anchor=tk.W, padx=10)

        return frame

    def main_ele_part(self, parent, frm_name):
        """
        绘制电梯内部件，包含电梯内部所有的按钮
        :param parent: 该frame的父控件
        :param frm_name: 该电梯部件的名字
        :return: ele frame
        """
        def label(frame, text, size=10, bold=True, bg="white"):
            return tk.Label(frame, text=text, bg=bg, font=_ft(size, bold))

        def button(frame, text, command, name):
            return tk.Button(frame, text=text, width=30,
                             bg="#9DA2AD", fg="white",
                             state=tk.NORMAL, command=command, name=name, font=_font())
        frame = tk.Frame(parent, name=frm_name, width=90, height=500, bg="white")
        if frm_name[-1] == "L":
            button(frame, "  1  ", lambda: self._onclick_ele_inside_button("L", int(frm_name[3]), 1),
                   name="1").pack(anchor=tk.N, padx=8, pady=8)
            button(frame, "  2  ", lambda: self._onclick_ele_inside_button("L", int(frm_name[3]), 2),
                   name="2").pack(anchor=tk.N, padx=8, pady=8)
            button(frame, "  3  ", lambda: self._onclick_ele_inside_button("L", int(frm_name[3]), 3),
                   name="3").pack(anchor=tk.N, padx=8, pady=8)
            button(frame, "  4  ", lambda: self._onclick_ele_inside_button("L", int(frm_name[3]), 4),
                   name="4").pack(anchor=tk.N, padx=8, pady=8)
            button(frame, "  5  ", lambda: self._onclick_ele_inside_button("L", int(frm_name[3]), 5),
                   name="5").pack(anchor=tk.N, padx=8, pady=8)
            button(frame, "  6  ", lambda: self._onclick_ele_inside_button("L", int(frm_name[3]), 6),
                   name="6").pack(anchor=tk.N, padx=8, pady=8)
            button(frame, "  7  ", lambda: self._onclick_ele_inside_button("L", int(frm_name[3]), 7),
                   name="7").pack(anchor=tk.N, padx=8, pady=8)
            button(frame, "  8  ", lambda: self._onclick_ele_inside_button("L", int(frm_name[3]), 8),
                   name="8").pack(anchor=tk.N, padx=8, pady=8)
            button(frame, "  9  ", lambda: self._onclick_ele_inside_button("L", int(frm_name[3]), 9),
                   name="9").pack(anchor=tk.N, padx=8, pady=8)
            button(frame, "  10  ", lambda: self._onclick_ele_inside_button("L", int(frm_name[3]), 10),
                   name="10").pack(anchor=tk.N, padx=8, pady=8)

            tkui.v_seperator(frame, width=5, bg="#AEBFA0").pack(side=tk.LEFT, fill=tk.Y)

            label(frame, frm_name[3] + "号电梯", bg="whitesmoke").pack(anchor=tk.W, expand=True, fill=tk.BOTH)
        else:
            button(frame, "  11  ", lambda: self._onclick_ele_inside_button("R", int(frm_name[3]), 11),
                   name="11").pack(anchor=tk.N, padx=8, pady=8)
            button(frame, "  12  ", lambda: self._onclick_ele_inside_button("R", int(frm_name[3]), 12),
                   name="12").pack(anchor=tk.N, padx=8, pady=8)
            button(frame, "  13  ", lambda: self._onclick_ele_inside_button("R", int(frm_name[3]), 13),
                   name="13").pack(anchor=tk.N, padx=8, pady=8)
            button(frame, "  14  ", lambda: self._onclick_ele_inside_button("R", int(frm_name[3]), 14),
                   name="14").pack(anchor=tk.N, padx=8, pady=8)
            button(frame, "  15  ", lambda: self._onclick_ele_inside_button("R", int(frm_name[3]), 15),
                   name="15").pack(anchor=tk.N, padx=8, pady=8)
            button(frame, "  16  ", lambda: self._onclick_ele_inside_button("R", int(frm_name[3]), 16),
                   name="16").pack(anchor=tk.N, padx=8, pady=8)
            button(frame, "  17  ", lambda: self._onclick_ele_inside_button("R", int(frm_name[3]), 17),
                   name="17").pack(anchor=tk.N, padx=8, pady=8)
            button(frame, "  18  ", lambda: self._onclick_ele_inside_button("R", int(frm_name[3]), 18),
                   name="18").pack(anchor=tk.N, padx=8, pady=8)
            button(frame, "  19  ", lambda: self._onclick_ele_inside_button("R", int(frm_name[3]), 19),
                   name="19").pack(anchor=tk.N, padx=8, pady=8)
            button(frame, "  20  ", lambda: self._onclick_ele_inside_button("R", int(frm_name[3]), 20),
                   name="20").pack(anchor=tk.N, padx=8, pady=8)

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

        def button(frame, text, command, name):
            return tk.Button(frame, text=text, width=20, height=8,
                             bg="#9DA2AD", fg="white",
                             state=tk.NORMAL, command=command, name=name, font=_font())

        def space(n):
            s = " "
            r = ""
            for i in range(n):
                r += s
            return r

        frame = tk.Frame(parent, width=200, bg="white")

        tkui.v_seperator(frame, width=5, bg="#AEBFA0").pack(side=tk.LEFT, fill=tk.Y)
        label(frame, "电梯外部按钮模拟区", 12, True).pack(anchor=tk.N, padx=20, pady=5)

        tkui.h_seperator(frame, 7)

        f1 = tk.Frame(frame, bg="white")
        label(f1, space(8) + "选择楼层数，在对应的楼层按下上下键").pack(side=tk.LEFT, pady=5)
        f1.pack(fill=tk.X)

        f2 = tk.Frame(frame, bg="white")
        label(f2, space(5) + "*", fg="red").pack(side=tk.LEFT, pady=5)
        label(f2, "楼层:").pack(side=tk.LEFT)
        floor_select_box = ttk.Combobox(f2)
        floor_select_box.pack(side=tk.LEFT)
        floor_select_box["value"] = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                                     "11", "12", "13", "14", "15", "16", "17", "18", "19", "20")   #给下拉菜单设定值
        floor_select_box.current(0)         #设定下拉菜单的默认值为第1个
        f2.pack(fill=tk.X)
        label(frame, "", 12, True).pack(anchor=tk.N, padx=20, pady=5)
        button(frame, "  上  ", lambda: self._onclick_ele_inside_button("R", int(frm_name[3]), 20),
               name="ele_up").pack(anchor=tk.N, padx=8, pady=8)
        button(frame, "  👇  ", lambda: self._onclick_ele_inside_button("R", int(frm_name[3]), 20),
               name="ele_down").pack(anchor=tk.N, padx=8, pady=8)

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

        frame = tk.Frame(self.root, width=200, height=180, bg="white")

        tkui.v_seperator(frame, 5, bg="#FFFFFF").pack(side=tk.LEFT)
        can1 = tk.Canvas(frame, width=160, height=160, bg="black").pack(side=tk.LEFT, padx=10, pady=10)
        tkui.v_seperator(frame, 7, bg="#FFFFFF").pack(side=tk.LEFT)
        can2 = tk.Canvas(frame, width=160, height=160, bg="black").pack(side=tk.LEFT, padx=10, pady=10)
        tkui.v_seperator(frame, 7, bg="#FFFFFF").pack(side=tk.LEFT)
        can3 = tk.Canvas(frame, width=160, height=160, bg="black").pack(side=tk.LEFT, padx=10, pady=10)
        tkui.v_seperator(frame, 7, bg="#FFFFFF").pack(side=tk.LEFT)
        can4 = tk.Canvas(frame, width=160, height=160, bg="black").pack(side=tk.LEFT, padx=10, pady=10)
        tkui.v_seperator(frame, 7, bg="#FFFFFF").pack(side=tk.LEFT)
        can5 = tk.Canvas(frame, width=160, height=160, bg="black").pack(side=tk.LEFT, padx=10, pady=10)

        frame.propagate(False)
        
        return frame

    # ****************************************************************************
    # 以下是按钮调用的函数                                                           #
    # ****************************************************************************

    def _info_close_up(self):
        """
        用于隐藏提示栏的函数
        :return: 无
        """
        frm1 = self.root.children["frm_mainbody"]
        frm2 = frm1.children["frm_maininfo"]
        frm2.pack_forget()

    def _info_show_down(self):
        """
        用于显示提示栏的函数
        :return: 无
        """
        frm1 = self.root.children["frm_mainbody"]
        frm2 = frm1.children["frm_maininfo"]
        frm2.pack()

    def _close(self):
        """
        用于在用户退出时确认
        :return: 无
        """
        if tkui.show_confirm("Confirm Exit?"):
            self.root.destroy()

    def _onclick_ele_inside_button(self, ele_part, ele_num="0", target_floor="0"):
        frm = self.root.children["frm_mainbody"]
        frm_l = frm.children["ele%d_L" % ele_num]
        frm_r = frm.children["ele%d_R" % ele_num]
        if ele_part == "L":
            but = frm_l.children["%d" % target_floor]
        else:
            but = frm_r.children["%d" % target_floor]
        if but["state"] == tk.NORMAL:
            but["state"] = tk.DISABLED
            but["bg"] = "#AEBFA0"
        else:
            but["state"] = tk.NORMAL
            but["bg"] = "#9DA2AD"


if __name__ == "__main__":
    app = App()             # 实例化
    app.root.mainloop()     # 启动主循环
