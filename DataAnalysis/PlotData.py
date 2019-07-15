#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 11 01:36:39 2018

@author: camkhanhdao

"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.ticker as ticker
import seaborn as sns
import CleanData

figure_path = credentials.get_path("figure_path")
month_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
              5: 'May', 6: 'June', 7: 'July', 8: 'August',
              9: 'September',  10: 'October', 11: 'November', 12: 'December'}
positions = [[0, 0], [0, 1], [1, 0], [1, 1]]
modules = ['v1', 'v2', 'v3', 'v4']
titles = ['Module 1', 'Module 2', 'Module 3', 'Module 4']

df = CleanData.main_merge()


class PlotData:

    def __init__(self, var='ic', index=0, types=1, month=6, path_name=figure_path):
        """

        :param index: int
        :param var: 'T', 'irr', 'tc', 'humc', 'ic' choose input data file
        :param types: 1: correlation plot, 2: scatter plot, 3: violin plot
        :param path_name: path to save figure
        """
        self.index = index
        self.path_name = path_name
        self.plot_name = index * 10
        self.var = var
        self.types = types
        self.month = month

    def data_frame(self):
        df_dict = {'T': 'T_index', 'irr': 'irr_index'}
        drop_dict = {'tc': ['hum', 'irr', 'T_index', 'hum_index'],
                     'humc': ['T', 'T_index', 'hum_index', 'irr'],
                     'ic': ['hum', 'irr_index', 'hum_index', 'T']}
        groupby = {'tc': 'irr_index', 'humc': 'irr_index', 'ic': 'T_index'}
        index_levels = {'ic': 'irr', 'tc': 'T', 'humc': 'hum'}
        if self.types == 1:
            correlation = df.drop(drop_dict.get(self.var), axis=1). \
                apply(lambda x: x.astype(np.float64)).groupby(groupby.get(self.var)).corr()
            correlation = correlation[correlation.index.get_level_values(1) == index_levels.get(self.var)]
            correlation.drop([index_levels.get(self.var)], axis=1, inplace=True)
            correlation.set_index(correlation.index.get_level_values(0), inplace=True)
            return correlation
        elif self.types == 2:
            data_frame = [df[df[df_dict.get(self.var)] == i].astype(np.float64) for i in range(0, 60, 10)]
            return data_frame
        elif self.types == 3:
            violin = df.set_index(df.index.month)[modules]
            violin.columns = titles
            data_frame = violin[violin.index == self.month].astype(np.float64)
            return data_frame

    def color_pick(self):
        df_plot = PlotData.data_frame(self)[self.index]
        cpick = cm.ScalarMappable(cmap=plt.get_cmap('Wistia'))
        cpick.set_array([])
        percentages = []
        for t in df_plot[self.var]:
            percentage = t / df_plot[self.var].max()
            if percentage > 1:
                percentage = 1
            if percentage < 0:
                percentage = 0
            percentages.append(percentage)

        return cpick.to_rgba(percentages)

    def scatter_plot(self):
        """
        in T scatter plot index in range(0,6)
        in irr scatter plot index in range(0,12)
        """
        suptitles = {'T': 'Open circuit voltage versus Temperature (at irradiance index = ',
                     'irr': 'Open circuit voltage versus Light intensity (at T index = '}
        xlabel = {'T': 'Temperature ' + u'$(\N{DEGREE SIGN} C)$',
                  'irr': 'Irradiance $mw/cm^2$'}
        df_plot = PlotData.data_frame(self)[self.index-1]
        fig, ax = plt.subplots(ncols=2, nrows=2, figsize=(20, 15))
        fig.suptitle(suptitles.get(self.var) + str(self.plot_name) + ')',
                     fontsize='x-large', y=0.92)

        for pos, module, title in zip(positions, modules, titles):
            ax[pos[0], pos[1]].scatter(df_plot[self.var], df_plot[module], alpha=.3,
                                       color=PlotData.color_pick(self))
            ax[pos[0], pos[1]].set_title(title, fontsize='large', y=0.92)

            model = np.polyfit(df_plot[self.var], df_plot[module], deg=1)
            x = df_plot[self.var]
            y = model[1] + model[0] * x

            ax[pos[0], pos[1]].plot(x, y, '-', color='k')
            ax[pos[0], pos[1]].set_xlabel(xlabel.get(self.var), fontsize='large')
            ax[pos[0], pos[1]].set_ylabel('Open circuit voltage $(V)$', fontsize='large')

        plt.savefig(figure_path + self.var + str(self.plot_name) + 'Wistia.png', dpi=300)

    def correlation_plot(self):

        suptitles = {'tc': 'Correlation coefficient of Open circuit voltage versus Temperature',
                     'ic': 'Correlation coefficient of Open circuit voltage versus Irradiation',
                     'humc': 'Correlation coefficient of Open circuit voltage versus R.H.'}
        xlabel = {'tc': 'Irradiation index ' + u'$mW/cm^2$',
                  'humc': 'Irradiation index ' + u'$mW/cm^2$',
                  'irr': 'Temperature '+u'$(\N{DEGREE SIGN} C)$'}
        ylim = {'tc': [-.8, .2], 'humc': [-.4,.8], 'ic': [0, 1]}

        df_correlation = PlotData.data_frame(self)
        st = sns.set_style("darkgrid", {"xtick.major.size": 3, "ytick.major.size": 3})
        sns.set_context("talk", rc={"lines.linewidth": 1.2})
        palette = sns.color_palette("deep", 4)
        markers = ['*', '^', 'o', '+']
        with sns.axes_style(style=st):
            fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(9, 7))
            fig.suptitle(suptitles.get(self.var), fontsize='medium', y=0.95)

            for module, title, cc, marker in zip(modules, titles, palette, markers):
                ax.scatter(df_correlation.index, df_correlation[module],
                           alpha=1, s=60, color=cc, marker=marker, label=module)
                ax.plot(df_correlation[module], '-', color=cc, linewidth=1.3,
                        label=module, alpha=.7)
                ax.legend(loc='best', bbox_to_anchor=(1, 1),
                          fancybox=True, fontsize='small').get_frame().set_edgecolor('white')

                ax.set_xlabel(xlabel.get(self.var), fontsize='small')
                ax.set_ylabel('correlation coefficient', fontsize='small')

                ax.tick_params(axis='y', width=1.5, labelsize='small')
                ax.tick_params(axis='x', width=1.5, labelsize='small')

                ax.spines['left'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['top'].set_visible(False)
                ax.yaxis.grid(True)

                ax.set_ylim(ylim.get(self.var)[0], ylim.get(self.var)[1])
                ax.yaxis.set_major_locator(ticker.MultipleLocator(0.2))

            plt.savefig(figure_path + self.var + 'correlation.png', dpi=300)

    def violin_plot(self):
        df_violoin = PlotData.data_frame(self)
        palette = sns.color_palette("deep", 4)
        sns.set_style("darkgrid", {"xtick.major.size": 3, "ytick.major.size": 3})
        sns.set_context("talk", rc={"lines.linewidth": 1.3})
        fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(9, 7))
        ax = sns.violinplot(data=df_violoin, palette=palette)
        ax.axhline(y=np.median(df_violoin['Module 1']), linewidth=1.3, color='#40404E',
                   linestyle=':', label='Module 1 median')
        ax.set_ylabel("Open circuit voltage $(V)$")
        ax.legend(loc='upper left')
        plt.title(month_dict.get(self.month))
        plt.savefig(figure_path + str(month_dict.get(self.month)) + ".png", dpi=300)











