def imports():
    """import numpy as np
from scipy.stats import *
import pandas as pd
import matplotlib.pyplot as plt"""


def num11():
    """data_old = 'Thr; Thr; NA; Thr; Two; NA; Five; One; Four; One; Thr; Thr; One; Thr; Five; Thr; One; One; NA; Five; Five; Thr; NA; Two; Five; NA; Thr; Thr; One; Two; Thr; Four; Thr; NA; Thr; One; Two; Four; Five; Thr; Two; Thr; Thr; Four; Two; One; One; Four; Two; Five; One; Thr; One; NA; Thr; Thr; One; Two; NA; Thr; Five; Five; One; Four; Two; Five; Thr; Two; NA; Thr; Two; Four; One; One; Thr; Thr; Thr; One; Two; Thr; Two; Thr; NA; Five; Two; Two; Thr; Thr; Thr; Four; Five; Thr; Five; Thr; One; Thr; Thr; Thr; Two; Thr; Thr; Thr; Thr; One; Thr; Five; Thr; One; Two; One; Four; NA; Thr; One; Five; Four; Five; Two; Five; Five; Two; Thr; One; NA; Thr; Two; Two; Two; Thr; Two; One; Two; NA; Thr; Five; Two; Five; NA; Four; One; Five; Two; Thr; One; Five; Four; Two; Five; Two; Thr; One; Thr; NA; Two; Five; Four; Thr; NA; Two; Thr; One; Two; Four; Two; Thr; Five; Four; One; Two; One; Thr; Five; Five; NA; One; One; Thr; Two; Thr; Four; Two; Thr; Thr; Four; Two; One; Thr; One; Two; One; One; Five; Four; Two; Thr; Thr; Five; Two; Five; Five; Two; Two; Thr; NA; Five; Two; Five; Thr; Four; Two; One; One; Thr; Thr; Four; Thr; Four; One; One; Four; Two; NA; NA; Two; Five; One; One; Five; One; Thr; Five; Thr; Thr; Two; One; Thr; Five; Two; Two; NA; Thr; One; Five; Thr; Thr; Two; One; Four; Thr; Thr; Two; Thr; One; Thr; Thr; Thr; One; Two; Thr; One; Thr; Thr; NA; Thr; Five; Thr; Two; Thr; Thr; Thr; Thr; One; Two; One; Two; One; One; Five; One; Two; One; Thr; One; Two; Five; Thr; One; Two; One; Five; One; One; One; Four; Thr; Two; Thr; Thr; Thr; One; One; One; Two; Thr; NA; Thr; Five; Two; One; Five; Two; One; One; Thr; Five; One; One; Thr; Thr; Four'

data = data_old.replace('NA; ', '').split('; ')

num_unique_answers = len(set(data))
print(f"1. Введите количество различных вариантов ответов респондентов, встречающиеся в очищенной выборке {num_unique_answers}")"""


def num12():
    """n_clean = len(data)
print(f'2. Введите объем очищенной от "NA" выборки {n_clean}')"""

def num13():
    """print(f'3. Введите количество пропущенных данных "NA" в исходной выборке {data_old.count("NA")}')"""

def num14():
    """proportion_f = data.count("Four") / len(data)
print(f'4. Введите долю респондентов, которые дали ответ "Four" {proportion_f})')"""

def num15():
    """z_90 = 1.645  # Z-значение для 90%-го доверительного интервала
# z_95 = 1.96
# z_99 = 2.576
error_margin = z_90 * np.sqrt(proportion_f * (1 - proportion_f) / n_clean)
upper_bound = proportion_f + error_margin
print("5. Правая граница 90%-го доверительного интервала для доли 'F':", upper_bound)"""

def num16():
    """lower_bound = proportion_f - error_margin
print("6. Левая граница 90%-го доверительного интервала для доли 'F':", lower_bound)"""

def num17():
    """chi_critical = chi2.ppf(0.95, df) # На уровне значимости 0.05
print("7. Критическое значение статистики хи-квадрат:", chi_critical)"""

def num18():
    """df = num_unique_answers - 1
print("8. Количество степеней свободы:", df)"""

def num19():
    """observed_counts = pd.Series(data).value_counts().values
expected_counts = [n_clean / num_unique_answers] * num_unique_answers
chi_squared = sum((observed_counts - expected_counts) ** 2 / expected_counts)
print("9. Наблюдаемое значение хи-квадрат:", chi_squared)"""

def num110():
    """reject_hypothesis = int(chi_squared > chi_critical)
print("10. Отвергается ли гипотеза о равновероятном распределении? (1 - да, 0 - нет):", reject_hypothesis)"""

def num111():
    """# 11 - гистограмма

plt.figure(figsize=(10, 6))
pd.Series(data).value_counts().plot(kind='bar', color='skyblue', edgecolor='black')
plt.title("Гистограмма для очищенной выборки", fontsize=16)
plt.xlabel("Ответы", fontsize=12)
plt.ylabel("Частота", fontsize=12)
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()"""

