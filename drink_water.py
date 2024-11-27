import tkinter as tk
#import psutil
import time
import json
import requests
from win10toast import ToastNotifier
import datetime
import webbrowser

#获取温度key
api_key = ""
#济南地区编号
locatnum = ""
#配置文件读取
my_script = {}
def getcript():
    try:
        global api_key,locatnum
        with open("./script/my_script.json", 'r', encoding='utf-8') as file:
             content = file.read()
        if(len(content) < 32):
            api_key = input("请输入api_key: ")
            locatnum = input("请输入地区编号: ")
            my_script["api_key"] = api_key
            my_script["locatnum"] = locatnum
            with open("./script/my_script.json", 'w', encoding='utf-8') as f:
                json.dump(my_script, f, ensure_ascii=False, indent=4)
        else:
            content = eval(content)
            values = list(content.values())
            api_key = values[0]
            locatnum = values[1]

    except SyntaxError as error:
        print("读取配置文件失败")
    except FileNotFoundError as error:
        print("my_script.json文件丢失")





#未来多天天气web端
lacalweather="https://www.baidu.com"
entrylist = []
# 创建窗口
window = tk.Tk()
window.title("提醒喝水小工具")
window['bg'] = 'black'
# 创建菜单
menu = tk.Menu(window, tearoff=0)
# 存储任务文件
file_name = './script/my_dict.json'
count = 0
save_dict = {}

# 设置窗口为无边框
window.overrideredirect(True)
window.resizable(True, True)

def win_max():
    w = window.winfo_screenwidth()
    h = window.winfo_screenheight()
    window.geometry("%dx%d" % (w, h))
    window.attributes("-topmost", True)

#置于最顶层
def top():
    window.attributes('-topmost', 'true')
#取消置顶
def remove_top():
    window.attributes('-topmost', 'false')
# 设置窗口透明度
window.attributes('-alpha', 0.5)  # 设置透明度为 0.7

# 创建标签
label = tk.Label(window, font=("楷体", 80,"bold"), fg="white",bg="black")
label.pack(padx=10, pady=10)
#label2 = tk.Label(window, font=("楷体", 20,"bold"), fg="white",bg="black")
#label2.pack(anchor=tk.E,ipadx=10)
labelTQ = tk.Label(window, font=("楷体", 20,"bold"), fg="aqua",bg="black")
labelTQ.pack(anchor=tk.E,ipadx=10)
label3 = tk.Label(window, font=("楷体", 20,"bold"), fg="white",bg="black",text="牛马任务栏：")
label3.pack(anchor=tk.W,ipadx=10)



# 发送 GET 请求获取天气信息

toaster = ToastNotifier()
def getTQ():
    url = f"https://devapi.qweather.com/v7/weather/now?location={locatnum}&key={api_key}"
    response = requests.get(url)
    print("sss")
    if response.status_code == 200:
        data = response.json()
        global lacalweather
        lacalweather = data['fxLink']
        result = "温度:" +data['now']['temp']+"°  湿度:" +data['now']['humidity']+"%  天气状况:"+data['now']['text']
    else:
        # 请求失败时打印提示信息
       resutl = "获取天气信息失败，请检查订阅是否充足"
    labelTQ.config(text=result)
    #每十分钟调用一次
    labelTQ.after(60000, getTQ)
def open_url(event):
    webbrowser.open(lacalweather.replace("/en/","/"), new=0)
    """ #英文版
        webbrowser.open(lacalweather, new=0)
    """

# 使用with语句确保文件正确关闭
try:
    with open(file_name, 'r', encoding='utf-8') as file:
         content = file.read()
    content = eval(content)
    keys = list(content.keys())
    values = list(content.values())
    count = len(content)
    for i in range(0, count, 1):
        var = tk.StringVar(value=keys[i] + ' ' + values[i])
        entrylist.append('entry' + str(i))
        entrylist[i] = tk.Entry(window, font=("楷体", 20, "bold"), fg="white", bg="black", textvariable=var)
        entrylist[i].pack(anchor=tk.W, ipadx=100)
except SyntaxError as error:
    labelerror = tk.Label(window, font=("楷体", 80, "bold"), fg="white", bg="black")
    labelerror.pack(padx=10, pady=10)
    labelerror.config(text="配置文件有问题:" + str(error), font=("楷体", 20))
    labelerror.pack()
    window.mainloop()

#桌面时钟
def update_clock():
    current_time =time.strftime("%H:%M:%S")
    #current_time =time.strftime("%H:%M")
    label.config(text=current_time)
    label.after(1000, update_clock)

#def update_ram():
    # 内存使用率
   # memory_percent = "内存%：" + str(psutil.virtual_memory().percent)
   # label2.config(text=memory_percent)
   # label2.after(5000, update_ram)
def exit_app():
    window.destroy()

#添加任务
def add_task():
    globals()["count"]=count +1
    entrylist.append('entry' + str(count- 1))
    current_time = time.strftime('%m-%d %H:%M | ', time.localtime())
    var = tk.StringVar(value=current_time)
    entrylist[count-1] = tk.Entry(window, font=("楷体", 20, "bold"), fg="white", bg="black", textvariable=var)
    entrylist[count-1].pack(anchor=tk.W, ipadx=100)
#保存任务
def save_task():
    for i in range(0,count,1):
        if((len(entrylist[i].get()[14:]))>0):
            save_dict[entrylist[i].get()[0:13]] = entrylist[i].get()[14:]
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(save_dict, f, ensure_ascii=False, indent=4)
    toaster.show_toast("恭喜牛马:",
                       "任务保存成功!",
                       icon_path="./script/die.ico",
                       duration=5,
                       threaded=True)
def alert():
    now_time = datetime.datetime.now()
    before5 = (now_time + datetime.timedelta(minutes=5)).strftime('%m-%d %H:%M')
    for i in range(0,count,1):
        if((len(entrylist[i].get()[14:]))>0):
            if entrylist[i].get()[0:11] == before5:
                toaster.show_toast("5分钟后牛马需要注意以下事项:",
                                   entrylist[i].get()[14:],
                                   icon_path = "ico.ico",
                                   duration = 5,
                                   threaded = True)
    labelTQ.after(60000, alert)
menu.add_command(label="添加任务", command=add_task)
menu.add_command(label="保存任务", command=save_task)
menu.add_command(label="置顶", command=top)
menu.add_command(label="置底", command=remove_top)
menu.add_command(label="全屏", command=win_max)
menu.add_command(label="退出", command=exit_app)
#更新内存
#update_ram()
#读取配置文件
getcript()
# 更新时钟
update_clock()
getTQ()
alert()

# 绑定鼠标右键事件
def show_menu(event):
    menu.post(event.x_root, event.y_root)

window.bind("<Button-3>", show_menu)

# 实现拖动功能
def start_drag(event):
    window.x = event.x
    window.y = event.y

def drag(event):
    deltax = event.x - window.x
    deltay = event.y - window.y
    new_x = window.winfo_x() + deltax
    new_y = window.winfo_y() + deltay
    window.geometry(f"+{new_x}+{new_y}")

window.bind("<ButtonPress-1>", start_drag)
window.bind("<B1-Motion>", drag)
labelTQ.bind("<Button-1>", open_url)
# 运行窗口循环
window.mainloop()