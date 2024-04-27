# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "matplotlib",
# ]
# ///
from itertools import chain
import matplotlib.pyplot as plt
import matplotlib.patches as patches


default_colors = [
    # r, g, b, a
    [92, 192, 98, 0.5],  # Green with 50% transparency
    [90, 155, 212, 0.5],  # Blue with 50% transparency
    [246, 236, 86, 0.6],  # Yellow with 60% transparency
    [241, 90, 96, 0.4],  # Red with 40% transparency
    [255, 117, 0, 0.3],  # Orange with 30% transparency
    [82, 82, 190, 0.2],  # Indigo with 20% transparency
]

# Normalize RGB color values to 0.0-1.0 range and leave alpha values unchanged
default_colors = [
    [r / 255.0, g / 255.0, b / 255.0, a] for r, g, b, a in default_colors
]


def draw_ellipse(
    ax,
    x,
    y,
    w,
    h,
    a,
    fillcolor,
):
    e = patches.Ellipse(xy=(x, y), width=w, height=h, angle=a, color=fillcolor)
    ax.add_patch(e)


def draw_text(
    ax,
    x,
    y,
    text,
    color=[0, 0, 0, 1],
    fontsize=14,
    ha="center",
    va="center",
):
    ax.text(
        x,
        y,
        text,
        horizontalalignment=ha,
        verticalalignment=va,
        fontsize=fontsize,
        color="black",
    )


def draw_annotate(
    ax,
    x,
    y,
    textx,
    texty,
    text,
    color=[0, 0, 0, 1],
    arrowcolor=[0, 0, 0, 0.3],
):
    """ """
    plt.annotate(
        text,
        xy=(x, y),
        xytext=(textx, texty),
        arrowprops=dict(color=arrowcolor, shrink=0, width=0.5, headwidth=8),
        fontsize=14,
        color=color,
        xycoords="data",
        textcoords="data",
        horizontalalignment='center',
        verticalalignment='center',
    )


def get_labels(data, fill=["number"]):
    """
    Compute labels for a Venn diagram given several sets.

    Given a list of sets, `get_labels` returns a dictionary where each key is a
    string representation of intersections and differences of these sets and the
    corresponding value is a depiction of the size (or other properties) of those
    set relationships, based on the `fill` parameters provided.

    Parameters
    ----------
    data : list of set, list of lists, or list of other iterable objects
        A list containing sets (or other iterable objects that can be converted
        to sets) whose relationships (like intersection, difference) will be
        represented in the labels of the Venn diagram.
    fill : list of str, optional
        A list of strings that determines what information the labels will show.
        Valid options are:
        - "number": the cardinality of the set (number of elements)
        - "logic": a string representation of the logical relationship
          (binary indicator) corresponding to that set
        - "percent": the percentage of elements in regards to the total number
          of unique elements across all sets.

    Returns
    -------
    labels : dict of (str, str)
        A dictionary where each key is a binary string that uniquely identifies
        a subset formed by intersection and/or difference of the original sets,
        and each value is a label for that subset containing information based on
        the `fill` options.

    Examples
    --------
    Getting the count of elements in the subsets given sets sampled from range objects:

    >>> set_a = set(range(10))
    >>> set_b = set(range(5, 15))
    >>> set_c = set(range(3, 8))
    >>> get_labels([set_a, set_b, set_c], fill=["number"])
    {'001': '0',   # Elements unique to set_c
     '010': '5',   # Elements unique to set_b
     '011': '0',   # Elements common to set_b and set_c but not in set_a
     '100': '3',   # Elements unique to set_a
     '101': '2',   # ...
     '110': '2',
     '111': '3'}   # Elements present in all three sets (set_a, set_b, set_c)

    Getting logical and numerical labels:

    >>> get_labels([set_a, set_b, set_c], fill=["logic", "number"])
    {'001': '001: 0', '010': '010: 5', '011': '011: 0', ... }

    Including percentages in the labels:

    >>> get_labels([set_a, set_b, set_c], fill=["number", "percent"])
    {'001': '0 (0.0%)', '010': '5 (22.7%)', '011': '0 (0.0%)', ... }

    Notes
    -----
    Each key in the output dictionary labels corresponds to a string of binary
    digits where '1' at position i means that the i-th input set in the `data`
    list is included in that group, and '0' means it is not. The length of the
    binary string is equal to the number of sets provided in `data`. For example,
    in the context of 3 input sets, the key '101' indicates elements that are
    in the first and third set but not in the second.

    See Also
    --------
    set.intersection : Method to calculate intersection of two or more sets.
    set.difference : Method to calculate the difference between two or more sets.
    """
    N = len(data)
    sets_data = [set(data[i]) for i in range(N)]  # sets for separate groups
    s_all = set(chain(*data))  # union of all sets

    # bin(3) --> '0b11', so bin(3).split('0b')[-1] will remove "0b"
    set_collections = {}
    for n in range(1, 2**N):
        key = bin(n).split('0b')[-1].zfill(N)
        value = s_all.copy()
        sets_for_intersection = [
            sets_data[i] for i in range(N) if key[i] == '1'
        ]
        sets_for_difference = [sets_data[i] for i in range(N) if key[i] == '0']
        for s in sets_for_intersection:
            value = value & s
        for s in sets_for_difference:
            value = value - s
        set_collections[key] = value

    labels = {k: "" for k in set_collections}

    if "logic" in fill:
        for k in set_collections:
            labels[k] = k + ": "

    if "number" in fill:
        for k in set_collections:
            labels[k] += str(len(set_collections[k]))

    if "percent" in fill:
        data_size = len(s_all)
        for k in set_collections:
            labels[k] += "(%.1f%%)" % (
                100.0 * len(set_collections[k]) / data_size
            )

    return labels


