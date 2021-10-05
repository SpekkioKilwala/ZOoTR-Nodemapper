import pandas as pd

df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

# df:
#      Fruit  Amount      City
# 0   Apples       4        SF
# 1  Oranges       1        SF
# 2  Bananas       2        SF
# 3   Apples       2  Montreal
# 4  Oranges       4  Montreal
# 5  Bananas       5  Montreal

# So I'm going to be defining networks (multiple separate networks) from dataframes.
# (Which the user can then join together.)
# First work out what the DFs look like, then figure out how to create those.
#   Using dicts would probably be a mess unless I was creating them separately.
# DON'T FORGET, this thing supports having one dataframe for the nodes and another one for the edges.

#              Cluster             Node
# 0       "Goron City"            "Main"
# 1       "Goron City"  "Darunia's Room"
# 2       "Goron City" "Lost Woods Warp"
# 3       "Goron City"       "By Grotto"
# 4    "Lon Lon Ranch"            "Main"
# 5 "Generic Grotto 1"
# 6 "Generic Grotto 2" GenGrotto
