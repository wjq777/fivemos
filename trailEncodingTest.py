import random
import os
import re
import psutil
import sys
import copy
import time
def generateChom(length):
    # 节点集合  初始节点
    componentSet = ["NMOS","PMOS","NMOS","PMOS"]  # 五管所需要的总数
    nodeSet = [255, 0]  # GNDA VDDA Vn Vout Vp
    nodeSet_Bias = ['CTP', 'CTN']
    Instruciton = ["MTN","CTP","MTN","CTP"]

    chrom = []          #[{},{},{}]

    while(len(chrom)<length):
        chrom_pice = {} #临时的一个字典，代表种群中的一个个体
        active_node = nodeSet[len(nodeSet)-1]
        instruciton = random.choice(Instruciton)
        Instruciton.remove(instruciton)
        type = random.choice(componentSet)
        componentSet.remove(type)
        #print(instruciton,type)
        if(instruciton == "MTN"):
            active_node += 1
            nodeSet.append(active_node)
            if(type == "NMOS"):
                #NMOS 	incoming：node3  outcoming：node1
                chrom_pice['ins'] = instruciton
                chrom_pice['type'] = type
                chrom_pice['node1'] = "outcoming"

                Bias = random.choice(nodeSet_Bias)
                nodeSet_Bias.remove(Bias)
                chrom_pice['node2'] = Bias   #fixed


                chrom_pice['node3'] = "incoming"
                chrom_pice['node4'] = "CTG"    # fixed
            if (type == "PMOS"):
                # PMOS   incoming：node2  outcoming：node1
                chrom_pice['ins'] = instruciton
                chrom_pice['type'] = type
                chrom_pice['node1'] = "outcoming"
                chrom_pice['node2'] ="incoming"
                chrom_pice['node3'] = "CTV"    # fixed
                chrom_pice['node4'] = "CTV"    # fixed



        if(instruciton == "CTP"):
            if (type == "NMOS"):
                # NMOS 	incoming：node3  outcoming：node1
                chrom_pice['ins'] = instruciton
                chrom_pice['type'] = type
                chrom_pice['node1'] = "outcoming"

                Bias = random.choice(nodeSet_Bias)
                nodeSet_Bias.remove(Bias)
                chrom_pice['node2'] = Bias  # fixed

                chrom_pice['node3'] = "incoming"
                chrom_pice['node4'] = "CTG"  # fixed
            if (type == "PMOS"):
                # PMOS   incoming：node2  outcoming：node1
                chrom_pice['ins'] = instruciton
                chrom_pice['type'] = type
                chrom_pice['node1'] = "outcoming"
                chrom_pice['node2'] = "incoming"
                chrom_pice['node3'] = "CTV"  # fixed
                chrom_pice['node4'] = "CTV"  # fixed

            chrom_pice["step"] = random.randint(0,active_node)
        chrom.append(chrom_pice)


    return chrom

def get_activeNum(chrom):
    activeNum = 0
    for item in chrom:
        if(item['ins']=='MTN'):
            activeNum +=1
    return activeNum

