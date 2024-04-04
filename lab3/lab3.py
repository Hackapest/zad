import pandas as pd
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
import seaborn as sns
from spyre import server
import os


DIR_NAME = "vhi_data_15-03-2024_23-19-19"

def loadFile(file, headers):
    pid = int(file.split('_')[1])

    df = pd.read_csv(os.path.join(DIR_NAME, file), header=1, names=headers)

    # Відкинути всі nan. При цьому враховуйте, що nan у файлі позначаються як -1
    df = df.drop(df.loc[df['VHI'] == -1].index)
    # Відкинути пустий стовбчик
    df = df.drop("empty", axis=1)
    # Відкинути останній рядок
    df = df.drop(df.index[-1])
    # В першому рядку неправильно задано рік
    df.at[0, "Year"] = df.at[0, "Year"][9:]
    # Дропнути Na
    df = df.dropna()

    df.insert(0, "pID", pid, True)

    df['Year'] = df['Year'].astype(int)
    df['Week'] = df['Week'].astype(int)

    return df

def idReplace(df):
    index_mapping = {
        1: 22,
        2: 24,
        3: 23,
        4: 25,
        5: 3,
        6: 4,
        7: 8,
        8: 19,
        9: 20,
        10: 21,
        11: 9,
        13: 10,
        14: 11,
        15: 12,
        16: 13,
        17: 14,
        18: 15,
        19: 16,
        21: 17,
        22: 18,
        23: 6,
        24: 1,
        25: 2,
        26: 7,
        27: 5,
    }
    df['pID'] = df['pID'].replace(index_mapping)
    return df


def loadFiles(dir_name):
    files = os.listdir(dir_name)
    headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
    res = []
    for file in files:
        res.append(loadFile(file, headers))

    df = pd.concat(res).drop_duplicates().reset_index(drop=True)
    df = df.loc[(df.pID != 12) & (df.pID != 20)]

    df = idReplace(df)

    return df

def filter_by_params(df, pid, date_range, week_range):
    finalDf = df[(df['pID'] == pid) &
                 (df['Year'].between(int(date_range[0]), int(date_range[1]))) &
                 (df['Week'].between(int(week_range[0]), int(week_range[1])))]
    return finalDf

rIDs = {
    1: 'Вінницька', 2: 'Волинська', 3: 'Дніпропетровська', 4: 'Донецька', 5: 'Житомирська',
    6: 'Закарпатська', 7: 'Запорізька', 8: 'Івано-Франківська', 9: 'Київська', 10: 'Кіровоградська',
    11: 'Луганська', 12: 'Львівська', 13: 'Миколаївська', 14: 'Одеська', 15: 'Полтавська',
    16: 'Рівенська', 17: 'Сумська', 18: 'Тернопільська', 19: 'Харківська', 20: 'Херсонська',
    21: 'Хмельницька', 22: 'Черкаська', 23: 'Чернівецька', 24: 'Чернігівська', 25: 'Республіка Крим'
}


class myApp(server.App):
    title = "LAB 3"

    inputs = [
        {
            "type": 'dropdown',
            "label": 'Індекс',
            "options": [
                {"label": "VCI", "value": "VCI"},
                {"label": "TCI", "value": "TCI"},
                {"label": "VHI", "value": "VHI"}
            ],
            "key": 'index',
            "action_id": "update_data"
        },
        {
            "type": 'dropdown',
            "label": 'Область',
            "options": [
                {"label": rIDs[i], "value": i} for i in range(1, 26)
            ],
            "key": 'region',
            "action_id": "update_data"
        },
        {
            "type": 'text',
            "label": 'Інтервал тижнів',
            "value": '1-52',
            "key": 'week_interval',
            "action_id": "update_data"
        },
        {
            "type": 'text',
            "label": 'Дата',
            "value": '1981-2021',
            "key": 'date_range',
            "action_id": "update_data"
        }
    ]
    
    controls = [{"type": "button", "label": "Оновити", "id": "update_data"}]
    tabs = ["Таблиця", "Графік"]
    outputs = [
        {"type": "table", "id": "table", "control_id": "update_data", "tab": "Таблиця"},
        {"type": "plot", "id": "plot", "control_id": "update_data", "tab": "Графік"}
    ]

    def getData(self, params):
        df = loadFiles(DIR_NAME)

        data = params['index']
        pid = int(params['region'])
        week_range = params['week_interval'].split('-')
        date_range = params['date_range'].split('-')

        df = filter_by_params(df, pid, date_range, week_range)

        return df

    def getPlot(self, params):
        df = loadFiles(DIR_NAME)

        data = params['index']
        pid = int(params['region'])
        week_range = params['week_interval'].split('-')
        date_range = params['date_range'].split('-')

        df = filter_by_params(df, pid, date_range, week_range)

        pivot_df = df.pivot(index='Year', columns='Week', values=data)
        plt.figure(figsize=(25, 10))
        sns.heatmap(pivot_df, cmap='coolwarm', cbar_kws={'label': data}, annot=True)
        plt.title(f'{data} Heatmap for pID {pid}')
        plt.xlabel('Week')
        plt.ylabel('Year')

        return plt.gcf()



def main():
    app = myApp()
    app.launch(port=8082)

if __name__ == '__main__':
    main()