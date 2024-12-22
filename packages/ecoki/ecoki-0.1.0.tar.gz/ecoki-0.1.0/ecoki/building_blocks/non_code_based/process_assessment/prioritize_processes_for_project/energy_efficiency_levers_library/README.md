<b><u>Building block: Prioritize processes for project</u></b>

Overview of different energy efficiency approaches, including examples and links to relevant ecoKI building blocks.

######

# Ansätze zur Energieeffizienz

<table border =4>
  <tr>
    <th><center>Bereich Fertigung</center></th>
    <th><center>Beschreibung des Bereichs</center></th>
    <th><center>Energie- und Ressourceneffizienz-Hebel (E&R)</center></th>
  </tr>
  <tr>
    <td><center>Produktdesign</center></td>
    <td><center>Der Entwurf des Produkts ist der erste Schritt im Produktionsprozess. Dieser Bereich umfasst alle Aktivitäten, die mit dem Produktdesign verbunden sind, wie z. B. die Festlegung von Funktionalität, Formfaktor und Materialien.</center> </td>
    <td>1. <a href = "#top1">Integriertes Produktlebenszyklus-Datenmanagement zur Unterstützung strategischer E&R-Entscheidungen </a></td>
  </tr>
  <tr>
    <td><center>Fertigungssysteme</center></td>
    <td><center>Der Bereich der Fertigungssysteme umfasst alle Prozesse und Maschinen, die zur Herstellung des Produkts verwendet werden.</center> </td>
    <td>2. <a href = "#top2">Optimierung der Betriebsparameter</a></br> 
        <br>3. <a href = "#top3">Optimierung des Materialeinsatzes (weniger Materialien verwenden, nachhaltige Materialien verwenden) </a></br> 
        <br>4. <a href = "#top4">Überwachung des E&R-Verbrauchs </a> </br> 
        <br>5. <a href = "#top5">Qualitätskontrolle zur Minimierung von Materialabfällen/Ausschüssen </a> </br> 
        <br>6. <a href = "#top6">Energieproduktkennzeichnungen für ganzheitliche Verbesserungen der Wertschöpfungskette </a></br> 
        <br>7. <a href = "#top7">Fortschrittliche Automatisierung und Kontrollen für Prozesspräzision und -stabilität </a></br> 
    </td>
  </tr>
  <tr>
    <td><center>Logistik</center></td>
    <td><center>Die Logistikdomäne besteht aus der Logistik innerhalb des Werks (Werkstatt und Lager) sowie an den Werksgrenzen (Eingang und Ausgang).</center> </td>
    <td>8. <a href = "#top8">E&R effiziente Produktionsplanung </a></br> 
        <br>9. <a href = "#top9">Effizientes Werkstattlayout zur Minimierung von Transport- und Wartezeiten </a></br> 
        <br>10. <a href = "#top10">Timing der In- und Outbound-Logistik zur Optimierung der E&R-Effizienz von Produktion und Produktlieferung </a></br>
    </td>
  </tr>
  <tr>
    <td><center>Wartung</center></td>
    <td><center>Die Instandhaltungsdomäne umfasst alle Instandhaltungstätigkeiten innerhalb des Werks sowie außerhalb des Werks für in Gebrauch befindliche Produkte.</center> </td>
    <td>11. <a href = "#top11">Intelligente Wartung zur Vermeidung von Ausfallzeiten und Verlängerung der Lebensdauer der Geräte</a>
 </br> </td>
  </tr>
  <tr>
    <td><center>Energie- und Ressourcenmanagement</center></td>
    <td><center>Der Bereich des E&R-Managements im Werk umfasst die gesamte Bereitstellung von Energie für das Werk, die Nutzung durch das Gebäude sowie den Umgang mit Produktionsnebenprodukten.</center> </td>
    <td>12. <a href = "#top12">Optimierung der technischen Gebäudeausrüstung</a></br> </td>
  </tr>
  <tr>
    <td><center>Recycling</center></td>
    <td><center>Der Bereich Recycling besteht aus Aktivitäten, die darauf abzielen, gebrauchte Produkte und Materialien wieder in den Produktionsprozess einzubringen.</center> </td>
    <td></td>
  </tr>
</table>

