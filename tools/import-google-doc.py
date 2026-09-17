"""Convertit l'export « Page Web » du Google Doc en pages MkDocs.
Le texte est repris verbatim ; seules la syntaxe Markdown et la structure changent."""
import re, pathlib, shutil
from urllib.parse import urlparse, parse_qs, unquote
from bs4 import BeautifulSoup
from markdownify import markdownify
from markdown.extensions.toc import slugify

# Usage : décompresser l'export « Page Web (.html, compressé) » du Google Doc
#         dans tools/export/<langue>/, puis lancer depuis la racine du dépôt :
#             .venv/bin/python tools/import-google-doc.py fr
#             .venv/bin/python tools/import-google-doc.py en
import sys
LANGUE = (sys.argv[1] if len(sys.argv) > 1 else "fr").lower()
if LANGUE not in ("fr", "en"):
    sys.exit("langue inconnue : attendu fr ou en")
SUFFIXE = "" if LANGUE == "fr" else "." + LANGUE          # docs/page.md / docs/page.en.md
SRC  = pathlib.Path(__file__).parent / "export" / LANGUE
HTML = next(SRC.glob("*.html"))
DOCS = pathlib.Path("docs")
IMG  = DOCS / "assets" / "img"

soup = BeautifulSoup(HTML.read_text(encoding="utf-8"), "html.parser")

# ---------------------------------------------------------------- 1. liens
for a in soup.find_all("a", href=True):
    if "google.com/url" in a["href"]:
        q = parse_qs(urlparse(a["href"]).query).get("q")
        if q:
            a["href"] = unquote(q[0])

# ------------------------------------------------- 2. emphases portées par CSS
css = re.search(r'<style[^>]*>(.*?)</style>', HTML.read_text(encoding="utf-8"), re.S).group(1)
BOLD, ITAL = set(), set()
for m in re.finditer(r'\.(c\d+)\{([^}]*)\}', css):
    cls, body = m.groups()
    if 'font-weight:700' in body:   BOLD.add(cls)
    if 'font-style:italic' in body: ITAL.add(cls)

def style_of(span):
    c = set(span.get("class") or [])
    return (bool(c & BOLD), bool(c & ITAL))

# fusionne les <span> voisins de même style : évite les « *29**jours* » à la conversion
for parent in soup.find_all(["p", "h1", "h2", "h3", "h4", "li", "td"]):
    prev = None
    for span in list(parent.find_all("span", recursive=False)):
        if prev is not None and style_of(prev) == style_of(span):
            for child in list(span.contents):
                prev.append(child)
            span.decompose()
        else:
            prev = span

for span in soup.find_all("span"):
    if not span.get_text(strip=True):
        continue
    b, i = style_of(span)
    if b: span.wrap(soup.new_tag("strong"))
    if i: span.wrap(soup.new_tag("em"))

# un paragraphe tout en italique : on remonte l'emphase au niveau du paragraphe,
# sinon markdownify produit des « ****et**** » aux jointures de spans
for para in soup.find_all(["p", "li"]):
    texts = [n for n in para.descendants if isinstance(n, str) and n.strip()]
    if not texts or not all(n.find_parent("em") for n in texts):
        continue
    for em in para.find_all("em"):
        em.unwrap()
    wrapper = soup.new_tag("em")
    for child in list(para.contents):
        wrapper.append(child.extract())
    para.append(wrapper)

# cellules de tableau : une ligne par paragraphe, séparées par <br>
for td in soup.find_all("td"):
    paras = td.find_all("p")
    for i, para in enumerate(paras):
        if i:
            para.insert_before(soup.new_tag("br"))
        para.unwrap()

