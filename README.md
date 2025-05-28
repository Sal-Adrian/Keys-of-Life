
# Keys of Life
Conway's Game of Life, except the tiles play a little song. A small project that mixes cellular automata and generative music.

## Demo

https://github.com/user-attachments/assets/59b1ad56-5020-48a2-9cf9-1455de6c9989


## Run `App.py`

### Requires:
- `tkinter`
- `ttkbootstrap`
- `PIL`
- `pygame`

## Miscellaneous:

| | |
| --- | --- |
| Board Length: | 3-30 |
| BPM: | 1-300 |
| Max Notes: | $\geq$ -1 |

When Max Notes = -1, all possible notes will play.

By default, the row with the most live tiles will play thier note. 
The "Random" checkbox negates this priority.

"Go Back" button loads board configuration since the last time "Play" button was pressed.

### Recommendations:

Don't have too many notes playing at once. It sounds annoying. I suggest keeping it less than 6.

Turning "Random" on when "Insen" & "In" Scale are selected sounds nice.
