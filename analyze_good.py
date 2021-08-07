import pandas as pd
from riotwatcher import LolWatcher, ApiError
import numpy as np
import time
import json
import sys, getopt

# --- Global Declaration --- #
VERSION = '11.14.1'

# DELETE THIS PIECE OF CODE AFTER TESTING
# euw = pd.read_csv('EUW1_DATA.csv')
# na = pd.read_csv('NA1_DATA.csv')
# kr = pd.read_csv('KR_DATA.csv')
# result = [euw, na, kr]
# df = pd.concat(result)
# DELETE THIS PIECE OF CODE AFTER TESTING

# gets the api key(which in this case is not that important since we will use it only for getting the datadragon
# information which can be accessed without a key
with open('api_key.txt', 'r') as f:
    key = f.readlines()
    data_watcher = LolWatcher(key)

# makes 3 dictionaries because we need to know which items are mythic, which are the completed and which are the boots
item_data = data_watcher.data_dragon.items(version=VERSION)['data']
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

# gets the runes dictionary, iter five because there are 0,1,2,4 runes, because later we will use them to classify
# the runes

runes_data = data_watcher.data_dragon.runes_reforged(VERSION)
runes_dic = {}
for x in range(5):
    runes_dic[runes_data[x]['id']] = runes_data[x]


# --- Classes Definition --- #

# the objective of this class is to have loaded the information, regardless the champion, for optimization
# this will receive an input of all the 3 datasets with games on it
class ChampionData:
    def __init__(self, matches_df):
        self.matches_df = matches_df

    def champion_data(self, identifier, role=None):
        if type(identifier) is int:
            games = self.matches_df.loc[self.matches_df['championId'] == identifier]
        elif type(identifier) is str:
            games = self.matches_df.loc[self.matches_df['championName'] == identifier]

        if role is None:
            top_games = games.loc[games['role'] == 'TOP']
            mid_games = games.loc[games['role'] == 'MIDDLE']
            jg_games = games.loc[games['role'] == 'JUNGLE']
            sup_games = games.loc[games['role'] == 'UTILITY']
            adc_games = games.loc[games['role'] == 'BOTTOM']
            role_list = [top_games, mid_games, jg_games, sup_games, adc_games]
            popular = role_list[1]
            for role in role_list:
                if len(role) > len(popular):
                    popular = role
            return popular
        elif role == 'MIDDLE':
            mid_games = games.loc[games['role'] == 'MIDDLE']
            return mid_games
        elif role == 'TOP':
            top_games = games.loc[games['role'] == 'TOP']
            return top_games
        elif role == 'JUNGLE':
            jg_games = games.loc[games['role'] == 'JUNGLE']
            return jg_games
        elif role == 'UTILITY':
            sup_games = games.loc[games['role'] == 'UTILITY']
            return sup_games
        elif role == 'BOTTOM':
            adc_games = games.loc[games['role'] == 'BOTTOM']
            return adc_games


# this class will be in charge of returning the best items for the selected role(which will be specified in the champion
# matches

