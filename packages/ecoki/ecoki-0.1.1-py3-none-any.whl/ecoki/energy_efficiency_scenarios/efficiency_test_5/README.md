<b><u>nergiebezogene Optimierung der Produktionsplanung</u></b>

Dieses Szenario zielt auf die verbesserte Planung der Maschinenbelegung in Hinblick auf eine Optimierung der Energieeffizienz ab.

###### <!-- This is the separator for the contents, above is displayed in popup and below in the details page  -->

# Szenario: Energiebezogene Optimierung der Produktionsplanung (statische Analyse auf Basis eines historischen Datensatzes)

Beschreibung:
Dieses Szenario zielt auf die verbesserte Planung der Maschinenbelegung in Hinblick auf eine Optimierung der Energieeffizienz ab.

Im Rahmen dieses Szenarios wird eine statische Analyse für einen historischen Datensatz durchgeführt. Möchte man bei erfolgreicher Durchführung diese Funktionalität Live abrufbar zu Verbesserung der eigenen Produktion einsetzen, ist im Anschluss Szenario X (Link) notwendig.

# Voraussetzungen

Voraussetzung für die erfolgreiche Anwendung dieses Szenarios ist ein historischer Datensatz der Produktionsaufträge und deren Belegungszeiten auf den Produktionsmaschinen bzw. Produktionslinien. In diesem Datensatz müssen für jeden Auftrag mindestens folgende Daten zur Verfügung stehen:

- Start des Produktionsauftrags
- Ende des Produktionsauftrags
- Volumen des Produktionsauftrags (Stückzahl, Mengeneinheit, Volumen oder ähnliche Kennzahl zur Beschreibung der Größe des Auftrags)
- Optional: Auf welcher Linie wurde der Auftrag produziert (nur notwendig, falls mehr als eine Produktionslinie vorhanden ist).
- Optional: Artikelnummer oder Bezeichnung pro Auftrag, falls unterschiedliche Produkte hergestellt werden.
- KPIs des produktionsauftrags:
* KPIs bezogen auf den Energieverbrauch oder die Qualität: Spezifischer Energieverbrauch bezogen auf das Volumen des Produktionsauftrags, optional weitere Energiekennzahlen (Druckluft, Gasverbrauch, Wasserverbrauch) bezogen auf das Volumen des Produktionsauftrags
* Qualitäts-KPIs des Produktionsauftrags
* Prozess-KPIs des Produktionsauftrags: Beispielsweise Dauer bezogen auf das Voliumen des Produktionsauftrags


Für alle KPIs, die später im Rahmen der Optimierung beachtet werden sollen, ist ein Modell notwendig, das pro Linie und optional auch pro Artikelnummer bei Angabe des Volumens des Produktionsauftrags eine Vorhersage für alle KPIs treffen kann. Falls dieses Modell nicht vorhanden ist, kann im Rahmen dieses Szenarios ein sehr einfaches lineares Modell in Abhängigkeit von Linie, Produktionsvolumen und Artikel gebildet werden.

Für einen Eindruck anhand eines konkreten Beispiels bitte die unten beigefügten Success Story bzw das Beispiel ansehen.

# Anleitung für die Lösung mit ecoKI

