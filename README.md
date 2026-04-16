# age-verification
Provides a secure age range API for self-declared OS-level age verification on Linux systems, as an optional standalone package.

This is a proof-of-concept. It has not been fully tested.

## Motivation
It is not the job of [init systems](https://en.wikipedia.org/wiki/Init) such as SystemD to force asking for [DOB and other PII](https://itsfoss.com/news/systemd-age-verification/), regardless of jusristiction (where OS-level age verification may not even be required), then store it in plain text. This project seeks to address [project over-reaching](https://youtube.com/watch?v=07hfECzhzG0) and security issues.

## Scope
The only goal of this project is to provide a secure age range API for regions requring OS-level age verification for Linux systems, as per OS-level age verification laws. There are inherent privacy and security issues around handeling age verification.

The following laws require an OS-level self-declared age verification age range API and *will be implemented*:
* [US - CA AB-1043](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202520260AB1043) (active)
* [US - CO SB 26-051](https://leg.colorado.gov/bill_files/112795/download)

The following laws require an OS-level self-declared data of birth, but do not explicitly require any sort of age range API and *will not be implemented*:
* [US - H.R.8250 ("Parents Decide Act")](https://www.congress.gov/119/bills/hr8250/BILLS-119hr8250ih.pdf)

The following laws require an OS-level forced-identification age verification age range API and *will never be implemented* due to [past forced-identification incidents](#Privacy-and-security-issues):
* [Brazil - Digital ECA](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/L15211.htm) (active)
* [US - IL HB 5511](https://ilga.gov/documents/legislation/104/HB/PDF/10400HB5511lv.pdf)
* [US - MI HB 1046](https://legislature.mi.gov/documents/2025-2026/billintroduced/House/pdf/2025-HIB-4429.pdf), [US - MI SB 191](https://www.legislature.mi.gov/documents/2025-2026/billintroduced/Senate/pdf/2025-SIB-0191.pdf)
* [US - NY SB 2025-S8240](https://legislation.nysenate.gov/pdf/bills/2025/S8240)
  
Currently both US - CA AB-1043 and US - CO SB 26-051 require the same age ranges. It is entierly possible that there will become multiple age brackets as new OS-level age verification laws get introduced or revised. This project is future-proofed against multiple age range brackets so that legacy data storage does not become an issue. This is done by asking users which juristiction applies. The use of IP address, precise location, time and date settings can be highly invasive and do not account for being in a different physical location. Dates of birth are being trusted to be correct, as should the region.

To ensure security, only root users should be able set age verification details of users. Additionally, details needed for age range must be encrypted at rest. Sensative details like DOB should not be passed as a function parameter in plain text as that allows it to be visible in the stack trace, undermining data security.

There will not be a direct way for "account setup" wizards to use this project as it would add extra complexity. There is not a way to ensure the program is connected to a TTY, which would be needed to get a password to decrypt the encrypted DOB function parameter. "Account setup" wizards are able store encrypted age verification details in the expected encrypted format in expected file locations.

## Privacy and security issues
This project recognises the dangers of [forced-identification](https://consumerrights.wiki/w/Forced_identification) methods:
* https://www.biometricupdate.com/202208/id-me-finds-itself-accused-of-biometric-data-privacy-violation
* https://www.eff.org/deeplinks/2024/06/hack-age-verification-company-shows-privacy-danger-social-media-laws
* https://www.idstrong.com/sentinel/tea-app-data-breach/
* https://reclaimthenet.org/age-verification-systems-france-privacy-risks-ai-forensics-report
* https://www.thecanary.co/uk/news/2025/10/10/discord-data-leak/
* https://www.bleepingcomputer.com/news/security/hackers-claim-discord-breach-exposed-data-of-55-million-users/
* https://cyberinsider.com/verizon-owned-brand-total-wireless-suffers-breach-exposing-customer-data/
* https://crypto.ro/en/analysis/sumsub-latest-security-breach-analyzed/
* https://www.openrightsgroup.org/press-releases/roblox-reddit-and-discord-users-compelled-to-use-biometric-id-system-backed-by-palantir-co-founder-peter-thiel/
* https://cybernews.com/security/global-data-leak-exposes-billion-records/
* https://www.malwarebytes.com/blog/news/2026/02/age-verification-vendor-persona-left-frontend-exposed
* https://reclaimthenet.org/yoti-gdpr-fine-age-verification
* https://www.openrightsgroup.org/press-releases/13-year-olds-could-be-compelled-to-use-unregulated-age-verification/

Note that age ranges trasmitted via the API are still prone to misuse. Services have a legal duty to not misuse it, but there is not any real measure that would stop them from doing so. The only way to prevent this would be if such data was never sent in the first place. It would be significantly better if on-device parental controls were to be used instead, as this would prevent such data being transmitted in the first place.

## Compliance details
Compatibility for the following OS-level self-declared age verification age range API has been implemented:
* US - CA AB-1043
* US - CO SB 26-051

The age range API returns values in the following format:
* `>=a - <b` - eg `>=0 - <13`
* `>=a` - eg `>=18`
* `?` - denotes an unknown age range

# Packaging
## Dependencies
* coreutils
* python
* python-dateutil
* python-dbus-next
* kdialog (optional - decryption dialogs for KDE)
* yad (optional - decryption dialogs for YAD)
* zenity (optional - decryption dialogs for GTK)

## Interal file storage locations
* `age-range-api.py` -> `/usr/lib/age-verification/age-range-api.py`
* `av_mgmt.py` -> `/usr/sbin/age-verification/av_mgmt.py`
* `dbus-AgeVerification.service` -> `/usr/share/dbus-1/system-services/com.example.AgeVerification.service`
* `dbus-AgeVerification.conf` -> `/usr/share/dbus-1/system.d/com.example.AgeVerification.conf`
* `dbus-AgeVerification.xml` -> `/usr/share/dbus-1/interfaces/com.example.AgeVerification.xml`
* `systemd-AgeVerification.service` -> `/usr/lib/systemd/system/com.example.AgeVerification.service`
* `utils.py` -> `/usr/lib/age-verification/utils.py`

## Registering age range API service
On systems using SystemD, users may need to run the following for the service to become active:
```
# systemctl daemon-reload
# systemctl enable com.example.AgeVerification.service
```
