import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 1000)


def backtest(df: pd.DataFrame, min_points: int, min_diff_points: int, rounding_nb: float, take_profit: float,
             stop_loss: float):

    candle_length = df.iloc[1].name - df.iloc[0].name

    df["rounded_high"] = round(df["high"] / rounding_nb) * rounding_nb
    df["rounded_low"] = round(df["low"] / rounding_nb) * rounding_nb

    price_groups = {"supports": dict(), "resistances": dict()}
    resistances_supports = {"supports": [], "resistances": []}

    for index, row in df.iterrows():

        for side in ["resistances", "supports"]:

            h_l = "high" if side == "resistances" else "low"

            if row["rounded_" + h_l] in price_groups[side]:

                grp = price_groups[side][row["rounded_" + h_l]]

                if index >= grp["last"] + min_diff_points * candle_length:
                    grp["prices"].append(row[h_l])

                    if len(grp["prices"]) >= min_points:
                        extreme_price = max(grp["prices"]) if side == "resistances" else min(grp["prices"])
                        resistances_supports[side].append({"price": extreme_price, "broken": False})

                    grp["last"] = index

            else:
                price_groups[side][row["rounded_" + h_l]] = {"prices": [row[h_l]], "start_time": index, "last": index}










