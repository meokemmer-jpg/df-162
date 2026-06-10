# df-162 — PRODUKTION [CRUX-MK]
*2026-06-09T11:05:00+00:00 | codex/gpt-5.5*

# DF-162 OPS-Onboarding-Workflow Betriebsbericht

## Zweck und Betriebsrahmen

Die Dark Factory `df-162` liefert einen kontrollierten Betriebsbericht fuer das
Operational-HR-Onboarding. Ihr Auftrag ist eng geschnitten: sie verfolgt
Bearbeitungsfortschritt, Durchlaufzeit, Schrittquote und Alterung offener
Onboardings. Die Factory ist bewusst kein HR-Aktionssystem. Sie schreibt keine
Schritte zurueck, sie setzt keine Haken, sie ueberspringt keine Pflichtpunkte
und sie schliesst keine Onboarding-Elemente automatisch ab. Dieser Read-Only-
Zuschnitt ist der zentrale Schutzmechanismus, weil Personalprozesse fuer
Familie Kemmer nur dann rho-stark sind, wenn Transparenz steigt, ohne dass
falsche Automatisierung Vertrauen oder Compliance belastet.

Der Lauf vom 9. Juni 2026 basiert auf dem im Repository vorhandenen
Produktionsreport `reports/df-162-2026-06-09.json`. Die Pre-Action-
Verification ist erfolgreich, die Laufumgebung ist `mock`, und die
Historienreihe seit dem 10. Mai 2026 zeigt keine Abweichung in den
ausgewiesenen Kennzahlen. Das bedeutet operativ zweierlei: Erstens ist der
Workflow stabil und reproduzierbar. Zweitens ist die aktuelle Sicht eine
kontrollierte Monitoring-Sicht und noch kein Real-Read aus einem HR-System wie
Personio oder BambooHR.

## Aktueller Kennzahlenstand

Zum Stichtag 9. Juni 2026 liegen **14 Pending-Onboardings** vor. Diese Zahl
steht seit allen vorhandenen Reportlaeufen unveraendert im System. Fuer den
Betrieb ist das ein klarer Lastwert: Das OPS-Team haelt dauerhaft vierzehn
aktive Faelle in Bearbeitung, ohne dass der Bestand in den verfuegbaren
Snapshots sinkt. Ein stabil hoher Bestand ist fuer eine Familie oder ein
kleines Unternehmensnetz kein akademischer KPI, sondern ein direkter Hinweis
auf gebundenes Fuehrungs-, HR- und IT-Aufmerksamkeitskapital.

Die Factory weist aktuell **18,5 Tage Completion-Time** aus. Im Datenmodell der
Engine heisst dieses Feld noch `average_onboarding_days`; die fachliche Mission
nennt als Zielgroesse `Median-Completion-Time-Days`. Fuer den Produktionslauf
ist daher sauber festzuhalten: **18,5 Tage sind der derzeit real verfuegbare
Zeitwert der Pipeline**. Er ist ueber alle vorhandenen Reports konstant. Damit
liegt keine Volatilitaet im Messsystem vor, wohl aber eine noch offene
Trennschaerfe zwischen Durchschnitt und Median. Solange kein fallweiser
Rohdatenfeed angeschlossen ist, dient der Wert 18,5 Tage als operativer
Leitwert fuer die Durchlaufzeit.

Die **Step-Completion-Rate liegt bei 82,0 Prozent**. Anders formuliert:
18 Prozent der erwarteten Onboarding-Schritte sind zum Zeitpunkt des Reports
nicht erledigt. Das ist nicht automatisch kritisch, aber es ist hoch genug, um
die Reibung im System sichtbar zu machen. Bei einem Bestand von 14 offenen
Onboardings zeigt diese Quote, dass Blockaden nicht auf Einzelfaelle begrenzt
sind, sondern systematisch an mehreren Stellen auftreten.

