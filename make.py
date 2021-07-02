from analyze import Champion, ChampionData
from datadragontest import Canvas
import pandas as pd
import discord
from discord import role
from discord.ext import commands
from riotwatcher import LolWatcher, ApiError
client = commands.Bot(command_prefix=".", help_command=None)
import os
kr = pd.read_csv('KR_DATA.csv')
euw = pd.read_csv('EUW1_DATA.csv')
la = pd.read_csv('LA2_DATA.csv')
result = [kr, euw, la]
df = pd.concat(result)
VERSION = '11.13.1'
champs_map = {
        "aatrox": ['atrox', 'atrocs', 1, 'Atrox'],
        "ahri": ['ari', 'ary', 'Ahri'],
        "akali": ['alt_name'],
        "alistar": ['Alistar', 'alista'],
        "amumu": ['Amumu', 'amomo'],
        "anivia": ['Anivia', 'ahnivia'],
        "annie": ['Annie', 'ani', 'any'],
        "aphelios": ['alt_name'],
        "ashe": ['alt_name'],
        "aurelion sol": ['aurelion'],
        "azir": ['alt_name'],
        "bard": ['bardo'],
        "blitzcrank": ['alt_name'],
        "brand": ['alt_name'],
        "braum": ['alt_name'],
        "caitlyn": ['alt_name'],
        "camille": ['alt_name'],
        "cassiopeia": ['alt_name'],
        "chogath": ["cho'gat", 'cho gat', 'cho'],
        "corki": ['alt_name'],
        "darius": ['alt_name'],
        "diana": ['alt_name'],
        "drMundo": ['dr. mundo', 'dr mundo','dr'],
        "draven": ['alt_name'],
        "ekko": ['alt_name'],
        "elise": ['alt_name'],
        "evelynn": ['alt_name'],
        "ezreal": ['alt_name'],
        "fiddlesticks": ['fidle'],
        "fiora": ['alt_name'],
        "fizz": ['alt_name'],
        "galio": ['alt_name'],
        "gangplank": ['alt_name'],
        "garen": ['alt_name'],
        "gnar": ['alt_name'],
        "gragas": ['alt_name'],
        "graves": ['alt_name'],
        "gwen": ['alt_name'],
        "hecarim": ['alt_name'],
        "heimerdinger": ['alt_name'],
        "illaoi": ['alt_name'],
        "irelia": ['alt_name'],
        "ivern": ['alt_name'],
        "janna": ['alt_name'],
        "JarvanIV": ['jarvan', 'jarvaniv'],
        "jax": ['alt_name'],
        "jayce": ['alt_name'],
        "jhin": ['alt_name'],
        "jinx": ['alt_name'],
        "kaisa": ["kai'sa", 'kai sa', 'kai'],
        "kalista": ['alt_name'],
        "karma": ['alt_name'],
        "karthus": ['alt_name'],
        "kassadin": ['alt_name'],
        "katarina": ['alt_name'],
        "kayle": ['alt_name'],
        "kayn": ['alt_name'],
        "kennen": ['alt_name'],
        "khazix": ["Kha'Zix", "kha'zix", 'k6', 'kha six', 'kha'],
        "kindred": ['alt_name'],
        "kled": ['alt_name'],
        "kogMaw": ["kog'maw", "kog"],
        "leblanc": ['leb'],
        "LeeSin": ['lisin', 'lee sin', 'li sin', 'lee'],
        "leona": ['alt_name'],
        "lillia": ['alt_name'],
        "lissandra": ['alt_name'],
        "lucian": ['alt_name'],
        "lulu": ['alt_name'],
        "lux": ['alt_name'],
        "malphite": ['alt_name'],
        "malzahar": ['alt_name'],
        "maokai": ['alt_name'],
        "MasterYi": ['master yi', 'maestro yi', 'master', 'maestro', 'yi'],
        "MissFortune": ["miss fortune", 'miss'],
        "mordekaiser": ['alt_name'],
        "morgana": ['alt_name'],
        "nami": ['alt_name'],
        "nasus": ['alt_name'],
        "nautilus": ['alt_name'],
        "neeko": ['alt_name'],
        "nidalee": ['alt_name'],
        "nocturne": ['alt_name'],
        "nunu": ['nunu', 'nunu y willump'],
        "olaf": ['alt_name'],
        "orianna": ['alt_name'],
        "ornn": ['alt_name'],
        "pantheon": ['panteon'],
        "poppy": ['alt_name'],
        "pyke": ['alt_name'],
        "qiyana": ['alt_name'],
        "quinn": ['quin'],
        "rakan": ['racan'],
        "rammus": ['alt_name'],
        "RekSai": ['rek','rek sai', 'Rek' ],
        "rell": ['alt_name'],
        "renekton": ['alt_name'],
        "rengar": ['alt_name'],
        "riven": ['alt_name'],
        "rumble": ['alt_name'],
        "ryze": ['alt_name'],
        "samira": ['alt_name'],
        "sejuani": ['alt_name'],
        "senna": ['alt_name'],
        "seraphine": ['alt_name'],
        "sett": ['alt_name'],
        "shaco": ['alt_name'],
        "shen": ['alt_name'],
        "shyvana": ['shivana'],
        "singed": ['alt_name'],
        "sion": ['alt_name'],
        "sivir": ['alt_name'],
        "skarner": ['scarner'],
        "sona": ['alt_name'],
        "soraka": ['alt_name'],
        "swain": ['alt_name'],
        "sylas": ['alt_name'],
        "syndra": ['alt_name'],
        "tahmkench": ['tahm kench', 'tahm'],
        "taliyah": ['alt_name'],
        "talon": ['alt_name'],
        "taric": ['alt_name'],
        "teemo": ['alt_name'],
        "thresh": ['alt_name'],
        "tristana": ['alt_name'],
        "trundle": ['alt_name'],
        "tryndamere": ['alt_name'],
        "twistedfate": ['twisted fate', 'twisted'],
        "twitch": ['alt_name'],
        "udyr": ['alt_name'],
        "urgot": ['alt_name'],
        "varus": ['alt_name'],
        "vayne": ['alt_name'],
        "veigar": ['alt_name'],
        "vel'koz": ["vel'koz", 'vel koz', 'vel'],
        "vi": ['alt_name'],
        "viego": ['alt_name'],
        "viktor": ['alt_name'],
        "vladimir": ['alt_name'],
        "volibear": ['alt_name'],
        "warwick": ['alt_name'],
        "wukong": ['alt_name'],
        "xayah": ['alt_name'],
        "xerath": ['alt_name'],
        "XinZhao": ['xin zhao', 'xin'],
        "Yasuo": ['alt_name'],
        "Yone": ['alt_name'],
        "yorick": ['alt_name'],
        "yuumi": ['alt_name'],
        "zac": ['alt_name'],
        "zed": ['alt_name'],
        "ziggs": ['alt_name'],
        "zilean": ['alt_name'],
        "zoe": ['alt_name'],
        "zyra": ['alt_name'],
    }

