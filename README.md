# Gothello Player

Copyright (c) 2019 Jason Holm

Gothello is a small-board game that combines aspects of
[Othello](https://en.wikipedia.org/wiki/Reversi) (also known as Reversi) and
[Go](https://en.wikipedia.org/wiki/Go_%28game%29).

This player uses negamax search with alpha-beta pruning and a transposition table.

This player is designed to connect to the [Gthd server](https://github.com/pdx-cs-ai/gothello-gthd)
and play against another player connected to the same server.

## Run
Once the server is running you can connect with `python3 gthplayer.py [color] [server name] [server number] [depth]`.

## License
This program is licensed under the "MIT License". Please see the file `LICENSE` for license terms.
