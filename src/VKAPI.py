import vk_api
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

vk_session = vk_api.VkApi(token='ad2506acad2506acad2506aceaae1d4a1baad25ad2506acc5b0fb048d178301c389446f')
vk = vk_session.get_api()
posts = vk.wall.get(domain='souffrantmittelalter', count=100)['items']
data = []
for i, post in enumerate(posts[::-1][:99]):
    post_date = datetime.fromtimestamp(post['date'])
    likes = post['likes']['count']
    if i > 0:
        prev_post_date = data[-1][1]
        interval_hour = round(( post_date - prev_post_date ).seconds / 60,0)
    else:
        interval_hour = 0

    data.append([
        post['id'],
        post_date,
        likes,
        post_date.hour,  # Для времени суток
        str(post_date.strftime('%A')),  # День недели
        interval_hour
    ])



df = pd.DataFrame({
    "id": [row[0] for row in data],
    "date": [row[1] for row in data],
    "like": [row[2] for row in data],
    "hour": [row[3] for row in data],
    "week_day": [row[4] for row in data],
    "interval_hour": [row[5] for row in data]
})

bins = [0, 15, 60, 180, 720, 1440, float("inf")]  # в минутах
labels = ['<15м', '15-60м', '1-3ч', '3-12ч', '12-24ч', '>24ч']

df['interval_group'] = pd.cut(
    df['interval_hour'],
    bins=bins,
    labels=labels,
    right=False
)

plt.figure(figsize=(10, 6))
sns.barplot(
    x='interval_group',
    y='like',
    data=df,
    estimator= np.mean ,
    order=labels
)
plt.title('Среднее количество лайков по интервалам между постами')
plt.xlabel('Интервал между постами')
plt.ylabel('Среднее количество лайков')
plt.savefig('plot1.png')

week_labels = [ 'Monday', 'Tuesday' ,'Wednesday' ,'Thursday' ,'Friday' ,'Saturday', 'Sunday']

plt.figure(figsize=(10, 6))
sns.barplot(
    x='week_day',
    y='like',
    data=df,
    estimator= np.mean,
    order=week_labels
)
plt.title('Среднее количество лайков по дням недели')
plt.xlabel('День недели')
plt.ylabel('Среднее количество лайков')
plt.savefig('plot2.png')

plt.figure(figsize=(10, 6))
sns.barplot(
    x='hour',
    y='like',
    data=df,
    estimator= np.mean
)
plt.title('Среднее количество лайков по часам')
plt.xlabel('Час')
plt.ylabel('Среднее количество лайков')
plt.savefig('plot.png')
df.to_csv("Данные вк")