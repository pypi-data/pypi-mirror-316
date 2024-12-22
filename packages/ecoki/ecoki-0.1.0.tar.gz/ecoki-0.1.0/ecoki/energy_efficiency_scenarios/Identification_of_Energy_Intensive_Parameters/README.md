<b><u>Identifizierung der relevantesten Features</u></b>

Diese Pipeline verwendet die recursive feature elimination (RFE) für die Merkmalsauswahl.

###### <!-- This is the separator for the contents, above is displayed in popup and below in the details page  -->

# Szenario: Identifizierung der relevantesten Features

Beschreibung:
Beim maschinellen Lernen wählen die Methoden der Merkmalsauswahl einen Teil der wichtigsten features (Spalten) aus einem Datensatz aus. Durch die Verringerung der Anzahl der Merkmale können Algorithmen für maschinelles Lernen effektiver arbeiten (mit geringerem Platz- oder Zeitaufwand) und bessere Ergebnisse liefern. Bestimmte Algorithmen des maschinellen Lernens können durch unnötige Eingangsmerkmale in die Irre geführt werden, was zu einer geringeren Vorhersagegenauigkeit führt. Im Zusammenhang mit der Energieeffizienz von Fertigungsprozessen kann die Feature Auswahl den Nutzern auch zeigen, welche Feature den Energieverbrauch eines untersuchten Prozesses am meisten beeinflussen.
Diese Pipeline verwendet die recursive feature elimination (RFE) für die Merkmalsauswahl. Die RFE-Technik versucht, eine Gruppe wesentlicher Merkmale zu finden, indem sie mit allen Merkmalen im Trainingsdatensatz beginnt und diese systematisch eliminiert, bis die gewünschte Anzahl erreicht ist. Dazu wird der im Kern des Modells verwendete Algorithmus für maschinelles Lernen verwendet, und die Merkmale werden nach ihrer Bedeutung geordnet, wobei die unwichtigsten Merkmale verworfen werden und das Modell mit den verbleibenden Merkmalen neu angepasst wird. Dieser Zyklus wird so lange wiederholt, bis die vorgegebene Anzahl von Merkmalen erreicht ist.
Die Pipeline ermöglicht es dem Benutzer das ML-Modell auswählen, das in der RFE verwendet werden soll, sowie die zu berücksichtigenden Merkmale und Labels auszuwählen.

# Voraussetzungen

Voraussetzung für die erfolgreiche Anwendung dieses Szenarios ist ein tabellarischer Datensatz, der später zum Trainieren eines ML-Modells verwendet werden soll. 

Für einen Eindruck anhand eines konkreten Beispiels bitte die unten beigefügten Success Story bzw das Beispiel ansehen.

# Anleitung für die Lösung mit ecoKI

1. <a href="localhost:20000/active/building_blocks_overview/RFE/">RFE-Pipeine</a> öffnen und pipeline erstellen
2. Nach starten der RFE-Pipeline muss zuerst mit dem Data_Reader Baustein die entsprechende Datenquelle (MongoDB, Dataverse, lokales .csv) und der entsprechende Datensatz ausgewählt werden
3. Wählen Sie im Data_Selector Baustein unter Manualle Konfiguration die Merkmale aus, die in die Analyse einbezogen werden sollen
4. Wählen Sie im RFE Baustein die Feature aus, sowie die Labels die mit Hilfe der Features vorhergesagt werden sollen
5. Wählen Sie die Art der Modellierung aus (Regression oder Klassifikation) sowie das Modell, das in der RFE-Analyse verwendet werden soll
6. Nach Auswahl der RFE Methode wird die Berechnung ausgeführt. Beachten Sie, dass die Berechnung je nach Anzahl der Stichproben (Zeilen) im Datensatz und der Leistung Ihres Computers mehrere Minuten dauern kann, wenn viele Merkmale (z.B. > ~20) ausgewählt sind 
7. Die Ergebnisse werden in einer Tabelle und ein Diagramm angezeigt. Oben sieht man eine Tabelle in der all Feature in "relevant" und "nicht relevant" aufgeteilt sind, sowie ein Rangliste aller Feature absteigend nach "Wichtigkeit". Unten kann man sehen wie die Genauigkeit der Vorhersage sich verbessert mit Zufuhr weitere Feature, sowie der Punkt ab dem das Hinzufügen von weiteren Features keine erhebliche Verbesserung erzeugt.

# Beispiel

Als Beispieldaten wird ein Beispieldatensatz aus einer Simulierten Schokoladenproduktion bereitgestellt

Success stories:
<a href="localhost:20000/active/building_blocks_overview/Example 3 - Chocolate Production/">RFE_Analysis_on_Chocolate_Production</a>

Bildquelle und Bildnachweis: Foto von <a href="https://www.pexels.com/@pixabay/">Pixaby</a> auf <a href="https://www.pexels.com/photo/photo-of-an-industrial-factory-emitting-smoke-247763/">Pexels</a>