# ---------------------------------------------------------------- 3. images
# Les GIF de l'export anglais sont les mêmes enregistrements d'écran français,
# réencodés 7x plus lourds (71 Mo contre 10). On réutilise donc les fichiers
# français : contenu identique, poids divisé par sept.
GIFS = {
    "installation-module.gif", "paiement-paypal.gif", "pay-later-activation.gif",
    "pay-later-messages.gif", "personnalisation-shortcuts.gif",
}
RENOMMAGE = {
 "fr": {
    "image18.gif": "installation-module.gif",      "image2.png":  "page-configuration.png",
    "image7.png":  "mode-prelevement.png",         "image20.gif": "paiement-paypal.gif",
    "image23.png": "shortcut-page-produit.png",    "image17.png": "shortcut-page-panier.png",
    "image14.png": "shortcut-inscription.png",     "image3.png":  "avantages-paypal-bouton.png",
    "image11.png": "avantages-paypal-inscription.png", "image12.png": "bouton-dans-page-commande.png",
    "image10.png": "bouton-fin-de-page.png",       "image6.gif":  "pay-later-activation.gif",
    "image16.gif": "pay-later-messages.gif",       "image1.gif":  "personnalisation-shortcuts.gif",
    "image8.png":  "onboarding-1-connexion.png",   "image13.png": "onboarding-1-code-compte.png",
    "image4.png":  "onboarding-2-checkout.png",    "image5.png":  "onboarding-3-pay-later.png",
    "image19.png": "onboarding-4-boutons.png",     "image24.png": "onboarding-5-statuts.png",
    "image9.png":  "onboarding-6-restriction-ip.png", "image21.png": "remboursement-back-office.png",
 },
 "en": {
    "image6.gif":  "installation-module.gif",      "image5.png":  "page-configuration.png",
    "image3.png":  "mode-prelevement.png",         "image8.gif":  "paiement-paypal.gif",
    "image7.png":  "shortcut-page-produit.png",    "image10.png": "shortcut-page-panier.png",
    "image9.png":  "shortcut-inscription.png",     "image12.png": "avantages-paypal-bouton.png",
    "image11.png": "avantages-paypal-inscription.png", "image15.png": "bouton-dans-page-commande.png",
    "image13.png": "bouton-fin-de-page.png",       "image14.gif": "pay-later-activation.gif",
    "image16.gif": "pay-later-messages.gif",       "image17.gif": "personnalisation-shortcuts.gif",
    "image18.png": "onboarding-1-connexion.png",   "image20.png": "onboarding-1-code-compte.png",
    "image21.png": "onboarding-2-checkout.png",    "image22.png": "onboarding-3-pay-later.png",
    "image23.png": "onboarding-4-boutons.png",     "image24.png": "onboarding-5-statuts.png",
    "image1.png":  "onboarding-6-restriction-ip.png", "image2.png":  "remboursement-back-office.png",
 },
}
RENAME = RENOMMAGE[LANGUE]

