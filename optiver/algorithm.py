
#   ALGO
## strategy works by seeing pattern in one market before the other 
## still needs normalisation from the parsed data as that makes it much more efficient
## please refactor and integrate with the trader class and normalise the data instead of directly running this as this assumes you do
## normalisation needs average and standard deviation of last few data points

def moving_avg(X, step):
    ma = np.empty(X.size)
    for i in range(X.size):
        sample = X[(i - step if i - step >= 0 else 0):i + 1]
        ma[i] = sum(sample)/sample.size
    return ma
    
if __name__ == '__main__':
    market_data = pd.read_csv('market_data.csv')
    trade_data = pd.read_csv('trades.csv')
    print(market_data.head(5))
    print(trade_data.head(5))

    market_data = market_data.to_numpy()
    trade_data = trade_data.to_numpy()

    market_data[:, 0] = [60 * (int(ts[:2]) - 11) + (int(ts[3:5]) - 43) for ts in market_data[:, 0]]

    esx_data = market_data[(market_data[:,1]) == 'ESX-FUTURE']
    sp_data = market_data[(market_data[:,1]) == 'SP-FUTURE']

    esx_close = []
    idx = 0
    for i in range(len(esx_data)):

        if esx_data[i][0] != idx:
            idx = esx_data[i][0]
            esx_close.append(esx_data[i-1])
    esx_close.append(esx_data[-1])
    esx_close = [trans[4] for trans in esx_close]

    sp_close = []
    idx = 0
    for i in range(len(sp_data)):

        if sp_data[i][0] != idx:
            idx = sp_data[i][0]
            sp_close.append(sp_data[i - 1])
    sp_close.append(sp_data[-1])
    sp_close = [trans[4] for trans in sp_close]

    min_len = min(len(sp_close), len(esx_close))

    correlation = np.corrcoef(sp_close[:min_len], esx_close[:min_len], rowvar=True)

    print(sum(sum(correlation)))

    correlations = []

    for shift in range(61):
        correlation = np.corrcoef(sp_close[:(min_len-shift)], esx_close[shift:min_len])
        correlations.append(sum(sum(correlation)))

    print(correlations)

    sp_close_np = np.array(sp_close)
    sp_close_m = sp_close_np.mean()
    sp_close_std = sp_close_np.std()
    sp_close_norm = (sp_close_np - sp_close_m) / sp_close_std

    esx_close_np = np.array(esx_close)
    esx_close_m = esx_close_np.mean()
    esx_close_std = esx_close_np.std()
    esx_close_norm = (esx_close_np - esx_close_m) / esx_close_std

    MA_TAIL = 20

    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

    # for i in range(15, 16, 5):
    #     plt.figure(int(i / 5))
    #     plt.plot(range(min_len - 9), esx_close_norm[9:min_len], 'b')
    #     plt.plot(range(min_len - 9), moving_avg(esx_close_norm, 9)[9:min_len], 'r')
    #     plt.plot(range(min_len-9), moving_avg(sp_close_norm, 15)[:min_len - 9], 'k')
    #     plt.show()
    #
    # plt.figure(2)
    # plt.plot(range(75), esx_close_norm[50 + 9: 125 + 9], 'b')
    # plt.plot(range(75), moving_avg(esx_close_norm, 9)[50 + 9:125 + 9], 'r')
    # plt.plot(range(75), moving_avg(sp_close_norm, 15)[50: 125], 'k')
    # plt.show()




    # plt.figure(1)
    # plt.plot(range(min_len), sp_close_norm[:min_len], 'r')
    # plt.plot(range(min_len), esx_close_norm[:min_len], 'b')
    # plt.show()
    # plt.figure(2)
    # plt.plot(range(min_len-9), sp_close_norm[:(min_len-9)], 'r')
    # plt.plot(range(min_len-9), esx_close_norm[9:min_len], 'b')
    # plt.show()
    # plt.figure(3)
    # plt.plot(range(min_len - 9), sp_close[:(min_len - 9)], 'r')
    # plt.plot(range(min_len - 9), esx_close[9:min_len], 'b')
    # plt.show()



    balance = 20000
    ratio = 0.9
    ACTION = 0
    esx = np.array([], dtype=float)
    sp = np.array([], dtype=float)
    esx_ma = None
    sp_ma = None
    no_stocks = 0

    trades =[(0, balance)]

    for t in range(min_len):
        esx = np.append(esx, [esx_close_norm[t]])
        sp = np.append(sp, [sp_close_norm[t]])
        esx_ma = moving_avg(esx, 9)
        sp_ma = moving_avg(sp[:-9], 15)

        if t > 15:
            esx_grad = esx_ma[t-1] - esx_ma[t-2]
            sp_grad = sp_ma[t - 10] - sp_ma[t - 11]

            if esx_grad > 0 and sp_grad > 0 and ACTION != BUY:
                ACTION = BUY
                price = no_stocks * esx[-1]
                print('BS: ', price)
                balance += price
                no_stocks = 0
                new_stocks = ratio * balance / esx[-1] * (esx_grad * 10)
                price = new_stocks * esx[-1]
                print('BL: ', price)
                balance -= price
                no_stocks += new_stocks
                print('BUY BALANCE: ', balance)
                trades.append((t, balance))

            elif esx_grad < 0 and sp_grad < 0 and ACTION != SELL:
                ACTION = SELL
                price = no_stocks * esx[-1]
                print('SL: ', price)
                balance += no_stocks * esx[-1]
                no_stocks = 0
                new_stocks = abs(ratio * balance / esx[-1] * (esx_grad * 10))
                price = new_stocks * esx[-1]
                print('SS: ', price)
                balance += price
                no_stocks -= new_stocks
                print('SELL BALANCE: ', balance)
                trades.append((t, balance))

    balance += no_stocks * esx[-1]
    no_stocks = 0
    trades.append((t, balance))

    print('END BALANCE: ', balance)

    plt.figure(9)
    plt.plot([trade[0] for trade in trades], [trade[1] for trade in trades])
    plt.show()