def num2():
    """data = '(-159.8, NA); (-196.4, 168); (-152.7, 165.6); (-186.8, 184.3); (-204.2, 171.8); (-155.2, 209); (-158.4, 161.9); (-173.3, 191.7); (-215.5, NA); (-171.4, 176.7); (-186.2, 156.7); (-195.9, 190.2); (-169, 152); (-144.2, 199.4); (-170.2, 170.4); (-154.6, NA); (-184, 115.9); (-166.9, 195.8); (NA, 134.9); (-205.3, 166.4); (-202, 211); (-198.6, 157.4); (-166.4, 183.4); (-135.6, 227.4); (-191.3, 132.5); (NA, 173.5); (-198.6, 250.9); (-223.3, 199.4); (-221.2, 207.7); (-214.2, NA); (-194.4, 192.6); (-148.3, 191.3); (-173.5, 212.8); (-197.9, 237.1); (-205.2, 183.9); (-191.4, 180.2); (-149.9, 191.1); (-151.6, 167.8); (-214.2, 216); (NA, 230); (-174, NA); (-165.2, 184.7); (-206.8, 151.4); (-184.4, 160.8); (-128.5, 172.3); (NA, 174.2); (-167.7, 199.1); (-217, 153.4); (-194.6, 170); (-171.8, 135.2); (-212.3, 153.5); (-192.6, 175.3); (-218.8, 163.9); (-155.5, NA); (-223.4, 183); (-180.5, 188.5); (-160.3, 166); (-132.2, 124.5); (-214, 177); (-179.4, 230.6); (-207.3, 182.5); (-204.6, 152.5); (-179.7, 146); (-161.7, 207.3); (-169.8, 172.4); (NA, 202.4); (NA, 212.3); (-194.2, 177.2); (-152.6, 164.3); (-213.6, 177.9); (-207.9, 269.6); (NA, 171.3); (-136.1, NA); (-217.9, 194.7); (-221, 203); (-186.8, 173.3); (-178.1, 133.3); (NA, 112.3); (NA, 253.4); (-185, 188.4); (-169, 181.9); (-202.9, 203); (-183.4, 191.2); (-195.8, 186.1); (-220.8, 158.9); (-195.8, 220.9); (NA, 165.7); (-234.7, 158); (-189.7, 240.6); (-186.8, 155.2); (-144.7, 217.1); (-200.7, 170.7); (-223, NA); (-232.2, 146.6); (-198.4, 169.5); (NA, 188.8); (-111.9, 142.8); (-169.8, 207.9); (-228.1, 162.4); (-207.1, 215.3); (-228.9, 217.1); (-167.3, 197.7); (-181.4, 146.1); (-164.9, 201.1); (-213.2, 211.8); (-170, 228); (NA, 230); (-180.2, 142.6); (-186.1, 201.6); (-221.9, 201.4); (-168.8, 197.4); (NA, 159.6); (-213.6, 154.1); (-179, 240.3); (-206.8, 148.4); (NA, 172.5); (-213.1, 180.1); (-173.4, 179.4); (-164.5, 258.5); (-210.8, 110.9); (-206.3, 198.3); (-199.8, 183.5); (-226.5, 175.8); (-207.4, 172.5); (-185.1, 152.6); (-166.9, 189.5); (-239.5, 159.8); (-180.2, 177.9); (-189.2, 196.2); (-159.4, 183.7); (NA, 141.4); (-209.9, 146.9); (-161.9, NA); (-169.7, 204.7); (NA, 167.2); (-204.2, 192.8); (-204.2, 168.7); (-191.1, 167.8); (NA, 174.4); (-161.4, 171.3); (-149.7, 182.9); (-223.1, NA); (NA, 159.8); (NA, 231.9); (-222.1, 182.9); (-193.6, 241.5); (-211.7, 198.5); (-144.7, 142.4); (-171.4, 191.7); (-182.8, 216.4)'.replace('NA', 'None').split('; ')

data = [eval(i) for i in data]

df = pd.DataFrame(data, columns=["Firm1", "Firm2"])

df_clean = df.dropna()

correlation, _ = pearsonr(df_clean["Firm1"], df_clean["Firm2"])
print("1. Коэффициент корреляции Пирсона между X и Y:", correlation)"""

def num21():
    """t_stat, p_value = ttest_ind(df_clean["Firm1"], df_clean["Firm2"], alternative='less') # или equal_var=False вместо параметра alternative='less'
print("2.1. P-value для проверки гипотезы о равенстве средних:", p_value)"""

def num22():
    """reject_mean_null = 1 if p_value < 0.1 else 0 # уровень значимости 0.1
print("2.2. Можно ли утверждать, что среднее значение больше у второй фирмы? (0 - нет, 1 - да):", reject_mean_null)"""

def num31():
    """var1 = np.var(df_clean["Firm1"], ddof=1)
var2 = np.var(df_clean["Firm2"], ddof=1)
f_stat = var1 / var2
df1 = len(df_clean["Firm1"]) - 1
df2 = len(df_clean["Firm2"]) - 1
p_value_variance = 1 - f.cdf(f_stat, df1, df2)
print("3.1. P-value для проверки гипотезы о равенстве дисперсий:", p_value_variance)"""

def num32():
    """reject_variance_null = 1 if p_value_variance < 0.05 else 0 # уровень значимости 0.05
print("3.2. Можно ли утверждать, что дисперсии показателей фирм различны? (0 - нет, 1 - да):", reject_variance_null)"""