# Sports-Betting
## Arbitrage model
My first model was an arbitrage detector to find any surebets (bets with guaranteed profit) between sportsbooks. Currently, I've only written code for scraping bets and events from 2 books using Selenium, so you probably be waiting a long time before you find any arbs. The main purpose of this model was to dip my toes into sports model creating, but maybe I'll revisit it and add more books.
## Regression models
These models use various regression methods, from simple implementations of statistics to machine learning algorithms. I haven't put all of them on here yet, but here's a summary for the ones I have included:
### Model v1
Uses XGB Boost Regressor model on a 2020 NBA team stats summary dataset so, given stats of a game, you can predict how many points the team scored. Now obviously you can't get stats for a game that hasn't happened yet, but the idea was you could use the teams performances during the current season to estimate how many total points would be scored for Over/Under odds. However, its a superficial model that was more of a test than anything, so I wouldn't reccommend using it :)
### Model v2
Uses Support Vector Classification (SVC) model on a dataset of all the games from the 2020 season scraped from SDQL. It uses 3 factors: whether the team is playing at home, whether they're the underdog, and whether they won the last game or not. It shows that such basic stats could yield profitable results, since most runs of the model on the test dataset yield a decent profit. 
