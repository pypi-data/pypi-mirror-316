<b><u>Modellierung und Optimierung der Prozessparameter eines Produktionsschritts zur Steigerung der Energieeffizienz  für zeitreihenbasierte Daten</u></b>

###### <!-- This is the separator for the contents, above is displayed in popup and below in the details page  -->

## Szenario: Modellierung und Optimierung der Prozessparameter eines Produktionsschritts zur Steigerung der Energieeffizienz für zeitreihenbasierte Daten (statische Analyse auf Basis eines historischen Datensatzes)

Dieses Szenario umfasst die Modellierung eines Prozesses oder Anlagenverhaltens mit anschließender Optimierung der zur Verfügung stehenden Prozessparameter. Primäres Ziel der Optimierung sollte im Idealfall eine direkte Reduzierung des spezifischen Energieeinsatzes oder der spezifischen Gesamtenergiekosten pro Bezugseinheit sein (pro Kilogramm, Stück oder Kubikmeter Produkt). Allerdings ist auch eine indirekte Optimierung der Energieeffizienz durch eine höhere Prozessverfügbarkeit und Prozesssicherheit, höheren Durchsatz, geringerer Ausfallzeiten, geringere Netzauslastung, höheren Anteil erneuerbarer Energien oder weniger Ausschuss durch verbesserte Produktqualität denkbar. Diese Optimierungsziele sind im Rahmen der Definition des Optimierungsziels individuell festlegbar.
Zusätzlich können neben den Optimierungsziel beliebig viele einzuhaltene Randbedingungen definiert werden. Diese können sich auf zu erreichende Kennzahlen der Produktqualität, des Durchsatzes oder der Prozessstabilität beziehen.

Im Rahmen dieses Szenarios wird eine statische Analyse für einen historischen Datensatz (Zeitreihendaten) durchgeführt. Möchte man bei erfolgreicher Durchführung diese Funktionalität Live abrufbar zu Verbesserung der eigenen Produktion einsetzen, ist im Anschluss folgendes Szenario notwendig: (Existiert noch nicht, Entwicklung in Planung) 

Zeitaufwand zur Durchführung des Szenarios: ca. 2 Stunden

Ist dieses Szenario ohne KI-Expertise durchführbar: Derzeit noch nicht, für die Konfiguration der Pipelines wird ein ecoKI-Application-Engineer benötigt. Für die Zukunft ist jedoch eine selbsständige Konfiguration mit GUI-Konfigurationsassistenten geplant.

## Voraussetzungen

Voraussetzung für die erfolgreiche Anwendung dieses Szenarios ist ein Zeitreihen-Datensatz, der Eingangs-, Prozess und Ausgangsdaten eines Prozesses beinhaltet. In diesen Daten müssen alle Einflüsse abgebildet sein, die notwendig sind, um das Verhalten und die Qualität des Prozesses hinreichend genau durch ein Modell beschreiben zu können.
Beispiele für die Eingangs-, Prozess und Ausgangsdaten eines Prozesses sind:

**Eingangsdaten:** Rohstoffdaten, Qualitätsmessungen aus vorherigen Produktionsschritten, Zustandsdaten des zu modellierenden Prozessschritts, Umgebungsbedingungen (z.B. die Außentemperatur)

**Prozessparameter:** Maschinenparameter, Rezepte

**Ausgangsdaten:** Qualitätskennzahlen des Produktes, Spezifische Energieverbrauchskennzahlen bezogen auf eine Produkteinheit (z.B. kWh elektrische pro Tonne, Energiekosten pro Stück, etc.), Spezifische Prozesskennzahlen bezogen auf eine Produkteinheit (z.B. Dauer pro Tonne, Auslastung der Maschine)

Eine weitere Voraussetzung ist die Definition eines Optimierungsziels und optional weiterer Randbedingungen basierend auf den Ausgangsdaten des Prozessschritts. Dies sollte derzeit durch einen ecoKI-Application Engineer vorgenommen werden. Für die Zukunft ist jedoch auch ein Konfigurationsassistent vorgesehen, sodass das Optimierungsziel direkt vom Nutzer eingegeben werden kann.

Für einen Eindruck anhand eines konkreten Beispiels bitte die unten beigefügten Success Story und das Beispiel ansehen.

## Anleitung für die Lösung mit ecoKI

