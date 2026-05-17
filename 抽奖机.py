import random
import colorama
import tkinter as tk
from tkinter import messagebox
from collections import Counter
import json
from PIL import Image, ImageTk
import math
import ctypes
import sys

if sys.platform == "win32":
    # 获取控制台窗口句柄
    console_window = ctypes.windll.kernel32.GetConsoleWindow()
    # 最小化窗口（6 = SW_MINIMIZE）
    ctypes.windll.user32.ShowWindow(console_window, 6)
    
    # 或者隐藏窗口（0 = SW_HIDE）
    # ctypes.windll.user32.ShowWindow(console_window, 0)
    
    # 恢复正常窗口（1 = SW_NORMAL）
    # ctypes.windll.user32.ShowWindow(console_window, 1)

# 尝试导入 pyttsx3 语音库
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("pyttsx3 未安装，语音功能将不可用")

# 尝试导入 matplotlib 用于图表展示
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("matplotlib 未安装，图表功能将不可用")

colorama.init()

class Colors:
    RED = "\033[31m"
    GREEN = "\033[32m"
    BLUE = "\033[34m"
    RESET = "\033[0m"

# 学号列表
a = [2101, 2102, 2104, 2105, 2106, 2107, 2108, 2109, 2110, 2112, 
     2113, 2114, 2115, 2116, 2117, 2118, 2120, 2121, 2122, 2123, 2124, 
     2126, 2127, 2128, 2129]

# 初始化抽奖历史记录
draw_history = []

def speak_with_pyttsx3(text):
    """使用 pyttsx3 播放语音（每次独立初始化引擎）"""
    if not TTS_AVAILABLE:
        print(f"[文本显示] {text}")
        return
    
    try:
        # 每次播放都创建新的引擎实例
        engine = pyttsx3.init()
        
        # 设置语音属性
        engine.setProperty("rate", 200)  # 语速
        engine.setProperty("volume", 2.0)  # 音量
        
        # 尝试设置中文语音（如果有的话）
        voices = engine.getProperty("voices")
        # 查找中文语音
        for voice in voices:
            if "chinese" in voice.name.lower() or "zh" in voice.id.lower():
                engine.setProperty("voice", voice.id)
                break
        
        # 播放语音
        engine.say(text)
        engine.runAndWait()
        
        print(f"[语音] 播放完成: {text[:30]}...")
        
        # 重要：删除引擎实例，确保下次可以重新初始化
        del engine
        
    except Exception as e:
        print(f"[语音] 播放错误: {e}")
        # 如果播放失败，至少显示文本
        print(f"[文本显示] {text}")

