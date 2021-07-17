from discord.ext import commands
from riotwatcher import LolWatcher, ApiError
from analyze_good import ChampionData, ChampionBuild
from datadragontest import Canvas
import pandas as pd
from discord import role
import discord
import os
import sys, getopt
client = commands.Bot(command_prefix=".", help_command=None)
kr = pd.read_csv('KR_DATA.csv')
euw1 = pd.read_csv('EUW1_DATA.csv')
na1 = pd.read_csv('NA1_DATA.csv')
result = [kr, euw1, na1]
df = pd.concat(result)
VERSION = '11.14.1'

with open('api_key.txt', 'r') as f:
    key = f.readlines()
    data_watcher = LolWatcher(key)


class Consult:
    def __init__(self, champion_id, role=None):
        self.champion_id = champion_id
        self.role = role
    #
    # def analyze(self):


champions = data_watcher.data_dragon.champions(version=VERSION)['data']

champ_maps = {
    266: ["Aatrox", "aatrox", "AATROX", 'atrox', 'atroz'],
    103: ["Ahri", "ahri", "AHRI", 'ari'],
    84: ["Akali", "akali", "AKALI", 'akali'],
    12: ["Alistar", "alistar", "ALISTAR", 'alitar'],
    32: ["Amumu", "amumu", "AMUMU", 'ammumu', 'amumu'],
    34: ["Anivia", "anivia", "ANIVIA"],
    1: ["Annie", "annie", "ANNIE", 'anni', 'ani', 'any', 'anny'],
    523: ["Aphelios", "aphelios", "APHELIOS", 'afelios', 'apelios', 'ap'],
    22: ["Ashe", "ashe", "ASHE", 'ache', 'a'],
    136: ["AurelionSol", "aurelionsol", "AURELIONSOL", 'aurelion', 'sol', 'aurelion sol'],
    268: ["Azir", "azir", "AZIR", 'asir', 'asur'],
    432: ["Bard", "bard", "BARD", 'bardo', ],
    53: ["Blitzcrank", "blitzcrank", "BLITZCRANK", 'blitz', 'blizcrank', 'blitzcrank'],
    63: ["Brand", "brand", "BRAND", 'bran'],
    201: ["Braum", "braum", "BRAUM"],
    51: ["Caitlyn", "caitlyn", "CAITLYN", 'cait', 'caitlin'],
    164: ["Camille", "camille", "CAMILLE", 'camile'],
    69: ["Cassiopeia", "cassiopeia", "CASSIOPEIA", 'cassio', 'casio', 'cass', 'cassiopeia'],
    31: ["Chogath", "chogath", "CHOGATH", 'chogat', 'shogat', "cho'gath", "chogat", "cho'gat"],
    42: ["Corki", "corki", "CORKI", 'korki', 'corki', 'corqui', 'korki', 'koki'],
    122: ["Darius", "darius", "DARIUS"],
    131: ["Diana", "diana", "DIANA"],
    119: ["Draven", "draven", "DRAVEN", 'draiven', 'draven'],
    36: ["DrMundo", "drmundo", "DRMUNDO", 'dr mundo', 'mundo', 'dr'],
    245: ["Ekko", "ekko", "EKKO", 'eko', 'ecco', 'eco', 'ecum'],
    60: ["Elise", "elise", "ELISE", 'elyse', 'elisse'],
    28: ["Evelynn", "evelynn", "EVELYNN", 'evelin', 'evelinn', 'eve'],
    81: ["Ezreal", "ezreal", "EZREAL", 'ez'],
    9: ["Fiddlesticks", "fiddlesticks", "FIDDLESTICKS", 'fiddle', 'fiddlestics', 'fidlestics', 'fidlesticks', 'fidol'],
    114: ["Fiora", "fiora", "FIORA"],
    105: ["Fizz", "fizz", "FIZZ", 'fis', 'fiz'],
    3: ["Galio", "galio", "GALIO", 'nopelien', 'galo'],
    41: ["Gangplank", "gangplank", "GANGPLANK", 'gp', 'gankplanc', 'gankplanck', 'ganplan'],
    86: ["Garen", "garen", "GAREN"],
    150: ["Gnar", "gnar", "GNAR", 'nar', 'gnarr'],
    79: ["Gragas", "gragas", "GRAGAS"],
    104: ["Graves", "graves", "GRAVES"],
    887: ["Gwen", "gwen", "GWEN", 'wen', ':v', 'wuen'],
    120: ["Hecarim", "hecarim", "HECARIM", 'ecarim', 'eca', 'heca', 'jeca'],
    74: ["Heimerdinger", "heimerdinger", "HEIMERDINGER", 'heimerdinger', 'heimer', 'heimmer', 'heimmendinger'],
    420: ["Illaoi", "illaoi", "ILLAOI", 'illa', 'iyaoi'],
    39: ["Irelia", "irelia", "IRELIA"],
    427: ["Ivern", "ivern", "IVERN"],
    40: ["Janna", "janna", "JANNA"],
    59: ["JarvanIV", "jarvaniv", "JARVANIV", 'jarvan', 'jarvis', 'jarvan cuarto', 'jarban'],
    24: ["Jax", "jax", "JAX", 'jac'],
    126: ["Jayce", "jayce", "JAYCE", 'jaise', 'jayse'],
    202: ["Jhin", "jhin", "JHIN", 'jin'],
    222: ["Jinx", "jinx", "JINX", 'jix', 'jincs'],
    145: ["Kaisa", "kaisa", "KAISA", "kai'sa", 'kai sa'],
    429: ["Kalista", "kalista", "KALISTA"],
    43: ["Karma", "karma", "KARMA"],
    30: ["Karthus", "karthus", "KARTHUS", 'kartus', 'khartus'],
    38: ["Kassadin", "kassadin", "KASSADIN", 'kasadin'],
    55: ["Katarina", "katarina", "KATARINA", 'kata', 'cata'],
    10: ["Kayle", "kayle", "KAYLE", 'kayle'],
    141: ["Kayn", "kayn", "KAYN"],
    85: ["Kennen", "kennen", "KENNEN"],
    121: ["Khazix", "khazix", "KHAZIX", 'k6', 'ksix', 'six', 'khasics', 'kasix'],
    203: ["Kindred", "kindred", "KINDRED", 'kindre'],
    240: ["Kled", "kled", "KLED"],
    96: ["KogMaw", "kogmaw", "KOGMAW", 'kogmau', 'komau', 'kog mau', 'kog'],
    7: ["Leblanc", "leblanc", "LEBLANC", 'leblanc', 'leb', 'leb blank'],
    64: ["LeeSin", "leesin", "LEESIN", 'lisin', 'lee', 'lee sin', 'sin'],
    89: ["Leona", "leona", "LEONA"],
    876: ["Lillia", "lillia", "LILLIA"],
    127: ["Lissandra", "lissandra", "LISSANDRA", 'liss', 'lissandra'],
    236: ["Lucian", "lucian", "LUCIAN"],
    117: ["Lulu", "lulu", "LULU"],
    99: ["Lux", "lux", "LUX"],
    54: ["Malphite", "malphite", "MALPHITE", 'malpite', 'malfite', 'literalphite'],
    90: ["Malzahar", "malzahar", "MALZAHAR"],
    57: ["Maokai", "maokai", "MAOKAI"],
    11: ["MasterYi", "masteryi", "MASTERYI"],
    21: ["MissFortune", "missfortune", "MISSFORTUNE", 'miss', 'miss fortune', 'fortune'],
    62: ["MonkeyKing", "monkeyking", "MONKEYKING", 'wukong', 'wu', 'wukong'],
    82: ["Mordekaiser", "mordekaiser", "MORDEKAISER", 'mordecaiser'],
    25: ["Morgana", "morgana", "MORGANA"],
    267: ["Nami", "nami", "NAMI", 'namy'],
    75: ["Nasus", "nasus", "NASUS"],
    111: ["Nautilus", "nautilus", "NAUTILUS", 'nauti'],
    518: ["Neeko", "neeko", "NEEKO", 'nico', 'niko', 'neeko'],
    76: ["Nidalee", "nidalee", "NIDALEE", 'nidali'],
    56: ["Nocturne", "nocturne", "NOCTURNE"],
    20: ["Nunu", "nunu", "NUNU", 'nunu y willump'],
    2: ["Olaf", "olaf", "OLAF"],
    61: ["Orianna", "orianna", "ORIANNA"],
    516: ["Ornn", "ornn", "ORNN"],
    80: ["Pantheon", "pantheon", "PANTHEON"],
    78: ["Poppy", "poppy", "POPPY"],
    555: ["Pyke", "pyke", "PYKE"],
    246: ["Qiyana", "qiyana", "QIYANA"],
    133: ["Quinn", "quinn", "QUINN"],
    497: ["Rakan", "rakan", "RAKAN"],
    33: ["Rammus", "rammus", "RAMMUS", 'ramus'],
    421: ["RekSai", "reksai", "REKSAI", 'rek sai', 'rek', 'sai'],
    526: ["Rell", "rell", "RELL", 'rel'],
    58: ["Renekton", "renekton", "RENEKTON", 'renek'],
    107: ["Rengar", "rengar", "RENGAR"],
    92: ["Riven", "riven", "RIVEN"],
    68: ["Rumble", "rumble", "RUMBLE"],
    13: ["Ryze", "ryze", "RYZE"],
    360: ["Samira", "samira", "SAMIRA"],
    113: ["Sejuani", "sejuani", "SEJUANI"],
    235: ["Senna", "senna", "SENNA"],
    147: ["Seraphine", "seraphine", "SERAPHINE"],
    875: ["Sett", "sett", "SETT"],
    35: ["Shaco", "shaco", "SHACO"],
    98: ["Shen", "shen", "SHEN"],
    102: ["Shyvana", "shyvana", "SHYVANA", 'shivana'],
    27: ["Singed", "singed", "SINGED"],
    14: ["Sion", "sion", "SION"],
    15: ["Sivir", "sivir", "SIVIR"],
    72: ["Skarner", "skarner", "SKARNER"],
    37: ["Sona", "sona", "SONA"],
    16: ["Soraka", "soraka", "SORAKA"],
    50: ["Swain", "swain", "SWAIN"],
    517: ["Sylas", "sylas", "SYLAS"],
    134: ["Syndra", "syndra", "SYNDRA"],
    223: ["TahmKench", "tahmkench", "TAHMKENCH", 'kench', 'kenc', 'quench', 'tham', 'tahm'],
    163: ["Taliyah", "taliyah", "TALIYAH"],
    91: ["Talon", "talon", "TALON"],
    44: ["Taric", "taric", "TARIC"],
    17: ["Teemo", "teemo", "TEEMO"],
    412: ["Thresh", "thresh", "THRESH"],
    18: ["Tristana", "tristana", "TRISTANA"],
    48: ["Trundle", "trundle", "TRUNDLE"],
    23: ["Tryndamere", "tryndamere", "TRYNDAMERE"],
    4: ["TwistedFate", "twistedfate", "TWISTEDFATE"],
    29: ["Twitch", "twitch", "TWITCH"],
    77: ["Udyr", "udyr", "UDYR"],
    6: ["Urgot", "urgot", "URGOT"],
    110: ["Varus", "varus", "VARUS"],
    67: ["Vayne", "vayne", "VAYNE"],
    45: ["Veigar", "veigar", "VEIGAR"],
    161: ["Velkoz", "velkoz", "VELKOZ", 'vel'],
    254: ["Vi", "vi", "VI"],
    234: ["Viego", "viego", "VIEGO"],
    112: ["Viktor", "viktor", "VIKTOR"],
    8: ["Vladimir", "vladimir", "VLADIMIR"],
    106: ["Volibear", "volibear", "VOLIBEAR"],
    19: ["Warwick", "warwick", "WARWICK"],
    498: ["Xayah", "xayah", "XAYAH"],
    101: ["Xerath", "xerath", "XERATH"],
    5: ["XinZhao", "xinzhao", "XINZHAO"],
    157: ["Yasuo", "yasuo", "YASUO"],
    777: ["Yone", "yone", "YONE"],
    83: ["Yorick", "yorick", "YORICK"],
    350: ["Yuumi", "yuumi", "YUUMI"],
    154: ["Zac", "zac", "ZAC"],
    238: ["Zed", "zed", "ZED"],
    115: ["Ziggs", "ziggs", "ZIGGS"],
    26: ["Zilean", "zilean", "ZILEAN"],
    142: ["Zoe", "zoe", "ZOE"],
    143: ["Zyra", "zyra", "ZYRA"],
    'TOP': ['top', 'toplane'],
    'MIDDLE': ['mid', 'middle'],
    'JUNGLE': ['jg', 'jungle', 'selva', 'jungla'],
    'UTILITY': ['sup', 'supp', 'support', 'soporte'],
    'BOTTOM': ['adc', 'adcarry', 'carry'],
}
role_map = {
    'TOP': ['top', 'toplane'],
    'MIDDLE': ['mid', 'middle'],
    'JUNGLE': ['jg', 'jungle', 'selva', 'jungla'],
    'UTILITY': ['sup', 'supp', 'support', 'soporte'],
    'BOTTOM': ['adc', 'adcarry', 'carry'],
}