def decodeChom(chrom):

    decode_chrom = {}
    pop_size = len(chrom)

    for i in range(pop_size): #遍历每一个个体
        active_node = 0
        decode_chrom_one = []
        for item in chrom[i]:
            decode_chromPiece = {}
            if(item['ins'] == 'MTN'):
                active_node += 1
                decode_chromPiece['ins'] = item['ins']
                decode_chromPiece['type'] = item['type']
                if(decode_chromPiece['type'] == 'PMOS'):

                    #判断输入输出端口
                    if(item['node1']=='outcoming'):
                        decode_chromPiece['node1'] = str(active_node)
                        decode_chromPiece['node2'] = str(active_node - 1)
                    else:
                        decode_chromPiece['node1'] = str(active_node - 1)
                        decode_chromPiece['node2'] = str(active_node)

                    decode_chromPiece['node3'] = 'VDDA'
                    decode_chromPiece['node4'] = 'VDDA'
                if (decode_chromPiece['type'] == 'NMOS'):

                    if(item['node1']=='outcoming'):
                        decode_chromPiece['node1'] = str(active_node)
                        decode_chromPiece['node3'] = str(active_node - 1)
                    else:
                        decode_chromPiece['node1'] = str(active_node - 1)
                        decode_chromPiece['node3'] = str(active_node)


                    node2 = item['node2']
                    if (node2 == 'CTP' ) :
                        decode_chromPiece['node2'] = "Vp"
                    if (node2 == 'CTN'):
                        decode_chromPiece['node2'] = "Vn"

                    decode_chromPiece['node4'] = 'GNDA'

            if (item['ins'] == 'CTP'):
                decode_chromPiece['ins'] = item['ins']
                step = item['step']
                decode_chromPiece['type'] = item['type']
                if (decode_chromPiece['type'] == 'PMOS'):

                    # 判断输入输出端口
                    if (item['node1'] == 'outcoming'):
                        decode_chromPiece['node1'] = str(active_node)
                        decode_chromPiece['node2'] = str(active_node - step)
                    else:
                        decode_chromPiece['node1'] = str(active_node - step)
                        decode_chromPiece['node2'] = str(active_node)

                    decode_chromPiece['node3'] = 'VDDA'
                    decode_chromPiece['node4'] = 'VDDA'
                if (decode_chromPiece['type'] == 'NMOS'):

                    if (item['node1'] == 'outcoming'):
                        decode_chromPiece['node1'] = str(active_node)
                        decode_chromPiece['node3'] = str(active_node - step)
                    else:
                        decode_chromPiece['node1'] = str(active_node - step)
                        decode_chromPiece['node3'] = str(active_node)

                    node2 = item['node2']
                    if (node2 == 'CTP'):
                        decode_chromPiece['node2'] = "Vp"
                    if (node2 == 'CTN'):
                        decode_chromPiece['node2'] = "Vn"

                    decode_chromPiece['node4'] = 'GNDA'

            decode_chrom_one.append(decode_chromPiece)

        decode_chrom[i] = decode_chrom_one

    return decode_chrom

def usingHspiceToGetfit(chrom_val, out_file_name):
    activeNum = get_activeNum(chrom_val)
    #print(activeNum)

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
        if(node1 == '0'):
            node1 = 'Vin'
        if(node1 == str(activeNum)):
            node1 = 'Vout'

        node2 = chrom_val[i]['node2']
        if (node2 == '0'):
            node2 = 'Vin'
        if (node2 == str(activeNum)):
            node2 = 'Vout'

        node3 = chrom_val[i]['node3']
        if (node3 == '0'):
            node3 = 'Vin'
        if (node1 == str(activeNum)):
            node3 = 'Vout'

        node4 = chrom_val[i]['node4']
        if (node4 == '0'):
            node4 = 'Vin'
        if (node4 == str(activeNum)):
            node4 = 'Vout'

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
    if(result1 == None):
        return -999

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
    chrom = decodeChom(chrom)

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
    #交叉 没想好怎么交叉
    return  selected_chrom
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

        crossed_chrom[counter] = chrom_tem
        counter += 1

    return crossed_chrom

def mutate(crossed_chrom):
    """
    mutate(): 变异操作函数，对杂交后的后代进行变异操作
    :param crossed_chrom: 杂交后代的染色体
    :return:

    变异操作：变异操作有两种：1.输入输出点的变异；2.操作指令的变异

    此处可以克隆选择算法
    """
    mutated_chrom = crossed_chrom
    p_mutate = 0.6  # 变异概率
    random_num = random.random()
    if (random_num < p_mutate):  # 发生变异
        chrom_length = len(crossed_chrom)  # 种群个数

        chrom_individual_index = random.randint(0, chrom_length - 1) #选择的个体index
        chrom_individual  = mutated_chrom[chrom_individual_index] #选择的个体染色体
        #print("chrom_individual",chrom_individual)

        #在个体中选择CTP的操作
        chrom_piece_index = 5
        while(True):
            chrom_piece_index = random.randint(0, len(chrom_individual) - 1)
            if(chrom_individual[chrom_piece_index]['ins'] == 'CTP'):
                break


        active_num = get_activeNum(chrom_individual)
        #克隆小种群，小种群个数为active_node的个数 改变Step
        clone_Chrom = {}

        for i in range(active_num+1):
            chrom_individual[chrom_piece_index]['step'] = i
            clone_Chrom[i] = copy.deepcopy(chrom_individual)

        #print('克隆种群clone_Chrom', clone_Chrom)
        # 计算适应度值
        fit_val_clone = fit_cal(clone_Chrom, source_path)
        #print("克隆适应度值",fit_val_clone)

        #排序
        newChrom = {}
        newFitval = {}
        # 排序
        fitval = sorted(fit_val_clone.items(), key=lambda x: x[1], reverse=True)
        for i in range(len(fitval)):
            newFitval[i] = fitval[i][1]
            newChrom[i] = clone_Chrom[fitval[i][0]]
        #用适应度最大值替代原有的个体
        print("克隆适应度值", newFitval)
        mutated_chrom[chrom_individual_index] = newChrom[0]
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