def show_frequency_chart():
    """显示频率分布图表"""
    if not draw_history:
        messagebox.showinfo("提示", "暂无抽奖记录，无法生成图表")
        return
    
    if not MATPLOTLIB_AVAILABLE:
        messagebox.showinfo("提示", "matplotlib 未安装，图表功能不可用")
        return
    
    # 计算所有历史记录的统计
    all_drawn = []
    for draw in draw_history:
        all_drawn.extend(draw)
    
    counter = Counter(all_drawn)
    
    # 按学号排序
    sorted_nums = sorted(a)
    frequencies = [counter.get(num, 0) for num in sorted_nums]
    
    # 创建图表窗口
    chart_window = tk.Toplevel()
    chart_window.title("抽奖频率分布图")
    chart_window.geometry("900x600")
    
    # 设置窗口位置居中
    screen_width = chart_window.winfo_screenwidth()
    screen_height = chart_window.winfo_screenheight()
    x = (screen_width - 900) // 2
    y = (screen_height - 600) // 2
    chart_window.geometry(f"900x600+{x}+{y}")
    
    # 标题
    title_label = tk.Label(chart_window, text="抽奖频率分布图", 
                          font=("Arial", 14, "bold"))
    title_label.pack(pady=10)
    
    # 创建matplotlib图形
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 8))
    
    # 设置中文字体支持
    plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 绘制条形图
    bars = ax1.bar([str(num) for num in sorted_nums], frequencies, color='skyblue', edgecolor='black')
    ax1.set_xlabel('学号', fontsize=12)
    ax1.set_ylabel('出现次数', fontsize=12)
    ax1.set_title('各学号抽中次数分布', fontsize=14, fontweight='bold')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(axis='y', alpha=0.3)
    
    # 在条形上显示数值
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{int(height)}', ha='center', va='bottom', fontsize=9)
    
    # 绘制饼图（只显示被抽中的学号）
    drawn_nums = [num for num in sorted_nums if counter.get(num, 0) > 0]
    drawn_freq = [counter.get(num, 0) for num in drawn_nums]
    
    if drawn_nums:
        # 创建标签
        labels = [f'{num}({freq})' for num, freq in zip(drawn_nums, drawn_freq)]
        
        # 使用tab20c颜色映射，确保相邻颜色不同
        # 生成颜色列表，确保颜色数量足够且不重复
        colors = []
        cmap = plt.cm.tab20c  # 使用tab20c颜色映射，它有20种不同的颜色
        num_colors = len(drawn_nums)
        
        # 生成不重复的颜色
        for i in range(num_colors):
            # 使用不同的起始点避免相邻颜色相同
            color_idx = (i * 5) % 20  # 乘以质数5，确保颜色分布更均匀
            colors.append(cmap(color_idx))
        
        # 绘制饼图
        wedges, texts, autotexts = ax2.pie(drawn_freq, labels=labels, colors=colors,
                                          autopct='%1.1f%%', startangle=90,
                                          textprops={'fontsize': 9})
        ax2.set_title('抽中比例分布', fontsize=14, fontweight='bold')
        ax2.axis('equal')  # 确保饼图是圆的
        
        # 调整文本位置避免重叠
        plt.setp(autotexts, size=8, weight="bold")
    
    else:
        ax2.text(0.5, 0.5, '暂无抽中记录', ha='center', va='center', fontsize=14)
        ax2.axis('off')
    
    plt.tight_layout()
    
    # 将matplotlib图形嵌入到tkinter窗口
    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # 添加统计信息
    total_selections = len(all_drawn)
    total_draws = len(draw_history)
    avg_per_draw = total_selections / total_draws if total_draws > 0 else 0
    
    stats_text = (f"统计信息:\n"
                  f"总抽奖次数: {total_draws}次\n"
                  f"总抽取人数: {total_selections}人\n"
                  f"平均每次抽取: {avg_per_draw:.2f}人\n"
                  f"最高频次: {max(frequencies) if frequencies else 0}次\n"
                  f"最低频次: {min(frequencies) if frequencies else 0}次")
    
    stats_label = tk.Label(chart_window, text=stats_text, 
                          font=("Arial", 10), justify=tk.LEFT, bg="#f0f0f0")
    stats_label.pack(pady=5)
    
    # 添加按钮框架
    button_frame = tk.Frame(chart_window)
    button_frame.pack(pady=10)
    
    # 保存图表按钮
    def save_chart():
        try:
            filename = f"抽奖统计图_{len(draw_history)}次.png"
            fig.savefig(filename, dpi=150, bbox_inches='tight')
            messagebox.showinfo("保存成功", f"图表已保存为: {filename}")
        except Exception as e:
            messagebox.showerror("保存失败", f"保存图表时出错: {str(e)}")
    
    save_button = tk.Button(button_frame, text="保存图表", command=save_chart, width=10)
    save_button.pack(side=tk.LEFT, padx=5)
    
    # 关闭按钮
    close_button = tk.Button(button_frame, text="关闭图表", 
                            command=chart_window.destroy, width=15,
                            bg="#e74c3c", fg="white", font=("Arial", 10, "bold"))
    close_button.pack(side=tk.LEFT, padx=5)