@client.event
async def on_ready():
    print('bot ready')


class Consult:
    def __init__(self, champion, role=None):
        self.champion = champion
        self.role = role
        matches = ChampionData(df)
        champion_matches = matches.champion_data(self.champion, self.role)
        champion = ChampionBuild(champion_matches)
        self.mythic, self.core, self.final, self.starter, self.boots, self.primary_runes, self.secondary_runes, self.spell1, self.spell2, self.champion_name = champion.get_all_data()

    def make_all_info(self):
        if self.role is None:
            image = Canvas(self.mythic, self.core, self.final, self.primary_runes, self.secondary_runes, self.champion,
                           self.starter, self.boots, self.spell1, self.spell2)
            image.make_image()
        else:
            image = Canvas(self.mythic, self.core, self.final, self.primary_runes, self.secondary_runes, self.champion,
                           self.starter, self.boots, self.spell1, self.spell2)
            image.make_image(self.role)



def check_img(champion, rol=None):
    if rol is None:
        file = './all_info/popular_' + str(champion) + ".png"
        if os.path.isfile(file):
            return file
        else:
            kayn = Consult(champion)
            kayn.make_all_info()
            return file

    else:
        file = './all_info/popular_' + str(champion) + '_' + rol + ".png"
        if os.path.isfile(file):
            return file
        else:
            kindred = Consult(champion, rol)
            kindred.make_all_info()
            return file


