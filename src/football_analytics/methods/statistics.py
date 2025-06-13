import numpy as np
import pandas as pd
import statsmodels.api as sm

def calculate_home_odds_ratio(df: pd.DataFrame) -> tuple:
    home_df = pd.DataFrame({"Home": 1, "Win": df["FTHG"] > df["FTAG"]})
    away_df = pd.DataFrame({"Home": 0, "Win": (df["FTAG"] > df["FTHG"]).astype(int)})
    df = pd.concat([home_df, away_df], ignore_index=True)

    # Prepare Data
    X = sm.add_constant(df[["Home"]])
    y = df["Win"]

    # Fit logistic regression
    model = sm.Logit(y, X).fit(disp=0)
    # Calculate odds ratios and confidence intervals
    home_odds_ratio = np.exp(model.params[1])
    ci_odds_ratios = np.exp(model.conf_int().loc["Home"])

    return (home_odds_ratio, ci_odds_ratios)

def get_odds_ratios_and_probabilities(logit: sm.Logit):
    def odds_to_prob(odds):
        return odds / (1 + odds)

    model = logit.fit()
    print(model.summary())
    coef = model.params
    odds_ratios = np.exp(coef)

    odds_away = odds_ratios['const']
    odds_home = odds_away * odds_ratios['Home']  # multiply baseline odds by Home OR

    p_away = odds_to_prob(odds_away)
    p_home = odds_to_prob(odds_home)

    ci_coef = model.conf_int()
    ci_coef.columns = ['[0.025', '0.0975]']
    ci_odds_ratios = np.exp(ci_coef)

    ci_odds_away = ci_odds_ratios.loc['const']
    ci_odds_home = ci_odds_away * ci_odds_ratios.loc['Home']  # multiply baseline odds by Home OR

    ci_p_away = odds_to_prob(ci_odds_away)
    ci_p_home = odds_to_prob(ci_odds_home)

    # Create results DataFrame
    odds_ratio = pd.DataFrame({
        'Odds Ratio': odds_ratios,
        '[0.025': [
            ci_odds_ratios.loc['const']['[0.025'], ci_odds_ratios.loc['Home']['[0.025']
        ],
        '0.0975]': [
            ci_odds_ratios.loc['const']['0.0975]'], ci_odds_ratios.loc['Home']['0.0975]']
        ],
    }).rename(index={'const': 'Away', 'Home': 'Home'})

    win_prob = pd.DataFrame({
        'Win Probability': [p_away, p_home],
        '[0.025': [
            ci_p_away['[0.025'], ci_p_home['[0.025']
        ],
        '0.0975]': [
            ci_p_away['0.0975]'], ci_p_home['0.0975]']
        ],
    }).rename(index={0: 'Away', 1: 'Home'})

    return odds_ratio, win_prob
