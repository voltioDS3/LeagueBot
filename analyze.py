from os import execlp
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import time
from riotwatcher import LolWatcher, ApiError

# --- JOINING DATAFRAMES --- #
# kr = pd.read_csv('KR_DATA.csv')
# euw = pd.read_csv('EUW1_DATA.csv')
# la = pd.read_csv('LA2_DATA.csv')
# result = [kr, euw, la]
# df = pd.concat(result)

# --- READING THE JSON FILES FOR MAKING THE DICTIONARIES FOR RUNES , ITEMS , MYTHIC ITEMS ETC ---#
f = open('item.json',)
item_data = json.load(f)
item_data = item_data['data']
f.close()
mythic_dic = {}
complete_dic = {}
boots_dic = {}
for item in item_data:
    if 'rarityMythic' in item_data[item]['description'] and 'ornnBonus' not in item_data[item]['description']:
        mythic_dic[int(item)] = item_data[item]
    elif item_data[item]['gold']['total'] >= 1600 and 'ornnBonus' not in item_data[item]['description']:
        complete_dic[int(item)] = item_data[item]
    else:
        for tag in item_data[item]['tags']:
            if tag == 'Boots':
                boots_dic[int(item)] = item_data[item]
# print(boots_dic)
# print(mythic_dic.keys())

f = open('runesReforged.json',)
runes_data = json.load(f)
f.close()

runes_dic = {}
for x in range(5):
    runes_dic[runes_data[x]['id']] = runes_data[x]


# --- CLASS DEFINITION ---#

# I defined this class because is more structuctured to obtain the data from separetly, this class is only to do that, you can put a number or a champ
# name to start the indexing, it returns all the data, doesnt care about role


class ChampionData:
    
    def __init__(self, df):
        self.df = df

    def get_champion_data(self, identifier):
        if type(identifier) == int:
            data = self.df.loc[self.df['championId'] == identifier]
            return data
        elif type(identifier) == str:
            data = self.df.loc[self.df['championName'] == identifier]
            return data


# here is where the magic occurs , is the place to make consults, it is based in role type of functions, there are a special fuction for every roll also
# there is one for the most played role,  we split the datasets in the __init___(self) part because it will be more easy this way , i am planning on
# export this stadistics to a kind of file that we can read and then produce a image to send through a discord channel(yes this proyect is oriented to discord bot)


