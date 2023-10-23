# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 15:27:09 2023

@author: VP
"""
from statsbombpy import sb
import pandas as pd
# import numpy as np


# #fut_data_sample = pd.read_excel("fut_data_sample.xlsx", sheet_name = "fut_data_sample", engine="openpyxl")

time = "Bayern Munich"

data_sample_competitions = sb.competitions()
data_sample = sb.matches(competition_id=9, season_id=27) #sb.matches(competition_id=2, season_id=27)
data_sample = data_sample[(data_sample['home_team'] == time) | (data_sample['away_team'] == time)] 
              # alldata[(alldata[IBRD] !=0) | (alldata[IMF] !=0)]
#data_lineup = sb.lineups(match_id=3754124)["Manchester City"]
team_matches = data_sample["match_id"]
#events = sb.events(match_id=3754124) #3754124
temp_events = 0

for x in team_matches:
    globals()["temp_events"] = sb.events(match_id=f"{x}")
    team_matches = pd.concat([team_matches, temp_events])

team_matches = team_matches[team_matches['team'] == time] 
team_matches = team_matches[[ 'player', 'location', 'team', 'shot_type', 'possession', 'position', 'type',
                              'shot_key_pass_id', 'shot_outcome', 'shot_statsbomb_xg', 'shot_technique',
                              'match_id']]

####Calculando a quantidade de xG de cada jogador
team_xg = team_matches[team_matches['shot_statsbomb_xg'].notnull()]
team_player_xg = team_xg.groupby(['player','team'])['shot_statsbomb_xg'].sum()
team_player_xg = team_player_xg.to_frame()
team_player_xg_agg = team_player_xg.sort_values(by=['shot_statsbomb_xg'], ascending=False) #GOLS ESPERADOS POR PLAYER

####Calculando o número de gols de cada jogador para comparar com o esperado
team_gols = team_matches[team_matches['shot_outcome'] == "Goal"]
team_player_goals = team_gols.groupby(['player','team'])['shot_outcome'].count()
team_player_goals = team_player_goals.to_frame()
team_player_goals_agg = team_player_goals.sort_values(by=['shot_outcome'], ascending=False) #GOLS REAIS POR PLAYER

Comparacao_xg_reais = pd.merge(team_player_xg_agg, team_player_goals_agg, how="left", on=["player"])
Comparacao_xg_reais = Comparacao_xg_reais.rename(columns={"player": "Jogador", "shot_statsbomb_xg": "Gols esperados xG", "shot_outcome" : "Gols reais"})

# Comparacao_str = Comparacao_xg_reais.to_string()
# 34 partidas





# data_sample_competitions = sb.competitions()
# # competitions = data_sample_competitions['competition_id'].unique()
# seasons = data_sample_competitions['season_id'].unique()

# compet_seasons = pd.DataFrame()
# temp_comp      = pd.DataFrame()

# for x in seasons:
#     # competition_id = 0
#     # competitions = data_sample_competitions['competition_id'].unique()
#     # DF.loc[DF['coluna2'] == 1, 'coluna1'].unique()
#     competitions = data_sample_competitions.loc[data_sample_competitions["season_id"] == x,"competition_id"].unique().tolist()
#     # print(f"{competitions}")
#     for y in competitions :
#         print(f"Season id:{x}")
#         print(f"Compet id:{y}")
#         # globals()["temp_comp"] = sb.matches(competition_id=f"{y}", season_id=f"{x}")
#         globals()["temp_comp"] = sb.matches(competition_id=y, season_id=x)
#         compet_seasons = pd.concat([compet_seasons, temp_comp])


