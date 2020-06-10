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
# stdscr.nodelay(True)

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
    stdscr.clear()
    stdscr.refresh()
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
            stdscr.clear()
            stdscr.refresh()
            break
        paint_windows(sub_windows)
        chain_refresh(sub_windows)


def menu_view(rows:int, cols:int):
    stdscr.clear()
    stdscr.refresh()
    options = ['Multiplex', 'Quote', 'News', 'Plot']
    width = 0
    for o in options:
        if len(o) > width:
            width = len(o)

    width += 2
    length = len(options) + 2
    
    start_x = int((cols * .5) - (width))
    start_y = int((rows * .5) - (length))
    header = curses.newwin(3, width, start_y - 3, start_x)
    menu = curses.newwin(length, width, start_y, start_x)
    sub_windows = [menu, header]
    paint_windows(sub_windows)
    header.addstr(1, 1, "MENU")
    for i, o in enumerate(options):
        menu.addstr(1 + i, 1, o)
    menu.addstr(1, 1, options[0].upper())
    chain_refresh(sub_windows)
    cursor_x = start_x + 1
    cursor_y = start_y + 1
    stdscr.move(cursor_y, cursor_x)
    stdscr.refresh()
    
    while True:
        stdscr.refresh()
        c = stdscr.getch()
        if c == ord('q'):
            break
        elif c == ord('k'):
            if (cursor_y > start_y + 1):
                cursor_y -= 1
        elif c == ord('j'):
            if (cursor_y < start_y + length -2):
                cursor_y += 1
        elif c == ord('e'):
            if cursor_y == start_y + 2:
                composite_view(rows, cols)
        stdscr.move(cursor_y, cursor_x)
        for i, o in enumerate(options):
            if cursor_y - (start_y+1) == i:
                menu.addstr(1 + i, 1, o.upper())
            else:
                menu.addstr(1 + i, 1, o)
        paint_windows(sub_windows)
        chain_refresh(sub_windows)


# main loop
def main(stdscr):
    rows, cols = stdscr.getmaxyx()
    # composite_view(rows, cols)
    menu_view(rows, cols)
    
wrapper(main)

# shutdown functions
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()

if DEBUG:
    debug(debug_queue)

