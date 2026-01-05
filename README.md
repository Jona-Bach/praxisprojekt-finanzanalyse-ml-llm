# Praxisprojekt Bericht Jonathan Bach

---

## 1. Einleitung

### 1.1 Problemstellung

Die Analyse von Aktien und anderen Anlagemöglichkeiten stellt für viele Privatanleger eine erhebliche Herausforderung dar. Insbesondere Einsteiger stoßen auf mehrere grundlegende Probleme:

Erstens fehlt es häufig an einer fundierten Datengrundlage und dem notwendigen Fachwissen, um fundierte Investitionsentscheidungen zu treffen. Die Komplexität der Finanzmärkte und die Vielzahl verfügbarer Kennzahlen überfordern unerfahrene Anleger und erschweren den Einstieg in die eigenständige Aktienanalyse.

Zweitens werden zunehmend Large Language Models (LLMs) für finanzielle Entscheidungen und Investitionsempfehlungen herangezogen, ohne dass ein systematischer Vergleich mit etablierten quantitativen Analysemethoden vorliegt. Es besteht ein Bedarf, die Leistungsfähigkeit von LLMs im Vergleich zu traditionellen Machine Learning-Algorithmen im Kontext der Finanzmarktanalyse zu evaluieren.

Drittens mangelt es vielen Interessierten an Kenntnissen über die Implementierung und Anwendung von Machine Learning-Algorithmen für die Analyse von Finanzdaten. Die technische Einstiegshürde verhindert, dass potenzielle Nutzer von den Möglichkeiten moderner Analysemethoden profitieren können.

### 1.2 Zielsetzung

Ziel dieses Praxisprojekts ist die Entwicklung einer webbasierten Analyseplattform, die Nutzern einen niedrigschwelligen Zugang zur datengestützten Aktienanalyse ermöglicht. Die Plattform verfolgt folgende Kernziele:

1. **Datenintegration und -bereitstellung**: Implementierung einer Funktionalität zum automatisierten Download und zur Verwaltung von Finanzdaten, um Nutzern eine solide Datengrundlage für ihre Analysen zu bieten.

2. **Standardisierte Finanzanalyse**: Bereitstellung grundlegender Analysewerkzeuge und Kennzahlen, die eine erste Bewertung von Aktien ohne tiefgreifende Vorkenntnisse ermöglichen.

3. **Machine Learning-Integration**: Implementierung vorgefertigter Machine Learning-Algorithmen, die es Nutzern erlauben, sowohl heruntergeladene Finanzdaten als auch eigene Datensätze zu trainieren und auszuwerten, ohne selbst Programmierkenntnisse besitzen zu müssen.

4. **Vergleichende Evaluation von Analysemethoden**: Entwicklung einer Funktionalität zum Training und Vergleich von traditionellen Machine Learning-Modellen und Large Language Models auf identischen Datensätzen. Dabei soll insbesondere die Möglichkeit geschaffen werden, zusätzliches Kontextwissen (z.B. politische Informationen) in die LLM-Analyse zu integrieren.

5. **Nutzerunterstützung durch Conversational AI**: Integration eines Chatbot-basierten Sprachassistenten, der Nutzer bei der Bedienung der Plattform unterstützt und den Umgang mit den verschiedenen Analysewerkzeugen erleichtert.

Durch die Kombination dieser Komponenten soll eine Plattform entstehen, die sowohl als Lernumgebung für Einsteiger als auch als praktisches Analysewerkzeug für fortgeschrittene Nutzer dient und gleichzeitig einen empirischen Vergleich verschiedener Analysemethoden im Finanzkontext ermöglicht. Die Plattform wird auf Englisch bereitgestellt, da Englisch die führende Sprache in Wirtschaft und Finanzwesen ist und so eine breite, internationale Nutzung ermöglicht.

### 1.3 Herangehensweise

Die Entwicklung der Analyseplattform erfolgt in einem iterativen Prozess und basiert auf einer modularen Softwarearchitektur, die eine klare Trennung zwischen Frontend, Backend und Datenverarbeitung gewährleistet.

#### 1.3.1 Technologie-Stack

Für die Realisierung des Projekts wird ein moderner Technologie-Stack eingesetzt:

- **Frontend**: Das Benutzerinterface wird mit Streamlit implementiert, einem Framework für die schnelle Entwicklung von datenorientierten Webanwendungen in Python. Dies ermöglicht eine intuitive Bedienoberfläche ohne umfangreiche Webentwicklungskenntnisse.

- **Datenvisualisierung**: Zur grafischen Darstellung von Finanzdaten und Analyseergebnissen wird Plotly verwendet, das interaktive und professionelle Visualisierungen ermöglicht.

- **Machine Learning**: Für die Implementierung der Machine Learning-Algorithmen dient Scikit-Learn als primäres Framework, das eine breite Palette standardisierter Algorithmen und Werkzeuge für das Training und die Evaluation von Modellen bereitstellt.

- **Large Language Model Integration**: Die LLM-Funktionalität wird über Ollama realisiert, das sowohl lokal auf dem System des Nutzers als auch in einem Docker-Container betrieben werden kann.

- **Deployment**: Die gesamte Anwendung wird als Docker-Container bereitgestellt, um Plattformunabhängigkeit und eine unkomplizierte Installation ohne manuelle Konfiguration von Abhängigkeiten zu gewährleisten. Der Quellcode wird über GitHub versioniert und öffentlich zugänglich gemacht.

#### 1.3.2 Datengrundlage

Die Plattform integriert Finanzdaten aus zwei Hauptquellen:

1. **Alpha Vantage API**: Ermöglicht den Zugriff auf umfassende Finanzdaten und erfordert einen individuellen API-Schlüssel, den Nutzer (eingeschränkt) kostenlos beziehen können.

2. **Yahoo Finance API**: Dient als ergänzende, frei zugängliche Datenquelle für historische und aktuelle Marktdaten.

Die verfügbaren Daten umfassen:
- **OHLCV-Daten** (Open, High, Low, Close, Volume) für historische Kursentwicklungen
- **Unternehmensmetriken** wie Kennzahlen zur Fundamentalanalyse
- **Aktuelle Preisinformationen**, die auf Abruf aktualisiert werden können
- **Nutzerdefinierte Datensätze**, die Anwender für eigene Analysen hochladen können

#### 1.3.3 Softwarearchitektur

Das Projekt folgt einer klaren Strukturierung in Frontend und Backend:

- **Backend**: Umfasst die Datenverarbeitungslogik, Datenbankanbindungen, API-Services und die Implementierung der Machine Learning-Algorithmen. Diese Komponenten sind modular aufgebaut und voneinander entkoppelt, um Wartbarkeit und Erweiterbarkeit zu gewährleisten.

- **Frontend**: Das Streamlit-basierte Dashboard greift auf die Backend-Funktionen zu und stellt die Ergebnisse benutzerfreundlich dar.

- **Datenverwaltung**: Alle persistenten Daten werden strukturiert in einem dedizierten Data-Ordner gespeichert, wobei eine Datenbankstruktur die effiziente Verwaltung und Abfrage von Finanzdaten ermöglicht.

#### 1.3.4 Entwicklungsprozess

Die Implementierung erfolgt in folgenden Schritten:

