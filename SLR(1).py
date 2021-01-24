# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 15:56:43 2020

@author: Gaojunfeng1020
"""


from graphviz import Digraph

Edges=[]
node=[]
first=[]
follow=[]
V=[]
T=[]
time=0
dic={}

class Edge:
    def __init__(self,n1,n2):
        self.n1=n1
        self.n2=n2
        self.pos=0
    


class dfaState:
    def __init__(self,n):
        self.no=n
        self.edges=[]
        self.nextDfaState={}
        self.value=str()
   
dfaStates=[dfaState(i) for i in range(99)]        

def inputWenfa():
    Edges=[]
    wenfa=str('')
    while True:
        wenfa=input('')    
        if wenfa=='0':
            break
        n=wenfa.split('->')
        Edges.append(Edge(n[0],n[1]))
    return Edges
        
def find_V_and_T(Edges):
    V=set() #非终结符
    T=set() #终结符
    for i in range(len(Edges)):
        V.add(Edges[i].n1)
    for i in range(len(Edges)):
        for j in range(len(Edges[i].n2)):
            if Edges[i].n2[j] not in V:
                T.add(Edges[i].n2[j])
    return V,T

#求First集合
def First(Edges,V):
    first={}
    for v in V:
        ist=set()
        for edge in Edges:
            if edge.n1==v and edge.n2[0]!=v:
                ist.add(edge.n2[0])
        first[v]=ist
    
    first=First_1(first)
    """
    for key,value in first.items():
        Va=value.copy()
        for va in value:
            if va in V:
                Va.remove(va)
                Va=Va|first[va]
        first[key]=Va      
    """
    return first

def First_1(first):
    b=False
    for key,value in first.items():
        Va=value.copy()
        for va in value:
            if va in V:
                b=True
                Va.remove(va)
                Va=Va|first[va]
        first[key]=Va    
        if b==True:
            First_1(first)
    return first

def expandEdge(Edges):
    for edge in Edges:
        n2=edge.n2.split('|')
        if len(n2)>1:
            Edges.remove(edge)
            for i in range(len(n2)):
                Edges.append(Edge(edge.n1,n2[i]))
    return Edges

#求Follow集
def Follow(Edges,V):
    follow={}
    for v in V:
        follow[v]=set()
    follow[Edges[0].n1].add('#')
    for k in range(2):
        for edge in Edges:
            for i in range(len(edge.n2)):            
                if i<len(edge.n2)-1:
                    if edge.n2[i] in V:
                        if edge.n2[i+1] in V:
                            follow[edge.n2[i]]=follow[edge.n2[i]]|first[edge.n2[i+1]]
                        else:
                            follow[edge.n2[i]].add(edge.n2[i+1])
                elif edge.n2[i] in V:
                    follow[edge.n2[i]]=follow[edge.n2[i]]|follow[edge.n1]

    return follow



def init_dfa(Edges,start,dfastate):
    global time
    for edge in Edges:
        if edge.n1==start:
            dfastate.edges.append(edge)
            

            
            if edge.pos<len(edge.n2) and (edge.n1!=edge.n2[edge.pos] or (edge.n1==edge.n2[edge.pos] and edge.pos>0)):
                if edge.n2[edge.pos] not in dfastate.nextDfaState.keys():
                    time+=1
                    dfastate.nextDfaState[edge.n2[edge.pos]]=time
                init_dfa(Edges,edge.n2[edge.pos],dfastate)

                
    return dfastate



def dfa(Edges,dfastate_edges,key,dfastate):
    global time
    for ns_edge in dfastate_edges:
        if ns_edge.pos<len(ns_edge.n2) and ns_edge.n2[ns_edge.pos]==key:
            if ns_edge.pos<len(ns_edge.n2):
                pos=ns_edge.pos+1
                new_edge=Edge(ns_edge.n1,ns_edge.n2)
                new_edge.pos=ns_edge.pos+1
                dfastate.edges.append(new_edge)
                if pos<len(new_edge.n2):
                    time+=1
                    dfastate.nextDfaState[new_edge.n2[new_edge.pos]]=time
                    dfastate=init_dfa(Edges,new_edge.n2[new_edge.pos],dfastate)
                    
    return dfastate



def SLR1TABLE(dfaStates,V,T):
    T.add('#')
    table=[['']+list(T)+list(V)]
    for i in range(max(dic.values())+1):
        t=[i]
        for j in range(len(table[0])-1):
            t.append('')
        table.append(t)
    ch_dic={}
    u=0
    for i in table[0]:
        ch_dic[i]=u
        u=u+1
    for i in range(max(dic.keys())+1):
        if i in dic.keys():
            for key,value in dfaStates[i].nextDfaState.items():
                if key in T:
                    table[dic[i]+1][ch_dic[key]]='s'+str(dic[value])
                elif key in V:
                    table[dic[i]+1][ch_dic[key]]=str(dic[value])
                else:
                    print('error')
            
            for edge in dfaStates[i].edges:
                if edge.pos==len(edge.n2):
                    for j in range(len(Edges)):
                        if Edges[j].n1==edge.n1 and Edges[j].n2==edge.n2:
                            if edge.n1!=Edges[0].n1:
                                if edge.n2[edge.pos-1] in V:
                                    for f in follow[edge.n2[edge.pos-1]]:
                                        if table[dic[i]+1][ch_dic[f]]=='':
                                            table[dic[i]+1][ch_dic[f]]='r'+str(j)
                                else:
                                    for f in follow[edge.n1]:
                                        if table[dic[i]+1][ch_dic[f]]=='':
                                            table[dic[i]+1][ch_dic[f]]='r'+str(j)
                            else:
                                table[dic[i]+1][ch_dic['#']]='acc'
                            break

    return table

def is_SLR1(dfaStates,V,T):
    rr_num=[] #存在规约和规约冲突的状态号
    rp_num=[] #存在规约和移进冲突的状态号
    rr_not_slr=[]
    rp_not_slr=[]
    is_slr1=True
    for i in range(max(dic.keys())):
        return_edge=[]
        for edge in dfaStates[i].edges:
            if edge.pos==len(edge.n2):
                return_edge.append(edge.n1)
        if len(return_edge)>=1:
            #判断规约移进冲突
            if len(dfaStates[i].nextDfaState)>0:
                for n1 in return_edge:
                    bing=set(dfaStates[i].nextDfaState)&follow[n1]
                    rp_num.append([dic[i],n1,set(dfaStates[i].nextDfaState)])
                    if len(bing)>0:
                        rp_not_slr.append([dic[i],n1,set(dfaStates[i].nextDfaState),bing])
                        is_slr1=False
                        
            
            #判断规约规约冲突
            for nn1 in return_edge:
                for nnn1 in return_edge:
                    if nn1==nnn1:
                        continue
                    rr_num.append([dic[i],nn1,nnn1])
                    if len(follow[nn1]&follow[nnn1])>0:
                        rr_not_slr.append([dic[i],n1,set(dfaStates[i].nextDfaState),bing])
                        is_slr1=False
                        
    return rr_num,rp_num,rr_not_slr,rp_not_slr,is_slr1
    

import os

def printDFA(dfaStates,time):
    #输出DFA图
    g=Digraph(graph_attr={'rankdir':'LR','dpi':'1500'},format='jpg')
    #添加结点
    global dic
    u=0
    for i in range(time+1):
        dfaStates[i].value+='I'+str(u)+':\n'
        exist_edge=0
        for edge in dfaStates[i].edges:
            exist_edge=1
            temp=list(edge.n2)
            temp.insert(edge.pos,'.')
            n2=''.join(temp)
            dfaStates[i].value+=edge.n1+'→'+n2+'\n'
        if exist_edge==1:
            dic[i]=u
            
            g.node(str(u),label=dfaStates[i].value,shape='rectangle')    
            u=u+1
    print(str(dic))
    #添加边
    for i in range(time+1):
        if i not in dic.keys():
            continue
        for key,value in dfaStates[i].nextDfaState.items():
            g.edge(str(dic[i]),str(dic[value]),label=key)
    
    if not os.path.exists('./image'):
        os.mkdir('./image')
    g.view(filename='./image/view')
    g.render(filename='output',directory='./image')


def check(dfastate):
    global node
    
    for i in range(len(node)):
        equal=1
        if len(dfastate.edges)!=len(node[i])-1:
            continue
        for j in range(len(dfastate.edges)):
            if dfastate.edges[j].n1==node[i][j].n1 and dfastate.edges[j].n2==node[i][j].n2 and dfastate.edges[j].pos==node[i][j].pos:
                continue
            else:
                equal=0
                break
        if equal==1:
            return i
    return -1


from PyQt5.QtWidgets import QTableView, QHeaderView, QFormLayout,   QVBoxLayout,QWidget,QApplication ,QHBoxLayout, QPushButton,QMainWindow,QGridLayout,QLabel
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import  QStandardItemModel,QStandardItem
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox,QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap,QImage
from PyQt5.Qt import *


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SLR1(object):
    def setupUi(self, SLR1):
        SLR1.setObjectName("SLR1")
        SLR1.resize(1680, 963)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SLR1.sizePolicy().hasHeightForWidth())
        SLR1.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(SLR1)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.openfile = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openfile.sizePolicy().hasHeightForWidth())
        self.openfile.setSizePolicy(sizePolicy)
        self.openfile.setObjectName("openfile")
        self.verticalLayout.addWidget(self.openfile)
        self.ana = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ana.sizePolicy().hasHeightForWidth())
        self.ana.setSizePolicy(sizePolicy)
        self.ana.setObjectName("ana")
        self.verticalLayout.addWidget(self.ana)
        spacerItem = QtWidgets.QSpacerItem(20, 100, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.wenfa = QtWidgets.QTextEdit(self.centralwidget)
        self.wenfa.setObjectName("wenfa")
        self.verticalLayout_2.addWidget(self.wenfa)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.First = QtWidgets.QTextBrowser(self.centralwidget)
        self.First.setObjectName("First")
        self.verticalLayout_3.addWidget(self.First)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)
        self.follow = QtWidgets.QTextBrowser(self.centralwidget)
        self.follow.setObjectName("follow")
        self.verticalLayout_4.addWidget(self.follow)
        self.verticalLayout_3.addLayout(self.verticalLayout_4)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_2.addLayout(self.verticalLayout_7)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.verticalLayout_9.addLayout(self.horizontalLayout_2)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_5.addWidget(self.label_7)
        self.graphicsView = QtWidgets.QTextEdit(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout_5.addWidget(self.graphicsView)
        self.verticalLayout_9.addLayout(self.verticalLayout_5)
        self.horizontalLayout_3.addLayout(self.verticalLayout_9)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setObjectName("tableView")
        self.verticalLayout_10.addWidget(self.tableView)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_10.addWidget(self.label_6)
        self.is_slr1 = QtWidgets.QTextBrowser(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.is_slr1.sizePolicy().hasHeightForWidth())
        self.is_slr1.setSizePolicy(sizePolicy)
        self.is_slr1.setObjectName("is_slr1")
        self.verticalLayout_10.addWidget(self.is_slr1)
        self.horizontalLayout_3.addLayout(self.verticalLayout_10)
        self.verticalLayout_12.addLayout(self.horizontalLayout_3)
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.verticalLayout_12.addLayout(self.verticalLayout_11)
        self.horizontalLayout_4.addLayout(self.verticalLayout_12)
        SLR1.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(SLR1)
        self.statusbar.setObjectName("statusbar")
        SLR1.setStatusBar(self.statusbar)
        self.ana.clicked.connect(self.analyze)
        self.retranslateUi(SLR1)
        QtCore.QMetaObject.connectSlotsByName(SLR1)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.openfile.clicked.connect(self.showDialog1)

    def retranslateUi(self, SLR1):
        _translate = QtCore.QCoreApplication.translate
        SLR1.setWindowTitle(_translate("SLR1", "SLR1"))
        self.openfile.setText(_translate("SLR1", "打开..."))
        self.ana.setText(_translate("SLR1", "分析"))
        self.label_3.setText(_translate("SLR1", "输入文法"))
        self.wenfa.setPlaceholderText(_translate("SLR1", "输入或打开txt\n如:\nA->B\nC->D|e"))
        self.label.setText(_translate("SLR1", "First集合"))
        self.label_2.setText(_translate("SLR1", "Follow集合"))
        self.label_7.setText(_translate("SLR1", "LR(0)DFA图"))
        self.label_4.setText(_translate("SLR1", "SLR(1)分析表"))
        self.label_6.setText(_translate("SLR1", "是否是SLR(1)文法"))


    def showDialog1(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '.')
        if fname[0]:
            f = open(fname[0], 'r')
            with f:
                data = f.read()
                self.wenfa.setText(data)
        
    def analyze(self):    
        #-----------初始化
        global Edges
        global time
        global first
        global follow
        global T
        global V
        global dfaStates
        global dic
        global node
        node=[]
        Edges=[]
        time=0
        first=[]
        follow=[]
        T=[]
        dic={}
        V=[]
        dfaStates=[dfaState(i) for i in range(99)]     
        self.graphicsView.clear()
        #------------------------------------------------------------------
        
        #获得从输入的文本边集---------------------------------------------
        
        wenfa_text=self.wenfa.toPlainText()+'\n\n'
        wenfa_text+='扩展文法：\n'
        edges=self.wenfa.toPlainText().strip().split('\n')
        print(edges)
        
        for e in edges:
            e=e.split('->')
            n2=e[1].split('|')
            if len(n2)>1:
                for i in range(len(n2)):
                    Edges.append(Edge(e[0],n2[i]))
            else:
                Edges.append(Edge(e[0],e[1]))
        Edges.insert(0,Edge(Edges[0].n1+"'",Edges[0].n1))
        num=0
        for edge in Edges:
            wenfa_text+='({0})'.format(str(num))+edge.n1+'->'+edge.n2+'\n'
            num=num+1
            print(edge.n1+'->'+edge.n2)
        self.wenfa.setText(wenfa_text)
        #-----------------------------------------------------------------------
        
        V,T=find_V_and_T(Edges) #求终结符和非终结符
        
        first=First(Edges,V) #求first集合
        
        #在界面中显示first集合-------------------------------------------------
        first_text=str()
        for key,value in first.items():
            first_text+='first({0})={1}\n'.format(key,str(value))
        self.First.setText(first_text)
        #---------------------------------------------------------------------
        
        #
        follow=Follow(Edges,V)#求follow集合
        
        #在界面中显示follow集合-------------------------------------------------
        follow_text=str()
        for key,value in follow.items():
            follow_text+='follow({0})={1}\n'.format(key,str(value))
        self.follow.setText(follow_text)
        #---------------------------------------------------------------------
        
        #构建nfa图（核心代码）-------------------------------------------------
         
        dfaStates[0]=init_dfa(Edges,Edges[0].n1,dfaStates[0])
        #判断当前结点是否已存在
        temp_node=dfaStates[0].edges.copy()
        temp_node.append(dfaStates[0].no)
        node.append(temp_node)
        queue=[]
        for ne in dfaStates[0].nextDfaState.items():
            queue.append([0,ne])
        while len(queue)>0:
            temp=queue.pop(0)
            dfaStates[temp[1][1]]=dfa(Edges,dfaStates[temp[0]].edges,temp[1][0],dfaStates[temp[1][1]])
           
            #判断当前结点是否已存在
            pos=check(dfaStates[temp[1][1]])
            #若已存在，则当前结点与已存在结点合并
            if pos>-1:
                time=time-len(dfaStates[temp[1][1]].nextDfaState)
                dfaStates[temp[0]].nextDfaState[temp[1][0]]=pos
                dfaStates.remove(dfaStates[temp[1][1]])
            #若不存在，则记录当前结点
            else:
                temp_node=dfaStates[temp[1][1]].edges.copy()
                temp_node.append(dfaStates[temp[1][1]].no)
                node.append(temp_node)
                
            if len(dfaStates[temp[1][1]].nextDfaState)>0 and pos==-1:
                for ne in dfaStates[temp[1][1]].nextDfaState.items():
                    queue.append([temp[1][1],ne])
                    
        #--------------------------------------------------------------------
        
        printDFA(dfaStates,time)#绘制DFA图
        
        #将DFA图在GUI中显示--------------------------------------------------
        
        # 0.获取光标对象
        tc = self.graphicsView.textCursor()
        # 1.创建一个 QTextImageFormat 对象
        tif = QTextImageFormat()
        
        # 2.设置相关的参数
        tif.setName("./image/output.jpg")    #图片名称
        tif.setWidth(1000)            #图片宽度
        tif.setHeight(800)           #图片高度
        
        tc.insertImage(tif)          #插入图片
        #---------------------------------------------------------------------
        
        
        table=SLR1TABLE(dfaStates,V,T)#求SLR(1)分析表
        
        #在界面中显示分析表---------------------------------------------------
        self.model=QStandardItemModel(len(table)-1,len(table[0])-1)#存储任意结构数据
        self.model.setHorizontalHeaderLabels(table[0][1:])
        row_name=[str(t[0]) for t in table if t[0]!='']
        self.model.setVerticalHeaderLabels(row_name)
        for row in range(1,len(table)):
            for column in range(1,len(table[0])):
                i=QStandardItem(table[row][column])
                self.model.setItem(row-1,column-1,i)
        self.tableView.setModel(self.model)
        #--------------------------------------------------------------------
        
        #判断是否是SLR(1)文法-------------------------------------------------
        rr_num,rp_num,rr_not_slr,rp_not_slr,is_slr1=is_SLR1(dfaStates,V,T)
        text=str()
        if len(rr_num)==0 and len(rp_num)==0:
            text+='是LR(0)文法，无规约-规约冲突与规约-移进冲突。'
        elif is_slr1==True:
            text+='是SLR(1)文法\n'
            for rp in rp_num:
                text+='状态{0}存在规约-移进冲突，但follow({1})∩{2}=Φ，SLR(1)文法可解决冲突。\n'.format(rp[0],rp[1],str(rp[2]))
            for rr in rr_num:
                text+='状态{0}存在规约-规约冲突，但follow({1})∩follow({2})=Φ，SLR(1)文法可解决冲突。\n'.format(rr[0],rr[1],rr[2])
        
        elif is_slr1==False:
            text+='不是SLR(1)文法\n'
            for rp in rp_not_slr:
                text+='状态{0}存在规约-移进冲突，但follow({1})∩{2}={3}≠Φ，SLR(1)文法无法解决冲突。\n'.format(rp[0],rp[1],str(rp[2]),str(rp[3]))
            for rr in rr_not_slr:
                text+='状态{0}存在规约-规约冲突，但follow({1})∩follow({2})={3}≠Φ，SLR(1)文法无法解决冲突。\n'.format(rr[0],rr[1],rr[2],str(rr[3]))
        self.is_slr1.setText(text)
        #---------------------------------------------------------------------
        
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow


class UsingTest(QMainWindow, Ui_SLR1):
    def __init__(self, *args, **kwargs):
        super(UsingTest, self).__init__(*args, **kwargs)
        self.setupUi(self)  # 初始化ui    
if __name__=='__main__':  
    
    app = QApplication(sys.argv)
    win = UsingTest()
    win.show()
    sys.exit(app.exec_())