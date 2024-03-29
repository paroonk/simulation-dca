import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import xlsxwriter.utility
from matplotlib import style
from scipy import optimize

pd.set_option('expand_frame_repr', False)
# pd.set_option('max_rows', 7)
pd.options.display.float_format = '{:.2f}'.format
# style.use('ggplot')
indicator_list = ['Avg. Cost', 'Mean', 'Std', 'SR', 'IRR', 'Dividend', 'Wealth Per Cost']

if __name__ == '__main__':
    # Excel to Pickle #
    # df_1Y = pd.read_excel('data/#Summary_1Y.xlsx', sheet_name='Result', header=[0, 1], index_col=[0])
    # df_1Y_Ind = {}
    # for ind in indicator_list:
    #     df_1Y_Ind[ind] = df_1Y[ind].melt(var_name='Algorithm', value_vars=df_1Y[ind].columns, value_name=ind)
    # df_1Y = pd.concat([df_1Y_Ind[ind] for ind in indicator_list], axis=1).T.drop_duplicates().T
    # df_1Y.to_pickle('data/Summary_1Y.pkl')
    # df_3Y = pd.read_excel('data/#Summary_3Y.xlsx', sheet_name='Result', header=[0, 1], index_col=[0])
    # df_3Y_Ind = {}
    # for ind in indicator_list:
    #     df_3Y_Ind[ind] = df_3Y[ind].melt(var_name='Algorithm', value_vars=df_3Y[ind].columns, value_name=ind)
    # df_3Y = pd.concat([df_3Y_Ind[ind] for ind in indicator_list], axis=1).T.drop_duplicates().T
    # df_3Y.to_pickle('data/Summary_3Y.pkl')
    # df_5Y = pd.read_excel('data/#Summary_5Y.xlsx', sheet_name='Result', header=[0, 1], index_col=[0])
    # df_5Y_Ind = {}
    # for ind in indicator_list:
    #     df_5Y_Ind[ind] = df_5Y[ind].melt(var_name='Algorithm', value_vars=df_5Y[ind].columns, value_name=ind)
    # df_5Y = pd.concat([df_5Y_Ind[ind] for ind in indicator_list], axis=1).T.drop_duplicates().T
    # df_5Y.to_pickle('data/Summary_5Y.pkl')

    # Import Pickle #
    df = {}
    df['1Y'] = pd.read_pickle('data/Summary_1Y.pkl')
    df['3Y'] = pd.read_pickle('data/Summary_3Y.pkl')
    df['5Y'] = pd.read_pickle('data/Summary_5Y.pkl')

    for graph in indicator_list:
        print(graph)
        fig, ax = plt.subplots(nrows=3, ncols=2, sharex=True, sharey='row', figsize=(10, 9), dpi=80)
        fig2, ax2 = plt.subplots(nrows=3, ncols=1, sharex=True, sharey='row', figsize=(10, 6), dpi=80)
        palette = plt.get_cmap('tab10')
        p_index = 0
        # bins = np.histogram(np.hstack((
        #     df['1Y'].loc[df['1Y']['Algorithm'] == 'DCA'][graph],
        #     df['3Y'].loc[df['3Y']['Algorithm'] == 'DCA'][graph],
        #     df['5Y'].loc[df['5Y']['Algorithm'] == 'DCA'][graph],
        #     df['1Y'].loc[df['1Y']['Algorithm'] == 'VA'][graph],
        #     df['3Y'].loc[df['3Y']['Algorithm'] == 'VA'][graph],
        #     df['5Y'].loc[df['5Y']['Algorithm'] == 'VA'][graph],
        # )), bins=30)[1]
        bins = 25
        for row, year in enumerate(['1Y', '3Y', '5Y']):
            for col, algorithm in enumerate(['DCA', 'VA']):
                sns.distplot(df[year].loc[df[year]['Algorithm'] == algorithm][graph], bins=bins, kde=False, label='{} {}'.format(algorithm, year), color=palette(p_index), hist_kws=dict(edgecolor='k', linewidth=1), ax=ax[row, col])
                sns.kdeplot(df[year].loc[df[year]['Algorithm'] == algorithm][graph], label='{} {}'.format(algorithm, year), linestyle='--', ax=ax2[row])
                p_index = p_index + 1
                ax[row, col].set_title('{} {}'.format(algorithm, year))
                ax[row, col].set(ylabel='Frequency')
                ax[row, col].tick_params(labelbottom=True)
                ax[row, col].yaxis.grid(alpha=0.5)
            ax2[row].set_title('{}'.format(year))
            ax2[row].tick_params(labelbottom=True)
            ax2[row].yaxis.grid(alpha=0.5)

        fig.suptitle('Distributions of {}'.format(graph), y=1.0, fontsize=17)
        fig.tight_layout()
        fig.subplots_adjust(top=0.92)
        fig2.suptitle('Normal Distribution Curves of {}'.format(graph), y=1.0, fontsize=17)
        fig2.tight_layout()
        fig2.subplots_adjust(top=0.92)
        # plt.show()
        fig.savefig('graph/{}_1.png'.format(graph))
        fig2.savefig('graph/{}_2.png'.format(graph))

    # bplot = sns.boxplot(y='Avg. Cost', x='Algorithm',
    #                     data=df_1Y,
    #                     width=0.5,
    #                     palette="colorblind")
    # bplot = sns.stripplot(y='Avg. Cost', x='Algorithm',
    #                       data=df_1Y,
    #                       jitter=True,
    #                       marker='o',
    #                       alpha=0.5,
    #                       color='black')
