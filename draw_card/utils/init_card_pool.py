

def init_game_pool(game: str, data: dict):
    if game == 'prts':
        SIX_LIST = [data[name]['名称'] for name in data if data[name]['星级'] == '6' and '干员寻访' in data[name]['获取途径']]
        FIVE_LIST = [data[name]['名称'] for name in data if data[name]['星级'] == '5' and '干员寻访' in data[name]['获取途径']]
        FOUR_LIST = [data[name]['名称'] for name in data if data[name]['星级'] == '4' and '干员寻访' in data[name]['获取途径']]
        THREE_LIST = [data[name]['名称'] for name in data if data[name]['星级'] == '3' and '干员寻访' in data[name]['获取途径']]
        return SIX_LIST, FIVE_LIST, FOUR_LIST, THREE_LIST

