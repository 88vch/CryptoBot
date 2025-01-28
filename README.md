# CryptoBot
todo;
- finish analyzing initial code (line 98-)
- try to run the code
    If fail,
    - check api's and see what needs re-writing
    - make adjustments as necessary
    - create hyperparameters, create a script that auto-runs every [x] period of time to scan for winners, logging them down somewhere
    - (EVEN MORE ADVANCED): create another agent which runs after this parser, and checks each record (wins / losses, etc) and makes adjustments to the code (is this possible; will need to re-write initial parser script to be an object [so thatt modifications can be made in real time without having to modify code])

<br><hr>

source (op): https://x.com/Web3Marmot/status/1883960123334484279

source (op code): https://pastebin.com/uyvFEQHU


<br><hr>

### APIs used
| API | API Call | DevLinks |
|------------------|-----------------|-----------------|
| dexscreener    | https://api.dexscreener.com/latest/dex/tokens/{token_address}    | https://docs.dexscreener.com/api/reference    |
| tweetscout    | https://tweetscout.io/token/{token_name}    | https://app.tweetscout.io/developer    |
| rugcheck    | https://rugcheck.xyz/tokens/{token_address}    | https://api.rugcheck.xyz/swagger/index.html#/    |
