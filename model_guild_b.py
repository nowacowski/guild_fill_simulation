# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 18:14:04 2022

@author: pnowakowski
"""

import numpy as np
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
    
    new_players = st.number_input('# New Players (daily):', 0, 10000, 100, 10)
    days = st.number_input('Day no:', 1, 10000, 100, 1)
    guild_fill = st.number_input('Guild fill no:', 1, 20, 19, 1)
    tut = st.number_input('Completed tutorial %:', 1, 100, 65, 1)
    churn = st.selectbox('Churn type',(1,2))
    
    
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
            
            
tut_compl = tut/100
n = new_players*tut_compl


ret_x = np.array([1,2,3,4,5,6,7,14,30,60,90])
ret_y = np.array([r1,r2,r3,r4,r5,r6,r7,r14,r30,r60,r90])/100

def func(x, a, b, c, d, e, f):
    return a * np.exp(-x/b) + c * np.exp(-x/d) + e * np.exp(-x/f)

popt, pcov = sc.optimize.curve_fit(func,ret_x,ret_y,p0=(0.23,3,0.05,10,0.03,100))


a2 = func(np.linspace(0,days,days+1),popt[0], popt[1], popt[2], popt[3], popt[4], popt[5])
a2 = a2/tut_compl
a2[0] = 1


dau = np.sum(n*a2[1:days+1])



######retention chart#######

ret_df = pd.DataFrame(columns=['Day of Game', 'Retention'])
ret_df['Day of Game'] = ret_x
ret_df['Retention'] = ret_y

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


#############################################################################


z2=np.empty(0)
z4=np.empty(0)
z5=np.empty(0)
z2_idx=np.empty(0, int)

for j in range(1,days+1):
    i2 = n
    i3 = 0
    i4=0
    # i=0
    while i2 > 1:
        i = 0
        # i5 = 0
        if j==1 or z2.size <= i4:
            i5=0
        else:
            i5=z2[i4]
        
        while i5 < guild_fill and i3 < n:
            if i4+1 <= z2.size:
                z2[i4]+=1
                i5+=1
            else:
                i5+=1
                
            i3+=1
            i+=1
            
        i2=i2-i
        
        if i4==0:
            z=np.array(i)
        else:
            z=np.append(z,i)
        i4+=1
        # print(i)
    
    
    
    
    if j>2:
        
        if z.size < np.shape(z5)[1]:
            z_sub = np.zeros(np.shape(z5)[1])
            z_sub[0:z.size] = z
            z = z_sub
            
        zx = np.linspace(0,z.size-1, z.size).astype(int)
        zx[0:np.shape(z2_idx)[1]] = np.argsort(z2_idx[-1])
        z = z[zx]
        
        
        
        
        
    if j == 1:
        z5=z
    elif j==2:
        z4 = np.pad(z5,(0,z.size-z5.size), mode='constant')
        z5 = np.vstack((z,z4))
    else:
        if z.size >= z2.size: #np.shape(z5)[1]:
            z4 = np.pad(z5,[(0,0),(0,z.size-np.shape(z5)[1])], mode='constant')
        else:
            
            z = np.pad(z,(0,np.shape(z5)[1]-z.size), mode='constant')
            z4 = z5
        z5 = np.vstack((z,z4))
    
    
    
    zz=np.copy(z5)
    if j==1:
        l = np.sum(zz) - np.round(np.sum(zz)*a2[1:j+1])
    else:
        l = np.sum(zz, axis=1) - np.round(np.sum(zz, axis=1)*a2[1:j+1])
        
        
        
    if churn == 1:
        for k in range(0,j):
            m = l[k]
            if j==1:
                o = zz.size
                while m > 0:
                    o-=1
                    while zz[o]>0 and m > 0:
                        zz[o]-=1
                        m-=1
            else:
                o = np.shape(zz)[1]
                while m > 0:
                    o-=1
                    while zz[k,o]>0 and m > 0:
                        zz[k,o]-=1
                        m-=1
                        
    elif churn == 2:
        if j==1:
            guilds = zz.size
        else:
            guilds = np.shape(zz)[1]
            
        for k in range(0,j):
            m = l[k]
            while m > 0:
                for mm in range(1,guilds+1):
                    mm2 = guilds-mm
                    if j==1:
                        if zz[mm2] > 0:
                            zz[mm2]-=1
                            m-=1
                    else:
                        if zz[k,mm2] > 0:
                            zz[k,mm2]-=1
                            m-=1
        
    
    
    if j==1:
        z2 = zz
    else:          
        z2 = np.sum(zz, axis=0)
        
    
    z2_sort_idx = np.argsort(z2)[::-1]
    if j==1:
        z2_idx = np.append(z2_idx,z2_sort_idx)
    else:
        r = np.ones((j-1,z2_sort_idx.size))*np.linspace(0,z2_sort_idx.size-1, z2_sort_idx.size)
        if j==2:
            r[0:j-1,0:z2_idx.size] = z2_idx
        else:
            r[0:j-1,0:np.shape(z2_idx)[1]] = z2_idx
        
        z2_idx = np.vstack((r,z2_sort_idx))
    
    z2 = z2[z2_sort_idx]




########results display################################################

st.metric("Active Players after day "+str(days)+": ",str(dau))
st.metric("New players joining guild:",str(n))




df=pd.DataFrame(z2, columns=['Members'])
df2=df.value_counts().to_frame()
df2.reset_index(inplace=True)
df2 = df2.rename(columns = {0:'Count'})
df2 = df2.sort_values(by=['Members'], ascending=False)
# df2 = df2.set_index('Members')

df3 = pd.DataFrame(df2['Count']*guild_fill-df2['Members']*df2['Count'])
df4 = pd.concat([df2, df3], axis=1)
df4 = df4.rename(columns = {0:'Free Spots'})

places = df4[df4['Members']>0]['Free Spots'].sum()
st.metric("Places in non-empty Guilds:",str(places))
st.write("##")

st.write("#### Guilds ")
st.table(df4)

st.write("##")
with st.expander("Retention Fit"):
    st.altair_chart(e, use_container_width=True)