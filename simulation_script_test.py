# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 14:37:25 2022

@author: pnowakowski
"""
import numpy as np
#from scipy.optimize import curve_fit
import scipy as sc
import streamlit as st
import altair as alt
import pandas as pd


st.set_page_config(layout="wide")

###############functions#####################

def make_grid(cols,rows):
    grid = [0]*cols
    for i in range(cols):
        with st.container():
            grid[i] = st.columns(rows)
    return grid

#################sidebar######################

with st.sidebar:
    st.write(
        """
        # Input Values
        """
    )
    new_players = st.number_input('# New Players (daily):', 0, 10000, 1000, 10)
    #days = st.slider('Day no:', 1, 10000, 10000, 1)
    days = st.number_input('Day no:', 1, 10000, 1000, 1)
    guild_fill = st.number_input('Guild fill no:', 1, 20, 19, 1)
    filled_guilds_players = st.number_input('% Players in guilds with 19-20 members:', 1, 100, 75, 1)
    players_guild_left_b = st.number_input('Members left in Guild:', 1, 20, 16, 1)
    tutorial_finish = st.number_input('Completed tutorial %:', 1, 100, 63, 1)
    
    # ret_d1 = st.number_input('Retention D1 %:', 1, 100, 25, 1)
    
    
    with st.expander("Retention Fit Parameters"):
        with st.container():
            mygrid = make_grid(12,1)
            r1 = mygrid[0][0].number_input('Retention D1:', 0., 100., 25.0, 0.5)
            r2 = mygrid[1][0].number_input('Retention D2:', 0., 100., 15.0, 0.5)
            r3 = mygrid[2][0].number_input('Retention D3:', 0., 100., 12.0, 0.5)
            r4 = mygrid[3][0].number_input('Retention D4:', 0., 100., 10.0, 0.5)
            r5 = mygrid[4][0].number_input('Retention D5:', 0., 100., 9.0, 0.5)
            r6 = mygrid[5][0].number_input('Retention D6:', 0., 100., 8.5, 0.5)
            r7 = mygrid[6][0].number_input('Retention D7:', 0., 100., 8.0, 0.5)
            r14 = mygrid[7][0].number_input('Retention D14:', 0., 100., 6.0, 0.1)
            r30 = mygrid[8][0].number_input('Retention D30:', 0., 100., 4.0, 0.1)
            r60 = mygrid[10][0].number_input('Retention D60:', 0., 100., 3.0, 0.1)
            r90 = mygrid[11][0].number_input('Retention D90:', 0., 100., 2.0, 0.1)
    
    with st.expander("Players in Guilds distribution"):
        with st.container():
            mygrid = make_grid(20,1)
            g1 = mygrid[0][0].number_input('Guild 1:', 0., 100., 0.4, 0.5)
            g2 = mygrid[1][0].number_input('Guild 2:', 0., 100., 1.6, 0.5)
            g3 = mygrid[2][0].number_input('Guild 3:', 0., 100., 1.2, 0.5)
            g4 = mygrid[3][0].number_input('Guild 4:', 0., 100., 0.5, 0.5)
            g5 = mygrid[4][0].number_input('Guild 5:', 0., 100., 0.4, 0.5)
            g6 = mygrid[5][0].number_input('Guild 6:', 0., 100., 0.3, 0.5)
            g7 = mygrid[6][0].number_input('Guild 7:', 0., 100., 0.6, 0.5)
            g8 = mygrid[7][0].number_input('Guild 8:', 0., 100., 0.4, 0.1)
            g9 = mygrid[8][0].number_input('Guild 9:', 0., 100., 0.5, 0.1)
            g10 = mygrid[9][0].number_input('Guild 10:', 0., 100., 0.6, 0.1)
            g11 = mygrid[10][0].number_input('Guild 11:', 0., 100., 0.9, 0.1)
            g12 = mygrid[11][0].number_input('Guild 12:', 0., 100., 0.8, 0.1)
            g13 = mygrid[12][0].number_input('Guild 13:', 0., 100., 1.4, 0.1)
            g14 = mygrid[13][0].number_input('Guild 14:', 0., 100., 1.7, 0.1)
            g15 = mygrid[14][0].number_input('Guild 15:', 0., 100., 2.6, 0.1)
            g16 = mygrid[15][0].number_input('Guild 16:', 0., 100., 3., 0.1)
            g17 = mygrid[16][0].number_input('Guild 17:', 0., 100., 4., 0.1)
            g18 = mygrid[17][0].number_input('Guild 18:', 0., 100., 8.1, 0.1)
            g19 = mygrid[18][0].number_input('Guild 19:', 0., 100., 36., 0.1)
            g20 = mygrid[19][0].number_input('Guild 20:', 0., 100., 34., 0.1)



##############calculations########################

ret_x = np.array([1,2,3,4,5,6,7,14,30,60,90])
ret_y = np.array([r1,r2,r3,r4,r5,r6,r7,r14,r30,r60,r90])/100

def func(x, a, b, c, d, e, f):
    return a * np.exp(-x/b) + c * np.exp(-x/d) + e * np.exp(-x/f)

popt, pcov = sc.optimize.curve_fit(func,ret_x,ret_y,p0=(0.23,3,0.05,10,0.03,100))


#days = 1001
#new_players = 1000
a1 = np.ones((days+1,1))*new_players
a2 = func(np.linspace(0,days,days+1),popt[0], popt[1], popt[2], popt[3], popt[4], popt[5])
# a2 = a2*((ret_d1/100)/a2[1])
a2[0] = 1

#day = 10000
dau = np.sum(new_players*a2[0:days])


ret_df = pd.DataFrame(columns=['Day of Game', 'Retention'])
ret_df['Day of Game'] = ret_x
ret_df['Retention'] = ret_y

######retention chart#######
a3 = func(np.linspace(0,100,100),popt[0], popt[1], popt[2], popt[3], popt[4], popt[5])
a3[0] = 1
ret_fit_df = pd.DataFrame(columns=['Day of Game', 'Retention'])
ret_fit_df['Day of Game'] = np.linspace(1,90,90)
ret_fit_df['Retention'] = a3[1:91] 

c = alt.Chart(ret_df).mark_circle(color='#FF0000', size=100).encode(
    x='Day of Game', y='Retention'
    )
d = alt.Chart(ret_fit_df).mark_line(stroke='#5276A7', interpolate='monotone').encode(
    x='Day of Game', y='Retention'
    )
e = alt.layer(c, d)
###############

#guild_fill = 18
guilds = (dau-new_players+(new_players*tutorial_finish/100))/guild_fill
dau_1 = np.sum(new_players*a2[0:days+1])
players_guild_left = (dau_1 - new_players)/guilds



####################

old_players = (dau_1 - new_players)

data = [
        [1, str(g1)+'%', old_players*g1/100],
        [2, str(g2)+'%', old_players*g2/100],
        [3, str(g3)+'%', old_players*g3/100],
        [4, str(g4)+'%', old_players*g4/100],
        [5, str(g5)+'%', old_players*g5/100],
        [6, str(g6)+'%', old_players*g6/100],
        [7, str(g7)+'%', old_players*g7/100],
        [8, str(g8)+'%', old_players*g8/100],
        [9, str(g9)+'%', old_players*g9/100],
        [10, str(g10)+'%', old_players*g10/100],
        [11, str(g11)+'%', old_players*g11/100],
        [12, str(g12)+'%', old_players*g12/100],
        [13, str(g13)+'%', old_players*g13/100],
        [14, str(g14)+'%', old_players*g14/100],
        [15, str(g15)+'%', old_players*g15/100],
        [16, str(g16)+'%', old_players*g16/100],
        [17, str(g17)+'%', old_players*g17/100],
        [18, str(g18)+'%', old_players*g18/100],
        [19, str(g19)+'%', old_players*g19/100],
        [20, str(g20)+'%', old_players*g20/100]
        ]
g_df = pd.DataFrame(data, columns=['Guild members no', 'Distribution %', 'Players'])



# guilds_b = old_players/players_guild_left_b
guilds_b = g_df[g_df['Guild members no']<19]['Players'].sum()

guilds_needed = np.floor(((new_players*tutorial_finish/100)-1)/(19-players_guild_left_b))+6




########results display##############

st.metric("Active Players on day "+str(days)+": ",str(dau))
st.write("##")
st.write("### Specifying 'Guild fill no'")
st.metric("Guilds: ",str(guilds))
st.metric("Left in Guild: ",str(players_guild_left))
st.write("##")
st.write("### Specifying 'Members left in Guild'")
st.metric("Guilds: ",str(guilds_b))
st.metric("Guilds needed: ",str(guilds_needed))

st.write("##")
with st.expander("Retention Fit"):
    st.altair_chart(e, use_container_width=True)

st.write("##")
with st.expander("Guild Distribution"):
    st.table(g_df)

