# EODHD coverage check (2026-10-12, free tier)

- S&P 500 names our free data is missing: **103**; listed by EODHD: **102 (99.0%)**
- Delisted US tickers EODHD lists: 60,420 (common stocks: 33,175)
- Price samples returning data: 11 of 15 (free tier = last 12 months only, so only recently delisted names can return rows)

Decision rule: subscribe for ONE month only if ≥90% of the missing names are listed. Then rerun with `--depth` and cancel unless ≥90% of them return history back to the year they went missing.

| Ticker | Missing from | Listed | Status | EODHD name | Price rows | First | Last |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AABA | 2017 | yes | delisted | Altaba Inc |  |  |  |
| ABMD | 2018 | yes | delisted | ABIOMED Inc |  |  |  |
| ADS | 2017 | yes | delisted | Alliance Data Systems Corporation |  |  |  |
| AET | 2017 | yes | delisted | Aetna Inc |  |  |  |
| AGN | 2017 | yes | delisted | Allergan plc |  |  |  |
| ALXN | 2017 | yes | delisted | Alexion Pharmaceuticals Inc |  |  |  |
| ANDV | 2017 | yes | delisted | Andeavor |  |  |  |
| ANSS | 2017 | yes | delisted | ANSYS Inc | 0 |  |  |
| APC | 2017 | yes | active | ARKO Petroleum Corp. |  |  |  |
| ATVI | 2017 | yes | delisted | Activision Blizzard Inc |  |  |  |
| AVB | 2017 | yes | delisted | AvalonBay Communities Inc | 211 | 2025-10-13 | 2026-08-14 |
| BBBY | 2017 | yes | delisted | Bed Bath & Beyond, Inc. |  |  |  |
| BCR | 2017 | yes | delisted | C.R. Bard Inc |  |  |  |
| CA | 2017 | yes | delisted | Xtrackers California Municipal Bonds ETF |  |  |  |
| CBS | 2017 | yes | delisted | ViacomCBS Inc |  |  |  |
| CDAY | 2021 | no |  |  |  |  |  |
| CELG | 2017 | yes | delisted | Celgene Corporation |  |  |  |
| CERN | 2017 | yes | delisted | Cerner Corp |  |  |  |
| CHK | 2017 | yes | delisted | Chesapeake Energy Corporation |  |  |  |
| CMA | 2017 | yes | delisted | Comerica Incorporated |  |  |  |
| COG | 2017 | yes | delisted | Cabot Oil & Gas Corporation |  |  |  |
| COL | 2017 | yes | delisted | Rockwell Collins Inc |  |  |  |
| CSRA | 2017 | yes | active | Cohen & Steers ETF Trust |  |  |  |
| CTLT | 2020 | yes | delisted | Catalent Inc |  |  |  |
| CTRA | 2021 | yes | delisted | Coterra Energy Inc | 143 | 2025-10-13 | 2026-05-07 |
| CTXS | 2017 | yes | delisted | Citrix Systems Inc |  |  |  |
| CXO | 2017 | yes | delisted | Concho Resources Inc |  |  |  |
| DAY | 2024 | yes | delisted | Dayforce Inc. | 79 | 2025-10-13 | 2026-02-04 |
| DFS | 2017 | yes | delisted | Discover Financial Services | 0 |  |  |
| DISCA | 2017 | yes | delisted | Discovery Inc |  |  |  |
| DISCK | 2017 | yes | delisted | Discovery Inc |  |  |  |
| DISH | 2017 | yes | delisted | DISH Network Corporation |  |  |  |
| DNB | 2017 | yes | delisted | Dun & Bradstreet Holdings Inc. |  |  |  |
| DRE | 2017 | yes | delisted | Duke Realty Corporation |  |  |  |
| EA | 2017 | yes | delisted | Electronic Arts Inc | 203 | 2025-10-13 | 2026-08-04 |
| ENDP | 2017 | yes | delisted | Endo International PLC |  |  |  |
| ESRX | 2017 | yes | delisted | Express Scripts Holding Co |  |  |  |
| ETFC | 2017 | yes | delisted | E*TRADE Financial LLC |  |  |  |
| EVHC | 2017 | yes | delisted | Envision Healthcare Holdings |  |  |  |
| FDXF | 2026 | yes | active | FedEx Freight Holding Company, Inc. | 96 | 2026-05-26 | 2026-10-09 |
| FL | 2017 | yes | delisted | Foot Locker Inc |  |  |  |
| FLIR | 2017 | yes | delisted | FLIR Systems Inc. |  |  |  |
| FRC | 2019 | yes | delisted | First Republic Bank |  |  |  |
| FTR | 2017 | yes | delisted | Frontier Communications Corporation |  |  |  |
| GGP | 2017 | yes | delisted | General Growth Properties Inc  |  |  |  |
| HAR | 2017 | yes | delisted | Harman International Industries Inc./DE/ |  |  |  |
| HBI | 2017 | yes | delisted | Hanesbrands Inc |  |  |  |
| HES | 2017 | yes | delisted | Hess Corporation | 0 |  |  |
| HOLX | 2017 | yes | delisted | Hologic Inc | 121 | 2025-10-13 | 2026-04-07 |
| HONA | 2026 | yes | active | Honeywell Aerospace Inc | 82 | 2026-06-15 | 2026-10-09 |
| IPG | 2017 | yes | delisted | Interpublic Group of Companies Inc | 33 | 2025-10-13 | 2025-11-26 |
| JNPR | 2017 | yes | delisted | Juniper Networks Inc | 0 |  |  |
| JWN | 2017 | yes | delisted | Nordstrom Inc |  |  |  |
| K | 2017 | yes | delisted | Kellanova | 42 | 2025-10-13 | 2025-12-10 |
| KSU | 2017 | yes | delisted | Kansas City Southern |  |  |  |
| LEG | 2017 | yes | delisted | Leggett & Platt Incorporated |  |  |  |
| LLL | 2017 | yes | delisted | JX Luxventure Ltd |  |  |  |
| LLTC | 2017 | yes | delisted | Linear Technology Corp |  |  |  |
| LVLT | 2017 | yes | delisted | Level 3 Communications Inc |  |  |  |
| MJN | 2017 | yes | delisted | Mead Johnson Nutrition CO |  |  |  |
| MNK | 2017 | yes | delisted | Mallinckrodt plc |  |  |  |
| MON | 2017 | yes | delisted | Monument Circle Acquisition Corp |  |  |  |
| MRO | 2017 | yes | delisted | Marathon Oil Corporation |  |  |  |
| MXIM | 2018 | yes | delisted | Maxim Integrated Products Inc |  |  |  |
| MYL | 2017 | yes | delisted | Viatris Inc |  |  |  |
| NBL | 2017 | yes | delisted | Noble Energy Inc |  |  |  |
| NFX | 2017 | yes | active | Corgi NFLX 2x Daily ETF |  |  |  |
| NLSN | 2017 | yes | delisted | Nielsen Holdings PLC |  |  |  |
| PBCT | 2017 | yes | delisted | People's United Financial Inc |  |  |  |
| PDCO | 2017 | yes | delisted | Patterson Companies Inc |  |  |  |
| PX | 2017 | yes | delisted | P10 Inc |  |  |  |
| PXD | 2017 | yes | delisted | Pioneer Natural Resources Co |  |  |  |
| Q | 2025 | yes | active | Qnity Electronics, Inc | 240 | 2025-10-27 | 2026-10-09 |
| QRVO | 2017 | yes | delisted | Qorvo Inc |  |  |  |
| RAI | 2017 | yes | delisted | Reynolds American Inc |  |  |  |
| RHT | 2017 | yes | delisted | Red Hat Inc |  |  |  |
| RTN | 2017 | yes | delisted | Raytheon Company |  |  |  |
| SCG | 2017 | yes | delisted | SCANA Corporation |  |  |  |
| SEE | 2017 | yes | delisted | Sealed Air Corporation |  |  |  |
| SIVB | 2018 | yes | delisted | SVB Financial Group |  |  |  |
| SNI | 2017 | yes | delisted | Scripps Networks Interactive Inc |  |  |  |
| SOLS | 2025 | yes | active | Solstice Advanced Materials, Inc | 245 | 2025-10-20 | 2026-10-09 |
| SPLS | 2017 | yes | active | PIMCO US Stocks PLUS Active Bond Exchange Traded Fund |  |  |  |
| SRCL | 2017 | yes | delisted | Stericycle Inc |  |  |  |
| STJ | 2017 | yes | delisted | St. Jude Medical Inc |  |  |  |
| SWN | 2017 | yes | delisted | Southwestern Energy Company |  |  |  |
| TGNA | 2017 | yes | delisted | Tegna Inc |  |  |  |
| TIF | 2017 | yes | delisted | Tiffany & Co |  |  |  |
| TSS | 2017 | yes | delisted | Total System Services Inc |  |  |  |
| TWTR | 2018 | yes | delisted | Twitter Inc |  |  |  |
| TWX | 2017 | yes | delisted | Time Warner Inc |  |  |  |
| VAR | 2017 | yes | delisted | Varian Medical Systems Inc |  |  |  |
| VIAB | 2017 | yes | delisted | Viacom Inc |  |  |  |
| VIAC | 2019 | yes | delisted | Paramount Global |  |  |  |
| WBA | 2017 | yes | delisted | Walgreens Boots Alliance Inc |  |  |  |
| WBD | 2022 | yes | delisted | Warner Bros Discovery Inc |  |  |  |
| WCG | 2018 | yes | delisted | WellCare Health Plans Inc |  |  |  |
| WFM | 2017 | yes | delisted | Whole Foods Market Inc |  |  |  |
| WRK | 2017 | yes | delisted | WestRock Co |  |  |  |
| WYND | 2017 | yes | delisted | WYND |  |  |  |
| XEC | 2017 | yes | delisted | Cimarex Energy Co |  |  |  |
| XL | 2017 | yes | delisted | XL Fleet Corp |  |  |  |
| XLNX | 2017 | yes | delisted | Xilinx Inc |  |  |  |
