# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from collections import Counter
from pandas import DataFrame, Series
item_all = pd.read_csv('/Users/IkkiTanaka/Documents/zozo_analysis/ST_03_ITEM.csv',encoding='Shift_JIS')
log_all = pd.read_csv('/Users/IkkiTanaka/Documents/zozo_analysis/log_season7.csv',encoding='Shift_JIS')
prod_all = pd.read_csv('/Users/IkkiTanaka/Documents/zozo_analysis/ST_01_RECOMMEND/ST_01_RECOMMEND.csv',encoding='Shift_JIS')

log_all_sort = log_all.sort_index(by=[u'グループID',u'閲覧日時'], ascending=[True,True])

cnt_all=Counter()
for session in log_all_sort[u'商品ID']:
    cnt_all[session]+= 1
Top_100 = cnt_all.most_common(100)
Top_100 = DataFrame(Top_100)
Top_100.columns = [u'商品ID',u'閲覧数'] 

kounyu_all=DataFrame()
for i in xrange(1,96):
    log_part = log_all_sort[log_all_sort[u'グループID']==i]
    cnt=Counter()
    for session in log_part[u'商品ID']:
        cnt[session]+= 1

    top_100 = cnt.most_common(len(cnt))
    top_100 = DataFrame(top_100)
    top_100.columns = [u'商品ID',u'閲覧数']
    
    TTTT = top_100.isin(prod_all[u'商品ID'].values.tolist())[u'商品ID']
    kounyu = DataFrame(top_100)[TTTT][0:100][u'商品ID']
    if len(kounyu)<100:
        for j in xrange(100):
            kounyu = kounyu.append(Top_100[j:(j+1)][u'商品ID'])
            if len(kounyu)==100:
                break
    kounyu = DataFrame(kounyu)
    kounyu_all = kounyu_all.append(kounyu)

for i in kounyu_all[u'商品ID']:
    cnt[i]+=1
ALL_top = cnt.most_common(len(cnt))
ALL_top = DataFrame(ALL_top)
ALL_top.columns = [u'商品ID',u'閲覧数']

"""
ここまでlog_season7
ここからlog_season9
"""
log_all = pd.read_csv('/Users/IkkiTanaka/Documents/zozo_analysis/log_season9.csv',encoding='Shift_JIS')
log_all_sort = log_all.sort_index(by=[u'グループID',u'閲覧日時'], ascending=[True,True])


kounyu_all=DataFrame()
for i in xrange(1,96):
    log_part = log_all_sort[log_all_sort[u'グループID']==i]
    cnt=Counter()
    for session in log_part[u'商品ID']:
        cnt[session]+= 1

    top_100 = cnt.most_common(len(cnt))
    top_100 = DataFrame(top_100)
    top_100.columns = [u'商品ID',u'閲覧数']
    
    TTTT = top_100.isin(prod_all[u'商品ID'].values.tolist())[u'商品ID']
    kounyu = DataFrame(top_100)[TTTT][0:60][u'商品ID']
    if len(kounyu)<100:
        for j in xrange(len(ALL_top)):
            kounyu = kounyu.append(ALL_top[j:(j+1)][u'商品ID'])
            kounyu = kounyu.drop_duplicates()
            if len(kounyu)==100:
                break
    kounyu = DataFrame(kounyu)
    kounyu_all = kounyu_all.append(kounyu)

kounyu_all.to_csv('/Users/IkkiTanaka/Documents/zozo_analysis/programming_folder/kekka.csv', sep=',')



