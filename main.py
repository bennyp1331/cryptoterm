import curses
from curses import wrapper

# curses setup
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
stdscr.nodelay(True)

# main loop
def main(stdscr):
    rows, cols = stdscr.getmaxyx()
    
    # ALLOC = tuple(cols (x) , rows (y))
    TOP_A = tuple(cols, round(rows * .1, 1))
    BOT_A = tuple(cols, round(rows * .3, 1))
    y = (rows - (TOP_A[1] + BOT_A[1]))
    M_LEFT_A = tuple(cols * .6, y)
    x = cols - M_LEFT_A[0]
    M_RIGHT_A = tuple(x, y)

    t_banner = curses.newwin(TOP_A[1], TOP_A[0],0,0)
    start_loc = TOP_A[1] + M_LEFT_A[1]
    b_banner = curses.newwin(BOT_A[1], BOT_A[0],start_loc,0)

    while True:
        c = stdscr.getch()
        if c == ord('q'):
            break
wrapper(main)

# shutdown functions
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()

