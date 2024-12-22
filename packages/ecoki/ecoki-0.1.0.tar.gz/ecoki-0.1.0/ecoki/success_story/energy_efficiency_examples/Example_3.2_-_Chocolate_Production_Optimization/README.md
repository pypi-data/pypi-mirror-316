<b><u>Example #3.2: Optimize the machine parameters of a chocolate production process using optimized feature analysis to reduce energy</u></b>

###### <!-- This is the separator for the contents, above is displayed in popup and below in the details page  -->

## Beispiel: Optimieren Sie die Maschinenparameter eines Schokoladenherstellungsprozesses mit Hilfe einer optimierten Merkmalsanalyse, um Energie zu sparen.

In diesem Beispiel wird folgendes Energieeffizienz-Szenario mit einem Beispieldatensatz aus einer Simulierten Schokoladenproduktion durchgeführt:

Folgende Pipeline wird verwendet:

[http://localhost:20000/active/building_blocks_overview/Train_Xgboost_Multi/](http://localhost:20000/active/building_blocks_overview/Train_Xgboost_Multi/)

[http://localhost:20000/active/building_blocks_overview/Run_Parameter_Optimisation_Test_ML_chocolate/](http://localhost:20000/active/building_blocks_overview/Run_Parameter_Optimisation_Test_ML_chocolate/)

## Beschreibung Datensatz

Der Datensatz besteht aus circa drei Jahre Meßung einer simulierten Schokoladen-Produktion, für die jeweils folgende Daten pro Minute aufgenommen wurden:

Metadaten:

- **simulationID**: Diverse Kombinationen von Parameter wurden Simuliert. Jede Kombination hat eine eingene SimulationID

Sechs Maschinen:

- **press**: *In der Presse wird Kakaobutter wird aus der Schokoladenmasse gepresst* 
- **tempering1**, **tempering2**: *Beim Temperieren wird die Schokolade langsam erwärmt und dann abgekühlt, damit die Fettmoleküle gleichmäßig kristallisieren und die Schokolade beim Erstarren eine glatte, glänzende Oberfläche erhält.*
- **conching1**, **conching2**, **conching3**: *Beim Conchieren wird die Schokoladenmasse über einen längeren Zeitraum kontinuierlich gemischt, gemahlen und geknetet.*


Für jede der sechs Maschinen in der Produktion:

- **temperature** oder **pressure**: *Parameter der Maschine der  eingestellt werden kann*
- **delaytime**: *Dauer der Verarbeitung nachdem eine Maschine gefüllt wurde*
- **power**: *Leistung der Maschine, kW*
- **energy**: *Verbrauchte Energie, kWh (in der Simulation)*
- **number_of_batches**: *Anzahl Chargen produziert (eine Charge ist ~20-30 kG Schokolade)*

Drei mögliche Rezepte:

- **recipe_chocolate_Dark_Chocolate**
- **recipe_chocolate_Milk_Chocolate**
- **recipe_chocolate_Normal_Chocolate**

Qualität:

- **quality_rating**: *Meßwert der Qualität zwischen 0 und 100*
- **quality_classification**: *Klassifizierung der Qualität. <91 ist "Low", <96 ist "Good", >96 ist "Best"*

Summen:

- **total_batches_processed**
- **total_energy_consumption**
- **total_energy_per_batch**
- **energy_per_unit_process:** *Normalisieter Wert des Energieverbrauchs pro kG Schokolage*


## Aufgabe 

Ihre Aufgabe ist es, eine optimierte Merkmalsanalyse zu verwenden, um die Maschinenparameter so zu optimieren, dass die "Energie_pro_Einheit_Prozess" am stärksten reduziert wird, während der erforderliche Wert für die "Qualitätsbewertung" erhalten bleibt.

Die Daten können aus der ecoKI Datenbank (MongoDB) oder aus dem Dataverse geladen werden, wenn Sie keinen Zugriff auf eine konfigurierte ecoKI Datenbank (lokal oder remote) haben. 

- Im Dataverse hat der .csv-Datensatz den Namen "example_3_chocolate_production".
- In der ecoKI-Datenbank (MongoDB) hat der .json-Datensatz den Namen _"Chocolate_Production_v09"_.

In der Zwischenzeit kann eine neuere Version des Datensatzes verfügbar sein. Derzeit sind auch verschiedene Stichprobengrößen verfügbar. Wählen Sie eine kleinere Stichprobe, um die Pipeline schneller auszuführen (obwohl das ML-Modell dann weniger zu trainieren hat).

Der erste Schritt besteht darin, ein ML-Modell zu trainieren. Die Optimierungspipeline erfordert ein trainiertes Modell. Dies kann mit der Pipeline <a href="http://localhost:20000/active/building_blocks_overview/Train_Xgboost_Multi/">Train_XGBoost_Multi</a> durchgeführt werden. Konfigurieren Sie die Optimierungspipeline unter der Bedingung "quality rating>97" (siehe Abbildung unten) und überprüfen Sie die Ausgabe des Optimierers. Für andere Konfigurationen, siehe Bild und replizieren.

<br>
<p align="center">
<img src="/static/ecoki/img/Optimization_Configuration.png" width="70%" height="50%"> 
<p align="center">
<em> Abb. 1: Benötigte Konfigurationen des Optimierungsbausteins, für diese Übung.</em>
<p>
<br>

<b>Frage 1:</b> Welches sind die optimalen Einstellungen für die einzelnen Maschinenparameter?
<br>
<br>
<b>Frage 2:</b> Die Optimierungsergebnisse enthalten Daten zu drei verschiedenen Schokoladenrezepten. Können Sie herausfinden, wie hoch der unterschiedliche optimierte Energieverbrauch für die verschiedenen Rezepte ist?
Die drei unterschiedlichen Werte von "energy_per_unit_process" in der Grafik sind auf die drei Schokoladenrezepte zurückzuführen. Jeder Wert deutet auf ein bestimmtes Rezept hin, auch wenn es schwierig sein wird, zu erkennen, welcher Wert einem bestimmten Schokoladenrezept entspricht.
<br>
<br>
(Optional) 
<b>Frage 3:</b> Führen Sie die Optimierung erneut durch (indem Sie die Pipeline löschen und neu starten), aber setzen Sie diesmal die Qualitätsbeschränkung auf > 0, so dass sie effektiv nicht eingeschränkt ist. Um wie viel geringer ist der Energieverbrauch, wenn die Qualitätsbeschränkung wegfällt? 
<br>
<br>
<br>
Bildquelle und Bildnachweis: Foto von <a href="https://www.pexels.com/@polina-tankilevitch/">Polina Tankilevitch</a> auf <a href="https://www.pexels.com/photo/close-up-photo-of-assorted-chocolates-4110101/">Pexels</a>
