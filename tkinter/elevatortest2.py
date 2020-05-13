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
import global_variable
from enum import Enum
import time
import threading

# *****************************************************************************
# 枚举类
# *****************************************************************************


Floor = Enum("Floor", ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                       "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"))

inside_ask = []
outside_ask = []
waiting_ask = []


class State(Enum):
    STOP = 0
    RUNNING = 1


class Direction(Enum):
    STOP = 0
    UP = 1
    DOWN = 2


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


def check_floor_legal(current_floor):
    if 0 <= current_floor <= 20:
        return True
    else:
        return False


# *****************************************************************************
# App类说明：应用程序主类，绘制GUI窗口，响应事件，完成ui更新
# 开发人员: @poros666 徐炳昌1850953
# 开发时间: 2020-5-5
# 开发注释: 本文件里ele为elevator的缩写
# *****************************************************************************


class App:

    # floor_select_variable = tk.StringVar()

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("%dx%d" % (1250, 950))  # 窗体尺寸
        tkui.center_window(self.root)  # 将窗体移动到屏幕中央
        self.root.iconbitmap(None)  # 窗体图标
        self.root.title("Elevator")
        self.root.resizable(False, False)  # 设置窗体不可改变大小
        self.root.protocol('WM_DELETE_WINDOW', self._close)  # 监听退出按键，弹出确认
        self.body()  # 绘制窗体组件

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
        for ele_num in range(1, 6):
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

        frame = tk.Frame(parent, name=frm_name, width=90, height=580, bg="white")
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
            button(frame, "  开  ", lambda: self._onclick_ele_open_close_button(int(frm_name[3]), 1),
                   name="open").pack(anchor=tk.N, padx=8, pady=8)
            button(frame, "  报警  ", lambda: self._onclick_ele_alarm_button(),
                   name="alarm").pack(anchor=tk.N, padx=8, pady=8)

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
            button(frame, "  关  ", lambda: self._onclick_ele_open_close_button(int(frm_name[3]), 1),
                   name="close").pack(anchor=tk.N, padx=8, pady=8)

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

        frame = tk.Frame(parent, name="frm_outside", width=200, bg="white")

        tkui.v_seperator(frame, width=5, bg="#AEBFA0").pack(side=tk.LEFT, fill=tk.Y)
        label(frame, "电梯外部按钮模拟区", 12, True).pack(anchor=tk.N, padx=20, pady=5)

        tkui.h_seperator(frame, 7)

        f1 = tk.Frame(frame, bg="white")
        label(f1, space(8) + "选择楼层数，在对应的楼层按下上下键").pack(side=tk.LEFT, pady=5)
        f1.pack(fill=tk.X)

        f2 = tk.Frame(frame, name="outside", bg="white")
        label(f2, space(5) + "*", fg="red").pack(side=tk.LEFT, pady=5)
        label(f2, "楼层:").pack(side=tk.LEFT)
        floor_select_box = ttk.Combobox(f2, name="floor_select_box")
        floor_select_box.pack(side=tk.LEFT)
        floor_select_box["value"] = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                                     "11", "12", "13", "14", "15", "16", "17", "18", "19", "20")  # 给下拉菜单设定值
        floor_select_box.current(0)  # 设定下拉菜单的默认值为第1个
        f2.pack(fill=tk.X)
        label(frame, "", 12, True).pack(anchor=tk.N, padx=20, pady=5)
        button(frame, "  上  ", lambda: self._onclick_ele_outside_button("U"),
               name="ele_up").pack(anchor=tk.N, padx=8, pady=8)
        button(frame, "  👇  ", lambda: self._onclick_ele_outside_button("D"),
               name="ele_down").pack(anchor=tk.N, padx=8, pady=8)

        return frame

    def down(self):
        """
        绘制底部的frame，包含电梯的显示屏
        :return: down frame
        """

        def label(frame, name, text, size=60, bold=True, bg="white", fg="black"):
            return tk.Label(frame, name=name, text=text, width=3, bg=bg, fg=fg, font=_ft(size, bold))

        def button(frame, text, command):
            return tk.Button(frame, text=text, bg="#303030", fg="white", command=command, font=_font())

        frame = tk.Frame(self.root, name="frm_scr", width=200, height=180, bg="white")
        tkui.v_seperator(frame, 14, bg="#FFFFFF").pack(side=tk.LEFT)
        label(frame, "ele_sc_1", "12↑↓").pack(side=tk.LEFT, fill=tk.Y)
        tkui.v_seperator(frame, 35, bg="#FFFFFF").pack(side=tk.LEFT)
        label(frame, "ele_sc_2", "12↑↓").pack(side=tk.LEFT, fill=tk.Y)
        tkui.v_seperator(frame, 35, bg="#FFFFFF").pack(side=tk.LEFT)
        label(frame, "ele_sc_3", "12↑↓").pack(side=tk.LEFT, fill=tk.Y)
        tkui.v_seperator(frame, 35, bg="#FFFFFF").pack(side=tk.LEFT)
        label(frame, "ele_sc_4", "12↑↓").pack(side=tk.LEFT, fill=tk.Y)
        tkui.v_seperator(frame, 35, bg="#FFFFFF").pack(side=tk.LEFT)
        label(frame, "ele_sc_5", "12↑↓").pack(side=tk.LEFT, fill=tk.Y)

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

    def _onclick_ele_inside_button(self, ele_part, ele_num=0, target_floor=0):
        # zhaodao but
        frm = self.root.children["frm_mainbody"]
        frm_l = frm.children["ele%d_L" % ele_num]
        frm_r = frm.children["ele%d_R" % ele_num]
        if ele_part == "L":
            but = frm_l.children["%d" % target_floor]
        else:
            but = frm_r.children["%d" % target_floor]
        # xiugai yanse
        if but["state"] == tk.NORMAL:
            but["state"] = tk.DISABLED
            but["bg"] = "#AEBFA0"
        # shengcheng ask
        ask = {"ele_part": ele_part, "ele_num": ele_num, "target_floor": target_floor}
        inside_ask.append(ask)

    def _onclick_ele_outside_button(self, target_direction):
        frm = self.root.children["frm_mainbody"]
        frm_out = frm.children["frm_outside"]
        out = frm_out.children["outside"]
        # print(out.children.items())
        box = out.children["floor_select_box"]
        if target_direction == "U":
            but = frm_out.children["ele_up"]
        else:
            but = frm_out.children["ele_down"]

        if but["state"] == tk.NORMAL:
            but["state"] = tk.DISABLED
            but["bg"] = "#AEBFA0"

        current_floor = box.get()
        ask = {"target_direction": target_direction, "current_floor": current_floor}
        outside_ask.append(ask)

    def _onclick_ele_open_close_button(self, ele_num=0, open=0):
        if ele.ele_set[ele_num]["state"] == State.STOP and ele.ele_set[ele_num]["direction"] == Direction.STOP:
            if open == 0:
                ele.ele_set[ele_num]["open"] = False
                print("door open")
            if open == 1:
                ele.ele_set[ele_num]["open"] = True
                print("door open")
        else:
            tkui.show_info("只有在停止的时候才能开门哦！")

    def _onclick_ele_alarm_button(self):
        tkui.show_info("已报警！")



