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
