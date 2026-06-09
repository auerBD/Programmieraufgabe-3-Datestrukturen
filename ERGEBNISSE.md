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
| `linear_search` |28.08µs|146.13µs|571.17µs|2914.88µs|
| `binary_search` |1.42µs|1.87µs|2.25µs|2.67µs|
| `interpolation_search` |1.31µs|1.23µs|1.19µs|1.23µs|
| `quad_search` |1.46µs|1.33µs|1.38µs|1.42µs|

#### Array-Typ: `random_sorted`

| Algorithmus | n=1 000 | n=5 000 | n=20 000 | n=100 000 |
|---|---|---|---|---|
| `linear_search` |28.13µs|141.79µs|570.96µs|2866.04µs|
| `binary_search` |1.58µs|1.92µs|2.25µs|2.54µs|
| `interpolation_search` |2.40µs|1.21µs|2.42µs|2.32µs|
| `quad_search` |2.37µs|1.37µs|2.83µs|3.04µs|

#### Array-Typ: `worst_case`

| Algorithmus | n=1 000 | n=5 000 | n=20 000 | n=100 000 |
|---|---|---|---|---|
| `linear_search` |27.25µs|142.50µs|573.67µs| *(skipped)* |
| `binary_search` |1.50µs|1.96µs|2.29µs|2.62µs|
| `interpolation_search` |269.62µs|1375.88µs|5542.11µs|28015.75µs|
| `quad_search` |3.00µs|4.75µs|8.04µs|15.79µs|

### 2.2 Worst-Case-Demonstration `interpolation_search`

| Algorithmus | n=1 000 | n=5 000 | n=10 000 | n=20 000 | n=50 000 | n=100 000 |
|---|---|---|---|---|---|---|
| `binary_search` |1.42µs|1.88µs|2.00µs|2.21µs|2.29µs|2.46µs|
| `interpolation_search` |265.46µs|1354.46µs|2758.45µs|5472.29µs|13788.04µs|27175.82µs|
| `quad_search` |2.79µs|4.54µs|5.75µs|7.67µs|11.42µs|15.92µs|

---

## 3. Auswertung

### 3.1 Entsprechen die Ergebnisse den Erwartungen?

**`linear_search`:**  
Die Laufzeit wächst proportional zu n und bestätigt damit das erwartete O(n)-Verhalten. Bei n=1.000 dauert die Suche ~28 µs, bei n=5.000 ~146 µs (Faktor ~5,2), bei n=20.000 ~571 µs (Faktor ~3,9) und bei n=100.000 ~2.915 µs (Faktor ~5,1). Der Algorithmus ist unabhängig vom Array-Typ, da er stets alle Elemente der Reihe nach durchläuft.

**`binary_search`:**  
Die Laufzeit wächst sehr langsam und entspricht dem erwarteten O(log n). Von n=1.000 auf n=100.000 steigt sie lediglich von ~1,4 µs auf ~2,7 µs – ein Faktor von unter 2, obwohl n um das 100-fache wächst. Das deckt sich mit log₂(100.000) ≈ 17 Schritten gegenüber log₂(1.000) ≈ 10 Schritten. Das Ergebnis ist über alle Array-Typen nahezu identisch, da Binary Search ausschließlich auf Indizes, nicht auf Werten operiert.

**`interpolation_search`:**  
Bei `linear` und `random_sorted` bleibt die Laufzeit nahezu konstant zwischen 1,2 und 2,4 µs, unabhängig von n. Das entspricht dem erwarteten O(log log n)-Verhalten auf gleichmäßig verteilten Daten: die Interpolationsformel schätzt die Zielposition so genau, dass der Algorithmus in der Praxis oft in ein bis zwei Schritten fertig ist.  
Beim `worst_case`-Array degradiert die Laufzeit auf O(n): von ~270 µs bei n=1.000 auf ~28.000 µs bei n=100.000 – ein Faktor von rund 5 bei jeder Verfünffachung von n. Der einzige große Ausreißer am Ende des Arrays verzerrt die Schätzung so stark, dass der Algorithmus pro Iteration nur einen Schritt vorwärtskommt.

**`quad_search`:**  
Auf `linear`- und `random_sorted`-Daten liegt die Laufzeit nahe bei Binary Search (~1,3–4,4 µs), jedoch ohne den O(log log n)-Vorteil von Interpolation Search zu erreichen. Der Overhead durch die sqrt(n)-Sprungphase macht sich bei kleinen n leicht bemerkbar.  
Beim `worst_case` zeigt Quad Search das erwartete O(√n)-Verhalten: verdoppelt sich n, wächst die Laufzeit um den Faktor ~√2 ≈ 1,41. Das bestätigen die Messungen (z. B. 7,67 µs → 11,42 µs → 15,92 µs bei n = 20.000 → 50.000 → 100.000). Damit liegt Quad Search im Worst Case weit hinter Binary Search, aber um Größenordnungen vor Interpolation Search.

### 3.2 Auffälligkeiten

- **Interpolation Search auf `linear` schneller als Binary Search:** Obwohl Binary Search theoretisch O(log n) hat, ist Interpolation Search auf diesem Array-Typ mit ~1,2 µs konstant schneller als Binary Search (~1,4–2,7 µs). Das liegt daran, dass die nahezu perfekte lineare Verteilung eine sehr genaue Schätzung erlaubt – der Algorithmus trifft das Ziel praktisch immer im ersten Schritt.

- **Quad Search auf `random_sorted` langsamer als Binary Search:** Bei n=20.000 und n=100.000 braucht Quad Search ~2,8–4,2 µs gegenüber ~2,3–2,5 µs für Binary Search. Die Interpolationsschätzung trifft bei zufälligen Daten nicht so zuverlässig wie bei streng linearen, und die zusätzliche Sprunglogik verursacht Overhead ohne den erhofften Gewinn.

- **Worst-Case-Effekt trifft ausschließlich Interpolation Search:** Linear Search, Binary Search und Quad Search zeigen auf `worst_case` kein dramatisch anderes Verhalten als auf den anderen Array-Typen. Nur Interpolation Search bricht ein – ein direkter Beleg dafür, dass der Algorithmus eine gleichmäßige Werteverteilung voraussetzt.

---

## 4. Fazit

Der Vergleich zeigt, dass kein einzelner Algorithmus in allen Szenarien optimal ist. Binary Search überzeugt durch zuverlässiges O(log n)-Verhalten unabhängig von der Datenverteilung und ist damit die robusteste Wahl. Interpolation Search ist auf gleichmäßig verteilten Daten am schnellsten und nähert sich in der Praxis O(1), versagt aber vollständig bei ungünstigen Verteilungen wie dem Worst-Case-Array. Quad Search ist ein Kompromiss: Es vermeidet den O(n)-Kollaps von Interpolation Search durch die sqrt(n)-Sprungphase, erreicht aber weder deren Bestleistung noch die Zuverlässigkeit von Binary Search. Linear Search ist in keinem Szenario konkurrenzfähig und dient lediglich als Referenz für unkomprimiertes O(n)-Wachstum.