1. **Datenschicht**: Aufbau der Datenbankstruktur und Implementierung der API-Anbindungen für den automatisierten Datenimport.

2. **Backend-Funktionalität**: Entwicklung der Datenverarbeitungslogik und Implementierung der Machine Learning-Algorithmen sowie der LLM-Integration.

3. **Frontend-Entwicklung**: Gestaltung des Streamlit-Dashboards mit Zugriff auf alle Backend-Funktionen und intuitive Nutzerführung.

4. **Integration und Testing**: Verbindung aller Komponenten und Sicherstellung der Funktionalität über verschiedene Deployment-Szenarien (lokal, Docker-Container).

--- 

## 2. Grundlagen

Der folgende Abschnitt beschreibt die theoretischen und fachlichen Grundlagen, die für das Verständnis dieses Projektes notwendig sind. Dabei werden sowohl finanzwirtschaftliche Konzepte als auch technische Grundlagen erläutert, die in der Implementierung der Analyseplattform zur Anwendung kommen.

### 2.1 Finanzmarktgrundlagen

Da diese Plattform auf die Analyse von Finanzdaten ausgelegt ist, ist ein grundlegendes Verständnis zentraler Begriffe und Konzepte der Finanzwirtschaft erforderlich. Die nachfolgend erläuterten Begriffe und Kennzahlen bilden die Basis für die im Dashboard implementierten Analysefunktionen und werden sowohl für grundlegende Datenvisualisierungen als auch als Input für Machine Learning-Algorithmen verwendet.

#### 2.1.1 Grundlegende Begriffe

**OHLCV-Daten**

OHLCV steht für "Open, High, Low, Close, Volume" und bezeichnet die fundamentalen Preisdaten, die die Kursentwicklung einer Aktie innerhalb eines definierten Zeitraums beschreiben. Diese Datenstruktur ist der Standard für die Darstellung von Kursbewegungen an Finanzmärkten:

- **Open**: Der Eröffnungskurs der Aktie zu Beginn der betrachteten Zeitperiode
- **High**: Der höchste Kurs, den die Aktie während der Zeitperiode erreicht hat
- **Low**: Der niedrigste Kurs, den die Aktie während der Zeitperiode erreicht hat
- **Close**: Der Schlusskurs der Aktie am Ende der Zeitperiode
- **Volume**: Die Anzahl der gehandelten Aktien während der Zeitperiode

Diese Datenpunkte werden typischerweise in Form von Candlestick-Charts (Kerzencharts) visualisiert, die eine kompakte Darstellung der Kursbewegungen ermöglichen (Murphy, 1999). OHLCV-Daten bilden die Grundlage für technische Analysen und sind essenziell für die Anwendung von Machine Learning-Algorithmen auf Finanzzeitreihen.

**Aktien**

Aktien (englisch: Stocks oder Shares) sind Unternehmensanteile, die von Kapitalgesellschaften ausgegeben und an Börsen gehandelt werden. *Wenn ein Unternehmen selbst neue Aktien ausgibt und an Investoren verkauft, geschieht dies über den Primärmarkt. Nach dieser ersten Transaktion zwischen den Unternehmen und den Investoren werden die Aktien am Sekundärmarkt unter den Investoren gehandelt, und zwar ohne Mitwirken der Aktiengesellschaft. Wenn man beispielsweise 100 Aktien von Starbucks Coffee kaufen möchte, platziert man eine Order an einer Börse, an der Starbucks unter dem Tickersymbol SBUX gehandelt wird. Man würde die Aktien von jemandem erwerben, der bereits Aktien von Starbucks hält, und nicht von Starbucks selbst.* (Berk & DeMarzo, 2015, S. 32).

Für die vorliegende Plattform sind insbesondere die am Sekundärmarkt gehandelten Aktien relevant, da die verwendeten APIs historische und aktuelle Kursdaten dieser Sekundärmarkttransaktionen bereitstellen.

**Ticker-Symbole**

Ticker-Symbole (oder kurz: Tickers) sind standardisierte Abkürzungen, die zur eindeutigen Identifikation von Wertpapieren an Börsen verwendet werden. Diese Kürzel ermöglichen eine effiziente Referenzierung und Abfrage von Finanzdaten über APIs. Beispiele für Ticker-Symbole sind AMZN (Amazon), GOOGL (Alphabet/Google) oder MSFT (Microsoft). Die Verwendung von Ticker-Symbolen ist zentral für die Datenbeschaffung in dieser Plattform, da sowohl die Alpha Vantage API als auch die Yahoo Finance API Ticker-Symbole als primären Identifikator verwenden.

**Adjusted Close**

Der bereinigte Schlusskurs (Adjusted Close) ist eine Modifikation des regulären Schlusskurses, die Kursanpassungen aufgrund von Dividendenausschüttungen, Aktiensplits und anderen Kapitalmaßnahmen berücksichtigt. Diese Bereinigung ist für historische Analysen von großer Bedeutung, da sie eine verzerrungsfreie Betrachtung der tatsächlichen Wertentwicklung ermöglicht (Yahoo Finance, 2024). Für Machine Learning-Anwendungen wird daher empfohlen, Adjusted Close-Werte anstelle der nominalen Schlusskurse zu verwenden, um Modellverzerrungen zu vermeiden.

#### 2.1.2 Wichtige Finanzkennzahlen

Finanzielle Kennzahlen (Key Performance Indicators, KPIs) dienen der quantitativen Bewertung von Unternehmen und werden sowohl in der Fundamentalanalyse als auch als Features für Machine Learning-Modelle eingesetzt.

**Marktkapitalisierung (Market Capitalization)**

Die Marktkapitalisierung gibt den Börsenwert eines Unternehmens an. *Der Unternehmenswert von börsennotierten Unternehmen zeigt sich im Börsenwert (auch Marktkapitalisierung genannt), der dem Gesamtwert aller börsennotierten Aktien der Aktiengesellschaft entspricht* (Amely & Immenkötter, 2023). 

Die Berechnung erfolgt nach der Formel:

**Marktkapitalisierung = Aktienkurs × Anzahl ausstehender Aktien**

Die Marktkapitalisierung dient als Indikator für die Unternehmensgröße und wird häufig zur Kategorisierung von Aktien verwendet (Large-Cap, Mid-Cap, Small-Cap).

**Kurs-Gewinn-Verhältnis (KGV / P/E Ratio)**

*Das Kurs-Gewinn-Verhältnis (KGV), oder auch Price-Earnings-Ratio (PER), ist der am häufigsten verwendete Multiplikator. Es setzt die Marktkapitalisierung ins Verhältnis zum Jahresüberschuss beziehungsweise – auf eine Aktie bezogen – den Aktienkurs zum Gewinn je Aktie. Das KGV sagt aus, mit dem Wievielfachen des Gewinns ein Unternehmen an der Börse gehandelt wird. Das KGV teilt also Aktionären mit, wie viele Jahre das Unternehmen den angesetzten Gewinn erwirtschaften und ausschütten müsste, bis sie ihren Kaufpreis wieder »reinbekommen«* (Amely & Immenkötter, 2023).

Die Interpretation des KGV ist kontextabhängig: Ein hohes KGV kann auf hohe Wachstumserwartungen hindeuten, während ein niedriges KGV eine Unterbewertung oder geringe Wachstumsaussichten signalisieren kann.

