#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Neural Network Figures

# The MIT License
#
# Copyright (c) 2017 Jeremie DECOCK (http://www.jdhp.org)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import matplotlib.pyplot as plt

import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from matplotlib.figure import Figure
from matplotlib.axes import Axes


def init_figure(
    size_x: int = 10,
    size_y: int = 5
) -> tuple[Figure, Axes]:
    """
    Initialize a matplotlib figure and axis.

    Parameters
    ----------
    size_x : int, optional
        Width of the figure in inches (default is 10).
    size_y : int, optional
        Height of the figure in inches (default is 5).

    Returns
    -------
    tuple[Figure, Axes]
        A tuple containing the figure and axis objects.
    """
    fig, ax = plt.subplots(figsize=(size_x, size_y))

    ax.set_axis_off()
    ax.axis('equal')
    ax.set_xlim(-10, 20)   # TODO

    return fig, ax


def draw_neuron(
    axis: Axes,
    center: tuple[float, float],
    radius: float,
    fill_color: str = 'w',
    line_color: str = 'k',
    line_width: float = 1,
    empty: bool = False,
    ag_func: str | None = None,
    tr_func: str | None = None
) -> None:
    """
    Draw a neuron (circle) on a given axis.

    Parameters
    ----------
    axis : Axes
        The matplotlib axis to draw the neuron on.
    center : tuple of float
        The (x, y) coordinates of the center of the neuron.
    radius : float
        The radius of the neuron.
    fill_color : str, optional
        The fill color of the neuron (default is 'w' for white).
    line_color : str, optional
        The color of the neuron's outline (default is 'k' for black).
    line_width : float, optional
        The width of the neuron's outline (default is 1).
    empty : bool, optional
        If True, the neuron will be drawn as an empty circle (default is False).
    ag_func : str or None, optional
        The aggregation function to draw inside the neuron (default is None).
        Options are "sum".
    tr_func : str or None, optional
        The transition function to draw inside the neuron (default is None).
        Options are "linear", "logistic", "sigmoid".

    Returns
    -------
    None
    """

    #circle = plt.Circle(center, radius, fill=True, color=fill_color, alpha=0)
    #axis.add_artist(circle)

    circle = mpatches.Circle(
        xy=center,
        radius=radius,
        fill=True,
        edgecolor=line_color,
        facecolor=fill_color
    )
    circle.set_zorder(20)  # put the circle on top
    axis.add_patch(circle)

    #circle = plt.Circle(center, radius, fill=False, color=line_color)
    #ax.add_artist(circle)

    x = center[0]
    y = center[1]

    if not empty:
        line = mlines.Line2D(
            xdata=[x, x],
            ydata=[y - radius + 0.05, y + radius - 0.05],
            lw=line_width,
            color=line_color
        )
        line.set_zorder(21)
        axis.add_line(line)

    # Agregation function ######################

    if not empty and ag_func == "sum":
        line = mlines.Line2D(
            xdata=[x - radius/4., x - 3 * radius/4., x - radius/2., x - 3. * radius/4., x - radius/4.],
            ydata=[y + radius/4., y + radius/4., y, y - radius/4., y - radius/4.],
            lw=line_width,
            color=line_color
        )
        line.set_zorder(21)
        axis.add_line(line)

    # Transition function ######################

    if not empty and tr_func == "linear":
        line = mlines.Line2D(
            xdata=[x + radius/4., x + 3. * radius/4.],
            ydata=[y - radius/4., y + radius/4.],
            lw=line_width,
            color=line_color
        )
        line.set_zorder(21)
        axis.add_line(line)
    elif not empty and tr_func == "logistic":
        line = mlines.Line2D(
            xdata=[x + radius/4., x + radius/2., x + radius/2., x + 3. * radius/4.],
            ydata=[y - radius/4., y - radius/4., y + radius/4., y + radius/4.],
            lw=line_width,
            color=line_color
        )
        line.set_zorder(21)
        axis.add_line(line)
    elif not empty and tr_func == "sigmoid":
        arc1 = mpatches.Arc(
            xy=(x + 1. * radius/4., y),
            width=radius/2.,
            height=radius/2.,
            angle=0,
            theta1=-90,
            theta2=0,
            ec=line_color,
            lw=line_width,
            fill=False
        )
        arc2 = mpatches.Arc(
            xy=(x + 3. * radius/4., y),
            width=radius/2.,
            height=radius/2.,
            angle=0,
            theta1=90,
            theta2=180,
            ec=line_color,
            lw=line_width,
            fill=False
        )

        arc1.set_zorder(21)
        arc2.set_zorder(21)

        axis.add_patch(arc1)
        axis.add_patch(arc2)
    elif not empty and tr_func == "identity":
        plt.text(
            x=x + radius/4.,
            y=y - radius/4.,
            s="1",
            fontsize=10,   # TODO
            color=line_color,
            zorder=21
        )


def draw_synapse(
    axis: Axes,
    p1: tuple[float, float],
    p2: tuple[float, float],
    color: str = 'k',
    line_width: float = 1,
    label: str = "",
    label_position: float = 0.25,
    label_offset_y: float = 0.3,
    label_color: str = 'k',
    fontsize: int = 12
) -> None:
    """
    Draw a synapse (line) between two points on a given axis.

    Parameters
    ----------
    axis : Axes
        The matplotlib axis to draw the synapse on.
    p1 : tuple of float
        The (x, y) coordinates of the starting point.
    p2 : tuple of float
        The (x, y) coordinates of the ending point.
    color : str, optional
        The color of the line (default is 'k' for black).
    line_width : float, optional
        The width of the line (default is 1).
    label : str, optional
        The label to place near the line (default is an empty string).
    label_position : float, optional
        The position of the label along the line as a fraction of the line length (default is 0.25).
    label_offset_y : float, optional
        The vertical offset of the label from the line (default is 0.3).
    fontsize : int, optional
        The font size of the label (default is 12).

    Returns
    -------
    None
    """
    line = mlines.Line2D(
        xdata=[p1[0], p2[0]],
        ydata=[p1[1], p2[1]],
        lw=line_width,
        color=color
    )
    line.set_zorder(10)
    axis.add_line(line)

    plt.text(
        x=p1[0] + label_position * (p2[0]-p1[0]),
        y=p1[1] + label_position * (p2[1]-p1[1]) + label_offset_y,
        s=label,
        fontsize=fontsize,
        color=label_color
    )