<a name = "top3">
## #1 Optimierung der Einsatzstoffe
</a> 
### Kategorie: Fertigungssysteme
### Beschreibung:
Die Optimierung von Einsatzstoffen besteht im Wesentlichen darin, die Menge an ressourcenintensiven oder umweltschädlichen Einsatzstoffen zu verringern, indem entweder generell weniger Einsatzstoffe verwendet oder Einsatzstoffe durch nachhaltigere ersetzt werden. Bei diskreten Bearbeitungsprozessen werden Ressourcen wie Schmiermittel, Druckluft und Prozessgase verbraucht, die erhebliche Auswirkungen auf die Umwelt haben. Im Vergleich zur diskreten Fertigung hat die Prozessindustrie in der Regel mit größeren Mengen und einer größeren Vielfalt an Einsatzstoffen zu tun. Hier kann dieser Hebel eine sehr wichtige Rolle spielen. ML ist für diesen Hebel sehr gut geeignet, da es zur Modellierung der Beziehungen zwischen Inputs, Produktionsparametern und Ressourcenverbrauch verwendet werden kann.

### Typische Voraussetzungen
* Daten über die gemessenen Mengen an verbrauchtem Einsatzmaterial pro Charge oder Produkt 
* Daten zur Qualität der Ergebnisse oder andere Erfolgskriterien (z. B. Zusammensetzung, Materialeigenschaften, Gewicht, Stabilität usw.)

### Typische Ergebnisse
* Weniger verbrauchte Materialien
* Material durch nachhaltiges Material ersetzt
* Qualität erhalten

### Anwendbarkeit von ML
* High

### Beispiel
*Optimierung der Mischfutterproduktion:*
Wie der Name schon sagt, müssen bei der Herstellung von Mischfuttermitteln verschiedene Bestandteile zu einem Futter kombiniert werden, das alle Nährstoffe enthält, die das Vieh braucht. In einer Rezeptur können über hundert verschiedene Zutaten verwendet werden, von Hauptbestandteilen wie Soja und Getreide bis hin zu Spurenmengen von Vitaminen und Aminosäuren. In diesem Beispiel verfügte ein Hersteller über Daten zu den Mengen der Zutaten für jede Futtermittelproduktion sowie über Qualitätsmessungen der meisten Fertigprodukte.  Mithilfe von ML wurde ein Modell erstellt, mit dem Beziehungen zwischen den Mengen der Einsatzstoffe und den daraus resultierenden Qualitätsmessungen abgeleitet werden konnten. Auf der Grundlage dieses Modells wurde dann eine Optimierung durchgeführt, um die Mengen an Einsatzstoffen zu minimieren, was dazu führte, dass Möglichkeiten zur Verringerung des Einsatzes bestimmter Zutaten ermittelt wurden.


<a name = "top2">
## #2 Optimierung der Betriebsparameter
</a>
### Kategorie: Fertigungssysteme
### Beschreibung:
Die Einstellung von Betriebsparametern kann einen erheblichen Einfluss auf die Energie- und Ressourceneffizienz eines Prozesses haben. Durch die Analyse von Daten aus Produktionsläufen lassen sich Zusammenhänge zwischen Energie- und Ressourcenverbrauch, Produktionsqualität und den verschiedenen Parametern ermitteln. Bei Prozessen mit wenigen Parametern ist dies mit einfachen statistischen Analysen recht einfach möglich, während bei komplexen Prozessen mit vielen Parametern fortgeschrittenere Analysen, zum Beispiel mit maschinellem Lernen, erforderlich sind, um Zusammenhänge zu ermitteln. Sobald diese Zusammenhänge bekannt sind, können die Parameter mit dem Ziel optimiert werden, den Energie- und Ressourcenverbrauch bei gleichbleibender Qualität zu minimieren. 

### Typische Voraussetzungen
* Messungen aller (oder der meisten) Prozessparameter
* Daten zur Qualität der Ergebnisse oder andere Erfolgskriterien (z. B. Zusammensetzung, Materialeigenschaften, Gewicht, Stabilität usw.)

### Typische Ergebnisse
* Weniger Energie oder Ressourcen verbraucht
* Qualität erhalten

### Anwendbarkeit von ML
* High