**Kurs-Buchwert-Verhältnis (Price-to-Book Ratio, P/B)**

Das Kurs-Buchwert-Verhältnis vergleicht den aktuellen Börsenkurs einer Aktie mit ihrem bilanziellen Buchwert (Eigenkapital pro Aktie). Die Interpretation erfolgt wie folgt:

- **P/B ≈ 1**: Der Markt bewertet das Unternehmen etwa zu seinem bilanziellen Eigenkapitalwert
- **P/B > 1**: Der Markt erwartet einen Mehrwert durch immaterielle Faktoren wie Markenwert, Wachstumspotenzial oder hohe Profitabilität
- **P/B < 1**: Kann auf eine Unterbewertung, operative Probleme oder bilanzielle Besonderheiten hindeuten

Es ist zu beachten, dass der Buchwert stark von Bilanzierungsvorschriften abhängt und insbesondere bei wissensintensiven Unternehmen mit hohen immateriellen Vermögenswerten weniger aussagekräftig sein kann (Damodaran, 2012).

**Eigenkapitalrendite (Return on Equity, ROE)**

Die Eigenkapitalrendite gibt an, wie effizient ein Unternehmen das eingesetzte Eigenkapital verzinst. Ein höherer ROE indiziert eine höhere Profitabilität im Verhältnis zum Eigenkapital. Die Berechnung erfolgt nach:

**ROE = (Jahresüberschuss / Eigenkapital) × 100%**

Der ROE ist eine zentrale Kennzahl zur Bewertung der Rentabilität und wird häufig im Branchenvergleich herangezogen (Eayrs et al., 2011; Investopedia, 2024a).

**Gewinnmarge (Profit Margin)**

Die Gewinnmarge gibt an, welcher Anteil des Umsatzes als Gewinn verbleibt, nachdem alle Kosten berücksichtigt wurden. Sie wird typischerweise in Prozent ausgedrückt und berechnet sich als:

**Gewinnmarge = (Nettogewinn / Umsatz) × 100%**

Je nach Betrachtung kann zwischen verschiedenen Gewinnmargen unterschieden werden: Bruttogewinnmarge (Gross Margin), operative Gewinnmarge (Operating Margin) und Nettogewinnmarge (Net Profit Margin). Höhere Gewinnmargen deuten auf eine effiziente Kostenstruktur und starke Preissetzungsmacht hin (Investopedia, 2024b).

**Beta-Faktor**

Der Beta-Faktor misst die systematische Volatilität einer Aktie im Verhältnis zu einem Referenzmarkt oder Index. Die Interpretation erfolgt wie folgt:

- **Beta = 1**: Die Aktie schwankt im Durchschnitt genau wie der Referenzindex
- **Beta > 1**: Die Aktie weist höhere Volatilität auf und reagiert stärker auf Marktbewegungen (höheres Risiko)
- **Beta < 1**: Die Aktie ist weniger volatil als der Markt (defensiver Charakter)

*Ein Beta-Faktor (auch kurz Beta oder β) gibt an, wie stark die Aktie im Vergleich zum Markt beziehungsweise zu einem Index schwankt. Man sagt auch, er misst also die Schwankungsintensität (Volatilität) einer Aktie im Vergleich zu einem Index. Hat eine Aktie ein Beta von 1, so verhält sie sich genau wie der Index. Ist das Beta größer als 1, so reagiert die Aktie stärker als der Index. Bei einem Beta zwischen 0 und 1 würde die Aktie auch steigen, wenn der Markt an Wert gewinnt. Der Kursanstieg der Aktie wäre jedoch nicht so groß. Bei einem negativen Beta verhalten sich Index und Aktie gegenläufig: Wenn der Index steigt, verliert die Aktie an Wert und anders herum. Diesen Fall werden Sie aber nur sehr selten antreffen. Beta-Faktoren werden aus der Historie abgeleitet. Sie geben also wieder, wie sich die Aktie in der Vergangenheit im Vergleich zum Markt verhalten hat. Das bedeutet aber nicht, dass dies in Zukunft genauso sein muss* (Amely & Immenkötter, 2023).

Wichtig zu beachten ist, dass der Beta-Faktor vom gewählten Referenzindex, der Branchenzugehörigkeit des Unternehmens und dem betrachteten Zeitraum abhängt. Für Machine Learning-Anwendungen kann Beta als Feature zur Risikoquantifizierung genutzt werden.

#### 2.1.3 Zeitreihenanalyse im Finanzkontext

Finanzdaten weisen typischerweise eine zeitliche Struktur auf, wodurch Zeitreihenanalysemethoden für ihre Verarbeitung besonders relevant sind. Aktienkurse, Handelsvolumina und Finanzkennzahlen werden in regelmäßigen Intervallen erfasst und bilden somit Zeitreihen, deren Analyse spezifische statistische und algorithmische Ansätze erfordert.

Zeitreihenprognosen gehören zu den klassischen Anwendungsfällen des Machine Learning im Finanzbereich. *Eine weitere verbreitete Anwendung ist die Vorhersage von Zeitreihen (wie etwa Aktienkursen)* (Müller & Guido, 2017). Die Besonderheit von Finanzzeitreihen liegt in ihrer Nicht-Stationarität, ihrer hohen Volatilität und der Präsenz von Autokorrelationen, die bei der Modellierung berücksichtigt werden müssen (Box et al., 2015).

Für die vorliegende Plattform sind insbesondere folgende Aspekte der Zeitreihenanalyse relevant:

- **Historische Datenmuster**: Die Identifikation von Trends, Saisonalität und zyklischen Mustern in historischen Kursdaten
- **Feature Engineering**: Die Ableitung zeitabhängiger Features wie gleitende Durchschnitte, Momentum-Indikatoren oder Volatilitätsmaße
- **Sequenzielle Datenverarbeitung**: Die Berücksichtigung der zeitlichen Reihenfolge bei der Modellierung, insbesondere bei der Aufteilung in Trainings- und Testdaten

Diese Konzepte bilden die Grundlage für die Implementierung sowohl der traditionellen Machine Learning-Algorithmen als auch der LLM-basierten Analysen in der Plattform.

Hier ist die überarbeitete und erweiterte Version des Machine Learning-Abschnitts:

---

### 2.2 Machine Learning Grundlagen

Machine Learning (maschinelles Lernen) bezeichnet Verfahren, bei denen Computer aus Daten lernen, ohne explizit programmiert zu werden. Für die vorliegende Plattform sind sowohl die grundlegenden Konzepte des maschinellen Lernens als auch spezifische Algorithmen relevant, die zur Analyse und Prognose von Finanzdaten eingesetzt werden.

#### 2.2.1 Lernparadigmen

**Supervised Learning (Überwachtes Lernen)**

Beim überwachten Lernen wird ein Modell mit bereits gelabelten Daten trainiert, das heißt, zu jedem Eingabedatenpunkt existiert eine bekannte Zielgröße (Label). Das Modell lernt die Beziehung zwischen Eingabemerkmalen und Zielgröße und kann anschließend Vorhersagen für neue, unbekannte Daten treffen (Müller & Guido, 2017). Diese Trainingsmethode eignet sich besonders für Regressionsaufgaben (z.B. Kursprognosen) und Klassifikationsaufgaben (z.B. Auf-/Abwärtsbewegungen von Aktienkursen).

