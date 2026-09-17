"""Traduit la couverture du PDF selon la langue de la passe de build.

mkdocs-static-i18n relance un build complet par langue : mkdocs-with-pdf produit
donc bien un PDF par langue, chacun ne contenant que ses propres pages. Mais la
configuration du plugin est globale — sans ce hook, le PDF anglais sort avec une
couverture et un sommaire en français.

Les surcharges par langue d'i18n ne portent que sur quelques clés du site
(site_name, copyright, theme…) et pas sur les options des autres plugins, d'où
ce passage par un hook. `on_env` est le premier événement où la langue de la
passe est connue, et il précède l'écriture du PDF.

On écrit dans l'objet `Options` du plugin et non dans sa configuration : le
plugin fige ses options au moment d'`on_config`, c'est-à-dire avant ce hook.
Modifier `plugin.config` ne prendrait effet qu'à la passe suivante — soit la
mauvaise langue.
"""

COUVERTURE = {
    "fr": {
        "cover_title": "Documentation utilisateur",
        "cover_subtitle": "Module PayPal Officiel V6.X — PrestaShop V1.7.X et supérieur",
        "toc_title": "Sommaire",
    },
    "en": {
        "cover_title": "User documentation",
        "cover_subtitle": "Official PayPal module V6.X — PrestaShop V1.7.X and above",
        "toc_title": "Table of contents",
    },
}


def on_env(env, config, files, **kwargs):
    plugin = config["plugins"].get("with-pdf")
    if plugin is None:
        return env                      # configuration de développement : pas d'export PDF
    textes = COUVERTURE.get(config["theme"]["language"])
    options = getattr(plugin, "_options", None)
    if textes and options is not None:
        options._cover_title = textes["cover_title"]
        options._cover_subtitle = textes["cover_subtitle"]
        options.toc_title = textes["toc_title"]
    return env