1. Zunächst einmal muss der entsprechende Datensatz bereinigt und in die ecoKI-Datenbank gebracht werden. Dazu bitte die Pipeline X verwenden (Link)
2. Als nächstes wird Pipeline X gestartet und der Datensatz aus der Datenbank ausgewählt. In den nächsten Schritten erfolgt die Konfiguration.
3. Als erstes werden die Spalten für Start des Produktionsauftrags, Ende des Produktionsauftrags und Volumen des Produktionauftrags aus den vorhandenen Spalten des Datensatzes zugeordnet. Dies erfolgt über eine manuelle Eingabe durch den Nutzer.
4. Falls unterschiedliche Artikel produziert werden, erfolgt im nächsten Schritt außerdem die Auswahl der Spalte, in der die Artikelbezeichnung für jeden Auftrag angegeben ist.
5. Falls außerdem unterschiedliche Linien für die Produktion des Auftrags zur Verfügung stehen, erfolgt im nächsten Schritt außerdem die Auswahl der Spalte, in der die Linienzugehörigkeit für jeden Auftrag angegeben ist.
7. Im nächsten Schritt werden alle KPIs aus den bestehenden Spalten ausgewählt, die später für die Optimierung relevant sind.
8. Auf Basis dieser Auswahl werden dann im nächsten Schritt automatisch pro Kombination aus Linie und Artikelnummer lineare Regressionsmodelle für jede KPI erstellt. Sollten zu wenig oder keine Daten für die Kombination aus Linie und Artikelnummer vorhanden sein, werden dafür keine linearen Modelle trainiert. Statdessen wird zusätzlich pro Linie über alle artikelnummern ein zusätzliches lineares Modell pro KPI erstellt, das in solchen Fällen verwendet werden kann.
9. In diesem Schritt ist eine Auswertung der Modellperformance möglich. Dazu wird für jedes Modell der mean Squared Eror errechnet und dem Nutzer grafisch zur Verfügung gestellt.
10. Nun werden durch den Nutzer die Optimierungsziele definiert. Dies ist durch Definition eines primären optimierungsziels und mehrerer Randbedingungen möglich. das primäre Optimierungsziel sollte aus einer Addition der energiebezogenen KPIs bestehen. Im Ideafall werden diese umgerechnet auf Gesamt-kWH pro Produktionsvolumen, alternativ ist bei Verwendung meherer Energieträger auch die Umrechnung auf Gesamtenergiekosten pro Produktionsvolumen vorteilhaft.
Als erste Randbedingung sollte außerdem die Produktionszeit definiert werden. Hier ist es möglich, den zeitlichen Korridor zu definieren, in dem die vom Optimierer vorgeschlagene Produktionszeit von der tatsächlichen Produktionszeit abweichen darf. Dies erfolgt mit einer oberen und unteren Grenze ausgehend von der Staretzeit. Beispiel: obere Grenze Startzeit +12 Stunden, untere Grenze Startzeit - 3 Stunden
Im nächsten Schritt sollte als weitere Randbedingung außerdem definiert werden, welche Artikel auf welcher Linie produziert werden können. Falls ein Artikel auf allen Linien laufen kann, ist dort "Frei" einzutragen, ansonsten eine Liste der erlaubten Linien.
Als nächste Randbedingung ist optional ein Load Balancing möglich. Dies kann dabei unterstützen, Lastspitzen zu vermeiden, das Stromnetz zu entlasten und Netzentgelte zu verringern. Für jede Linie kann dort definiert werden, wieviel kW sie im Betrieb verbraucht. Außerdem kann ein Gesamt-Leistungslimit festgelegt werden. Dieses Limit würde dann bei der Optimierung der Auftragsbelegung vom Optimierer nicht überschritten werden. Vorsicht: Dies kann dazu führen, dass bei großer Auftragslage nicht alle Aufträge in dem festgelegten Zeitrkorridor abgearbeitet werden können. Für diesen Fall ist eine Priorisierung notwendig.
Zuletzt ist es außerdem möglich für den Fall der Optimierung auf gesamtenergiekosten und dem Einkauf der Energie nach Börsenstrompreis auch möglich, eine variable KPI in Abhängigkeit der aktuellen Strombezugskosten zu erstellen. Für diesen Fall werden die Marktpreisdaten der SMARD-Plattform der Bundesnetzagentur verwendet. Dies soll dazu führen, dass Produktion vor allem in Zeiten günstiger Energie geplant wird. Um über diesen Mechanismus Effekte erzielen zu können, sollte das zeitfenster für die Produktion jedoch möglichst groß definiert werden, damit Schwankungen über den Tagesverlauf und über die Wetterbedingungen zur Verfügbarkeit erneuerbarer Energien im Netz ausgenutzt werden können.
11. Nachdem die Optimierungsziele festgelegt wurden, wird nun der Optimierungsvorgang für den hochgeladenen historischen datensatz durchgeführt.
12. Im nächsten Schritt werden die Ergebnisse dem Nutzer grafisch bereitgestellt. Für jede KPI wird über alle Aufträge ermittelt, wie stark sich diese für den Datenauszug erhöht beziehungsweise verringert haben.
13. Sie haben nun einen Eindruck erhalten, wie groß das Potenzial für Einsparungen in der Planung und Belegung Ihrer Produktionsanlagen sein kann. Bei großen Effekten bietet sich an, mehr Energie und Aufwand in eine kontinuierliche Bereitstellung und Integration dieser Schätzung in Ihre internen Abläufe zu investieren. Dafür steht als Ausblick das unten aufgelistete Szenario bereit:

Wenn dieses Szenario erfolgreich durchgeführt wurde, sind folgende Szenarien machbar:
- Kontinuierliche Bereitstellung einer energiebezogenen Optimierung der Produktionsplanung (Link)

# Beispiel

Als Beispieldaten wird ein Datenstz einer Röstmaschine beeitgestellt (TBD when dataset is available)

Success stories:
TBD (Link)
Problem definitions:
TBD (Link)