class Champion:
    role_map = {
        'MIDDLE': [],
        'TOP': [],
        'JUNGLE': []
    }
    primary_map = {
    8100 :0,
    8300: 1,
    8000: 2, 
    8400: 3,
    8200: 4
}  

    
    lol_watcher = LolWatcher('RGAPI-26458851-510c-426a-8623-182076ff9220')
    
    champions = lol_watcher.data_dragon.champions(version='11.12.1')
    def __init__(self, champion_data, role=None):
        # define all the data set
        self.champion_data = champion_data
        # for identidying the champion to the user of something , might use later
        self.champion_name = champion_data['championName']
        
        for name in self.champion_name:
            self.champion_name = name
                    

        
        self.popular_starter = []
        # to split the data into mid role
        self.mid_role = self.champion_data.loc[self.champion_data['lane'] == 'MIDDLE']

        # to split the data into top role
        self.top_role = self.champion_data.loc[self.champion_data['lane'] == 'TOP']

        # to split the data into top role
        self.jg_role = self.champion_data.loc[self.champion_data['lane'] == 'JUNGLE']

        # this one is a little tricky because the role adc and support share the same lane which is bottom  this is why these two lines of code
        self.sup_role = self.champion_data.loc[self.champion_data['lane'] == 'BOTTOM']
        self.sup_role = self.sup_role.loc[self.sup_role['role'] == 'SUPPORT']

        # the same method is applied to the adc role
        self.adc_role = self.champion_data.loc[self.champion_data['lane'] == 'BOTTOM']
        self.adc_role = self.sup_role.loc[self.sup_role['role'] == 'CARRY']

        # i don't really know why did i done this list but maybe is to iter through them but since there will be a funciton for every role i think its  decapited
        role_list = [self.mid_role, self.top_role,
                     self.jg_role, self.sup_role, self.adc_role]

        # we assing a random role to start the comparison to get  the popular role(the one with more games)
        self.popular = role_list[0]
        for role in role_list:
            # the len of a dataframe returns the numbers of rows that it has
            if len(self.popular) < len(role):
                self.popular = role

    # this function is pretty usefull, it gets all the items , runes, spels that the player used in every game and makes a dictionary with a
    # numpy array that has (times played, winrate) it takes a dataframe as atribute
    def get_played(self, frame):
        # sellecting the data that we are interested in
        analysis = frame[['item0', 'item1', 'item2', 'item3', 'item4', 'item5', 'spell1',
                          'spell2', 'perk0', 'perk1', 'perk2', 'perk3', 'perk4', 'perk5', 'win']]

        count = 0  # this count variable is pretty important because with this we will know in which item, perk, spell we are
        item_dic = {}
        spell1 = {}
        spell2 = {}
        primary = {}
        primary_1 = {}
        primary_2 = {}
        primary_3 = {}
        secondary = {}
        secondary_1 = {}
        win = np.array([1, 1])  # a array representing a win
        lose = np.array([1, 0])  # a array representing a lose
        for row in analysis.itertuples():  # itertuples is a method of a DataFrame object that returns a tuple of the row , in this case all the rows
            # starting at position 1 because 0 is only the index of the row and we won't need it for the analysis
            for value in row[1:]:
                if count <= 5:
                    if value in item_dic.keys():
                        if row[15] == 1:
                            item_dic[value] = np.add(item_dic[value], win)

                        else:
                            item_dic[value] = np.add(item_dic[value], lose)
                    else:
                        item_dic[value] = np.array([1, row[15]])

                elif count == 6:
                    if value in spell1.keys():
                        if row[15] == 1:
                            spell1[value] = np.add(
                                spell1[value], np.array([1, 1]))
                        else:
                            spell1[value] = np.add(
                                spell1[value], np.array([1, 0]))
                    else:
                        spell1[value] = np.array([1.0, float(row[15])])

                elif count == 7:
                    if value in spell2.keys():
                        if row[15] == 1:
                            spell2[value] = np.add(
                                spell2[value], np.array([1, 1]))
                        else:
                            spell2[value] = np.add(
                                spell2[value], np.array([1, 0]))
                    else:
                        spell2[value] = np.array([1, row[15]])

                elif count == 8:
                    if value in primary.keys():
                        if row[15] == 1:
                            primary[value] = np.add(
                                primary[value], np.array([1, 1]))
                        else:
                            primary[value] = np.add(
                                primary[value], np.array([1, 0]))
                    else:
                        primary[value] = np.array([1, row[15]])

                elif count == 9:
                    if value in primary_1.keys():
                        if row[15] == 1:
                            primary_1[value] = np.add(
                                primary_1[value], np.array([1, 1]))
                        else:
                            primary_1[value] = np.add(
                                primary_1[value], np.array([1, 0]))
                    else:
                        primary_1[value] = np.array([1, row[15]])

                elif count == 10:
                    if value in primary_2.keys():
                        if row[15] == 1:
                            primary_2[value] = np.add(
                                primary_2[value], np.array([1, 1]))
                        else:
                            primary_2[value] = np.add(
                                primary_2[value], np.array([1, 0]))
                    else:
                        primary_2[value] = np.array([1, row[15]])

                elif count == 11:
                    if value in primary_3.keys():
                        if row[15] == 1:
                            primary_3[value] = np.add(
                                primary_3[value], np.array([1, 1]))
                        else:
                            primary_3[value] = np.add(
                                primary_3[value], np.array([1, 0]))
                    else:
                        primary_3[value] = np.array([1, row[15]])

                elif count == 12:
                    if value in secondary.keys():
                        if row[15] == 1:
                            secondary[value] = np.add(
                                secondary[value], np.array([1, 1]))
                        else:
                            secondary[value] = np.add(
                                secondary[value], np.array([1, 0]))
                    else:
                        secondary[value] = np.array([1, row[15]])

                elif count == 13:
                    if value in secondary_1.keys():
                        if row[15] == 1:
                            secondary_1[value] = np.add(
                                secondary_1[value], np.array([1, 1]))
                        else:
                            secondary_1[value] = np.add(
                                secondary_1[value], np.array([1, 0]))
                    else:
                        secondary_1[value] = np.array([1, row[15]])

                count += 1
            count = 0
        for key in item_dic.keys():
            try:
                item_dic[key] = item_dic[key].astype('float64')
                item_dic[key][1] = (item_dic[key][1] / item_dic[key][0])*100
            except Exception:
                print('herewaws-1')

        for key in spell1.keys():
            spell1[key] = spell1[key].astype('float64')
            spell1[key][1] = (spell1[key][1] / spell1[key][0])*100

        for key in spell2.keys():
            spell2[key] = spell2[key].astype('float64')
            spell2[key][1] = (spell2[key][1] / spell2[key][0])*100

        for key in primary.keys():
            primary[key] = primary[key].astype('float64')
            primary[key][1] = (primary[key][1] / primary[key][0])*100

        for key in primary_1.keys():
            primary_1[key] = primary_1[key].astype('float64')
            primary_1[key][1] = (primary_1[key][1] / primary_1[key][0])*100

        for key in primary_2.keys():
            primary_2[key] = primary_2[key].astype('float64')
            primary_2[key][1] = (primary_2[key][1] / primary_2[key][0])*100

        for key in primary_3.keys():
            primary_3[key] = primary_3[key].astype('float64')
            primary_3[key][1] = (primary_3[key][1] / primary_3[key][0])*100

        for key in secondary.keys():
            secondary[key] = secondary[key].astype('float64')
            secondary[key][1] = (secondary[key][1] / secondary[key][0])*100

        for key in secondary_1.keys():
            secondary_1[key] = secondary_1[key].astype('float64')
            secondary_1[key][1] = (
                secondary_1[key][1] / secondary_1[key][0])*100

        return item_dic, spell1, spell2, primary, primary_1, primary_2, primary_3, secondary, secondary_1

    def winrate(self):
        win_count = 0
        for win in self.popular['win']:
            if win == 1:
                win_count += 1
        self.win_rate = (win_count*100) / len(self.popular['win'])

    def get_popular(self):

        # -- GET WIRATE ---#
        self.winrate()
        # --- END ---#

        #---  GETTING ALL THE THIGS OF THE CHAMP WITH WINRATE AND PICKRATE --- #
        item_dic, spell1, spell2, primary, primary_1, primary_2, primary_3, secondary, secondary_1 = self.get_played(
            self.popular)

        #--- GETTING POPULAR ITEMS AND RUNES ---#
        self.get_played_items(item_dic)
        primary_list, secondary_list = self.get_played_runes(primary, primary_1, primary_2,
                                                             primary_3, secondary, secondary_1)

        return self.popular_mythic, self.popular_core ,self.popular_final,self.popular_starter, self.popular_boots, primary_list, secondary_list, self.champion_name
        # --- DELETE THIS IS ONLY TO KNOW THAT THE CODE WORKS, IT IS ONLY TEMPORAL ---#
        
        # print(self.popular_mythic)
        # print(self.popular_core)
        # print(self.popular_final)
        
        # print(primary_list)
        # print(secondary_list)
        # print(spell1)
        # print(spell2)
        # -- END OF THE TEST PIECE OF CODE ---#
        
    # this function will do the same that the other does to the items , it will evaluate and keep the runes with the most playrate
    def get_played_runes(self, primary, primary_1, primary_2, primary_3, secondary, secondary_1):
        popular_primary = None
        for primar in primary.keys():
            if popular_primary is None:
                popular_primary = primar

            # the line above is for filter the most played rune on that champ
            if primary[primar][0] > primary[popular_primary][0]:
                popular_primary = primar

            # print(
            #     f'{primar} rune has {primary[primar][0]} and {primary[primar][1]} wineate')

        # the // is for getting only the integrer value to identify the tree bc all trees ends the same way
        primary_tree = int(popular_primary//100)*100
        if primary_tree == 9100:
            primary_tree = 8000
        if primary_tree == 9900:
            primary_tree = 8100
        primary_tree = self.primary_map[primary_tree]
        
        # print(popular_primary)

        # FIRST SLOTH OF PRIMARY PAGE
        popular_primary_1 = None
        for primary1 in primary_1.keys():
            if primary1 == 8410:
                tree = 1
            if primary1 == 8299:
                tree = 4
            elif primary1 != 8410 and primary1 != 8299:
                tree = int(primary1//100)*100
                if tree == 9100:
                    tree = 8000
                if tree == 9900:
                    tree = 8100
                tree = self.primary_map[tree]
            
            if tree == primary_tree:
                if popular_primary_1 is None:
                    popular_primary_1 = primary1

                if primary_1[primary1][0] > primary_1[popular_primary_1][0]:
                    popular_primary_1 = primary1
            # print(
            #     f'{primary1} rune has {primary_1[primary1][0]} and {primary_1[primary1][1]} wineate')

        # print(popular_primary_1)
        # DONE PRIMARY_1

        # SECOND SLOTH OF PRIMARY PAGE
        popular_primary_2 = None
        for primary2 in primary_2.keys():
            if primary2 == 8410:
                tree = 1
            if primary2 == 8299:
                tree = 4
            elif primary2 != 8410 and primary2 != 8299:
                tree = int(primary2//100)*100
                if tree == 9100:
                    tree = 8000
                if tree == 9900:
                    tree = 8100
                tree = self.primary_map[tree]
            
            
            if tree == primary_tree:
                if popular_primary_2 is None:
                    popular_primary_2 = primary2
                if primary_2[primary2][0] > primary_2[popular_primary_2][0]:
                    popular_primary_2 = primary2

        #     print(
        #         f'{primary2} rune has {primary_2[primary2][0]} and {primary_2[primary2][1]} winrate ')
        # print(popular_primary_2)
        # DONE primary_2

        # tridth sloth of primary page
        popular_primary_3 = None
        for primary3 in primary_3.keys():
            if primary3 == 8242:
                tree = 3
            elif primary3 == 8410:
                tree = 1
            elif primary3 == 8299:
                tree = 4
            elif primary3 != 8410 and primary3 != 8299 and primary3 != 8242:
                tree = int(primary3//100)*100
                if tree == 9100:
                    tree = 8000
                if tree == 9900:
                    tree = 8100
                tree = self.primary_map[tree]
            
            
            if tree == primary_tree:
                if popular_primary_3 is None:
                    popular_primary_3 = primary3
                if primary_3[primary3][0] > primary_3[popular_primary_3][0]:
                    popular_primary_3 = primary3

        #     print(
        #         f'{primary3} rune has {primary_3[primary3][0]} and {primary_3[primary3][1]} winrate ')
        # print(popular_primary_3)
        # DONEEE PRIMARY 3
        popular_primary_list = [
            popular_primary, popular_primary_1, popular_primary_2, popular_primary_3]


        
        popular_secondary = None
        for second in secondary.keys():
            if second == 8242:
                tree = 3
            if second == 8410:
                tree = 1
            if second == 8299:
                tree = 4
            elif second != 8410 and second != 8299:
                tree = int(second//100)*100
                if tree == 9100:
                    tree = 8000
                if tree == 9900:
                    tree = 8100
                tree = self.primary_map[tree]
            
            if tree != primary_tree:
                if popular_secondary is None:
                    popular_secondary = second

                if secondary[second][0] > secondary[popular_secondary][0] and tree != primary_tree:
                    popular_secondary = second


        if popular_secondary == 8242:
            secondary_tree = 3

        elif popular_secondary == 8410:
            secondary_tree = 1
        elif popular_secondary == 8299:
            secondary_tree = 4
        elif popular_secondary != 8410 and popular_secondary != 8299:
            secondary_tree = (popular_secondary//100)*100
            if secondary_tree == 9100:
                secondary_tree = 8000
            if secondary_tree == 9900:
                secondary_tree = 8100
            secondary_tree = self.primary_map[secondary_tree]
            
        print(f'{secondary_tree} this is' )
        popular_secondary_1 = None
        for second1 in secondary_1.keys():
            if second1 == 8242:
                print('yes')
                tree = 3
            elif second1 == 8410:
                print('velociti')
                tree = 1
            elif second1 == 8299:
                tree = 4
            elif second1 != 8410 and second1 != 8299 and second1 != 8242:
                tree = (second1//100)*100
                if tree == 9100:
                    tree = 8000
                if tree == 9900:
                    tree = 8100
                tree = self.primary_map[tree]
            
            

            if tree == secondary_tree:
                if popular_secondary_1 is None:
                    popular_secondary_1 = second1
                if secondary_1[second1][0] > secondary_1[popular_secondary_1][0]:
                    popular_secondary_1 = second1

        popular_secondary_list = [popular_secondary, popular_secondary_1]

        return popular_primary_list, popular_secondary_list

    def get_played_items(self, item_dic):
        self.popular_mythic = None
        self.popular_core = [None, None]
        self.popular_final = [None, None, None]
        self.popular_boots = None
        item_dic[-1] = np.array([0, 0])
        for item in item_dic.keys():
            try:
                # we iter the item_dic keys because then we will compare them to for making it easier to identify if the item is mythic or a complete item
                if item in mythic_dic.keys():
                    if self.popular_mythic == None:
                        self.popular_mythic = -1

                    if item_dic[item][0] > item_dic[self.popular_mythic][0]:
                        self.popular_mythic = item
                        pass

                elif item in complete_dic.keys():
                    if self.popular_core[0] == None:
                        self.popular_core[0] = -1
                        self.popular_core[1] = -1

                        # new
                        self.popular_final[0] = -1
                        self.popular_final[1] = -1
                        self.popular_final[2] = -1
                        # finally
                    if item_dic[item][0] > item_dic[self.popular_core[0]][0]:
                        self.popular_core[1] = self.popular_core[0]
                        self.popular_core[0] = item

                    elif item_dic[item][0] > item_dic[self.popular_core[1]][0]:
                        self.popular_final[0] = self.popular_core[1]
                        self.popular_core[1] = item

                    elif item_dic[item][0] > item_dic[self.popular_final[0]][0]:
                        self.popular_final[1] = self.popular_final[0]
                        self.popular_final[0] = item
                    elif item_dic[item][0] > item_dic[self.popular_final[1]][0]:
                        self.popular_final[2] = self.popular_final[1]
                        self.popular_final[1] = item
                    elif item_dic[item][0] > item_dic[self.popular_final[2]][0]:
                        self.popular_final[2] = item

                    # print(
                    #     f"{item} is a mythic {complete_dic[item]['name']} with {item_dic[item][0]} picks and {item_dic[item][1]} winrate")
                elif item in boots_dic.keys():
                    if self.popular_boots == None:
                        self.popular_boots = item
                    elif item_dic[item][0] > item_dic[self.popular_boots][0]:
                        self.popular_boots = item
            except Exception:
                print('exeption')

    def get_played_spels(self, spell1, spell2):
        pass

    def get_starters(self,role=None):
        tags = self.champions['data'][self.champion_name]['tags']
        for tag in tags:
            partype = tag
        
        if role == 'jg':
            self.popular_starter.append(1)
            self.popular_starter.append(2031)
        if role == 'sup':
            for tag in self.champions['data'][self.champion_name]['tags']:

                if tag == 'Marksman':
                    self.popular_starter.append(3862)
                    self.popular_starter.append(2)
                    return
                elif tag == 'Tank' or tag == 'Assasin':
                    self.popular_starter.append(3)
                    self.popular_starter.append(2)
                    return
                elif tag == 'Mage':
                    self.popular_starter.append(3850)
                    self.popular_starter.append(2)
        elif role == None:

            for tag in self.champions['data'][self.champion_name]['tags']:
                if tag == "Fighter" and partype == "None":
                    self.popular_starter.append(1055)
                    self.popular_starter.append(2003)
                    return
                elif tag == "Fighter" and partype == "Mana" or partype == "Flow":
                    self.popular_starter.append(1055)
                    self.popular_starter.append(2033)
                    return
                if tag == "Tank":
                    self.popular_starter.append(1054)
                    self.popular_starter.append(2003)
                    return
                if tag == "Marksman":
                    self.popular_starter.append(1055)
                    self.popular_starter.append(2003)
                    return
                if tag == "Mage":
                    self.popular_starter.append(1056)
                    return
                if tag == "Assasin": 
                    self.popular_starter.append(1055)
                    self.popular_starter.append(2003)
                    return
    def get_mid(self):
        pass

    def get_top(self):
        pass

    def get_adc(self):
        pass

    def get_sup(self):
        pass

    def get_jg(self):
        pass


# --- TEST PART OF THE FILE, WHEN THE FILE IS READY , TRANSFORM IT TO A MODULE AND START USING IT ON OTHER FILE ---#
# data = ChampionData(df)
# champion_data = data.get_champion_data(2)
# # print(champion_data)
# annie = Champion(champion_data)
# # print(annie.champion_name)
# annie.get_popular()
# annie.get_starters("jg")
# print(annie.popular_starter)
# print(annie.win_rate)

#--- END ---#