Im Kontext dieser Plattform werden überwachte Lernverfahren eingesetzt, um historische Finanzdaten mit bekannten Kursentwicklungen zu nutzen, um zukünftige Entwicklungen vorherzusagen.

**Unsupervised Learning (Unüberwachtes Lernen)**

Im Gegensatz zum überwachten Lernen erhält das Modell beim unüberwachten Lernen keine vorgegebenen Labels. Stattdessen versucht der Algorithmus, eigenständig Strukturen und Muster in den Daten zu identifizieren (Müller & Guido, 2017). Typische Anwendungen sind Clustering-Verfahren, bei denen Datenpunkte nach Ähnlichkeit gruppiert werden, oder Dimensionsreduktionsverfahren zur Extraktion relevanter Features.

Für Finanzanalysen kann unüberwachtes Lernen beispielsweise zur Gruppierung ähnlicher Aktien nach Verhaltensmustern oder zur Identifikation anomaler Marktbewegungen genutzt werden.

#### 2.2.2 Datenaufteilung und Preprocessing

**Trainings-, Validierungs- und Testdaten**

Eine zentrale Praxis im Machine Learning ist die Aufteilung des verfügbaren Datensatzes in separate Teilmengen. Die **Trainingsdaten** (typischerweise 60-80% des Gesamtdatensatzes) dienen zum Training des Modells. Die **Testdaten** (20-40%) werden ausschließlich zur finalen Evaluation verwendet und bleiben dem Modell während des Trainings unbekannt (Hastie et al., 2009).

Diese strikte Trennung ist essentiell, um Data Leakage zu vermeiden – ein Phänomen, bei dem Informationen aus den Testdaten unbeabsichtigt in den Trainingsprozess einfließen und somit zu überschätzten Leistungsmetriken führen. Für Zeitreihendaten, wie sie bei Finanzdaten vorliegen, ist zusätzlich zu beachten, dass die zeitliche Reihenfolge bei der Aufteilung gewahrt bleiben muss: Trainingsdaten stammen aus einem früheren Zeitraum als Testdaten, um realistische Prognoseszenarien zu simulieren.

**Feature-Skalierung**

Merkmale (Features) in Datensätzen können stark unterschiedliche Wertebereiche aufweisen. Während beispielsweise das Handelsvolumen einer Aktie in Millionen gemessen wird, können prozentuale Renditen im Bereich von wenigen Dezimalpunkten liegen. Diese Heterogenität kann die Konvergenz vieler Machine Learning-Algorithmen verlangsamen oder zu suboptimalen Ergebnissen führen (Géron, 2019).

Feature-Skalierung adressiert dieses Problem durch Transformation aller Merkmale in einen einheitlichen Wertebereich, typischerweise [0, 1] bei Min-Max-Skalierung oder auf Standardnormalverteilung (Mittelwert 0, Standardabweichung 1) bei Standardisierung. Dies ermöglicht eine schnellere Konvergenz und verbesserte Modellperformance, insbesondere bei distanzbasierten Algorithmen und neuronalen Netzen.

**Overfitting und Underfitting**

Ein fundamentales Problem beim maschinellen Lernen ist das Finden der Balance zwischen Modellkomplexität und Generalisierungsfähigkeit. **Overfitting** (Überanpassung) tritt auf, wenn ein Modell die Trainingsdaten zu genau lernt, einschließlich Rauschen und zufälliger Schwankungen, wodurch es auf neuen Daten schlecht abschneidet. Das Modell hat die spezifischen Beispiele "auswendig gelernt", statt allgemeine Muster zu erkennen (Müller & Guido, 2017).

**Underfitting** (Unteranpassung) hingegen liegt vor, wenn ein Modell zu einfach ist, um die zugrundeliegenden Strukturen in den Daten zu erfassen. Es generalisiert zwar gut, aber mit schlechter Gesamtperformance, da es selbst auf den Trainingsdaten keine ausreichende Genauigkeit erreicht.

Die Herausforderung besteht darin, ein Modell zu entwickeln, das komplex genug ist, um relevante Muster zu erkennen, aber nicht so komplex, dass es auf trainingsspezifische Besonderheiten überreagiert. Regularisierungstechniken, Cross-Validation und die Überwachung von Trainings- und Validierungsmetriken helfen, dieses Gleichgewicht zu finden.

#### 2.2.3 Machine Learning-Algorithmen

Im Folgenden werden die in der Plattform implementierten Machine Learning-Algorithmen erläutert, die zur Analyse von Finanzdaten eingesetzt werden.

**Lineare Regression**

Die lineare Regression ist ein grundlegendes Regressionsverfahren, das versucht, eine lineare Beziehung zwischen Eingabemerkmalen und einer kontinuierlichen Zielgröße zu modellieren. *Lineare Modelle zur Regression lassen sich als Regressionsmodelle beschreiben, bei denen die Vorhersage bei einem Merkmal eine Gerade ist, bei zwei Merkmalen ist sie eine Ebene und bei mehr Dimensionen eine Hyperebene* (Müller & Guido, 2017).

Obwohl die Annahme linearer Zusammenhänge restriktiv erscheinen mag, können lineare Modelle bei hochdimensionalen Datensätzen mit vielen Features erstaunlich leistungsfähig sein. *Insbesondere wenn Sie mehr Merkmale als Trainingsdatenpunkte haben, lässt sich jede Zielgröße y ausgezeichnet als lineare Funktion modellieren (auf den Trainingsdaten)* (Müller & Guido, 2017). Im Finanzkontext wird lineare Regression häufig zur Trendidentifikation und als Baseline-Modell für komplexere Verfahren verwendet.

**Decision Tree (Entscheidungsbaum)**

Entscheidungsbäume sind hierarchische Modelle, die auf einer Sequenz von binären Entscheidungen basieren. *Entscheidungsbäume sind weitverbreitete Modelle für Klassifikations- und Regressionsaufgaben. Im Wesentlichen erlernen sie eine hierarchische Folge von Ja/Nein-Fragen, die zu einer Entscheidung führen. Diese Fragen sind ähnlich zu denen im Spiel »20 Fragen«* (Müller & Guido, 2017).

Der Algorithmus teilt den Merkmalsraum rekursiv in Regionen auf, wobei jede Teilung durch eine einfache Entscheidungsregel bestimmt wird (z.B. "Ist der gleitende 50-Tage-Durchschnitt größer als der aktuelle Kurs?"). Diese intuitive Struktur macht Entscheidungsbäume interpretierbar, birgt jedoch die Gefahr des Overfittings, insbesondere bei tiefen Bäumen (Breiman et al., 1984).

**Random Forest**

Random Forest ist ein Ensemble-Verfahren, das die Schwächen einzelner Entscheidungsbäume durch Kombination vieler Bäume adressiert. *Ein Random Forest ist im Wesentlichen eine Menge von Entscheidungsbäumen, wobei sich jeder Baum ein wenig von den übrigen unterscheidet. Die Idee bei Random Forests ist, dass jeder Baum eine recht gute Vorhersage treffen kann, aber voraussichtlich einen Teil der Daten overfittet. Wenn wir viele Bäume konstruieren, die alle gut funktionieren und auf unterschiedliche Weise overfitten, können wir durch Mitteln der Ergebnisse das Overfitting reduzieren* (Müller & Guido, 2017).

