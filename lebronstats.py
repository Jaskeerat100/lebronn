import pandas as pd
from collections import defaultdict
from functools import reduce

# -------- REGULAR SEASON DATA --------
# Format: (Season, Team, G, GS, PPG, FG%, FT%, FGA, MPG, POS, AST)
lebron_regular = [
    ("2003-04", "CLE", 79, 79, 20.9, 0.417, 0.754, 18.9, 39.5, "SF", 5.9),
    ("2004-05", "CLE", 80, 80, 27.2, 0.472, 0.750, 20.4, 42.4, "SF", 7.2),
    ("2005-06", "CLE", 79, 79, 31.4, 0.480, 0.738, 23.1, 42.5, "SF", 6.6),
    ("2006-07", "CLE", 78, 78, 27.3, 0.476, 0.698, 20.8, 40.9, "SF", 6.0),
    ("2007-08", "CLE", 75, 74, 30.0, 0.484, 0.712, 21.9, 40.4, "SF", 7.2),
    ("2008-09", "CLE", 81, 81, 28.4, 0.489, 0.780, 20.1, 37.7, "SF", 7.2),
    ("2009-10", "CLE", 76, 76, 29.7, 0.503, 0.767, 20.1, 39.0, "SF", 8.6),
    ("2010-11", "MIA", 79, 79, 26.7, 0.510, 0.759, 18.8, 38.8, "SF", 7.0),
    ("2011-12", "MIA", 62, 62, 27.1, 0.531, 0.771, 19.3, 37.5, "SF", 6.2),
    ("2012-13", "MIA", 76, 76, 26.8, 0.565, 0.753, 17.8, 37.9, "SF", 7.3),
    ("2013-14", "MIA", 77, 77, 27.1, 0.567, 0.750, 17.6, 37.7, "SF", 6.3),
    ("2014-15", "CLE", 69, 69, 25.3, 0.488, 0.710, 18.5, 36.1, "SF", 7.4),
    ("2015-16", "CLE", 76, 76, 25.3, 0.520, 0.731, 18.2, 35.6, "SF", 6.8),
    ("2016-17", "CLE", 74, 74, 26.4, 0.548, 0.678, 18.2, 37.8, "SF", 8.7),
    ("2017-18", "CLE", 82, 82, 27.5, 0.542, 0.731, 19.3, 36.9, "PG", 9.1),
    ("2018-19", "LAL", 55, 55, 27.4, 0.510, 0.665, 19.9, 35.2, "PG", 8.3),
    ("2019-20", "LAL", 67, 67, 25.3, 0.493, 0.693, 19.4, 34.6, "PG", 10.2),
    ("2020-21", "LAL", 45, 45, 25.0, 0.513, 0.698, 18.3, 33.4, "PG", 7.8),
]

# -------- PLAYOFF DATA --------
# Format: (Season, G, PPG, FGA, MPG, FG%)
lebron_playoffs = [
    ("2005-06", 13, 30.8, 21.5, 42.5, 0.476),
    ("2006-07", 20, 25.1, 21.3, 41.4, 0.416),
    ("2007-08", 13, 28.2, 21.1, 42.5, 0.419),
    ("2008-09", 14, 35.3, 20.2, 41.1, 0.510),
    ("2009-10", 11, 29.1, 19.8, 41.5, 0.502),
    ("2010-11", 21, 23.7, 19.9, 43.9, 0.466),
    ("2011-12", 23, 30.3, 21.4, 42.7, 0.500),
    ("2012-13", 23, 25.9, 20.3, 41.7, 0.491),
    ("2013-14", 20, 27.4, 19.5, 42.1, 0.565),
    ("2014-15", 20, 26.8, 22.3, 42.4, 0.417),
    ("2015-16", 21, 26.3, 21.0, 39.1, 0.525),
    ("2016-17", 18, 32.8, 22.4, 41.3, 0.565),
    ("2017-18", 22, 34.0, 22.5, 41.9, 0.539),
    ("2019-20", 21, 27.6, 20.7, 41.0, 0.560),
]

