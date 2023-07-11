import pandas as pd
from pandas import DataFrame
import datetime
import numpy as np
import matplotlib.pyplot as plt
# file_path = "c1.xltx"
# sheet_name = "c1"
# df = pd.read_excel(file_path, sheet_name=sheet_name)
#
# num_rows = len(df["序号"])
# print(num_rows)
#
# id_list = []
# len_list = []
# data_list = []
# time_list = []
# for i in range(num_rows):
#     time_ = df["系统时间"][i]
#     time_ = datetime.datetime.strptime(time_, "%H:%M:%S.%f")
#     time_list.append(time_)
#     id_list.append(df["ID号"][i])
#     str_len = int(df["长度"][i], 16)
#     len_list.append(str_len)
#     data_ = df["数据"][i]
#     data_ = data_[3:-1]
#     data_list.append(data_)
#     print(i)
# id_array = np.array(id_list)
# len_array = np.array(len_list)
# data_array = np.array(data_list)
# time_array = np.array(time_list)
# np.save("c1_id.npy", id_array)
# np.save("c1_len.npy", len_array)
# np.save("c1_data.npy", data_array)
# np.save("c1_time.npy", time_array)

time_array = np.load("c1_time.npy", allow_pickle=True)
id_array = np.load("c1_id.npy", allow_pickle=True)
data_array = np.load("c1_data.npy", allow_pickle=True)
len_array = np.load("c1_len.npy", allow_pickle=True)
num_msg = np.size(time_array, 0)
id = "0x7e"
pos_list = []
current_list = []
pos_current_time_list = []
state_word_list = []
vel_list = []
torque_list = []
vel_torque_time_list = []

tpdo_motor1 = "0x01FE"
tpdo_motor2 = "0x02FE"
for i in range(num_msg):
    if id_array[i] == tpdo_motor1:
        str_data = data_array[i]
        len = len_array[i]
        if len < 8:
            continue
        data_ = str_data.split(" ", len)
        pos_ = int(data_[0], 16) + int(data_[1], 16) * 256 + int(data_[2], 16) * 65536 + int(data_[3],
                                                                                             16) * 16777216
        pos_ = pos_ / 8192.0 / 50.0 * 360.0
        current_ = int(data_[6], 16) + int(data_[7], 16) * 256
        state_ = int(data_[4], 16) + int(data_[5], 16) * 256
        pos_list.append(pos_)
        current_list.append(current_)
        state_word_list.append(state_)
        time_ = time_array[i]
        time_ = time_.hour * 3600 + time_.minute * 60 + time_.second + time_.microsecond * 0.001
        pos_current_time_list.append(time_)

    elif id_array[i] == tpdo_motor2:
        str_data = data_array[i]
        len = len_array[i]
        if len < 8:
            continue
        data_ = str_data.split(" ", len)
        vel_ = int(data_[0], 16) + int(data_[1], 16) * 256 + int(data_[2], 16) * 65536 + int(data_[3],
                                                                                             16) * 16777216
        vel_ = vel_ / 8192.0 / 50.0 * 360.0
        torque_ = int(data_[6], 16) + int(data_[7], 16) * 256
        state_ = int(data_[4], 16) + int(data_[5], 16) * 256
        vel_list.append(vel_)
        torque_list.append(torque_)
        time_ = time_array[i]
        time_ = time_.hour * 3600 + time_.minute * 60 + time_.second + time_.microsecond * 0.001
        vel_torque_time_list.append(time_)

data_array = np.array(state_word_list)
idx = np.arange(np.size(data_array,0))
plt.plot(idx, data_array)
plt.show()