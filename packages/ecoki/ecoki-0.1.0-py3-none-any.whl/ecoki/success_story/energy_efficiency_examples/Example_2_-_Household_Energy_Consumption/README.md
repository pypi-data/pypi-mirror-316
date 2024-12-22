<b><u>Example #2: Monitor and investigate the energy consumption of a household</u></b>

###### <!-- This is the separator for the contents, above is displayed in popup and below in the details page  -->

## Beispiel: Untersuchung der Energieverbräuche eines Privathaushaltes

In diesem Beispiel wird folgendes Energieeffizienz-Szenario mit einem Beispieldatensatz mit den Energieverbräuche von einem Privathaushalt durchgeführt.

Folgende Pipeline wird verwendet:
[http://localhost:20000/active/building_blocks_overview/Monitor_Energy_Consumption/](http://localhost:20000/active/building_blocks_overview/Monitor_Energy_Consumption/)

## Beschreibung Datensatz

Die Daten bestehen aus dem Energieverbrauch eines Haushalts, Temperatur- und Luftfeuchtigkeitsmessungen in verschiedenen Räumen sowie den Wetterbedingungen.
28 Merkmale und Kennzeichnungen insgesamt:

- Kumulierter Energieverbrauch (Wh) der Geräte in einem Haushalt, sowie der Beleuchtung

- Temperatur und Feuchtigkeitsmessungen von 9 Räumen im Haus

- Verschiedene Wetterbedingungen im Freien

- Ca. 20.000 Datenproben

Datenquelle: [https://archive.ics.uci.edu/ml/datasets/Appliances+energy+prediction#](https://archive.ics.uci.edu/ml/datasets/Appliances+energy+prediction#)


## Aufgabe 

Die Aufgabe ist es die benötigten Spalten aus dem Datensatz auszuwählen, und in dem energy monitoring dashboard dazustellen, um zu untersuchen. 

Die Daten können aus der ecoKI Datenbank (MongoDB) geladen werden, oder aus der Dataverse, sollte Sie nicht Zugriff auf eine eingerichtete ecoKI Datenbank haben (local oder remote). 

- In der Dataverse hat der .csv Datensatz den Namen _"example_2_household_energy"_
- In der ecoKI Datenbank (MongoDB) hat der .json Datensatz den Namen _"Appliances_Energy_Prediction
.energy_data_complete"_

Durch Nutzung der verschiedene verfügbaren Zeitintervalle im energy monitoring dashboard, sollen folgende Fragen beantwortet werden:

**Frage 1:** Finden Sie bestimmte Zeiten am Tag in dem der Energieverbrauch durch Haushaltsgeräte besonders hoch ist?

**Frage 2:** Finden Sie bestimmte Zeiten am Tag in dem der Energieverbrauch durch Beleuchtung besonders hoch ist?

**Frage 3:** Finden Sie bestimmte Tage in der Woche in dem der Energieverbrauch durch Haushaltsgeräte besonders hoch ist?

**Frage 4:** Finden Sie bestimmte Tage in der Woche in dem der Energieverbrauch durch Beleuchtung besonders hoch ist?

Bildquelle und Bildnachweis: Foto von <a href="https://pixabay.com/users/kapa65-61253/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=794364">Karsten Paulick</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=794364">Pixabay</a>