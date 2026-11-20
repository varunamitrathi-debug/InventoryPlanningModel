# Inventory planning model for an online wholesaler (Excel)

**Question.** How much stock should a UK gift wholesaler hold for its 30 best selling products, how often should it reorder, and where is the money in improving the policy?

**Answer in one line.** At a 95% service level and a two week lead time the 30 products need £34,183 of safety stock and about £73,000 of average stock. Ordering monthly is already close to optimal (switching to EOQ saves only £1,924 a year), so the real lever is lead time: cutting it from two weeks to one frees £10,012 of safety stock.

## Approach

* **Real demand.** Took 52 weeks of UK sales (6 December 2010 to 4 December 2011) from the UCI Online Retail II dataset and computed weekly mean and standard deviation of units for the 30 highest revenue products (`prepare.py`). Cancellations, returns and one 74,215 unit order that was cancelled the same day are excluded.
* **Excel model.** For each product: ABC class, unit cost, economic order quantity, orders per year, safety stock, reorder point, average stock value and annual ordering and holding cost, compared with a baseline of ordering once a month.
* **Stress it.** A sensitivity table shows safety stock value for service levels from 90% to 99.5% and lead times of one to four weeks. A check sheet runs nine automatic tests.

## Key findings

* **Scale.** The 30 products sold 456,612 units worth £1,336,034 in the year. Twenty of them are class A and bring 78.6% of that revenue.
* **Monthly ordering is nearly optimal.** EOQ cycle cost is £19,434 against £21,358 for monthly ordering, a saving of £1,924 a year (9.0%). For the biggest sellers the EOQ works out at about 12 orders a year anyway.
* **Service level is expensive at the top end.** Safety stock value rises from £34,183 at 95% to £48,346 at 99%, an increase of 41%.
* **Lead time is the cheapest lever.** At 95% service, safety stock falls from £34,183 with a two week lead time to £24,171 with one week, 29% less. At a 25% holding rate that is about £2,500 a year.

## Recommendation

* Keep the monthly ordering rhythm for class A products; recalculating EOQ adds little.
* Negotiate a one week lead time (or local buffer stock) with the suppliers of the 20 class A products first; they hold £25,821 of the £34,183 safety stock.
* Set service level by class rather than one number for everything, and review the Christmas lines separately: their demand is seasonal, so a single yearly standard deviation overstates safety stock outside the season and understates it in the peak.

## What is an assumption

Demand, prices and revenue come from the data. Service level (95%), lead time (2 weeks), cost per order (£40), holding cost (25% a year), gross margin (50%, used because the data has selling prices but not costs) and the monthly baseline are **assumptions**, all on the Inputs sheet with their reasoning.

## Files

```
InventoryPlanningModel/
  README.md                      this summary
  Inventory Planning Model.xlsx  Dashboard, Inputs, Data, Calculation, Sensitivity, Checks, Sources
  Build Guide.md                 step by step layout and formulas
  prepare.py                     builds the weekly demand table from the raw data
  output/sku demand.csv          result of prepare.py
  data/                          put the UCI workbook here (not committed)
```

## Tools

Excel (SQRT, NORMSINV, SUMPRODUCT, SUMIF, COUNTIF, data validation, charts), Python with pandas for data preparation.

## How to run

1. Open `Inventory Planning Model.xlsx`, change the service level or lead time on the Inputs sheet and watch the Dashboard. The Checks sheet should say "All checks pass".
2. To rebuild the demand table, download [Online Retail II from UCI](https://archive.ics.uci.edu/dataset/502/online+retail+ii), save the workbook in `data/` as `online retail.xlsx`, then run `pip install pandas openpyxl` and `python prepare.py`.

Data: Chen, D. (2012). Online Retail II. UCI Machine Learning Repository. CC BY 4.0.
