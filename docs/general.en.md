# General

## Are you a PayPal Business customer?

**You are already a PayPal customer:** Go to [chapter 2](#what-is-the-official-paypal-module)

**Not a PayPal customer yet?**

- [Open a business account](https://www.paypal.com/fr/business)
- Download and install the PayPal module and start accepting simplified payments with PayPal on your PrestaShop store.

## What is the Official PayPal module?

**With PayPal, receive your payments online. Send invoices. Review your latest sales. Keep growing.**

**With PayPal, increase conversion at checkout**

66% increase in the conversion rate at checkout *(2)*

91% of the PayPal users surveyed consider PayPal an easy payment method *(3)*

*Conversion at checkout is measured from the moment the customer starts paying*

**With PayPal, win more loyal customers**

19% more repeat buyers *(4)*

*2 - Nielsen study on behalf of PayPal, Nielsen | Powered by the Médiamétrie behavioural panel in France (FR) covering nearly 6,000 SMEs with PC transactions made by 2,000 consumers between July 2022 and June 2023.*

3 - *Nielsen study on behalf of PayPal, Nielsen attitudinal survey in France (September 2023) conducted among 2,000 people who had recently made purchases (in the last 4 weeks) from SMEs, including 1,000 PayPal transactions and 1,000 non-PayPal transactions.*

*4 - Nielsen, commissioned by PayPal. Nielsen Media consumer panel covering 7,200 SMEs in seven markets (United States, United Kingdom, Germany, France, Italy, Spain and Australia) with 147,000 purchases by 35,000 consumers on desktop over one year (July 2020 to June 2021, except the United States with data from April 2020 to March 2021).*

**PayPal is always by your side, even after the sale.**

**The PayPal teams are available by phone (or live chat) if you have any questions.**

**Benefit from simplified shipping, business insights and much more with PayPal for Business.**

## Product matrix

Depending on the location of your merchant account, different PayPal payment methods and features will be available. See the table below

To find out which payment options are available in your country as a PayPal Business account holder, go to this page:

<https://developer.paypal.com/docs/payouts/standard/reference/country-feature/>

**Below are the payment options available in the PayPal module V6.X for PrestaShop V1.7.X**

|  | Worldwide | Germany\* | Brazil and Mexico | USA |
| --- | --- | --- | --- | --- |
| **Payment methods** | - PayPal | - PayPal<br>- Credit card<br>- Pay Upon Invoice<br>- Local payment methods<br>- SEPA | - PayPal<br>- Credit card | - PayPal<br>- Venmo |
| **Features** | - Installment payments via a PayPal account (United States, United Kingdom, France, Italy, Spain, Canada, Germany, Australia) | - Installment payments via a PayPal account | - Installment payments via a PayPal account or credit card<br>- Credit card vaulting | - Installment payments via a PayPal account<br>- PayPal account vaulting |
| **Payment integration** | Advanced Checkout with the JavaScript SDK for 22 countries and 37 currencies: <https://developer.paypal.com/docs/checkout/advanced/eligibility/> | | | |

**The currencies supported by the PayPal module are the following**

<https://developer.paypal.com/api/rest/reference/currency-codes/>

*\* If Germany is the default country of your PrestaShop store, you must configure your payment options.*

## Creating test accounts

The PayPal test environment is a self-contained virtual testing environment that mimics the PayPal production environment. It is a protected space in which you can run and watch your application process the requests you send to the PayPal APIs without affecting the balances of live PayPal accounts.

In order to install the PayPal account on your PrestaShop store, we recommend that you **first create test accounts** so that you can test the entire payment process before switching your module to production mode.

In the Official PayPal module, you can configure your module in test mode (i.e. ‘Sandbox’ mode) or in production mode.

The full test account creation procedure is explained here:

<https://developer.paypal.com/tools/sandbox/accounts/>

Two types of test account are required in order to test all payments and features:

- A merchant account able to receive payments, called a ‘business sandbox account’;
- A customer account able to place orders, called a ‘personal sandbox account’.

By default, PayPal test accounts have all features enabled.

Production accounts have PayPal payment enabled by default, but some other payment methods or features may require activation on your PayPal production merchant account (local payment methods, card vaulting).

For each payment method and each feature, this documentation will indicate whether activation is required.

Once your test accounts have been created, you can install the Official PayPal module on your PrestaShop store.