def show_statistics():
    """显示统计信息"""
    if not draw_history:
        messagebox.showinfo("统计", "暂无抽奖记录")
        return
    
    stats_window = tk.Toplevel()
    stats_window.title("抽奖统计信息")
    stats_window.geometry("350x550")
    
    # 设置窗口位置到右上角
    screen_width = stats_window.winfo_screenwidth()
    window_width = 350
    window_height = 600
    x_position = screen_width - window_width - 10
    y_position = 5
    stats_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
    # 计算所有历史记录的统计
    all_drawn = []
    for draw in draw_history:
        all_drawn.extend(draw)
    
    counter = Counter(all_drawn)
    
    # 标题
    tk.Label(stats_window, text=f"全部抽奖历史统计", 
             font=("Arial", 12, "bold")).pack(pady=10)
    
    # 总抽奖次数和总抽取人数
    tk.Label(stats_window, text=f"总抽奖次数: {len(draw_history)}次", 
             font=("Arial", 10)).pack()
    tk.Label(stats_window, text=f"总抽取人数: {len(all_drawn)}人", 
             font=("Arial", 10)).pack()
    
    # 理论期望
    if len(draw_history) > 0:
        avg_per_draw = len(all_drawn) / len(draw_history)
        expected_per_student = len(all_drawn) / len(a)
        tk.Label(stats_window, 
                text=f"平均每次抽取: {avg_per_draw:.1f}人", 
                font=("Arial", 9), fg="gray").pack()
        tk.Label(stats_window, 
                text=f"理论期望: {expected_per_student:.1f}次/学号", 
                font=("Arial", 9), fg="gray").pack()
    
    # 创建按钮框架
    button_frame = tk.Frame(stats_window)
    button_frame.pack(pady=10)
    
    # 添加查看频率图表按钮
    if MATPLOTLIB_AVAILABLE:
        chart_button_text = "查看频率分布图表"
        chart_button_color = "#3498db"
    else:
        chart_button_text = "matplotlib未安装"
        chart_button_color = "#95a5a6"
    
    chart_button = tk.Button(button_frame, text=chart_button_text,
                            command=show_frequency_chart if MATPLOTLIB_AVAILABLE else None, width=25,
                            bg=chart_button_color, fg="white",
                            font=("Arial", 10, "bold"))
    chart_button.pack()
    
    # 创建滚动区域
    stats_frame = tk.Frame(stats_window)
    stats_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
    
    # 添加滚动条
    scrollbar = tk.Scrollbar(stats_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # 显示统计的文本框
    stats_text = tk.Text(stats_frame, height=15, width=30, 
                        yscrollcommand=scrollbar.set, font=("Arial", 10))
    stats_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=stats_text.yview)
    
    # 按出现次数排序
    sorted_stats = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    
    # 添加统计信息
    stats_text.insert(tk.END, "学号  出现次数  占比\n")
    stats_text.insert(tk.END, "="*30 + "\n")
    
    total_selections = len(all_drawn)
    for num, count in sorted_stats:
        percentage = (count / total_selections * 100) if total_selections > 0 else 0
        # 添加颜色标记：根据出现次数使用不同颜色
        if count >= 3:
            stats_text.insert(tk.END, f"{num}      {count}      {percentage:.1f}% 🔥\n")
        elif count >= 2:
            stats_text.insert(tk.END, f"{num}      {count}      {percentage:.1f}% ⭐\n")
        else:
            stats_text.insert(tk.END, f"{num}      {count}      {percentage:.1f}%\n")
    
    # 如果有些学号从未出现，也显示出来
    missing = [num for num in a if num not in counter]
    if missing:
        stats_text.insert(tk.END, "\n从未出现的学号:\n")
        stats_text.insert(tk.END, "="*30 + "\n")
        # 每行显示5个学号
        for i in range(0, len(missing), 5):
            line_numbers = missing[i:i+5]
            stats_text.insert(tk.END, ", ".join(str(num) for num in line_numbers) + "\n")
    
    stats_text.config(state=tk.DISABLED)
    
    # 添加关闭按钮
    close_button = tk.Button(stats_window, text="关闭", 
                            command=stats_window.destroy, width=10)
    close_button.pack(pady=10)
    
    return stats_window

