from src.read_data.load_data import load_production, load_use_1970_2021
from src.tools.tools import get_np_from_df
from src.calc_trade.calc_trade_tools import expand_trade_to_past_and_future, get_imports_and_exports_from_net_trade, \
    get_trade_test_data, visualize_trade


def get_trade(country_specific, scaler):
    net_trade_1970_2021 = _get_net_trade_1970_2021(country_specific)
    net_trade = expand_trade_to_past_and_future(net_trade_1970_2021,
                                                scaler=scaler,
                                                first_available_year=1970,
                                                last_available_year=2021)

    imports, exports = get_imports_and_exports_from_net_trade(net_trade)

    return imports, exports


def _get_net_trade_1970_2021(country_specific):
    df_use = load_use_1970_2021(country_specific=country_specific)
    df_production = load_production(country_specific=country_specific)

    use_1970_2021 = get_np_from_df(df_use, data_split_into_categories=False)
    production_1900_2022 = get_np_from_df(df_production, data_split_into_categories=False)
    production_1970_2021 = production_1900_2022[:, 70:122]

    net_trade_1970_2021 = use_1970_2021 - production_1970_2021
    net_trade_1970_2021 = net_trade_1970_2021.transpose()

    return net_trade_1970_2021


def _test():
    country_specific = False
    production, demand, available_scrap_by_category = get_trade_test_data(country_specific)
    imports, exports = get_trade(country_specific,
                                 scaler=demand)
    trade = imports - exports

    # _visualize_trade_demand_correlation(trade, demand)

    print(f'Trade is loaded with shape: {trade.shape}')
    visualize_trade(trade, steel_type='crude')


def _visualize_trade_demand_correlation(trade, demand):
    # TODO delete / decide
    import numpy as np
    print(trade[:, :, 1].shape)
    print(demand.shape)
    r = np.array([np.corrcoef(trade[:, i, 1], demand[:, i, 1])[0, 1] for i in range(12)])
    print(np.mean(r))
    print(r)
    print(r.shape)
    present_trade = trade[70:121, :3, 1]
    present_demand = demand[70:121, :3, 1]
    years = range(1970, 2021)
    regions = ['CAZ trade', 'CAZ demand', 'CHA trade', 'CHA demand', 'EUR trade', 'EUR demand']
    colors = ['r', 'g', 'b']
    from matplotlib import pyplot as plt
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Time (y)')
    ax1.set_ylabel('Steel traded (t)')
    ax2 = ax1.twinx()
    ax2.set_ylabel('Steel demand (t)')
    for i in range(3):
        ax1.plot(years, present_trade[:, i], color=colors[i])
        ax2.plot(years, present_demand[:, i], '--', color=colors[i])
    plt.legend(regions)
    fig.tight_layout()
    plt.title('Steel demand/trade correlation?')
    plt.show()


if __name__ == '__main__':
    _test()