# Convert playoff list to dictionary by season
playoff_dict = {s[0]: s for s in lebron_playoffs}

# -------- FUNCTIONAL ANALYSIS --------

# Regular Season Functional Answers
over_28_ppg = list(map(lambda x: x[0], filter(lambda x: x[4] > 28, lebron_regular)))
fg_over_500 = list(map(lambda x: x[0], filter(lambda x: x[5] > 0.5, lebron_regular)))
cle_ft_over_720 = list(map(lambda x: x[0], filter(lambda x: x[1] == "CLE" and x[6] > 0.720, lebron_regular)))
mia_fg = list(map(lambda x: x[5], filter(lambda x: x[1] == "MIA", lebron_regular)))
avg_mia_fg = round(sum(mia_fg) / len(mia_fg), 3)
total_games = reduce(lambda acc, x: acc + x[2], lebron_regular, 0)
games_missed = list(map(lambda x: (x[0], 82 - x[2]), lebron_regular))
total_gs = sum(map(lambda x: x[3], lebron_regular))
percent_started = round((total_gs / total_games) * 100, 2)
years_played = len(lebron_regular)

# AST by position
ast_by_pos = defaultdict(list)
for x in lebron_regular:
    ast_by_pos[x[9]].append(x[10])
avg_ast_by_pos = {pos: sum(vals)/len(vals) for pos, vals in ast_by_pos.items()}
best_ast_pos = max(avg_ast_by_pos, key=avg_ast_by_pos.get)

# Playoff Analysis
total_playoff_games = sum(p[1] for p in lebron_playoffs)
total_fga = sum(p[3] * p[1] for p in lebron_playoffs)
avg_fga_playoffs = round(total_fga / total_playoff_games, 2)

fg_comparison = []
for reg in lebron_regular:
    season = reg[0]
    if season in playoff_dict:
        reg_fg = reg[5]
        po_fg = playoff_dict[season][5]
        winner = "Regular" if reg_fg > po_fg else "Playoffs"
        fg_comparison.append((season, reg_fg, po_fg, winner))

mpg_comparison = list(map(lambda s: (s[0], s[8], playoff_dict[s[0]][4]), filter(lambda s: s[0] in playoff_dict, lebron_regular)))
both_above_500_seasons = [s[0] for s in lebron_regular if s[0] in playoff_dict and s[5] > 0.5 and playoff_dict[s[0]][5] > 0.5]

# -------- FINAL OUTPUT --------

print("\n===== LEBRON JAMES REGULAR SEASON ANALYSIS =====")
print("1. Seasons > 28 PPG:", over_28_ppg)
print("2. Seasons FG% > .500:", fg_over_500)
print("3. CLE Seasons FT% > .720:", cle_ft_over_720)
print("4. Avg FG% in MIA:", avg_mia_fg)
print("5. Total Games Played:", total_games)
print("6. Games Missed Per Season:")
for season, missed in games_missed:
    print(f"   {season}: {missed}")
print("7. % Games Started:", f"{percent_started}%")
print("8. Years Played:", years_played)
print("9. AST Avg by Position:", avg_ast_by_pos)
print("   -> Highest: ", best_ast_pos)

print("\n===== PLAYOFF vs REGULAR SEASON ANALYSIS =====")
print("1. Total Playoff Games:", total_playoff_games)
print("2. Avg FG Attempts/Game (Playoffs):", avg_fga_playoffs)
print("3. FG% Comparison (Reg vs Playoffs):")
for item in fg_comparison:
    print(f"   {item[0]}: REG {item[1]} vs PO {item[2]} → Higher in: {item[3]}")
print("4. MPG Comparison:")
for m in mpg_comparison:
    print(f"   {m[0]}: REG {m[1]} MPG vs PO {m[2]} MPG")
print("5. Seasons with FG% > .500 in BOTH REG & PO:", both_above_500_seasons)
