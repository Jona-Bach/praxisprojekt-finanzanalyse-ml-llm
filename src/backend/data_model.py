kpi_list = [
    "Kurs-Buchwert-Verhältnis (KBV)",
    "Kurs-Cashflow-Verhältnis (KCV)",
    "Dividendenrendite",
    "Ausschüttungsquote (Payout Ratio)",
    "Eigenkapitalrendite (ROE)",
    "Gesamtkapitalrendite (ROA)",
    "Return on Capital Employed (ROCE)",
    "Return on Invested Capital (ROIC)",
    "Bruttogewinnmarge",
    "EBIT-Marge",
    "EBITDA-Marge",
    "Nettogewinnmarge",
    "Umsatzwachstum",
    "Gewinnwachstum",
    "Kapitalumschlag",
    "Working Capital",
    "Cashflow-Marge",
    "Liquidität 1. Grades (Cash Ratio)",
    "Liquidität 2. Grades (Quick Ratio)",
    "Liquidität 3. Grades (Current Ratio)",
    "Eigenkapitalquote",
    "Fremdkapitalquote",
    "Dynamischer Verschuldungsgrad",
    "Zinsdeckungsgrad",
    "Anlagendeckungsgrad I",
    "Anlagendeckungsgrad II",
    "Kurs-Gewinn-Verhältnis (Wachstum) (KGV)",
    "Kurs-Umsatz-Verhältnis (KUV)",
    "PEG Ratio",
    "Free Cashflow",
    "Operativer Cashflow",
    "Gewinn je Aktie (EPS)",
    "Verschuldungsgrad",
    "EV/EBITDA",
    "Beta",
    "Graham-Number"
]

alpha_vantage_kpis = {
    "Kurs-Buchwert-Verhältnis (KBV)": "PriceToBookRatio",
    "Dividendenrendite": "DividendYield",
    "Ausschüttungsquote (Payout Ratio)": "PayoutRatio",
    "Eigenkapitalrendite (ROE)": "ReturnOnEquityTTM",
    "Gesamtkapitalrendite (ROA)": "ReturnOnAssetsTTM",
    "Nettogewinnmarge": "ProfitMargin",
    "Umsatzwachstum": "QuarterlyRevenueGrowthYOY",  # *4 für annualisiert
    "Gewinnwachstum": "QuarterlyEarningsGrowthYOY",  # *4 für annualisiert
    "Kapitalumschlag": "AssetTurnover",
    "Cashflow-Marge": "operating_cashflow_margin",   # operatingCashFlow / revenue (selbst berechnen)
    "Eigenkapitalquote": "equityRatio",
    "Fremdkapitalquote": "debtRatio",
    "Kurs-Gewinn-Verhältnis (Wachstum) (KGV)": "PERatio",
    "Kurs-Umsatz-Verhältnis (KUV)": "PriceToSalesRatioTTM",
    "PEG Ratio": "PEGRatio",
    "Free Cashflow": "freeCashFlow",                 # operatingCashFlow - capex
    "Operativer Cashflow": "operatingCashFlow",
    "Gewinn je Aktie (EPS)": "EPS",
    "EV/EBITDA": "EVToEBITDA",
    "Beta": "Beta"
}

initial_tickers = [
    "AAPL",   # Apple
    "MSFT",   # Microsoft
    "GOOGL",  # Alphabet (Google)
    "AMZN",   # Amazon
    "META",   # Meta Platforms
    "TSLA",   # Tesla
    "NVDA",   # Nvidia
    "JPM",    # JPMorgan Chase
    "V",      # Visa
    "NFLX"    # Netflix
]