### Beispiel
*Herstellung von Mischfuttermitteln:*
Wie der Name schon sagt, müssen bei der Herstellung von Mischfuttermitteln verschiedene Bestandteile zu einem Futter kombiniert werden, das alle Nährstoffe enthält, die das Vieh braucht. In einer Rezeptur können mehr als hundert verschiedene Zutaten verwendet werden, von Hauptbestandteilen wie Soja und Getreide bis hin zu Spurenmengen von Vitaminen und Aminosäuren. Diese werden dann in mehreren Produktionsschritten mit einer Vielzahl von Betriebsparametern verarbeitet. Ein Hersteller verfügte über Daten zu den Zutaten, den Prozessparametern, dem Energieverbrauch und den Qualitätsmaßnahmen für jede produzierte Charge.  Mithilfe von ML wurde ein Modell erstellt, mit dem sich Beziehungen zwischen all diesen Faktoren ableiten ließen. Anhand dieses Modells wurde dann eine Optimierung durchgeführt, um den Energieverbrauch durch Änderung der Betriebsparameter zu minimieren.
*Metallschneiden:*
Ein Hersteller, der in seiner Produktion in großem Umfang Schaft- und Planfräsen einsetzte, sammelte detaillierte Daten zum Stromverbrauch der Fräser, zur Schnittgeschwindigkeit, zum Vorschub sowie zur Schnitttiefe und -breite. Außerdem wurden Oberflächenqualität und Werkzeugstandzeit genau überwacht. In kontrollierten Versuchsläufen sammelten sie Daten zu verschiedenen Konfigurationen dieser Parameter. Der Vergleich der Ergebnisse zeigte, dass die Schnittgeschwindigkeit im Vergleich zu den derzeit verwendeten Werten erhöht werden konnte, ohne den Stromverbrauch wesentlich zu erhöhen oder die Oberflächenqualität zu verschlechtern, was zu Energieeinsparungen durch kürzere Bearbeitungszeiten führte.


<a name = "top1">
## #3 Integriertes Produktlebenszyklus-Datenmanagement zur Unterstützung strategischer Nachhaltigkeitsentscheidungen
</a> 
### Kategorie: Produktdesign
### Beschreibung:
Produktlebenszyklusdaten umfassen eine Vielzahl von Informationen über ein Produkt, von der Herstellung über die Nutzung bis hin zur Entsorgung (von der Wiege bis zur Bahre). Diese Daten fallen außerhalb der Grenzen eines einzelnen Herstellers an, was ihre Erfassung zu einer Herausforderung macht. Sobald sie jedoch erfasst sind, können sie dem Hersteller neue Erkenntnisse liefern. Software für das Produktlebenszyklusmanagement (PLM) ermöglicht die Verwaltung solcher Daten. Die Integration von PLM-Daten mit Daten zur Produktnachhaltigkeit kann Unternehmen bei der Entscheidung darüber, welche und wie sie ihre Produkte auf nachhaltigere Weise entwerfen und herstellen, wertvolle Unterstützung bieten. Dieser integrierte Ansatz wird manchmal auch als grünes PLM bezeichnet. ML ist in diesem Bereich nicht anwendbar, da die Analysen der PLM-Daten in der Regel eher einfach sind.

### Typische Voraussetzungen
* Zugang zu Daten über den Produktlebenszyklus
* PLM-Software
* Das Produkt sollte einen signifikanten Energie-/Ressourcen-Fußabdruck in der Nutzungsphase haben.

### Typische Ergebnisse
* Einblicke in die Gestaltung von Produkten für mehr Nachhaltigkeit
* Verbesserte Einbeziehung von Umweltpraktiken in das strategische Geschäftsmodell eines Unternehmens
* Verbesserte Nachhaltigkeit des gesamten Lebenszyklus eines Produkts

### Anwendbarkeit von ML
* Niedrig

