# Merge to One?
-rw-r--r-- 1 Fergal 197121 1636 Mar 28 16:29 heathrow_save_departures_json.py       ToolA
-rw-r--r-- 1 Fergal 197121 1647 Mar 28 17:40 heathrow_save_arrivals_json.py         ToolB

# Tidy their dependencies
-rw-r--r-- 1 Fergal 197121 4831 Mar 28 17:27 heathrow_parsing.py                    Main1
-rw-r--r-- 1 Fergal 197121 2260 Mar 27 21:47 heathrow_flight_tables.py              Main2

# Keep working
-rw-r--r-- 1 Fergal 197121 4889 Mar 27 21:46 test_heathrow_parsing.py               ok
-readme instructions44

# Merge
## Try keep the three scripty parts as generics
-rw-r--r-- 1 Fergal 197121  757 Mar 27 21:46 dict_to_dataframe.py                   merge
-rw-r--r-- 1 Fergal 197121 2379 Mar 27 21:46 date_to_dict.py                        merge
-rw-r--r-- 1 Fergal 197121  966 Mar 27 21:46 dataframe_to_csv.py                    merge

# DONE:
# Rename
-rw-r--r-- 1 Fergal 197121 3211 Mar 27 21:46 heathrow_plot_wip.py                   z
-rw-r--r-- 1 Fergal 197121  654 Mar 27 21:46 heathrow_plot_empirical_wip.py         z
-rw-r--r-- 1 Fergal 197121 1293 Mar 27 21:46 heathrow_dataframe_pickle.py           z   
## Make redundant?
-rw-r--r-- 1 Fergal 197121 1205 Mar 27 21:46 heathrow_extraction.py                 z+