Die Diversität der Bäume wird durch zwei Mechanismen erreicht: (1) Jeder Baum wird auf einer zufälligen Teilmenge der Trainingsdaten trainiert (Bootstrap-Sampling), und (2) bei jeder Teilung wird nur eine zufällige Auswahl der verfügbaren Features betrachtet. Durch Aggregation der Vorhersagen aller Bäume (Mittelwertbildung bei Regression, Mehrheitsentscheidung bei Klassifikation) entsteht ein robustes Modell mit hoher Generalisierungsfähigkeit (Breiman, 2001).

**Logistische Regression**

Trotz der irreführenden Bezeichnung handelt es sich bei der logistischen Regression um ein Klassifikationsverfahren, nicht um einen Regressionsalgorithmus. *Die zwei beliebtesten linearen Algorithmen zur Klassifikation sind logistische Regression, die in der Klasse linear_model.LogisticRegression implementiert ist, sowie lineare Support Vector Machines (lineare SVMs), implementiert als svm.LinearSVC (SVC steht für Support Vector Classifier). Trotz seines Namens handelt es sich bei LogisticRegression um ein Klassifikationsverfahren und keinen Regressionsalgorithmus, und wir sollten ihn keinesfalls mit LinearRegression verwechseln* (Müller & Guido, 2017).

Die logistische Regression modelliert die Wahrscheinlichkeit der Zugehörigkeit zu einer Klasse mittels der logistischen Funktion (Sigmoid-Funktion). Im Finanzkontext wird sie häufig für binäre Klassifikationsprobleme eingesetzt, beispielsweise zur Vorhersage, ob eine Aktie steigen oder fallen wird.

**Richtungsklassifikation**

Ein spezifischer Anwendungsfall im Finanzbereich ist die Richtungsklassifikation, bei der vorhergesagt wird, ob der Kurs einer Aktie in einem definierten Zeitraum steigt (Label: 1) oder fällt (Label: 0). Dies transformiert das Regressionsproblem der Kursprognose in ein binäres Klassifikationsproblem. Als Features können technische Indikatoren, Momentum-Kennzahlen oder fundamentale Unternehmenskennzahlen dienen. Die Richtungsklassifikation ist besonders relevant für Handelsstrategien, bei denen die Richtung der Kursbewegung wichtiger ist als die exakte Höhe der Veränderung (Atsalakis & Valavanis, 2009).

#### 2.2.4 Evaluationsmetriken

Die Bewertung der Modellleistung erfolgt anhand quantitativer Metriken, die je nach Aufgabenstellung (Regression oder Klassifikation) variieren.


**Accuracy (Genauigkeit)**: Die Accuracy gibt den Anteil korrekt klassifizierter Instanzen an allen Vorhersagen an. Sie wird berechnet als:

**Accuracy = (Anzahl korrekter Vorhersagen) / (Gesamtanzahl Vorhersagen)**

Obwohl Accuracy intuitiv verständlich ist, kann sie bei unbalancierten Datensätzen irreführend sein. *Die wichtigsten Werte für den Parameter scoring bei der Klassifikation sind accuracy (der voreingestellte Wert), roc_auc für die Fläche unter der ROC-Kurve, average_precision für die Fläche unter der Relevanz-Sensitivitäts-Kurve, f1, f1_macro, f1_micro und f1_weighted für den binären F1-Score und dessen unterschiedlich gewichtete Varianten* (Müller & Guido, 2017).

**Precision (Präzision)**: Die Precision misst den Anteil der tatsächlich positiven Fälle unter allen als positiv klassifizierten Instanzen. Sie ist besonders relevant, wenn falsch-positive Vorhersagen hohe Kosten verursachen:

**Precision = True Positives / (True Positives + False Positives)**

Im Finanzkontext bedeutet eine hohe Precision, dass bei einer Vorhersage "Kursanstieg" dieser auch tatsächlich mit hoher Wahrscheinlichkeit eintritt (Sokolova & Lapalme, 2009).


**Regressionsmetriken**

**Mean Squared Error (MSE)**: Der mittlere quadratische Fehler ist eine der gebräuchlichsten Metriken für Regressionsaufgaben. Er berechnet die durchschnittliche quadratische Abweichung zwischen vorhergesagten und tatsächlichen Werten:

**MSE = (1/n) × Σ(y_i - ŷ_i)²**

Durch die Quadrierung werden größere Fehler stärker gewichtet, was das MSE sensitiv gegenüber Ausreißern macht (Müller & Guido, 2017).

**Root Mean Squared Error (RMSE)**: Der RMSE ist die Quadratwurzel des MSE und hat den Vorteil, in derselben Einheit wie die Zielgröße ausgedrückt zu werden:

**RMSE = √MSE**

Im Finanzkontext repräsentiert der RMSE die durchschnittliche absolute Abweichung der Kursprognose in Währungseinheiten, was die Interpretation erleichtert.

Hier ist die überarbeitete und erweiterte Version des LLM-Abschnitts:


### 2.3 Large Language Models (LLMs)

Large Language Models stellen eine zentrale Komponente dieser Plattform dar und ermöglichen einen innovativen Vergleich zwischen traditionellen Machine Learning-Verfahren und modernen generativen KI-Ansätzen für die Finanzanalyse. Im Folgenden werden die grundlegenden Konzepte von LLMs sowie die verwendete Infrastruktur erläutert.

#### 2.3.1 Grundlagen von Large Language Models

Large Language Models sind auf Basis neuronaler Netze trainierte Modelle, die darauf spezialisiert sind, natürliche Sprache zu verstehen und zu generieren. Diese Modelle basieren überwiegend auf der Transformer-Architektur, die 2017 von Vaswani et al. eingeführt wurde und die Verarbeitung sequenzieller Daten durch Attention-Mechanismen revolutionierte (Vaswani et al., 2017).

**Funktionsweise und Architektur**

LLMs generieren Text durch probabilistische Vorhersage des nächstwahrscheinlichsten Tokens (Wort oder Wortfragment) basierend auf dem vorherigen Kontext. Dieser Prozess wird autoregressive Textgeneration genannt, bei der das Modell iterativ Wahrscheinlichkeitsverteilungen über mögliche nächste Tokens berechnet (Brown et al., 2020). Die Modelle werden mit riesigen Textkorpora trainiert, die oft hunderte Milliarden bis Billionen von Tokens umfassen, und bestehen aus Milliarden von Parametern – Gewichtungen in den neuronalen Netzen, die während des Trainings optimiert werden.

**Fähigkeiten und Anwendungen**

Moderne LLMs zeigen bemerkenswerte Fähigkeiten, die über einfache Textgenerierung hinausgehen:

- **Sprachverständnis und -generierung**: Fähigkeit, menschenähnliche Texte zu produzieren und komplexe sprachliche Strukturen zu verstehen
- **Reasoning und Problemlösung**: Durchführung logischer Schlussfolgerungen und Lösung mathematischer Aufgaben durch im Training erworbene Muster (Wei et al., 2022)
- **Kontextverarbeitung**: Verarbeitung und Integration von Informationen über längere Textpassagen hinweg
- **Few-Shot und Zero-Shot Learning**: Anpassung an neue Aufgaben mit wenigen oder ohne spezifische Trainingsbeispiele (Brown et al., 2020)

