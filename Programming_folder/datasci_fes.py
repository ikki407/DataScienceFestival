# -*- coding: utf-8 -*-
import pandas as pd

item_all = pd.read_csv('/Users/IkkiTanaka/Documents/zozo_analysis/ST_03_ITEM.csv',encoding='Shift_JIS')
log_all = pd.read_csv('/Users/IkkiTanaka/Documents/zozo_analysis/ST_04_LOG.csv',encoding='Shift_JIS')
prod_all = pd.read_csv('/Users/IkkiTanaka/Documents/zozo_analysis/ST_01_RECOMMEND/ST_01_RECOMMEND.csv',encoding='Shift_JIS')

d = log_all[u'閲覧日時']
"""
    LOG_SEASON
"""
M=[i for i in range(0,len(log_all)) if  (pd.to_datetime(d[i]).year==2012 or pd.to_datetime(d[i]).year==2013) and (pd.to_datetime(d[i]).month==4 or pd.to_datetime(d[i]).month==5 or pd.to_datetime(d[i]).month==6 or pd.to_datetime(d[i]).month==7)]

M_list=M[:]
log_season=log_all.ix[M_list]
log_season.to_csv('/Users/IkkiTanaka/Documents/zozo_analysis/LOG_SEASON.csv', sep=',',encoding='shift-JIS')

"""
    log_season7
"""
log_all = pd.read_csv('/Users/IkkiTanaka/Documents/zozo_analysis/LOG_SEASON.csv',encoding='Shift_JIS')
d = log_all[u'閲覧日時']
M=[i for i in range(0,len(log_all)) if pd.to_datetime(d[i]).year==2013 and pd.to_datetime(d[i]).month==4]

M_list=M[:]
log_season=log_all.ix[M_list]
log_season.to_csv('/Users/IkkiTanaka/Documents/zozo_analysis/log_season7.csv', sep=',',encoding='shift-JIS')

"""
    log_season9
"""
log_all = pd.read_csv('/Users/IkkiTanaka/Documents/zozo_analysis/log_season7.csv',encoding='Shift_JIS')
d = log_all[u'閲覧日時']
M=[i for i in range(0,len(log_all)) if pd.to_datetime(d[i]).day in [22,23,24,25,26,27,28,29,30] ]

M_list=M[:]
log_season=log_all.ix[M_list]
log_season.to_csv('/Users/IkkiTanaka/Documents/zozo_analysis/log_season9.csv', sep=',',encoding='shift-JIS')

