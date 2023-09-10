import json


def v_aroma():
    with open(f'aroma/aroma_vse.json', encoding='utf-8') as file:  # открытие страницы с ароматами из файла
        src = file.read()
        src= json.loads(src)
        zapros = input("Выберите аромат: \n" + "".join([f'{i["Название ароматизатора"]} \n' for i in src]))
        for i in src:
            if zapros in i["Название ароматизатора"]:
                return "".join([f'{i[m]} \n' for m in i])
            #else : return f"Нет такого аромата"
def v_kras():
    with open(f'kras/kras_vse.json', encoding='utf-8') as file:  # открытие страницы с красителем из файла
        src1 = file.read()
        src1= json.loads(src1)
        zapros = input("Выберите краситель: \n" + "".join([f'{i["Название красителя"]} \n' for i in src1]))
        for i in src1:
            if zapros in i["Название красителя"]:
                return "".join([f'{i[m]} \n' for m in i])
            #else:
            #    return f"Нет такого цвета"
def wosk():
    plotnost_woska = {
        "Соевый воск": 0.90,
        "Кокосовый воск": 0.97,
        "Пчелиный вокс": 0.96,
        "Парафин": 0.89
    }
    q_wosk = input(F"Выберите воск из списка: {plotnost_woska}:\n")
    p_wost = plotnost_woska[q_wosk]
    v = input(f'Введите граммовку воска: ')
    return f'Воск - {q_wosk}, объём свечи - {int(v) * p_wost} мл.'

def fitil():
    vid_fitil = {
        "хлопковый",
        "конопляный",
        "деревянный",
        "армированный"

    }
    vid_fitil2 = {
        "крученый",
        "плетеный",
        "косички"
    }
    q_fitil1 = input(f'Выберите фитиль из списка: {vid_fitil}')
    q_fitil2 = input(f'Выберите фитиль из списка: {vid_fitil2}')
    if q_fitil1 == "хлопковый" or q_fitil1 == "конопляный":
        res_fitil = f'Фитиль - {q_fitil1} {q_fitil2}'
    else:
        res_fitil = f'Фитиль - {q_fitil1}'
    return res_fitil


def svecha():
    # wosk()
    # fitil()
    # v_aroma()
    # v_kras()
    print(f'Ваша свеча получилась со следующими характеристиками :\n{wosk()}\n{fitil()}\nЦвет - {v_kras()}\nАромат - {v_aroma()}')

svecha()
# ykrashenie
# tara
# gips
# woda