class ChampionBuild:
    role_map = {
        'MIDDLE': [],
        'TOP': [],
        'JUNGLE': []
    }
    primary_map = {
        8100: 0,
        8300: 1,
        8000: 2,
        8400: 3,
        8200: 4
    }
    champions = data_watcher.data_dragon.champions(version=VERSION)

    def __init__(self, matches):
        self.matches = matches
        # information to gather
        self.starter = []
        self.mythic = None
        self.core = [None, None]
        self.final = [None, None, None]
        self.boots = None
        self.primary_runes = []
        self.secondary_runes = []
        self.spell1 = None
        self.spell2 = None
        # final of information to gather
        self.champion_name = self.matches['championName']
        for name in self.champion_name:
            self.champion_name = name
        self.win_rate = 0
        self.role = self.matches['role']
        for role in self.role:
            self.role = role
        print(self.champion_name)

    def statistics(self, frame):
        # selecting the data that we are interested in
        analysis = frame[['item0', 'item1', 'item2', 'item3', 'item4', 'item5', 'spell1',
                          'spell2', 'perk0', 'perk1', 'perk2', 'perk3', 'perk4', 'perk5', 'win']]

        count = 0  # this count variable is pretty important because with this we will know in which item, perk, spell
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
                item_dic[key][1] = (item_dic[key][1] / item_dic[key][0]) * 100
            except Exception:
                print('herewaws-1')

        for key in spell1.keys():
            spell1[key] = spell1[key].astype('float64')
            spell1[key][1] = (spell1[key][1] / spell1[key][0]) * 100

        for key in spell2.keys():
            spell2[key] = spell2[key].astype('float64')
            spell2[key][1] = (spell2[key][1] / spell2[key][0]) * 100

        for key in primary.keys():
            primary[key] = primary[key].astype('float64')
            primary[key][1] = (primary[key][1] / primary[key][0]) * 100

        for key in primary_1.keys():
            primary_1[key] = primary_1[key].astype('float64')
            primary_1[key][1] = (primary_1[key][1] / primary_1[key][0]) * 100

        for key in primary_2.keys():
            primary_2[key] = primary_2[key].astype('float64')
            primary_2[key][1] = (primary_2[key][1] / primary_2[key][0]) * 100

        for key in primary_3.keys():
            primary_3[key] = primary_3[key].astype('float64')
            primary_3[key][1] = (primary_3[key][1] / primary_3[key][0]) * 100

        for key in secondary.keys():
            secondary[key] = secondary[key].astype('float64')
            secondary[key][1] = (secondary[key][1] / secondary[key][0]) * 100

        for key in secondary_1.keys():
            secondary_1[key] = secondary_1[key].astype('float64')
            secondary_1[key][1] = (
                                          secondary_1[key][1] / secondary_1[key][0]) * 100

        return item_dic, spell1, spell2, primary, primary_1, primary_2, primary_3, secondary, secondary_1  # this s #

    def winrate(self):
        win_count = 0
        for win in self.matches['win']:
            if win == 1:
                win_count += 1
        self.win_rate = (win_count * 100) / len(self.matches['win'])

    def get_items(self, item_dic):
        item_dic[-1] = np.array([0, 0])
        for item_get_items in item_dic.keys():
            try:
                # we iter the item_dic keys because then we will compare them to for making it easier to identify if the item is mythic or a complete item
                if item_get_items in mythic_dic.keys():
                    if self.mythic is None:
                        self.mythic = -1

                    if item_dic[item_get_items][0] > item_dic[self.mythic][0]:
                        self.mythic = item_get_items
                        pass

                elif item_get_items in complete_dic.keys():
                    if self.core[0] == None:
                        self.core[0] = -1
                        self.core[1] = -1

                        # new
                        self.final[0] = -1
                        self.final[1] = -1
                        self.final[2] = -1
                        # finally
                    if item_dic[item_get_items][0] > item_dic[self.core[0]][0]:
                        self.core[1] = self.core[0]
                        self.core[0] = item_get_items

                    elif item_dic[item_get_items][0] > item_dic[self.core[1]][0]:
                        self.final[0] = self.core[1]
                        self.core[1] = item_get_items

                    elif item_dic[item_get_items][0] > item_dic[self.final[0]][0]:
                        self.final[1] = self.final[0]
                        self.final[0] = item_get_items
                    elif item_dic[item_get_items][0] > item_dic[self.final[1]][0]:
                        self.final[2] = self.final[1]
                        self.final[1] = item_get_items
                    elif item_dic[item_get_items][0] > item_dic[self.final[2]][0]:
                        self.final[2] = item_get_items

                    # print( f"{item} is a mythic {complete_dic[item]['name']} with {item_dic[item][0]} picks and {
                    # item_dic[item][1]} winrate")
                elif item_get_items in boots_dic.keys():
                    if self.boots is None:
                        self.boots = item_get_items
                    elif item_dic[item_get_items][0] > item_dic[self.boots][0]:
                        self.boots = item_get_items
            except Exception:
                print('exception getting the items')

    def get_runes(self, primary, primary_1, primary_2, primary_3, secondary, secondary_1):
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
        primary_tree = int(popular_primary // 100) * 100
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
                tree = int(primary1 // 100) * 100
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
                tree = int(primary2 // 100) * 100
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
                tree = int(primary3 // 100) * 100
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
                tree = int(second // 100) * 100
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
            secondary_tree = (popular_secondary // 100) * 100
            if secondary_tree == 9100:
                secondary_tree = 8000
            if secondary_tree == 9900:
                secondary_tree = 8100
            secondary_tree = self.primary_map[secondary_tree]

        popular_secondary_1 = None
        for second1 in secondary_1.keys():
            if second1 == 8242:

                tree = 3
            elif second1 == 8410:

                tree = 1
            elif second1 == 8299:
                tree = 4
            elif second1 != 8410 and second1 != 8299 and second1 != 8242:
                tree = (second1 // 100) * 100
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

        self.primary_runes = popular_primary_list
        self.secondary_runes = popular_secondary_list

    def get_starters(self):
        tags = self.champions['data'][self.champion_name]['tags']

        print(f'the tags are {tags}')
        partype = self.champions['data'][self.champion_name]['partype']
        print(f'partype is {partype}')

        if self.role == 'JUNGLE':
            self.starter.append(1035)
            self.starter.append(1039)
            self.starter.append(2031)
        elif self.role == 'UTILITY':
            for tag in self.champions['data'][self.champion_name]['tags']:

                if tag == 'Marksman':
                    self.starter.append(3862)
                    self.starter.append(2003)
                    self.starter.append(2003)
                    return
                elif tag == 'Tank' or tag == 'Assasin':
                    self.starter.append(3854)
                    self.starter.append(2003)
                    self.starter.append(2003)
                    return
                elif tag == 'Mage':
                    self.starter.append(3850)
                    self.starter.append(2003)
                    self.starter.append(2003)
                    
        else:

            for tag in tags:
                if tag == "Fighter" and partype == "None":
                    self.starter.append(1055)
                    self.starter.append(2003)
                    return
                elif tag == "Fighter" and partype == "Mana":
                    self.starter.append(1055)
                    self.starter.append(2033)
                    return

                elif tag == "Fighter" and partype == "Flow":
                    self.starter.append(1055)
                    self.starter.append(2003)
                    return

                if tag == "Tank":
                    self.starter.append(1054)
                    self.starter.append(2003)
                    return
                if tag == "Marksman":
                    self.starter.append(1055)
                    self.starter.append(2003)
                    return
                if tag == "Mage":
                    self.starter.append(1056)
                    self.starter.append(2033)

                    return
                if tag == "Assasin" or partype == 'Energy':
                    self.starter.append(1055)
                    self.starter.append(2003)
                    return

    def get_spells(self, spell1, spell2):
        print(spell1)
        print(spell2)
        # the all_dic in necessary because people doesn't always use flash in f, so i have to sum them all in one dic
        # to make a fair comparison , unless there could be space for errors.
        all_dic = {}
        summoner_keys = list(spell1.keys())
        for key1 in spell2.keys():
            if key1 not in summoner_keys:
                summoner_keys.append(key1)

        # add all the playtime of the summoner in total
        for summoner in summoner_keys:
            if summoner in spell1.keys() and summoner in spell2.keys():
                all_dic[summoner] = np.add(spell1[summoner], spell2[summoner])

            elif summoner in spell1.keys():
                all_dic[summoner] = spell1[summoner]
            elif summoner in spell2.keys():
                all_dic[summoner] = spell2[summoner]
        print(all_dic)
        self.spell1 = None
        self.spell2 = None
        for spell in all_dic:
            if self.spell1 is None:
                self.spell1 = spell
            elif all_dic[spell][0] > all_dic[self.spell1][0]:
                self.spell1 = spell

        del all_dic[self.spell1]
        for spell in all_dic:
            if self.spell2 is None:
                self.spell2 = spell
            elif all_dic[spell][0] > all_dic[self.spell2][0]:
                self.spell2 = spell


        print(self.spell1)
        print(self.spell2)

    def get_all_data(self):

        item_dic, spell1, spell2, primary, primary_1, primary_2, primary_3, secondary, secondary_1 = self.statistics(
            self.matches)
        self.winrate()  # win rate check
        self.get_items(item_dic)  # mythic, core ,final and boots check
        self.get_runes(primary, primary_1, primary_2, primary_3, secondary, secondary_1)  # primary_runes and secondary
        self.get_starters()  # starter check
        self.get_spells(spell1, spell2)

        return self.mythic, self.core, self.final, self.starter, self.boots, self.primary_runes, self.secondary_runes, self.spell1, self.spell2, self.champion_name

# all_matches = ChampionData(df)
# annie_mid_matches = all_matches.champion_data(2)
# annie_mid = ChampionBuild(annie_mid_matches)
# annie_mid.get_all_data()
