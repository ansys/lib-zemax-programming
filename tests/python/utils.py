# Copyright (C) 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np


def make_subplots_in_horizontal(figs: dict):
    cols = len(figs)
    whole_fig = make_subplots(rows=1, cols=cols, subplot_titles=tuple(figs.keys()))
    for i, title in enumerate(figs):
        whole_fig.add_trace(figs[title], row=1, col=i + 1)
    whole_fig.update_xaxes(scaleanchor="x", scaleratio=1)
    whole_fig.update_yaxes(scaleanchor="x", scaleratio=1)
    whole_fig.update_layout(
        go.Layout(scene=dict(aspectmode="data")), coloraxis={"colorscale": "jet"}
    )
    return whole_fig


def map_infos(dataset: dict):
    result = {"Name": [], "Max": [], "Min": [], "rms": [], "pv": []}
    for item in dataset:
        result["Name"].append(item)
        result["Max"].append(np.nanmax(dataset[item]))
        result["Min"].append(np.nanmin(dataset[item]))
        result["rms"].append(np.nanmean(dataset[item] ** 2) ** 0.5)
        result["pv"].append(np.nanmax(dataset[item]) - np.nanmin(dataset[item]))
    result = pd.DataFrame.from_dict(result)
    return result


def convert_mf_to_list(mf_file):
    with open(mf_file, 'r', encoding='utf-16-le') as f:
        data = f.readlines()

    _, *data = data
    return [row.split() for row in data]


if __name__ == "__main__":
    pass
