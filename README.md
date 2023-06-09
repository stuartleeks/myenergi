# myenergi

This repo contains code for exploring the myenergi API :-)


## myenergy API

API has the following fields (not all present in every data point):

| Field name | Description     | Notes (*)                                    |
| ---------- | --------------- | -------------------------------------------- |
| yr         | year            | e.g. `2023`                                  |
| mo         | month           | e.g. `1`                                     |
| dom        | day of month    | e.g. `1`                                     |
| dow        | day of week     | e.g. `"Sun"`                                 |
| hr         | hour            | e.g. `10` , if missing assume `0`            |
| min        | minute          | e.g. `1`, if missing assume `0`              |
| imp        | imported energy | imported energy in J                        |
| gep        |                 | generated energy in J                       |
| exp        |                 | exported energy in J                        |
| h1d        |                 | energy used by h1d in J                     |
| h2d        |                 | energy used by h2d in J                     |
| h3d        |                 | energy used by h3d in J                     |
| h1b        |                 | energy used by h1b in J                     |
| h2b        |                 | energy used by h2b in J                     |
| h3b        |                 | energy used by h3b in J                     |
| v1         | voltage         | in decavolts, i.e. divide by 10 to get volts |
| frq        | frequency       | in centahertz, i.e. divide by 100 to  hertz  |


The `Energy_Report.py` script parses the API response fields as:

| Variable | Formula                                    |
| -------- | ------------------------------------------ |
| y_import | imp/(60*1000)                              |
| y_gep    | gep/(60*1000)                              |
| y_exp    | exp/(60*1000)                              |
| y_z1     | h1d/(60*1000)                              |
| y_z2     | h2d/(60*1000)                              |
| y_z3     | h3d/(60*1000)                              |
| y_z1b    | h1b/(60*1000)                              |
| y_z2b    | h2b/(60*1000)                              |
| y_z3b    | h3b/(60*1000)                              |
| y_zappi  | y_z1 + y_z2 + y_z3 + y_z1b + y_z2b + y_z3b |

The CSV output has the following headers:

| Header text                | value                  | formula                                             |
| -------------------------- | ---------------------- | --------------------------------------------------- |
| Date                       | day/month/year         |                                                     |
| Import (kWh)               | daily_import           | sum(y_import)/60                                    |
| Export (kWh)               | daily_export           | sum(y_exp)/60                                       |
| Generation (kWh)           | daily_generation       | sum(y_gep)/60                                       |
| Zappi Energy (kWh)         | daily_EV               | sum(yzappi)/60                                      |
| Self Consumption (kWh)     | daily_self_consumption | daily_generation - daily_export                     |
| Total Property Usage (kWh) | daily_property_usage   | daily_import + daily_self_consumption               |
| Green Percentage           | daily_green_percentage | 100 * daily_self_consumption / daily_property_usage |


NOTE:
* The CSV headers indicate kWh. The script initially divides by `60*1000` then further divides by `60`. This suggests that the API returns J. (1 kWh = 3600,000 J)



## Links

-  https://myaccount.myenergi.com/

-  https://github.com/ashleypittman/mec
-  https://github.com/twonk/MyEnergi-App-Api
-  https://myenergi.info/extracting-energy-data-t7445-s40.html
-  https://myenergi.info/api-f54/
-  https://support.myenergi.com/hc/en-gb/articles/5069627351185-How-do-I-get-an-API-key-
	


Leaf?!
- https://github.com/filcole/pycarwings2 (via https://github.com/ashleypittman/mec)