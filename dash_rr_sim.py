# -*- coding: utf-8 -*-
# @Time : 18/03/2024 7:52 pm
# @Author : trembles
# @File : dash_rr_sim.py


import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def main():
    st.title("Risk reward simulator")

    with st.sidebar:
        st.header("Parameters")
        st.account_size  = st.number_input("Starting account size. [$]", value=100000)
        st.brokerage = st.number_input("Commision per round trip trade. [$]", value=5)
        st.tick_value = st.number_input("Minimum tick value. [$]", value=5)
        st.write("Trading metrics")
        st.win_rate  = st.slider('Win Rate', 0, 100, 50,1)
        st.win_in_ticks  = st.number_input("Average win in ticks.", value=20)
        st.loss_in_ticks  = st.number_input("Average loss in ticks.", value=10)
        st.write("Tests")
        st.total_trades = st.number_input("Trades per test", value=100 )
        st.total_sims = st.number_input("Simnulations to run", value=100 )

    sim_result = []
    for i in range(st.total_sims):
        equity = st.account_size
        account_value = [equity]
        win_trade = st.win_in_ticks * st.tick_value - st.brokerage
        loss_trade = st.loss_in_ticks * -st.tick_value - st.brokerage

        # below creating an array of length 'total_trades' containing random numbers between 1 and 100
        outcomes = list(np.round(np.random.uniform(1, 101, st.total_trades), 2))
        for i in range(len(outcomes)):
            trade = outcomes[i]
            win = trade <= st.win_rate
            profit = win_trade if win else loss_trade
            equity += profit
            account_value.append(equity)

        sim_result.append(account_value)

    df = pd.DataFrame(sim_result)  # Convert to DataFrame

    # get average of all simulations
    df.loc['Average'] = df.iloc[:, :].mean()

    df2 = pd.DataFrame.transpose(df)

    plt_txt = f'WR: {st.win_rate}%, Win: {st.win_in_ticks} [ticks], Loss: {st.loss_in_ticks} [ticks], simulations: {st.total_sims} \n' \
              f'Brokerage per round trip ${st.brokerage} \n' \
              f'Portfolio Average: {round(df2["Average"].iloc[-1] - st.account_size, 1)}'

    st.write(f'WR: {st.win_rate}%, Win: {st.win_in_ticks} [ticks], Loss: {st.loss_in_ticks} [ticks], simulations: {st.total_sims}')
    st.write(f'Brokerage per round trip ${st.brokerage}')
    st.write(f'Portfolio Average return over {st.total_trades} trades: ${round(df2["Average"].iloc[-1] - st.account_size, 1)}')


    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    ax.plot(df2, alpha=0.5)
    ax.plot(df2['Average'], color='k', linewidth=2, label='Average')
    ax.ticklabel_format(useOffset=False, style='plain')
    ax.set_title(f'Monte Carlo simulation. {st.total_sims} trials')

    ax.set_xlabel('Trades')
    ax.set_ylabel('PnL')

    plt.grid()

    st.pyplot(fig)

if __name__ == "__main__":
    st.set_page_config(
        page_title="Risk reward simulator", page_icon=":chart_with_upwards_trend:"
    )
    main()
    with st.sidebar:
        st.markdown("Made by Github\Trembles")