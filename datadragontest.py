from riotwatcher import LolWatcher, ApiError
from PIL import Image 
VERSION = '11.13.1'

with open('api_key.txt', 'r') as f:
    key = f.readlines()
    data_watcher = LolWatcher(key)

runes = data_watcher.data_dragon.runes_reforged(version=VERSION)
items = data_watcher.data_dragon.items(version=VERSION)


class Canvas:
    image_pos_map = {
        0: (0,10),
        1: (50,285),
        2: (50,510),
        3: (50,735)
    }
    core_map = {
    0: (760,445),
    1: (980,445),
        
    }
    starter_map = {
      0: (540,160),
    1: (760,160),
    2:(980,160),
    }
    sec_pos_map = {
        0: (300,10),
        1: (300,285),
        2: (300,510),
        3: (300,735)
    }
    primary_map = {
    8100 :0,
    8300: 1,
    8000: 2, 
    8400: 3,
    8200: 4
}   
    final_map ={
    0:(540,750),
    1: (760,750),
    2: (980,750),  
    }
    runes = data_watcher.data_dragon.runes_reforged(version=VERSION)
    items = data_watcher.data_dragon.items(version=VERSION)
    spells = data_watcher.data_dragon.summoner_spells(version=VERSION)
    
    base_path = './img/'
    background_path = r"./background.png"
    items_path = './' + VERSION + '/img/item/'
    def __init__(self, mythic, core, final, primary_runes, secondary_runes, champion, starter, boots, spell1,spell2):
        self.champion = champion
        self.mythic = mythic #int
        self.core = core # a list of ints
        self.final = final # other list of ints
        self.primary_runes = primary_runes # list of ints
        self.secondary_runes = secondary_runes # list of ints
        self.canvas = Image.open(Canvas.background_path)
        self.canvas = self.canvas.resize(size=(1920,1000))
        self.starter = starter
        self.boots = boots
        self.spell1 = spell1
        self.spell2 = spell2
    def make_image(self):
        self.find_runes()
        self.find_items()
        self.find_starter()
        print(self.boots)
        self.find_boots()
        self.canvas.save('./all_info/' + 'popular_' + str(self.champion) + '.png')
    def find_runes(self):
        keystone = (self.primary_runes[0] // 100)*100
        if keystone == 9100:
            keystone = 8100
        if keystone == 9900:
            keystone = 8100
        
        keystone = Canvas.primary_map[keystone]
        print(keystone)
        # for the primary page
        for sloth in range(4):
            try:
                row = Canvas.runes[keystone]['slots'][sloth]['runes']
                for rune in row:
                    if self.primary_runes[sloth] == rune['id']:
                        if sloth > 0:
                            rune_img = Image.open(Canvas.base_path + rune['icon'])
                            rune_img = rune_img.resize(size=(150,150))
                            self.canvas.paste(rune_img, Canvas.image_pos_map[sloth], mask = rune_img)
                        else:
                            rune_img = Image.open(Canvas.base_path + rune['icon'])
                            self.canvas.paste(rune_img, Canvas.image_pos_map[sloth], mask = rune_img)
                    
                    
            except IndexError:
                print(f'error at {sloth}')

        secondary_keystone = (self.secondary_runes[0] // 100)*100
        if secondary_keystone == 9100:
            secondary_keystone = 8000
        if secondary_keystone == 9900:
            secondary_keystone = 8100
        secondary_keystone = Canvas.primary_map[secondary_keystone]
        
        print(secondary_keystone)
        secondary_key_image = Image.open(Canvas.base_path + Canvas.runes[secondary_keystone]['icon'])
        secondary_key_image = secondary_key_image.resize(size=(150,150))
        self.canvas.paste(secondary_key_image, (300,50), mask = secondary_key_image)
        for sloth in range(4):
            try:
                row = Canvas.runes[secondary_keystone]['slots'][sloth]['runes']
                for rune in row:
                    if self.secondary_runes[0] == rune['id']:
                        rune_img = Image.open(Canvas.base_path + rune['icon'])
                        rune_img = rune_img.resize(size=(150,150))
                        self.canvas.paste(rune_img, Canvas.sec_pos_map[sloth], mask = rune_img)
                    elif self.secondary_runes[1] == rune['id']:
                        rune_img = Image.open(Canvas.base_path + rune['icon'])
                        rune_img = rune_img.resize(size=(150,150))
                        self.canvas.paste(rune_img, Canvas.sec_pos_map[sloth], mask = rune_img)
                        
            except:
                print('yes')

    def find_items(self):
        size = ((180,180))
        mythic_img = Image.open(Canvas.items_path + Canvas.items['data'][str(self.mythic)]['image']['full'])
        mythic_img = mythic_img.resize((180,180))
        self.canvas.paste(mythic_img, (540,445))
        for x in range(2):
            core_img = Image.open(Canvas.items_path + Canvas.items['data'][str(self.core[x])]['image']['full'])
            core_img = core_img.resize(size)
            self.canvas.paste(core_img, Canvas.core_map[x])
        
        for x in range(3):
            final_img = Image.open(Canvas.items_path + Canvas.items['data'][str(self.final[x])]['image']['full'])
            final_img = final_img.resize(size)
            self.canvas.paste(final_img, Canvas.final_map[x])
        
    def find_starter(self):
        size = ((180,180))
        for x in range(len(self.starter)):
            starter_img = Image.open(Canvas.items_path + Canvas.items['data'][str(self.starter[x])]['image']['full'])
            starter_img = starter_img.resize(size)
            self.canvas.paste(starter_img, Canvas.starter_map[x])
        print(self.starter)
    
    def find_boots(self):
        size = ((180,180))
        boots_img = Image.open(Canvas.items_path + Canvas.items['data'][str(self.boots)]['image']['full'])
        boots_img = boots_img.resize(size=size)
        self.canvas.paste(boots_img, (1210,160))
# photo = Canvas(6630,[3053, 3065],[3075, 6333, 3143],[8010, 9111, 9104, 8299],[8304, 8410], 1, False)
# photo.find_runes()

# photo.find_items()
# photo.canvas.save('template.png')
# photo.canvas.show()