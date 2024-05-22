# 该脚本实现了在本地扫码自动打印功能，并可对扫码数字再处理。
# 1.创建标签模板scantoprint.yix 使用数据源scandata.csv
# 2.制作自动打印脚本do_print.bat设置ELabel安装目录和E-Label.exe bat 打印命令
# 3.def execute_and_print 字符处理，默认是分割为三个字符串
import tkinter as tk
from tkinter import messagebox
import csv
import os
import subprocess
import threading

# 创建主窗口
root = tk.Tk()
root.title("易标签扫码打印-字符处理")
root.minsize(600, 500)
root.option_add("*Font.Name", "Microsoft YaHei")  # 指定默认字体
root.option_add("*Font.Size", 12)  # 设置默认字体大小为12

# 设置窗口在屏幕中间显示
def center_window():
    width = 600
    height = 500
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

# 在窗口创建后，调用center_window来居中显示
root.after(0, center_window)

# 创建一个文本输入框，用于"扫码录入"
entry_label = tk.Label(root, text="扫码录入:")
entry_label.pack()

entry_var = tk.StringVar()  # 创建一个StringVar对象来存储输入框的值
entry = tk.Entry(root, textvariable=entry_var)
entry.pack()

# 光标自动出现在输入框中
entry.focus_set()

# 创建一个复选框，用于决定是否在执行打印后清空输入框
clear_entry_var = tk.BooleanVar()  # 创建一个BooleanVar对象来存储复选框的状态
clear_entry_checkbox = tk.Checkbutton(root, text="执行后清空输入框", variable=clear_entry_var)
clear_entry_checkbox.pack()

# 为文本输入框绑定回车键事件
entry.bind("<Return>", lambda event: execute_and_print())

# 保存数据到CSV文件，并执行批处理文件
def execute_and_print():
    content = entry_var.get()  # 获取输入框的内容
    # 处理内容，分割为三个字段
    data1 = content[:3]
    data2 = content[3:6]
    data3 = content[6:] if len(content) > 6 else ""

    # 保存内容到CSV文件
    save_to_csv(data1, data2, data3)
    
    # 执行批处理文件
    threading.Thread(target=run_batch_file).start()

    # 根据复选框的状态决定是否清空输入框
    if clear_entry_var.get():  # 如果复选框被勾选
        entry.delete(0, tk.END)  # 清空输入框

# 保存数据到CSV文件
def save_to_csv(data1, data2, data3):
    csv_file = "scandata.csv"
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["data1", "data2", "data3"])  # 写入字段名称
        writer.writerow([data1, data2, data3])  # 写入数据


def run_batch_file():
    # 批处理文件名
    batch_file_name = "do_print.bat"
    
    # 获取当前脚本运行的目录
    current_dir = os.path.dirname(os.path.realpath(__file__))
    
    # 构建批处理文件的完整路径
    batch_file_path = os.path.join(current_dir, batch_file_name)
    
    # 检查批处理文件是否存在
    if not os.path.isfile(batch_file_path):
        messagebox.showerror("错误", f"批处理文件不存在: {batch_file_path}")
        return
    
    # 执行批处理文件
    try:
        subprocess.run(batch_file_path, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("错误", f"批处理文件执行失败: {e}")


# 创建执行打印和执行批处理文件的按钮
execute_print_button = tk.Button(root, text="执行打印", command=execute_and_print)
execute_print_button.pack()

# 运行主循环
root.mainloop()