start = time.clock()
#相关全局变量
source_path=r'E:\hspiceProject\myFiveMos_ee' #路径
var_file_name = 'netlist'  # 参数文件名称，即网表的名称
in_file_name = 'myfivemos'  # .sp文件名称
pop_size = 5

"""
tem = {0: [{'ins': 'MTN', 'type': 'NMOS', 'node1': 'outcoming', 'node2': 'CTP', 'node3': 'incoming', 'node4': 'CTG'},
           {'ins': 'CTP', 'type': 'PMOS', 'node1': 'outcoming', 'node2': 'incoming', 'node3': 'CTV', 'node4': 'CTV', 'step': 0},
           {'ins': 'MTN', 'type': 'PMOS', 'node1': 'outcoming', 'node2': 'incoming', 'node3': 'CTV', 'node4': 'CTV'},
           {'ins': 'CTP', 'type': 'NMOS', 'node1': 'outcoming', 'node2': 'CTN', 'node3': 'incoming', 'node4': 'CTG', 'step':2}]}
print("五管运放为:",fit_cal(tem,source_path))
"""


chrom = {}
for i in range(pop_size):
    chrom[i] = generateChom(4)

fit_val = fit_cal(chrom=chrom, source_path=source_path)  # 计算初始种群的适应度
print("初始种群的适应度",fit_val)
best_chrom = {}
best_chrom_fitval = {}
gen = 0

print("初始种群",chrom)
while(gen<500):
    gen += 1  #第0代为初始化种群，此处从第一代开始
    chrom, chrom_fitval = ga_optimize(fit_val,chrom=chrom,source_path=source_path)  # ga 寻优

    # 精英算法，把上一代的最优个体替换下一代的最差个体
    if (gen > 1):
        chrom[pop_size-1] = best_chrom[gen - 1]
        fit_val[pop_size-1] = best_chrom_fitval[gen - 1]
    #排序
    newChrom = {}
    newFitval = {}
    #排序
    fitval = sorted(chrom_fitval.items(), key=lambda x: x[1], reverse=True)
    for i in range(len(fitval)):
        newFitval[i] = fitval[i][1]
        newChrom[i] = chrom[fitval[i][0]]
    chrom = newChrom
    chrom_fitval = newFitval


    best_chrom[gen], best_chrom_fitval[gen] = chrom[0], chrom_fitval[0]  # 存储当代最优的染色体及其适应度值
    chrom, fit_val = chrom, chrom_fitval  # 新的种群

    #种群被一个个体占领，引入新的个体
    if(fit_val[0] == fit_val[len(fit_val)-1]):
        for i in range(int(pop_size/2)):
            chrom[i] = generateChom(4)

    fit_val = fit_cal(chrom,source_path)

    print('现在是第 ' + str(gen) + ' 代')
    print('fit_val:',fit_val)
    print('best_chrom_fitval',best_chrom_fitval)

    #保存每一代最好最差的结果到一个文件中
    #f = open("E:\hspiceProject\myFiveMos_ee\genInformation\genInformation.txt","a")
    #f.write(str(gen)+"代"+":"+ str(fit_val[0])+ " " + str(fit_val[len(fit_val)-1]) +"\n")
end = time.clock()
print("500代用时：",end-start)