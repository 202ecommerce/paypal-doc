# Documentation utilisateur – Module PayPal Officiel pour PrestaShop

Documentation du module PayPal V6.X pour PrestaShop V1.7.X et supérieur.
Site statique généré avec [MkDocs](https://www.mkdocs.org/) et le thème
[Material](https://squidfunk.github.io/mkdocs-material/), aux couleurs de la charte PayPal.

## Installation locale

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Puis lancer le serveur de développement (rechargement automatique) :

```bash
.venv/bin/mkdocs serve
```

Le site est alors disponible sur <http://127.0.0.1:8000>.

### macOS sans droits administrateur

Le plugin d'export PDF (`mkdocs-with-pdf`) s'appuie sur WeasyPrint, qui exige les
bibliothèques système Pango et Cairo — installables via Homebrew, donc indisponibles
sans droits admin. Dans ce cas, utiliser la configuration de dev qui désactive ce plugin :

```bash
.venv/bin/mkdocs serve -f mkdocs.local.yml
```

Le PDF reste généré normalement en production par la CI, qui installe ces bibliothèques.

### Générer le PDF en local

```bash
ENABLE_PDF_EXPORT=1 .venv/bin/mkdocs build
```

## Structure

| Chemin | Rôle |
| --- | --- |
| `docs/` | Les pages Markdown, une par chapitre du document source |
| `docs/assets/img/` | Captures d'écran et GIF de démonstration du back-office |
| `docs/assets/css/paypal.css` | Charte graphique PayPal (couleurs, typographie, composants) |
| `mkdocs.base.yml` | Configuration commune : thème, navigation (`nav:`), plugins |
| `mkdocs.yml` | Production — hérite de la base et ajoute l'export PDF. C'est ce fichier que lance la CI. |
| `mkdocs.local.yml` | Développement — hérite de la base, sans l'export PDF |
| `tools/import-google-doc.py` | Ré-import du contenu depuis le Google Doc |

Les plugins sont déclarés en **mapping** et non en liste : l'héritage MkDocs fusionne
les mappings mais remplace les listes. Une liste ferait disparaître les plugins de la
base dans les configurations qui en héritent — et l'aperçu local cesserait de refléter
la production.

Pour ajouter une page : créer le fichier `.md` dans `docs/`, **puis la déclarer dans la
section `nav:` de `mkdocs.yml`** — sans quoi elle n'apparaîtra pas dans le menu.


## Traductions

Le français est la langue par défaut et vit à la racine ; l'anglais vit sous `/en/`.
Chaque page existe en deux fichiers :

```
docs/configuration.md      ->  /configuration/    (français)
docs/configuration.en.md   ->  /en/configuration/ (anglais)
```

Les deux langues sont générées par le même convertisseur, depuis deux Google Docs
distincts. Les libellés de navigation se traduisent dans `nav_translations`, sous la
locale `en` de `mkdocs.base.yml`.

### Images

| | Emplacement |
| --- | --- |
| Captures françaises | `docs/assets/img/` |
| Captures anglaises | `docs/assets/img/en/` |
| GIF de démonstration | `docs/assets/img/` — **mutualisés entre les deux langues** |

Les GIF de l'export anglais sont les mêmes enregistrements d'écran que les français,
réencodés sept fois plus lourds (71 Mo contre 10). Le convertisseur ne les recopie
donc pas côté anglais.

> **État des visuels.** Les captures anglaises portent des annotations en anglais,
> mais l'interface PrestaShop qu'elles montrent reste en français. Les GIF sont
> intégralement en français. Une version anglaise complète suppose de réenregistrer
> ces visuels sur une boutique en locale anglaise.

## Mettre à jour le contenu depuis les Google Docs

1. Dans le Google Doc : **Fichier > Télécharger > Page Web (.html, compressé)**.
   C'est le seul export qui conserve les **GIF animés** et la résolution d'origine des
   images — l'export Markdown les aplatit en PNG et les redimensionne à 605 px.
2. Décompresser le zip dans `tools/export/fr/` ou `tools/export/en/`.
3. Lancer :

```bash
.venv/bin/python tools/import-google-doc.py fr
```

```bash
.venv/bin/python tools/import-google-doc.py en
```

Le script régénère l'intégralité des pages de la langue demandée, sans toucher à
l'autre : il résout les emphases portées par des classes CSS, déballe les liens du
redirecteur Google, remet les titres à leur niveau, répare les en-têtes de tableaux,
renomme les images et convertit les blocs « NB / A noter / Attention » (et leurs
équivalents anglais) en encarts. **Le texte n'est jamais reformulé.**

Il signale en fin d'exécution tout lien interne non résolu — Google Docs référence
parfois des signets qu'il n'exporte pas. Les corriger dans `SIGNETS_PERDUS`.

Toute correction faite à la main dans `docs/` sera écrasée : corriger le Google Doc,
puis réimporter.

## Contrôle qualité du design

Le dépôt utilise [impeccable](https://impeccable.style) pour détecter les anti-patterns
d'interface. Les règles ignorées sont partagées dans `.impeccable/config.json`.

Installation (non versionnée, 14 Mo de binaires) :

```bash
npx impeccable install
```

Lancer le détecteur sur le site généré :

```bash
.claude/skills/impeccable/scripts/impeccable detect site/ docs/assets/css/paypal.css
```

## Déploiement

Le workflow `.github/workflows/docs.yml` build le site (HTML + PDF) et le publie
automatiquement sur la branche `gh-pages` à chaque push sur `main`.

Étape à faire une seule fois côté GitHub : Settings > Pages > Build and deployment >
Source = "Deploy from a branch" > sélectionner la branche `gh-pages`.

Le PDF sera accessible à l'URL : `https://<user>.github.io/<repo>/pdf/documentation-paypal.pdf`