def venn2(labels, names=['A', 'B'], **options):
    """
    Plots a 2-set Venn diagram.

    Parameters
    ----------
    labels : dict[str, str]
        A label dict where keys are identified via binary codes ('01', '10', '11').
        A valid set could look like: {'01': 'text 1', '10': 'text 2', '11': 'text 3'}.
        Unmentioned codes are considered as ''.
    names : list[str]
        Group names.
    more :
        Colors, figsize, dpi, fontsize

    Returns
    -------
    tuple
        A tuple containing pyplot Figure and AxesSubplot object.
    """
    colors = options.get('colors', [default_colors[i] for i in range(2)])
    figsize = options.get('figsize', (9, 7))
    dpi = options.get('dpi', 96)
    fontsize = options.get('fontsize', 14)

    fig = plt.figure(0, figsize=figsize, dpi=dpi)
    ax = fig.add_subplot(111, aspect='equal')
    ax.set_axis_off()
    ax.set_ylim(bottom=0.0, top=0.7)
    ax.set_xlim(left=0.0, right=1.0)

    # body
    draw_ellipse(ax, 0.375, 0.3, 0.5, 0.5, 0.0, colors[0])
    draw_ellipse(ax, 0.625, 0.3, 0.5, 0.5, 0.0, colors[1])
    draw_text(ax, 0.74, 0.30, labels.get('01', ''), fontsize=fontsize)
    draw_text(ax, 0.26, 0.30, labels.get('10', ''), fontsize=fontsize)
    draw_text(ax, 0.50, 0.30, labels.get('11', ''), fontsize=fontsize)

    # legend
    draw_text(
        ax,
        0.20,
        0.56,
        names[0],
        colors[0],
        fontsize=fontsize,
        ha="right",
        va="bottom",
    )
    draw_text(
        ax,
        0.80,
        0.56,
        names[1],
        colors[1],
        fontsize=fontsize,
        ha="left",
        va="bottom",
    )
    leg = ax.legend(
        names, loc='center left', bbox_to_anchor=(1.0, 0.5), fancybox=True
    )
    leg.get_frame().set_alpha(0.5)

    return fig, ax