def show_result(selected_numbers):
    """显示抽奖结果"""
    # 添加到历史记录
    draw_history.append(selected_numbers)
    
    result_window = tk.Toplevel()
    result_window.title("抽奖结果")
    result_window.geometry("250x400")
    
    # 设置窗口位置到左上角
    screen_width = result_window.winfo_screenwidth()
    window_width = 150
    window_height = 590
    x_position = 10
    y_position = 5
    result_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
    # 显示标题
    title_label = tk.Label(result_window, text="中奖号码:", font=("Arial", 12, "bold"))
    title_label.pack(pady=5)
    
    # 显示中奖号码
    result_text = tk.Text(result_window, width=20, height=10, wrap=tk.WORD, font=("Arial", 10))
    result_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    
    for num in selected_numbers:
        result_text.insert(tk.END, f"{num}\n")
    
    result_text.config(state=tk.DISABLED)
    
    # 显示抽取人数信息
    info_label = tk.Label(result_window, 
                         text=f"本次抽取 {len(selected_numbers)} 人\n总抽奖次数: {len(draw_history)}",
                         font=("Arial", 9), fg="blue")
    info_label.pack(pady=5)
    
    # 按钮框架
    button_frame = tk.Frame(result_window)
    button_frame.pack(pady=10)
    
    # 查看统计按钮
    stats_button = tk.Button(button_frame, text="查看统计", 
                            command=show_statistics, width=10)
    stats_button.pack(side=tk.LEFT, padx=5)
    
    # 关闭按钮
    close_button = tk.Button(button_frame, text="关闭", 
                            command=result_window.destroy, width=10)
    close_button.pack(side=tk.LEFT, padx=5)
    
    # 语音播报中奖号码（每次独立初始化引擎）
    if selected_numbers and TTS_AVAILABLE:
        numbers_text = "、".join(str(num) for num in selected_numbers)
        # 延迟一点播放，让窗口先显示
        result_window.after(100, lambda: speak_with_pyttsx3(f"恭喜中奖同学：{numbers_text}，恭喜恭喜！"))
    
    # 延迟一点显示统计窗口，避免重叠
    result_window.after(100, show_statistics)

def get_text():
    """获取输入并执行抽奖"""
    try:
        text = input_var.get().strip()
        if not text:
            messagebox.showwarning("警告", "请输入要抽取的人数！")
            return
            
        c = int(text)
        if c <= 0:
            messagebox.showwarning("警告", "请输入大于0的数字！")
            return
        elif c > len(a):
            messagebox.showwarning("警告", f"抽取人数不能超过{len(a)}人！")
            return
            
        # 使用SystemRandom进行更安全的随机抽取
        sys_random = random.SystemRandom()
        
        # 随机抽取
        selected = sys_random.sample(a, c)
        show_result(selected)
        
    except ValueError:
        messagebox.showerror("错误", "请输入有效的数字！")
    except Exception as e:
        messagebox.showerror("错误", f"发生错误：{str(e)}")

def clear_text():
    """清空输入框"""
    input_var.set("")

def add_number(num):
    """添加数字到输入框"""
    current = input_var.get()
    if len(current) < 2:  # 限制最多输入2位数
        input_var.set(current + str(num))

def quick_draw():
    """快速抽取1人"""
    if len(a) == 0:
        messagebox.showwarning("警告", "没有可抽取的学号！")
        return
    
    sys_random = random.SystemRandom()
    selected = sys_random.sample(a, 1)
    show_result(selected)

def on_closing():
    """程序关闭时的处理"""
    try:
        # 保存历史记录到文件
        with open("抽奖历史记录.json", "w", encoding="utf-8") as f:
            json.dump({"draw_history": draw_history}, f, ensure_ascii=False, indent=2)
        print("[系统] 历史记录已保存")
    except Exception as e:
        print(f"[系统] 保存历史记录失败: {e}")
    
    root.destroy()
    print("[系统] 程序已关闭")

