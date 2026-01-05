# Praxisprojekt Bericht Jonathan Bach

---

## Inhaltsverzeichnis
- [1. Einleitung](#1-einleitung)
  - [1.1 Problemstellung](#11-problemstellung)
  - [1.2 Zielsetzung](#12-zielsetzung)
  - [1.3 Herangehensweise](#13-herangehensweise)
    - [1.3.1 Technologie-Stack](#131-technologie-stack)
    - [1.3.2 Datengrundlage](#132-datengrundlage)
    - [1.3.3 Softwarearchitektur](#133-softwarearchitektur)
    - [1.3.4 Entwicklungsprozess](#134-entwicklungsprozess)
- [2. Grundlagen](#2-grundlagen)
  - [2.1 Finanzmarktgrundlagen](#21-finanzmarktgrundlagen)
    - [2.1.1 Grundlegende Begriffe](#211-grundlegende-begriffe)
    - [2.1.2 Wichtige Finanzkennzahlen](#212-wichtige-finanzkennzahlen)
    - [2.1.3 Zeitreihenanalyse im Finanzkontext](#213-zeitreihenanalyse-im-finanzkontext)
  - [2.2 Machine Learning Grundlagen](#22-machine-learning-grundlagen)
    - [2.2.1 Lernparadigmen](#221-lernparadigmen)
    - [2.2.2 Datenaufteilung und Preprocessing](#222-datenaufteilung-und-preprocessing)
    - [2.2.3 Machine Learning-Algorithmen](#223-machine-learning-algorithmen)
    - [2.2.4 Evaluationsmetriken](#224-evaluationsmetriken)
  - [2.3 Large Language Models (LLMs)](#23-large-language-models-llms)
    - [2.3.1 Grundlagen von Large Language Models](#231-grundlagen-von-large-language-models)
    - [2.3.2 Ollama als lokale LLM-Infrastruktur](#232-ollama-als-lokale-llm-infrastruktur)
    - [2.3.3 LLMs im Finanzkontext](#233-llms-im-finanzkontext)
- [3. Datenbeschreibung](#3-datenbeschreibung)
  - [3.1 Datenquellen](#31-datenquellen)
  - [3.2 Datenumfang](#32-datenumfang)
  - [3.3 Datenpipeline und Speicherung](#33-datenpipeline-und-speicherung)
  - [3.4 Datenaufbereitung](#34-datenaufbereitung)
  - [3.5 Datenqualität und Limitationen](#35-datenqualität-und-limitationen)
  - [3.6 Nutzerbereitgestellte Daten](#36-nutzerbereitgestellte-daten)
- [4. Implementierung](#4-implementierung)
  - [4.1 Systemarchitektur und Technologie-Stack](#41-systemarchitektur-und-technologie-stack)
    - [4.1.1 Architekturkonzept](#411-architekturkonzept)
    - [4.1.2 Technologie-Stack](#412-technologie-stack)
    - [4.1.3 Projektstruktur](#413-projektstruktur)
  - [4.2 Dateninfrastruktur](#42-dateninfrastruktur)
    - [4.2.1 Datenbankdesign und -struktur](#421-datenbankdesign-und--struktur)
      - [4.2.1.1 alphavantage.db (Rohdaten)](#4211-alphavantagedb-rohdaten)
      - [4.2.1.2 alphavantage_processed.db (Verarbeitete Daten)](#4212-alphavantage_processeddb-verarbeitete-daten)
      - [4.2.1.3 yfinance.db (Yahoo Finance Daten)](#4213-yfinancedb-yahoo-finance-daten)
      - [4.2.1.4 system_config.db (Persistente Konfiguration)](#4214-system_configdb-persistente-konfiguration)
      - [4.2.1.5 users_database.db (Nutzerdaten)](#4215-users_databasedb-nutzerdaten)
      - [4.2.1.6 Datenbankzugriff via SQLAlchemy](#4216-datenbankzugriff-via-sqlalchemy)
    - [4.2.2 API-Integration](#422-api-integration)
      - [4.2.2.1 Alpha Vantage API (av_connect.py)](#4221-alpha-vantage-api-av_connectpy)
      - [4.2.2.2 Yahoo Finance API (yf_connect.py)](#4222-yahoo-finance-api-yf_connectpy)
    - [4.2.3 Datenverarbeitung (ETL-Pipeline)](#423-datenverarbeitung-etl-pipeline)
      - [4.2.3.1 Alpha Vantage Processing](#4231-alpha-vantage-processing)
      - [4.2.3.2 Daten-Update-Orchestrierung (scheduler.py)](#4232-daten-update-orchestrierung-schedulerpy)
  - [4.3 Backend-Implementierung](#43-backend-implementierung)
    - [4.3.1 Datenbankschicht](#431-datenbankschicht)
      - [4.3.1.1 Zentrale Datenzugriffsschicht (db_functions.py)](#4311-zentrale-datenzugriffsschicht-db_functionspy)
      - [4.3.1.2 Nutzerdatenbank-Verwaltung (users_database.py)](#4312-nutzerdatenbank-verwaltung-users_databasepy)
      - [4.3.1.3 Utility-Funktionen (database_utils.py)](#4313-utility-funktionen-database_utilspy)
    - [4.3.2 Machine Learning Pipeline](#432-machine-learning-pipeline)
    - [4.3.3 LLM-Integration](#433-llm-integration)
      - [4.3.3.1 Verbindungs-Management (llm_functions.py)](#4331-verbindungs-management-llm_functionspy)
    - [4.3.4 Hilfsfunktionen und Konfiguration](#434-hilfsfunktionen-und-konfiguration)
      - [4.3.4.1 Zentrale Datenstrukturen (data_model.py)](#4341-zentrale-datenstrukturen-data_modelpy)
      - [4.3.4.2 Markdown-Content (markdown.py)](#4342-markdown-content-markdownpy)
      - [4.3.4.3 Anwendungsstart (launch.py)](#4343-anwendungsstart-launchpy)
  - [4.4 Frontend-Implementierung](#44-frontend-implementierung)
    - [4.4.1 Streamlit-Architektur](#441-streamlit-architektur)
    - [4.4.2 Seitenstruktur](#442-seitenstruktur)
      - [4.4.2.1 Startseite (Start.py)](#4421-startseite-startpy)
      - [4.4.2.2 Datenmanagement (1 Data.py)](#4422-datenmanagement-1-datapy)
      - [4.4.2.3 Machine Learning (2 Machine Learning.py)](#4423-machine-learning-2-machine-learningpy)
      - [4.4.2.4 LLM Playground (3 LLM Playground.py)](#4424-llm-playground-3-llm-playgroundpy)
      - [4.4.2.5 Assistent (4 Assistant.py)](#4425-assistent-4-assistantpy)
      - [4.4.2.6 Einstellungen (5 Settings.py)](#4426-einstellungen-5-settingspy)
    - [4.4.3 Asset-Management](#443-asset-management)
  - [4.5 Containerisierung und Deployment](#45-containerisierung-und-deployment)
    - [4.5.1 Dockerfile](#451-dockerfile)
    - [4.5.2 Docker Compose](#452-docker-compose)
    - [4.5.3 Dependency Management](#453-dependency-management)
    - [4.5.4 Deployment-Prozess](#454-deployment-prozess)
  - [4.6 Performance](#46-performance)
    - [4.6.1 SQLite-Performance bei großen Datensätzen](#461-sqlite-performance-bei-großen-datensätzen)
    - [4.6.2 Streamlit Session State vs. Persistenz](#462-streamlit-session-state-vs-persistenz)
    - [4.6.3 LLM-Integration: Modellgröße vs. Hardware](#463-llm-integration-modellgröße-vs-hardware)
  - [4.7 Code-Qualität und Wartbarkeit](#47-code-qualität-und-wartbarkeit)
    - [4.7.1 Error Handling](#471-error-handling)
    - [4.7.2 Code-Dokumentation](#472-code-dokumentation)
    - [4.7.3 Modularität und Wiederverwendbarkeit](#473-modularität-und-wiederverwendbarkeit)
- [Literatur](#literatur)

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

# 4. Implementierung

Die Implementierung der Finanzanalyse-Plattform erfolgte auf Basis einer modularen Softwarearchitektur mit klarer Trennung zwischen Datenhaltung, Backend-Logik und Frontend-Präsentation. Im Folgenden werden die technische Umsetzung, zentrale Designentscheidungen und die Struktur der implementierten Komponenten beschrieben.

## 4.1 Systemarchitektur und Technologie-Stack

### 4.1.1 Architekturkonzept

Die Plattform folgt einer **Drei-Schichten-Architektur**. Diese Architekturentscheidung ermöglicht eine unabhängige Entwicklung und Wartung einzelner Komponenten sowie eine flexible Erweiterbarkeit des Systems.

```
┌─────────────────────────────────────────────────────────┐
│              Präsentationsschicht                       │
│                  (Streamlit UI)                         │
│  - Start.py, Data.py, Machine Learning.py               │
│  - LLM Playground.py, Assistant.py, Settings.py         │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              Logikschicht (Backend)                     │
│  ┌──────────────────────────────────────────────────┐   │
│  │   API Services (yf_connect, av_connect, ollama)  │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │   Data Processing (alphavantage_processing)      │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │   Database Layer (db_functions, users_database)  │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │   Machine Learning (ML-Module)                   │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │   Orchestrierung (scheduler, llm_functions)      │   │
│  └──────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│           Datenhaltungsschicht (SQLite)                 │
│  - alphavantage.db, alphavantage_processed.db           │
│  - yfinance.db, system_config.db, users_database.db     │
└─────────────────────────────────────────────────────────┘
```

Die Wahl einer Schichtenarchitektur bietet mehrere Vorteile: Änderungen in der Datenbankstruktur können isoliert in der Datenhaltungsschicht vorgenommen werden, ohne Frontend-Code anzupassen. Die Backend-Logik kann unabhängig von der UI getestet werden, und einzelne Komponenten lassen sich bei Bedarf durch alternative Implementierungen ersetzen.

### 4.1.2 Technologie-Stack

Die Auswahl der Technologien erfolgte unter Berücksichtigung der Projektanforderungen, der Verfügbarkeit von Bibliotheken für Finanzanalysen und der Entwicklungsgeschwindigkeit:

| Komponente | Technologie | Version | Begründung |
|------------|-------------|---------|------------|
| **Programmiersprache** | Python | 3.x | De-facto-Standard für Data Science und ML, umfangreiches Ökosystem |
| **Frontend-Framework** | Streamlit | - | Rapid Prototyping für datengetriebene Anwendungen ohne JavaScript-Kenntnisse erforderlich |
| **Datenbank** | SQLite | 3.x | Embedded Database ohne separate Installation, ausreichend für Prototyp-Umfang |
| **ORM** | SQLAlchemy | - | Abstraktionsschicht für Datenbankzugriffe, Schutz vor SQL-Injection |
| **ML-Framework** | Scikit-Learn | - | Standardisierte API, breite Algorithmenauswahl, gut dokumentiert |
| **Visualisierung** | Plotly | - | Interaktive Charts mit JavaScript-Rendering, native Streamlit-Integration |
| **API-Client (Finanzdaten)** | yfinance, Alphavantage | - | Bewährte Bibliotheken für Finance, kostenlos und ohne API-Key + API-Key pflichtig |
| **HTTP-Client** | requests | - | Standard-Bibliothek für HTTP-Anfragen (Alpha Vantage API) |
| **LLM-Framework** | Ollama | - | Lokale LLM-Ausführung, datenschutzfreundlich, keine Cloud-Abhängigkeit |
| **Containerisierung** | Docker, Docker Compose | - | Reproduzierbare Deployment-Umgebung, vereinfachte Installation |

Die Entscheidung für SQLite als Datenbanksystem basiert auf der Eignung für Einzelnutzer-Anwendungen und die Vermeidung zusätzlicher Infrastrukturanforderungen. Für produktive Multi-User-Szenarien wäre eine Migration zu PostgreSQL oder MySQL zu empfehlen.

Streamlit wurde gegenüber Alternativen wie Dash oder Flask bevorzugt, da es die schnellste Entwicklung interaktiver Dashboards ermöglicht und eine native Integration von Data Science-Bibliotheken bietet (Streamlit Inc., 2024).

### 4.1.3 Projektstruktur

Die Implementierung folgt einer hierarchischen Ordnerstruktur, die eine klare Trennung von Verantwortlichkeiten gewährleistet:

```
PRAXISP_SOURCE/
├── data/                          # Persistente Datenhaltung
│   ├── alphavantage.db
│   ├── alphavantage_processed.db
│   ├── yfinance.db
│   ├── system_config.db
│   └── users_database.db
│
├── saved_models/                  # Persistierte ML-Modelle
│
├── src/
│   ├── backend/
│   │   ├── api_services/          # Externe API-Anbindungen
│   │   │   ├── yf_connect.py
│   │   │   ├── av_connect.py
│   │   │   └── ollama_connect.py
│   │   ├── data_processing/       # ETL-Pipeline
│   │   │   └── alphavantage_processing.py
│   │   ├── database/              # Datenzugriffsschicht
│   │   │   ├── db_functions.py
│   │   │   ├── database_utils.py
│   │   │   └── users_database.py
│   │   ├── machine_learning/      # ML-Algorithmen
│   │   ├── data_model.py          # Zentrale Datenstrukturen
│   │   ├── launch.py              # Anwendungsstart
│   │   ├── llm_functions.py       # LLM-Hilfsfunktionen
│   │   ├── markdown.py            # UI-Textinhalte
│   │   └── scheduler.py           # Daten-Update-Orchestrierung
│   │
│   └── frontend/
│       └── st/
│           ├── assets/            # Statische Ressourcen
│           ├── pages/             # Streamlit-Seiten
│           │   ├── 1 Data.py
│           │   ├── 2 Machine Learning.py
│           │   ├── 3 LLM Playground.py
│           │   ├── 4 Assistant.py
│           │   └── 5 Settings.py
│           └── Start.py           # Einstiegspunkt
│
├── docker-compose.yml             # Container-Orchestrierung
├── Dockerfile                     # Container-Definition
└── requirements.txt               # Python-Dependencies
```

Diese Struktur implementiert das **Package-by-Feature-Prinzip** auf oberster Ebene (Backend/Frontend) und das **Package-by-Layer-Prinzip** innerhalb des Backends (API Services, Data Processing, Database, ML). Dies erleichtert den Zugriff auf einzelne Komponenten.

---

## 4.2 Dateninfrastruktur

### 4.2.1 Datenbankdesign und -struktur

Die Datenhaltung basiert auf **fünf separaten SQLite-Datenbanken**, die jeweils unterschiedliche Datendomänen abdecken. Diese Aufteilung ermöglicht eine klare Trennung von Rohdaten, verarbeiteten Daten, Nutzerdaten und Systemkonfigurationen.

#### 4.2.1.1 alphavantage.db (Rohdaten)

Diese Datenbank dient als Speicher für unverarbeitete Daten aus der Alpha Vantage API und enthält zwei Haupttabellen:

**Tabelle: `alphavantage_daily_pricing`**
- Funktion: Speicherung von Kurszeitreihen
- Struktur: OHLCV-Format (Open, High, Low, Close, Volume) plus Adjusted Close
- Primary Key: Composite Key aus `(symbol, date)`
- Datenherkunft: Alpha Vantage API Endpoint `TIME_SERIES_DAILY_ADJUSTED`

**Tabelle: `alphavantage_raw_kpi`**
- Funktion: Speicherung fundamentaler Unternehmenskennzahlen
- Inhalt: Diverse KPIs im Rohformat ohne Vorverarbeitung
- Primary Key: `symbol`
- Besonderheit: Enthält zahlreiche Spalten, von denen viele überwiegend NULL-Werte aufweisen

Die bewusste Trennung zwischen Kurs- und KPI-Daten folgt dem Prinzip der **Normalisierung** und vermeidet Wiederholungen, da Kursdaten eine Zeitreihendimension besitzen, während KPIs typischerweise statisch für ein Unternehmen sind.

#### 4.2.1.2 alphavantage_processed.db (Verarbeitete Daten)

Diese Datenbank enthält bereinigte Varianten der Alpha Vantage-Rohdaten:

**Tabelle: `alphavantage_pricing_processed`**
- Funktion: Bereinigte Kursdaten
- Verarbeitung: Entfernung NaN-dominierter Spalten, Duplikat-Eliminierung
- Constraint: `UNIQUE(symbol, date)` verhindert doppelte Einträge auf Datenbankebene

**Tabelle: `alphavantage_processed_kpi`**
- Funktion: Bereinigte Unternehmenskennzahlen
- Verarbeitung: Entfernung von Spalten mit >80% NULL-Werten
- Rationale: Reduzierung des Datenvolumens und Fokussierung auf tatsächlich verfügbare Kennzahlen

Die Existenz einer separaten "processed"-Datenbank implementiert das **Data Lake vs. Data Warehouse**-Konzept im Kleinen: Rohdaten bleiben unverändert erhalten (Data Lake), während verarbeitete Daten für Analysen optimiert werden (Data Warehouse).

#### 4.2.1.3 yfinance.db (Yahoo Finance Daten)

Dies ist die umfangreichste Datenbank mit historischen Daten für die Initial-Ticker-Liste von ca. 400 Aktien:

**Tabelle: `yf_pricing_history`**
- Funktion: Historische Kursdaten
- Struktur: OHLCV-Format mit Adjusted Close
- Zeitraum: Ab 1995 bis aktuell (konfigurierbar)
- Datenmenge: Mehrere Millionen Datensätze je nach Zeitraum
- Primary Key: `(symbol, date)`
- Besonderheit: Auto-Adjusted Kurse standardmäßig aktiviert

**Tabelle: `yf_company_info`**
- Funktion: Unternehmensmetadaten
- Inhalt: Name, Sektor, Industrie, Land, Kurzbeschreibung
- Primary Key: `symbol`
- Verwendung: Kontextualisierung in der Data-Analyseansicht

Die Größe dieser Datenbank (mehrere Millionen Datensätze) erfordert besondere Aufmerksamkeit hinsichtlich Query-Performance, wofür SQLite-Indizes auf den Primary Keys automatisch angelegt werden.

#### 4.2.1.4 system_config.db (Persistente Konfiguration)

Diese Datenbank implementiert einen **Key-Value-Store** für anwendungsweite Einstellungen:

**Tabelle: `global_config`**
- Struktur: `ID` (Integer, Primary Key), `name` (TEXT), `Value` (TEXT), `Tag` (Bool)
- Funktion: Persistierung von Einstellungen über Streamlit-Neustarts hinweg
- Typische Inhalte:
  - Button-Status-Flags (technische Absicherung gegen Session State-Verlust)
  - Ausgewähltes LLM-Modell für Assistenten
  - Modifizierte Initial-Ticker-Liste (als JSON-String)
  - Ollama-Verbindungskonfiguration
  - ML-Training-Parameter (z.B. Zeilenlimits)

Die Implementierung eines eigenen Konfigurationssystems war notwendig, da Streamlit's Session State bei jedem Neustart zurückgesetzt wird. Durch Speicherung kritischer Konfigurationen in SQLite wird Persistenz gewährleistet, während gleichzeitig der Session State für transiente UI-Zustände verwendet werden kann (Hybridansatz).

#### 4.2.1.5 users_database.db (Nutzerdaten)

Diese Datenbank enthält dynamisch erstellte Tabellen aus Nutzer-Uploads:

- Funktion: Speicherung von CSV/Excel-Importen
- Schema: Dynamisch basierend auf importierten Daten
- Spaltennamen: Automatisch normalisiert (Leerzeichen entfernt, lowercase, Unterstriche)
- Besonderheit: Ermöglicht Nutzern das Einbringen eigener Datensätze für Analysen

Die Trennung der Nutzerdatenbank von Systemdatenbanken folgt dem **Principle of Least Privilege**: Nutzer können nur in ihrer eigenen Datenbank Tabellen anlegen/löschen, ohne Systemdaten zu gefährden.

#### 4.2.1.6 Datenbankzugriff via SQLAlchemy

Alle Datenbankoperationen erfolgen ausschließlich über SQLAlchemy als Object-Relational Mapping (ORM) Framework. Dies bietet mehrere Vorteile:

1. **SQL-Injection-Prävention**: Parametrisierte Queries verhindern Injection-Angriffe
2. **Datenbankabstraktion**: Potenzielle Migration zu anderen DBMS vereinfacht
3. **Pythonic API**: Datenbankzugriffe folgen Python-Konventionen
4. **Automatische Typkonvertierung**: Mapping zwischen SQL- und Python-Typen

Die hauptsächliche zentrale Abstraktion erfolgt über das Modul [`db_functions.py`](src/backend/database/db_functions.py), das alle CRUD-Operationen kapselt und dem Frontend eine konsistente Schnittstelle bietet.

### 4.2.2 API-Integration

#### 4.2.2.1 Alpha Vantage API (av_connect.py)

Die Alpha Vantage API dient als Quelle für fundamentale Unternehmenskennzahlen und historische Kursdaten. Die Implementierung befindet sich in [`av_connect.py`](src/backend/api_services/av_connect.py).

**Authentifizierung:**
Der API-Key wird aus dem Streamlit Session State ausgelesen (`st.session_state.api_key_av`) und nicht persistent gespeichert. Diese Designentscheidung erhöht die Sicherheit, da sensible Zugangsdaten nicht in Konfigurationsdateien oder Datenbanken abgelegt werden. Allerdings erfordert dies eine erneute Eingabe nach jedem Neustart der Anwendung.

**Rate Limiting:**
Alpha Vantage limitiert kostenlose Accounts auf:
- 25 Anfragen pro Tag
- 5 Anfragen pro Minute

Die Implementierung enthält Schutzmechanismen zur Einhaltung dieser Limits und zur Vermeidung unnötiger API-Belastung. Die genaue Strategie (z.B. Sleep zwischen Requests, Request-Counter) ist im Code hinterlegt.

**Orchestrierung:**
API-Calls werden nicht direkt aus [`av_connect.py`](src/backend/api_services/av_connect.py) initiiert, sondern über das zentrale Orchestrierungsmodul [`scheduler.py`](src/backend/scheduler.py). Dies zentralisiert die Kontrolle über Daten-Updates.

**Verwendete Funktionen:**
- [`create_av_raw_entry()`](src/backend/database/db_functions.py): Speichert Rohdaten in `alphavantage.db`
- [`create_av_pricing_entry()`](src/backend/database/db_functions.py): Speichert Pricing-Daten

#### 4.2.2.2 Yahoo Finance API (yf_connect.py)

Die Yahoo Finance API wird über die Python-Bibliothek `yfinance` angebunden und erfordert keine Authentifizierung. Die Implementierung befindet sich in [`yf_connect.py`](src/backend/api_services/yf_connect.py).

**Zentrale Funktionen:**

**[`download_yf_pricing_raw_timeperiod()`](src/backend/api_services/yf_connect.py):**
- Zweck: Download von Kursdaten für definierten Zeitraum
- Parameter: Liste von Symbolen, Startdatum (2024-01-01), Enddatum (2025-01-01)
- Besonderheit: Zeitgrenzen sind aktuell hart codiert
- Speicherung: Direkt in `yf_pricing_history`-Tabelle

**[`download_yf_pricing_raw_newest()`](src/backend/api_services/yf_connect.py):**
- Zweck: Aktualisierung auf neueste verfügbare Daten
- Parameter: Symbol, Period (Standard: "1d")
- Verwendung: Inkrementelle Updates einzelner Ticker

**[`download_price_history()`](src/backend/api_services/yf_connect.py):**
- Zweck: Initiales Befüllen der Datenbank
- Zeitraum: Ab 1995 bis 2020
- Verarbeitung: Batch-Processing für Ticker-Liste
- Verwendung: Einmalig beim Setup

**[`download_yf_company_info()`](src/backend/api_services/yf_connect.py):**
- Zweck: Download von Unternehmensmetadaten
- Quelle: `yfinance.Ticker.info`-Dictionary
- Speicherung: In `yf_company_info`-Tabelle

**Auto-Adjusted Kurse:**
Alle Funktionen verwenden standardmäßig `auto_adjust=True`, um automatisch für Splits und Dividenden bereinigte Kurse zu laden. Dies ist essentiell für korrekte historische Analysen, da nominale Kurse durch Splits verzerrt wären (Yahoo Finance, 2024).

**Verbindungsmanagement:**

**[`check_connection()`](src/backend/llm_functions.py):**
- Zweck: Prüfung der Erreichbarkeit der Ollama-Instanz
- Implementierung: HTTP-Request an Ollama-Healthcheck-Endpoint
- Rückgabe: Boolean (True wenn erreichbar)

**[`ensure_model()`](src/backend/llm_functions.py):**
- Zweck: Sicherstellung der Modellverfügbarkeit
- Prüfung: Abfrage der installierten Modelle via Ollama API
- Verwendung: Vor LLM-Anfragen zur Fehlervermeidung

**[`base_url_from_choice()`](src/backend/llm_functions.py):**
- Zweck: Ermittlung der korrekten Ollama-URL basierend auf Deployment-Szenario
- Optionen:
  - `'local'`: `http://localhost:11434` (lokale Installation)
  - `'host'`: `http://host.docker.internal:11434` (Container greift auf Host zu)
  - `'container'`: `http://ollama:11434` (Container-zu-Container-Kommunikation)
- Rationale: Verschiedene Deployment-Szenarien erfordern unterschiedliche Netzwerk-Konfigurationen

### 4.2.3 Datenverarbeitung (ETL-Pipeline)

#### 4.2.3.1 Alpha Vantage Processing

Die Verarbeitung der Alpha Vantage-Rohdaten erfolgt durch das Modul [`alphavantage_processing.py`](src/backend/data_processing/alphavantage_processing.py) und implementiert eine einfache **ETL-Pipeline** (Extract, Transform, Load).

**Extract-Phase:**
Rohdaten werden aus `alphavantage.db` extrahiert:
- Tabelle `alphavantage_daily_pricing` → Pandas DataFrame
- Tabelle `alphavantage_raw_kpi` → Pandas DataFrame

**Load-Phase:**
Daten werden automatisch bereinigt und verjüngte in `alphavantage_processed.db` geschrieben:
- Tabelle `alphavantage_pricing_processed`
- Tabelle `alphavantage_processed_kpi`
- `UNIQUE`-Constraint auf `(symbol, date)` verhindert Duplikate auf Datenbankebene

**Erweiterbarkeit:**
Die aktuelle Implementierung ist bewusst generisch gehalten und kann um weitere Verarbeitungsschritte ergänzt werden:
- Imputation fehlender Werte (z.B. Forward-Fill für Zeitreihen)
- Feature-Engineering (z.B. gleitende Durchschnitte)
- Normalisierung/Standardisierung numerischer Spalten
- Outlier-Detection und -Behandlung

**Frontend-Zugriffsfunktionen:**
Das Modul stellt Hilfsfunktionen für Frontend-Abfragen bereit:
- [`get_unique_symbols_from_table()`](src/backend/data_processing/alphavantage_processing.py): Liefert verfügbare Symbole
- [`get_processed_entries_by_symbol()`](src/backend/data_processing/alphavantage_processing.py): Filtert Daten nach Symbol
- [`get_processed_table()`](src/backend/data_processing/alphavantage_processing.py): Lädt komplette Tabelle

#### 4.2.3.2 Daten-Update-Orchestrierung (scheduler.py)

Das Modul [`scheduler.py`](src/backend/scheduler.py) fungiert als zentraler Orchestrator für Daten-Updates und das initiale Laden der Daten.

**Hauptfunktionen:**

**[`load_data(data: list)`](src/backend/scheduler.py):**
- Zweck: Download und Verarbeitung von Alpha Vantage-Daten für Symbol-Liste
- Ablauf:
  1. Iteration über Symbol-Liste
  2. API-Call für Pricing-Daten via [`av_connect.py`](src/backend/api_services/av_connect.py)
  3. API-Call für KPI-Daten via [`av_connect.py`](src/backend/api_services/av_connect.py)
  4. Speicherung in Rohdatenbank
  5. Trigger der Processing-Pipeline via [`alphavantage_processing.py`](src/backend/data_processing/alphavantage_processing.py)
  6. Aktualisierung des Last-Update-Timestamps in `system_config.db`
- Logging: Backend-Protokollierung von Erfolg/Fehler pro Symbol
- Error Handling: Fehler bei einzelnen Symbolen brechen Gesamtprozess nicht ab (Robustheit)

**[`load_initial_data()`](src/backend/scheduler.py):**
- Zweck: Initiales Laden der Default-Ticker-Liste
- Ablauf:
  1. Prüfung auf benutzerdefinierte Ticker-Liste in `system_config.db`
  2. Falls vorhanden: Verwendung der Custom-Liste
  3. Falls nicht: Fallback auf Standard-Liste aus [`data_model.py`](src/backend/data_model.py) (ca. 400 Symbole)
  4. Aufruf von [`load_data()`](src/backend/scheduler.py) mit ermittelter Liste
- Rationale: Ermöglicht Nutzern Anpassung der Initial-Daten ohne Code-Änderungen

**Zukünftige Erweiterungen:**
Die Bezeichnung "scheduler" impliziert zeitgesteuerte Ausführung. Aktuell erfolgen Updates manuell über Frontend-Buttons. Eine mögliche Erweiterung wäre die Integration eines Scheduling-Frameworks (z.B. APScheduler) für automatisierte Updates in definierten Intervallen.

---

## 4.3 Backend-Implementierung

### 4.3.1 Datenbankschicht

#### 4.3.1.1 Zentrale Datenzugriffsschicht (db_functions.py)

Das Modul [`db_functions.py`](src/backend/database/db_functions.py) implementiert und kapselt sämtliche Datenbankoperationen. Dies gewährleistet eine konsistente Schnittstelle zwischen Frontend und Datenbank und ermöglicht eine zentrale Fehlerbehandlung.

**Funktionsgruppen:**

**Alpha Vantage Rohdaten:**
- [`create_av_raw_entry()`](src/backend/database/db_functions.py): INSERT für KPI-Rohdaten
- [`create_av_pricing_entry()`](src/backend/database/db_functions.py): INSERT für Pricing-Rohdaten
- Verwendung: Ausschließlich durch [`av_connect.py`](src/backend/api_services/av_connect.py) nach API-Calls

**Yahoo Finance Daten:**
- [`create_yf_price_history_entry()`](src/backend/database/db_functions.py): Standard INSERT für Kursdaten
- [`create_yf_price_history_entry_ml()`](src/backend/database/db_functions.py): Spezialversion für ML-Workflows
- [`create_yf_company_information_entry()`](src/backend/database/db_functions.py): INSERT für Unternehmensmetadaten
- [`create_yf_company_from_info(info: dict)`](src/backend/database/db_functions.py): Erstellt Company-Info aus yfinance-Dictionary
- Verwendung: Durch [`yf_connect.py`](src/backend/api_services/yf_connect.py) zur Datenspeicherung

**Generische Tabellenoperationen:**
- [`get_table(table_name: str)`](src/backend/database/db_functions.py): SELECT * als Pandas DataFrame
- [`get_unique_table(table_name: str)`](src/backend/database/db_functions.py): SELECT DISTINCT
- [`get_unique_table_modded(table_name: str, subset=None)`](src/backend/database/db_functions.py): DISTINCT auf Teilmenge der Spalten
- [`get_table_names(database_path: str)`](src/backend/database/db_functions.py): Listet Tabellen einer Datenbank
- [`delete_table(database_path: str, table_name: str)`](src/backend/database/db_functions.py): DROP TABLE

Diese generischen Funktionen abstrahieren SQLAlchemy-Operationen und bieten eine einheitliche Pandas-basierte Schnittstelle, die im gesamten Frontend verwendet wird.

**System-Konfiguration (Key-Value-Store):**
- [`add_system_config(name: str, value: str, tag: bool)`](src/backend/database/db_functions.py): Neuen Config-Eintrag anlegen
- [`get_system_config_by_name(name: str)`](src/backend/database/db_functions.py): Config-Wert auslesen
- [`get_config_dict(name: str)`](src/backend/database/db_functions.py): Config als Dictionary
- [`update_system_config(name: str, value: str)`](src/backend/database/db_functions.py): Config aktualisieren
- [`delete_system_config(name: str)`](src/backend/database/db_functions.py): Config entfernen

Diese Funktionen implementieren einen einfachen Key-Value-Store in SQLite und ermöglichen typsichere Speicherung durch das `data_type`-Feld (Deserialisierung beim Auslesen).

**Listen-Konfiguration (für Ticker-Listen):**
- [`add_list_system_config(name: str, values: list, description: str)`](src/backend/database/db_functions.py): Liste als JSON speichern
- [`get_list_system_config(name: str)`](src/backend/database/db_functions.py): JSON zu Python-Liste deserialisieren
- [`update_list_system_config(name: str, values: list)`](src/backend/database/db_functions.py): Liste aktualisieren
- [`append_to_list_system_config(name: str, item: str)`](src/backend/database/db_functions.py): Element hinzufügen
- [`remove_from_list_system_config(name: str, item: str)`](src/backend/database/db_functions.py): Element entfernen

Diese spezialisierten Funktionen vereinfachen die Verwaltung von Listen (z.B. Initial-Ticker-Liste) durch Abstraktion der JSON-Serialisierung.

**Frontend-Abfragen (Yahoo Finance):**
- [`get_yf_company_info(symbol: str)`](src/backend/database/db_functions.py): Company-Info für einzelnes Symbol
- [`get_yf_price_history(symbol: str)`](src/backend/database/db_functions.py): Vollständige Kurshistorie
- [`get_yf_pricing_raw(symbol: str)`](src/backend/database/db_functions.py): Rohe Pricing-Daten
- [`get_yf_price_history_ml(symbol: str)`](src/backend/database/db_functions.py): Pricing-Daten optimiert für ML
- [`get_all_yf_price_history()`](src/backend/database/db_functions.py): Kompletter Datensatz aller Symbole

Diese Funktionen sind auf typische Frontend-Anfragen optimiert und liefern vorgefilterte/sortierte DataFrames.

**Symbol-Extraktion:**
- [`get_symbols_from_table(database_path: str, table_name: str)`](src/backend/database/db_functions.py): Extrahiert eindeutige Symbole aus Tabelle
- Verwendung: Population von Dropdown-Menüs im Frontend

#### 4.3.1.2 Nutzerdatenbank-Verwaltung (users_database.py)

Das Modul [`users_database.py`](src/backend/database/users_database.py) verwaltet die dynamisch erstellten Nutzertabellen und implementiert spezielle Logik für CSV/Excel-Imports.

**Kernfunktionen:**

**Tabellenerstellung aus Uploads:**
- Import von CSV/Excel-Dateien
- Automatische Schema-Inferenz durch Pandas
- Spaltennormalisierung: Leerzeichen entfernen, Konvertierung zu lowercase, Ersetzung durch Unterstriche
- Rationale: Vermeidung von SQL-Syntaxproblemen durch einheitliche Namenskonventionen

**CRUD-Operationen:**
- Auflisten vorhandener Tabellen
- Auslesen gespeicherter Tabellen als DataFrame
- Löschen von Tabellen
- Rationale: Vollständige Kontrolle über Nutzerdaten

Die Trennung dieser Logik von [`db_functions.py`](src/backend/database/db_functions.py) folgt dem **Single Responsibility Principle**: [`db_functions.py`](src/backend/database/db_functions.py) verwaltet Systemdatenbanken, [`users_database.py`](src/backend/database/users_database.py) verwaltet Nutzerdatenbanken.

#### 4.3.1.3 Utility-Funktionen (database_utils.py)

Das Modul [`database_utils.py`](src/backend/database/database_utils.py) stellt übergreifende Hilfsfunktionen bereit.

**[`delete_any_table(table_name: str, source: str)`](src/backend/database/database_utils.py):**
- Zweck: Vereinheitlichte Löschfunktion für alle Datenbanken
- Parameter `source`: 'user', 'alphavantage', 'alphavantage_processed', 'yfinance', 'system'
- Implementierung: Mapping von Source-String zu Datenbankpfad, Delegierung an [`delete_table()`](src/backend/database/db_functions.py)
- Rationale: Vereinfachung der Löschlogik im Frontend durch Single-Entry-Point

### 4.3.2 Machine Learning Pipeline

Einige Machine Learning-Komponenten befinden sich im Ordner [`machine_learning/`](src/backend/machine_learning/). Die dort enthaltenen Module ([`get_training_data.py`](src/backend/machine_learning/get_training_data.py), [`price_predictions.py`](src/backend/machine_learning/price_predictions.py), [`processing_datasets.py`](src/backend/machine_learning/processing_datasets.py), [`training_data.py`](src/backend/machine_learning/training_data.py), [`tree_ml.py`](src/backend/machine_learning/tree_ml.py), [`up_or_down.py`](src/backend/machine_learning/up_or_down.py)) sind in der aktuellen Version nicht aktiv im Frontend eingebunden und werden daher in dieser Dokumentation nicht detailliert beschrieben. Die Module enthalten Vorarbeiten zur Datenextraktion, Datensatzverarbeitung und Algorithmus-Konfiguration, die als Basis für zukünftige ML-Funktionalitäten dienen können.

Die Machine-Learning-Funktionalität ist in der aktuellen Version **direkt im Streamlit-Frontend** implementiert und befindet sich unter  
[`src/frontend/st/pages/2 Machine Learning.py`](src/frontend/st/pages/2%20Machine%20Learning.py).  
Der Playground erlaubt es, auf Basis der vorhandenen Datenquellen (Yahoo Finance / AlphaVantage / User-Tabellen) schnell Modelle zu trainieren, zu evaluieren und als `.pkl` zu speichern.


**Überblick: Ziel des Playgrounds**

Der ML-Playground ist als **experimentelle Trainings- und Evaluationsumgebung** konzipiert. Nutzer:innen können:

- eine Datenquelle auswählen (z.B. AlphaVantage Pricing + KPI)
- Feature-Spalten (X) und Target-Spalte (y) bestimmen
- optional einen **Vorhersagehorizont** (Zukunfts-Target) aktivieren
- optional einen **Zeitreihenmodus** mit Lag-Features nutzen
- ein Modell trainieren und einfache Metriken/Plots sehen
- das trainierte Modell inkl. Metadaten speichern

Die Speicherung erfolgt als **Model-Bundle** (Joblib) unter `saved_models/`.

**Automatische Vorverarbeitung (Typ-Konvertierung)**

Um unterschiedliche Datenquellen möglichst robust nutzbar zu machen, wird eine automatische Konvertierung angewendet:

**1) Numerik-Erkennung (`_try_parse_numeric_series`)**
- versucht String-Spalten als Float zu parsen
- unterstützt u.a.:
  - `1.234,56` → `1234.56` (deutsche Schreibweise)
  - `12,3%` → `12.3`
  - Entfernen von `€`, `$`, Leerzeichen
- eine Spalte wird nur konvertiert, wenn mindestens ~50% der Werte plausibel numerisch sind

**2) Datums-/Zeit-Erkennung (`auto_convert_numeric_and_datetime`)**
- erkennt Spalten mit Namen wie `date`, `time`, `timestamp`
- konvertiert per `pd.to_datetime` (wenn >50% sinnvoll parsebar sind)

Diese Schritte reduzieren manuelle Fehler und ermöglichen ein flexibles Arbeiten mit heterogenen Tabellen.


**Auswahl von Feature- und Target-Spalten**

Im UI können Features (`X`) als Multiselect gewählt werden und ein Target (`y`) per Selectbox.  
Wichtig: Bei Regression kann **Data Leakage** entstehen, wenn `target_col` gleichzeitig in den Feature-Spalten enthalten ist und kein Shift/Time-Series-Mode verwendet wird. Dafür zeigt der Playground einen Hinweis an.


**Zukunfts-Target / Vorhersagehorizont**

Optional kann ein **Zukunfts-Target** erzeugt werden:

\[
y_{\text{future}}(t) = y(t + \Delta)
\]

Unterstützte Horizonte:
- `1 Tag`
- `3 Wochen`
- `3 Monate`
- `1 Jahr`

Implementiert wird dies als Merge-Shift auf der Zeitspalte (`timestamp`/`date`/etc.).  
Zeilen, für die kein Future-Wert existiert, werden entfernt (Drop-NaN).

**Zeitreihenmodus (Lag-Features)**

Der Zeitreihenmodus erzeugt aus einer Basis-Spalte (typischerweise dem Target) automatisch Lag-Features:

- `target_lag_1, target_lag_2, ... target_lag_n`

Beispiel bei `n_lags = 5`:
- `close_lag_1` = close(t-1)
- `close_lag_5` = close(t-5)

Diese Lag-Spalten werden dann als Features genutzt.  
Für den Train/Test-Split wird `shuffle=False` verwendet, um die zeitliche Ordnung nicht zu zerstören.

**Feature-Engineering & Encoding**

Für die Modellierung werden Features abhängig vom Typ verarbeitet:

**Numerische Features**
- bleiben numerisch oder werden aus Strings konvertiert (wie oben)
- optionales Scaling per `StandardScaler`

**Kategorische Features**
- werden per One-Hot-Encoding (`pd.get_dummies(drop_first=True)`) kodiert  
  → reduziert Dummy-Falle, jedoch kann es bei vielen Kategorien zu Feature-Explosion kommen

**NaN-Handling**
- nach Encoding und Target-Konvertierung werden NaNs konsequent entfernt  
  → falls dadurch keine Daten übrig bleiben, wird ein Fehler geworfen


**Unterstützte Algorithmen (Kurzbeschreibung)**

Im Playground stehen mehrere Modelltypen zur Auswahl:

##### 1) Lineare Regression (Regression)
**Zweck:** Prognose eines kontinuierlichen Werts (z.B. Preis, KPI).  
**Eigenschaften:**
- lernt lineare Zusammenhänge zwischen Features und Target
- schnell, gut interpretierbar
- anfällig für nichtlineare Muster

##### 2) Decision Tree Regressor (Regression)
**Zweck:** Regression mit nichtlinearen Zusammenhängen.  
**Eigenschaften:**
- bildet Entscheidungsregeln (Splits) über Features
- kann nichtlineare Beziehungen modellieren
- Risiko: Overfitting bei tiefen Bäumen / wenig Daten

##### 3) Random Forest Regressor (Regression)
**Zweck:** robusteres Regressionsmodell durch Ensemble vieler Trees.  
**Eigenschaften:**
- reduziert Overfitting im Vergleich zu einem einzelnen Tree
- kann komplexe Muster abbilden
- mehr Rechenzeit/Memory, weniger interpretierbar

##### 4) Logistische Regression (Klassifikation)
**Zweck:** Klassifikation eines diskreten Targets (z.B. Klasse A/B/C).  
**Eigenschaften:**
- lineares Modell, aber für Klassifikation (Wahrscheinlichkeiten)
- benötigt Encodierung der Klassen (LabelEncoder)
- profitiert oft von Feature-Scaling

##### 5) Richtungsklassifikation (Up/Down) mit LogReg
**Zweck:** Vorhersage, ob ein zukünftiger Wert höher ist als der aktuelle.  
Target wird binär erzeugt:

- `direction_up = 1`, wenn `future_value > current_value`, sonst `0`

Diese Variante setzt voraus, dass ein Vorhersagehorizont (Shift) aktiv ist.


**Evaluation & Visualisierung**

Je nach Modelltyp werden unterschiedliche Metriken ausgegeben:

**Regression**
- MSE (Mean Squared Error)
- RMSE (Root Mean Squared Error)
- R² (Bestimmtheitsmaß)
- Linienplot: `y_true` vs. `y_pred` (Streamlit line_chart)

**Klassifikation**
- Accuracy
- Konfusionsmatrix (ConfusionMatrixDisplay)


**Modell-Speicherung (Model Bundles)**

Trainierte Modelle werden als `.pkl` in `saved_models/` gespeichert.  
Gespeichert werden neben dem Modell auch Metadaten, u.a.:

- Algorithmus-Name
- Datenquelle
- Feature-Spalten / Target-Spalte
- optionaler Scaler
- Vorhersagehorizont
- LabelEncoder (bei Klassifikation)
- Time-Series-Mode + Lag-Parameter

Damit ist eine spätere Wiederverwendung (Inference) grundsätzlich möglich, sofern die Input-Features wieder im gleichen Schema vorliegen.


#### Grenzen und bekannte Einschränkungen

- **Kein Hyperparameter-Tuning:** Modelle werden mit Standard-Settings trainiert (z.B. RandomForest mit fixen `n_estimators`).
- **Kein Cross-Validation:** Aktuell nur Train/Test-Split; Ergebnisse können je nach Split variieren.
- **NaN-Drop kann Daten stark reduzieren:** Bei vielen fehlenden Werten kann nach Preprocessing nur ein kleiner Rest übrig bleiben.
- **Feature-Explosion bei One-Hot-Encoding:** Sehr viele Kategorien können zu großen, sparsamen Feature-Matrizen führen.
- **Zeitreihen-Validierung vereinfacht:** Der Zeitreihenmodus verhindert Shuffle, ersetzt aber kein professionelles Walk-Forward/Backtesting.
- **Rate-Limits / Datenqualität:** Je nach Datenquelle können Lücken, Ausreißer oder API-Limits das Training beeinflussen.
- **Daten-Leakage möglich:** Wenn Target und Features nicht sauber getrennt sind (Playground warnt in typischen Fällen, kann aber nicht alle Leaks erkennen).

### 4.3.3 LLM-Integration

#### 4.3.3.1 Verbindungs-Management (llm_functions.py)

Das Modul [`llm_functions.py`](src/backend/llm_functions.py) abstrahiert die Kommunikation mit Ollama und stellt Hilfsfunktionen für Verbindungsprüfung und Konfiguration bereit.

**[`check_connection(base_url: str)`](src/backend/llm_functions.py):**
- Implementierung: HTTP-GET-Request an Ollama-API
- Timeout: Kurze Timeout-Dauer zur schnellen Fehlerkennung
- Verwendung: Vor LLM-Anfragen zur Validierung der Verbindung

**[`ensure_model(base_url: str, model_name: str)`](src/backend/llm_functions.py):**
- Implementierung: Abfrage der installierten Modelle über Ollama-API
- Rückgabe: Boolean (True wenn Modell verfügbar)
- Verwendung: Prävention von Fehlern durch nicht-existente Modelle

**[`base_url_from_choice(choice: str)`](src/backend/llm_functions.py):**
- Mapping-Logik: String-Choice → URL
- Unterstützte Szenarien:
  - Lokale Ollama-Installation
  - Docker-Container greift auf Host-Ollama zu
  - Container-zu-Container-Kommunikation
- Rationale: Flexibles Deployment ohne Code-Änderungen

### 4.3.4 Hilfsfunktionen und Konfiguration

#### 4.3.4.1 Zentrale Datenstrukturen (data_model.py)

Das Modul [`data_model.py`](src/backend/data_model.py) definiert anwendungsweite Konstanten und Standard-Konfigurationen.

**TICKERS-Liste:**
- Inhalt: Ca. 400 Aktiensymbole
- Verwendung:
  - Initiales Datenbank-Setup via [`download_price_history()`](src/backend/api_services/yf_connect.py)
  - Initiales Laden der Ticker via [`load_initial_data`](src/backend/scheduler.py)
  - Fallback bei fehlender Custom-Ticker-Liste
  - Basis für Dropdown-Menüs im Frontend
  - Referenz in Settings-Seite
- Rationale: Zentrale Definition vermeidet Inkonsistenzen

**Weitere Strukturen:**
- Default-Metriken für Analysen
- ML-Algorithmus-Konfigurationen (falls verwendet)

Die Auslagerung dieser Definitionen in ein separates Modul folgt dem Prinzip der **Konfiguration als Code** und erleichtert Anpassungen ohne Suche im gesamten Codebase.

#### 4.3.4.2 Markdown-Content (markdown.py)

Das Modul [`markdown.py`](src/backend/markdown.py) enthält die Textinhalte für Welcome- und Setup-Seiten als String-Konstanten.

**Funktionen:**
- `get_welcome_markdown()`: Liefert Welcome-Text
- `get_setup_markdown()`: Liefert Setup-Anleitung

**Rationale:**
Auslagerung von UI-Texten aus Frontend-Code verbessert:
- **Wartbarkeit**: Textänderungen ohne Durchsuchen von UI-Dateien
- **Wiederverwendbarkeit**: Gleiche Texte können in mehreren Pages verwendet werden
- **Übersichtlichkeit**: Frontend-Code fokussiert auf Logik statt Content

#### 4.3.4.3 Anwendungsstart (launch.py)

Das Modul [`launch.py`](src/backend/launch.py) dient als Einstiegspunkt für die Docker-Container-Ausführung.

**Funktionalität:**
- Start der Streamlit-Anwendung mit vordefinierten Parametern
- Konfiguration von Port und Host
- Ermöglicht konsistenten Start im Container-Kontext

**Rationale:**
Zentralisierung der Startkonfiguration vereinfacht Docker-Deployment und vermeidet Hardcoding von Parametern in Dockerfiles.

---

## 4.4 Frontend-Implementierung

### 4.4.1 Streamlit-Architektur

Die Frontend-Implementierung nutzt Streamlit's **Multi-Page-App-Struktur**, bei der Seiten automatisch aus dem [`pages/`](src/frontend/st/pages/)-Ordner geladen werden (Streamlit Inc., 2024). Der Einstiegspunkt ist [`Start.py`](src/frontend/st/Start.py), die als Hauptseite beim Aufruf der Anwendung angezeigt wird.

**Session State Management:**

Streamlit's Session State wird für **transiente UI-Zustände** verwendet, die nur während einer Sitzung relevant sind:
- Aktuelle Ticker-Auswahl
- Temporäre API-Keys (Security-Maßnahme)
- UI-Element-Stati (Expander geöffnet/geschlossen)
- Zwischenergebnisse von Berechnungen

Für **persistente Zustände** wird stattdessen `system_config.db` verwendet (siehe 4.2.1.4). Diese Hybridstrategie kombiniert die Vorteile beider Ansätze: Session State für Performance, Datenbank für Persistenz.

### 4.4.2 Seitenstruktur

#### 4.4.2.1 Startseite (Start.py)

Die Startseite [`Start.py`](src/frontend/st/Start.py) dient als Einstiegspunkt und umfasst:

**Page Configuration:**
```python
st.set_page_config(
    page_title="Finanzanalyse-Plattform",
    page_icon="📈",
    layout="wide"
)
```

**Sidebar:**
- Anzeige des Plattform-Logos aus [`assets/LogoFinsight.png`](src/frontend/st/assets/LogoFinsight.png)
- Konsistente Darstellung über alle Seiten durch Streamlit's automatische Sidebar-Synchronisation

**Hauptbereich:**
- **Tab 1 (Welcome)**: Markdown-Content aus [`get_welcome_markdown()`](src/backend/markdown.py)
- **Tab 2 (Setup)**: Markdown-Content aus [`get_setup_markdown()`](src/backend/markdown.py), API-Key-Eingabe, Ollama-Konfiguration

Die Aufteilung in Tabs (statt separate Seiten) reduziert die Anzahl der Navigation-Items und gruppiert konzeptionell zusammengehörige Inhalte.

#### 4.4.2.2 Datenmanagement (1 Data.py)

Die Seite [`1 Data.py`](src/frontend/st/pages/1 Data.py) implementiert alle datenbezogenen Funktionalitäten:

**Funktionsgruppen:**
1. **Kursdaten-Visualisierung**: Candlestick-Charts mit Plotly, Volumen-Darstellung
2. **Unternehmensinfos**: Anzeige von Metadaten aus `yf_company_info`
3. **Datenladen**: Single-Ticker-Updates, Initial-Data-Load
4. **Eigene Daten**: CSV/Excel-Upload, Tabellenverwaltung

**Technische Implementierung:**
- Verwendung von Streamlit-Tabs zur Strukturierung
- Plotly für interaktive Charts (Zoom, Pan, Hover-Tooltips)
- Direkte Aufrufe von Backend-Funktionen aus [`db_functions.py`](src/backend/database/db_functions.py) und [`yf_connect.py`](src/backend/api_services/yf_connect.py)

#### 4.4.2.3 Machine Learning (2 Machine Learning.py)

Die Seite [`2 Machine Learning.py`](src/frontend/st/pages/2 Machine Learning.py) bietet die Schnittstelle für ML-Workflows:

**Geplante Funktionalität:**
- Algorithmus-Auswahl (Dropdown)
- Parameter-Konfiguration (Streamlit-Widgets)
- Training-Trigger (Button mit Progress-Bar)
- Ergebnis-Visualisierung (Metriken, Confusion Matrix, Prediction vs. Actual)

Die konkrete Implementierung dieser Funktionalitäten ist in der aktuellen Version noch ausstehend, da die ML-Module im Backend noch nicht vollständig in die UI integriert sind.

#### 4.4.2.4 LLM Playground (3 LLM Playground.py)

Die Seite [`3 LLM Playground.py`](src/frontend/st/pages/3 LLM Playground.py) ermöglicht Interaktion mit dem LLM:

**Geplante Funktionalität:**
- Modell-Auswahl (aus verfügbaren Ollama-Modellen)
- Prompt-Eingabe (Text-Area)
- Kontextualisierung (Einbindung von Finanzdaten)
- Response-Darstellung (Streaming oder vollständige Antwort)

#### 4.4.2.5 Assistent (4 Assistant.py)

Die Seite [`4 Assistant.py`](src/frontend/st/pages/4 Assistant.py) implementiert einen Chatbot zur Nutzerunterstützung:

**Geplante Funktionalität:**
- Chat-Interface (ähnlich ChatGPT-UI)
- Chat-History-Management (Session State)
- Hilfe-Prompts für Dashboard-Nutzung
- Integration mit Ollama via [`ollama_connect.py`](src/backend/api_services/ollama_connect.py)

#### 4.4.2.6 Einstellungen (5 Settings.py)

Die Seite [`5 Settings.py`](src/frontend/st/pages/5 Settings.py) bietet Konfigurationsmöglichkeiten:

**Funktionalitäten:**
- **Initial-Ticker-Liste-Editor**: Anzeige und Bearbeitung der Ticker-Liste, Speicherung via [`add_list_system_config()`](src/backend/database/db_functions.py)
- **Ollama-Verbindung**: Auswahl des Verbindungstyps (local/host/container)
- **ML-Parameter**: Konfiguration von Training-Limits
- **System-Info**: Anzeige von Last-Update-Timestamps

Die Settings-Seite nutzt intensiv die `system_config.db`-Funktionen, um Einstellungen persistent zu speichern.

### 4.4.3 Asset-Management

**Primärer Asset-Ordner:**
[`src/frontend/st/assets/`](src/frontend/st/assets/) enthält:
- Logos (PNG-Dateien)
- `assistantinfos.txt`: Kontext-Informationen für Assistenten-Prompts

**Fallback-Mechanismus:**
Der Unterordner [`pages/assets_safety/`](src/frontend/st/pages/assets_safety/) dupliziert kritische Assets. Dies adressiert ein Streamlit-spezifisches Problem: Pages in Unterordnern haben teilweise Probleme mit relativen Pfaden zu Assets im Hauptordner. Der Fallback-Ordner stellt sicher, dass Logos auch bei Pfadproblemen angezeigt werden können.

---

## 4.5 Containerisierung und Deployment

### 4.5.1 Dockerfile

Das [`Dockerfile`](Dockerfile) definiert das Container-Image für die Hauptanwendung:

**Basis-Image:**
- Python 3.x (Slim-Variante zur Reduktion der Image-Größe)

**System-Dependencies:**
- Build-Tools für Compilierung von Python-Paketen mit C-Extensions
- Curl für Healthchecks

**Python-Dependencies:**
- Installation via [`requirements.txt`](requirements.txt)
- `--no-cache-dir`-Flag reduziert Image-Größe

**Anwendungscode:**
- COPY des gesamten Projektverzeichnisses

**Exposed Port:**
- Port 8501 (Streamlit-Standard)

**Healthcheck:**
- Periodische Prüfung des Streamlit-Healthcheck-Endpoints
- Ermöglicht Container-Orchestrierung die Erkennung von Problemen

**Entry Point:**
- Start via [`launch.py`](src/backend/launch.py)

### 4.5.2 Docker Compose

Die Datei [`docker-compose.yml`](docker-compose.yml) orchestriert zwei Services:

**Service: app**
- Build-Context: Aktuelles Verzeichnis
- Port-Mapping: 8501:8501
- Environment-Variablen: Streamlit-Konfiguration
- Dependency: Wartet auf Ollama-Service

**Service: ollama**
- Image: `ollama/ollama:latest` (offizielles Ollama-Image)
- Volume: `ollama_data` für Modell-Persistierung
- Rationale: Lokale LLM-Ausführung ohne Cloud-Abhängigkeit

**Netzwerk:**
- Bridge-Netzwerk für Container-zu-Container-Kommunikation
- Ermöglicht App-Zugriff auf Ollama via Hostname `ollama`

### 4.5.3 Dependency Management

Die Datei [`requirements.txt`](requirements.txt) spezifiziert alle Python-Abhängigkeiten mit **Version-Pinning** zur Gewährleistung reproduzierbarer Builds:

**Zentrale Dependencies:**
- `streamlit`: Frontend-Framework
- `pandas`: Datenmanipulation
- `plotly`: Visualisierung
- `sqlalchemy`: ORM
- `yfinance`: Yahoo Finance API-Client
- `requests`: HTTP-Client
- `scikit-learn`: ML-Framework

Die explizite Versionsspezifikation vermeidet Breaking Changes durch automatische Updates und stellt sicher, dass die Anwendung in verschiedenen Umgebungen identisch funktioniert.

### 4.5.4 Deployment-Prozess

**Build:**
```bash
docker-compose build
```
Erstellt Container-Images basierend auf Dockerfile-Definitionen.

**Start:**
```bash
docker-compose up -d
```
Startet Services im Detached-Modus (Hintergrund).

**Logs:**
```bash
docker-compose logs -f app
```
Zeigt Anwendungs-Logs in Echtzeit (Follow-Modus).

**Stop:**
```bash
docker-compose down
```
Stoppt und entfernt Container (Volumes bleiben erhalten).

**Vollständiges Reset:**
```bash
docker-compose down -v
```
Entfernt auch Volumes (Datenverlust!), nützlich für Clean-State.

## 4.6 Performance

### 4.6.1 SQLite-Performance bei großen Datensätzen

**Problem:**
Die `yf_pricing_history`-Tabelle enthält mehrere Millionen Datensätze, was Abfragen verlangsamen kann.

**Implementierte Optimierungen:**
- **Primary Key auf (symbol, date)**: Automatischer Index von SQLite
- **Gefilterte Abfragen**: [`get_yf_price_history(symbol)`](src/backend/database/db_functions.py) lädt nur relevante Daten

**Weitere mögliche Optimierungen (nicht implementiert):**
- Zusätzliche Indizes auf häufig gefilterten Spalten
- Partitionierung großer Tabellen nach Jahr
- Pagination bei Frontend-Abfragen
- Migration zu PostgreSQL für bessere Performance bei Millionen Datensätzen

### 4.6.2 Streamlit Session State vs. Persistenz

**Problem:**
Streamlit's Session State wird bei jedem Neustart zurückgesetzt. Kritische Einstellungen (z.B. ausgewähltes LLM-Modell) gehen verloren.

**Implementierte Lösung: Hybridansatz**

**Session State für:**
- Temporäre UI-Zustände (Expander, Tabs)
- Aktuelle Selektionen (Ticker, Algorithmus)
- Zwischenergebnisse
- Alphavantage API-Key (aus Sicherheitsgründen)

**system_config.db für:**
- Gewähltes LLM-Modell
- Custom Initial-Ticker-Liste
- Button Zustände
- Update spezifische Einstellungen

Diese Strategie kombiniert Performance (Session State ist schneller als DB-Zugriffe) mit Persistenz (wichtige Einstellungen überdauern Neustarts).

### 4.6.3 LLM-Integration: Modellgröße vs. Hardware

**Problem:**
Moderne LLMs mit Milliarden Parametern erfordern erheblichen RAM (z.B. 7B-Modell ≈ 8-16GB RAM ohne Quantisierung).

**Implementierte Lösung:**
- Nutzung von Ollama's **Quantisierung** (4-Bit, 8-Bit) zur Reduktion des Speicherbedarfs
- Nutzer-Information über Hardwareanforderungen verschiedener Modelle
- Flexibilität bei Modellauswahl (kleinere Modelle für eingeschränkte Hardware)

**Nicht-implementierte Alternativen:**
- Cloud-basierte LLM-APIs (Datenschutz-Bedenken)
- Model-Offloading (Teile des Modells auf CPU/GPU verteilen)


## 4.7 Code-Qualität und Wartbarkeit

### 4.7.1 Error Handling

**Strategie:**
Alle kritischen Operationen (Datenbankzugriffe, API-Calls, Datei-I/O) sind mit Try-Except-Blöcken abgesichert. Fehler werden geloggt und dem Nutzer über Streamlit's `st.error()` kommuniziert.

**Typische Error-Handling-Struktur:**
```python
try:
    # Kritische Operation
    result = database_operation()
except SpecificException as e:
    logging.error(f"Detaillierte Fehlermeldung: {e}")
    st.error("Nutzerfreundliche Fehlermeldung")
    # Graceful Degradation oder Fallback
```

### 4.7.2 Code-Dokumentation

**Docstrings:**
Alle Funktionen in Backend-Modulen enthalten Docstrings nach Google-Style-Konvention:
- Kurzbeschreibung
- Detaillierte Erklärung
- Args-Sektion
- Returns-Sektion
- Beispiele (wo sinnvoll)

**Kommentare:**
Komplexe Logik wird inline kommentiert, insbesondere bei:
- Nicht-trivialem Feature Engineering
- Datenbankschema-spezifischen Operationen
- Workarounds für Library-Limitierungen

### 4.7.3 Modularität und Wiederverwendbarkeit

Die Implementierung folgt konsequent dem **DRY-Prinzip** (Don't Repeat Yourself):
- Zentrale Datenzugriffsfunktionen in [`db_functions.py`](src/backend/database/db_functions.py)
- Wiederverwendbare API-Call-Wrapper
- Gemeinsame Utility-Funktionen

Dies reduziert Code-Duplikation und vereinfacht Wartung (Änderungen nur an einer Stelle notwendig).

---

# 5. Resultate (Dashboard)

Dieses Kapitel beschreibt die sichtbaren Ergebnisse des Praxisprojekts „FinSight“ aus Sicht der Nutzerinnen und Nutzer. Im Fokus stehen das entstandene Streamlit-Dashboard, die Interaktionslogik, der typische User Flow sowie die wahrnehmbare Qualität (Usability, Stabilität, Performance). Ergänzend werden die wichtigsten Seiten und Funktionen anhand der realisierten UI-Struktur eingeordnet und mit Abbildungen (als Platzhalter) dokumentiert.  

Die in Kapitel 4 beschriebene technische Architektur (Drei-Schichten-Architektur, SQLite-Datenhaltung, modulare Backend-Services) spiegelt sich im Dashboard als klar strukturiertes, mehrseitiges Anwendungskonzept wider. Die App ist so gestaltet, dass Nutzer ohne tiefes Data-Science- oder Programmierwissen Daten explorieren, Modelle trainieren und LLM-basierte Analysen durchführen können, während fortgeschrittene Nutzer über flexible Auswahlmechanismen (Datenquellen, Features/Targets, Modellparameter) experimentelle Workflows realisieren können.

---

## 5.1 Ergebnisübersicht: Was ist entstanden?

Als Resultat wurde eine lauffähige Streamlit-Anwendung entwickelt, die folgende Kernziele erfüllt:

1. **Datenbereitstellung und -verwaltung**
   - Nutzung bereits vorbefüllter Datenbanken (Yahoo Finance, Alpha Vantage raw/processed)
   - Upload und Persistierung nutzereigener Tabellen (CSV/Excel) in `users_database.db`
   - Aktualisierungs- und Download-Funktionen für Kurs- und KPI-Daten

2. **Interaktive Datenanalyse**
   - Analyse einzelner Symbole inkl. Kennzahlen und Zeitreihenvisualisierung
   - Vergleichsanalyse mehrerer Aktien über ein gemeinsames Chart
   - Datenbankübersichten als Transparenz- und Debugging-Ansicht (Tabellen/Zeilen)

3. **Machine Learning Studio**
   - Training vordefinierter scikit-learn Modelle (Regression & Klassifikation)
   - Konfigurierbarer Train/Test-Split, optionales Feature-Scaling
   - Zeitreihenmodus (Lag-Features) und Prognosehorizont (Future Target Shift)
   - Automatische Speicherung trainierter Modelle inkl. Metadaten als `.pkl`

4. **LLM Playground**
   - Datenbasierte Analyse per lokal ausgeführtem LLM (Ollama)
   - Verschiedene Analysemodi (Regression, Classification, Trend, Free Analysis)
   - Konfigurierbare Sample Size und Custom Prompt
   - Einsicht in den generierten Prompt (Transparenz)

5. **Assistant**
   - Chatbasierter Hilfsassistent zur Unterstützung bei Nutzung und Interpretation
   - Modell konfigurierbar, Fokus auf niedrigschwelliger Benutzerhilfe

6. **Settings**
   - Persistente Konfiguration (Ticker-Liste, Training-Limits, Ollama-Quelle, Modellverwaltung)
   - Verwaltung gespeicherter Modelle (Löschen, Überblick über Dateigrößen)
   - Sicherheitsorientierte Behandlung sensibler Keys (Alpha Vantage Key nur Session)

---

## 5.2 Nutzererlebnis: Einstieg und typischer User Flow

Aus Anwendersicht ist FinSight als Multi-Page-Dashboard konzipiert. Der Einstieg erfolgt über die **Startseite** (`Start.py`), welche eine strukturierte Orientierung bietet und gleichzeitig notwendige Setup-Schritte zentralisiert.

### 5.2.1 Erster Einstieg (Onboarding)

Beim ersten Start wird der Nutzer in der Regel über folgende Reihenfolge geführt:

1. **Welcome**: Kurzüberblick über Ziele und Funktionsumfang  
2. **Setup**: Hinweise zur Bedienung, Konfiguration von:
   - Alpha-Vantage API-Key (für bestimmte Downloads)
   - Ollama-Verbindung (local/host/container)
   - ggf. Standardmodelle für Assistant/LLM Playground

Dieser Flow reduziert Einstiegsbarrieren und adressiert typische Probleme bei daten- und modellgetriebenen Anwendungen: fehlende Keys, fehlende LLM-Verbindung oder unklare Datenquellen.

**Link (Code):**  
- Startseite: [`src/frontend/st/Start.py`](src/frontend/st/Start.py)

---

## 5.3 Dashboard-Struktur: Seiten und Interaktionsprinzipien

Die UI ist in funktionale Bereiche aufgeteilt, die den Arbeitsprozess abbilden: **Daten → Modellierung → LLM → Assistance → Konfiguration**. Die Navigation erfolgt über Streamlit-Seiten im Ordner `pages/`.

**Übersicht (Code):**
- [`src/frontend/st/pages/1 Data.py`](src/frontend/st/pages/1%20Data.py)  
- [`src/frontend/st/pages/2 Machine Learning.py`](src/frontend/st/pages/2%20Machine%20Learning.py)  
- [`src/frontend/st/pages/3 LLM Playground.py`](src/frontend/st/pages/3%20LLM%20Playground.py)  
- [`src/frontend/st/pages/4 Assistant.py`](src/frontend/st/pages/4%20Assistant.py)  
- [`src/frontend/st/pages/5 Settings.py`](src/frontend/st/pages/5%20Settings.py)

---

## 5.4 Data-Seite: Analyse- und Datenmanagement als Dashboard-Erlebnis

Die Data-Seite stellt den zentralen Einstieg in die fachliche Arbeit mit Finanzdaten dar. Der Nutzer erlebt hier eine Kombination aus **Kontrollpanel (Sidebar)** und **Analysefläche (Main Area)**.

### 5.4.1 Sidebar: Kontrollpanel für Datenupdates und Datenimport

Die Sidebar bündelt systemnahe Operationen:
- Anzeige „Last manual update“ als Statuskarte
- Buttons für:
  - **Update All Data**
  - **Update Processed Data**
  - **Update Single Ticker Data**
- Download neuer Ticker (optional, abhängig von Key und Datenquelle)
- Upload eigener Datensätze inkl. Konfliktstrategie (Fail/Replace/Append)

Diese Anordnung unterstützt eine klare Handlungskette:
**(1) Daten verfügbar machen → (2) Daten aktualisieren → (3) Daten analysieren**

### 5.4.2 Analyse-Tab: Interaktive Exploration einzelner Symbole

Im Analysebereich erfolgt die Auswahl eines Symbols aus einer vordefinierten Ticker-Liste (~400 Symbole). Anschließend werden Unternehmensinformationen und Kennzahlen angezeigt (z.B. Sector, Industry, Market Cap, PE Ratio, Beta).  

Darauf aufbauend kann eine Kennzahl bzw. Metrik ausgewählt und als Zeitreihe visualisiert werden. Interaktive Features (Zoom, Hover, Bereichsauswahl) verbessern die Nutzbarkeit insbesondere bei langen Zeitreihen.

### 5.4.3 Compared Stock Analysis: Mehrfachvergleich im selben Dashboard

Die Vergleichsanalyse ermöglicht die Auswahl mehrerer Symbole und zeigt deren Schlusskurse in einer gemeinsamen Visualisierung. Ergänzend werden zentrale Kennzahlen tabellarisch gegenübergestellt. Dies führt zu einem „Dashboard-Charakter“, in dem visuelle Trendbeobachtung (Chart) und kompakte Kennzahlen (Metrikblöcke/Tabelle) kombiniert sind.

### 5.4.4 Tab „Databases“: Transparenz über Datenhaltung

Der zweite Tab liefert eine Übersicht über verfügbare Tabellen (systemseitig und userseitig). Dies wird im Nutzererlebnis als „Admin-/Data-Lake“-Ansicht wahrgenommen und unterstützt:
- Verständnis, welche Daten vorhanden sind
- Debugging (z.B. warum ein Symbol fehlt)
- Kontrolle über userseitige Importe

**Abbildung 5-1 (Platzhalter): Data-Seite – Analyseansicht**  
> *Hier Screenshot einfügen:* Ticker-Auswahl, Unternehmensinfos, Metrik-Auswahl, Chart  
`![Data – Analyseansicht](assets/figures/fig_5_1_data_analysis.png)`

**Abbildung 5-2 (Platzhalter): Data-Seite – Tabellensicht / Datenbanken**  
> *Hier Screenshot einfügen:* Tabellenlisten, User-Tabellen, Row Count  
`![Data – Datenbanken](assets/figures/fig_5_2_data_databases.png)`

---

## 5.5 Machine Learning Studio: Ergebnisorientiertes Training im Dashboard

Das Machine Learning Studio stellt die Transformation von Daten in Modelle als interaktiven Prozess bereit. Aus Nutzersicht wirkt diese Seite wie eine Kombination aus „Training Wizard“ und „Experimentierlabor“ (Playground), wobei die wichtigsten Parameter in der Sidebar konzentriert sind.

### 5.5.1 Sidebar als Trainings-Konsole

Die Sidebar übernimmt die Rolle eines Konfigurationspanels:
- Algorithmuswahl (Regression/Klassifikation)
- Datenquellenauswahl (Yahoo Finance, Alpha Vantage, User Tables)
- Test-Set-Größe (Slider)
- Feature-Scaling (StandardScaler, optional)
- Time-Series Mode (Lag-Features) inkl. Lag-Anzahl
- Training starten per Button

Diese Struktur führt zu einer klaren Interaktionslogik:
**Konfigurieren → Daten laden → Features/Target wählen → Horizon/Time-Series einstellen → Trainieren → Ergebnisse prüfen → Modell speichern**

### 5.5.2 Hauptfläche: Datenkontrolle und Modellbildung

Nach Laden einer Datenquelle zeigt die Seite:
- Übersichtsmodule (Zeilen/Spalten/erkannte Zeitspalte)
- DataFrame Preview (scrollbar)
- Feature- und Target-Auswahl

Die automatische Erkennung einer Zeitspalte („time series found“) wirkt aus Nutzerperspektive als Assistenzfunktion, die Fehler reduziert (z.B. falsche Spaltenwahl für Forecast Horizon).

### 5.5.3 Prognosehorizont und Zeitreihenmodus als besondere Ergebnisfunktion

Zwei Funktionen erhöhen den praktischen Wert für Finanzdaten:

1. **Forecast Horizon (Future Target Shift)**  
   Die Zielvariable wird zeitlich verschoben, um „zukünftige“ Werte zu prognostizieren (1 Day, 3 Weeks, 3 Months, 1 Year).  
   Für Nutzer ist dies eine intuitive Abstraktion: „Ich möchte den Kurs in X Zeit prognostizieren.“

2. **Time-Series Mode (Lag-Features)**  
   Statt manuell viele Features zu wählen, kann die Anwendung Lag-Features aus dem Target erzeugen.  
   Dies erlaubt schnelle Baselines für Zeitreihenmodelle ohne komplexes Feature Engineering.

### 5.5.4 Ergebnisdarstellung: Metriken und Visualisierung

Nach Training werden je nach Modelltyp unterschiedliche Ausgaben gezeigt:

- **Regression:** RMSE, MSE, R² und Vergleichsplot `y_true` vs `y_pred`  
- **Klassifikation:** Accuracy und Konfusionsmatrix

Die Kombination aus numerischen Metriken und Visualisierung unterstützt eine schnelle Ergebnisbewertung im Dashboard-Kontext.

### 5.5.5 Persistenz: Speicherung der Modelle und Wiederverwendung

Modelle werden als `.pkl` gespeichert und enthalten neben dem Modell auch Metadaten (Algorithmus, Features, Scaler, Horizon, Lag-Mode).  
Für Nutzer entsteht dadurch ein „Model Registry“-ähnlicher Effekt: Trainingsläufe werden reproduzierbar und wiederverwendbar.

**Abbildung 5-3 (Platzhalter): ML Studio – Konfiguration und DataFrame Preview**  
`![ML Studio – Daten & Settings](assets/figures/fig_5_3_ml_overview.png)`

**Abbildung 5-4 (Platzhalter): ML Studio – Trainingsergebnisse (Regression)**  
`![ML Studio – Regression Result](assets/figures/fig_5_4_ml_regression_result.png)`

**Abbildung 5-5 (Platzhalter): ML Studio – Trainingsergebnisse (Klassifikation)**  
`![ML Studio – Classification Result](assets/figures/fig_5_5_ml_classification_result.png)`

---

## 5.6 Saved Models: Wiederverwendung als Nutzermehrwert

Die Saved-Models-Ansicht (als separater Bereich/Tab innerhalb der ML-Seite) erweitert das Training um einen praktischen Workflow:

- Übersicht aller Modelle inkl. Metadaten (Algo, Data Source, Target, Horizon, Time-Series Mode)
- Auswahl eines Modells und Anzeige technischer Details
- Download-Funktion für lokale Weiterverwendung
- „Try the model with current data“ als Inferenz-Demo

Aus Nutzerperspektive entsteht so eine nachvollziehbare Kette:
**Trainieren → Speichern → Wiederverwenden → Exportieren**

Diese Funktionalität ist ein wesentliches Ergebnis, da sie ein häufiges Problem in Prototypen löst: Modelle verschwinden nicht nach dem Training, sondern sind als Artefakte verfügbar.

**Abbildung 5-6 (Platzhalter): Saved Models – Modellübersicht**  
`![Saved Models – Overview](assets/figures/fig_5_6_saved_models.png)`

---

## 5.7 LLM Playground: Datenbasierte Analyse als Text-Resultat

Der LLM Playground ergänzt die klassischen ML-Workflows durch eine sprachbasierte Analyse. Der Nutzer erlebt hier ein Dashboard, das nicht primär numerische Outputs liefert, sondern **erklärenden Text**, der aus Datenproben und statistischen Zusammenfassungen erzeugt wird.

### 5.7.1 Verbindungskonzept (local/host/container) als Ergebnis

Die App bietet drei Verbindungsoptionen (Container Ollama / Host / Local).  
Damit ist die Nutzung flexibel: vollständig lokal (datenschutzfreundlich) oder containerisiert (reproduzierbares Deployment).

### 5.7.2 Auswahl der Datenquelle und Sample Size

Analog zur ML-Seite kann eine Datenquelle gewählt werden.  
Zusätzlich wird festgelegt, wie viele Zeilen an das LLM übergeben werden (bis max. 50). Dies wirkt als:
- Sicherheitsmechanismus gegen zu große Prompts
- Usability-Funktion zur Fokussierung auf „aktuelle“ Daten

### 5.7.3 Analysemodi und Custom Prompt

Der Nutzer kann zwischen mehreren Modi wählen:
- Regression
- Classification
- Trend Analysis
- Free Analysis

Damit entsteht ein „Prompt-Template-System“, ohne dass Nutzer direkt Prompt Engineering beherrschen müssen. Der Custom Prompt erlaubt dennoch zusätzliche Steuerung.

### 5.7.4 Ergebnisdarstellung und Transparenz

Das Resultat wird als Text angezeigt („LLM Analysis Result“). Zusätzlich werden:
- Modellname
- Prediction Type
- Datenquelle
- Features/Target
- Antwortzeit
- Sample Size

dokumentiert. Die Einsicht in den generierten Prompt erhöht Transparenz und Nachvollziehbarkeit.

**Abbildung 5-7 (Platzhalter): LLM Playground – Konfiguration und Resultat**  
`![LLM Playground – Result](assets/figures/fig_5_7_llm_playground.png)`

---

## 5.8 Assistant: Nutzerunterstützung als Dashboard-Komponente

Der Assistant stellt ein ergänzendes Ergebnis dar, das weniger auf Datenanalyse und stärker auf **Hilfe und Guidance** ausgerichtet ist.  

Aus Nutzersicht ist dies ein „kontextueller Helpdesk“, der:
- Fragen zur Anwendung beantwortet
- Hinweise zu Modelltraining und Interpretation geben kann
- den Einstieg für nicht-technische Nutzer erleichtert

Wesentliche UI-Elemente:
- Chatfenster
- Reset des Chatverlaufs
- Anzeige des aktuell verwendeten Modells (z.B. `phi3:mini`)

**Abbildung 5-8 (Platzhalter): Assistant – Chat-Interface**  
`![Assistant – Chat UI](assets/figures/fig_5_8_assistant.png)`

---

## 5.9 Settings: Konfiguration als Ergebnis für Wartbarkeit und Steuerbarkeit

Die Settings-Seite ist aus Ergebnis-Sicht ein zentraler Baustein, da sie die App **langfristig nutzbar** macht. Sie reduziert Hardcoding und erlaubt Anpassungen ohne Codeänderung.

### 5.9.1 Global Settings
- Ollama-Konfiguration (Local/Standard)
- Reset-Funktionen
- Alpha Vantage Key Eingabe (Session-orientiert)

### 5.9.2 Data Settings
- Löschen ausgewählter Tabellen (mit Sicherheitsabfrage)
- Initial Ticker Verwaltung (Standardliste vs. Customliste)
- Begrenzung des frühesten Analyse-Datums (Performance und Fokus)

### 5.9.3 Machine Learning Settings
- Übersicht und Löschung gespeicherter Modelle
- Konfiguration Training Limits:
  - minimal erforderliche Zeilenanzahl
  - maximale Trainingszeilen

### 5.9.4 Assistant Settings
- Auswahl der Ollama-Quelle
- Modellmanagement inkl. Download falls nicht verfügbar

**Abbildung 5-9 (Platzhalter): Settings – Konfigurationsbereiche**  
`![Settings – Overview](assets/figures/fig_5_9_settings.png)`

---

## 5.10 Zusammenfassung der Ergebnisse und Bewertung aus Nutzersicht

### 5.10.1 Erreichte Anforderungen

Die Anwendung erfüllt die Kernanforderung einer **anwenderfreundlichen Finanzanalyse-Plattform**, indem sie:
- mehrere Datenquellen integriert
- Daten persistiert und verwaltet
- ML-Training und LLM-Analyse in UI-Workflows übersetzt
- Ergebnisse verständlich visualisiert oder textuell erklärt
- zentrale Konfiguration über Settings bereitstellt
- lokal wie containerisiert betrieben werden kann

### 5.10.2 Stärken des Dashboards
- **Modularität im UI:** klare Seitenstruktur entlang typischer Workflows  
- **Niedrige Einstiegshürde:** Setup-Seite und Assistant reduzieren Fehlbedienung  
- **Exploration + Experiment:** Data-Seite (Exploration) und ML/LLM (Experiment) ergänzen sich  
- **Persistenz:** gespeicherte Modelle und system_config ermöglichen Wiederverwendung  
- **Lokaler Betrieb (Privacy):** Ollama lokal/containerisiert ohne Cloud-Abhängigkeit

### 5.10.3 Grenzen und beobachtbare Einschränkungen
- Große Tabellen (z.B. mehrere Millionen Zeilen) können Ladezeiten verursachen; Sicherheitslimits begrenzen Trainingszeilen.
- Die ML-Seite stellt primär eine Trainingsumgebung bereit; fachliche Validität hängt stark von sinnvoller Feature/Target-Auswahl ab.
- LLM-Analysen sind abhängig von Modellqualität, Promptlänge und Datenprobe; Ergebnisse sind qualitativ, nicht deterministisch.
- Alpha Vantage Limits (Requests pro Minute/Tag) beeinflussen Download-Workflows.

### 5.10.4 Ergebnischarakter
Insgesamt ist FinSight als **funktionsfähiger Prototyp** mit ausgeprägtem Dashboard-Charakter zu bewerten. Die Anwendung demonstriert die Integration von:
- Dateninfrastruktur (SQLite, ETL, Updates)
- klassischer Analytics (Charts, Kennzahlen)
- ML-Workflows (Training, Evaluation, Model Bundles)
- LLM-Workflows (Prompting, Analyse, Assistenz)

Damit wurde ein umfassendes, interaktives Ergebnis artefaktisch umgesetzt, das sowohl für explorative Nutzung (Analyse & Vergleiche) als auch für experimentelle Modellierung (ML/LLM) geeignet ist.

---

## 5.11 Hinweise zur Dokumentation der Abbildungen

Für die finale Berichtsversion wird empfohlen, die Platzhalter-Abbildungen durch Screenshots zu ersetzen.  
Geeignete Screenshots sind insbesondere:

- Data: Analyseansicht + Vergleichsanalyse + Datenbanken-Tab
- ML Studio: Einstellungen + DataFrame Preview + Ergebnisansichten (Regression/Klassifikation)
- Saved Models: Übersicht + Modelldetail + Inferenz-Expander
- LLM Playground: Verbindungs-Setup + Ergebnis + Prompt-Ansicht
- Assistant: Chatfenster
- Settings: Global/Data/ML/Assistant Bereiche

Zur konsistenten Referenzierung im Bericht empfiehlt sich ein Ordner, z.B.:  
`src/frontend/st/assets/figures/` oder `report_assets/figures/`  
und ein fortlaufendes Abbildungsnummern-Schema.



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
- Streamlit Inc. (2024). Streamlit Documentation. https://docs.streamlit.io
- Yahoo Finance (2024). Adjusted Close Definition. https://finance.yahoo.com

Hinweis: Alle relativen Pfadangaben in diesem Dokument (z.B. db_functions.py) sind als Hyperlinks konzipiert, die bei Anzeige im Repository direkt zu den entsprechenden Dateien führen.


# Probleme: LLM passt nicht gut zur ausgabe ist beschränkt auf Kapazität

# Unsaubere impolementierung mit Load_data und knopf druck

# Alphavntage erfordert Key

# performance nicht gut

# Andere Datenbank maybe besser