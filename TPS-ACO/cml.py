# # -*- coding: utf-8 -*-
# import random
# import copy
# import sys
# from cnc import CNC
# import itertools
# import multiprocessing as mp
#
# # 参数
# (ALPHA, BETA, RHO, Q) = (1.0, 2.0, 0.5, 100.0)
# # 城市数，蚁群
# (city_num, ant_num) = (8, 50)
# MAXLEN = 64
#
# distance_x = [
#     100, 100, 200, 200, 300, 300, 400, 400
# ]
#
# distance_y = [
#     100, 200, 100, 200, 100, 200, 100, 200
# ]
#
# # 城市距离和信息素
# distance_graph = [[0.0 for col in range(city_num)] for raw in range(city_num)]
#
# time_exchange = [28, 31]
# time_process_single = 560
# time_process = [400, 378]
# time_clean = 25
# time_move = [0, 20, 33, 46]
# index_map = [
#     0, 0, 1, 1, 2, 2, 3, 3, 4, 4
# ]
#
# pheromone_graph = [[1.0 for col in range(city_num)] for raw in range(city_num)]
#
#
# # ----------- 蚂蚁 -----------
# class Ant(object):
#     # 初始化
#     def __init__(self, ID):
#
#         self.ID = ID  # ID
#
#     def set_cnc_first(self, cnc1):
#         self.__cnc_first = cnc1
#         # print "cnc1:", self.__cnc_first
#         self.__cnc_second = list(set([i for i in range(0, 8)]) - set(self.__cnc_first))
#         # print "cnc2:", self.__cnc_second
#         self.__clean_data()  # 随机初始化出生点
#
#     def get_first_process_num(self):
#         return self.__cnc_first
#
#     # 初始数据
#     def __clean_data(self):
#
#         self.path = []  # 当前蚂蚁的路径
#
#         self.total_distance = 0.0  # 当前路径的总距离
#         self.move_count = 0  # 移动次数
#         self.current_city = -1  # 当前停留的城市
#         # self.open_table_city = [True for i in xrange(city_num)]  # 探索城市的状态
#
#         city_index = random.randint(0, 1)  # 随机初始出生点 因为rgv是固定0或1位置出发]
#         self.current_city = city_index
#         self.path.append(city_index)
#         # self.open_table_city[city_index] = False
#         self.move_count = 1
#
#         self.available_cnc = [i for i in range(0, 8)]
#
#         self.clock = 0
#
#         self.cncs = []
#
#         self.has_first = False
#
#         for i in range(0, 8):
#             if i in self.__cnc_first:
#                 self.cncs.append(CNC(time_process_single, time_process[0]))
#             else:
#                 self.cncs.append(CNC(time_process_single, time_process[1]))
#
#     # 选择下一个城市
#     def __choice_next_city(self):
#         self.has_first = True
#
#         next_city = -1
#         select_citys_prob = [0.0 for i in range(city_num)]
#         total_prob = 0.0
#
#         # 获取去下一个城市的概率
#         # 第一遍的时候，还不能直接进行二部图寻路
#         choose = []
#         if self.current_city in self.__cnc_first and not self.cncs[
#             self.current_city].has_production():
#             self.has_first = False
#
#
#
#         if self.has_first:
#             for i in self.available_cnc:
#                 if not (self.current_city in self.__cnc_first and i in self.__cnc_first) and not (
#                         self.current_city in self.__cnc_second and i in self.__cnc_second):
#                     try:
#                         # 计算概率：与信息素浓度成正比，与距离成反比
#                         select_citys_prob[i] = pow(pheromone_graph[self.current_city][i], ALPHA) * pow(
#                             (1.0 / distance_graph[self.current_city][i]), BETA)
#                         total_prob += select_citys_prob[i]
#                         choose.append(i)
#                     except ZeroDivisionError:
#                         print('Ant ID: {ID}, current city: {current}, target city: {target}'.format(ID=self.ID,
#                                                                                                     current=self.current_city,
#                                                                                                     target=i))
#                         sys.exit(1)
#         else:
#             for i in self.available_cnc:
#                 if i in self.__cnc_first:
#                     try:
#                         # 计算概率：与信息素浓度成正比，与距离成反比
#                         select_citys_prob[i] = pow(pheromone_graph[self.current_city][i], ALPHA) * pow(
#                             (1.0 / distance_graph[self.current_city][i]), BETA)
#                         total_prob += select_citys_prob[i]
#                         choose.append(i)
#                     except ZeroDivisionError:
#                         print('Ant ID: {ID}, current city: {current}, target city: {target}'.format(ID=self.ID,
#                                                                                                     current=self.current_city,
#                                                                                                     target=i))
#                         sys.exit(1)
#
#         # if len(choose) > 1:
#         #     print("here")
#
#         # 轮盘选择城市
#         if total_prob > 0.0:
#             # 产生一个随机概率
#             temp_prob = random.uniform(0.0, total_prob)
#             # for i in self.available_cnc:
#             for i in choose:
#                     # 轮次相减
#                 temp_prob -= select_citys_prob[i]
#                 if temp_prob < 0.0:
#                     next_city = i
#                     break
#
#         # 未从概率产生，顺序选择一个未访问城市
#         if next_city == -1 and len(choose) != 0:
#             # for i in self.available_cnc:
#             #     if not (self.current_city in self.__cnc_first and i in self.__cnc_first) and not (
#             #             self.current_city in self.__cnc_second and i in self.__cnc_second):
#             #         next_city = i
#             #         break
#             next_city = choose[0]
#
#         # 返回下一个城市序号 可能会出现-1的情况，因为工序问题，即使空着也不是应有的工序
#         return next_city
#
#     # 计算路径总距离
#     def __cal_total_distance(self):
#
#         temp_distance = 0.0
#
#         for i in range(1, len(self.path)):
#             start, end = self.path[i-1], self.path[i]
#             temp_distance += distance_graph[start][end]
#
#         # 回路
#         start = end
#         end = self.path[0]
#         # 9.15.7:00
#         if len(self.available_cnc) == 0:
#             self.total_distance += self.get_extra_time()
#
#         temp_distance += distance_graph[start][end]
#         self.total_distance = temp_distance
#
#     # 移动操作
#     def __move(self, next_city):
#         ans = distance_graph[self.current_city][next_city]
#         self.path.append(next_city)
#         # self.open_table_city[next_city] = False
#         self.total_distance += distance_graph[self.current_city][next_city]
#         self.current_city = next_city
#         self.move_count += 1
#
#         return ans
#
#     def get_extra_time(self):
#         my_min = 100000
#         # 不需要考虑是否是由于第一步没有做完导致的next=-1，因为即使是相同型号的，也会在下一次判断中next=-1成立，从而再一次进行本函数，直到找到合适的
#         for i in self.cncs:
#             if not i.is_available(self.clock):
#                 time = i.get_leaving_time(self.clock)
#                 if my_min > time:
#                     my_min = time
#
#         self.total_distance += my_min
#
#         return my_min
#
#     def __update_cnc(self):
#         self.available_cnc = []
#         for i in range(0, 8):
#             if self.cncs[i].is_available(self.clock):
#                 self.available_cnc.append(i)
#
#     # 搜索路径
#     def search_path(self):
#
#         # 初始化数据
#         self.__clean_data()
#
#         # 搜素路径，遍历完所有城市为止
#
#         # update
#         self.clock += time_exchange[self.current_city % 2]
#         self.cncs[self.current_city].process(self.clock)
#         self.__update_cnc()
#
#
#         # len(self.available_cnc) != 0 and
#         while  len(self.path) < MAXLEN:
#             # 移动到下一个城市
#             next_city = self.__choice_next_city()
#             if next_city == -1:
#                 self.clock += self.get_extra_time()
#
#             else:
#                 self.clock += self.__move(next_city)
#                 if next_city in self.__cnc_second:
#                     self.cncs[next_city].process(self.clock - time_clean)
#                 else:
#                     self.cncs[next_city].process(self.clock)
#
#             self.__update_cnc()
#             # print "path: ", self.path
#             # 判断是不是重复的循环
#             if len(self.path) == 16:
#                 flag = True
#                 for i in range(0, 8):
#                     if self.path[i] != self.path[i + 8]:
#                         flag = False
#
#                 if flag:
#                     while len(self.path) > 8:
#                         self.path.pop()
#                     break
#         # if len(self.available_cnc) == 0:
#
#         # 计算路径总长度
#         self.__cal_total_distance()
#         # self.total_distance += self.path[]
#
#         # modify
#         self.total_distance += time_exchange[self.path[0]%2]
#
#
# # ----------- TSP问题 -----------
#
# class TSP(object):
#     def __init__(self, cnc1=[0, 2, 4, 6], n=city_num):
#         # 城市数目初始化为city_num
#         self.n = n
#
#         self.new(cnc1)
#
#         # 计算城市之间的距离
#         # for i in xrange(city_num):
#         #     for j in xrange(city_num):
#         #         temp_distance = pow((distance_x[i] - distance_x[j]), 2) + pow((distance_y[i] - distance_y[j]), 2)
#         #         temp_distance = pow(temp_distance, 0.5)
#         #         distance_graph[i][j] = float(int(temp_distance + 0.5))
#         for i in range(city_num):
#             for j in range(city_num):
#                 distance_graph[i][j] = time_move[abs(index_map[i] - index_map[j])]
#                 if j % 2 == 0:
#                     distance_graph[i][j] += time_exchange[0]
#                 else:
#                     distance_graph[i][j] += time_exchange[1]
#
#                     # distance_graph_bak = copy(distance_graph)
#
#     # 初始化
#     def new(self, cnc1):
#         self.nodes = []  # 节点坐标
#
#         # 初始化城市节点
#         for i in range(len(distance_x)):
#             # 在画布上随机初始坐标
#             x = distance_x[i]
#             y = distance_y[i]
#             self.nodes.append((x, y))
#
#         # 顺序连接城市
#         # self.line(range(city_num))
#
#         # 初始城市之间的距离和信息素
#         for i in range(city_num):
#             for j in range(city_num):
#                 pheromone_graph[i][j] = 1.0
#
#         self.ants = [Ant(ID) for ID in range(ant_num)]  # 初始蚁群
#
#         # 加入洗料时间
#         cnc2 = list(set([i for i in range(0, 8)]) - set(cnc1))
#         for i in cnc2:
#             for j in range(city_num):
#                 if i != j:
#                     distance_graph[j][i] += time_clean
#         # 分组设置
#         for i in self.ants:
#             i.set_cnc_first(cnc1)
#
#         self.best_ant = Ant(-1)  # 初始最优解
#         self.best_ant.total_distance = 1 << 31  # 初始最大距离
#         self.iter = 1  # 初始化迭代次数
#
#     # 开始搜索
#     def search_path(self, count=1000):
#         while self.iter < count:
#             # 遍历每一只蚂蚁
#             for ant in self.ants:
#                 # 搜索一条路径
#                 ant.search_path()
#                 # 与当前最优蚂蚁比较
#                 if ant.total_distance < self.best_ant.total_distance:
#                     # 更新最优解
#                     self.best_ant = copy.deepcopy(ant)
#             # 更新信息素
#             self.__update_pheromone_gragh()
#             print(u"迭代次数：", self.iter, u"最佳路径总距离：", float(self.best_ant.total_distance), "路径顺序： ", self.best_ant.path,
#                   "原始分数：", self.best_ant.total_distance * self.best_ant.clock, "总共时间：", self.best_ant.clock)
#             self.iter += 1
#
#         return self.best_ant
#
#     # 更新信息素
#     def __update_pheromone_gragh(self):
#
#         # 获取每只蚂蚁在其路径上留下的信息素
#         temp_pheromone = [[0.0 for col in range(city_num)] for raw in range(city_num)]
#         for ant in self.ants:
#             for i in range(1, city_num):
#                 start, end = ant.path[i - 1], ant.path[i]
#                 # 在路径上的每两个相邻城市间留下信息素，与路径总距离反比
#                 temp_pheromone[start][end] += Q / ant.total_distance
#                 temp_pheromone[end][start] = temp_pheromone[start][end]
#
#         # 更新所有城市之间的信息素，旧信息素衰减加上新迭代信息素
#         for i in range(city_num):
#             for j in range(city_num):
#                 pheromone_graph[i][j] = pheromone_graph[i][j] * RHO + temp_pheromone[i][j]
#
#
# # -----------多进程-----------
#
# def multitask(cnc1_num, count=1000):
#     ants = []
#     for i in itertools.combinations([i for i in range(8)], cnc1_num):
#         ants.append(TSP(list(i)))
#     pool = mp.Pool(len(ants))
#     jobs = [pool.apply_async(ant.search_path, args=(count,)) for ant in ants]
#     results = [j.get() for j in jobs]
#     # contents = []
#
#     my_min = results[0].total_distance
#     for i in results:
#         print(i.total_distance)
#         if i.total_distance < my_min:
#             my_min = i.total_distance
#             ans = i
#
#     print(u"选择第一道工序的编号：", ans.get_first_process_num(), u"最佳路径总距离：", float(ans.total_distance), "路径顺序： ", ans.path,
#               "原始分数：", ans.total_distance * ans.clock, "总共时间：", ans.clock)
#
#
#
#
# # ----------- 程序的入口处 -----------
#
# if __name__ == '__main__':
#     print(u"""
# --------------------------------------------------------
#     程序：蚁群算法解决TPS问题程序
#     作者：syd
#     日期：2015-12-10
#     语言：Python 3,5+
# --------------------------------------------------------
#     """)
#     test = TSP()
#     ant = test.search_path()
#     print(ant.total_distance)
#     # multitask(4, 50)
