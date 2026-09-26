"""Derive Thai efficiency-loss indicators from downloaded public data (EPPO, Ember, World Bank).
Run: .venv/bin/python model/analysis.py   -> writes data/derived_*.csv
All numbers computed from files in data/; see DATA.zh.md for sources."""
import pandas as pd, json
D='data/'
g=pd.read_csv(D+'eppo_11_27.csv'); ga=g.pivot_table(index='Year',columns='Fuel Type',values='Quantity',aggfunc='sum')
ga['Total']=ga.sum(axis=1); ga['Domestic']=ga.Total-ga.Imported
ga['gas_share_total_%']=ga['Natural Gas']/ga.Total*100
ga['gas_share_domestic_%']=ga['Natural Gas']/ga.Domestic*100
s=pd.read_csv(D+'eppo_11_37.csv'); sa=s.pivot_table(index='Year',columns='Sector',values='Quantity',aggfunc='sum'); sa['Total']=sa.sum(axis=1)
gap=pd.DataFrame({'generation_GWh':ga.Total,'sales_GWh':sa.Total})
gap['gap_GWh']=gap.generation_GWh-gap.sales_GWh; gap['gap_%']=gap.gap_GWh/gap.generation_GWh*100
t=pd.read_csv(D+'eppo_11_34.csv'); ta=t.pivot_table(index='Year',columns='Tariff',values='Quantity',aggfunc='sum'); ta_share=ta.div(ta.sum(axis=1),axis=0)*100
l=pd.read_csv(D+'eppo_11_28.csv'); pk=l[l.LOAD=='PEAK'].groupby('Year').Quantity.max(); lf=l[l.LOAD=='LOAD FACTOR'].groupby('Year').Quantity.mean()
out=pd.concat([ga[['Total','Natural Gas','Imported','Renewable Energy','Coal & Lignite','Hydro Electricity','gas_share_total_%','gas_share_domestic_%']],
               gap[['sales_GWh','gap_GWh','gap_%']], pk.rename('EGAT_system_peak_MW'), lf.rename('avg_monthly_load_factor_%')],axis=1).loc[2010:2025]
out.round(2).to_csv(D+'derived_annual_2010_2025.csv')
ta_share.loc[2015:2025].round(2).to_csv(D+'derived_sales_share_by_tariff_class.csv')
w=pd.read_csv(D+'wb_td_losses.csv'); w.pivot(index='year',columns='iso',values='loss_pct').loc[2010:].round(2).to_csv(D+'derived_td_losses_peers_WB.csv')
print(out.loc[2019:].round(1).to_string()); print(ta_share.loc[[2019,2024,2025]].round(1).T.to_string())
