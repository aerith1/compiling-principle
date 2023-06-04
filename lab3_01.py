#文法
dict={
    "S":['aAB', 'd'],
    "A":['bAS','ε'],
    "B":['cAB', 'ε']
}
# 文法右部
Vr=[]
for item in dict.keys():
    Vr.extend(dict[item])
Vr=list(set(Vr))
Vr.sort()
#非终结符
VN=[]
for item in dict.keys():
    VN.append(item)
print("非终结符VN集合为：{}".format(VN))
 
#终结符
VT=[]
for item in dict.values():
    for it in item:#遍历key值
        for i in it:
            if i not in VN: 
                VT.append(i)
VT=list(set(VT))
# 排序
VT.sort()
# VT.append("ε")
print("终结符VT集合为:{}".format(VT))

#翻转字符串，返回字符串
def Reverse(str):
    return str[::-1]

#找产生式,返回产生式右部
def findR(Vn,str0):
    if Vn in dict.keys() :
        ProRight=dict[Vn]
        for str in ProRight:
            if str0 == str[0]:
                return str
    return ''

def findL(item):
    for SL in VN:
        for it in dict[SL]:
            if it == item:
                return SL
    return ''

# 将产生式添加进栈内
def addS(V,S):
    newS=list(S)
    for i in V:
        newS.append(i)
    return  newS

# 获取 First集
def Fi(S):
    if S in VN:
        Fi=[]
        return First(S,Fi)
    else:
        return list(S)
def First(S,Fi):
    for item in dict[S]:
        if item[0] in VT:
            Fi.append(item[0])
        else:
            First(item[0],Fi)
    Fi = list(set(Fi))
    Fi.sort()
    return Fi

#print(Fi('B'))

# 获取 Follow 集
def Fo(S):
    if S in VN:
        Fo=[]
        Fo=Follow(S,Fo)
        Fo = list(set(Fo))
        Fo.sort()
        if 'ε' in Fo:
            Fo.remove('ε')
        return Fo
    else:
        return list(S) 
def Follow(S,Fo):
    if S == VN[0]:
        Fo.append('#')
        return Fo
    for item in Vr:
        if S in item:
            i = item.index(S)
            if i+1 < len(item):
                # aBc
                if item[i+1] in VT:
                    Fo.append(item[i+1])
                # A->aBC
                elif item[i+1] in VN:
                     First(item[i+1],Fo)
                     # C->ε
                     if findR(item[i+1],'ε') != '' and findL(item) != item[len(item)-1]:
                        Follow(findL(item),Fo)
            # aB
            else:
                if findL(item) != item[len(item)-1]:
                    Follow(findL(item),Fo)
                else:
                    pass

    return Fo

# 获取 Select 集
def Se(S,V):
    if S in VN:
        Se=[]
        return Select(S,V,Se)
def Select(S,V,Se):
    if V[0] in VT and V[0] != 'ε':
        return list(V[0])
    elif V[0] == 'ε':
        Se.extend(Fo(S))
        return Se
    elif V[0] in VN:
        if 'ε' in dict[V[0]]:
            Se.extend(V[1])
            Se.remove('ε')
            Se.extend(Fo(V[0]))
        Se.extend(Fi(V[0]))
        return Se
    return Se

# 获取 匹配的产生式
def So(S,vn):
    if findR(S,vn) != '':
        for t in dict[S]:
            if vn in Se(S,t):
                return t 
    return ''
print(So('S','a'))

# 分析表
VTn=[]
VTn = VT[:]
VTn.remove('ε')
VTn.append('#')
print('分析表：')
print("  ",end='')
print(''.join(str(i).center(5) for i in VTn))
for S in VN:
    li = []
    for i in range(len(VT)):
        li.append('err')
    print(S,end=' ')
    for Si in dict[S]:
        for item in VTn:
            if item in Se(S,Si):
                i = VTn.index(item)
                li[i] = Si
    print(''.join(str(i).center(5) for i in li))
    print('\n')


#输入串
str=list(input("请输入要分析的符号串："))
str.append("#")
#步骤
count=0 
#符号栈
S=["#"]
S.append(VN[0])
VR=""
print("步骤\t符号栈S[i]\t输入串str[j]\t产生式")
while len(S)!=0:
    count += 1
    s0 = str[0]
    #VR0 = findR(S[-1], str[0])
    VR0 = So(S[-1], str[0])
    if S[-1] == "#" and s0 == "#":
        print("%s\t%s\t%s\t acc" % ( count, "".join(S).center(10), "".join(str).center(10)))
        print("输入符号串是该文法的句子！")
    elif VR0 != "" and S[-1] not in VT:
        print("%s\t%s\t%s\t%s" % ( count, "".join(S).center(10), "".join(str).center(10), S[-1] + "->" + VR0 ))
    elif  VR0 in VT or S[-1]  in VT:
        print("%s\t%s\t%s\t匹配弹出%s" % ( count, "".join(S).center(10), "".join(str).center(10),str[0]))
    elif findR(S[-1],'ε') != '':
        print("%s\t%s\t%s\t%s" % ( count, "".join(S).center(10), "".join(str).center(10), S[-1] + "->ε"))
    elif VR0=="":
        print("输入符号串不是该文法的句子！")
        break
    PopS = S.pop()
    VR = findR(PopS, str[0])
    if PopS not in VT:#如果栈顶元素不是终结字符
        if VR!="":
            if VR[0] in VN :
                temp = Reverse(VR)
                S = addS(temp,S)
            elif VR[0] in VT and VR[0]!="ε":
                temp = Reverse(VR)
                S = addS(temp, S)
            elif VR[0]=="ε" and VR[0] in VT:
                pass
        elif VR=="":    
            pass
    elif PopS in VT:
        if s0==PopS:
            if PopS=="#":
                print("输入符号串是该文法的句子！")
            elif PopS!="#":
                str = str[1:]
        elif s0!=PopS:
            if PopS=="#":
                print("输入符号串不是该文法的句子！")
                pass