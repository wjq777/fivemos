#五管运算放大器

import random
import os
import re
import psutil
import sys

pop_size = 50
generation = 500
#1.种群初始化

nodeSet = ["Vout", "Vin", "1"] #GNDA VDDA Vn Vout Vp
#allSet = ["Vout","2","1","Vp","Vn"]

"""
def generateChom_paper(length):
    nodeSet = ["Vin","Vout"]
    componentSet = ["NMOS", "NMOS","PMOS","PMOS"]  # 此处可以控制电路的器件比例
    else_Input = ["Vp", "Vn"]
    chrom = []
    instruction = ["1","1","1","2"]

    for i in range(length):
        chrom_pice = {}
        if (i==0):
            chrom_pice["instruction"] = "1"
            type = random.choice(componentSet)
            if (type == "NMOS"):

                chrom_pice['type'] = type
                chrom_pice['node1'] = random.choice(nodeSet)
                #去掉type保证2个Nmos 2个Pmos 减少复杂度
                componentSet.remove(type)

                node2 = random.choice(else_Input)
                else_Input.remove(node2)  # 去掉一个输入端
                chrom_pice['node2'] = node2

                chrom_pice['node3'] = random.choice(nodeSet)
                chrom_pice['node4'] = "GNDA"

            else:
                chrom_pice['type'] = type
                componentSet.remove(type)

                chrom_pice['node1'] = random.choice(nodeSet)
                chrom_pice['node2'] = random.choice(nodeSet)
                chrom_pice['node3'] = "VDDA"
                chrom_pice['node4'] = "VDDA"
        if(i>0):
            instruction = random.choice(instruction)
            if(instruction=="1"):
                chrom_pice["instruction"] = "1"
                chrom_pice['type'] = random.choice(componentSet)
                if (chrom_pice['type'] == "NMOS"):
                    chrom_pice['node1'] = random.choice(nodeSet)

                    node2 = random.choice(else_Input)
                    else_Input.remove(node2)  # 去掉一个输入端
                    chrom_pice['node2'] = node2

                    chrom_pice['node3'] = random.choice(nodeSet)
                    chrom_pice['node4'] = "GNDA"






    return chrom


def generateChom_version1(length):
    # 节点集合  初始节点
    componentSet = ["NMOS", "PMOS"]  # 此处可以控制电路的器件比例
    nodeSet = ["Vout", "2", "1"]  # GNDA VDDA Vn Vout Vp
    nodeSet_Input = ["Vp", "Vn"]
    chrom = []
    index = 1

    for i in range(length):

        chrom_pice = {}
        chrom_pice['type'] = random.choice(componentSet)
        if (chrom_pice['type'] == "NMOS"):
            chrom_pice['node3'] = "GNDA"
            chrom_pice['node4'] = "GNDA"
            if (len(nodeSet_Input) != 0):
                # 先把输入端放在NMOS的node2上
                chrom_pice['node1'] = random.choice(nodeSet)
                node2 = random.choice(nodeSet_Input)
                nodeSet_Input.remove(node2)  # 去掉一个输入端
                chrom_pice['node2'] = node2
            else:
                chrom_pice['node1'] = random.choice(nodeSet)
                chrom_pice['node2'] = random.choice(nodeSet)
        if (chrom_pice['type'] == "PMOS"):
            chrom_pice['node1'] = random.choice(nodeSet)
            chrom_pice['node2'] = random.choice(nodeSet)
            chrom_pice['node3'] = "VDDA"
            chrom_pice['node4'] = "VDDA"


        chrom.append(chrom_pice)





    return chrom
"""

def generateChom(length):
    # 节点集合  初始节点
    componentSet = ["NMOS","NMOS", "PMOS", "PMOS"]  # 此处可以控制电路的器件比例

    nodeSet = ["Vout", "Vin", "1"]  # GNDA VDDA Vn Vout Vp
    nodeSet_Input = ["Vp", "Vn"]
    chrom = []
    index = 1

    for i in range(length):
        chrom_pice = {}


        if (i<=1):
            type = "NMOS"

            chrom_pice['type'] = type
            #componentSet.remove(type)

            # node1
            chrom_pice['node1'] = random.choice(nodeSet)

            # node2
            node2 = random.choice(nodeSet_Input)
            nodeSet_Input.remove(node2)  # 去掉一个输入端
            chrom_pice['node2'] = node2

            # node3
            chrom_pice['node3'] = random.choice(nodeSet)

            # node4
            chrom_pice['node4'] = "GNDA"




        if (i > 1):
            type = "PMOS"

            #componentSet.remove(type)
            chrom_pice['type'] = type
            chrom_pice['node1'] = random.choice(nodeSet)
            chrom_pice['node2'] = random.choice(nodeSet)
            chrom_pice['node3'] = "VDDA"
            chrom_pice['node4'] = "VDDA"


        chrom.append(chrom_pice)





    return chrom