class ElevatorSet:
    ele_set = {
        1: {"inside_queue": {}, "outside_up_queue": {}, "outside_down_queue": {}},
        2: {"inside_queue": {}, "outside_up_queue": {}, "outside_down_queue": {}},
        3: {"inside_queue": {}, "outside_up_queue": {}, "outside_down_queue": {}},
        4: {"inside_queue": {}, "outside_up_queue": {}, "outside_down_queue": {}},
        5: {"inside_queue": {}, "outside_up_queue": {}, "outside_down_queue": {}},
    }

    def __init__(self):
        for ele_num in range(1, 6):
            self.ele_set[ele_num]["floor"] = 1
            self.ele_set[ele_num]["state"] = State.STOP
            self.ele_set[ele_num]["direction"] = Direction.STOP
            self.ele_set[ele_num]["asked"] = False
            self.ele_set[ele_num]["open"] = False
            for j in range(1, 21):
                self.ele_set[ele_num]["inside_queue"][j] = 0
                self.ele_set[ele_num]["outside_up_queue"][j] = 0
                self.ele_set[ele_num]["outside_down_queue"][j] = 0


def watcher():
    def _test():
        # print(inside_ask)
        print(outside_ask)
        # print(ele.ele_set[1]["inside_queue"])
        # print("ele_set = ", ele.ele_set[1])
        # print(ele.ele_set[1]["outside_up_queue"])
        # print("print 2:", ele.ele_set[1]["outside_up_queue"][2])
        pass

    def _ele_move1():

        for ele_num in range(1, 6):
            '''if ele.ele_set[ele_num]["open"]:
                ele.ele_set[ele_num]["open"] = False
                print("door close")'''

            if ele.ele_set[ele_num]["state"] == State.STOP:
                if ele.ele_set[ele_num]["direction"] == Direction.UP:
                    if not _check_front_free(ele_num, ele.ele_set[ele_num]["floor"]):
                        #  ff not  / SU-->RU
                        print("SU-->RU")
                        ele.ele_set[ele_num]["state"] = State.RUNNING
                        ele.ele_set[ele_num]["direction"] = Direction.UP
                        ele.ele_set[ele_num]["open"] = False
                        print("door close")
                    else:
                        # ff yes / SU-->SS
                        print("SU-->SS")
                        ele.ele_set[ele_num]["state"] = State.STOP
                        ele.ele_set[ele_num]["direction"] = Direction.STOP
                        ele.ele_set[ele_num]["open"] = False
                        print("door close")
                if ele.ele_set[ele_num]["direction"] == Direction.DOWN:
                    if not _check_front_free(ele_num, ele.ele_set[ele_num]["floor"]):
                        #  ff not  / SD-->RD
                        print("SD-->RD")
                        ele.ele_set[ele_num]["state"] = State.RUNNING
                        ele.ele_set[ele_num]["direction"] = Direction.DOWN
                        ele.ele_set[ele_num]["open"] = False
                        print("door close")
                    elif _check_front_free(ele_num, ele.ele_set[ele_num]["floor"]):
                        # ff yes / SD-->SS
                        print("SD-->SS")
                        ele.ele_set[ele_num]["state"] = State.STOP
                        ele.ele_set[ele_num]["direction"] = Direction.STOP
                        ele.ele_set[ele_num]["open"] = False
                        print("door close")
                if ele.ele_set[ele_num]["direction"] == Direction.STOP:
                    flag_this_floor = False
                    if _check_ask_empty(ele_num, ele.ele_set[ele_num]["floor"]) == "this":
                        # SS-->SS  open door
                        ele.ele_set[ele_num]["state"] = State.STOP
                        ele.ele_set[ele_num]["direction"] = Direction.STOP
                        ele.ele_set[ele_num]["open"] = True
                        flag_this_floor = True
                        print("door open")
                    if _check_ask_empty(ele_num, ele.ele_set[ele_num]["floor"]) == "empty":
                        # SS-->SS
                        ele.ele_set[ele_num]["state"] = State.STOP
                        ele.ele_set[ele_num]["direction"] = Direction.STOP
                    if _check_ask_empty(ele_num, ele.ele_set[ele_num]["floor"]) == "up":
                        # SS-->RU
                        print("SS-->RU")
                        ele.ele_set[ele_num]["state"] = State.RUNNING
                        ele.ele_set[ele_num]["direction"] = Direction.UP
                    if _check_ask_empty(ele_num, ele.ele_set[ele_num]["floor"]) == "down":
                        # SS-->RD
                        print("SS-->RD")
                        ele.ele_set[ele_num]["state"] = State.RUNNING
                        ele.ele_set[ele_num]["direction"] = Direction.DOWN
                    if ele.ele_set[ele_num]["open"] and flag_this_floor == False:
                        ele.ele_set[ele_num]["open"] = False
                        print("door close")

            elif ele.ele_set[ele_num]["state"] == State.RUNNING:
                if ele.ele_set[ele_num]["direction"] == Direction.UP:
                    if ele.ele_set[ele_num]["inside_queue"][ele.ele_set[ele_num]["floor"]] == 1:
                        if _check_front_free(ele_num, ele.ele_set[ele_num]["floor"]) or ele.ele_set[ele_num]["floor"] == 20:
                            # ff1 or top     / RU-->SS
                            print("in RU-->SS")
                            ele.ele_set[ele_num]["state"] = State.STOP
                            ele.ele_set[ele_num]["direction"] = Direction.STOP
                            refresh_ele_inside_button(ele_num, ele.ele_set[ele_num]["floor"])
                        elif not _check_front_free(ele_num, ele.ele_set[ele_num]["floor"]):
                            # ff0     / RU-->SU
                            print("RU-->SU")
                            ele.ele_set[ele_num]["state"] = State.STOP
                            ele.ele_set[ele_num]["direction"] = Direction.UP
                            refresh_ele_inside_button(ele_num, ele.ele_set[ele_num]["floor"])
                        ele.ele_set[ele_num]["inside_queue"][ele.ele_set[ele_num]["floor"]] = 0
                        ele.ele_set[ele_num]["open"] = True
                        print("door open")
                    if ele.ele_set[ele_num]["outside_up_queue"][ele.ele_set[ele_num]["floor"]] == 1:
                        # up  / RU-->SU
                        print("RU-->SU")
                        ele.ele_set[ele_num]["state"] = State.STOP
                        ele.ele_set[ele_num]["direction"] = Direction.UP
                        # ref out up but
                        ele.ele_set[ele_num]["open"] = True
                        print("door open")
                        ele.ele_set[ele_num]["outside_up_queue"][ele.ele_set[ele_num]["floor"]] = 0
                    if ele.ele_set[ele_num]["outside_down_queue"][ele.ele_set[ele_num]["floor"]] == 1:
                        # down  / RU-->SD
                        ele.ele_set[ele_num]["state"] = State.STOP
                        ele.ele_set[ele_num]["direction"] = Direction.DOWN
                        ele.ele_set[ele_num]["outside_down_queue"][ele.ele_set[ele_num]["floor"]] = 0
                        ele.ele_set[ele_num]["open"] = True
                        print("door open")

                if ele.ele_set[ele_num]["direction"] == Direction.DOWN:
                    if ele.ele_set[ele_num]["inside_queue"][ele.ele_set[ele_num]["floor"]] == 1:
                        if _check_front_free(ele_num, ele.ele_set[ele_num]["floor"]) or ele.ele_set[ele_num]["floor"] == 0:
                            # ff1 or top     / RD-->SS
                            print("in RD-->SS")
                            ele.ele_set[ele_num]["state"] = State.STOP
                            ele.ele_set[ele_num]["direction"] = Direction.STOP
                            refresh_ele_inside_button(ele_num, ele.ele_set[ele_num]["floor"])
                        else:
                            # ff0     / RD-->SD
                            print("RD-->SD")
                            ele.ele_set[ele_num]["state"] = State.STOP
                            ele.ele_set[ele_num]["direction"] = Direction.DOWN
                            refresh_ele_inside_button(ele_num, ele.ele_set[ele_num]["floor"])
                        ele.ele_set[ele_num]["inside_queue"][ele.ele_set[ele_num]["floor"]] = 0
                        ele.ele_set[ele_num]["open"] = True
                        print("door open")
                    if ele.ele_set[ele_num]["outside_up_queue"][ele.ele_set[ele_num]["floor"]] == 1:
                        # up  / RD-->SU
                        ele.ele_set[ele_num]["state"] = State.STOP
                        ele.ele_set[ele_num]["direction"] = Direction.UP
                        # ref out up but
                        ele.ele_set[ele_num]["outside_up_queue"][ele.ele_set[ele_num]["floor"]] = 0
                        ele.ele_set[ele_num]["open"] = True
                        print("door open")
                    if ele.ele_set[ele_num]["outside_down_queue"][ele.ele_set[ele_num]["floor"]] == 1:
                        # down  / RD-->SD
                        ele.ele_set[ele_num]["state"] = State.STOP
                        ele.ele_set[ele_num]["direction"] = Direction.DOWN
                        ele.ele_set[ele_num]["outside_down_queue"][ele.ele_set[ele_num]["floor"]] = 0
                        ele.ele_set[ele_num]["open"] = True
                        print("door open")

                if ele.ele_set[ele_num]["direction"] == Direction.STOP:
                    pass


        for ele_num in range(1, 6):
            # 直接移动电梯
            '''if ele.ele_set[ele_num]["state"] == State.STOP and ele.ele_set[ele_num]["direction"] != Direction.STOP:
                ele.ele_set[ele_num]["state"] = State.RUNNING'''
            if ele.ele_set[ele_num]["state"] == State.RUNNING:
                if ele.ele_set[ele_num]["direction"] == Direction.UP:
                    print("up")
                    ele.ele_set[ele_num]["floor"] += 1
                elif ele.ele_set[ele_num]["direction"] == Direction.DOWN:
                    print("down")
                    ele.ele_set[ele_num]["floor"] -= 1

    def _ele_move():
        for ele_num in range(1, 6):
            if ele.ele_set[ele_num]["open"]:
                ele.ele_set[ele_num]["open"] = False
                print("door close")
            if ele.ele_set[ele_num]["asked"]:
                if ele.ele_set[ele_num]["inside_queue"][ele.ele_set[ele_num]["floor"]] == 1:
                    if _check_front_free(ele_num, ele.ele_set[ele_num]["floor"]):
                        # 前方无任务，到站，状态变停停
                        print("not got")
                        ele.ele_set[ele_num]["state"] = State.STOP
                        ele.ele_set[ele_num]["direction"] = Direction.STOP
                        refresh_ele_inside_button(ele_num, ele.ele_set[ele_num]["floor"])
                        ele.ele_set[ele_num]["asked"] = False
                        ele.ele_set[ele_num]["open"] = True
                    else:
                        # 前方仍有任务，到站，状态变停-
                        print("still got")
                        ele.ele_set[ele_num]["state"] = State.STOP
                        refresh_ele_inside_button(ele_num, ele.ele_set[ele_num]["floor"])
                    ele.ele_set[ele_num]["inside_queue"][ele.ele_set[ele_num]["floor"]] = 0
                if ele.ele_set[ele_num]["outside_up_queue"][ele.ele_set[ele_num]["floor"]] == 1:
                    pass
                if ele.ele_set[ele_num]["outside_down_queue"][ele.ele_set[ele_num]["floor"]] == 1:
                    pass
                print("im here", ele.ele_set[1]["state"], ele.ele_set[1]["direction"])
                # 直接移动电梯
                '''if ele.ele_set[ele_num]["state"] == State.STOP and ele.ele_set[ele_num]["direction"] != Direction.STOP:
                    ele.ele_set[ele_num]["state"] = State.RUNNING'''
                if ele.ele_set[ele_num]["state"] == State.RUNNING:
                    if ele.ele_set[ele_num]["direction"] == Direction.UP:
                        print("up")
                        ele.ele_set[ele_num]["floor"] += 1
                    elif ele.ele_set[ele_num]["direction"] == Direction.DOWN:
                        print("down")
                        ele.ele_set[ele_num]["floor"] -= 1

    def _check_ask(ele_num, cur_floor):
        pass

    def _check_front_free(ele_num, cur_floor):
        flag = True
        if ele.ele_set[ele_num]["direction"] == Direction.UP:
            for i in range(cur_floor + 1, 20):
                if ele.ele_set[ele_num]["inside_queue"][i] == 1:
                    flag = False
                    break
                if ele.ele_set[ele_num]["outside_up_queue"][i] == 1:
                    flag = False
                    break
                if ele.ele_set[ele_num]["outside_down_queue"][i] == 1:
                    flag = False
                    break
        elif ele.ele_set[ele_num]["direction"] == Direction.UP:
            for i in range(20, cur_floor):
                if ele.ele_set[ele_num]["inside_queue"][i] == 1:
                    flag = False
                    break
                if ele.ele_set[ele_num]["outside_up_queue"][i] == 1:
                    flag = False
                    break
                if ele.ele_set[ele_num]["outside_down_queue"][i] == 1:
                    flag = False
                    break
        print("_check_front_free:", flag)
        return flag

    def _check_ask_empty(ele_num, cur_floor):

        flag = "empty"
        for i in range(cur_floor + 1, 20):
            if ele.ele_set[ele_num]["inside_queue"][i] == 1:
                flag = "up"
                break
            if ele.ele_set[ele_num]["outside_up_queue"][i] == 1:
                flag = "up"
                break
            if ele.ele_set[ele_num]["outside_down_queue"][i] == 1:
                flag = "up"
                break
        for i in range(1, cur_floor):
            if ele.ele_set[ele_num]["inside_queue"][i] == 1:
                flag = "down"
                break
            if ele.ele_set[ele_num]["outside_up_queue"][i] == 1:
                flag = "down"
                break
            if ele.ele_set[ele_num]["outside_down_queue"][i] == 1:
                flag = "down"
                break
        if ele.ele_set[ele_num]["inside_queue"][cur_floor] == 1:
            flag = "this"
            ele.ele_set[ele_num]["inside_queue"][cur_floor] = 0
            refresh_ele_inside_button(ele_num, cur_floor)
        if ele.ele_set[ele_num]["outside_up_queue"][cur_floor] == 1:
            flag = "this"
            ele.ele_set[ele_num]["outside_up_queue"][cur_floor] = 0
        if ele.ele_set[ele_num]["outside_down_queue"][cur_floor] == 1:
            ele.ele_set[ele_num]["outside_down_queue"][cur_floor] = 0
            flag = "this"

        return flag

    def _main():
        while True:
            time.sleep(2)
            _test()
            mutex.acquire()
            _ele_move1()
            mutex.release()

    t = threading.Thread(target=_main, name="watcher")  # guanbi xaincheng
    t.daemon = True
    t.start()


