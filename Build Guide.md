# Build guide: inventory planning model in Excel

Two evenings. The finished workbook is the answer key.

## Evening 1: demand data

* Download [Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii), save it in `data/` as `online retail.xlsx`, run `pip install pandas openpyxl` then `python prepare.py`.
* The script keeps UK sales from 6 December 2010 for exactly 52 weeks, drops cancellations, returns, non product codes (postage, fees) and one cancelled bulk order, picks the 30 products with the most revenue and works out weekly units for each. Weeks with no sales count as zero, which matters for the standard deviation.
* Paste `output/sku demand.csv` into the Data sheet from row 5. Add column H, cumulative revenue share: `=SUM($G$5:G5)/SUM($G$5:$G$34)` and fill down. The rows are already sorted by revenue, so this column drives the ABC classes.

## Evening 2: the workbook

Arial throughout, blue for inputs, black for formulas, green for links to another sheet.

**Inputs (B5 to B12):** service level 95%, lead time 2 weeks, cost per order £40, holding rate 25%, gross margin 50%, class A cut off 80%, class B cut off 95%, baseline 12 orders a year. Put the reasoning for each in column C.

**Calculation:** `B4` holds the z value: `=NORMSINV(Inputs!$B$5)` (1.645 at 95%). Then one row per product from row 7:

| Col | Item | Formula in row 7 |
|---|---|---|
| C | ABC class | `=IF(Data!H5<=Inputs!$B$10,"A",IF(Data!H5<=Inputs!$B$11,"B","C"))` |
| D | Annual units | `=Data!C5` |
| E | Unit cost | `=Data!F5*(1-Inputs!$B$9)` |
| F | Holding cost per unit per year | `=E7*Inputs!$B$8` |
| G | EOQ | `=SQRT(2*D7*Inputs!$B$7/F7)` |
| H | Orders per year | `=D7/G7` |
| I | Safety stock | `=$B$4*Data!E5*SQRT(Inputs!$B$6)` |
| J | Reorder point | `=Data!D5*Inputs!$B$6+I7` |
| K | Average stock value | `=(G7/2+I7)*E7` |
| L | Ordering cost per year | `=H7*Inputs!$B$7` |
| M | Holding cost per year | `=(G7/2+I7)*F7` |
| N | Total | `=L7+M7` |
| O | Monthly ordering cycle cost | `=Inputs!$B$12*Inputs!$B$7+D7/Inputs!$B$12/2*F7` |
| P | EOQ cycle cost | `=L7+G7/2*F7` |
| Q | Saving | `=O7-P7` |

Why these work, in one line each:

* **EOQ** balances two costs that move in opposite directions: ordering more often costs more in admin, ordering less often means holding more stock.
* **Safety stock** covers demand that runs above average during the lead time. Weekly variation grows with the square root of the number of weeks, hence `SQRT(lead time)`.
* **Reorder point** is the stock level at which to place an order: expected demand during the lead time plus the buffer.
* **Cycle cost** leaves safety stock out so the comparison between EOQ and monthly ordering is like for like.

Add a Total row with SUM for the money columns and `=SUMPRODUCT(I7:I36,E7:E36)` for total safety stock value.

**Sensitivity:** service levels 90% to 99.5% down column A, lead times 1 to 4 across row 4. Each cell: `=NORMSINV($A5)*SQRT(B$4)*SUMPRODUCT(Data!$E$5:$E$34,Calculation!$E$7:$E$36)`.

**Dashboard:** key numbers linked from the Calculation totals, a small ABC table using COUNTIF and SUMIF, and a column chart of safety stock value against service level.

**Checks:** nine TRUE or FALSE tests (30 products present, service level in range, cumulative share ends at 100%, every product classed, EOQ positive, reorder point at least the safety stock, EOQ never worse than monthly, sensitivity agrees with the calculation, totals add up) and a summary cell.

## Write up

Lead with the answer, give the numbers, say clearly which inputs are assumptions, and name the model's main limit: Christmas products are seasonal, so one yearly standard deviation is a simplification.