def usingHspiceToGetfit(chrom_val, out_file_name):

    exe_path = r'C:\synopsys\Hspice_C-2009.09\BIN\hspice.exe'  # hspice 软件安装的位置
    var_file_name = 'netlist'  # 参数文件名称，即网表的名称
    in_file_name = 'myfivemos'  # .sp文件名称
    source_path = 'E:\hspiceProject\myFiveMos_ee'
    #把染色体的值写进网表文件
    nestlistFile = open(source_path + '\\' + var_file_name, 'w+')  # w+:新建读写，会将文件内容清零;若文件不存在，创建
    nestlistFile.write('.PARAM' + '\n')
    nestlistFile.write('.SUBCKT FIVEMOS_ee GNDA VDDA Vb Vn Vout Vp' + '\n')
    for i in range(len(chrom_val)):
        type = chrom_val[i]['type']
        if (type == "NMOS"):
            type = 'n18e2r'
        else:
            type = 'p18e2r'
        node1 = chrom_val[i]['node1']
        node2 = chrom_val[i]['node2']
        node3 = chrom_val[i]['node3']
        node4 = chrom_val[i]['node4']
        nestlistFile.write('M'+ str(i+1) + ' ' +
                node1 + ' ' + node2 + ' ' + node3 + ' ' + node4 + ' ' + type + ' ' +
                           'W=6u L=2u M=1' + '\n')
    nestlistFile.write('M6 Vb Vb GNDA GNDA n18e2r W=500n L=2u M=1' + '\n')
    nestlistFile.write('M5 Vin Vb GNDA GNDA n18e2r W=1.9u L=2u M=1' + '\n')
    nestlistFile.write('.ENDS' + '\n')
    nestlistFile.close()



    while 1:
        if os.path.exists(source_path + '\\' + var_file_name):
            break

    ct_var_file = os.path.getmtime(source_path + '\\' + var_file_name)  # ct:create time #获取修改时间
# 调用hspice软件仿真
    proc = psutil.Popen(exe_path + ' -i ' + source_path + '\\' + in_file_name + '.sp' + ' -o ' + source_path + '\\'
                        + out_file_name)

    # 读仿真输出文件的参数值
    while 1:
        if os.path.exists(source_path + '\\' + out_file_name + '.lis'):  # 数据已写入文件，则停止等待
            # 异常处理1
            counter0 = 0
            while 1:
                try:
                    ct_out_file = os.path.getmtime(source_path + '\\' + out_file_name + '.lis')  # 获取输出文件的修改时间
                    break
                except FileNotFoundError:
                    counter0 += 1
            if ct_out_file > ct_var_file:  # 不满足，则证明数据未输出到文件中
                # time.sleep(1)
                break
            # 等待 hspice 进程结束，否则会跟后面打开仿真输出文件发生冲突
        try:
            while 1:
                if proc.pid not in psutil.pids():
                    break
        except:
            print('Unexpected error:', sys.exc_info()[0])
        # 异常处理2
        counter1 = 0
        while 1:
            try:
                #print(source_path + out_file_name + '.lis')
                with open(source_path + out_file_name + '.lis', 'r+') as fp:
                    data = fp.read()
                break
            except PermissionError:
                counter1 += 1
    #print(data)
    result1 = re.search(r'\s*1.0000e\+00\s*(.*)\s', data)
    #print(result1)
    #if(result1 == None):
    #    return 0

    gain = (float(result1.group(1))) #增益

    #if (gain<=0):
    #    return 0

    #算带宽的正则
    """
    #result2 = re.search(r'\+\d\d\s*-(.*)',data)
    result2 = re.search(r'(.*)\+\d\d\s*-\d\.\d\d\de', data)
    print(result2)
    """

    return gain

def fit_cal(chrom, source_path):
    #STEP1 删除目录下的文件
    def delete_dir(path):
        del_list = os.listdir(path)
        for f in del_list:
            os.remove(path + '\\' + f)
        os.removedirs(path)

