# 一、实验内容  
设计一个应用软件，以实现SLR(1)分析器的生成。
# 二、实验要求  
1.必做功能：  
 （1）要提供一个源程序编辑界面，让用户输入文法规则（可保存、打开存有文法规则的文件）  
 （2）检查该文法是否需要进行文法的扩充。  
 （3）求出该文法各非终结符号的first集合与follow集合，并提供窗口以便用户可以查看这些集合结果。  
   (4) 需要提供窗口以便用户可以查看文法对应的LR(0)DFA图。（可以用画图的方式呈现，也可用表格方式呈现该图点与边的关系数据）  
 （5）需要提供窗口以便用户可以查看该文法是否为SLR(1)文法。（如果非SLR(1)文法，可查看其原因）  
 （6）需要提供窗口以便用户可以查看文法对应的SLR(1)分析表。（如果该文法为SLR(1)文法时）  
 （7）应该书写完善的软件文档  
# 三、实现思路
本项目是根据用户输入的文法，计算出文法的first集和follow集，并根据文法计算LR(0)的DFA图，然后再根据first集和follow集判断文法是否是SLR(1)文法，然后生成文法对应的SLR(1)分析表。  
# 四、示例图片
![图片](https://github.com/Gao-JF/SLR-1-analysis/blob/main/test.png?raw=true)