LEGENDES = {
 "fr": {
    "installation-module.gif": "Installation du module depuis le back-office PrestaShop",
    "page-configuration.png": "Page de configuration du module PayPal",
    "mode-prelevement.png": "Réglage du mode de prélèvement",
    "paiement-paypal.gif": "Modes de paiement « En contexte » et « Rediriger »",
    "shortcut-page-produit.png": "Bouton PayPal Express Checkout sur une page produit",
    "shortcut-page-panier.png": "Bouton PayPal Express Checkout sur la page panier",
    "shortcut-inscription.png": "Bouton PayPal Express Checkout à l’étape d’inscription",
    "avantages-paypal-bouton.png": "Bouton affichant les avantages PayPal",
    "avantages-paypal-inscription.png": "Bouton par défaut à l’étape d’inscription",
    "bouton-dans-page-commande.png": "Bouton de paiement dans la page de commande",
    "bouton-fin-de-page.png": "Bouton de paiement à la fin de la page de commande",
    "pay-later-activation.gif": "Activation du bouton « Buy Now Pay Later »",
    "pay-later-messages.gif": "Configuration des messages « Buy Now Pay Later »",
    "personnalisation-shortcuts.gif": "Personnalisation des raccourcis PayPal Express Checkout",
    "onboarding-1-connexion.png": "Étape 1 — connexion au compte PayPal Professionnel",
    "onboarding-1-code-compte.png": "Étape 1 — code du compte de connexion",
    "onboarding-2-checkout.png": "Étape 2 — configuration du checkout",
    "onboarding-3-pay-later.png": "Étape 3 — paiement en plusieurs fois",
    "onboarding-4-boutons.png": "Étape 4 — personnalisation des boutons de raccourci",
    "onboarding-5-statuts.png": "Étape 5 — statuts de commande et webhooks",
    "onboarding-6-restriction-ip.png": "Étape 6 — restriction IP",
    "remboursement-back-office.png": "Écran de remboursement du back-office PrestaShop",
 },
 "en": {
    "installation-module.gif": "Installing the module from the PrestaShop back office",
    "page-configuration.png": "PayPal module configuration page",
    "mode-prelevement.png": "Payment collection mode setting",
    "paiement-paypal.gif": "‘In-context’ and ‘Redirect’ payment modes",
    "shortcut-page-produit.png": "PayPal Express Checkout button on a product page",
    "shortcut-page-panier.png": "PayPal Express Checkout button on the cart page",
    "shortcut-inscription.png": "PayPal Express Checkout button at the sign-up step",
    "avantages-paypal-bouton.png": "Button showing the PayPal benefits",
    "avantages-paypal-inscription.png": "Default button at the sign-up step",
    "bouton-dans-page-commande.png": "Payment button inside the checkout page",
    "bouton-fin-de-page.png": "Payment button at the bottom of the checkout page",
    "pay-later-activation.gif": "Enabling the ‘Buy Now Pay Later’ button",
    "pay-later-messages.gif": "Configuring the ‘Buy Now Pay Later’ messages",
    "personnalisation-shortcuts.gif": "Customizing the PayPal Express Checkout shortcuts",
    "onboarding-1-connexion.png": "Step 1 — signing in to the PayPal Business account",
    "onboarding-1-code-compte.png": "Step 1 — account connection code",
    "onboarding-2-checkout.png": "Step 2 — checkout configuration",
    "onboarding-3-pay-later.png": "Step 3 — installment payments",
    "onboarding-4-boutons.png": "Step 4 — customizing the shortcut buttons",
    "onboarding-5-statuts.png": "Step 5 — order statuses and webhooks",
    "onboarding-6-restriction-ip.png": "Step 6 — IP restriction",
    "remboursement-back-office.png": "Refund screen in the PrestaShop back office",
 },
}
LEGEND = LEGENDES[LANGUE]

# les captures sont propres à chaque langue, les GIF sont mutualisés
DOSSIER_IMG = IMG if LANGUE == "fr" else IMG / LANGUE
CHEMIN_IMG = (lambda nom: f"assets/img/{nom}" if nom in GIFS
              else f"assets/img/{'' if LANGUE == 'fr' else LANGUE + '/'}{nom}")

DOSSIER_IMG.mkdir(parents=True, exist_ok=True)
copiees = 0
for old, new in RENAME.items():
    if LANGUE != "fr" and new in GIFS:
        continue                      # GIF mutualisé avec le français
    shutil.copy(SRC / "images" / old, DOSSIER_IMG / new)
    copiees += 1

# ------------------------------------------------------- 4. routage des pages
# Même arborescence dans les deux langues : seuls les intitulés changent.
ROUTAGE = {
 "fr": ({
    "Installation du module PayPal Officiel":            "installation",
    "Naviguer dans votre page de configuration":         "navigation",
    "Configurations disponibles dans le module PayPal Officiel": "configuration",
    "On Boarding du module PayPal Officiel":             "onboarding",
    "Remboursement d’une transaction":                   "remboursements",
  }, {
    "Général":                                     "general",
    "Fonctionnalités spécifiques Allemagne":       "specificites-allemagne",
    "Fonctionnalités spécifiques USA":             "specificites-usa",
    "Fonctionnalités spécifiques Mexique / Brésil": "specificites-mexique-bresil",
    "Utilisation du module":                       "utilisation",
    "Pré-requis":                                  "prerequis",
    "Contact":                                     "contact",
  }),
 "en": ({
    "Installing the Official PayPal module":             "installation",
    "Navigating your configuration page":                "navigation",
    "Settings available in the Official PayPal module":  "configuration",
    "Onboarding for the Official PayPal module":         "onboarding",
    "Refunding a transaction":                           "remboursements",
  }, {
    "General":                                     "general",
    "Germany-specific features":                   "specificites-allemagne",
    "USA-specific features":                       "specificites-usa",
    "Mexico / Brazil-specific features":           "specificites-mexique-bresil",
    "Using the module":                            "utilisation",
    "Prerequisites":                               "prerequis",
    "Contact":                                     "contact",
  }),
}
_h2, _h1 = ROUTAGE[LANGUE]
ROUTE_H2 = {k: v + SUFFIXE + ".md" for k, v in _h2.items()}
ROUTE_H1 = {k: v + SUFFIXE + ".md" for k, v in _h1.items()}
def route(h1, h2):
    if h2 in ROUTE_H2: return ROUTE_H2[h2], h2, 2
    if h1 in ROUTE_H1: return ROUTE_H1[h1], h1, 1
    return None, None, None

