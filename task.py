""""
Apriori算法实现
windows  python3.6
github:https://github.com/ZZLLY/DataMining3
参考资料：https://www.cnblogs.com/llhthinker/p/6719779.html
步骤:
1、k=1时扫描D,k>1时根据Lk-1,求Ck
2、在Ck集合里,根据最小支持度,求Lk(使用先验性质可优化速度)
3、重复上述步骤,直至找出所有Lk,合并
4、根据最小置信度，得出强规则
tips:k=1,2,3...n(n为项集中的项的最大项数)
"""


def load_data():
    # 根据word文档,项目集I={ I1，I2，I3，I4，I5，I6}
    data = [['I1', 'I2', 'I3'], ['I1', 'I4', 'I5'], ['I1', 'I3', 'I6'],
            ['I4', 'I5', 'I6'], ['I2', 'I3', 'I6'], ['I1', 'I3', 'I4', 'I5'],
            ['I3', 'I4', 'I5'], ['I2', 'I3'], ['I1', 'I3', 'I4', 'I5'], ['I2', 'I6']]
    return data


def is_apriori(Ck_item, last_Lk):
    # 先验性质：任何非频繁的（k-1）项集都不是频繁k项集的子集
    for item in Ck_item:
        sub_Ck = Ck_item - frozenset([item])
        if sub_Ck not in last_Lk:
            return False
    return True


def create_C1(data):
    # 把单个项放入集合，去重
    C1 = set()
    for t in data:
        for item in t:
            item_set = frozenset([item])
            C1.add(item_set)
    return C1


def create_Ck(last_Lk, k):
    # 获得候选项集
    Ck = set()
    list_last_Lk = list(last_Lk)
    # k-1项集中，两两组合取并集，变成k项集
    for i in range(len(last_Lk)):
        for j in range(i+1, len(last_Lk)):
            l1 = list(list_last_Lk[i])
            l2 = list(list_last_Lk[j])
            l1.sort()
            l2.sort()
            # 两个项集有且只有1个项不同，取并集，不然不是k项集
            # 如[I1,I2,I3] + [I2,I3,I4] => [I1,I2,I3,I4]   3项集=>4项集
            #   [I1,I2,I3] + [I2,I4,I5] => [I1,I2,I3,I4,I5]  3项集=>5项集
            if l1[0:k - 2] == l2[0:k - 2]:
                # 取并集
                tmp = list_last_Lk[i] | list_last_Lk[j]
                # 根据先验性质
                if is_apriori(tmp, last_Lk):
                    Ck.add(tmp)
    return Ck


def get_Lk(data, Ck, min_support, support_data):
    Lk = set()
    # 支持度计数
    item_count = {}
    for t in data:
        for item in Ck:
            if item.issubset(t):
                if item not in item_count:
                    # 如果该项首次出现，加入并计数1
                    item_count[item] = 1
                else:
                    item_count[item] += 1
    # 根据最小支持度,筛选加入Lk,并记录支持度
    for item in item_count:
        if item_count[item] >= min_support:
            Lk.add(item)
            support_data[item] = item_count[item]
    return Lk


def get_big_rules(L, support_data, min_conf):
    big_rule_list = []
    sub_set_list = []
    # 根据最小置信度，得出强规则
    # 如 freq_set = [I1,I2,I3]   sub_set = [I1]
    #    conf = sup([I1,I2,I3]) - sup([freq_set - sub_set])
    #  即conf = sup([I1,I2,I3]) - sup([I2,I3])
    for i in range(len(L)):
        for freq_set in L[i]:
            for sub_set in sub_set_list:
                if sub_set.issubset(freq_set):
                    conf = support_data[freq_set] / support_data[freq_set - sub_set]
                    big_rule = (freq_set - sub_set, sub_set, conf)
                    if conf >= min_conf and big_rule not in big_rule_list:
                        big_rule_list.append(big_rule)
            sub_set_list.append(freq_set)
    return big_rule_list


if __name__ == '__main__':
    # 设定最小支持度和最小置信度
    min_support = 3
    min_conf = 0.7
    # 存放所有的Lk
    L = []
    # 存放满足最小支持度的项集及其支持度
    support_data = {}
    # 读取数据
    data = load_data()
    # 项集中的项的最大项数
    n = 0
    for item in data:
        if n < len(item):
            n = len(item)
    # C1需要单独处理
    C1 = create_C1(data)
    L1 = get_Lk(data, C1, min_support, support_data)
    # 集合
    last_Lk = L1.copy()
    L.append(L1)
    # k=2...n 可以循环处理
    for i in range(2, n+1):
        Ci = create_Ck(last_Lk, i)
        Li = get_Lk(data, Ci, min_support, support_data)
        last_Lk = Li.copy()
        L.append(Li)
    # 根据最小置信度获得big_rules
    big_rules = get_big_rules(L, support_data, min_conf)
    # 结果展示
    for Lk in L:
        if Lk:
            print("="*50)
            print("frequent " + str(len(list(Lk)[0])) + "-itemsets\t\tsupport")
            print("="*50)
            for freq_set in Lk:
                print(freq_set, '\t', support_data[freq_set])
    print("=" * 50)
    print("\nBig Rules:")
    for item in big_rules:
        print(item[0], "=>", item[1], "conf: ", item[2])
