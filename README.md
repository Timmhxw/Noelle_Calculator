# Noelle_Calculator

[![诺艾尔神教](favicon.ico)](https://www.noelle.cool/)
[![诺艾尔神教git](https://img.shields.io/badge/-%E8%AF%BA%E8%89%BE%E5%B0%94%E7%A5%9E%E6%95%99-orange)](https://github.com/Genshin-Impact-Cult-of-Noelle)

### 计算器介绍
##### Noelle_Calculator:带UI的基于诺艾尔面板及武器、圣遗物数据的伤害计算器
##### 本家：https://github.com/Genshin-Impact-Cult-of-Noelle/noelle-Calculator

##### 注意：本程序中防御抗性乘区的数值采用理论公式计算，由于各个乘区存在数值误差，得到的结果会略低于夜雪大大的程序中依据实际伤害文本逆推得到的结果

##### 各版本的一些特性在release里面较详细的描述，有什么bug的话欢迎B站/米游社找我~没有bug更好2333
---
> 源码的入口在main_func.py，ui.py为旧版easygui版本ui设计的脚本，仅留作纪念。ui_tk.py为实际的ui脚本
>
> 武器、圣遗物、其他buff可按照格式修改，基础格式参见buff.py
---
> 3.2版本更新主要内容
>-
>- 添加了芙宁娜和猎人套，补充了计算公式中暴击率的增益以及最大值限制
>
>- 标注了other_buff.py中的DIY part，现在可以通过按照模板新建person类的子类，来规范创建队友buff

---
> 3.1版本更新主要内容
>-
>- 可通过build_env.bat创建conda环境，当然前提是有conda。随后用run.bat在conda环境中运行代码。pyinstall.bat提供了定制化代码后通过pyinstaller自动生成可执行文件包的脚本
>
>- 新增了Query_for_other_person对象，用于询问其他角色的参数，以便计算基于参数的增益对女仆伤害的影响。`允许填到一半退出编辑重新选择“其他buff”，此时已填充完整的角色参数会自动保存，并在再次编辑前询问是否使用历史数据。被取消勾选的角色buff数据会自动清除，关闭主窗口后该历史数据不会保存。`目前提供双岩、岩伤杯、钟离、夜兰、五郎、云堇六种“其他buff”。
>
>- 初始界面背景图片名设置为background_cc.png，访问新角色参数窗口的背景图片名为background.png，可通过修改文件名更换背景
>
>- 已设置与原图宽高比相同的自适应的窗体大小，强制锁高度最大800，最小没有限制
>
>- 凹了一下对齐，看起来更工整了~