TICKERS = [
    "NVDA",   # 1
    "OPEN",   # 2
    "ONDS",   # 3
    "PLUG",   # 4
    "INTC",   # 5
    "TSLA",   # 6
    "BBAI",   # 7
    "SOFI",   # 8
    "GOOGL",  # 9
    "F",      # 10
    "NU",     # 11
    "PFE",    # 12
    "GRAB",   # 13
    "PLTR",   # 14
    "AMZN",   # 15
    "AMD",    # 16
    "DNN",    # 17
    "AAL",    # 18
    "ACHR",   # 19
    "AAPL",   # 20
    "T",      # 21
    "MARA",   # 22
    "CIFR",   # 23
    "NIO",    # 24
    "BMNR",   # 25
    "BBD",    # 26
    "RGTI",   # 27
    "SOUN",   # 28
    "IREN",   # 29
    "WULF",   # 30
    "KVUE",   # 31
    "NOK",    # 32
    "ORCL",   # 33
    "PCG",    # 34
    "BAC",    # 35
    "GOOG",   # 36
    "VALE",   # 37
    "WMT",    # 38
    "NFLX",   # 39
    "SNAP",   # 40
    "QBTS",   # 41
    "RIVN",   # 42
    "HOOD",   # 43
    "RIG",    # 44
    "CRWV",   # 45
    "ABEV",   # 46
    "WBD",    # 47
    "BE",     # 48
    "APLD",   # 49
    "MU",  # 50
    "BULL",   # 51
    "NBIS",   # 52
    "RKT",    # 53
    "UBER",   # 54
    "RXRX",   # 55
    "HBAN",   # 56
    "VZ",     # 57
    "QS",     # 58
    "MSFT",   # 59
    "CMCSA",  # 60
    "BTE",    # 61
    "AMCR",   # 62
    "EOSE",   # 63
    "AVGO",   # 64
    "MSTR",   # 65
    "IONQ",   # 66
    "BBWI",   # 67
    "JOBY",   # 68
    "SMCI",   # 69
    "CLSK",   # 70
    "BTG",    # 71
    "KO",     # 72
    "GGB",    # 73
    "AGNC",   # 74
    "QUBT",   # 75
    "SMR",    # 76
    "CSCO",   # 77
    "ET",     # 78
    "HL",     # 79
    "VICI",   # 80
    "MRK",    # 81
    "GAP",    # 82
    "HPE",    # 83
    "CMG",    # 84
    "OKLO",   # 85
    "CLF",    # 86
    "META",   # 87
    "TSM",    # 88
    "PYPL",   # 89
    "SLB",    # 90
    "CDE",    # 91
    "STLA",   # 92
    "SNDK",   # 93
    "OWL",    # 94
    "ITUB",   # 95
    "DOW",    # 96
    "CRCL",   # 97
    "EXAS",   # 98
    "PATH", 
    "LYFT",   # 101
    "NVO",    # 102
    "FCX",    # 103
    "RKLB",   # 104
    "VLY",    # 105
    "HIMS",   # 106
    "RIOT",   # 107
    "CCL",    # 108
    "CSX",    # 109
    "LEN",    # 110
    "UUUU",   # 111
    "ANET",   # 112
    "INFY",   # 113
    "CPRT",   # 114
    "PBR",    # 115
    "COMP",   # 116
    "KEY",    # 117
    "BABA",   # 118
    "MRVL",   # 119
    "WFC",    # 120
    "CORZ",   # 121
    "AUR",    # 122
    "B",      # 123 (Barrick Mining Corporation → Ticker wirklich nur "B")
    "XOM",    # 124
    "CVE",    # 125
    "TTD",    # 126
    "AG",     # 127
    "KDP",    # 128
    "KMI",    # 129
    "DKNG",   # 130
    "LRCX",   # 131
    "NCLH",   # 132
    "IQ",     # 133
    "ON",     # 134
    "C",      # 135 (Citigroup Inc.)
    "CAG",    # 136
    "BMY",    # 137
    "RF",     # 138
    "COLD",   # 139
    "NEE",    # 140
    "ERIC",   # 141
    "MRNA",   # 142
    "PTON",   # 143
    "BSX",    # 144
    "ASTS",   # 145
    "HAL",    # 146
    "GLXY",   # 147
    "JNJ",    # 148
    "XYZ",    # 149 (Block, Inc. → Ticker “SQ” existiert, aber du listest “XYZ” als Symbol)
    "PINS",   # 150
    "NGD",    # 151
    "CARR",   # 152
    "LUMN",   # 153
    "TGT",    # 154
    "NKE",    # 155
    "COIN",   # 156
    "OBDC",   # 157
    "PG",     # 158
    "LYG",    # 159
    "JD",     # 160
    "KHC",    # 161
    "MCHP",   # 162
    "JPM",    # 163
    "TXN",    # 164
    "CPNG",   # 165
    "ZETA",   # 166
    "TOST",   # 167
    "UMC",    # 168
    "VG",     # 169
    "EXK",    # 170
    "DVN",    # 171
    "MDT",    # 172
    "OSCR",   # 173
    "STUB",   # 174
    "PL",     # 175
    "NUVB",   # 176
    "MDLZ",   # 177
    "WDC",    # 178
    "MP",     # 179
    "CZR",    # 180
    "UEC",    # 181
    "GM",     # 182
    "QCOM",   # 183
    "DIS",    # 184
    "EQT",    # 185
    "VRT",    # 186
    "XPEV",   # 187
    "EQX",    # 188
    "RBLX",   # 189
    "GILD",   # 190
    "PRMB",   # 191
    "SHOP",   # 192
    "SBUX",   # 193
    "UAL",    # 194
    "NEM",    # 195
    "KIM",    # 196
    "BA",     # 197
    "CNH",    # 198
    "TJX",    # 199
    "CX",     #
    "IBRX",   # 201
    "HLN",    # 202
    "TEVA",   # 203
    "VFC",    # 204
    "UWMC",   # 205
    "CNQ",    # 206
    "PR",     # 207
    "DAL",    # 208
    "MPW",    # 209
    "CRGY",   # 210
    "FSM",    # 211
    "MO",     # 212
    "PDD",    # 213
    "PPTA",   # 214
    "ABT",    # 215
    "S",      # 216
    "AES",    # 217
    "CVX",    # 218
    "TFC",    # 219
    "CAVA",   # 220
    "OXY",    # 221
    "HRL",    # 222
    "MS",     # 223
    "BTDR",   # 224
    "CWAN",   # 225
    "VTRS",   # 226
    "ESTC",   # 227
    "V",      # 228
    "UPS",    # 229
    "DBK.DE", # 230
    "CLVT",   # 231
    "BP",     # 232
    "BB",     # 233
    "CFLT",   # 234
    "U",      # 235
    "AMAT",   # 236
    "HST",    # 237
    "NXE",    # 238
    "STNE",   # 239
    "TME",    # 240
    "UNH",    # 241
    "CRDO",   # 242
    "DELL",   # 243
    "GEHC",   # 244
    "MGM",    # 245
    "FAST",   # 246
    "AEG",    # 247
    "BAX",    # 248
    "SCHW",   # 249
    "ELAN",   # 250
      "PPL",     # 251
    "APH",     # 252
    "PANW",    # 253
    "WMB",     # 254
    "BKR",     # 255
    "ABBV",    # 256
    "BKD",     # 257
    "DTE.DE",  # 258
    "CTSH",    # 259
    "VNET",    # 260
    "PTEN",    # 261
    "ACI",     # 262
    "CNC",     # 263
    "PEP",     # 264
    "USB",     # 265
    "GENI",    # 266
    "ROST",    # 267
    "ASX",     # 268
    "LCID",    # 269
    "FLNC",    # 270
    "GT",      # 271
    "WU",      # 272
    "TU",      # 273
    "LITE",    # 274
    "JHX",     # 275
    "SE",      # 276
    "CL",      # 277
    "BEKE",    # 278
    "KGC",     # 279
    "CRM",     # 280
    "HD",      # 281
    "GIS",     # 282
    "AZN",     # 283
    "BCS",     # 284
    "NLY",     # 285
    "FIG",     # 286
    "FLG",     # 287
    "HUT",     # 288
    "O",       # 289
    "AEO",     # 290
    "CCJ",     # 291
    "DOC",     # 292
    "LUV",     # 293
    "CELH",    # 294
    "AHR",     # 295
    "COP",     # 296
    "GLW",     # 297
    "EXC",     # 298
    "WIT",     # 299
    "COMM",    # 300
      "IBKR",   # 301
    "WY",     # 302
    "M",      # 303
    "ABNB",   # 304
    "RITM",   # 305
    "PM",     # 306
    "ALAB",   # 307
    "SNOW",   # 308
    "ENPH",   # 309
    "VOD",    # 310
    "PAGS",   # 311
    "EQNR",   # 312
    "ONON",   # 313
    "FRMI",   # 314
    "SBSW",   # 315
    "DASH",   # 316
    "QXO",    # 317
    "KR",     # 318
    "RUN",    # 319
    "FITB",   # 320
    "ORLY",   # 321
    "CVS",    # 322
    "TEM",    # 323
    "XP",     # 324
    "HBI",    # 325
    "AXTA",   # 326
    "SO",     # 327
    "AVTR",   # 328
    "ZTS",    # 329
    "MRP",    # 330
    "CPB",    # 331
    "CHWY",   # 332
    "CTRA",   # 333
    "VST",    # 334
    "TMUS",   # 335
    "YMM",    # 336
    "WRD",    # 337
    "ADT",    # 338
    "ARM",    # 339
    "ENR.DE", # 340
    "GEN",    # 341
    "IAG",    # 342
    "IVZ",    # 343
    "DDOG",   # 344
    "UPST",   # 345
    "RTX",    # 346
    "LOW",    # 347
    "LYB",    # 348
    "CCC",    # 349
    "BRK-B",  # 350
      "BEN",     # 351
    "APP",     # 352
    "OGE",     # 353
    "PBR-A",   # 354
    "AR",      # 355
    "SW",      # 356
    "TECK",    # 357
    "ACN",     # 358
    "KKR",     # 359
    "FE",      # 360
    "STM",     # 361
    "KMB",     # 362
    "GTM",     # 363
    "TMC",     # 364
    "SEDG",    # 365
    "ESI",     # 366
    "CSGP",    # 367
    "APA",     # 368
    "LI",      # 369
    "IBM",     # 370
    "WSC",     # 371
    "MBLY",    # 372
    "IOT",     # 373
    "FLO",     # 374
    "MOS",     # 375
    "PCAR",    # 376
    "ZIM",     # 377
    "CART",    # 378
    "GE",      # 379
    "TSCO",    # 380
    "AIG",     # 381
    "PONY",    # 382
    "D",       # 383 (Dominion Energy)
    "FTNT",    # 384
    "IP",      # 385
    "GME",     # 386
    "CNP",     # 387
    "PSKY",    # 388
    "INVH",    # 389
    "DXCM",    # 390
    "LHA.DE",  # 391
    "BN",      # 392
    "AFRM",    # 393
    "KMX",     # 394
    "DHI",     # 395
    "GTLB",    # 396
    "MIR",     # 397
    "IFX.DE",  # 398
    "BRBR",    # 399
    "CFG",     # 400
    "CLS",     # 401
    "HOG",     # 402
    "LVS",     # 403
    "GNW",     # 404
    "MNST",    # 405
    "BF-B",    # 406
    "CRBG",    # 407
    "CTVA",    # 408
    "AA",      # 409
    "EIX",     # 410
    "JCI",     # 411
    "IBN",     # 412
    "ADPT",    # 413
    "ARCC",    # 414
    "IPG",     # 415
    "BJ",      # 416
    "TTEK",    # 417
    "COHR",    # 418


]