def load_history():
    """加载历史记录"""
    global draw_history
    try:
        with open("抽奖历史记录.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            draw_history = data.get("draw_history", [])
        print(f"[系统] 已加载历史记录: {len(draw_history)} 条")
    except FileNotFoundError:
        draw_history = []
        print("[系统] 未找到历史记录文件，创建新记录")
    except Exception as e:
        print(f"[系统] 加载历史记录失败: {e}")
        draw_history = []

def toggle_collapse():
    """切换窗口收起/展开状态"""
    global is_collapsed
    
    if is_collapsed:
        # 展开窗口
        root.geometry(f"{expanded_width}x{expanded_height}+{root.winfo_x()}+{root.winfo_y()}")
        root.overrideredirect(False)  # 恢复窗口装饰
        # 显示所有主框架内容
        main_frame.pack(fill=tk.BOTH, expand=True)
        # 隐藏收起胶囊
        capsule_frame.place_forget()
        # 移除窗口透明
        root.configure(bg='SystemButtonFace')
        root.attributes('-transparentcolor', '')
        # 取消置顶
        root.attributes('-topmost', False)
        # 更新标题
        root.title("抽奖机")
        # 更新收起/展开按钮文本
        toggle_button.config(text="收起主界面")
        is_collapsed = False
    else:
        # 获取屏幕尺寸
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # 计算胶囊位置（屏幕上方正中央）
        capsule_x = (screen_width - capsule_width) // 2
        capsule_y = 1  # 距离屏幕顶部10像素，避免被任务栏遮挡
        
        # 收起窗口
        root.geometry(f"{capsule_width}x{capsule_height}+{capsule_x}+{capsule_y}")
        root.overrideredirect(True)  # 隐藏标题栏
        # 隐藏主框架
        main_frame.pack_forget()
        # 显示胶囊
        capsule_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        # 设置窗口透明，只显示胶囊
        root.configure(bg=transparent_color)
        root.attributes('-transparentcolor', transparent_color)
        # 设置置顶
        root.attributes('-topmost', True)
        # 更新标题
        root.title("抽奖机 (胶囊模式)")
        # 更新收起/展开按钮文本
        toggle_button.config(text="展开")
        is_collapsed = True
    
def start_drag(event):
    """开始拖动窗口"""
    global drag_x, drag_y
    drag_x = event.x
    drag_y = event.y

def drag_window(event):
    """拖动窗口"""
    x = root.winfo_x() + event.x - drag_x
    y = root.winfo_y() + event.y - drag_y
    root.geometry(f"+{x}+{y}")

def start_capsule_drag(event):
    """开始拖动胶囊"""
    global drag_x, drag_y
    drag_x = event.x
    drag_y = event.y

def drag_capsule(event):
    """拖动胶囊"""
    x = root.winfo_x() + event.x - drag_x
    y = root.winfo_y() + event.y - drag_y
    root.geometry(f"+{x}+{y}")

def create_rounded_rect(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    """创建圆角矩形"""
    points = [
        x1+radius, y1,
        x2-radius, y1,
        x2, y1,
        x2, y1+radius,
        x2, y2-radius,
        x2, y2,
        x2-radius, y2,
        x1+radius, y2,
        x1, y2,
        x1, y2-radius,
        x1, y1+radius,
        x1, y1
    ]
    return canvas.create_polygon(points, **kwargs, smooth=True)

def animate_capsule_pulse():
    """胶囊脉动动画"""
    if is_collapsed:
        # 获取当前时间戳
        import time
        current_time = time.time()
        pulse = (math.sin(current_time * 3) + 1) / 2  # 0到1之间波动
        
        # 计算颜色渐变
        r = int(41 + pulse * 15)  # 41-56
        g = int(128 + pulse * 30)  # 128-158
        b = int(185 + pulse * 15)  # 185-200
        
        color = f'#{r:02x}{g:02x}{b:02x}'
        capsule_canvas.itemconfig("capsule_bg", fill=color)
        
        # 继续动画
        root.after(50, animate_capsule_pulse)

# 创建主窗口
root = tk.Tk()
root.title("抽奖机")

# 加载历史记录
load_history()

# 设置窗口图标
try:
    img = Image.open("(2).png")  # 可以是PNG, JPG等格式
    photo = ImageTk.PhotoImage(img)
    root.iconphoto(False, photo)
except:
    pass

# 窗口尺寸和位置
expanded_width = 250
expanded_height = 430
capsule_width = 200
capsule_height = 30

# 获取屏幕尺寸
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()

# 计算主窗口在屏幕正中央的位置
x_position = int((screenwidth - expanded_width) / 2)
y_position = int((screenheight - expanded_height) / 2)

# 确保窗口不会完全居中半小时，设置最小偏移量
if y_position < 100:  # 如果太靠近顶部，向下移动一些
    y_position = 100
    
size_geo = f'{expanded_width}x{expanded_height}+{x_position}+{y_position}'
root.geometry(size_geo)

# 透明颜色用于实现胶囊效果
transparent_color = 'gray15'

# 初始状态不置顶（主界面展开状态）
root.attributes('-topmost', False)

# 窗口状态变量
is_collapsed = False
drag_x = 0
drag_y = 0

root.protocol("WM_DELETE_WINDOW", on_closing)

# 创建主框架 - 展开时显示的内容
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# 创建胶囊框架 - 收起时显示的内容（灵动岛风格）
capsule_frame = tk.Frame(root, bg=transparent_color)

# 创建胶囊的画布
capsule_canvas = tk.Canvas(capsule_frame, width=capsule_width, height=capsule_height, 
                          bg=transparent_color, highlightthickness=0)
capsule_canvas.pack()

# 绘制胶囊背景（圆角矩形）
capsule_bg = create_rounded_rect(capsule_canvas, 5, 5, capsule_width-5, capsule_height-5, 
                                 radius=25, fill='#2980b9', tags="capsule_bg")

# 添加文字和按钮到胶囊
# 左侧：抽奖次数
count_label = tk.Label(capsule_frame, text=f"🎰 {len(draw_history)}", 
                      font=("微软雅黑",7 , "bold"), bg='#2980b9', fg='white')
count_label.place(x=15, y=15 , anchor=tk.W)

# 中间：快速抽奖按钮
quick_button = tk.Button(capsule_frame, text="🎲 快速抽1人", 
                        command=quick_draw, bg='#e74c3c', fg='white',
                        font=("微软雅黑", 6, "bold"), bd=0, relief=tk.FLAT,
                        activebackground='#c0392b', activeforeground='white')
quick_button.place(x=capsule_width/2, y=15, anchor=tk.CENTER)

# 右侧：展开按钮
expand_button = tk.Button(capsule_frame, text="展开", 
                         command=toggle_collapse, bg='#2ecc71', fg='white',
                         font=("微软雅黑", 6 , "bold"), bd=0, relief=tk.FLAT,
                        activebackground='#27ae60', activeforeground='white')
expand_button.place(x=capsule_width-34, y=15 , anchor=tk.CENTER)

# 使整个胶囊可拖动
capsule_canvas.bind("<Button-1>", start_capsule_drag)
capsule_canvas.bind("<B1-Motion>", drag_capsule)
quick_button.bind("<Button-1>", start_capsule_drag)
quick_button.bind("<B1-Motion>", drag_capsule)
expand_button.bind("<Button-1>", start_capsule_drag)
expand_button.bind("<B1-Motion>", drag_capsule)
count_label.bind("<Button-1>", start_capsule_drag)
count_label.bind("<B1-Motion>", drag_capsule)

# 隐藏胶囊
capsule_frame.place_forget()

# 创建输入变量
input_var = tk.StringVar()

# 创建输入标签
input_label = tk.Label(main_frame, text="请输入抽取人数:", font=("Arial", 10))
input_label.pack(pady=10)

# 创建输入显示框
input_display = tk.Entry(main_frame, textvariable=input_var, font=("Arial", 14), 
                        justify="center", state="readonly", width=10)
input_display.pack(pady=5)

# 创建数字按钮框架
number_frame = tk.Frame(main_frame)
number_frame.pack(pady=10)

# 创建数字按钮
buttons = []
for i in range(1, 10):
    row = (i-1) // 3
    col = (i-1) % 3
    btn = tk.Button(number_frame, text=str(i), font=("Arial", 12), width=3,
                   command=lambda num=i: add_number(num))
    btn.grid(row=row, column=col, padx=5, pady=5)
    buttons.append(btn)

# 第4行：0按钮
zero_btn = tk.Button(number_frame, text="0", font=("Arial", 12), width=3,
                    command=lambda: add_number(0))
zero_btn.grid(row=3, column=1, padx=5, pady=5)

# 创建功能按钮框架
button_frame = tk.Frame(main_frame)
button_frame.pack(pady=20)

# 抽奖按钮
draw_button = tk.Button(button_frame, text="开始抽奖", command=get_text, 
                       bg="#4CAF50", fg="white", font=("Arial", 10), width=8)
draw_button.pack(side=tk.LEFT, padx=10)

# 清空按钮
clear_button = tk.Button(button_frame, text="清空", command=clear_text,
                        bg="#f44336", fg="white", font=("Arial", 10), width=8)
clear_button.pack(side=tk.LEFT, padx=10)

# 收起/展开按钮框架
collapse_frame = tk.Frame(main_frame)
collapse_frame.pack(pady=5)

# 收起/展开按钮
toggle_button = tk.Button(collapse_frame, text="收起主界面", command=toggle_collapse,
                         bg="#2196F3", fg="white", font=("Arial", 10), width=8)
toggle_button.pack()

# 显示总人数信息和抽奖历史
info_label = tk.Label(main_frame, text=f"总人数: {len(a)}人", font=("Arial", 9), fg="gray")
info_label.pack(pady=5)

# 显示历史记录次数
history_label = tk.Label(main_frame, text=f"已抽奖次数: {len(draw_history)}次", 
                        font=("Arial", 9), fg="green")
history_label.pack(pady=2)

# 语音状态提示
if TTS_AVAILABLE:
    voice_status = tk.Label(main_frame, text="✓ 语音功能: 已启用", 
                           font=("Arial", 8), fg="green")
else:
    voice_status = tk.Label(main_frame, text="✗ 语音功能: 未启用", 
                           font=("Arial", 8), fg="red")
voice_status.pack(pady=2)

# 图表状态提示
if MATPLOTLIB_AVAILABLE:
    chart_status = tk.Label(main_frame, text="✓ 图表功能: 已启用", 
                           font=("Arial", 8), fg="green")
else:
    chart_status = tk.Label(main_frame, text="✗ 图表功能: 未安装", 
                           font=("Arial", 8), fg="orange")
chart_status.pack(pady=2)

# 自动更新历史记录显示
def update_history_label():
    history_label.config(text=f"已抽奖次数: {len(draw_history)}次")
    count_label.config(text=f"🎰 {len(draw_history)}")
    root.after(1000, update_history_label)

# 启动标签更新
root.after(1000, update_history_label)

# 启动胶囊脉动动画
root.after(100, animate_capsule_pulse)

# 启动主循环
try:
    # 检查学号是否被修改的代码
    s = ""
    for x in range(2101, 2130):
        if x in a:
            pass
        elif x in [2103,2111,2119,2125] :
            pass
        else:
            s += f"{x} "
    if len(s) > 0:
        s += "！"
        messagebox.showerror("错误", f"{s}\n你居然敢改我的代码！\n就抽你了！")
    
  
    root.mainloop()
    
except Exception as e:
    messagebox.showerror("错误", f"程序运行出错：{str(e)}")
    import traceback
    traceback.print_exc()
