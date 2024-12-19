import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pyberries as pyb


def plot_datapoints_and_mean(df, ax, dsList, x='', y='', hue='Group', revert_y_axis: bool = True, **kwargs):
    df = df[[hue, x, y]].astype({y: 'category', hue: 'category'})
    ax = sns.pointplot(data=df, x=x, y=y, hue=hue, hue_order=df[hue].unique(),
                       join=False, dodge=.8-.8/len(dsList), markers="d", scale=.75, errorbar=None, ax=ax)
    ax = pyb.plots.stripplot(df, x=x, y=y, hue=hue, alpha=.15, dodge=True, zorder=1, legend=False, ax=ax, **kwargs)
    if not ax.get_legend() is None:
        ax.get_legend().set_title("")
    if revert_y_axis:
        plt.gca().invert_yaxis()
    return ax


def plot_heatmap(df, ax, revert_y_axis: bool = False, **kwargs):
    ax = pyb.plots.histplot(df, cbar=True, ax=ax, **kwargs)
    if revert_y_axis:
        plt.gca().invert_yaxis()
    return ax


def plot_timeseries(df, ax, x='', y='', hue='Group', **kwargs):
    ax = pyb.plots.scatterplot(df, x=x, y=y, hue=hue, ax=ax, **kwargs)
    ax = sns.lineplot(data=df, x=x, y=f'{y}_movmean', hue=hue, legend=False, ax=ax)
    return ax


def plot_boxenplot(df, ax, log: bool = False, **kwargs):
    ax = pyb.plots.boxenplot(df, dodge=True, ax=ax, **kwargs)
    if log:
        plt.yscale('log')
    return ax


def plot_histogram_fit(df_in, hist, model, ax, fit_results: dict, **kwargs):
    groupby = kwargs.get('hue', 'Group')
    fit_df = pd.DataFrame(columns=['x', 'Fit', groupby])
    for grp, data in hist.groupby(groupby, sort=False):
        x_model = np.linspace(data.bins.iloc[0], data.bins.iloc[-1], 300)
        df = pd.DataFrame({'x': x_model, 'Fit': model(x_model, *fit_results[grp]), groupby: grp})
        fit_df = pd.concat([fit_df, df], axis=0)
    ax = pyb.plots.histplot(df_in, ax=ax, **kwargs)
    ax = sns.lineplot(data=fit_df, x='x', y='Fit', hue=groupby, legend=False, ax=ax, linestyle='dashed')


def plot_line_fit(df_in, model, ax, fit_results: dict, **kwargs):
    groupby = kwargs.get('hue', 'Group')
    x = kwargs.get('x', 'Frame')
    fit_df = pd.DataFrame(columns=['x', 'Fit', groupby])
    for grp, data in df_in.groupby(groupby, sort=False):
        if grp in fit_results.keys():
            x_model = np.linspace(data[x].iloc[0], data[x].iloc[-1], 300)
            df = pd.DataFrame({'x': x_model, 'Fit': model(x_model, *fit_results[grp]), groupby: grp})
            fit_df = pd.concat([fit_df, df], axis=0)
    ax = pyb.plots.lineplot(df_in, ax=ax, **kwargs)
    ax = sns.lineplot(data=fit_df, x='x', y='Fit', hue=groupby, hue_order=fit_df[groupby].unique(),
                      legend=False, ax=ax, linestyle='dashed')


def plot_rates_summary(rates, ax, **kwargs):
    ax = pyb.plots.pointplot(rates, ax=ax, **kwargs)
    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1), labelspacing=1)


def plot_grey_lines_and_highlight(df_in, ax, color='gray', estimator=None, alpha=0.4, highlight=None, **kwargs):
    highlight_by_index = kwargs.pop('highlight_by_index', False)
    units = kwargs.get('units')
    ax = pyb.plots.lineplot(df_in, color=color, estimator=estimator, alpha=alpha, legend=False, ax=ax, **kwargs)
    df = df_in.copy()
    n_units = len(df[units].unique())
    if highlight_by_index:
        highlight = df[units].unique()[highlight]
    df = df[df[units] == highlight]
    print(f'Displaying unit {highlight} ({n_units} units available)')
    ax = sns.lineplot(data=df, x=kwargs.get('x'), y=kwargs.get('y'), color='red', legend=False)
