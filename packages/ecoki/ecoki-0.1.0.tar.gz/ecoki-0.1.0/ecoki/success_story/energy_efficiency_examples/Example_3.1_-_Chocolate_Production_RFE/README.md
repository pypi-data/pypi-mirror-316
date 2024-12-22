<b><u>Example #3.1: Identify the machine parameters with greatest impact on energy consumption of a chocolate production process using recursive feature elimination</u></b>

###### <!-- This is the separator for the contents, above is displayed in popup and below in the details page  -->

## Beispiel: Identifizierung der Prozessparameter mit größtem Einfluss auf einer Schokoladenproduktion

In diesem Beispiel wird folgendes Energieeffizienz-Szenario mit einem Beispieldatensatz aus einer Simulierten Schokoladenproduktion durchgeführt:

Folgende Pipeline wird verwendet:
[http://localhost:20000/active/building_blocks_overview/RFE/](http://localhost:20000/active/building_blocks_overview/RFE/)

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
- **quality_classification**: *Klassifizierung der Qualität. <94 ist "Low", <95 ist "Good", >95 ist "Best"*

Summen:

- **total_batches_processed**
- **total_energy_consumption**
- **total_energy_per_batch**
- **energy_per_unit_process:** *Normalisieter Wert des Energieverbrauchs pro kG Schokolage*


## Aufgabe 

Ihre Aufgabe ist es, durch eine Recursive Feature Elimination Analyse herauszufinden welche **drei** Maschinenparameter die **"energy_per_unit_process"** am meisten beeinflußen. 

Die Daten können aus der ecoKI Datenbank (MongoDB) geladen werden, oder aus der Dataverse, sollte Sie nicht Zugriff auf eine eingerichtete ecoKI Datenbank haben (local oder remote). 

- In der Dataverse hat der .csv Datensatz den Namen _"example_3_chocolate_production"_
- In der ecoKI Datenbank (MongoDB) hat der .json Datensatz den Namen _"Chocolate_Production
.chocolate_production_v05_sample_180k"_.
\
Ggf. ist eine neuere Version des Datensatzes inzwischen verfügbar. Aktuell sind auch verschiedene "sample" Größen verfügbar; wählen Sie ein kleineres Sample um die Pipeline schneller ausführen zu können (wobei das ML Modell dann weniger dann zum trainieren hat).

**Frage 1:** Welche drei Parameter haben am meisten Einfluss?

**Frage 2:** Schauen Sie die Grafik an. Wie viele der gesamten Parameter scheint das Modell zu benötigen um eine gute Vorhersage zu machen?

(Optional)
**Frage 3:** Wenn Sie die Pipeline mehrmals ausführen, können Sie die Rangfolge der drei Parameter, bzgl. Einfluss, bestimmen


Bildquelle und Bildnachweis: Foto von <a href="https://www.pexels.com/@paola-marchesi-146505364/">Paola Marchesi</a> auf <a href="https://www.pexels.com/photo/metal-grinder-and-visitors-in-a-chocolate-factory-12564493/">Pexels</a>