#确保source_path\path_data'文件下为空
    chrom_val = {}
    path_data = source_path + r'\output_data'
    if os.path.exists(path_data):  # 如果 /data 不为空，则删除
        delete_dir(path_data)
        # 加个循环，确保删除
        while os.path.exists(path_data):
            delete_dir(path_data)
        os.mkdir(path_data)
    else:  os.mkdir(path_data)      # 否则，新建该目录

    # sp_fit_func(chrom, out_file_name)作用为：修改netlist ，然后仿真，得到输出文件的参数结果
    #输出文件名为out_file_name

    file_counter = 0 #文件数量
    for key, val in chrom.items():    # key=0 1 2 3 4 。如  key=0时，val = [{'instruction ': '1', 'node1': 'VCC', 'node2': 'OUT', 'node3': 'VCC', 'node4': 'VCC', 'type': 'PMOS', 'param1': '1U', 'param2': '20U'}, {'instruction ': '1', 'node1': 'VCC', 'node2': 'OUT', 'node3': 'VCC', 'node4': 'VCC', 'type': 'PMOS', 'param1': '1U', 'param2': '20U'}]

        out_file_name = r'\output_data' + r'\out_file' + str(file_counter)  # 输出的 .lis 文件的名称
        file_counter += 1

        #计算
        chrom_val[key] = usingHspiceToGetfit(val,out_file_name)#计算第key个染色体的适应值
        # val = [{'instruction ': '1', 'node1': 'VCC', 'node2': 'OUT', 'node3': 'VCC', 'node4': 'VCC', 'type': 'PMOS','param1': '1U', 'param2': '20U'},{'instruction ': '1', 'node1': 'VCC', 'node2': 'OUT', 'node3': 'VCC', 'node4': 'VCC', 'type': 'PMOS','param1': '1U', 'param2': '20U'}]

    fit_val = chrom_val
    return fit_val

def select(fit_val, chrom):
    """
    select(): 选择函数，根据染色体的适应度值选择种群中的染色体
    :param fit_val: 这一代中所有染色体的适应度值，为一个数值，为 dict
    :param chrom: 这一代种群的所有染色体，为 dict
    :return:

    选择操作使用的算法是锦标赛法：从种群中随机选择 k 个个体，比较这 k 个个体的适应度，将适应度最高的个体选入下一代；重复上述
    过程，直到达到预定规模. 这里的 k 取一般值2，预定规模为本代种群规模.
    """
    population = [key for key in chrom]

    selected_chrom, selected_val = {}, {}  # 完成选择后的种群
    for i in range(len(chrom)):
        tem = random.choices(population, k=2)
        tem_val = {}
        for j in tem:
            tem_val[j] = fit_val[j]  # 获取对应的适应度值
        max_chrom = max(zip(tem_val.values(), tem_val.keys()))
        selected_chrom[i], selected_val[i] = chrom[max_chrom[1]], max_chrom[0]  # 得到一个选择的染色体及其适应度值

    return selected_chrom, selected_val

def cross(selected_chrom):
    #进行单点交叉
    population_index = [key for key in selected_chrom] #[0, 1, 2, 3, 4, 5, ...., 49]
    crossed_chrom = {}
    counter = 0

    while counter < len(selected_chrom):
        #留前百分之10个适应度值最高的直接进入下一代
        best10per = int(0.2 * (len(selected_chrom)))
        if(counter < best10per):
            crossed_chrom[counter] = selected_chrom[counter]
            counter += 1
            continue

        while(1):
            tem = random.choices(population_index,k=2) #选择两个父代
            if(tem[0]!=tem[1]):
                break
        chrom_tem = []
        #从中间交叉
        chrom_tem.append(selected_chrom[tem[0]][0])  # 第一个父代的第1段
        chrom_tem.append(selected_chrom[tem[0]][1])  # 第一个父代的第2段
        chrom_tem.append(selected_chrom[tem[1]][2])  # 第二个父代的第3段
        chrom_tem.append(selected_chrom[tem[1]][3])  # 第二个父代的第4段
        """
        cross_point = random.choice([1,2,3])
        if(cross_point == 1):
            chrom_tem.append(selected_chrom[tem[0]][0]) #第一个父代的第0段
            chrom_tem.append(selected_chrom[tem[1]][1]) #第二个父代的第1段
            chrom_tem.append(selected_chrom[tem[1]][2]) #第二个父代的第2段
            chrom_tem.append(selected_chrom[tem[1]][3]) #第二个父代的第3段
        if (cross_point == 2):
            chrom_tem.append(selected_chrom[tem[0]][0])  # 第一个父代的第1段
            chrom_tem.append(selected_chrom[tem[0]][1])  # 第一个父代的第2段
            chrom_tem.append(selected_chrom[tem[1]][2])  # 第二个父代的第3段
            chrom_tem.append(selected_chrom[tem[1]][3])  # 第二个父代的第4段
        if (cross_point == 3):
            chrom_tem.append(selected_chrom[tem[0]][0])  # 第一个父代的第1段
            chrom_tem.append(selected_chrom[tem[0]][1])  # 第一个父代的第2段
            chrom_tem.append(selected_chrom[tem[0]][2])  # 第二个父代的第3段
            chrom_tem.append(selected_chrom[tem[1]][3])  # 第二个父代的第4段
        """
        crossed_chrom[counter] = chrom_tem
        counter += 1

    return crossed_chrom