def refresher():
    # 刷新指令队列以及电梯状态---调度指令
    def _refresh_ask():
        mutex.acquire()
        _refresh_inside_ask()
        _refresh_outside_ask()
        mutex.release()

    def _refresh_inside_ask():
        for ask in inside_ask:
            ele.ele_set[ask["ele_num"]]["inside_queue"][ask["target_floor"]] = 1
            ele.ele_set[ask["ele_num"]]["asked"] = True
            # print("ccc", ele.ele_set[ask["ele_num"]]["state"], ele.ele_set[ask["ele_num"]]["direction"])
            # 对静止的电梯给与初动力
            if ele.ele_set[ask["ele_num"]]["state"] == State.STOP and ele.ele_set[ask["ele_num"]][
                "direction"] == Direction.STOP:
                # print("bbb")
                if ele.ele_set[ask["ele_num"]]["floor"] < ask["target_floor"]:
                    ele.ele_set[ask["ele_num"]]["state"] = State.RUNNING
                    ele.ele_set[ask["ele_num"]]["direction"] = Direction.UP
                    # print("aaa", ele.ele_set[ask["ele_num"]]["state"], ele.ele_set[ask["ele_num"]]["direction"])
                elif ele.ele_set[ask["ele_num"]]["floor"] > ask["target_floor"]:
                    ele.ele_set[ask["ele_num"]]["state"] = State.RUNNING
                    ele.ele_set[ask["ele_num"]]["direction"] = Direction.DOWN
        inside_ask.clear()

    def _refresh_outside_ask():
        possible_ele = {}
        for ask in outside_ask:
            if ask["target_direction"] == "U":
                for ele_num in range(1, 6):
                    if ele.ele_set[ele_num]["direction"] == Direction.STOP:
                        possible_ele[ele_num] = _ele_distance(ele_num, ask["current_floor"])
                        #print(ele_num, _ele_distance(ele_num, ask["current_floor"]))
                    if ele.ele_set[ele_num]["direction"] == Direction.UP and ele.ele_set[ele_num]["floor"] <= int(ask[
                        "current_floor"]):
                        possible_ele[ele_num] = _ele_distance(ele_num, ask["current_floor"])
                        #print(ele_num, _ele_distance(ele_num, ask["current_floor"]))
                if len(possible_ele) == 0:
                    pass
                else:
                    a = sorted(possible_ele.items(), key=lambda item: item[1])  # mkd
                    ele.ele_set[a[0][0]]["outside_up_queue"][int(ask["current_floor"])] = 1
                    outside_ask.remove(ask)

            elif ask["target_direction"] == "D":
                print("ask:", ask)
                for ele_num in range(1, 6):
                    if ele.ele_set[ele_num]["direction"] == Direction.STOP:
                        possible_ele[ele_num] = _ele_distance(ele_num, ask["current_floor"])
                        # print(ele_num, _ele_distance(ele_num, ask["current_floor"]))
                    if ele.ele_set[ele_num]["direction"] == Direction.DOWN and ele.ele_set[ele_num]["floor"] >= int(ask[
                                                                                                                        "current_floor"]):
                        possible_ele[ele_num] = _ele_distance(ele_num, ask["current_floor"])
                        # print(ele_num, _ele_distance(ele_num, ask["current_floor"]))
                if len(possible_ele) == 0:
                    pass
                else:
                    a = sorted(possible_ele.items(), key=lambda item: item[1])  # mkd
                    ele.ele_set[a[0][0]]["outside_down_queue"][int(ask["current_floor"])] = 1
                    outside_ask.remove(ask)



    def _ele_distance(ele_num, current_floor):
        return abs(ele.ele_set[ele_num]["floor"] - int(current_floor))
    # 刷新电梯状态表
    def _refresh_ele_state():
        pass



    # 根据当前选择的外楼层号刷新上下按钮状态
    def _refresh_outside_but():

        flag_up = 0
        flag_down = 0
        frm = app.root.children["frm_mainbody"]
        frm_out = frm.children["frm_outside"]
        out = frm_out.children["outside"]
        # print(out.children.items())
        box = out.children["floor_select_box"]
        current_floor = box.get()
        # (current_floor)

        for i in range(1, 6):
            if ele.ele_set[i]["outside_up_queue"][int(current_floor)] == 1:
                flag_up = 1
                break
        if flag_up == 0:
            but = frm_out.children["ele_up"]
            but["state"] = tk.NORMAL
            but["bg"] = "#9DA2AD"
        else:
            but = frm_out.children["ele_up"]
            but["state"] = tk.DISABLED
            but["bg"] = "#AEBFA0"

        for i in range(1, 6):
            if ele.ele_set[i]["outside_down_queue"][int(current_floor)] == 1:
                flag_down = 1
                break
        if flag_down == 0:
            but = frm_out.children["ele_down"]
            but["state"] = tk.NORMAL
            but["bg"] = "#9DA2AD"
        else:
            but = frm_out.children["ele_down"]
            but["state"] = tk.DISABLED
            but["bg"] = "#AEBFA0"

    def _main():
        while True:
            time.sleep(0.1)
            _refresh_ask()
            _refresh_ele_state()
            #_refresh_screen()
            _refresh_outside_but()

    t = threading.Thread(target=_main, name="refresher")  # guanbi xaincheng
    t.daemon = True
    t.start()

