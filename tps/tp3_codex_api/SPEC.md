# Règles métier — remboursement des notes de frais

Document de référence fourni par le service comptable. Le script `legacy/notes_frais.py` est censé les appliquer.

## Données

Fichier CSV, séparateur `;`, une dépense par ligne : `date;salarie;categorie;montant;devise`.

- `date` : AAAA-MM-JJ.
- `montant` : nombre positif, avec un point **ou une virgule** décimale (`12.50` ou `12,50`).
- `devise` : `EUR`, `USD` ou `GBP`.

## Règles

1. **Conversion d'abord.** Chaque montant est converti en euros avec les taux du fichier `taux.json` (1 USD = 0,92 EUR, 1 GBP = 1,17 EUR). Les plafonds s'appliquent **après** conversion.
2. **Plafonds par dépense**, en euros :
   - `repas` : 25,00 ;
   - `hotel` : 120,00 ;
   - `transport` : pas de plafond.
3. Le montant remboursé d'une dépense est le minimum entre le montant converti et le plafond, arrondi au centime.
4. **Catégorie inconnue** : la dépense n'est pas remboursée et elle est signalée (on ne l'ignore pas en silence).
5. Le total d'un salarié est la somme de ses dépenses remboursées, arrondie au centime.

## Sortie

Une ligne par salarié, triée par nom : `Nom : 123,45 EUR`. Puis, s'il y en a, la liste des dépenses rejetées avec leur motif.

## Exemples

| Dépense | Converti | Remboursé |
|---|---|---|
| repas, 18,00 EUR | 18,00 | 18,00 |
| repas, 32,00 EUR | 32,00 | 25,00 |
| hotel, 110 GBP | 128,70 | 120,00 |
| repas, 26 USD | 23,92 | 23,92 |
| taxi, 15 EUR | — | rejetée : catégorie inconnue |