Im Kontext dieser Plattform werden LLMs genutzt, um Finanzdaten zu analysieren, Muster zu identifizieren und textbasierte Insights zu generieren. Ein wesentlicher Vorteil gegenüber traditionellen ML-Algorithmen ist die Fähigkeit, zusätzliches Kontextwissen wie politische Ereignisse, Nachrichtenmeldungen oder Unternehmensberichte in die Analyse zu integrieren.

**Abgrenzung zu anderen neuronalen Netzarchitekturen**

Während LLMs auf Textverarbeitung spezialisiert sind, existieren weitere spezialisierte Architekturen für andere Modalitäten:

- **Convolutional Neural Networks (CNNs)**: Optimiert für Bilderkennung und -klassifikation durch hierarchische Feature-Extraktion (LeCun et al., 1998)
- **Generative Adversarial Networks (GANs)**: Bestehend aus Generator und Diskriminator zur Generierung neuer Bilder durch adversariales Training (Goodfellow et al., 2014)
- **Diffusionsmodelle**: Generieren Bilder durch iterative Entrauschung, beginnend von Zufallsrauschen (Ho et al., 2020)

Die Transformer-Architektur, auf der die meisten modernen LLMs basieren, hat sich aufgrund ihrer Skalierbarkeit und der Effizienz des Attention-Mechanismus als besonders erfolgreich für Sprachmodellierung erwiesen (Devlin et al., 2019).

#### 2.3.2 Ollama als lokale LLM-Infrastruktur

Die Größe moderner LLMs stellt eine erhebliche Herausforderung für deren Einsatz dar. Modelle wie GPT-3 mit 175 Milliarden Parametern oder größere Open-Source-Modelle können mehrere hundert Gigabyte Speicherplatz beanspruchen und erfordern für die Inferenz erhebliche Rechenressourcen, typischerweise spezialisierte GPU-Hardware (Brown et al., 2020). Dies macht den Einsatz solcher Modelle auf consumer-grade Hardware ohne weitere Optimierungen praktisch unmöglich.

**Ollama: Lokale LLM-Ausführung**

Ollama ist eine Open-Source-Plattform, die es ermöglicht, Large Language Models lokal auf Standard-Hardware auszuführen. Die Plattform abstrahiert die technische Komplexität der Modellausführung und implementiert verschiedene Optimierungstechniken, um LLMs auch auf weniger leistungsfähiger Hardware nutzbar zu machen (Ollama, 2024).

**Optimierungstechniken**

Ollama nutzt mehrere Verfahren zur Reduktion der Ressourcenanforderungen:

1. **Quantisierung**: Reduzierung der numerischen Präzision der Modellparameter von typischerweise 32-Bit oder 16-Bit Gleitkommazahlen auf 8-Bit, 4-Bit oder sogar niedrigere Präzision. Dies reduziert den Speicherbedarf und beschleunigt Berechnungen bei nur geringem Genauigkeitsverlust (Dettmers et al., 2022). Beispielsweise kann ein Modell mit 7 Milliarden Parametern durch 4-Bit-Quantisierung von circa 28 GB auf etwa 4 GB komprimiert werden.

2. **CPU-Fallback**: Ollama ermöglicht die Ausführung von Modellen auf CPUs, wenn keine GPU verfügbar ist, wenngleich mit reduzierter Inferenzgeschwindigkeit. Dies erweitert den Nutzerkreis erheblich, da keine spezialisierte Hardware vorausgesetzt wird.

3. **Dynamische Ressourcenverwaltung**: Intelligente Verwaltung des verfügbaren Arbeitsspeichers und Auslagerung nicht aktiv genutzter Modellteile zur Optimierung der Ressourcennutzung.

**Integration in die Plattform**

In der vorliegenden Plattform wird Ollama sowohl als lokale Installation auf dem System des Nutzers als auch als containerisierte Lösung innerhalb der Docker-Umgebung unterstützt. Dies bietet Nutzern Flexibilität in der Deployment-Strategie und ermöglicht den Einsatz von LLMs ohne Abhängigkeit von Cloud-basierten API-Services, was Datenschutz- und Kostenvorteile mit sich bringt.

Die Wahl des spezifischen LLM-Modells liegt beim Nutzer und sollte basierend auf den verfügbaren Hardwareressourcen getroffen werden: Kleinere Modelle (z.B. 7 Milliarden Parameter) laufen auf Standard-Hardware mit 16-32 GB RAM, während größere Modelle (13+ Milliarden Parameter) entsprechend leistungsfähigere Systeme erfordern.

#### 2.3.3 LLMs im Finanzkontext

Die Anwendung von LLMs für Finanzanalysen ist ein aufstrebendes Forschungsgebiet. Im Gegensatz zu traditionellen Machine Learning-Modellen, die primär numerische Features verarbeiten, können LLMs sowohl quantitative Daten als auch qualitative Textinformationen integrieren. Dies ermöglicht beispielsweise die Berücksichtigung von Earnings Call Transcripts, Nachrichtenartikeln oder Unternehmensberichten in der Analyse (Wu et al., 2023).

Ein weiterer Vorteil liegt in der Few-Shot-Lernfähigkeit: LLMs können durch geeignete Prompt-Gestaltung (Prompt Engineering) auf spezifische Analyseaufgaben ausgerichtet werden, ohne dass ein vollständiges Retraining notwendig ist. Dies senkt die Einstiegshürde für Nutzer ohne tiefgreifende Machine Learning-Kenntnisse erheblich.

Die vorliegende Plattform nutzt diese Eigenschaften, um Nutzern einen direkten Vergleich zwischen quantitativen ML-Ansätzen und qualitativ-angereicherten LLM-Analysen zu ermöglichen. Dabei bleibt zu beachten, dass LLMs keine deterministischen Prognosen liefern, sondern probabilistische Ausgaben generieren, deren Interpretation Domänenwissen erfordert.

---
## 3. Datenbeschreibung

### 3.1 Datenquellen

Die im Finanzdashboard verarbeiteten Daten stammen aus (i) externen Marktdaten- und Fundamentaldatenquellen sowie (ii) nutzerseitig bereitgestellten Dateien. Als externe Anbieter werden **Yahoo Finance**, **Alpha Vantage** und **Financial Modeling Prep (FMP)** eingesetzt. Die externen Quellen liefern primär **historische Kurszeitreihen** in Form von **OHLCV-Daten** (Open, High, Low, Close, Volume). Abhängig vom Anbieter stehen darüber hinaus **Unternehmensmetadaten** und **fundamentale Kennzahlen** zur Verfügung (z. B. Unternehmenskennzahlen über Alpha Vantage).

- **Yahoo Finance**: Bereitstellung historischer OHLCV-Zeitreihen sowie ausgewählter Unternehmensinformationen (z. B. Stammdaten/Profilinformationen, abhängig von der Abfrage).
- **Alpha Vantage**: Bereitstellung zeitnaher (daily) Kursdaten und zusätzlicher Unternehmensmetriken/Fundamentaldaten (anbieter- und endpointabhängig).
- **FMP**: Es liegen JSON-Datensätze aus FMP vor. Diese sind im aktuellen Implementierungsstand **noch nicht produktiv in die Datenpipeline integriert**, können jedoch bei Bedarf über eine entsprechende Import- und Harmonisierungsschicht angebunden werden.

