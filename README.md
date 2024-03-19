# Scraping Basketball
## Python Functions to Scrape BasketballReference for recent and historic NBA/ABA data
### Respository Contents
#### Juypter Notebooks
* "Getting Old Data (ABA).ipnyb" – Notebook containing uses of each function, along with development history of each function

**WARNING**: DO NOT RUN ALL CELLS OF THE NOTEBOOK, as gen_player_lm_data function takes ~10 minutes for most years
#### Python Files
* <ins>get_player_stats_team.py</ins> – obtains stats of all players for a given team in the designated year
    * **REQUIRED parameters**
        * team: full name of the NBA/ABA team, i.e. "Milwaukee Bucks," "Virginia Squires"
        * year: last year of an NBA/ABA season, i.e. for the 2022-23 season, use "2023"
        * mode: string matching any of 'totals|per_game|per_minute|per_poss|advanced'
        * Optional
            * league: string matching 'NBA|ABA' pertaining to the given league
* <ins>get_team_roster.py</ins> – obtains dict of all players for a given team in the designated year
    * **REQUIRED parameters**
        * team: full name of the NBA/ABA team, i.e. "Milwaukee Bucks," "Virginia Squires"
        * year: last year of an NBA/ABA season, i.e. for the 2022-23 season, use "2023"
        * Optional
            * league: string matching 'NBA|ABA' pertaining to the given league
    
    **RETURNS** 
        dict: {player1_name:{
                    'pos': string,
                    'height': string,
                    'weight': string,
                    'birth_date': string,
                    'birth_country': string,
                    'years_experience': char,
                    'college': string
                },
                player2_name:{...},
                ...
              }