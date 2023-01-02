from bovada_selenium import bov_main
from heritage_selenium import her_main
from arbitrage import arbitrage_main
from arbitrage import american_decimal
from multiprocessing import Pool
import pandas as pd
from functools import reduce
import time

def get_first_word(row, col_name):
    words = row[col_name].split(" ")
    if words[0] != "New":
        return words[0]
    else:
        return str(words[0] + ' ' + words[1])

def smap(f):
    df = f()
    print(str(f) + " succeeded!")
    return df

def runInParallel():
    pool = Pool()
    functionlist = [bov_main, her_main]
    res = pool.map(smap, functionlist)
    return res

def get_data():
    books = runInParallel()
    books_teams = ["bov_teams", "her_teams"]
    i = 0
    for book in books:
        book["team_shortened"] = book.apply(lambda row: get_first_word(row, books_teams[i]), axis=1)
        i += 1
    print(books)

    combined_df = reduce(lambda left,right: pd.merge(left,right,on=['team_shortened'], how='inner'), books)
    for (columnName, columnData) in combined_df.iteritems():
        if columnName.endswith('index'):
            combined_df = combined_df[combined_df.duplicated(subset=columnName, keep=False)]
    print(combined_df)
    return combined_df

def check_arbitrage(dataframe):
    odds_columns = []
    for colname in dataframe.columns:
        if colname.endswith('odds'):
            odds_columns.append(colname)
    
    best_odds = []
    odds_pair = []
    for index, row in dataframe.iterrows():
        best_odd = -100000000
        for colname in odds_columns:
            if int(row[colname]) > int(best_odd):
                best_odd = row[colname]
        odds_pair.append(best_odd)

        if index % 2 == False:
            best_odds.append(odds_pair)
            odds_pair = []
    
    for pair in best_odds:
        odd1, odd2 = pair[0], pair[1]
        arbitrage = arbitrage_main(american_decimal(odd1), american_decimal(odd2))
        if isinstance(arbitrage, bool) != True:
            # Arbitrage
            print("arb % = %{}\nreturn = ${} for every $100\nOutcome A stake = ${}\nOutcome B stake = ${}".format(round(100*arbitrage[0], 2),round(arbitrage[1],2),round(arbitrage[2],2),round(arbitrage[3],2)))
        else:
            # No arbitrage
            print("no dice :/")

def main():
    start_time = time.time()
    df = get_data()
    print("Data collection took", time.time() - start_time, "seconds.")
    check_arbitrage(df)

if __name__ == "__main__":
    main()
    ## USE THIS EXAMPLE DATA ABOVE IF U DONT WANNA WAIT FOR CHROME TO LOAD
    # data1 = [[0, 'Brooklyn Nets', -600],[0, 'Charlotte Hornets', +375],[1, "Cleveland Cavaliers", -260],[1, 'Chicago Bulls', +190],[2, 'Dallas Mavericks', -275],[2, 'San Antonio Spurs', +200]]
    # bov = pd.DataFrame(data1, columns=['bov_index', 'bov_teams', 'bov_odds'])
    # data2 = [[0, 'Brooklyn Nets', -570],[0, 'Charlotte Hornets', +343],[1, "Dallas Mavericks", -223],[1, 'San Antonio Spurs', +177],[2, 'New York Knicks', +139],[2, 'Houston Rockets', -173]]
    # her = pd.DataFrame(data2, columns=['her_index', 'her_teams', 'her_odds'])
    # books = [bov, her]