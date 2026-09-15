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
| `docs/` | Les pages Markdown |
| `docs/assets/img/` | Captures d'écran du back-office |
| `docs/assets/css/paypal.css` | Charte graphique PayPal (couleurs, typographie, composants) |
| `mkdocs.yml` | Configuration du site et arborescence de navigation (`nav:`) |
| `mkdocs.local.yml` | Surcharge de dev local, non versionnée |

Pour ajouter une page : créer le fichier `.md` dans `docs/`, **puis la déclarer dans la
section `nav:` de `mkdocs.yml`** — sans quoi elle n'apparaîtra pas dans le menu.

## Déploiement

Le workflow `.github/workflows/docs.yml` build le site (HTML + PDF) et le publie
automatiquement sur la branche `gh-pages` à chaque push sur `main`.

Étape à faire une seule fois côté GitHub : Settings > Pages > Build and deployment >
Source = "Deploy from a branch" > sélectionner la branche `gh-pages`.

Le PDF sera accessible à l'URL : `https://<user>.github.io/<repo>/pdf/documentation-paypal.pdf`
