<b><u>Überwachung des Energieverbrauchs in der Produktionsanlage</u></b>

Dieses Szenario verwendet Energieverbrauchdaten und erstellt ein Dashboard, in dem die Messungen chronologisch angezeigt werden können. 

###### <!-- This is the separator for the contents, above is displayed in popup and below in the details page  -->

# Szenario: Überwachung des Energieverbrauchs in der Produktionsanlage

Beschreibung:
Dieses Szenario verwendet Energieverbrauchdaten und erstellt ein Dashboard, in dem die Messungen chronologisch angezeigt werden können. 
Die Funktionen umfassen: 
* Möglichkeit, die Zeitskala zu variieren (z. B. um den Energieverbrauch nach Tagen, Monaten oder Wochen zu betrachten)
* Möglichkeit, mehrere Energieverbräuche zu aggregieren (z. B. von verschiedenen Maschinen, um den Gesamtenergieverbrauch zu sehen).

# Voraussetzungen

Voraussetzung für die erfolgreiche Anwendung dieses Szenarios ist ein tabellarischer Datensatz, der Energieverbräuche in der Produktionsanlage als Zeitreihen darstellt. Optimal ist, wenn Energieverbräuche für einzelnen Maschinen vorliegen und denn eine Auflösung  mindestens auf Stundenbasis verfügbar ist. Die Pipeline kann allerdings auch mit höheren oder niedrigeren Auflösungen sowie mit beliebig vielen Energieverbrauchern verwedet werden. Die Energiemessung sollte in Kilowattstunden sein.

Für einen Eindruck anhand eines konkreten Beispiels bitte die unten beigefügten Success Story bzw das Beispiel ansehen.

# Anleitung für die Lösung mit ecoKI

1. Zunächst einmal muss der entsprechende Datensatz bereinigt und in die ecoKI-Datenbank gebracht werden. Dazu bitte die ["Write Data"](http://localhost:20000/active/building_blocks_overview/Store_Data) pipeline
2. Die ["Energy Monitoring Dashboard"](http://localhost:20000/active/building_blocks_overview/Monitor_Energy_Consumption) pipeline starten
3. Die Energieverbrauchsspalten, die in das Dashboard importiert werden sollen, müssen ausgewählt werden.
4. Das Dashboard wird erstellt. 
5. Mit dem Dashboard kann nun interagiert werden: Es können verschiedene Zeiträume betrachtet, verschiedene chronologische Aggregationen vorgenommen und verschiedene Spalten zur Anzeige ausgewählt werden.

Wenn dieses Szenario erfolgreich durchgeführt wurde, sind folgende Szenarien machbar (Link).

# Beispiel

Als Beispieldaten wird ein Datenstz einer Röstmaschine beeitgestellt (TBD when dataset is available)

Success stories:
<a href="http://localhost:20000/active/building_blocks_overview/Household Energy Consumption/">Household Energy Consumption</a>
