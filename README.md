# age-verification
Provides a secure age range API for self-declared ages on Linux systems as an optional standalone program.

It is not the job of init systems such as SystemD to force asking for DOB, regardless of jusristiction, and then store PII in plain text.

"Account setup" wizards can store encrypted age verification details in the expected encrypted format in expected file locations. See `av_mgmt.sh` as a reference implementation.

This is a proof-of-concept. It has not been fully tested.

## Scope
Only age-ranges for self-declared age verification methods will be considered.

This project recognises the dangers of [forced-identification](https://consumerrights.wiki/w/Forced_identification) methods:
* https://www.idstrong.com/sentinel/tea-app-data-breach/
* https://reclaimthenet.org/age-verification-systems-france-privacy-risks-ai-forensics-report
* https://www.thecanary.co/uk/news/2025/10/10/discord-data-leak/
* https://www.bleepingcomputer.com/news/security/hackers-claim-discord-breach-exposed-data-of-55-million-users/
* https://www.malwarebytes.com/blog/news/2026/02/age-verification-vendor-persona-left-frontend-exposed
* https://www.openrightsgroup.org/press-releases/roblox-reddit-and-discord-users-compelled-to-use-biometric-id-system-backed-by-palantir-co-founder-peter-thiel/
* https://www.openrightsgroup.org/press-releases/13-year-olds-could-be-compelled-to-use-unregulated-age-verification/
* https://reclaimthenet.org/yoti-gdpr-fine-age-verification

As such, age ranges *exclusive* to forced-identification methods will never be included.

Note that age ranges trasmitted via the API is still prone to misuse. It would be significantly better if parental controls were to be used instead.

### Inside scope
Below is an incomplete list of age ranges that are supported.

Laws marked with an asterix require forced-identification. Users with root access are technically able to bypass forced-identification checks and redefine age verification details of all users.
#### Common age range 0
* `>=0 - <13`
* `>=13 - <16`
* `>=16 - <18`
* `>=18`

Includes:
* [US - CA AB-1043](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202520260AB1043)
* [US - CO SB 26-051](https://leg.colorado.gov/bill_files/112795/download)
* [US - MI HB 1046](https://legislature.mi.gov/documents/2025-2026/billintroduced/House/pdf/2025-HIB-4429.pdf) *, [US - MI SB 191](https://www.legislature.mi.gov/documents/2025-2026/billintroduced/Senate/pdf/2025-SIB-0191.pdf) *
* [US - NY SB 2025-S8240](https://legislation.nysenate.gov/pdf/bills/2025/S8240) *
### Outside of scope
Examples of age ranges outside of scope include:
* [Brazil - Digital ECA](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/L15211.htm)

# Packaging
## Dependencies
* bash
* coreutils
* python
* python-dateutil
* python-dbus-next
* gawk (optional - manage users' DOB as root)
* kdialog (optional - DOB decryption dialogs for KDE)
* yad (optional - DOB decryption dialogs for YAD)
* zenity (optional - DOB decryption dialogs for GTK)

## Interal file storage locations
* `age-range-api.py` -> `/usr/lib/age-verification/age-range-api.py`
* `av_mgmt.sh` -> `/usr/sbin/age-verification/av_mgmt.sh`
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
