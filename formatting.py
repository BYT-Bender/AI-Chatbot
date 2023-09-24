class TextStyle:
    fg = {
        'k': '\033[30m', # Black
        'K': '\033[90m', # Bright black
        'r': '\033[31m', # Red
        'R': '\033[91m', # Bright red
        'g': '\033[32m', # Green
        'G': '\033[92m', # Bright green
        'y': '\033[33m', # Yellow
        'Y': '\033[93m', # Bright yellow
        'b': '\033[34m', # Blue
        'B': '\033[94m', # Bright blue
        'm': '\033[35m', # Magenta
        'M': '\033[95m', # Bright magenta
        'c': '\033[36m', # Cyan
        'C': '\033[96m', # Bright cyan
        'w': '\033[37m', # White
        'W': '\033[97m', # Bright white
        'x': '\033[0m', # Reset
    }

    style = {
        'b': '\033[1m', # Bold
        'B': '\033[21m', # /Bold
        'i': '\033[3m', # Italic
        'I': '\033[23m', # /Italic
        'u': '\033[4m', # Underline
        'U': '\033[24m', # /Underline
        's': '\033[9m', # Strikethrough
        'S': '\033[29m', # /Strikethrough
        'v': '\033[7m', # Inverse
        'V': '\033[27m', # /Inverse
    }