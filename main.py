import curses
from curses import wrapper
import pprint

DEBUG = True

# rows = y
# cols = x
# stdscr.curses_func(y, x) 

# curses setup
stdscr = curses.initscr()
curses.start_color()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
stdscr.nodelay(True)

debug_queue = {}
def debug(dq: dict):
    for k, v in dq.items():
        print("{}: {}".format(k,v))

def paint_windows(windows: list):
    for i, w in enumerate(windows):
        w.border()

def chain_refresh(windows: list):
    for win in windows:
        win.refresh()

def debug_sub_wins(windows: list):
    for win in windows:
        debug_queue.update({win.__str__(): win.getmaxyx()})

def composite_view(rows:int, cols:int):
    
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

def menu_view(rows:int, cols:int):
    options = ['Multiplex', 'Quote', 'News', 'Plot']
    width = 0
    for o in options:
        if len(o) > width:
            width = len(o)

    width += 2
    length = len(options) + 2
    
    start_x = int((cols * .5) - (width))
    start_y = int((rows * .5) - (length))
    menu = curses.newwin(length, width, start_y, start_x)
    sub_windows = []
    sub_windows.append(menu)
    paint_windows(sub_windows)
    for i, o in enumerate(options):
        menu.addstr(1 + i, 1, o)
    chain_refresh(sub_windows)

# main loop
def main(stdscr):
    rows, cols = stdscr.getmaxyx()
    # composite_view(rows, cols)
    menu_view(rows, cols)
    
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