# --------------------------- 5. carte des ancres Google Docs -> page#slug
ANCHORS = {}
h1 = h2 = None
for el in soup.body.find_all(["h1", "h2", "h3", "h4", "a"]):
    if el.name == "a":
        aid = el.get("id")
        if aid and h1:
            page, _, _ = route(h1, h2)
            if page:
                ANCHORS[aid] = (page, last_slug)
        continue
    t = el.get_text(" ", strip=True)
    if not t:
        continue
    if el.name == "h1": h1, h2 = t, None
    elif el.name == "h2": h2 = t
    last_slug = slugify(t, "-")
    page, root, _ = route(h1, h2)
    if page:
        ANCHORS[el.get("id")] = (page, "" if t == root else last_slug)

# ------------------------------------------------------------ 6. conversion
# Signets que Google Docs référence mais n'exporte pas : la cible est déduite
# du texte du lien. Tout autre lien interne non résolu est signalé en fin de run.
SIGNETS_PERDUS = {
    "fr": {"id.gv6ng4p90xo": ("configuration.md",    "mode-de-prelevement")},
    "en": {"id.czwqti8srtug": ("configuration.en.md", "payment-collection-mode")},
}[LANGUE]

def to_md(el, page):
    md = markdownify(str(el), heading_style="ATX", bullets="-", strip=["span"])

    def fix_img(m):
        name = RENAME.get(m.group(1).split("/")[-1])
        if not name:
            return ""
        return f'![{LEGEND.get(name, "")}]({CHEMIN_IMG(name)}){{ loading=lazy }}'   # 10 Mo de GIF
    md = re.sub(r'!\[[^\]]*\]\(([^)\s]+)[^)]*\)', fix_img, md)

    def fix_link(m):
        label, href = m.group(1), m.group(2)
        key = href.lstrip("#")
        if href.startswith("#"):
            cible = ANCHORS.get(key) or SIGNETS_PERDUS.get(key)
            if cible:
                tgt_page, slug = cible
                href = (f"#{slug}" if tgt_page == page else
                        f"{tgt_page}#{slug}" if slug else tgt_page)
        return f"[{label}]({href})"
    md = re.sub(r'\[([^\]]*)\]\((#[^)]+)\)', fix_link, md)

    for a, b in [("\\-", "-"), ("\\=", "="), ("\\[", "["), ("\\]", "]"), ("\\_", "_")]:
        md = md.replace(a, b)
    md = md.replace("Pay Later*", "Pay Later\\*")      # astérisque de note, pas une emphase
    md = re.sub(r'\*\*\*\*', '** **', md)
    md = re.sub(r'[ \t]+$', '', md, flags=re.M)
    return re.sub(r'\n{3,}', '\n\n', md).strip()

def fix_table(md):
    """Google Docs n'a pas de <thead> : la 1re ligne sort vide, la 2e contient les libellés."""
    lines = md.split("\n")
    if len(lines) >= 3 and re.fullmatch(r'\|(\s*\|)+', lines[0]) and set(lines[1].replace("|", "").strip()) <= set("- :"):
        lines = [lines[2], lines[1]] + lines[3:]
    out = []
    for i, line in enumerate(lines):
        if i == 1 or not line.startswith("|"):
            out.append(line); continue
        cells = [re.sub(r'(?<=[^\s|])\s+-\s+', '<br>- ', c) for c in line.split("|")]
        out.append("|".join(cells))
    return "\n".join(out)

