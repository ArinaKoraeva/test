#1) Вычислите общую выручку за июль 2021 по тем сделкам, приход денежных
# средств которых не просрочен.

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
data = pd.read_excel("data.xlsx")
data = data.drop("Unnamed: 5", axis=1)
data['receiving_date'] = pd.to_datetime(data['receiving_date'], format='%Y%m%d', errors='coerce')
month = list(filter (lambda x: '2021' in x, data['status']) )
months_idx = list( map (lambda x : data.index[data['status'] == x] ,month))

#Вычислите общую выручку за июль 2021 по тем сделкам, приход денежных средств которых не просрочен.
def revenue_july (data):
    revenue = round(data.loc[(data['status'] != 'ПРОСРОЧЕНО') & (data.index >= months_idx[2][0] )& (data.index <= months_idx[3][0] ), 'sum'].sum(),2)
    return revenue

#Кто из менеджеров привлек для компании больше всего денежных средств в сентябре 2021?
def top_manager(data):
    data_sept = data.loc[(data.index > months_idx[4][0])& (data.index < months_idx[5][0])]
    sales = data_sept.groupby('sale')['sum'].sum()
    return  sales.idxmax()

#Какой тип сделок (новая/текущая) был преобладающим в октябре 2021?
def type_deal (data):
    data_oct = data.loc[(data.index > months_idx[5][0])]
    count = data_oct['new/current'].value_counts()
    return count.idxmax()

#Сколько оригиналов договора по майским сделкам было получено в июне 2021?
def count_originals_doc(data):
    count_doc = len (data.loc[(data.index < months_idx[1][0])&(data['document'] == 'оригинал')&(data['receiving_date']>='2021-06-01')&(data['receiving_date']<='2021-06-30')])
    return count_doc

#Как изменялась выручка компании за рассматриваемый период? Проиллюстрируйте графиком.
def revenue_month_bar (data):
    h=[]
    for i in range(len(month)) :
        if months_idx[i] == months_idx[len(months_idx)-1]:
            h.append(int(round(data.loc[(data.index > months_idx[i][0]),'sum'].sum(),2)))
        else:
            h.append(int(round(data.loc[(data.index > months_idx[i][0])& (data.index < months_idx[i+1][0]) ,'sum'].sum(),2)))
    df = []
    df.append(month)
    df.append(h)
    df = pd.DataFrame(df).transpose()
    df.columns =['month', 'sum']
    plt.bar(df['month'], df['sum']* 1e-1)
    plt.title('Выручка компании за рассматриваемый период')
    plt.xlabel('Месяц')
    plt.ylabel('Выручка')
    plt.show()   
#Oстаток каждого из менеджеров на 01.07.2021.
def calulate_bonus(row):
    if row['new/current'] == 'новая':
            return row['sum'] * 0.07
    else:
        if row['sum'] > 10000:
            return row['sum'] * 0.05
        else:
            return row['sum'] * 0.03
def balance_manager(data):
    data_filtered = data.loc[(data.index< months_idx[1][0])&(data['document'] == 'оригинал')&(data['receiving_date']>='2021-06-01')&(data['receiving_date']<='2021-06-30')&(data['status'] != 'ПРОСРОЧЕНО')].copy()
    data_filtered['bonus'] = data_filtered.apply(calulate_bonus, axis=1)
    data_filtered = data_filtered.groupby('sale')['bonus'].sum().reset_index()
    return data_filtered
print(f'Общая выручка за Июль: {revenue_july (data)} рублей')
print (f'Лучший менеджер за сентябрь : {top_manager(data)}')
print (f'Тип сделок "{type_deal (data)}" был преобладающим в октябре')  
print(f'Количество оригиналов договоров по майским сделкам, полученных в июне: {count_originals_doc(data)} штук ')
print(f'Остаток бонусов на 01.07.2021: \n{balance_manager(data)}')
print(revenue_month_bar (data))




    
