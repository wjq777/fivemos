import random
import os
import re
import psutil
import sys


pop_size = 30
generation = 500
#1.种群初始化
nodeSet = ["OUT", "IN", "VCC", "0"]

def usingHspiceToGetfit(chrom_val, out_file_name):
    exe_path = r'C:\synopsys\Hspice_C-2009.09\BIN\hspice.exe'  # hspice 软件安装的位置
    var_file_name = 'netlist'  # 参数文件名称，即网表的名称
    in_file_name = 'inv'  # .sp文件名称
    source_path = 'E:\hspiceProject\inverter\disconnected'
    #把染色体的值写进网表文件
    nestlistFile = open(source_path + '\\' + var_file_name, 'w+')  # w+:新建读写，会将文件内容清零;若文件不存在，创建
    nestlistFile.write('.PARAM' + '\n')
    nestlistFile.write('.SUBCKT INV IN OUT VCC 0' + '\n')

    # 写value
    if (chrom_val[0]['type'] == 'PMOS'):
        type = 'PCH'
    if (chrom_val[0]['type'] == 'NMOS'):
        type = 'NCH'
    nestlistFile.write('M1' + ' ' + chrom_val[0]['node1'] + ' ' + chrom_val[0]['node2'] + ' ' + chrom_val[0]['node3'] + ' ' + chrom_val[0][
        'node4'] + ' ' + type + ' ' + 'L=' + str(chrom_val[0]['param1']) + 'U' + ' ' + 'W=' + str(
        chrom_val[0]['param2']) + 'U' + '\n')

    if (chrom_val[1]['type'] == 'PMOS'):
        type = 'PCH'
    if (chrom_val[1]['type'] == 'NMOS'):
        type = 'NCH'
    nestlistFile.write('M2' + ' ' + chrom_val[1]['node1'] + ' ' + chrom_val[1]['node2'] + ' ' + chrom_val[1]['node3'] + ' ' + chrom_val[1][
        'node4'] + ' ' + type + ' ' + 'L=' + str(chrom_val[1]['param1']) + 'U' + ' ' + 'W=' + str(
        chrom_val[1]['param2']) + 'U' + '\n')

    nestlistFile.write('.ENDS' + '\n')
    nestlistFile.close()

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
                print(source_path + out_file_name + '.lis')
                with open(source_path + out_file_name + '.lis', 'r+') as fp:
                    data = fp.read()
                break
            except PermissionError:
                counter1 += 1

    result1 = re.search(r'in\s*out\s*0.\s*0.\s*(.*)\s', data)

    if (result1 == None):
        return 0

    Vout_0v = result1.group(1).strip()

    Vout_0v = float(Vout_0v)
    result2 = re.search(r'\s*2.0000e-10\s*5.000e\+00\s*(.*)\s', data)

    if (result2 == None):
        return 0

    Vout_5v = result2.group(1).strip()
    Vout_5v = (float(Vout_5v))

    #f_val = abs(5.0 - Vout_0v)  + abs(Vout_5v)
    f_val = ((5.0 - Vout_0v) * (5.0 - Vout_0v) + Vout_5v * Vout_5v) ** 0.5+0.003  # 分母
    """
    if (f_val == 0):
        f_val = 2.549e-07  # 可以理解为经验值 取它时就是标准反相器 个体适应度很强 符合实际情况
        f_val = 1 / f_val
        return f_val
    """
    f_val = 1 / f_val

    return pow(f_val,0.1)

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


exe_path = r'C:\synopsys\Hspice_C-2009.09\BIN\hspice.exe'  # hspice 软件安装的位置
var_file_name = 'netlist'  # 参数文件名称，即网表的名称
in_file_name = 'myfivemos'  # .sp文件名称
source_path = r'E:\hspiceProject\myFiveMos_ee'
out_file_name = str('myfivemos')  # 输出的 .lis 文件的名称
proc = psutil.Popen(exe_path + ' -i ' + source_path + '\\' + in_file_name + '.sp' + ' -o ' + source_path + '\\'
                        + out_file_name)




