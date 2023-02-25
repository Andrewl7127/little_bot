# Little Bot

<img src="https://user-images.githubusercontent.com/33340487/215303416-7116313b-1950-4922-9244-d6bda0aa4f2b.jpg" with="250" height="250">

## Features 
#### <i>Queue</i>
* Bot displays a message with specified react icons.
* Upon reaction to the bot message, player gets added to the corresponding queue.
# Once queue is full, players are asked to react within 10 minutes to stay in the queue.
* Bot notifies existing players in the queue of any addition or removal in real time in `#queue-notifications` which resets daily at 7 am pst.
* Queues automatically reset daily at 7 am pst.
#### <i>Maps, Agents, Guns, and Strat Random Generation</i>
* Allow players to type bot commands in the `#bot-commands` channel, which automatically resets daily at 7 am pst.
* `!map` to randomly generate a Valorant map choice.
* `!agent [number]` to generate the specified number of Valorant agent choices.
* `!gun` to randomly generate a gun choice from all the Valorant gun options. 
* `!pistol` to randomly generate a gun choice from only the Valorant pistol options.
* `!strat` to randomly generate a Valorant strat/play style.
#### <i>Events</i>
* Event notifications are housed in the `#events` channel, which automatically resets daily at 7 am pst.
* `!schedule [game] [time] [notify]` to schedule a game event at a certain time.
#### <i>Misc</i>
* `!fan` to become Anju Fanboy
* `!son` to become Anju Son
<br>

## Set up for Discord
* Create the following text channels: `#general`, `#help`, `#queues`, `#queue-notifications`, `#bot-commands`, `#events`
* Make sure permissions are set correctly for channels so that users can't add type or add reactions/other media to `#help`, `#queues`, `#queue-notifications`,  `#events`
* Create roles with format "`game`" for each game.
* Name emojis with the same name as the game it corresponds to.
<br>

## Set up for Developers
* Install `discord.py` library: <b>`pip install -U discord.py`</b>
* Install `dotenv` library: <b>`pip install -U python-dotenv`</b>
* Modify _server name_ on line 20 in `main.py`
* Modify _game choices_ on line 21 in `main.py`
* Modify _maps_ and _agents_ in `randomize.py`


#### Invite link: https://discord.com/oauth2/authorize?client_id=1068445743028903957&permissions=8&scope=bot
