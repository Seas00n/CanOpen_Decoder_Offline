import pandas as pd
from pandas import DataFrame
import datetime
import numpy as np
import matplotlib.pyplot as plt


# file_path = "c5.xltx"
# sheet_name = "c5"
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
# np.save("c5_id.npy", id_array)
# np.save("c5_len.npy", len_array)
# np.save("c5_data.npy", data_array)
# np.save("c5_time.npy", time_array)


def twosComplement_hex(hexval, bits):
    unsigned_int = int(hexval, 16)
    if bits == 32:
        signed_int = unsigned_int if unsigned_int < 0x80000000 else unsigned_int - 0x100000000
    elif bits == 16:
        signed_int = unsigned_int - 0x10000 if unsigned_int & 0x8000 else unsigned_int
    else:
        signed_int = unsigned_int
    return signed_int


time_array = np.load("c5_time.npy", allow_pickle=True)
id_array = np.load("c5_id.npy", allow_pickle=True)
data_array = np.load("c5_data.npy", allow_pickle=True)
len_array = np.load("c5_len.npy", allow_pickle=True)
num_msg = np.size(time_array, 0)
id = "0x7e"
pos_list = []
current_list = []
pos_current_time_list = []
pos_current_idx_list = []
state_word_list = []
vel_list = []
torque_list = []
vel_torque_time_list = []
vel_torque_idx_list = []
current_cmd_list = []
current_cmd_idx_list = []

tpdo_motor1 = "0x01FE"
tpdo_motor2 = "0x02FE"
cmd_sdo = "0x067E"
for i in range(num_msg):
    if id_array[i] == tpdo_motor1:
        str_data = data_array[i]
        len = len_array[i]
        if len < 8:
            continue
        pos_current_idx_list.append(i)
        data_ = str_data.split(" ", len)
        pos_ = data_[3] + data_[2] + data_[1] + data_[0]
        pos_ = twosComplement_hex(pos_, 32)
        pos_ = pos_ / 8192.0 / 50.0 * 360.0
        current_ = data_[7] + data_[6]
        current_ = twosComplement_hex(current_, 16)
        state_ = data_[5] + data_[4]
        state_ = twosComplement_hex(state_, 8)
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
        vel_torque_idx_list.append(i)
        data_ = str_data.split(" ", len)
        vel_ = data_[3] + data_[2] + data_[1] + data_[0]
        vel_ = twosComplement_hex(vel_, 32)
        vel_ = vel_ / 8192.0 / 50.0 * 360.0
        torque_ = data_[7] + data_[6]
        torque_ = twosComplement_hex(torque_, 16)
        state_ = data_[5] + data_[4]
        state_ = twosComplement_hex(state_, 8)
        vel_list.append(vel_)
        torque_list.append(torque_)
        time_ = time_array[i]
        time_ = time_.hour * 3600 + time_.minute * 60 + time_.second + time_.microsecond * 0.001
        vel_torque_time_list.append(time_)
    elif id_array[i] == cmd_sdo:
        str_data = data_array[i]
        len = len_array[i]
        if len < 8:
            continue
        data_ = str_data.split(" ", len)
        if data_[1] == '71' and data_[2] == '60':  # catch current cmd
            current_cmd_ = data_[5] + data_[4]
            current_cmd_ = twosComplement_hex(current_cmd_, 16)
            current_cmd_list.append(current_cmd_)
            current_cmd_idx_list.append(i)

d_array = np.array(state_word_list) * 0.08
d2_array = np.array(current_list)*0.05
d3_array = np.array(current_cmd_list) * 0.05
idx = np.array(pos_current_idx_list)
idx_2 = np.array(pos_current_idx_list)
idx_3 = np.array(current_cmd_idx_list)
plt.plot(idx, d_array, label='stateword')
plt.plot(idx_2, d2_array, label='position')
plt.plot(idx_3, d3_array, label='current_cmd')
plt.legend()
plt.show()
last_state = state_word_list[0]
print('{:016b}'.format(last_state))
for i in range(np.size(d_array,0)):
    if state_word_list[i] != last_state:
        last_state = state_word_list[i]
        print('{:016b}'.format(last_state))
        print(pos_current_idx_list[i])