def venn3(labels, names=['A', 'B', 'C'], **options):
    """
    plots a 3-set Venn diagram

    @type labels: dict[str, str]
    @type names: list[str]
    @rtype: (Figure, AxesSubplot)

    input
      labels: a label dict where keys are identified via binary codes ('001', '010', '100', ...),
              hence a valid set could look like: {'001': 'text 1', '010': 'text 2', '100': 'text 3', ...}.
              unmentioned codes are considered as ''.
      names:  group names
      more:   colors, figsize, dpi, fontsize

    return
      pyplot Figure and AxesSubplot object
    """
    colors = options.get('colors', [default_colors[i] for i in range(3)])
    figsize = options.get('figsize', (9, 9))
    dpi = options.get('dpi', 96)
    fontsize = options.get('fontsize', 14)

    fig = plt.figure(0, figsize=figsize, dpi=dpi)
    ax = fig.add_subplot(111, aspect='equal')
    ax.set_axis_off()
    ax.set_ylim(bottom=0.0, top=1.0)
    ax.set_xlim(left=0.0, right=1.0)

    # body
    draw_ellipse(ax, 0.333, 0.633, 0.5, 0.5, 0.0, colors[0])
    draw_ellipse(ax, 0.666, 0.633, 0.5, 0.5, 0.0, colors[1])
    draw_ellipse(ax, 0.500, 0.310, 0.5, 0.5, 0.0, colors[2])
    draw_text(ax, 0.50, 0.27, labels.get('001', ''), fontsize=fontsize)
    draw_text(ax, 0.73, 0.65, labels.get('010', ''), fontsize=fontsize)
    draw_text(ax, 0.61, 0.46, labels.get('011', ''), fontsize=fontsize)
    draw_text(ax, 0.27, 0.65, labels.get('100', ''), fontsize=fontsize)
    draw_text(ax, 0.39, 0.46, labels.get('101', ''), fontsize=fontsize)
    draw_text(ax, 0.50, 0.65, labels.get('110', ''), fontsize=fontsize)
    draw_text(ax, 0.50, 0.51, labels.get('111', ''), fontsize=fontsize)

    # legend
    draw_text(
        ax,
        0.15,
        0.87,
        names[0],
        colors[0],
        fontsize=fontsize,
        ha="right",
        va="bottom",
    )
    draw_text(
        ax,
        0.85,
        0.87,
        names[1],
        colors[1],
        fontsize=fontsize,
        ha="left",
        va="bottom",
    )
    draw_text(
        ax,
        0.50,
        0.02,
        names[2],
        colors[2],
        fontsize=fontsize,
        va="top",
    )
    leg = ax.legend(
        names,
        loc='center left',
        bbox_to_anchor=(1.0, 0.5),
        fancybox=True,
    )
    leg.get_frame().set_alpha(0.5)

    return fig, ax


