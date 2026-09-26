"""First rough levelized-cost comparison (THB per kWh saved or supplied) + evening-peak check.
DESIGN PROTOTYPE ONLY. Every input is in model/inputs.csv with status (verified / search-snippet / derived / ASSUMPTION).
Options without a sourced cost are reported as BREAK-EVEN capex instead of a cost (no invented numbers).
Run: .venv/bin/python model/model.py  -> model/results.csv, model/peak_check.csv"""
import csv
P={r['param']:float(r['value']) for r in csv.DictReader(open('model/inputs.csv'))}
def crf(r,n): return r*(1+r)**n/((1+r)**n-1)
rows=[]
for r in (0.03,P['discount_rate'],0.10):
    fx=P['fx_thb_per_usd']
    # 1) AC replacement at end-of-life: incremental cost baseline->best available (CLASP prices)
    for cap in ('12','24'):
        C=int(cap)*1000; h=P['ac_hours_res']
        kwh_b=C*h/P[f'ac{cap}_base_seer']/1000; kwh_e=C*h/P[f'ac{cap}_bat_seer']/1000; saved=kwh_b-kwh_e
        inc=P[f'ac{cap}_bat_price']-P[f'ac{cap}_base_price']; full=P[f'ac{cap}_bat_price']
        rows.append((r,f'AC {cap}k Btu/h: buy best-available instead of typical (at replacement)','saved',inc*crf(r,P['ac_life'])/saved,f'saves {saved:.0f} kWh/yr/unit @ {h:.0f} h/yr'))
        rows.append((r,f'AC {cap}k Btu/h: early retrofit (full new-unit cost, residential hours)','saved',full*crf(r,P['ac_life'])/saved,'upper bound; hotels run more hours -> lower cost'))
        h2=h*2  # sensitivity: commercial/hotel double hours (ASSUMPTION, not sourced)
        rows.append((r,f'AC {cap}k Btu/h: early retrofit, 2x hours (hotel-like, ASSUMPTION)','saved',full*crf(r,P['ac_life'])/(saved*2),'hours doubled = assumption'))
    # 2) rooftop solar (self-consumption), residential capex range
    for cx in ('rooftop_capex_10kw','rooftop_capex_5kw'):
        c=P[cx]; lc=c*(crf(r,P['rooftop_life'])+P['rooftop_om_frac'])/P['rooftop_yield']
        rows.append((r,f'Rooftop solar ({cx.split("_")[-1]} residential capex)','supplied',lc,'daytime only; 0 MW at 20:00-21:00 peak'))
    # 3) new CCGT on LNG
    for hr_key in ('ccgt_heat_rate','egat_fleet_heat_rate'):
        for lp in ('lng_price_low','lng_price_high'):
            fuel=P[hr_key]/1e6*P[lp]*fx
            cap=P['ccgt_capex']*fx*crf(r,P['ccgt_life'])/(8760*P['ccgt_capacity_factor'])
            rows.append((r,f'New CCGT on LNG (HR {P[hr_key]:.0f}, LNG ${P[lp]:.1f})','supplied',fuel+cap,f'fuel {fuel:.2f} + capital {cap:.2f} (CF {P["ccgt_capacity_factor"]}); excl. fixed O&M'))
            if r==P['discount_rate']:
                rows.append((r,f'Existing under-used gas plant, fuel only (HR {P[hr_key]:.0f}, LNG ${P[lp]:.1f})','supplied',fuel,'capacity already paid via availability payments'))
    # 4) BESS: cost per kWh shifted (storage adder only; charging energy cost excluded)
    capex=P['bess_capex']*fx; yrs=P['bess_life_cycles']/P['bess_cycles_per_year']
    rows.append((r,'BESS (4h-class, BNEF global turnkey price) - storage adder per kWh discharged','shifted',capex*crf(r,yrs)/(P['bess_cycles_per_year']*P['bess_rte']),'add cost of charging energy; Thai installed cost unknown'))
with open('model/results.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['discount_rate','option','basis','THB_per_kWh','note'])
    for x in rows: w.writerow([x[0],x[1],x[2],round(x[3],2),x[4]])
# break-even for options without sourced cost: max upfront THB per (kWh saved per year) to beat a benchmark
be=[]
for bench_name,bench in (('avg retail tariff',P['retail_avg_tariff']),('TOU peak rate',P['tou_peak'])):
    for life in (5,10,15):
        be.append((bench_name,bench,life,round(bench/crf(P['discount_rate'],life),2)))
with open('model/breakeven.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['benchmark','THB_per_kWh','measure_life_yr','max_upfront_THB_per_annual_kWh_saved'])
    w.writerows(be)
# evening-peak check (20:00-21:00): contribution factors are ASSUMPTIONS except where noted
peak=[('Rooftop solar (no storage)',0.0,'peak at 20:50-20:56 is after sunset (EGAT AR2024; IEEFA)'),
      ('BESS',1.0,'full rated power if dispatched at peak'),
      ('AC efficiency (residential)',None,'needs hourly end-use data: residential AC evening share unknown -> GAP'),
      ('AC efficiency / controls (hotels)',None,'hotel AC runs ~24h (Tangon 2018) -> high coincidence, magnitude unknown'),
      ('Demand response',1.0,'by design if called at peak; EGAT pilot 50 MW'),
      ('Grid loss reduction',None,'losses scale ~ with load^2, so peak-hour benefit > average; no Thai hourly loss data'),
      ('New CCGT / SMR',1.0,'firm capacity; SMR earliest 2037')]
with open('model/peak_check.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['option','MW_per_MW_nameplate_at_evening_peak','basis']); w.writerows(peak)
for x in rows:
    if x[0]==P['discount_rate']: print(f'{x[3]:6.2f}  {x[2]:8s} {x[1]}')
print(be)
