# age-verification
Provides a secure age range API for self-declared ages on Linux systems as an optional standalone program.

This is a proof-of-concept. It has not been fully tested.

## Motivation
It is not the job of [init systems](https://en.wikipedia.org/wiki/Init) such as SystemD to force asking for [DOB and other PII](https://itsfoss.com/news/systemd-age-verification/), regardless of jusristiction (where OS-level age verification may not even be required), then store it in plain text. This project seeks to address [project over-reaching](https://youtube.com/watch?v=07hfECzhzG0) and security issues.

## Scope
The only goal of this project is to provide a secure age range API for regions requring self-declared age verification. There are inherent privacy and security issues around handeling age verification.

Only age-ranges for self-declared age verification methods will be considered. There is no need to add extra complexity for otherwise unused age ranges.

It is entierly possible that there will become multiple age brackets as new OS-level age verification laws get introduced or revised. The project should be future-proofed against multiple age range requirements so that legacy configurations do not become an issue.

To ensure security, only root users should be able set age verification details of users. Additionally, details needed for age range must be encrypted at rest. Sensative details like DOB should not be passed as a function parameter in plain text as that allows it to be visible in the stack trace, undermining data security.

There will not be a direct way for "account setup" wizards to use this project as it would add extra complexity. There is not a way to ensure the program is connected to a TTY, which would be needed to get a password to decrypt the encrypted DOB function parameter. "Account setup" wizards are able store encrypted age verification details in the expected encrypted format in expected file locations.

## Privacy and security issues
This project recognises the dangers of [forced-identification](https://consumerrights.wiki/w/Forced_identification) methods:
* https://www.idstrong.com/sentinel/tea-app-data-breach/
* https://reclaimthenet.org/age-verification-systems-france-privacy-risks-ai-forensics-report
* https://www.thecanary.co/uk/news/2025/10/10/discord-data-leak/
* https://www.bleepingcomputer.com/news/security/hackers-claim-discord-breach-exposed-data-of-55-million-users/
* https://www.malwarebytes.com/blog/news/2026/02/age-verification-vendor-persona-left-frontend-exposed
* https://www.openrightsgroup.org/press-releases/roblox-reddit-and-discord-users-compelled-to-use-biometric-id-system-backed-by-palantir-co-founder-peter-thiel/
* https://www.openrightsgroup.org/press-releases/13-year-olds-could-be-compelled-to-use-unregulated-age-verification/
* https://reclaimthenet.org/yoti-gdpr-fine-age-verification

Note that age ranges trasmitted via the API is still prone to misuse. It would be significantly better if parental controls were to be used instead, as this would prevent software from having access to the age, DOB or age-range of users.

## Compliance details
Laws marked with an asterix require forced-identification. This project will never use forced-identification methods because of privacy and security issues outlined above.

This project uses common age range numbers to identify which juristiction should be appled. IP address, time and date settings, precise location, etc. are not used to obtain location as they are both highly invasive and do not account for traveling to differect physical locations.

### Supported age ranges
#### Common age range 0
* `>=0 - <13`
* `>=13 - <16`
* `>=16 - <18`
* `>=18`

Includes:
* [US - CA AB-1043](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202520260AB1043)
* [US - CO SB 26-051](https://leg.colorado.gov/bill_files/112795/download)
* [US - IL HB 5511](https://ilga.gov/documents/legislation/104/HB/PDF/10400HB5511lv.pdf) *
* [US - MI HB 1046](https://legislature.mi.gov/documents/2025-2026/billintroduced/House/pdf/2025-HIB-4429.pdf) *, [US - MI SB 191](https://www.legislature.mi.gov/documents/2025-2026/billintroduced/Senate/pdf/2025-SIB-0191.pdf) *
* [US - NY SB 2025-S8240](https://legislation.nysenate.gov/pdf/bills/2025/S8240) *

### Unsupported age ranges
Examples of age ranges that are not supported include:
* [Brazil - Digital ECA](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/L15211.htm) * (no spesific age range defined)

# Packaging
## Dependencies
* coreutils
* python
* python-dateutil
* python-dbus-next
* kdialog (optional - DOB decryption dialogs for KDE)
* yad (optional - DOB decryption dialogs for YAD)
* zenity (optional - DOB decryption dialogs for GTK)

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