def venn4(labels, names=['A', 'B', 'C', 'D'], **options):
    """
    plots a 4-set Venn diagram

    @type labels: dict[str, str]
    @type names: list[str]
    @rtype: (Figure, AxesSubplot)

    input
      labels: a label dict where keys are identified via binary codes ('0001', '0010', '0100', ...),
              hence a valid set could look like: {'0001': 'text 1', '0010': 'text 2', '0100': 'text 3', ...}.
              unmentioned codes are considered as ''.
      names:  group names
      more:   colors, figsize, dpi, fontsize

    return
      pyplot Figure and AxesSubplot object
    """
    colors = options.get('colors', [default_colors[i] for i in range(4)])
    figsize = options.get('figsize', (12, 12))
    dpi = options.get('dpi', 96)
    fontsize = options.get('fontsize', 14)

    fig = plt.figure(0, figsize=figsize, dpi=dpi)
    ax = fig.add_subplot(111, aspect='equal')
    ax.set_axis_off()
    ax.set_ylim(bottom=0.0, top=1.0)
    ax.set_xlim(left=0.0, right=1.0)

    # body
    draw_ellipse(ax, 0.350, 0.400, 0.72, 0.45, 140.0, colors[0])
    draw_ellipse(ax, 0.450, 0.500, 0.72, 0.45, 140.0, colors[1])
    draw_ellipse(ax, 0.544, 0.500, 0.72, 0.45, 40.0, colors[2])
    draw_ellipse(ax, 0.644, 0.400, 0.72, 0.45, 40.0, colors[3])
    draw_text(ax, 0.85, 0.42, labels.get('0001', ''), fontsize=fontsize)
    draw_text(ax, 0.68, 0.72, labels.get('0010', ''), fontsize=fontsize)
    draw_text(ax, 0.77, 0.59, labels.get('0011', ''), fontsize=fontsize)
    draw_text(ax, 0.32, 0.72, labels.get('0100', ''), fontsize=fontsize)
    draw_text(ax, 0.71, 0.30, labels.get('0101', ''), fontsize=fontsize)
    draw_text(ax, 0.50, 0.66, labels.get('0110', ''), fontsize=fontsize)
    draw_text(ax, 0.65, 0.50, labels.get('0111', ''), fontsize=fontsize)
    draw_text(ax, 0.14, 0.42, labels.get('1000', ''), fontsize=fontsize)
    draw_text(ax, 0.50, 0.17, labels.get('1001', ''), fontsize=fontsize)
    draw_text(ax, 0.29, 0.30, labels.get('1010', ''), fontsize=fontsize)
    draw_text(ax, 0.39, 0.24, labels.get('1011', ''), fontsize=fontsize)
    draw_text(ax, 0.23, 0.59, labels.get('1100', ''), fontsize=fontsize)
    draw_text(ax, 0.61, 0.24, labels.get('1101', ''), fontsize=fontsize)
    draw_text(ax, 0.35, 0.50, labels.get('1110', ''), fontsize=fontsize)
    draw_text(ax, 0.50, 0.38, labels.get('1111', ''), fontsize=fontsize)

    # legend
    draw_text(
        ax, 0.13, 0.18, names[0], colors[0], fontsize=fontsize, ha="right"
    )
    draw_text(
        ax,
        0.18,
        0.83,
        names[1],
        colors[1],
        fontsize=fontsize,
        ha="right",
        va="bottom",
    )
    draw_text(
        ax,
        0.82,
        0.83,
        names[2],
        colors[2],
        fontsize=fontsize,
        ha="left",
        va="bottom",
    )
    draw_text(
        ax,
        0.87,
        0.18,
        names[3],
        colors[3],
        fontsize=fontsize,
        ha="left",
        va="top",
    )
    leg = ax.legend(
        names, loc='center left', bbox_to_anchor=(1.0, 0.5), fancybox=True
    )
    leg.get_frame().set_alpha(0.5)

    return fig, ax


def cli():
    import argparse

    parser = argparse.ArgumentParser()

    # parser.add_argument(
    #     "-h",
    #     "--help",
    #     type=bool,
    #     action="store",
    #     default=False,
    # )
    #
    parser.add_argument(
        "-q",
        "--no-show",
        type=bool,
        action="store",
        default=False,
        help="Do not show the plot.",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Output file path. eg. venn.png",
    )

    parser.add_argument(
        "--fill",
        type=list,
        default=["number"],
        help="Fill options: number, logic, percent",
        choices=["number", "logic", "percent"],
    )

    parser.add_argument(
        "-n",
        "--name",
        type=str,
        action="append",
        help="Group names, use multiple times for multiple groups. eg. -n 'A' -n 'B'",
    )

    parser.add_argument(
        "-d",
        "--data",
        type=str,
        action="append",
        help="Data for the Venn diagram. Use multiple times for multiple sets. eg. -d '1 2 3'",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = cli()

    data = args.data
    fill = args.fill
    names = args.name
    out = args.output
    no_show = args.no_show

    nobjects = len(data)
    if nobjects > 4:
        raise ValueError("Only up to 4 sets are supported")

    labels = get_labels(
        data=data,
        fill=fill,
    )

    if nobjects == 2:
        fig, ax = venn2(labels, names=names)
    elif nobjects == 3:
        fig, ax = venn3(labels, names=names)
    elif nobjects == 4:
        fig, ax = venn4(labels, names=names)

    if out:
        plt.savefig(out, bbox_inches='tight')

    if not no_show:
        plt.show()