def cross_version1(selected_chrom, selected_val):
    max_index = sorted(selected_val, key=lambda x: selected_val[x]) #若不交叉，则选择适应度最强的作为下一代
    max_flag = 0 #用作不交叉时从大到小取值
    #print('max_index',max_index)
    population_index = [key for key in selected_chrom] #[0, 1, 2, 3, 4, 5, 6]
    p_cross = 0.2 #交叉概率
    crossed_chrom = {}
    counter = 0
    while counter < len(selected_chrom):
        p_this = random.uniform(0,1)
        if p_this<p_cross:
            #进行交叉
            tem = random.choices(population_index,k=2) #[0, 1, 2, 3, 4, 5, 6]
            chrom_tem = []
            chrom_tem.append(selected_chrom[tem[0]][0])
            chrom_tem.append(selected_chrom[tem[1]][1])
            crossed_chrom[counter] = chrom_tem
            #print('交叉：',counter)
            counter += 1
        else:
            chrom_tem = []
            chrom_tem= selected_chrom[max_index[max_flag]]
            crossed_chrom[counter] = chrom_tem
            #print('未交叉：', counter)
            #print('选取父代index为：',max_index[max_flag])
            max_flag += 1
            counter += 1
    return crossed_chrom

def mutate(crossed_chrom):
    """
    mutate(): 变异操作函数，对杂交后的后代进行变异操作
    :param crossed_chrom: 杂交后代的染色体
    :return:

    变异操作：先定为参数不变，MOS管第3,4个节点发生变
    """
    mutated_chrom = crossed_chrom
    p_mutate = 0.6#变异概率
    random_num = random.random()
    if (random_num < p_mutate):  # 发生变异
        chrom_length = len(crossed_chrom)
        mutate_num = 2
        for i in range(mutate_num):
            chrom_index = random.randint(0, chrom_length - 1)
            chromPiece_index = random.choice([0,1,2,3])
            if(mutated_chrom[chrom_index][chromPiece_index]['type'] == "NMOS"):
                mutated_chrom[chrom_index][chromPiece_index][random.choice(["node1","node3"])] = random.choice(nodeSet)
            if (mutated_chrom[chrom_index][chromPiece_index]['type'] == "PMOS"):
                mutated_chrom[chrom_index][chromPiece_index][random.choice(["node1","node2"])] = random.choice(nodeSet)

    return mutated_chrom

def ga_optimize(fit_val, chrom,source_path):
    """
        :param fit_val: 这一代中所有染色体的适应度值，为一个数值，为 dict
        :param chrom: 这一代种群的所有染色体，为 dict
        :return: new_chrom, 子代染色体
        :return: new_chrom_fitval, 子代染色体的适应度值，为降序排序，与new_chrom对应

    ########################测试
    chrom = selected_chrom
    fitval = selected_val
    newChrom = {}
    newFitval = {}
    # 排序
    fitval = sorted(fitval.items(), key=lambda x: x[1], reverse=True)
    for i in range(len(fitval)):
        newFitval[i] = fitval[i][1]
        newChrom[i] = chrom[fitval[i][0]]
    print(newFitval)
    ########################测试

    crossed_chrom = cross(selected_chrom)  # 交叉
    ########################测试
    fitval = fit_cal(crossed_chrom, source_path)  # 交叉后的种群适应度计算
    chrom = crossed_chrom
    newChrom = {}
    newFitval = {}

    # 排序
    fitval = sorted(fitval.items(), key=lambda x: x[1], reverse=True)
    for i in range(len(fitval)):
        newFitval[i] = fitval[i][1]
        newChrom[i] = chrom[fitval[i][0]]
    print(newFitval)

    ########################测试

    """

    selected_chrom, selected_val = select(fit_val, chrom)  # 选择
    crossed_chrom = cross(selected_chrom)  # 交叉
    mutated_chrom = mutate(crossed_chrom)  # 变异

    mutated_chrom_fitval = fit_cal(mutated_chrom,source_path)  # 变异后的种群适应度计算
    chrom = mutated_chrom
    fitval = mutated_chrom_fitval
    newChrom = {}
    newFitval = {}

    #排序
    fitval = sorted(fitval.items(), key=lambda x: x[1], reverse=True)
    for i in range(len(fitval)):
        newFitval[i] = fitval[i][1]
        newChrom[i] = chrom[fitval[i][0]]

    return newChrom, newFitval

