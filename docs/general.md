# Général

## Êtes-vous client PayPal pour les Professionnels ?

**Vous n’êtes pas client PayPal ?**

- [Ouvrez un compte](https://www.paypal.com/fr/business) professionnel
- Téléchargez et installez le module PayPal et commencez à accepter des paiements simplifiés avec PayPal sur votre PrestaShop.

## Qu'est-ce que le module PayPal Officiel ?

**Grâce à PayPal, recevez vos paiements en ligne. Envoyez des factures. Consultez vos dernières ventes. Continuez à vous développer.**

**Grâce à PayPal, augmentez la conversion lors du paiement**

66 % d’augmentation du taux de conversion lors du paiement *(2)*

91 % des utilisateurs PayPal interrogés estiment que PayPal est un moyen de paiement facile *(3)*

*La conversion lors du paiement est mesurée à partir du moment où le client commence à payer*

**Grâce à PayPal, gagnez plus de clients fidèles**

19 % d'acheteurs réguliers en plus *(4)*

*2 - Étude Nielsen pour le compte de PayPal, Nielsen | Optimisé par le panel comportemental Médiamétrie de France (FR) après de 6 000 PME avec des transactions PC effectuées par 2 000 consommateurs entre juillet 2022 et juin 2023.*

3 - *Étude Nielsen pour le compte de PayPal, enquête attitudinale Nielsen en France (septembre 2023) menée auprès de 2 000 personnes ayant récemment effectué des achats (4 dernières semaines) auprès de PME, dont 1 000 transactions PayPal et 1 000 transactions non PayPal.*

*4 - Nielsen, commandé par PayPal. Panel de consommateurs Nielsen Media auprès de 7 200 PME sur sept marchés (États-Unis, Royaume-Uni, Allemagne, France, Italie, Espagne et Australie) avec 147 000 achats de 35 000 consommateurs sur ordinateur au cours d'une année (juillet 2020 à juin 2021, sauf États-Unis avec des données d'avril 2020 à mars 2021).*

**PayPal est toujours à vos côtés, même après la vente.**

**Les équipes PayPal sont  à votre disposition par téléphone (ou par chat en direct) si vous avez des questions.**

**Bénéficiez d'une expédition simplifiée, d'informations commerciales et bien plus avec PayPal pour les Professionnels.**

## Matrice des produits

En fonction de la localisation de votre compte marchand, différentes méthodes de paiement et fonctionnalités PayPal seront disponibles. Voir le tableau ci-dessous

Pour connaître les options de paiement disponible dans votre pays en tant que compte PayPal pour les Professionnel, rendez-vous sur cette page :

<https://developer.paypal.com/docs/payouts/standard/reference/country-feature/>

**Ci-dessous les options de paiement disponibles dans le module PayPal V6.X pour PrestaShop V1.7.X**

|  | Monde entier | Allemagne\* | Brésil et Mexique | USA |
| --- | --- | --- | --- | --- |
| **Méthodes de paiement** | - PayPal | - PayPal<br>- Carte de credit<br>- Pay Upon Invoice<br>- Paiement locaux<br>- SEPA | - PayPal<br>- Carte de crédit | - PayPal<br>- Venmo |
| **Fonctionnalités** | - Paiement en plusieurs fois via compte PayPal (États-Unis, Royaume-Uni, France, Italie, Espagne, Canada, Allemagne, Australie) | - Paiement en plusieurs fois via compte PayPal | - Paiement en plusieurs fois via compte PayPal ou carte de crédit<br>- Enregistrement de carte de crédit | - Paiement en plusieurs fois via compte PayPal<br>- Enregistrement de compte PayPal |
| **Intégration du paiement** | Advanced Checkout avec Javascript SDK pour 22 pays et 37 devises : <https://developer.paypal.com/docs/checkout/advanced/eligibility/> | | | |

**Les devises supportées par le module PayPal sont les suivantes**

<https://developer.paypal.com/api/rest/reference/currency-codes/>

*\* Si l’Allemagne est le pays par défaut de votre boutique PrestaShop, vous devez configurer vos options de paiement.*

## Création de comptes de test

L'Environnement de test PayPal est un environnement de test virtuel autonome qui imite l'environnement de production PayPal. Il s'agit d'un espace protégé dans lequel vous pouvez lancer et observer votre application traiter les demandes que vous adressez aux API de PayPal sans modifier les soldes des comptes PayPal en direct.

Afin d’installer le compte PayPal sur votre PrestaShop, nous conseillons de **créer tout d’abord des comptes de test** afin de pouvoir tester l’ensemble de la procédure de paiement avant de passer votre module en mode production.

Dans le module PayPal Officiel, vous avez la possibilité de configurer votre module en mode test (i.e. mode ‘Sandbox’) ou en mode production.

L’ensemble de la procédure de création de comptes de tests est expliquée ici :

<https://developer.paypal.com/tools/sandbox/accounts/>

Deux types de compte de test sont nécessaires afin de tester l’ensemble des paiements et des fonctionnalités :

- Un compte marchand pouvant recevoir des paiements, appelé ‘business sandbox account’ ;
- Un compte client pouvant passer des commandes, appelé ‘personal sandbox account’.

Les comptes de tests PayPal ont par défaut l’ensemble des fonctionnalités activées.

Les comptes de production ont par défaut le paiement PayPal activé mais certains autres méthodes de paiement ou fonctionnalités peuvent nécessiter une activation sur votre compte marchand PayPal de production (paiement locaux, enregistrement de carte).

Cette documentation indiquera pour chaque méthode de paiement et pour chaque fonctionnalité si une activation est nécessaire.

Une fois vos comptes de test créés vous pouvez installer le module PayPal Officiel sur votre PrestaShop.
