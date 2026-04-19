# primo-progetto

## Stato
Repo iniziale — stack e scopo da definire.

## Convenzioni di lavoro (anti context-rot)

1. **Una sessione = un task.** A task chiuso: `/clear` o nuova sessione.
2. **Niente memoria implicita.** Tutto ciò che serve ricordare va in file:
   - Decisioni architetturali → `docs/decisions.md`
   - Piano corrente → `TODO.md`
   - Convenzioni → questo file
3. **Commit atomici.** Un task = un commit. Messaggi in italiano o inglese, imperativo.
4. **Subagent per esplorare.** Ricerche nel codice → Agent `Explore`, non lettura diretta.
5. **Branch di lavoro:** `claude/repo-cleanup-XKS7I` (non pushare altrove senza permesso).

## Comandi rapidi
_Da compilare quando il progetto avrà uno stack:_
- Install: `TODO`
- Dev: `TODO`
- Test: `TODO`
- Lint: `TODO`

## Stack
_Da definire._

## Subagent (quando delegare)

L'utente è inesperto: **è Claude a decidere** quando lanciare un subagent.

Usa subagent quando:
- **Explore** → ricerche ampie nel codice, domande "come funziona X in tutto il progetto"
- **Plan** → progettare implementazioni complesse multi-file
- **general-purpose** → task multi-step con molte letture

Non usare subagent per:
- Leggere un file noto (usa `Read`)
- Cercare una singola stringa (usa `Grep`)
- Task piccoli e locali

Quando l'utente dice *"analizza tutto…"*, *"come funziona X in tutto il progetto"*,
*"pianifica come aggiungere…"* → delega automaticamente senza chiedere.

## Note
- Leggere `TODO.md` all'inizio di ogni sessione per sapere a che punto siamo.
- Se stai spiegando la stessa cosa due volte, scrivila qui.
