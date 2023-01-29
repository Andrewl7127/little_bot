# Little Bot

<img src="https://user-images.githubusercontent.com/33340487/215303416-7116313b-1950-4922-9244-d6bda0aa4f2b.jpg" with="250" height="250">

## Features 
#### <i>Queue</i>
* Bot displays a message with specified react icons.
* Upon reaction to the bot message, player gets added to the corresponding queue. 
* Bot notifies existing players in the queue of any addition or removal in real time in `#queue-notifications` which resets daily at 7 am pst.
* Queues automatically reset daily at 7 am pst.
#### <i>Fanboy/Son adoption</i>
* `!fan` to become Anju Fanboy
* `!son` to become Anju Son
#### <i>Maps, Agents, Guns, and Strat Random Generation</i>
* Allow players to type bot commands in the `#bot-commands` channel, which automatically resets daily at 7 am pst.
* `!map` to randomly generate a map choice.
* `!agent [number]` to generate the specified number of agent choices.
* `!gun` to randomly generate a gun choice from all the gun options. 
* `!pistol` to randomly generate a gun choice from only the pistol options.
* `!strat` to randomly generate a strat/play style. 
<br>

## Set up for Discord
* Create a text channel named `#queues`
* Create a text channel for queue notifications named `#queue-notifications`
* Create a text channel named `#bot-commands`
* Make sure you have a text channel named `#general`
* Create roles with format "`LFG-game.title()`" for each game.
* Name emojis with the same name as the game it corresponds to.
<br>

## Set up for Developers
* Install `discord.py` library: <b>`pip install -U discord.py`</b>
* Install `dotenv` library: <b>`pip install -U python-dotenv`</b>
* Modify _server name_ on line 20 in `main.py`
* Modify _game choices_ on line 21 in `main.py`
* Modify _maps_ and _agents_ in `randomize.py`
