

import time

#自动获取当前时间的方法
def get_current_time():
    '''此方法返回以字符串形式的当前时间(格式为：yy-mm-dd hh:mm:ss)'''

    #初始化字符串时间
    st_crr_time = " "
    #获取当前本地时间
    cur_time = time.localtime()
    #拼接时间
    st_crr_time = str(cur_time[0])+"-"+str(cur_time[1])+"-"+str(cur_time[2])\
                +" "+str(cur_time[3])+":"+str(cur_time[4])+":"+str(cur_time[5])
    return st_crr_time

#计算时间差的方法
def sub_time_diff(start,end):
    ''' 此方法传入两个参数(都为字符串类型)，start为开始时间，end为结束时间，
    　　返回这两个时间的时间差（以天为单位，不足一天按一天算）'''
    #分割字符串得到时间的年月日
    start_time_arr = start.split(" ")
    start_time = start_time_arr[0].split("-")

    end_time_arr = end.split(" ")
    end_time = end_time_arr[0].split("-")

    #将得到的年月日放入元组中
    start_time_tuple = (int(start_time[0]),int(start_time[1]),int(start_time[2]),0,0,0,0,0,0)
    end_time_tuple = (int(end_time[0]),int(end_time[1]),int(end_time[2]),0,0,0,0,0,0)

    #将时间元组转换为新纪元秒数时间
    start_sec = time.mktime(start_time_tuple)
    end_sec = time.mktime(end_time_tuple)

    #用得到的新纪元秒数除以3600计算天数
    days = (end_sec - start_sec)//3600//24

    return int(days)