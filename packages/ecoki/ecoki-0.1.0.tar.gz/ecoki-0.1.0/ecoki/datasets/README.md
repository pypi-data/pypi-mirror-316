# ecoKI dataset folder

This folder is a place for the datasets required to execute building blocks and pipelines. 

**Please download the required dataset from the next cloud depending on the use cases:** https://ncld.ips.biba.uni-bremen.de/apps/files/?dir=/000_ecoKI_partners/010_workpackages/AP_2-4_Dissemination/Guidelines%20and%20Tutorials/Tutorial%20Use%20Case/Data/datasets_ecoki_repo&fileid=4662897

**Please do not add any new datasets in this folder and push them to the repo, instead upload the dataset to the same next cloud folder**

**If buidling blocks or pipelines need to read loacl dataset, set the file path to this folder**

## datasets and usage
| dataset | pipeline|example|
|  ----  | ----  |----  |
| [energydata_complete.csv](https://ncld.ips.biba.uni-bremen.de/apps/files/?dir=/000_ecoKI_partners/010_workpackages/AP_2-4_Dissemination/Guidelines%20and%20Tutorials/Tutorial%20Use%20Case/Data/datasets_ecoki_repo&openfile=4662903) | Store_Data  | energyMonitoring|
|  | Train_LinReg_Model  |execute_ecoki_pipeline|
|  | |object_structure |
|  |  |restapi|
|[tabular_data_nan.csv](https://ncld.ips.biba.uni-bremen.de/apps/files/?dir=/000_ecoKI_partners/010_workpackages/AP_2-4_Dissemination/Guidelines%20and%20Tutorials/Tutorial%20Use%20Case/Data/datasets_ecoki_repo&openfile=4662899) | Replace_Missing_Values  |missingDataImputation|
| |Train_XGBoost_Model_Dm  | |
| |Visualize_Data  | |
| [appliances_nans.csv](https://ncld.ips.biba.uni-bremen.de/apps/files/?dir=/000_ecoKI_partners/010_workpackages/AP_2-4_Dissemination/Guidelines%20and%20Tutorials/Tutorial%20Use%20Case/Data/datasets_ecoki_repo&openfile=4662900)  | Store_Data  | |
| [Scenario_1_apple_juice_production.csv](https://ncld.ips.biba.uni-bremen.de/apps/files/?dir=/000_ecoKI_partners/010_workpackages/AP_2-4_Dissemination/Guidelines%20and%20Tutorials/Tutorial%20Use%20Case/Data/datasets_ecoki_repo&openfile=4668787)  | Run_Parameter_Optimisation  | |
|  |Train_Xgboost_Multi||
|[household_power_consumption.txt](https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption)  |LSTM|
