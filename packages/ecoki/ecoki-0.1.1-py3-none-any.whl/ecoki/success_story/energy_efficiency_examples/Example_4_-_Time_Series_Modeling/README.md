<b><u>Example #7: Model and optimize parameters of a continuous production process</u></b>

###### <!-- This is the separator for the contents, above is displayed in popup and below in the details page  -->

## Beispiel: Optimierung der Prozessparameter einer thermische Behandlungsstation

Im Produktionsprozess wird ein Rohmaterial durch eine thermische Behandlungsstation transportiert, die aus einem Ofen und einem Druckbehälter besteht. Während des Transports wird das Material auf einem Förderband bewegt, dessen Geschwindigkeit sorgfältig gesteuert wird.
Die Temperatur des Ofens und der Druck im Behälter können permanent angepasst werden, um optimale Bedingungen für die thermische Behandlung zu gewährleisten. Diese Stellgrößen beeinflussen direkt die Gesamtleistungsaufnahme des Systems, da höhere Temperaturen und Drücke zu einem höheren Energieverbrauch führen können.
Die Qualität des Endprodukts wird anhand der Oberflächenrauhigkeit bewertet, die durch die Temperatur, den Druck und die Fördergeschwindigkeit während des Prozesses beeinflusst wird. Eine geringere Oberflächenrauhigkeit deutet auf eine höhere Produktqualität hin.
Ziel ist die Minimierung der Gesamtleistungsaufnahme zur Verringerung des Energieverbrauchs bei gleichzeitiger Sicherstellung einer Mindes-Produktqualität.
Dieser Datensatz ermöglicht die Modellierung und Optimierung des kontinuierlichen Produktionsprozesses durch das Verständnis der Beziehungen zwischen den Stellgrößen und den Qualitäts- sowie Leistungsmerkmalen, die eine mit gewisse zeitliche Abhängigkeit und Trägheit haben.

**Folgende Pipelines werden verwendet:**

Für die Modellierung: [http://localhost:20000/active/building_blocks_overview/Train_Neural_Network_Multi/](http://localhost:20000/active/building_blocks_overview/Train_Neural_Network_Multi/)

Für die Optimierung: [http://localhost:20000/active/building_blocks_overview/Run_Parameter_Optimisation_Time_Series_Wrapper/](http://localhost:20000/active/building_blocks_overview/Run_Parameter_Optimisation_Time_Series_Wrapper/)

Die für dieses Beispiel bereits konfigurierten Pipelines sind hier zu finden und können einfach ausgeführt werden:

Für die Modellierung: [http://localhost:20000/active/building_blocks_overview/Example_DS7_Train_Neural_Network_Multi/](http://localhost:20000/active/building_blocks_overview/Example_DS7_Train_Neural_Network_Multi/)

Für die Optimierung: [http://localhost:20000/active/building_blocks_overview/Example_DS7_Run_Parameter_Optimisation_Time_Series_Wrapper/](http://localhost:20000/active/building_blocks_overview/Example_DS7_Run_Parameter_Optimisation_Time_Series_Wrapper/)

**Folgendes ecoKI Szenario wird für dieses Beispiel durchgeführt:**

Die notwendigen Schritte für die Konfiguration der Pipelines und Interpretation der Ergenisse sind in folgendem Szenario als Anleitung erläutert: [http://localhost:20000/active/building_blocks_overview/Optimize Process Parameters Time Series/](http://localhost:20000/active/building_blocks_overview/Optimize Process Parameters Time Series/)


## Beschreibung Datensatz

Der dargestellte Datensatz repräsentiert einen industriellen Produktionsprozess, bei dem verschiedene Stellgrößen kontinuierlich überwacht und aufgezeichnet werden, um ihre Auswirkungen auf die Qualitäts- und Leistungsmerkmale des Prozesses zu analysieren. Die Aufzeichnungen erfolgen im Sekundenabstand (insgesamt 1000 Samples) und umfassen folgende Parameter:

- Temperatur (°C): Dies ist die Temperatur in einem Ofen, die innerhalb eines Bereichs von 100 bis 300 °C variiert. Die Temperaturregelung ist entscheidend für den thermischen Behandlungsprozess des hergestellten Produkts.
- Druck (bar): Der Druck wird in einem Behälter überwacht und liegt zwischen 1 und 20 bar. Der Druck beeinflusst verschiedene Aspekte des Prozesses, wie die Verdichtung und Homogenität des Produkts.
- Fördergeschwindigkeit (m/min): Die Geschwindigkeit, mit der das Material auf einem Förderband transportiert wird, variiert zwischen 0.5 und 3 m/min. Eine korrekte Steuerung der Fördergeschwindigkeit ist wichtig, um einen gleichmäßigen Produktionsfluss zu gewährleisten.
- Gesamtleistungsaufnahme (kW): Dies ist ein Prozessbezogenes Qualitätsmerkmal, das die gesamte Energieaufnahme des Systems in Abhängigkeit von den Stellgrößen (Temperatur, Druck und Fördergeschwindigkeit) darstellt. Die Gesamtleistungsaufnahme wird durch die Effizienz und Effektivität des Produktionsprozesses bestimmt.
- Oberflächenrauhigkeit (µm): Die Oberflächenrauhigkeit des Endprodukts wird gemessen. Sie ist ein entscheidendes Qualitätsmerkmal, das durch die Kombination der Stellgrößen beeinflusst wird und wichtige Informationen über die Beschaffenheit und Güte der Oberfläche liefert.

Der Datensatz enthält 10000 Zeilen und wurde KI-generiert (Quelle: GPT-4).

## Aufgabe 

Ihre Aufgabe ist es, durch die Optimierung der Parameter Druck und Temperatur die **"Gesamtleistungsaufnahme (kW)"** zu senken und herauszufinden, wie hoch die prognostizierte Energieeinsparung im Schnitt ist. Als Randbedingung muss jedoch ein **Höchstwert "Oberflächenrauhigkeit (µm)" von 26** eingehalten werden. Ansonsten kann das Produkt nicht verkauft werden. Die Einstellungen für diese Zielfunktion (objective function) wurden bereits vorkonfiguriert. Die Optimierung wird für die ersten 50 Zeitschritte des Testdatensatzes durchgeführt. 

Der .csv Datensatz finden Sie in der Dataverse, unter dem Namen:

- _"DS7_Time_Series_Production"_

Versuchen Sie mit Hilfe der Visualisierungen in der Optimierungs-Pipeline folgende Fragen zu beantworten:

**Frage 1:** Wie viel % Energie können im Durchschnitt eingespart werden? (Antwort kann mit dem Visualizer im Baustein "Prozessparameter Optimierer" erhalten werden)

Bildquelle und Bildnachweis: GPT-4
  