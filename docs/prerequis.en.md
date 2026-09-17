# Prerequisites

## TLS 1.2 and cURL 1.0.1c

The Payment Card Industry (PCI) has required the earliest versions of TLS to be retired from service. All organizations that handle credit card information are required to comply with this standard.

As part of this obligation, PayPal has updated its services to require TLS 1.2 for all HTTPS connections.

Connections to the sandbox environment use TLS 1.2 only.

Check the version of the underlying security library of your URL. If you use the OpenSSL libraries, please update them to version 1.0.1c as a minimum. If you use cURL, make sure its version is 7.34.0 or higher.

Please contact your hosting provider for further details.

## PHP version

Minimum PHP version: PHP 7.2

## Rounding settings

In some cases on PrestaShop, the rounding settings are not fully compatible with PayPal's requirements.

To prevent some transactions from failing, please change the PrestaShop rounding mode in CONFIGURE > Shop Parameters > General:

- Round type: “Round up away from zero, when it is half way there (recommended)”
- Rounding mode: “Round on each item”
- Number of decimals: “2”

## Checkout format: ‘One Page Checkout’

The Official PayPal module is designed to work according to the native PrestaShop rules.

In the native PrestaShop cart, a customer reaching the payment step is necessarily known: email, last name, first name, shipping address, billing address, etc.

When ‘One Page Checkout’ modules are used, the PayPal module may not be able to work because it does not receive the information it needs to continue the transaction.

If you come across a ‘One Page Checkout’ module that is not compatible with the Official PayPal module, [please do not hesitate to contact us](https://addons.prestashop.com/fr/contactez-nous?id_product=1748). If many merchants use the same module, an effort may be made to contact the publishers of ‘One Page Checkout’ modules in order to make the modules compatible.