### Beispiel
Dieser Artikel von SAP, einem bekannten Anbieter von PLM-Software, enthält mehrere Erfolgsbeispiele sowie einen Ausblick auf die Rolle von PLM für eine nachhaltige Fertigung:  
[https://www.sap.com/austria/insights/what-is-product-lifecycle-management.html](https://www.sap.com/austria/insights/what-is-product-lifecycle-management.html)

<a name = "top4">
## #4 Überwachung des Energie- und Ressourcenverbrauchs
</a> 
### Kategorie: Fertigungssysteme
### Beschreibung:
Transparenz über den Energie- und Ressourcenverbrauch ist ein grundlegender Schritt zur Verbesserung der Effizienz eines Produktionssystems. Eine kontinuierliche Überwachung des Verbrauchs kann Daten liefern, die eine Reihe von Erkenntnissen zur Verbesserung der Energie- und Ressourceneffizienz liefern können. So kann die Überwachung beispielsweise Transparenz darüber schaffen, wo und wann im Produktionsprozess ein hoher Verbrauch auftritt, welche Parameter für den Energieverbrauch relevant sind und allgemein das Bewusstsein des Personals für den Energie- und Ressourcenverbrauch schärfen. Die Messung des Energie- und Ressourcenverbrauchs wird auch immer mehr zu einer Anforderung, da die Vorschriften zur Berichterstattung über den CO2-Fußabdruck von Unternehmen und Produkten zunehmen. Energiemanagementsysteme (EMS) sind Software, mit der die gesammelten Verbrauchsdaten verwaltet und angezeigt werden können. Dieser Hebel erfüllt häufig die Voraussetzungen für den Einsatz von ML für weitere Analysen, da die Speicherung der überwachten Verbrauchsdaten eine Grundlage für das Training von ML-Modellen in einigen der anderen Hebel in diesem Leitfaden bildet.

### Typische Voraussetzungen
* Infrastruktur zur Datenerfassung (z. B. Sensoren zur Messung des Energieverbrauchs), die im gesamten Produktionssystem installiert ist

### Typische Ergebnisse
* Transparenz beim Energie- und Ressourcenverbrauch
* Identifizierung von Energiesenken
* Stärkeres Bewusstsein für den Konsum beim Personal
* Möglichkeit zur Berechnung und Meldung von Kohlenstoffemissionen
* Erster Schritt zur Zertifizierung nach ISO 50001

### Anwendbarkeit von ML
* Niedrig

### Beispiel
Beispiel eines großen Fertigungsunternehmens, das eine kommerzielle EMS-Software installiert und kontinuierliche Energieeinsparungen sowie eine ISO 50001-Zertifizierung erzielt hat:  
[https://www.oekotec.de/en/success-stories/deutsche-rockwool-process-optimization/](https://www.oekotec.de/en/success-stories/deutsche-rockwool-process-optimization/)

Beispiel eines großen Automobilherstellers, der nach der Einführung eines UMS seine Energiekosten um 22 % senken konnte: 
[https://www.pwc.de/de/energiewende/assets/energieverbrauch_erfolgreich_steuern.pdf#%5B%7B%22num%22%3A237%2C%22gen%22%3A0%7D%2C%7B%22name%22%3A%22FitR%22%7D%2C-70%2C-7%2C666%2C849%5D](https://www.pwc.de/de/energiewende/assets/energieverbrauch_erfolgreich_steuern.pdf#%5B%7B%22num%22%3A237%2C%22gen%22%3A0%7D%2C%7B%22name%22%3A%22FitR%22%7D%2C-70%2C-7%2C666%2C849%5D)

Ausführliche Informationen und Leitlinien zur Einführung eines UMS, bereitgestellt vom Umweltbundesamt:  
[https://www.umweltbundesamt.de/sites/default/files/medien/1410/publikationen/2020_04_07_energiemanagementsysteme_bf.pdf](https://www.umweltbundesamt.de/sites/default/files/medien/1410/publikationen/2020_04_07_energiemanagementsysteme_bf.pdf)


<a name = "top5">
## #5 Qualitätskontrolle zur Minimierung von Materialabfällen/Ausschüssen
</a> 
### Kategorie: Fertigungssysteme
### Beschreibung:
Die Material- und Ausschussreduzierung und -vermeidung ist ein klassischer Ansatz zur Verbesserung der Energie- und Ressourceneffizienz eines Fertigungssystems und seit langem einer der Hauptschwerpunkte der schlanken Fertigungsmethoden. Im Allgemeinen müssen verschwenderische Prozesse, bei denen beispielsweise unnötige Mengen an Material verbraucht werden oder eine große Anzahl von Fehlern und Nacharbeiten auftritt, zunächst ermittelt und dann verbessert werden. Eine Möglichkeit, Verschwendung aufzudecken, ist die Qualitätskontrolle. Wenn eine große Menge an Qualitätsdaten vorliegt und das zu untersuchende System komplex ist, kann maschinelles Lernen vor allem bei der Durchführung von Qualitätskontrollen helfen. Bilderkennungsalgorithmen können durch die visuelle Identifizierung von Produktfehlern eine Möglichkeit sein, Qualitätsdaten zu sammeln, wenn diese sonst nur schwer zu erfassen sind. Sobald der Materialabfall identifiziert ist, können verschiedene Maßnahmen ergriffen werden, um ihn zu reduzieren, z. B. die Änderung des Prozesses oder die Umrüstung auf effizientere Maschinen. Lässt sich der Abfall nicht reduzieren, können alternativ Optionen zur Wiederverwendung oder zum Recycling der Ressource in Betracht gezogen werden. Zusätzlich zur Bilderkennung kann ML dazu beitragen, die Ursachen für Qualitätsprobleme zu ermitteln, indem die Beziehung zwischen Parametern und Inputs und der Qualität modelliert wird.

### Typische Voraussetzungen
* Qualitätskontrollverfahren vorhanden
* Fähigkeit zur Messung von Materialabfall und Ausschuss

### Typische Ergebnisse
* Identifizierung der Stellen im Produktionsprozess, an denen Materialabfälle entstehen
* Verringerung oder Vermeidung von Materialabfällen
* Geringere Materialkosten
* Reduzierte Mängel

### Anwendbarkeit von ML
* Mittel

### Beispiel
Untersuchung der KI-unterstützten visuellen Qualitätskontrolle:  
[https://www.elunic.com/de/showcase/qualitaetssicherung-presswerk/](https://www.elunic.com/de/showcase/qualitaetssicherung-presswerk/)

Akademisches Papier, das einen Überblick über viele verschiedene Beispiele für die Abfallverringerung gibt:  
[https://doi.org/10.1016/j.jclepro.2017.09.108](https://doi.org/10.1016/j.jclepro.2017.09.108)



<a name = "top6">
## #6 Energieproduktkennzeichnungen für ganzheitliche Verbesserungen der Wertschöpfungskette
</a>
### Kategorie: Fertigungssystem
### Beschreibung:
Die Rückverfolgung des Energieverbrauchs für die Herstellung einzelner Produkte entlang des Herstellungsprozesses ist eine wertvolle Informationsgrundlage für Hersteller sowie für die Akteure entlang der gesamten Wertschöpfungskette. Mit dieser Transparenz auf Produktebene können Verbesserungen der Energieeffizienz des Herstellungsprozesses effektiver ermittelt werden, als wenn der Energieverbrauch nur auf einer höheren Granularitätsebene, z. B. der Werksebene, verfügbar ist. Über den Hersteller hinaus kann die Energieleistung in der gesamten Wertschöpfungskette verbessert werden, da die Transparenz eine bessere Koordinierung zwischen den Beteiligten ermöglicht. Der Schwerpunkt dieses Hebels liegt auf der Erfassung und dem Austausch von Daten über die gesamte Wertschöpfungskette hinweg, nicht auf der Analyse der Daten, so dass ML nicht erforderlich ist.

### Typische Voraussetzungen
* Energieverbrauchsdaten auf Produktebene

### Typische Ergebnisse
* Neue Erkenntnisse über produktspezifische Energieeinsparmöglichkeiten
* Einen Schritt näher an der Berechnung des CO2-Fußabdrucks von Produkten und an der Erlangung von Zertifizierungen (z. B. ISO50001, Carbon Disclosure Project, Greenhouse Gas Protocol)

### Anwendbarkeit von ML
* Niedrig

### Beispiel
NA


<a name = "top8">
## #8 Energie- und ressourceneffiziente Produktionsplanung
</a>
### Kategorie: Logistik
### Beschreibung:
In der Literatur wird bei diesem Ansatz im Allgemeinen zwischen angebots- und nachfrageseitigen Effizienzverbesserungen durch Zeitplanung unterschieden. Auf der Angebotsseite wird die Energiebereitstellung durch die Planung beeinflusst. Beispiele für Methoden sind Nutzungszeiten, Preise für kritische Spitzen, Echtzeitpreise und Lastkurvenstrafen. Auf der Nachfrageseite dient die Planung dazu, den Energie- und Ressourcenbedarf zu senken. Gahm et al. unterscheiden zwischen der Nichtverarbeitungsnachfrage (Energie und Ressourcen, die ohne Wertschöpfung für ein Produkt verwendet werden, z. B. Energiebedarf während Leerlaufzeiten) und der Verarbeitungsnachfrage (Energie und Ressourcen, die zur direkten Umwandlung von Inputs in gewünschte Outputs verwendet werden, z. B. Erhitzen eines Materials, um es umzuwandeln). Entlang der Angebots- und Nachfrageseite unterscheiden Gahm et al. auch, ob die Effizienzgewinne extern (der gesamte Energie- und Ressourcenbedarf der Fabrik wird reduziert) oder intern (der gesamte Energie- und Ressourcenverbrauch bleibt gleich, aber der zeitliche Verlauf des Bedarfs wird geändert, um die Gesamteffizienz zu verbessern) sind. Die Optimierung von Planungsproblemen ist ein häufiger Anwendungsbereich von ML. 

### Typische Voraussetzungen
* Daten zum Produktionsplan
* Daten zum Energieverbrauch während des Produktionsprozesses

### Typische Ergebnisse
* ...

### Anwendbarkeit von ML
* Mittel

### Beispiel
Forschungsprojekt, bei dem ein System zur Produktionsplanung entwickelt wurde, das den Energieverbrauch eines Herstellers um 5 % senken konnte:  
[https://www.cleaner-production.de/index.php/de/themen/umweltfreundliche-erzeugung-speicherung-und-verteilung-von-energie/energiekonzepte/517-energieeinsparungen-in-der-produktion-durch-intelligente-planung#zusammenfassung](https://www.cleaner-production.de/index.php/de/themen/umweltfreundliche-erzeugung-speicherung-und-verteilung-von-energie/energiekonzepte/517-energieeinsparungen-in-der-produktion-durch-intelligente-planung#zusammenfassung)

Beispiel einer Modellfabrik für die Planung der Produktion zur Vermeidung von Preisspitzen:  
[https://eta-fabrik.de/aktuell/news/2021/04/26/energieflexible-produktionsplanung/](https://eta-fabrik.de/aktuell/news/2021/04/26/energieflexible-produktionsplanung/)


<a name = "top9">
## #9 Effizientes Werkstattlayout zur Minimierung von Transport- und Wartezeiten
</a>
### Kategorie: Logistik
### Beschreibung:
Die Anordnung von Maschinen, Arbeitsplätzen, Werkzeugen und anderen Elementen, die für den Betrieb einer Fabrik benötigt werden, gehört zur Betriebsstruktur. Eine Verbesserung der Anordnung der Werkshalle kann den Energieverbrauch des Materialflusses in der gesamten Fabrik erheblich verbessern und den Energieverbrauch in der Fertigung senken, indem die Wartezeiten, in denen die Maschinen im Leerlauf laufen, verringert werden. Verbesserungen können zum Beispiel darin bestehen, Maschinen so zu positionieren, dass das Material nicht so weit transportiert werden muss, was Energie für Transportfahrzeuge spart. Oder die Neuanordnung von Arbeitsplätzen, um die Wartezeiten bei energieintensiven Prozessen zu verringern. Klassischerweise wurden Analysen zur Verbesserung des Layouts manuell durchgeführt. Es gibt einige Softwarelösungen, die kurze Wege und andere Layout-Optimierungen berechnen. ML wird häufig für die Minimierung von Routen eingesetzt, aber weniger für die Optimierung des Layouts, was ein ähnliches, aber anderes Problem ist.

### Typische Voraussetzungen
* Fähigkeit zur Umgestaltung der Werkshalle
* Dokumentation des Materialflusses (Spaghetti-Diagramm und Value Stream Mapping in der Six Sigma-Terminologie)

### Typische Ergebnisse
* Identifizierung und Reduzierung von verschwenderischem Transport und Bewegung 
* Identifizierung und Reduzierung unnötiger Prozesswartezeiten

### Anwendbarkeit von ML
* Niedrig

### Beispiel
In ihrer [Forschungsarbeit](https://doi.org/10.1016/j.promfg.2017.02.020) führen Fahad et al. eine Layout-Optimierung bei einem kleinen Hersteller von Niederspannungsschaltanlagen durch. Sie zeigen eine Verringerung der Energie für den Materialfluss um über 50 %, was zu Einsparungen von mehr als 250 kg CO2 pro Jahr führt.

<!-- <h6><b>&nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp LV manufacturing operations in the facility</b></h6>
<img src="https://www.researchgate.net/publication/315462426/figure/fig1/AS:669052821323776@1536526031091/LV-manufacturing-operations-in-the-facility.png" width="50%" height="30%" title= "LV manufacturing operations in the facility">  -->


<!-- ![New facility layout and its operations](/static/ecoki/img/Pic1_8.png) -->
<!-- <h6><b>&nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp New facility layout and its operations</b></h6>
<img src="Pic1_8.jpg" width="60%" height="30%" title= "New facility layout and its operations">  -->

<br>

<h6><b>&nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp New facility layout and its operations</b></h6>

<p align="center">
<img src="/static/ecoki/img/Pic1_8.png" width="40%" height="20%" title= "New facility layout and its operations"> 
</p>

<br>

Anleitung zur Erstellung eines [Spaghetti-Diagramms](https://www.sixsigmablackbelt.de/spaghetti-diagramm/)  
Leitfaden zur Durchführung eines [Wertstrom-Mappings](https://www.sixsigmablackbelt.de/wertstromanalyse-value-stream-mapping/)


<a name = "top10">
## #10 Timing der In- und Outbound-Logistik zur Optimierung der E&R-Effizienz von Produktion und Produktlieferung
</a>
### Kategorie: Logistik
### Beschreibung:
Die Eingangs- und Ausgangslogistik einer Fabrik ist ein Hebel, der schwer zu nutzen sein kann, da mehrere externe Interessengruppen (Kunden, Lieferanten, Logistikanbieter) beteiligt sind. Der Energieverbrauch dieser Aktivitäten kann jedoch erheblich sein und Verbesserungspotenzial aufweisen. [Wehner](https://doi.org/10.3390/su10061727) nennt mehrere übergeordnete Ansätze, wie z. B. die Vermeidung von Spitzenlieferungen, die Verfolgung einer effizienten Routenplanung und die Annahme von weniger, dafür aber volleren Lieferwagen. Diese Ansätze lassen sich relativ einfach umsetzen, aber je größer und komplexer die ein- und ausgehende Logistik eines Unternehmens ist, desto komplexer wird die Analyse zur Optimierung der Logistik. Bei diesen hohen Komplexitätsgraden kommt das maschinelle Lernen zum Einsatz, insbesondere für die Erstellung von Prognosen (z. B. Lieferzeiten), die wiederum ein effizienteres Logistikmanagement ermöglichen.

### Typische Voraussetzungen
* Vorhandensein umfangreicher Logistikaktivitäten in Ihrem Unternehmen

### Typische Ergebnisse
* Geringere Energiekosten
* Insgesamt verringerte Kosten für die ein- und ausgehende Logistik 

### Anwendbarkeit von ML
* Mittel

### Beispiel


<table border =1 align="center">
  <tr>
    <th><center>Levels</center></th>
    <th><center>Suggested Mitigations</center></th>
  </tr>
  <tr>
    <td><center>Transport</center></td>
    <td><center>Avoid peak deliveries(e.g., incentive delivery during off-peak times)<br> Ensure efficient routing <br>  Track real-time need for transport <br> Consolidate and combine heavy products but little volume with voluminous but light products <br>  Receive fewer but fuller trucks <br> Utilise the whole height of a truck(e.g., double-stack pallets)</center> </td>
  </tr>
  <tr>
    <td><center>Warehousing</center></td>
    <td><center>Standardise foldable and stackable boxes<br>  Label and pack products arriving at distribution centres in advance <br>  Demise alternatives to hanging garments <br> Reduce picking errors <br> Change product designs and sizes to better fit pallets</center>  </td>
  </tr>
  <tr>
    <td><center>Transhipment</center></td>
    <td><center>Order necessary volumes only<br>Use platform and information to support internal and external information flows <br> Concentrate all logistics-related knowledge in one division instead of spreading it over several divisions<br> Use an online marketplace to sell or buy free capacity <br>  Encourage collaboration (e.g., petition the political system)</center></td>
  </tr>
</table>  

<a name = "top11">  
## #11 Intelligente Wartung zur Vermeidung von Ausfallzeiten und Verlängerung der Lebensdauer der Geräte
</a>
### Kategorie: Wartung
### Beschreibung:
Moderne Wartungstechnologien, insbesondere Konzepte wie die vorausschauende Wartung, können eine Reihe von Vorteilen bieten, die die Energie- und Ressourceneffizienz eines Produktionssystems verbessern. Eine verbesserte Wartung kann die Lebensdauer von Anlagen verlängern, indem sie durchgeführt wird, bevor irreparable Schäden auftreten. Eine vorausschauende Wartung kann Störungen verhindern und unerwartete Ausfallzeiten vermeiden helfen, die in der Regel Energie und Ressourcen verschwenden (insbesondere bei energieintensiven Prozessen). Intelligente Instandhaltungsstrategien können auch die Gesamtleistung der Anlage verbessern, indem sie Probleme diagnostizieren, die die Effizienz beeinträchtigen. Fortgeschrittene Instandhaltungsstrategien haben neben den oben beschriebenen Umweltvorteilen auch klare wirtschaftliche Vorteile. ML eignet sich sehr gut für die Ermittlung von Ausfallmustern und -bedingungen und für die Vorhersage künftiger Ausfälle.

### Typische Voraussetzungen
* Anlagen, die mit Hardware zur Erfassung von Betriebsdaten wie Temperaturen, Vibrationen, Druck, Zyklen usw. ausgestattet sind.
* IT-Infrastruktur zur Übermittlung und Erfassung von Betriebsdaten

### Typische Ergebnisse
* Vermeidung von ungeplanten Ausfallzeiten und der damit verbundenen Energie- und Ressourcenverschwendung
* Erhöhte Betriebszeit
* Geringere Wartungskosten

### Anwendbarkeit von ML
* Hoch

### Beispiel
Details zur Zustandsüberwachung und vorausschauenden Wartung:  
[Link](https://www.itwm.fraunhofer.de/de/abteilungen/sys/maschinenmonitoring-und-regelung/predictive-maintenance-instandhaltung-machinelearning.html)

Anbieter von Hardware und Software für die vorausschauende Wartung, der auch verschiedene Anwendungsbeispiele aufführt:  
[Link](https://www.oneprod.com/de/anwendungen/)

<br>

<h6><b>&nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp Predictive Maintenance</b></h6>
<p align="center">
<img src="/static/ecoki/img/Pic1_10.png" width="40%" height="20%"> 
</p>

<br>
Quelle: [https://www.resource-deutschland.de/themen/echtzeitdaten/produktion/](https://www.resource-deutschland.de/themen/echtzeitdaten/produktion/)


<a name = "top12">
## #12 Optimierung der technischen Gebäudeausrüstung
</a>
### Kategorie: Energie- und Ressourcenmanagement
### Beschreibung:
Bei der Verbesserung der Energieeffizienz einer Produktionsanlage können neben den Maschinen auch die Gebäudehülle und die technische Infrastruktur (gemeinhin als technische Gebäudeausrüstung bezeichnet) eine wichtige Rolle spielen. Die technische Gebäudeausrüstung (TBS) ist für Aufgaben wie Temperaturregelung (z. B. Raum- und Prozesswärme), Lüftung und Klimatisierung (z. B. Abluftreinigung, Lufttechnik), Energietechnik (z. B. Energieversorgung, Beleuchtung) oder Wasserversorgung und -aufbereitung zuständig [31, 32]. Eine Studie des US-Energieministeriums ergab, dass im Durchschnitt mehr als 45 % des Energieverbrauchs in der Fertigung auf TBS (Prozesswärme und -kühlung sowie Anlagen) entfallen [33, 34]. Ein üblicher erster Schritt zur Reduzierung des TBS-Energieverbrauchs ist die Erstellung einer Energiewertstromanalyse. Danach können verschiedene der in diesem Dokument beschriebenen Hebel sowie weitere Hebel zur Verbesserung der Effizienz von TBS eingesetzt werden. Die TBS wird als separater Hebel hervorgehoben, da sie häufig als Gemeinkosten betrachtet und bei Effizienzinitiativen weitgehend ignoriert wird, wie Posselt argumentiert. ML spielt bei diesem Hebel in der Regel keine Rolle, da die erforderlichen Analysen in der Regel einfach sind.

### Typische Voraussetzungen
* Möglichkeit zur Messung des Energieverbrauchs der meisten TBS in Ihrer Einrichtung

### Typische Ergebnisse
* Identifizierung der wichtigsten Energieverbraucher außerhalb Ihrer Produktionsprozesse

### Anwendbarkeit von ML
* Niedrig

### Beispiel
[Posselt](https://doi.org/10.1016/j.procir.2014.06.067) präsentiert einen erweiterten Energiewertstrommodellierungsansatz zur Identifizierung aller TBS-Energieverbrauchspunkte in einem Schienenwerk der Siemens AG. Konkret wird ein Gebäude analysiert, in dem verschiedene Arten von Produktions- und Montageprozessen stattfinden (z.B. Schweißen, Fräsen, Schleifen und Inspektion). Sie finden heraus, dass TBS mehr Energie verbrauchen als die eigentlichen 

<br>


<h6><b>&nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp Classification of peripheral systems in value stream box layout</b></h6>
<p align="center">
<img src="/static/ecoki/img/Pic1_11.png" width="30%" height="15%"> 
<p>

<br>

<h6><b>&nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp Direct and indirect energy demands during six process steps comparing three products (A, B, C)</b></h6>
<p align="center">
<img src="/static/ecoki/img/Pic2_11.png" align="center" width="40%" height="20%" > 
<p>

