def format_season(season_num):
    s = str(season_num)
    if len(s) == 4:
        # e.g. '2425' -> '2024/25'
        return f"20{s[:2]}/{s[2:]}"
    elif len(s) == 3:
        # e.g. '506' -> '2005/06'
        start_decade = s[0]
        end_year = s[1:]
        start_year = f"200{start_decade}"
        return f"{start_year}/{end_year}"