space_champs_map = {
    "XinZhao":5,
    "MissFortune":21,
    "LeeSin":64,
    "RekSai":421,
    "MasterYi":11

}
with open('api_key.txt', 'r') as f:
    key = f.readlines()
    data_watcher = LolWatcher(key)




class Consult:
    def __init__(self, champion_id, role=None):
        self.champion_id = champion_id
        self.role = role
    
    def analyze(self):
        data = ChampionData(df)
        champion_data = data.get_champion_data(self.champion_id)
        self.champ = Champion(champion_data)
        if self.role == None:
            self.mythic, self.core ,self.final,self.starter, self.boots, self.primary_list, self.secondary_list, self.champion_name = self.champ.get_popular()
        print(self.primary_list)
    def make_all_info(self):
        self.all_info = Canvas(self.mythic, self.core, self.final, self.primary_list, self.secondary_list, self.champion_id, self.starter, self.boots)
        self.all_info.make_image()

@client.event
async def on_ready():
    print('bot ready')

@client.command(aliases=['allinfo', 'AllInfo'])
async def ai(ctx, champion):
    for value in champs_map.values():
        if champion in value:
            champion = list(champs_map.keys())[list(champs_map.values()).index(value)]
            break
    champion = champion[0].upper() + champion[1:]

    
    if os.path.isfile('./all_info/popular_' + str(champion) + ".png"):
        file = './all_info/popular_' + str(champion) + ".png"
        # await ctx.send(f'las runas de {champion} son : ')
        await ctx.send(file=discord.File(file))
    else:
       
        olaf = Consult(champion)
        olaf.analyze()
        olaf.make_all_info()
        file = './all_info/popular_' + str(champion) + ".png"
        # await ctx.send(f'las runas de {champion} son : ')
        await ctx.send(file=discord.File(file))

@client.command()
async def help(ctx):
    await ctx.send("""
#--- League Bot Commands ---#
.ai [champ] ---> overview of the champ , runes builds etc (Unfinished)
.runes [champ] [role(optional)] ---> only the runes

have fun, gl on da rift
    """)

client.run('ODQ3NDQ3ODQxMjM2MzIwMjU3.YK-NTg.8tuP_8K9qmRmC9kelmZ-Qiqwg2Y')
