# twitter_steam_market
Twitter bot with steam market integration. You can send query in PM to bot and it returns count of items which match the query.

# How to use:
Account of bot: https://twitter.com/CSGO_Market_Bot
Just send PM to bot on twitter with your query.
## Disclaimer 
Becaused of free twitter API, bot cant get your twitter ID, so you have to send the ID with the query. You can actually abuse it to send PMs to other users, but dont do it please.
## Query format
 TWITTER_ID name{SKIN_NAME} float{LOW,HIGH}  stickers_count={LOW,HIGH}
 where 

 - (*required) TWITTER_ID is your numeric twitter id. You can get it from here: tweeterid.com
 - (*required) SKIN_NAME is skin name with quality copied from steam market.
 Optional:
 - float LOW,HIGH is float interval (min: 0, max:1): float
 - stickers_count LOW,HIGH is stickers count interval (min: 0, max:4):int

Example: 414512641724516276 name{AK 47 | Redline (Field-Tested)} float{0.15,0.25}  stickers_count={1,4}

## TBD
price{PRICE}
skin without quality
stickers{NAME or NAME_REGEX}
pattern{PATTERN}