Der vierte Pflichtwert ist **Stale-Onboardings-30d**. Im aktuellen Reportmodell
existiert dafuer noch kein separates Zahlenfeld. Deshalb liefert dieser Lauf
keine einzeln gezaehlte Stale-Menge. Betriebsfest ausweisbar ist nur:
**0 explizit als >30 Tage markierte Faelle im Report**, weil der Report derzeit
keinen solchen Marker fuehrt. Diese Null ist damit eine Report-Null, keine
fallweise verifizierte Null. Genau diese Unterscheidung ist fuer Familie
Kemmer wichtig: ein sauber ausgewiesenes Datenloch ist billiger als eine
falsche Sicherheit.

## Blockerbild und Engpasslogik

Der gemeldete Drop-off liegt in der Phase **`equipment_setup`**. Die Top-
Blocker sind `account_access`, `device_delivery` und `manager_intro`. Diese
Reihenfolge ist betrieblich plausibel und wertvoll, weil sie die Verzahnung von
IT, Logistik und Fuehrung sichtbar macht.

`account_access` ist der haerteste Friktionspunkt, weil ohne Berechtigungen
weder produktive Systeme noch Lernstrecken noch Sicherheitsunterweisungen
sauber starten. Jeder Tag Wartezeit auf Accounts verlaengert die
Completion-Time nahezu vollstaendig, weil nachgelagerte Schritte zwar formal
existieren, praktisch aber nicht sinnvoll abschliessbar sind.

`device_delivery` liegt direkt dahinter. Das ist fuer OPS-Onboarding ein
klassischer Multiplikator: Ein fehlendes oder spaet geliefertes Geraet blockiert
Zugriff, Schulung, Kommunikation und Dokumentation gleichzeitig. Schon bei
vierzehn parallelen Faellen kann ein kleiner Hardware-Rueckstand die
Schrittquote deutlich druecken.

`manager_intro` ist der dritte Blocker und oft der am meisten unterschaetzte.
Wenn die fachliche Einordnung spaet kommt, bleibt das Onboarding zwar
administrativ gestartet, aber operativ ungerichtet. Fuer Familie Kemmer ist
dieser Punkt rho-relevant, weil neue Mitarbeitende ohne fruehe Fuehrungs-
Einbettung laenger bis zur produktiven Wertstiftung brauchen.

## Betriebswert fuer Familie Kemmer

Der direkte Wert dieses DF liegt nicht im blossen Messen, sondern in der
Verhinderung teurer Blindstellen. Die Konfiguration veranschlagt einen
jaehrlichen Rho-Korridor von **3.000 bis 14.000 Euro**, die Gesamtschaetzung
liegt bei **8.000 Euro pro Jahr**. Diese Spanne ist fuer den vorliegenden
Scope realistisch, weil `df-162` keinen Umsatz generiert, aber wiederkehrende
Koordinations- und Review-Arbeit komprimiert.

Bei **14 offenen Faellen**, **18,5 Tagen Durchlaufzeit** und **82,0 Prozent
Schrittquote** entsteht der Nutzen auf drei Ebenen. Erstens reduziert sich die
Suchzeit in HR- und OPS-Routinen: statt manuell in Mails, Tickets und
Spreadsheets zu springen, liegt ein konsistenter Lagepunkt vor. Zweitens sinkt
das Risiko, dass ein steckengebliebener Onboarding-Fall erst nach Wochen durch
Zufall auffaellt. Drittens wird Fuehrungszeit geschuetzt, weil Eskalationen auf
sichtbare Engpaesse rueckgebunden werden koennen, statt aus diffusen
Eindruckslagen zu entstehen.

