# Fonctionnalités spécifiques par pays

Certaines méthodes de paiement et fonctionnalités ne sont disponibles que dans certains pays, selon la localisation du compte marchand PayPal.

!!! warning "Pré-requis commun"
    Les **paramètres de localisation de la boutique PrestaShop** doivent être réglés sur le pays concerné. Dans le cas contraire, les options de paiement spécifiques à ce pays ne seront pas proposées.

## Allemagne

Fonctionnalités ajoutées à partir de la **version 5.7.0** du module :

- Nouvelle version de PayPal Plus : PayPal Checkout
- PayPal Checkout — extension Pay Upon Invoice (PUI)
- PayPal Checkout — extension ACDC
- PayPal Checkout — extension APM
- PayPal Checkout — extension PayPal Wallet
- PayPal Checkout — envoi du numéro de suivi sur les commandes PUI

### Conditions de mise en production

- S'assurer que la validation de l'email et du KYB a été obtenue ;
- Effectuer un test de paiement en direct (avec un produit à 0,01 €) sur **chacun** des modes de paiement, afin de vérifier que tous les paiements fonctionnent.

## États-Unis

- Paiement Venmo
- Vaulting (enregistrement) du compte PayPal

## Mexique et Brésil

- Vaulting du compte PayPal et de la carte bancaire
- PayPal Plus
- Paiement en plusieurs fois