1. Zunächst wird auf Basis des Datensatzes ein Modell erstellt. Dazu bitte die Pipeline Train_Neural_Network_Multi öffnen und über den unten aufgeführten Button starten: [http://localhost:20000/active/building_blocks_overview/Train_Neural_Network_Multi/](http://localhost:20000/active/building_blocks_overview/Train_Neural_Network_Multi/)
2. Gehen Sie in der Navigationsleiste auf "Active Pipelines". Wählen Sie dort die Pipeline "Train_Neural_Network_Multi" aus. Im darauf folgenden Fenster sehen Sie die Bausteine der Pipeline.
3. Falls Sie die Pipeline für unser Beispiel ausführen wollen, führen Sie die Pipeline durch einen Klick auf "Run pipeline" aus. Falls Sie die Pipeline für einen eigenen Datensatz konfigurieren möchten, wählen Sie "Configure run pipeline" und nutzen Sie die Konfigurationsassistenten für jeden Baustein.
4. Wechseln Sie in den Baustein "train_predict_nn_multi" und sehen Sie sich die Ergebnisse der ML-Modellierung für den Testdatensatz an. Sie sehen dort für alle Labels der Modellierung die "echten" Werte des Testdatensatzes sowie die Vorhersage des Modells. Je exakter das Modell, desto besser stimmt der "True"-Wert mit dem "Predicted"-Wert überein. Außerdem haben Sie unter "Model Summary" die mittleren quadratischen Fehler "Mean Squared Error" der Predictions angegeben, mit denen eine Bewertung der Modellierungsgüte möglich ist. 
5. Wenn Sie mit der Performance des Modells zufrieden sind und die Vorhersage nach Ihrer Einschätzung genau genug ist, können Sie nun in den nächsten Schritten mit der Optimierung fortfahren. Falls dies nicht der Fall ist, müssen Sie zunächst das Modell verbessern und erneut mit Schritt 1 starten. Maßnahmen für die Verbesserung sind in folgendem Non-Code-Building-Block beschrieben: (Anleitung noch in der Entwicklung)
6. Für die anschließende Optimierung starten Sie die Pipeline "Run_Parameter_Optimisation_Time_Series_Wrapper", Link: [http://localhost:20000/active/building_blocks_overview/Run_Parameter_Optimisation_Time_Series_Wrapper/](http://localhost:20000/active/building_blocks_overview/Run_Parameter_Optimisation_Time_Series_Wrapper/)
7. Gehen Sie in der Navigationsleiste anschließend auf "Active Pipelines". Wählen Sie dort die Pipeline "Run_Parameter_Optimisation_Time_Series_Wrapper" aus.
8. Falls Sie die Pipeline für unser Beispiel ausführen wollen, führen Sie die Pipeline durch einen Klick auf "Run pipeline" aus. Falls Sie die Pipeline für einen eigenen Datensatz konfigurieren möchten, oder Sie Einstellungen des Optimierers ändern möchten, wählen Sie "Configure run pipeline" und nutzen Sie die Konfigurationsassistenten für jeden Baustein.
9. Wechseln Sie auf den Baustein "Prozessparameter Optimierer". 
10. Sehen Sie sich in dem Baustein die Ergebnisse der Optimierung an. Details zu der angezeigten Visualisierung finden Sie in der Bausteinbeschreibung. Ermitteln Sie die durch die Optimierung vorgenommene Energieeinsparung über die Mittelwerte aus "Descriptive Statistics".
11. Wechseln Sie anschließend auf den Baustein "Optimierung 2D-Visualisierer". 
12. Sehen Sie sich in diesem Baustein die 2D-Plots zur Nachvollziehbarkeit der Optimierungsvorschläge an. Details zu der angezeigten Visualisierung finden Sie in der Bausteinbeschreibung.
13. Für den Fall, dass Sie andere Einstellungen für die Optimierung ausprobieren möchten , gehen Sie zurück zu Schritt 7 und führen die weiteren Schritte erneut aus.

Wenn dieses Szenario erfolgreich durchgeführt wurde, sind folgende Szenarien machbar:

Modellierung und Optimierung der Prozessparameter eines Prozesses zur Steigerung der Energieeffizienz für zeitreihenbasierte Daten (dynamische Analyse): (Derzeit in Planung/Erstellung)

## Beispiel
Als Beispieldaten wird ein Datenstz einer thermischen Behandlungsstation bereitgestellt, mit dem das Szenario durchgeführt werden kann.

Hier der Link: 
[http://localhost:20000/active/building_blocks_overview/Example 4 - Time Series Modeling/](http://localhost:20000/active/building_blocks_overview/Example 4 - Time Series Modeling/)