Zusätzlich können Nutzerinnen und Nutzer eigene Datensätze im Format **CSV** oder **Excel (XLS/XLSX)** hochladen, um individuelle Analysen durchzuführen oder alternative Datenquellen einzubinden.


### 3.2 Datenumfang

Der standardmäßig konfigurierte Download-Zeitraum umfasst **1995 bis 2020**. Dieser Zeitraum ist als Default in der Applikation hinterlegt, kann jedoch über eine **Settings-Seite** durch die Nutzerin bzw. den Nutzer angepasst werden. Als Ausgangsuniversum stehen derzeit **ca. 400 Aktien (Ticker-Symbole)** zur Verfügung, für die Daten auf Knopfdruck initial heruntergeladen und gespeichert werden können. Diese liegen als python Liste im Backend vor.

Die Datenbeschaffung erfolgt **nicht automatisiert über einen Scheduler**, sondern wird **manuell** durch Nutzerinteraktion (Button-Klick) ausgelöst. Eine zeitgesteuerte Aktualisierung (z. B. täglich/weekly) ist als mögliche Erweiterung vorgesehen.

Hinsichtlich der Aktualität werden die Quellen im Projekt derzeit unterschiedlich verwendet:
- **Alpha Vantage** wird für **tagesaktuelle (daily) Preisdaten** herangezogen (sofern verfügbar und API-Limits dies zulassen).
- **Yahoo Finance** wird primär für den **historischen Zeitraum (Default 1995–2020)** genutzt.

Nutzerseitig hochgeladene Daten unterliegen in der aktuellen Version **keiner inhaltlichen Plausibilitätsprüfung** (z. B. Vollständigkeit, Datentypen, Frequenz), sondern werden grundsätzlich als „gegeben“ übernommen. Dies ist bewusst so gewählt, um maximale Flexibilität zu ermöglichen, stellt jedoch eine Einschränkung hinsichtlich Datenqualität und Reproduzierbarkeit dar (siehe Abschnitt 3.5).


### 3.3 Datenpipeline und Speicherung

Der Datenimport wird innerhalb der Streamlit-Anwendung durch einen **manuellen Start** (Button-Klick) initiiert. Anschließend erfolgt der Abruf über die jeweiligen APIs, wobei die Verarbeitung in einer iterativen Schleife über definierte Ticker erfolgt. Nach dem Abruf werden die Rohdaten in ein einheitliches Persistenzmodell überführt und dauerhaft gespeichert.

Für die Speicherung wird eine lokale relationale Datenbank (**SQLite**) verwendet. Das Datenbankschema wird über **SQLAlchemy** modelliert und verwaltet. Dadurch werden die Daten
- **persistent** abgelegt (wiederholbar abrufbar),
- **strukturiert** gespeichert (Tabellenmodell),
- und können in nachgelagerten Verarbeitungsschritten (z. B. Feature Engineering, Modelltraining, Dashboard-Visualisierung) effizient abgefragt werden.

### 3.4 Datenaufbereitung

Die Datenaufbereitung ist im aktuellen Projektstand **quell- und datenartabhängig** umgesetzt:

- **Yahoo Finance**: Die über Yahoo Finance bezogenen Daten werden überwiegend als **Rohzeitreihen (OHLCV)** sowie als **Unternehmensinformationen** genutzt und werden in der derzeitigen Version **nur minimal transformiert** (z. B. Format-/Typkonvertierungen beim Import). Eine weitergehende Aufbereitung (z. B. Bereinigung, Outlier-Handling, Harmonisierung auf ein einheitliches Handelskalender-Regime) erfolgt derzeit nicht automatisiert.

- **Alpha Vantage**: Für Alpha-Vantage-Daten existiert ein **Processing-Skript**, das die Rohdaten aus der Datenbank extrahiert und eine Selektion/Filterung vornimmt. Dabei werden insbesondere Ticker/Datenreihen entfernt, die keine ausreichende Datenabdeckung aufweisen (z. B. fehlende Rückgaben für bestimmte Endpunkte). Die bereinigten Daten werden anschließend in eine „bereinigte“ Datenbankstruktur überführt, um sie konsistent für Modellierung und Auswertung bereitzustellen.

- **Umgang mit fehlenden Werten**: Fehlende Werte werden im aktuellen Workflow **in späteren Schritten** (z. B. im Machine-Learning-Skript) weiter behandelt, indem unvollständige Datensätze (Nullwerte) gefiltert bzw. ausgeschlossen werden. Dies reduziert das Risiko fehlerhafter Modellinputs, kann jedoch zu einer Verringerung der Datenbasis führen.

### 3.5 Datenqualität und Limitationen

Durch die Nutzung mehrerer externer Datenanbieter können systematische Unterschiede auftreten, insbesondere hinsichtlich
- **Berechnungsmethoden** (z. B. Adjustments für Splits/Dividenden),
- **Zeitzonen und Handelskalendern**,
- **Aggregationslogiken** (z. B. Definition von Tages-Schlusskursen bei unterschiedlichen Börsenplätzen),
- sowie **Datenlücken** durch API-Restriktionen.

Zusätzlich unterliegen die externen Datenquellen **API-Limits** (z. B. Request-Limits pro Zeiteinheit) und einer anbieterabhängigen **Aktualisierungsfrequenz**. Dies kann die Reproduzierbarkeit von Abrufen (Zeitpunktabhängigkeit) sowie die Vollständigkeit der Daten beeinträchtigen.

Eine weitere Einschränkung besteht darin, dass **nicht für alle Instrumente oder Zeiträume „Adjusted Close“-Preise** verfügbar sind. Je nach Analyseziel (z. B. Renditeberechnung über lange Horizonte) kann dies die Vergleichbarkeit von Zeitreihen beeinflussen. Insgesamt ist die Leistungsfähigkeit der Anwendung daher in hohem Maße von Datenzugang, API-Berechtigungen und Verfügbarkeit der jeweiligen Endpunkte abhängig.
Es werden für die meiste Analyse die adjusted_close Preise verwendet um eine möglichst unverzerrte Datengrundlage zu gewährleisten.

**Regionale Abdeckung**: Bei der Interpretation ist zu berücksichtigen, dass **Alpha Vantage** in der verwendeten Konfiguration primär **US-börsennotierte** Werte zuverlässig abdeckt. Europäische Titel können abhängig vom Symbolschema und der Datenverfügbarkeit unvollständig sein. Dies ist insbesondere relevant, wenn im Dashboard ein gemischtes Universum (USA/EU) betrachtet wird.

**Datentypen:** Viele der gespeicherten Werte werden zunächst als Strings aus den API-Antworten übernommen und in dieser Form in der Datenbank persistiert. Dies kann in späteren Verarbeitungsschritten (z. B. bei Berechnungen oder Modelltraining) zu Problemen führen. Daher werden die betroffenen Felder in der Machine-Learning-Vorverarbeitung in numerische Datentypen konvertiert. Es ist entsprechend zu berücksichtigen, dass Rohdaten teilweise in String-Form in der Datenbank vorliegen **können**.


