# Pré-requis

## TLS 1.2 et cURL 1.0.1c

Le Payment Card Industry (PCI) a exigé que les premières versions de TLS soient retirées du service. Toutes les organisations qui traitent des informations relatives aux cartes de crédit sont tenues de se conformer à cette norme.
Dans le cadre de cette obligation, PayPal a mis à jour ses services pour exiger TLS 1.2 pour toutes les connexions HTTPS.
Les connexions à l'environnement sandbox utilisent uniquement TLS 1.2.

Vérifiez la version de la bibliothèque de sécurité sous-jacente de votre URL. Si vous utilisez les bibliothèques OpenSSL, veuillez les mettre à jour vers la version 1.0.1c au minimum. Si vous utilisez cURL, assurez-vous que sa version est supérieure ou égale à 7.34.0.
Veuillez contacter votre hébergeur pour plus de détails.

## Version de PHP

Version PHP minimale : PHP 7.2

## Paramètres d’arrondi

Dans certains cas sur PrestaShop, les paramètres d'arrondi ne sont pas entièrement compatibles avec les exigences de PayPal.
Afin d'éviter que certaines transactions n’échouent, veuillez modifier le mode d'arrondi de PrestaShop dans CONFIGURER > Paramètres de la boutique > Paramètres généraux :

- Règle d'arrondi : “Arrondir vers l’infini quand valeur à mi-chemin (recommandé)”
- Type d'arrondi : “Arrondir pour chaque ligne”
- Nombre de décimales : “2”

## Format de checkout : ‘One Page Checkout’

Le module PayPal Officiel est conçu pour fonctionner selon les règles natives de PrestaShop.
Dans le panier natif de PrestaShop, un client arrivant au paiement est nécessairement connu : email, nom, prénom, adresse de livraison, de facturation, etc.
Dans le cas de l’utilisation de modules de ‘One Page Checkout’, il peut arriver que le module PayPal ne puisse pas fonctionner car il ne reçoit pas les informations dont il a besoin pour poursuivre la transaction.
Si vous repérez un module de ‘One Page Checkout’ non compatible avec le module PayPal Officiel [n’hésitez pas à nous contacter](https://addons.prestashop.com/fr/contactez-nous?id_product=1748). Si de nombreux marchands utilisent le même module, un effort peut être fait afin de contacter les éditeurs de modules de ‘One Page Checkout’ pour rendre les modules compatibles.
