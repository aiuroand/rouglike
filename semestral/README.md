# Rouglike Game


This is rouglike game implemented im python using pygame library.


You are playing for an adventurer who is lost in a labyrinth and wants to find an exit.
Your purpouse is to complete all levels by finding exit door avoiding all possible problems (doors, monsters).


Game may be launched using `make run` comand in terminal


You can control the game using your keyboard
- You can always leave the game using `ESC` button.

- In menu use `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `0` to interact and choose action.

- In game use `W` `A` `S` `D` to control you caharcter.


You can always try to create your own map using following rules:
- Map should be created in `/maps/` directory
- Map should be created in `ASCCI` format using only following symbols
- Map always have `rectangle` shape.
- Both height and width of the map can not be < 3.
- All borders should be filled by `#` symbol.
- Free spaces are filled with  ` ` (Space).
- Every map should contain `@` symbol (it represents a player)
- Every map should contain at least one exit door `E`
- Game has doors of 3 different colors: `blue`, `yellow` and `pink`,
    if you want to create a key of given color use `p`, `y`, `b` symbols.
    if you want to create a door of given color use `P`, `Y`, `B` symbols
- Game has 3 enemies' types:
    if you want to create enemy, that repeatedly moves up and down use `V` symbol (Vertical walking enemy)
    if you want to create enemy, that repeatedly moves left to right use `H` symbol (Horizontal walking enemy)
    if you want to create enemy, that would follow player always when there is a way betwwen him and player, use `R` symbol (Smart eney)


You can try to chage some window settings using `/src/window.conf` file
You can try to chage some game settings using `/src/game.conf` file


Gool Luck and Have fun!
