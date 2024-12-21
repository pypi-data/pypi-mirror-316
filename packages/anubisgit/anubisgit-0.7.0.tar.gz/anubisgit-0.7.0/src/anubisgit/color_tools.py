"""Anubis color tools"""

from matplotlib.colors import LinearSegmentedColormap, Colormap, ListedColormap


def get_color(cmap: Colormap, color_idx: int, total_keys: int) -> tuple:
    """
    Get color from a colormap based on index and total number of keys. If no
    color map is provided, defaults to white.

    Args:
        cmap (Colormap): The colormap from which to select the color.
        color_idx (int): The index of the color.
        total_keys (int): Total number of keys.

    Returns:
        tuple: The selected color from the colormap.
    """
    if isinstance(cmap, LinearSegmentedColormap):
        return cmap(int(color_idx * (cmap.N / total_keys + 1)))
    elif isinstance(cmap, ListedColormap):
        return cmap(color_idx % len(cmap.colors))
    else:
        try:
            return cmap[color_idx % len(cmap)]
        except:
            return (1.0, 1.0, 1.0)


def hex_to_rgb(color: str) -> tuple:
    """
    Translate Hexadecimal color to RGB color

    Args:
        color (str): Hex color code

    Rerurns:
        color_rgb (tuple): rgb translation
    """
    lv = len(color)
    color_rgb = tuple(int(color[i : i + lv // 3], 16) for i in range(0, lv, lv // 3))
    return color_rgb


def brighten_color(tuple_rgb, brighter=0.7):
    """

    To brighten the color, use a float valuecloser to 1

    """

    if brighter < 0:
        return tuple_rgb

    out = (
        (tuple_rgb[0] * (1 - brighter) + brighter),
        (tuple_rgb[1] * (1 - brighter) + brighter),
        (tuple_rgb[2] * (1 - brighter) + brighter),
        tuple_rgb[3],
    )

    return out