PAGES, intro = {}, []
h1 = h2 = None
started = False
for el in soup.body.find_all(["h1", "h2", "h3", "h4", "p", "ol", "ul", "table"]):
    if el.name == "p" and el.find_parent(["li", "td", "ol", "ul", "table"]):
        continue
    if el.name in ("ol", "ul") and (el.find(["h1", "h2", "h3", "h4"]) or el.find_parent(["ol", "ul"])):
        continue
    if el.name.startswith("h"):
        t = el.get_text(" ", strip=True)
        if not t:
            continue
        lvl = int(el.name[1])
        if lvl == 1: h1, h2, started = t, None, True
        elif lvl == 2: h2 = t
        page, root, base = route(h1, h2)
        if not page:
            continue
        pg = PAGES.setdefault(page, {"title": root, "body": []})
        if t != root:
            pg["body"].append(f"{'#' * max(2, lvl - base + 1)} {t.replace('Pay Later*', 'Pay Later')}")
        continue
    if not el.get_text(strip=True) and not el.find("img"):
        continue
    if not started:
        intro.append(el)
        continue
    # Pas de filtre sur les liens #h. ici : le sommaire Google Docs précède le
    # premier titre et est déjà écarté plus haut. Ce filtre supprimait en
    # revanche des paragraphes de contenu qui renvoient à un autre chapitre.
    page, root, base = route(h1, h2)
    if not page:
        continue
    md = to_md(el, page)
    if el.name == "table":
        md = fix_table(md)
    if md and not re.fullmatch(r'Page\s*sur\s*', md):                          # pied de page Google Docs
        PAGES[page]["body"].append(md)

# --------------------------------------------------------- 7. page d'accueil
ACCUEIL = {
 "fr": {
    "intro": "Introduction",
    "titre": "Documentation utilisateur",
    "sous_titre": "**Module PayPal V.6.X pour PrestaShop V.1.7.X et supérieur**",
    "sommaire": "Sommaire",
    "pdf_titre": "Version PDF",
    "pdf_texte": "Une version imprimable de cette documentation est disponible ici :"
                 " [Télécharger le PDF](https://202ecommerce.github.io/paypal-doc/pdf/documentation-paypal.pdf)",
    "pages": [
      ("Général", "general"), ("Installation du module PayPal Officiel", "installation"),
      ("Naviguer dans votre page de configuration", "navigation"),
      ("Configurations disponibles dans le module PayPal Officiel", "configuration"),
      ("On Boarding du module PayPal Officiel", "onboarding"),
      ("Remboursement d’une transaction", "remboursements"),
      ("Fonctionnalités spécifiques Allemagne", "specificites-allemagne"),
      ("Fonctionnalités spécifiques USA", "specificites-usa"),
      ("Fonctionnalités spécifiques Mexique / Brésil", "specificites-mexique-bresil"),
      ("Utilisation du module", "utilisation"), ("Pré-requis", "prerequis"), ("Contact", "contact"),
    ],
 },
 "en": {
    "intro": "Introduction",
    "titre": "User documentation",
    "sous_titre": "**PayPal module V.6.X for PrestaShop V.1.7.X and above**",
    "sommaire": "Table of contents",
    "pdf_titre": "PDF version",
    "pdf_texte": "A printable version of this documentation is available here:"
                 " [Download the PDF](https://202ecommerce.github.io/paypal-doc/en/pdf/documentation-paypal.pdf)",
    "pages": [
      ("General", "general"), ("Installing the Official PayPal module", "installation"),
      ("Navigating your configuration page", "navigation"),
      ("Settings available in the Official PayPal module", "configuration"),
      ("Onboarding for the Official PayPal module", "onboarding"),
      ("Refunding a transaction", "remboursements"),
      ("Germany-specific features", "specificites-allemagne"),
      ("USA-specific features", "specificites-usa"),
      ("Mexico / Brazil-specific features", "specificites-mexique-bresil"),
      ("Using the module", "utilisation"), ("Prerequisites", "prerequis"), ("Contact", "contact"),
    ],
 },
}
A = ACCUEIL[LANGUE]
INDEX = "index" + SUFFIXE + ".md"
intro_md = [to_md(e, INDEX) for e in intro]
start = next(i for i, m in enumerate(intro_md) if m.strip("* ") == A["intro"])
PAGES[INDEX] = {"title": A["titre"], "body":
    [A["sous_titre"]]
    + [m for m in intro_md[start + 1:] if m]
    + ["## " + A["sommaire"],
       "\n".join(f"{i}. [{titre}]({slug + SUFFIXE}.md)"
                 for i, (titre, slug) in enumerate(A["pages"], 1)),
       f'!!! note "{A["pdf_titre"]}"\n    {A["pdf_texte"]}']}