#相关全局变量
source_path=r'E:\hspiceProject\myFiveMos_ee' #路径
var_file_name = 'netlist'  # 参数文件名称，即网表的名称
in_file_name = 'myfivemos'  # .sp文件名称

#1.初始化种群并计算初始种群适应度
chrom = {}
for i in range(pop_size):
    chrom[i] = generateChom(4)
print(chrom)
"""
chrom[0][0]['type'] = 'NMOS'
chrom[0][0]['node1'] = 'Vout'
chrom[0][0]['node2'] = 'Vn'
chrom[0][0]['node3'] = '2'
chrom[0][0]['node4'] = 'GNDA'
chrom[0][1]['type'] = 'NMOS'
chrom[0][1]['node1'] = '1'
chrom[0][1]['node2'] = 'Vp'
chrom[0][1]['node3'] = '2'
chrom[0][1]['node4'] = 'GNDA'
chrom[0][2]['type'] = 'PMOS'
chrom[0][2]['node1'] = '1'
chrom[0][2]['node2'] = '1'
chrom[0][2]['node3'] = 'VDDA'
chrom[0][2]['node4'] = 'VDDA'
chrom[0][3]['type'] = 'PMOS'
chrom[0][3]['node1'] = 'Vout'
chrom[0][3]['node2'] = '1'
chrom[0][3]['node3'] = 'VDDA'
chrom[0][3]['node4'] = 'VDDA'
"""


fit_val = fit_cal(chrom=chrom, source_path=source_path)  # 计算初始种群的适应度

best_chrom = {}
best_chrom_fitval = {}



gen = 0
while(fit_val[0]<48):
    new_chrom, new_chrom_fitval = ga_optimize(fit_val,chrom=chrom,source_path=source_path)  # ga 寻优
    best_chrom[gen], best_chrom_fitval[gen] = new_chrom[0], new_chrom_fitval[0]  # 存储当代最优的染色体及其适应度值
    chrom, fit_val = new_chrom, new_chrom_fitval  # 新的种群
    print('现在是第 ' + str(gen) + ' 代')
    print('fit_val:',fit_val)
    print('best_chrom_fitval',best_chrom_fitval)

    #保存每一代最好最差的结果到一个文件中

    f = open("E:\hspiceProject\myFiveMos_ee\genInformation\genInformation.txt","a")
    f.write(str(gen)+"代"+":"+ str(fit_val[0])+ " " + str(fit_val[len(fit_val)-1]) +"\n")

    f.write("best :" + str(fit_val[0]) + "\n")
    #写chrom[0]
    for i in range(len(chrom[0])):
        type = chrom[0][i]['type']

        node1 = chrom[0][i]['node1']
        node2 = chrom[0][i]['node2']
        node3 = chrom[0][i]['node3']
        node4 = chrom[0][i]['node4']

        f.write('M'+ str(i+1) + ' ' + node1 + ' ' + node2 + ' ' + node3 + ' ' + node4 + ' ' + type + ' ' + 'W=6u L=2u M=1' + '\n')

    # 写chrom[last]
    last_index = len(chrom)-1
    f.write("worst: "+str(fit_val[len(fit_val)-1]) +"\n")
    for i in range(len(chrom[0])):
        type = chrom[last_index][i]['type']

        node1 = chrom[last_index][i]['node1']
        node2 = chrom[last_index][i]['node2']
        node3 = chrom[last_index][i]['node3']
        node4 = chrom[last_index][i]['node4']

        f.write('M'+ str(i+1) + ' ' + node1 + ' ' + node2 + ' ' + node3 + ' ' + node4 + ' ' + type + ' ' + 'W=6u L=2u M=1' + '\n')






    f.write("******************"+"\n")



    f.close()



    gen += 1



