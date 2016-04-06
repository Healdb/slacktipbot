# slacktipbot

# Syntax:

"!tipbot register" - generates new btc/ltc/doge addresses for user.

"!tipbot check" - shows addresses for all coins and balances for user.

"!tipbot addresses coin" - lists all registered users' addresses and their balances.  coin can be btc, ltc, or doge

"!tipbot tip amount coin username" - tips user indicated amount to their address.  Subamounts such as bits or satoshi are not accepted.  coin can be btc, ltc, or doge

"!tipbot make it rain coin amount" - tips everyone registered a share of indicated amount. Amount must be the last word in the command.  Subamounts such as bits or satoshi are not accepted.  coin can be btc, ltc, or doge

"!tipbot withdraw amount coin address" - withdraws indicated amount to indicated address.  Address must be the last word listed in command. Subamounts such as bits or satoshi are not accepted.  coin can be btc, ltc, or doge

"!tipbot shift amount coin1_coin2" - uses shapeshift to exchange coin1 to coin2.  coin can be btc, ltc, or doge

"!tipbot help" - links to this readme

#Usage:
Users will first need to "!tipbot register" for the bot to generate an address for them.  The user can then see their addresses with "!tipbot check".  Deposit to that address with your preferred coin (btc/ltc/doge), and you can then tip to other registered users.  Or withdraw using "!tipbot withdraw".  All tips and withdraws are "on-chain".

The free account at block.io allows up to 100 different addresses, so 99 users can be served an address in your slack group.  If you want more, you'll need to get a paid block.io account.  If you have multiple slack groups, it is highly recommended that you create a new block.io account for each slack group you want to run the tipbot in.  You'll need seperate instances of the tipbot for each slack group.

Note that direct messaging to the bot in Slack works as well, if you don't want to crowd public channels.  The bot can operate in multiple channels if you /invite it to them.  Be aware though, the bot operator in your Slack group can also read all the channels that the bot is in.

If you try to tip/withdraw/shift an amount greater than you are able, it will reattempt with your maximum available balance.  Say your balance is 1500 doge and you tried to withdraw 1500, but you are only able to withdraw 1498 due to network transaction fees, it will attempt to withdraw 1498 after the 1500 attempt fails.

#Dependencies:

[Block.io](https://github.com/BlockIo/block_io-python/blob/master/README.md):
`pip install block-io`

[Slackclient](https://github.com/slackhq/python-slackclient):
`pip install slackclient`

[Slacksocket](https://github.com/vektorlab/slacksocket)
`pip install slacksocket`

#Installation:
Install dependencies.  Then `git clone https://github.com/peoplma/slacktipbot`  (Tested in python 3.4).  Create an account at [block.io](https://block.io/).  Add your secret_pin to the key_pin.py file, and get your API key and add that to the key_pin.py file.  In Slack, go to the Slack "custom integratrions" page (by clicking in the upper left of your chat and choosing "Apps and integrations") and add a "bot".  Get the API key and add that to the key_pin.py file.

#Security:
The bot operator has full control over everyone's addresses (that's you, not me, unless I set up the bot in your slack channel).  Users can withdraw to an address they control, and it is recommended to do so.  Significant amounts of money should not be stored in the slacktipbot address, even if you trust the bot operator completely.