### 3.6 Nutzerbereitgestellte Daten

Nutzerinnen und Nutzer können eigene Datensätze im Format **CSV** oder **Excel (XLS/XLSX)** hochladen. Nach dem Upload werden die Daten in eine separate Datenbankstruktur integriert und stehen anschließend als Datenbasis für
- explorative Analysen und Visualisierungen im Dashboard,
- die Machine-Learning-Komponenten (z. B. Modelltraining/Inference),
- sowie die LLM-basierte Analyse (z. B. textuelle Zusammenfassung/Interpretation)
zur Verfügung.

In der aktuellen Implementierung erfolgt beim Upload lediglich eine grundlegende Einbettung in die Datenhaltung. Eine weiterführende Validierung (Schema-Prüfung, Datumsformat, Pflichtspalten, Duplikatbehandlung) ist als Erweiterung sinnvoll, um Datenqualität und Reproduzierbarkeit zu erhöhen.


### Mini-Schema (Tabellarische Übersicht)

| Tabelle | Quelle | Zweck | Primärschlüssel / Eindeutigkeit | Wichtige Spalten (Auszug) |
|---|---|---|---|---|
| `AV_RAW` | Alpha Vantage | Rohdaten zu Unternehmen (Overview) + ausgewählte Finanzabschluss-Positionen (Cashflow, Balance Sheet, Income Statement) | **Empfohlen:** `symbol` eindeutig (falls pro Symbol nur letzter Stand gespeichert wird) | `symbol`, `asset_type`, `name`, `description`, `cik`, `exchange`, `currency`, `country`, `sector`, `industry`, `address`, `official_site`, `fiscal_year_end`, `latest_quarter`, `market_capitalization`, `ebitda_overview`, `pe_ratio`, `peg_ratio`, `book_value`, `dividend_per_share`, `dividend_yield_raw`, `eps`, `revenue_ttm`, `gross_profit_ttm`, `return_on_equity_ttm`, `beta_raw`, `week_52_high`, `week_52_low`, `moving_average_50_day`, `moving_average_200_day`, `shares_outstanding`, `shares_float`, `percent_insiders`, `percent_institutions`, `dividend_date`, `ex_dividend_date`,  `fiscal_date_ending_cf`, `reported_currency_cf`, `operating_cashflow_raw`, `capital_expenditures_raw`, `dividend_payout`, `change_in_cash_and_cash_equivalents`, `net_income_cf`, `inventory_raw`, `total_liabilities_raw`, `total_shareholder_equity_raw`, `long_term_debt`, `retained_earnings`,`fiscal_date_ending_inc`, `reported_currency_inc`, `total_revenue_raw`, `operating_income_raw`, `ebit`, `ebitda_inc`, `net_income_raw` |
| `AV_PRICING` | Alpha Vantage (`TIME_SERIES_DAILY_ADJUSTED`) | Speicherung des zuletzt verfügbaren Tagesdatensatzes (Daily Adjusted) pro Symbol | **Empfohlen:** Unique (`symbol`, `date`) | `symbol`, `date`, `open`, `high`, `low`, `close`, `adjusted_close`, `volume`, `dividend_amount`, `split_coefficient` |
| `YF_COMPANY_INFO` | Yahoo Finance | Unternehmens-Stammdaten/Profilinformationen | **Empfohlen:** `symbol` eindeutig | `symbol`, `longName`, `shortName`, `sector`, `industry`, `longBusinessSummary`, `address1`, `city`, `state`, `zip`, `country`, `website`, `irWebsite`, `phone`, `fullTimeEmployees`, `companyOfficers`, `overallRisk`, `auditRisk`, `boardRisk`, `compensationRisk`, `shareHolderRightsRisk`, `exchange`, `fullExchangeName`, `region`, `language` |
| `YF_OHLCV` | Yahoo Finance | Historische Kurszeitreihe (OHLCV) | **Empfohlen:** Unique (`symbol`, `date`) | `symbol`, `date`, `open`, `high`, `low`, `close`, `volume`,`adj_close` |


---


## Literatur:
- Berk, Jonathan B.; DeMarzo, Peter M. 2015: Grundlagen der Finanzwirtschaft: Analyse, Entscheidung und Umsetzung, 3., aktualisierte Aufl., Pearson Deutschland GmbH
- Murphy, J. J. (1999). Technical Analysis of the Financial Markets. New York Institute of Finance.
- Damodaran, A. (2012). Investment Valuation. Wiley Finance.
- Box, G. E., Jenkins, G. M., Reinsel, G. C., & Ljung, G. M. (2015). Time Series Analysis: Forecasting and Control. Wiley.
- Yahoo Finance (2024). Adjusted Close Definition.
- Amely, Tobias, and Christine Immenkötter. Investition und Finanzierung Für Dummies, John Wiley & Sons, Incorporated, 2023
- Müller, Andreas C., and Sarah Guido. Einführung in Machine Learning mit Python : Praxiswissen Data Science, o'Reilly, 2017.
- Eayrs, Willis E., et al. Corporate Finance Training : Planung, Bewertung und Finanzierung Von Unternehmen, Schaffer-Poeschel Verlag fur Wirtschaft Steuern Recht GmbH, 2011.
- https://www.investopedia.com
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of Statistical Learning. Springer.
- Géron, A. (2019). Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow. O'Reilly Media.
- Breiman, L. (2001). Random Forests. Machine Learning, 45(1), 5-32.
- Breiman, L., Friedman, J., Stone, C. J., & Olshen, R. A. (1984). Classification and Regression Trees. CRC press.
- Atsalakis, G. S., & Valavanis, K. P. (2009). Surveying stock market forecasting techniques. Expert Systems with Applications, 36(3), 5932-5944.
- Sokolova, M., & Lapalme, G. (2009). A systematic analysis of performance measures for classification tasks. Information Processing & Management, 45(4), 427-437.
- Vaswani, A., et al. (2017). Attention is all you need. Advances in Neural Information Processing Systems, 30.
- Brown, T. B., et al. (2020). Language models are few-shot learners. Advances in Neural Information Processing Systems, 33, 1877-1901.
- Wei, J., et al. (2022). Chain-of-thought prompting elicits reasoning in large language models. Advances in Neural Information Processing Systems, 35.
- Devlin, J., et al. (2019). BERT: Pre-training of deep bidirectional transformers for language understanding. NAACL-HLT.
- LeCun, Y., et al. (1998). Gradient-based learning applied to document recognition. Proceedings of the IEEE, 86(11), 2278-2324.
- Goodfellow, I., et al. (2014). Generative adversarial nets. Advances in Neural Information Processing Systems, 27.
- Ho, J., et al. (2020). Denoising diffusion probabilistic models. Advances in Neural Information Processing Systems, 33.
- Dettmers, T., et al. (2022). LLM.int8(): 8-bit matrix multiplication for transformers at scale. Advances in Neural Information Processing Systems, 35.
- Wu, S., et al. (2023). BloombergGPT: A Large Language Model for Finance. arXiv preprint arXiv:2303.17564.
- Ollama (2024). Ollama Documentation. https://ollama.ai/
