# ERGEBNISSE – Laufzeitanalyse Suchalgorithmen

**Lehrveranstaltung:** Datenstrukturen und Algorithmen  

---

## 1. Erwartetes Laufzeitverhalten

### 1.1 Algorithmen

| Algorithmus | Durchschnitt | Worst Case | Bemerkung |
|---|---|---|---|
| `linear_search` | O(n) | O(n) | Kein Vorteil durch Sortierung |
| `binary_search` | O(log n) | O(log n) | Gleichmäßige Halbierung des Suchraums |
| `interpolation_search` | O(log log n) | O(n) | Optimal bei gleichmäßiger Verteilung |
| `quad_search` | O(log n) | O(log n) | Sprünge der Größe √n, dann binäre Suche |

### 1.2 Testdaten

**`make_linear_array(n)`**  
Das Array enthält Werte nahe bei i (ganzzahlige Indizes mit minimalem Rauschen ±0,4), d. h. die Werte sind annähernd gleichmäßig verteilt. Die Interpolationssuche kann dadurch ihre optimale Komplexität O(log log n) annähern, da die Interpolationsformel sehr präzise auf die gesuchte Position zeigt.

**`make_random_sorted_array(n)`**  
Die Werte werden gleichmäßig aus [0, 2n) gezogen und sortiert. Auch hier liegt im Erwartungswert eine gleichmäßige Verteilung vor. Die Interpolationssuche sollte ebenfalls nahe an O(log log n) liegen. Binäre und quadratische Suche bleiben stabil bei O(log n).

**`make_worst_case_array(n)`**  
Das Array besteht aus den Werten 0, 1, …, n−2 gefolgt von einem einzelnen Ausreißer n². Dieser extreme Ausreißer am Ende verzerrt die lineare Interpolationsschätzung massiv: Die Formel überschätzt die Position des gesuchten Werts stark, weshalb viele Iterationen notwendig werden. Das Ergebnis ist ein Worst-Case-Verhalten von O(n) für `interpolation_search`. Binäre Suche und quadratische Binärsuche sind von der Werteverteilung unabhängig und bleiben bei O(log n).

---

## 2. Messergebnisse

> *Tabellen werden nach der Implementierung mit den tatsächlichen Messwerten befüllt.*

### 2.1 Haupttabelle (Zeiten in µs)

#### Array-Typ: `linear`

| Algorithmus | n=1 000 | n=5 000 | n=20 000 | n=100 000 |
|---|---|---|---|---|
| `linear_search` | | | | |
| `binary_search` | | | | |
| `interpolation_search` |1.31µs|1.23µs|1.19µs|1.23µs|
| `quad_search` |4.60µs|1.80µs|1.80µs|2.20µs|

#### Array-Typ: `random_sorted`

| Algorithmus | n=1 000 | n=5 000 | n=20 000 | n=100 000 |
|---|---|---|---|---|
| `linear_search` | | | | |
| `binary_search` | | | | |
| `interpolation_search` |2.40µs|1.21µs|2.42µs|2.32µs|
| `quad_search` |4.30µs|4.10µs|4.60µs|10.40µs|

#### Array-Typ: `worst_case`

| Algorithmus | n=1 000 | n=5 000 | n=20 000 | n=100 000 |
|---|---|---|---|---|
| `linear_search` | | | *(skipped)* | *(skipped)* |
| `binary_search` | | | | |
| `interpolation_search` |269.62µs|1375.88µs|5542.11µs|28015.75µs|
| `quad_search` |4.40µs|7.40µs|12.30µs|25.40µs|

### 2.2 Worst-Case-Demonstration `interpolation_search`

| Algorithmus | n=1 000 | n=5 000 | n=10 000 | n=20 000 | n=50 000 | n=100 000 |
|---|---|---|---|---|---|---|
| `binary_search` | | | | | | |
| `interpolation_search` |265.46µs|1354.46µs|2758.45µs|5472.29µs|13788.04µs|27175.82µs|
| `quad_search` |3.70µs|5.70µs|7.20µs|11.90µs|13.90µs|19.10µs|

---

## 3. Auswertung

> *Wird nach der Implementierung und Messung ausgefüllt.*

### 3.1 Entsprechen die Ergebnisse den Erwartungen?

**`linear_search`:**  
*(Beobachtung und Vergleich mit erwartetem O(n) eintragen)*

**`binary_search`:**  
*(Beobachtung und Vergleich mit erwartetem O(log n) eintragen)*

**`interpolation_search`:**  
  Bei linearen Daten bleibt die laufzeit fast gleich, bei random nicht mehr perfekt linear da die schätzung schwieriger ist.
  Beim Worstcase wächst die Laufzeit fast proportional zu den Elementen.

**`quad_search`:**  
Quad Search liegt erwartungsgemäß zwischen Binary und Interpolation: im Normalfall ähnlich schnell wie Binary,
 im Worst Case ist es aber deutlich besser als Interpolation aber schlechter als Binary.

### 3.2 Auffälligkeiten

*(Besonderheiten, Abweichungen oder interessante Beobachtungen hier festhalten)*

---

## 4. Fazit

*(Kurze Zusammenfassung der wichtigsten Erkenntnisse aus dem Vergleich der Algorithmen)*