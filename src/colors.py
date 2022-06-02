"""
Simple Module for Terminal Colors
credits: Atzur & Woofina
https://github.com/atzuur
https://github.com/WoofinaS
"""

from re import findall
from os import system
system('')

# & == method
# @ == foreground
# $ == background

codes = { '&RESET'    : '\33[0m',
          '&BOLD'     : '\33[1m',
          '&ITALIC'   : '\33[3m',
          '&URL'      : '\33[4m',
          '&BLINK'    : '\33[5m',
          '&ALTBLINK' : '\33[6m',
          '&SELECTED' : '\33[7m',
          '&INVISIBLE': '\33[8m',
          '&STRIKE'   : '\33[9m',
          '@RGB'      : '\33[38;2;',
          '@BLACK'    : '\33[30m',
          '@RED'      : '\33[31m',
          '@GREEN'    : '\33[32m',
          '@YELLOW'   : '\33[33m',
          '@BLUE'     : '\33[34m',
          '@VIOLET'   : '\33[35m',
          '@BEIGE'    : '\33[36m',
          '@WHITE'    : '\33[37m',
          '@GREY'     : '\33[90m',
          '@LRED'     : '\33[91m',
          '@LGREEN'   : '\33[92m',
          '@LYELLOW'  : '\33[93m',
          '@LBLUE'    : '\33[94m',
          '@LVIOLET'  : '\33[95m',
          '@LBEIGE'   : '\33[96m',
          '@LWHITE'   : '\33[97m',
          '$RGB'      : '\33[48;2;',
          '$BLACK'    : '\33[40m',
          '$RED'      : '\33[41m',
          '$GREEN'    : '\33[42m',
          '$YELLOW'   : '\33[43m',
          '$BLUE'     : '\33[44m',
          '$VIOLET'   : '\33[45m',
          '$BEIGE'    : '\33[46m',
          '$WHITE'    : '\33[47m',
          '$GREY'     : '\33[100m',
          '$LRED'     : '\33[101m',
          '$LGREEN'   : '\33[102m',
          '$LYELLOW'  : '\33[103m',
          '$LBLUE'    : '\33[104m',
          '$LVIOLET'  : '\33[105m',
          '$LBEIGE'   : '\33[106m',
          '$LWHITE'   : '\33[107m' }


def printc (text: str):
    print(formatc(text))

def inputc (text: str):
    return input(formatc(text))

def formatc (text: str):

    formatted = text

    for key in list(codes):
        if key in formatted:
            formatted = formatted.replace(key, codes[key])

    formatted = formatted + codes['&RESET']

    return formatted


def print_success (text     : str,
                   prefix   : str = 'SUCCESS',
                   isolate  : bool = False,
                   noprefix : bool = False):

    out = formatc(f'@LGREEN{text}')

    if not noprefix:
        out = formatc(f'@WHITE[&BOLD@GREEN{prefix}&RESET@WHITE] >>> ') + out

    if isolate:
        out = '\n' + out + '\n'

    print(out)


def print_error (text     : str,
                 prefix   : str = 'ERROR',
                 isolate  : bool = False,
                 noprefix : bool = False):

    out = formatc(f'@LRED{text}')

    if not noprefix:
        out = formatc(f'@WHITE[&BOLD@RED{prefix}&RESET@WHITE] >>>') + out

    if isolate:
        out = '\n' + out + '\n'

    print(out)


def print_warning (text     : str,
                   prefix   : str = 'WARNING',
                   isolate  : bool = False,
                   noprefix : bool = False):

    out = formatc(f'@YELLOW{text}')

    if not noprefix:
        out = formatc(f'@WHITE[&BOLD@YELLOW{prefix}&RESET@WHITE] >>>') + out

    if isolate:
        out = '\n' + out + '\n'

    print(out)


def print_rainbow (text      : str | list | tuple,
                   density   : int  =  1,
                   start     : str  = 'RED',
                   rainbowFG : bool = True,  rainbowBG     : bool =  False,
                   staticFG  : bool = False, staticFGcolor : str  = 'WHITE',
                   staticBG  : bool = False, staticBGcolor : str  = 'BLACK'):

    Rcolors = ['RED', 'YELLOW', 'GREEN', 'LBLUE', 'BLUE', 'VIOLET']

    if rainbowFG and rainbowBG:
        colors = list(map(lambda color: f'@{color}' + f'${color}', Rcolors))

    elif rainbowFG:
        colors = list(map(lambda color: f'@{color}', Rcolors))

    elif rainbowBG:
        colors = list(map(lambda color: f'${color}', Rcolors))

    if type(text) is str:
        rText = findall(f'.{{1,{density}}}', f'{text}')

    elif type(text) is list or type(text) is tuple:
        rText = text

    else: raise TypeError(f'Invalid input type: {type(text)}')

    merged = []
    x = Rcolors.index(start) - 1
    for i in range(0, len(rText)): 
        x += 1
        if x > len(colors) - 1: x = 0

        merged.append(colors[x])
        merged.append(rText[i])

    out = ''.join(map(str, merged))

    if staticFG:
        fgCol = f'@{staticFGcolor}'
        out   = fgCol + out
    if staticBG:
        bgCol = f'${staticBGcolor}'
        out   = bgCol + out

    return printc(out)


def rgb (text: str, r = 0, g = 0, b = 0) -> str:
    return f'\33[38;2;{r};{g};{b}m' + text + codes['&RESET']


def syntax_hl (text: str):

    r = codes['&RESET']

    parens = ('(', ')', '{', '}', '[', ']')

    ops = ('+', '-', '/', '\\',
           '%', '=', '&', '$', 
           '@', '?', '|', '<', 
           '>', '*', '!', '~', '^')

    delims = (',', '.', ':', ';')

    dflt = '\033[38;5;189m' # default text color

    fmt = lambda char, *rgbvals: rgb(char, *rgbvals) + r

    hl = list(text)

    for idx, char in enumerate(hl):

        if char.isdigit():   hl[idx] = fmt(char, 255, 168, 227)

        elif char in parens: hl[idx] = fmt(char, 140, 190, 178)

        elif char in ops:    hl[idx] = fmt(char, 195, 117, 243)

        elif char in delims: hl[idx] = fmt(char, 156, 191, 255)

        else: hl[idx] = dflt + char + r

    return ''.join(hl) + r



### WIP ###

def avg (vals: tuple):

    total = 0

    for val in vals:
        total += val

    return total / len(vals)


def interpolate (minv: int, maxv: int, steps: int) -> tuple:

    if minv == maxv or maxv - minv < 1: # if minv is equal to maxv
        return (maxv,) * (steps + 1)

    if minv > maxv: # swap minv and maxv if they're in the wrong order
        minv, maxv = maxv, minv

    og_minv, og_maxv = minv, maxv

    between = tuple(range(minv, maxv + 1))

    result = between[::int(len(between) / steps)]

    if og_minv > og_maxv: list(result).reverse()

    if len(result[1:-1]) < 1:
        return (og_maxv,) * (steps + 1)

    else:
        return result[1:-1]


def gen_gradient (first: tuple, second: tuple, factor: int = 2):

    f, s, t = [interpolate(f, s, factor) for f, s in zip(first, second)]

    ordered = [(r, g, b) for r, g, b in zip(f, s, t)]

    # split ordered list into chunks of len(first)
    l = len(first)
    splt = [ordered[n:n+l] for n in range(0, len(ordered), l)][0]

    if avg(first) > avg(second):
        splt.reverse()

    out = [ first,
            *splt,
            second ]

    return out