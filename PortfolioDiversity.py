import bs4 as bs
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import os
import pandas as pd
import pandas_datareader.data as web
import requests

style.use('ggplot')
end=dt.date.today()
start=dt.datetime(end.year-1,end.month,end.day)

print('This program calculates a correlation coefficient matrix for the adjusted close values of given group of stocks. It can help you observe potential diversification opportunities!')
print('Please enter a portfolio, one stock ticker at a time in uppercase.\nPress enter at the prompt when you have entered your entire portfolio')
tickers=[]
ticker='TICK TOCK'

while ticker!='':
    print('Portfolio:{}'.format(tickers))
    ticker=input('Add Stock to Portfolio: ')
    if ticker=='':
        break
    else:
        try:
            #verify the ticker input exists
            web.DataReader(ticker, 'yahoo', start, end)
            tickers.append(ticker)  
        except:
            print("INCORRECT TICKER. Please enter a valid ticker for a stock in Upper case (Ex. AAPL,GOOG,TSLA)")

def compile():
    main_df = pd.DataFrame()
    for count,ticker in enumerate(tickers[:10]):
        df = web.DataReader(ticker, 'yahoo', start, end)
        #Get adj close data
        df.rename(columns = {'Adj Close':ticker}, inplace=True)
        df.drop(['Open','High','Low','Close','Volume'], 1, inplace=True)
        if main_df.empty:
            main_df=df
        else:
            main_df=main_df.join(df, how='outer')
    return main_df

def visualize(main_df):

    df_corr = main_df.corr()

    data = df_corr.values
    fig = plt.figure()
    ax=fig.add_subplot(1,1,1)
    #building colored matrix
    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)
    fig.colorbar(heatmap)    
    ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()

    column_labels = df_corr.columns
    row_labels=df_corr.index

    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)
    plt.xticks(rotation=90)
    heatmap.set_clim(-1,1)
    plt.tight_layout()
    plt.show()   
    
visualize(compile())
            