def refresh_screens():
    # 根据各个电梯状态及楼层刷新显示屏内容
    def _refresh_screen():
        frm = app.root.children["frm_scr"]
        for i in range(1, 6):
            if ele.ele_set[i]["state"] == State.STOP:
                if ele.ele_set[i]["open"]:
                    frm.children["ele_sc_%d" % i]["text"] = "开%d" % ele.ele_set[i]["floor"]
                else:
                    frm.children["ele_sc_%d" % i]["text"] = "%d" % ele.ele_set[i]["floor"]
            if ele.ele_set[i]["direction"] == Direction.UP and ele.ele_set[i]["open"] == False:
                frm.children["ele_sc_%d" % i]["text"] = "%d↑" % ele.ele_set[i]["floor"]
            if ele.ele_set[i]["direction"] == Direction.DOWN and ele.ele_set[i]["open"] == False:
                frm.children["ele_sc_%d" % i]["text"] = "%d↓" % ele.ele_set[i]["floor"]
    def _main():
        while True:
            time.sleep(0.1)
            #mutex.acquire()
            _refresh_screen()
            #mutex.release()

    t = threading.Thread(target=_main, name="refresher")  # guanbi xaincheng
    t.daemon = True
    t.start()

def refresh_ele_inside_button(ele_num=0, target_floor=0):
    # zhaodao but
    frm = app.root.children["frm_mainbody"]
    frm_l = frm.children["ele%d_L" % ele_num]
    frm_r = frm.children["ele%d_R" % ele_num]
    ele_part = "R"
    if 0 <= target_floor <= 10:
        ele_part = "L"

    if ele_part == "L":
        but = frm_l.children["%d" % target_floor]
    else:
        but = frm_r.children["%d" % target_floor]
    but["state"] = tk.NORMAL
    but["bg"] = "#9DA2AD"


if __name__ == "__main__":
    ele = ElevatorSet()
    '''print(ele.ele_set[1]["state"])
    ele.ele_set[1]["inside_queue"][3] = 0
    ele.ele_set[1]["inside_queue"][20] = 0
    for items in ele.ele_set[1]["inside_queue"].items():
        if items[0] == 4:
            print(items[1])'''
    app = App()  # 实例化
    mutex = threading.Lock()  # 创建一把锁
    app.root.after(0, watcher)
    app.root.after(0, refresher)
    app.root.after(0, refresh_screens())

    app.root.mainloop()  # 启动主循环
