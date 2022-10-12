from twitter_scraper_selenium import scrap_keyword
import pandas as pd
import csv

#scrap 10 posts by searching keyword "india" from date 30th August till date 31st August
scrap_keyword(keyword="ablation", browser="firefox",
                      tweets_count=10000, output_format="csv" ,until="2022-10-10", since="2020-01-01", filename='ablation_full')



# df = pd.DataFrame(csv)
# df.to_csv('embolization.csv')