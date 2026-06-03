# Programmieraufgabe 3 – Suchalgorithmen

**Lehrveranstaltung:** Datenstrukturen und Algorithmen  
**Betreuer:** DI Dr. Dirk Martin  
**Abgabe:** bis 10.06.  

---

## Aufgabenstellung

Implementierung und Laufzeitanalyse verschiedener Suchalgorithmen in Python auf Basis der Vorlage `assignment_3.py`.

### Zu implementierende Methoden

| Methode | Beschreibung |
|---|---|
| `linear_search` | Sequentielle Suche (ggf. zu adaptieren) |
| `binary_search` | Klassische binäre Suche auf sortierten Arrays |
| `interpolation_search` | Interpolationssuche auf sortierten Arrays |
| `quad_search` | Quadratische Binärsuche auf sortierten Arrays |

### Testdaten-Generatoren

Drei verschiedene Array-Typen werden zur Laufzeitmessung verwendet:

| Generator | Beschreibung |
|---|---|
| `make_linear_array(n)` | Sortiertes Array mit Werten ≈ i + kleines Rauschen |
| `make_random_sorted_array(n)` | Sortiertes Array mit n zufälligen Floats aus [0, 2n) |
| `make_worst_case_array(n)` | Array, das O(n)-Verhalten bei `interpolation_search` erzwingt |

---

## Projektstruktur

```
.
├── README.md
├── ERGEBNISSE.md
└── assignment_3.py
```

---

## Ausführung

```bash
python assignment_3.py
```

Das Skript gibt eine Laufzeittabelle für alle Suchmethoden über verschiedene Array-Typen und Größen (n = 1 000, 5 000, 20 000, 100 000) aus, gefolgt von einer Worst-Case-Demonstration für `interpolation_search`.

---

## Abgabe

- `assignment_3.py` (vollständig implementiert)
- `ERGEBNISSE.md` (Laufzeitanalyse und Kommentare)
- Abgabe über GitHub / Moodle