# --------------------------------------- 7 bis. encarts « NB / A noter / Attention »
MARQUEURS = {
    "fr": {"nb": "note", "a noter": "note", "à noter": "note", "attention": "danger"},
    "en": {"nb": "note", "note": "note", "please note": "note", "warning": "danger"},
}
MARKERS = MARQUEURS[LANGUE]

def strip_em(s):
    s = re.sub(r'^\*{1,3}|\*{1,3}$', '', s.strip())
    return s.strip()

def is_italic(block):
    b = block.strip()
    return b.startswith("*") and b.endswith("*") and not b.startswith("**")

def to_admonitions(body):
    out, i = [], 0
    while i < len(body):
        block = body[i]
        head = strip_em(block)
        # marqueur seul sur son paragraphe, ou suivi de « : » — pas « A noter que ... »
        key = re.match(r'^(' + "|".join(sorted(MARKERS, key=len, reverse=True)) + r')\s*(:|$)', head, re.I)
        if not key or block.startswith("#"):
            out.append(block); i += 1; continue
        kind = MARKERS[key.group(1).lower()]
        rest = strip_em(head[key.end():].strip(" :"))
        title = key.group(1).rstrip()
        content = []
        if rest and len(rest) <= 80:                     # « NB : Délai de validité… » -> titre
            title = rest[0].upper() + rest[1:]
        elif rest:
            content = [rest]
        i += 1
        while i < len(body) and is_italic(body[i]) and not body[i].startswith("#"):
            content.append(strip_em(body[i])); i += 1
        # marqueur en gras seul : le paragraphe suivant lui appartient
        if not content and i < len(body):
            nxt = body[i]
            if not nxt.startswith(("#", "!", "|", "-", "*", "!!!")):
                content.append(nxt); i += 1
        if not content:
            out.append(block); continue
        lines = [f'!!! {kind} "{title}"']
        for c in content:
            lines += ["    " + l if l.strip() else "" for l in c.split("\n")]
            lines.append("")
        out.append("\n".join(lines).rstrip())
    return out

for page in PAGES.values():
    page["body"] = to_admonitions(page["body"])

# ------------------------------------------------------------- 8. écriture
# on n'efface que les pages de la langue en cours : les autres traductions restent
for f in DOCS.glob("*.md"):
    parties = f.name.split(".")
    langue_du_fichier = parties[1] if len(parties) == 3 else "fr"
    if langue_du_fichier == LANGUE:
        f.unlink()
FRONTMATTER = {}

for name, page in sorted(PAGES.items()):
    txt = FRONTMATTER.get(name, "") + "\n\n".join([f"# {page['title']}"] + [p for p in page["body"] if p.strip()])
    (DOCS / name).write_text(re.sub(r'\n{3,}', '\n\n', txt).rstrip() + "\n", encoding="utf-8")
    print(f"  {name:32} {len(txt):6} car.")
# contrôle sur les fichiers réellement écrits : un lien Google résiduel est un lien mort
orphelins = set()
for f in DOCS.glob("*" + SUFFIXE + ".md"):
    orphelins |= set(re.findall(r'\]\((#(?:id|h)\.[A-Za-z0-9]+)\)', f.read_text(encoding="utf-8")))
if orphelins:
    print("\n⚠ liens internes non résolus — à corriger dans SIGNETS_PERDUS :")
    for a in sorted(orphelins):
        print("   ", a)
print(f"\nlangue {LANGUE} : {copiees} images copiées dans {DOSSIER_IMG}, "
      f"{len(GIFS)} GIF mutualisés, {len(ANCHORS)} ancres mappées")
