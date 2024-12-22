<b><u>Modellierung des Energieverbrauchs einer gesamten Produktionsanlage durch Zusammenschalten mehrerer Prozessmodelle</u></b>

In diesem Szenario wird die Zusammenschaltung mehrerer Einzelmodelle von Prozessschritten zu einem Gesamtmodell einer Fabrik oder Produktionsanlage ermöglicht.
###### <!-- This is the separator for the contents, above is displayed in popup and below in the details page  -->

# Szenario: Modellierung des Energieverbrauchs einer gesamten Produktionsanlage durch Zusammenschalten mehrerer Prozessmodelle (statische Analyse auf Basis eines historischen Datensatzes)

Beschreibung:
In diesem Szenario wird die Zusammenschaltung mehrerer Einzelmodelle von Prozessschritten zu einem Gesamtmodell einer Fabrik oder Produktionsanlage ermöglicht. Dabei kann die Struktur der Zusammenschaltung flexibel definiert werden, um das tatsächliche Verhalten der Anlage abbilden zu können. Beispielsweise können Ausgänge von einzelnen Prozessmodellen gleichzeitig Eingang weiterer Modelle des folgenden Prozessschritts sein. Als Ergebnis dieses Szenarios steht ein Gesamtmodell mit entsprechenden Eingangsgrößen bereit, das verschiedene Ausgangsgrößen modellieren kann.

Das Modell kann genutzt werden, um 
a) relevate energiebezogene KPIs der Anlage zu modellieren. Dies wird in diesem Szenario beschrieben und bereitgestellt.
b) diese KPIs auf Basis des erstellen Modells zu optimieren. Dafür ist jedoch ein weiterführendes Szenario notwendig (siehe hier Link)

Im Rahmen dieses Szenarios wird eine statische Analyse für einen historischen Datensatz durchgeführt. Möchte man bei erflgreicher Durchführung diese Funktionalität Live abrufbar zu Verbesserung der eigenen Produktion einsetzen, ist im Anschluss Szenario X (Link) notwendig.

# Voraussetzungen

Voraussetzung für die erfolgreiche Anwendung dieses Szenarios ist das Vorhandensein verschiedener maschinell erlernter Einzelprozessmodelle beziehungsweise der Daten für die Erstellung dieser Einzelprozessmodelle. Für die Modellierung eines Einzelprozesses bitte den Anleitungen in Szenario X folgen (Link). Außerdem muss bekannt sein, wie diese Modelle miteinander verschaltet sein müssen, um das Gesamtanlagenverhalten abbilden zu können.

Für einen Eindruck anhand eines konkreten Beispiels bitte die unten beigefügte Success Story und das Beispiel ansehen.

# Anleitung für die Lösung mit ecoKI

1. Zunächst einmal müssen die verschiedenen Einzelmodelle auf Datenbasis trainiert werden. Dazu bitte den Anleitungen in Szenario X folgen (Link). Dieses muss für jedes der notwendigen Modelle durchgeführt werden.
2. Sobald diese Einzelprozessmodelle trainiert wurden und für die Abfrage der Predictions zur Verfügung stehen, kann mit der Zusammenschaltung begonnen werden. Dazu bitte die Pipeline X auswählen und entsprechend der nächsten Schritte in dieser Anleitung konfigurieren. 
3. Zunächst einmal müssen Sie alle für die Zusammenschaltung verwendeten Modelle auswählen. Dies erfolgt auf Basis der Pipeline IDs der Modelle. 
4. Danach werden alle Eingänge und alle Ausgänge pro ausgewähltem Modell angezeigt. Hier bitte entsprechend alle Ausgänge, die Eingänge in ein weiteres Modell sind, mit diesen Eingängen verbinden.
5. Nachdem alle Verbindungen vorgenommen worden sind, bleiben alle nicht verbundenen Eingänge und Ausgänge als Eingänge und Ausgänge des zusammengeschaltenen Modells übrig.
6. Das Modell ist nun fertig zusammengestellt und kann optional im nächsten Schritt anhand von Beispieldaten evaluiert werden.
7. Für die Performance des Modells auf diesen Beispieldaten steht über das Dashboard eine Visualisierung bereit.
8. Um Vorhersagen des neu aggregierten Modells abfragen zu können, steht eine Predict-Funktionalität bereit. Um diese nutzen zu können, müssen Sie die Predict-Funktion mit einem Datensatz als Argument aufrufen, der alle Eingänge des aggregierten Modells beinhaltet.


Wenn dieses Szenario erfolgreich durchgeführt wurde, sind folgende Szenarien machbar:
- Eine Optimierung des Anlagenmodells durch Variation der einzelner Eingänge des aggregierten Gesamtmodells. (Link)

# Beispiel

Als Beispieldaten wird ein Datenstz einer Recyclinganalge verwendet (TBD when dataset is available). Dieses Beispiel finden Sie hier: Link

Success stories:
TBD (Link)
Problem definitions:
TBD (Link)