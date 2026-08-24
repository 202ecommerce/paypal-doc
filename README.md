# Documentation fonctionnelle – Module PayPal PrestaShop

## Installation locale

```bash
pip install -r requirements.txt
mkdocs serve
```

Le PDF n'est pas généré en local par défaut (build plus lent). Pour le forcer :

```bash
ENABLE_PDF_EXPORT=1 mkdocs build
```

## Déploiement

Le workflow `.github/workflows/docs.yml` build le site (HTML + PDF) et le publie
automatiquement sur la branche `gh-pages` à chaque push sur `main`.

Étape à faire une seule fois côté GitHub : Settings > Pages > Build and deployment >
Source = "Deploy from a branch" > sélectionner la branche `gh-pages`.

Le PDF sera accessible à l'URL : `https://<user>.github.io/<repo>/pdf/documentation-paypal.pdf`
