import matplotlib.pyplot as plt
import pandas as pd

# Создаем данные
lst1 = [1, 2, 3, 4, 5]
lst2 = ['2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04', '2022-01-05']

# Преобразуем список дат в формат datetime
dates = pd.to_datetime(lst2)

# Строим график
plt.plot(dates, lst1, marker='o')
plt.xlabel('Дата')
plt.ylabel('Числа')
plt.title('График чисел от времени')
plt.show()