Fuer ein Familienunternehmen oder eine Familien-Holding ist gerade diese
Verlaesslichkeit zentral. Personalvorgaenge greifen schnell in Reputation,
Vertrauen und Teamstabilitaet ein. Eine kleine Factory, die rein beobachtet und
sauber dokumentiert, hat deshalb einen ueberproportionalen Hebel: Sie spart
nicht nur Stunden, sondern senkt die Wahrscheinlichkeit stiller Folgeschaeden
wie doppelte Nachfragen, verlorene Einstiegstage oder informelle Schattenlisten.

## Sofort einsetzbarer Betriebsablauf

Der Produktionsbetrieb von `df-162` ist bereits lauffaehig. Ein Standardlauf
erzeugt unter `reports/df-162-{date}.json` den tagesbezogenen Kennzahlenstand.
Der technische Kern ist bewusst klein gehalten: Locking ueber
`/tmp/df-162.lock`, Dateistabilitaetspruefung fuer Real-Reads, Keyword-Sperre
gegen Entscheidungsrhetorik und ein klarer Mock-Fallback. Diese Architektur
senkt das Fehlerrisiko im Betrieb deutlich, weil Ausfaelle keine Folgeaktionen
in HR-Systemen ausloesen koennen.

Fuer den Tagesbetrieb ergibt sich daraus eine klare Reihenfolge:

1. Start des Engine-Laufs im Mock- oder Real-Read-Modus.
2. Schreiben des Reports mit Zeitstempel und Provenance-Rahmen.
3. Sichtung der vier Kernwerte im OPS-Review.
4. Abgleich der drei Top-Blocker mit den verantwortlichen Funktionen.
5. Manuelle Bearbeitung der betroffenen Onboarding-Faelle ausserhalb des DF.

Der entscheidende Satz fuer den operativen Einsatz lautet: **Die Factory
meldet, Menschen handeln.** Genau dadurch bleibt die Q0-Sperre intakt. Kein
Schritt wird automatisch geschlossen, kein Schritt wird uebersprungen, kein
Onboarding wird durch den DF verfuegt.

## Kontrollluecken und naechste Ausbaustufe im bestehenden Rahmen

Zwei Luecken sind offen sichtbar. Die erste betrifft `Stale-Onboardings-30d`:
die Missionskennzahl existiert, das aktuelle Reportschema fuehrt sie aber noch
nicht als numerisches Feld. Die zweite betrifft `Median-Completion-Time-Days`:
die Fachsprache spricht vom Median, die Engine persistiert aktuell einen
Durchschnittswert. Beide Punkte sind keine kosmetischen Details, sondern
relevant fuer die Genauigkeit des Betriebsbildes.

Trotzdem ist der DF heute einsetzbar, weil der vorhandene Scope bereits
hinreichend Nutzen liefert: offene Faelle, Zeitwert, Schrittquote und
Blockerphase sind vorhanden, stabil und testabgedeckt. Die Erweiterung auf
fallweise Altersklassen und einen echten Median kann spaeter ohne Bruch des
Sicherheitsmodells erfolgen, solange der Read-Only-Charakter erhalten bleibt.

## Fazit

`df-162` steht am 9. Juni 2026 als kontrollierte, produktionsfaehige
Monitoring-Factory fuer OPS-Onboarding bereit. Der aktuelle Stand lautet:
**14 Pending-Onboardings, 18,5 Tage Completion-Time-Leitwert, 82,0 Prozent
Step-Completion-Rate, 0 explizit ausgewiesene >30-Tage-Stale-Faelle im
Reportmodell**. Der operative Engpass sitzt in `equipment_setup`, getragen von
`account_access`, `device_delivery` und `manager_intro`.

Fuer Familie Kemmer liegt der Wert nicht in maximaler Automatisierung, sondern
in kontrollierter Transparenz. Genau das liefert dieser DF: ein belastbares
Lagebild, geringe Eingriffsgefahr, klare Engpasssicht und einen kleinen,
resistenten Prozesskern, der Personal-Onboarding nachvollziehbar macht, ohne
selbst Personalentscheidungen oder Schrittabschluesse zu erzeugen.
