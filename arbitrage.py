def american_decimal(american):
    # positive
    if american > 0:
        return ((american/100) + 1)
    # negative
    if american < 0:
        return ((100/abs(american)) + 1)

def arbitrage_main(pos, neg):
    ## CHECK FOR ARBITRAGE
    outcome = (1/pos) + (1/neg)
    
    if outcome < 1:
        return_on_investment = 100/outcome - 100
        stake_pos = (100/pos)/outcome
        stake_neg = (100/neg)/outcome
        return outcome, return_on_investment, stake_pos, stake_neg
    else:
        return False

if __name__ == "__main__":
    arbitrage = arbitrage_main(american_decimal(+130), american_decimal(-120))
    if isinstance(arbitrage, bool) != True:
        print("arb % = %{}\nreturn = ${} for every $100\nOutcome A stake = ${}\nOutcome B stake = ${}".format(round(100*arbitrage[0], 2),round(arbitrage[1],2),round(arbitrage[2],2),round(arbitrage[3],2)))
    else:
        print("no dice :/")