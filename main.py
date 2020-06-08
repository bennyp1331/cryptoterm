import curses
from curses import wrapper
import pprint

DEBUG = True

# curses setup
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
stdscr.nodelay(True)

debug_queue = {}
def debug(dq: dict):
    for k, v in dq.items():
        print("{}: {}".format(k,v))

def paint_windows(windows: list):
    progression = ['#', '.','+','$','0','%']
    for i, w in enumerate(windows):
        w.bkgd(progression[i])

def chain_refresh(windows: list):
    for win in windows:
        win.refresh()

def debug_sub_wins(windows: list):
    for win in windows:
        debug_queue.update({win.__str__(): win.getmaxyx()})
 
# main loop
def main(stdscr):
    rows, cols = stdscr.getmaxyx()
    
    # ALLOC = tuple(cols (x) , rows (y))
    TOP_A = (cols, int(rows * .1))
    BOT_A = (cols, int(rows * .3))
    y = (rows - (TOP_A[1] + BOT_A[1]))
    M_LEFT_A = (int(cols * .6), y)
    x = cols - M_LEFT_A[0]
    M_RIGHT_A = (x, y)

    t_banner = curses.newwin(TOP_A[1], TOP_A[0],0,0)
    mid_left = curses.newwin(M_LEFT_A[1], M_LEFT_A[0], TOP_A[1], 0)
    mid_right = curses.newwin(M_RIGHT_A[1], M_RIGHT_A[0], TOP_A[1], M_LEFT_A[0])
    start_loc = TOP_A[1] + M_LEFT_A[1]
    b_banner = curses.newwin(BOT_A[1], BOT_A[0],start_loc,0)
    sub_windows = [t_banner, mid_left, mid_right, b_banner]
    
    paint_windows(sub_windows)
    chain_refresh(sub_windows)
    debug_queue.update({'t_banner': t_banner.getmaxyx()})
    debug_sub_wins(sub_windows)

    while True:
        stdscr.refresh()
        c = stdscr.getch()
        if c == ord('q'):
            break
wrapper(main)

# shutdown functions
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()

if DEBUG:
    debug(debug_queue)

