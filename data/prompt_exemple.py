
PROMPT: str = """

........

## Formatage Markdown avancé (strict Obsidian)
- Hiérarchisation: # pour titre principal, ## pour sections principales, ### pour sous-sections, #### pour concepts spécifiques
- **Mettre en gras** uniquement les définitions critiques et termes techniques fondamentaux
- *Mettre en italique* les variables dans le texte (hors formules)
- Formules mathématiques: utiliser LaTeX entre $$ pour les équations complexes, $ pour les expressions simples dans le texte
- Exemple de formule: $$\Delta S = \frac{Q}{T}$$ où $\Delta S$ représente la variation d'entropie
- Pour chaque formule importante: expliquer la signification physique et les unités de chaque variable

## Liens et références croisées Obsidian
- Créer des liens internes avec [[concept]] pour tous les termes techniques majeurs (minimum 15-20 liens)
- Utiliser la syntaxe ![[diagramme_conceptuel]] pour référencer les diagrammes importants
- Grouper les concepts connexes avec des tags spécifiques: #principe #cycle #composant #coefficient

## Callouts et éléments visuels Obsidian
- > [!NOTE] Pour les définitions fondamentales et clarifications
- > [!TIP] Pour les astuces de calcul ou d'application pratique
- > [!WARNING] Pour les limitations, précautions ou erreurs courantes
- > [!IMPORTANT] Pour les principes fondamentaux ou règles critiques
- > [!EXAMPLE] Pour les cas d'application concrets


PRODUIT directement le résumé technique en Markdown sans aucun commentaire préliminaire ou conclusif sur le processus. Ne pas encadrer la réponse de backticks.
"""