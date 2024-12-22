<b><u>Example #1: Model and optimize parameters of an apple juice production</u></b>

###### <!-- This is the separator for the contents, above is displayed in popup and below in the details page  -->

## Beispiel: Optimierung der Prozessparameter einer Apfelsaftproduktion

In diesem Beispiel wird folgendes Energieeffizienz-Szenario mit einem Beispieldatensatz aus einer Apfelsaft-Produktionsanlage durchgeführt.

Folgende Pipeline wird verwendet:
[http://localhost:20000/active/building_blocks_overview/Run_Parameter_Optimisation/](http://localhost:20000/active/building_blocks_overview/Run_Parameter_Optimisation/)

## Beschreibung Datensatz

Der Datensatz besteht aus 4898 Produktions-Batches einer Apfelsaft-Produktion, für die jeweils folgende Daten pro Produktions-Batch aufgenommen wurden:

- "temperature_cooling_input":
- "flow_meter_input_1":
- "flow_meter_input_2":
- "residual sugar":
- "chlorides":
- "free sulfur dioxide":
- "total sulfur dioxide":
- "process_parameter_1":
- "process_parameter_2":
- "workload_machine_1": Mittlere Auslastung pro Produktionsbatch
- "energy_consumption_production": Der elektrische Energieverbrauch des Batches in kWh pro Batch
- "apple_juice_quality": Die Produktqualität auf einer Skala von 0-10 pro Batch angegeben(0=schlechteste Qualität)

## Aufgabe 

Ihre Aufgabe ist es, durch die Optimierung die **"energy_consumption_production"** zu senken und herauszufinden, wie hoch die prognostizierte Energieeinsparung ist. Als Randbedingung muss jedoch eine **Mindest-Qualität "apple_juice_quality" von 5** eingehalten werden. Ansonsten kann das Produkt nicht verkauft werden. Die Einstellungen für diese Zielfunktion (objective function) wurden bereits vorkonfiguriert. Als zu optimierende Parameter werden die Prozessparameter "process_parameter_1" und "process_parameter_2" definiert. Diese können in festgelegten Grenzen verändert werden. Auch diese wurden bereits vorkonfiguriert. Die Optimierung wird für die ersten 100 Produktions-Batches des Testdatensatzes durchgeführt. 

Der .csv Datensatz finden Sie in der Dataverse, unter dem Namen:

- _"example_1_apple_juice_production"_

Falls keins Ihnen zur verfügung gestellt wurde, muss als erster Schritt ein ML Modell trainiert werden. Die Optimierungs-Pipeline benötigt nämlich ein trainiertes Modell. Dies kann mit eins der Train_XGBoost pipelines z.B. gemacht werden. Wenden Sie sich bitte an ein ecoKI Teammitglied für genaue Anleitungen. 

Versuchen Sie mit Hilfe der Visualisierungen in der Optimierungs-Pipeline folgende Fragen zu beantworten:

**Frage 1:** Wie viel kWh können im Durchschnitt pro Produktionsbatch eingespart werden? (Antwort kann mit dem Baustein "Prozessparameter Optimierer" erhalten werden)

**Frage 2:** Warum wird beim Optimierungsvorschlag für den Batch mit dem "Testdaten_Index"=0 der vorgeschlagene Wert für "process_parameter_1" nicht deutlich über 0.995 gesetzt? Laut Plot könnte man dadurch doch weitere Energieeinsparungen erzielen. (Antwort kann mit dem Baustein "Optimierung_2D_Visualisierer" erhalten werden)

Nachdem diese Fragen beantwortet wurden, kann nun optional eine Änderung der Zielfunktion der Optimierung vorgenommen werden. Dies ist möglich, indem Sie auf "Configure pipeline structure" klicken und in den Settings des Optimierungsbausteins die "objective_function" ändern. Zur Beantwortung der folgenden beiden Fragen soll **ausschließlich der Wert des Feldes "boundary" für die "condition_1" ("apple_juice_quality")** geändert werden. Davon abgesehen bitte keine weiteren Änderungen vornehmen! Durch einen Klick auf "Save Changes and restart pipeline" wird die Pipeline erneut mit den neuen Einstellungen ausgeführt.

**Frage 3:** Um den Apfelsaft als Premiumprodukt verkaufen zu können, ist eine Mindestqualität von 6.0 notwendig. Auf welchen durchschnittlichen Wert würde sich das prognostizierte Energiesparpotenzial verändern, wenn in der Optimierung für die **"apple_juice_quality" ein Wert von mindestens 6.0** vorgegeben wird?

**Frage 4:** Alternativ kann eine Produktlinie auch mit einer Mindest-Qualität von 4.0 verkauft werden. Ergibt sich durch diese Absenkung ein weiteres Energiesparpotenzial?

Bildquelle und Bildnachweis: Foto von <a href="https://unsplash.com/es/@dylu?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Jacek Dylag</a> auf <a href="https://unsplash.com/de/fotos/imEqHThoix8?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
  