@client.command(aliases=['allinfo', 'AllInfo'])
async def ai(ctx, champion, aux=None, aux1=None):
    # this if aux is None, then this is only the champ, with popular role
    champion = champion.lower()
    if aux is None:
        for value in champ_maps.values():
            if champion in value:
                champion = list(champ_maps.keys())[list(champ_maps.values()).index(value)]

                print(check_img(champion))
                break
        print(champion)
    # there are 3 possible options
    # 1. aux is role, then aux1 is None and this means one word champ and its role
    # 2. aux is second word of champ, and aux1 is none, then is a 2 word champs with popular role
    # 3. aux is second word champ and aux1 is its role, thus is a 2 word champ with is specific role
    elif aux is not None and aux1 is None:  # this means either opcion 1 or 2
        aux = aux.lower()

        for value in champ_maps.values():
            if aux in value:
                aux = list(champ_maps.keys())[list(champ_maps.values()).index(value)]

                if aux in role_map.keys():
                    # thi means that is option 1
                    for value in champ_maps.values():
                        if champion in value:
                            champion = list(champ_maps.keys())[list(champ_maps.values()).index(value)]
                            break
                    check_img(champion, aux)
                elif type(aux) is int:
                    # this means that is option 2
                    check_img(champion)
                    print(champion)

    if aux is not None and aux1 is not None:
        # this means option 3, thus we will

        print('option3')
        for value in champ_maps.values():
            if champion in value:
                champion = list(champ_maps.keys())[list(champ_maps.values()).index(value)]
                break

        for value in champ_maps.values():
            if aux in value:
                aux = list(champ_maps.keys())[list(champ_maps.values()).index(value)]

        for value in champ_maps.values():
            if aux1 in value:
                aux1 = list(champ_maps.keys())[list(champ_maps.values()).index(value)]
        if type(champion) is int and aux1 in role_map.keys():
            print('make consult with champion and aux1')
        elif type(aux) is int and aux1 in role_map.keys():
            print('make consult with aux and aux1')


client.run('ODQ3NDQ3ODQxMjM2MzIwMjU3.YK-NTg.8tuP_8K9qmRmC9kelmZ-Qiqwg2Y')
