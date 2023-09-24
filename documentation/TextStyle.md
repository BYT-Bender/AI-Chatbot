# TextStyle Class Documentation

## Overview

The `TextStyle` class is a utility class used for applying text styles and colors to text output in the terminal. It provides a set of predefined text styles and foreground colors that can be used to format text in the terminal.

## Class Members

### `fg`

This member of the `TextStyle` class defines foreground text colors. It is a dictionary where the keys are color codes, and the values are ANSI escape codes that change the text color. These codes are used to set the foreground text color in the terminal.

#### Example:

```python
fg = {
    'k': '\033[30m',  # Black
    'r': '\033[31m',  # Red
    'g': '\033[32m',  # Green
    # ...
}
```

### `style`

This member of the `TextStyle` class defines text styles such as bold, italic, underline, and more. Similar to `fg`, it is a dictionary where the keys are style codes, and the values are ANSI escape codes that apply the specified text style.

#### Example:

```python
style = {
    'b': '\033[1m',  # Bold
    'i': '\033[3m',  # Italic
    'u': '\033[4m',  # Underline
    # ...
}
```

## Usage

To apply a text style or color to a piece of text, you can use the ANSI escape codes defined in the `TextStyle` class. For example, to make text red and bold, you can use the following code:

```python
styled_text = TextStyle.fg['r'] + TextStyle.style['b'] + "This is red and bold text" + TextStyle.fg['x'] + TextStyle.style['B']
```

Here, `TextStyle.fg['r']` sets the text color to red, `TextStyle.style['b']` makes the text bold, and `TextStyle.fg['x'] + TextStyle.style['B']` resets the style to its default state.

## Supported Colors and Styles

The `TextStyle` class provides a range of colors and styles, including common foreground colors, text styles like bold and italic, and more. You can refer to the class members to see the available options.

<div style="display:flex; justify-content: left;">

Color | Alias | HEX | ANSI
--- | --- | --- |---
Black | `k` | `#000000` | `\033[30m`
Red | `r` | `#ff0000` | `\033[31m`
Green | `g` | `#00ff00` | `\033[32m`
Yellow | `y` | `#ffff00` | `\033[33m`
Blue | `b` | `#0000ff` | `\033[34m`
Magenta | `m` | `#ff00ff` | `\033[35m`
Cyan | `c` | `#00ffff` | `\033[36m`
White | `w` | `#ffffff` | `\033[37m`

Color | Alias | HEX | ANSI
--- | --- | --- |---
Bright black | `K` | `#5f5f5f` | `\033[90m`
Bright red | `R` | `#ff5f5f` | `\033[91m`
Bright green | `G` | `#5fff5f` | `\033[92m`
Bright yellow | `Y` | `#ffff5f` | `\033[93m`
Bright blue | `B` | `#5f5fff` | `\033[94m`
Bright magenta | `M` | `#ff5fff` | `\033[95m`
Bright cyan | `C` | `#5fffff` | `\033[96m`
Bright white | `W` | `#a8a8a8` | `\033[97m`

</div>

<div style="display:flex; justify-content: left;">

Style | Alias | ANSI
--- | --- | ---
Bold | `b` | `\033[1m`
Italic | `i` | `\033[3m`
Underline | `u` | `\033[4m`
Strikethrough | `s` | `\033[9m`
Inverse | `v` | `\033[7m`

Style | Alias | ANSI
--- | --- | ---
Close Bold | `B` | `\033[21m`
Close Italic | `I` | `\033[23m`
Close Underline | `U` | `\033[24m`
Close Strikethrough | `S` | `\033[29m`
Close Inverse | `V` | `\033[27m`

</div>

## Caution

Be cautious when using ANSI escape codes for text formatting, as they may not be supported by all terminal emulators. Additionally, excessive use of text styles and colors can make text hard to read or visually unpleasant, so use them sparingly and consider accessibility.
