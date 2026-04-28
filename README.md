# age-verification
Provides a secure age range API for self-declared OS-level age verification on Linux systems, as an optional standalone package.

License: [Unlicense](LICENSE).

## Motivation
This project seeks to address design flaws, project over-reaching and security issues.

The design of the [DBus proposal](https://lists.ubuntu.com/archives/ubuntu-devel/2026-March/043510.html) does not make sense. Only an API for reading the age range is needed. No need to add setting age or date of birth as part of the API. No need for taking a user parameter either. Applications should only care about the current user. The design assumes all age brackets will be the same. That is not a viable approach due to worldwide age category differences.

Implementing the API as part of xdg-desktop-portal does not make sense. It would only use usable by sandboxed enviroments (Flatpak, Snap), rather than all programs. The laws require all system programs to use it. The portal would require spesific backend DE/WM implmentation, while a universal DBus API would only need to be implemented in one place.

It is not the job of [init systems](https://en.wikipedia.org/wiki/Init) such as SystemD to ask for [DOB and other PII](https://itsfoss.com/news/systemd-age-verification/). SystemD is [already more than an init system](https://youtube.com/watch?v=07hfECzhzG0). Not all Linux systems depend on SystemD. There are alternative init systems. Choice in all aspects of the system allows for innovation.

The SystemD implementation stores date of birth in plain text. This is not how PII should be treated - it must be stored securely.

Even though the birth date field is optional in SystemD UserDB, it becomes mandatory in all implementations that integrate with it. There have been many PRs to deeply integrate with the SystemD implementation:
* [accountsservice](https://gitlab.freedesktop.org/accountsservice/accountsservice/-/merge_requests/176)
* [xdg-desktop-portal](https://github.com/flatpak/xdg-desktop-portal/pull/1922)
* [Calamares installer](https://codeberg.org/Calamares/calamares/pulls/2499)
* [Arch install](https://github.com/archlinux/archinstall/pull/4290)
* [Ubuntu Desktop Provision PR #1338](https://github.com/canonical/ubuntu-desktop-provision/pull/1338)
* [Ubuntu Desktop Provision PR #1339](https://github.com/canonical/ubuntu-desktop-provision/pull/1339)

The implementations assume all users live in a jurisdiction where OS-level verification applies. That is simply not the case.

## Scope
The only goal of this project is to provide a secure age range API for regions requiring OS-level age verification for Linux systems, as per OS-level age verification laws. There are inherent [privacy and security issues](#Privacy-and-security-issues) around handling age verification. This project will *never* implement forced-identification age verification age range API mandates because of them.

The following laws require an OS-level self-declared age verification age range API and *will be implemented*:
* [US - CA AB 1043 ("Age verification signals: software applications and online services")](https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=202520260AB1043) (enacted; activates on 2027-01-01)
* [US - CO SB 26-051 ("Age Attestation on Computing Devices")](https://leg.colorado.gov/bills/SB26-051)
* [US - IL SB 3977 ("Children's Social Media Safety Act")](https://ilga.gov/Legislation/BillStatus/FullText?GAID=18&DocNum=3977&DocTypeID=SB&LegId=167475&SessionID=114)

The following laws require an OS-level self-declared date of birth, but do not explicitly require any sort of age range API and *will not be implemented*:
* [US - H.R.8250 ("Parents Decide Act")](https://www.congress.gov/bill/119th-congress/house-bill/8250)

The following laws require an OS-level forced-identification age verification age range API and *will never be implemented*:
* [Brazil - Digital ECA](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/L15211.htm) (active since 2026-03-17)
* [US - IL HB 5511 ("Children's Social Media Safety Act")](https://www.ilga.gov/Legislation/BillStatus/FullText?GAID=18&DocNum=5511&DocTypeID=HB&LegId=0&SessionID=114)
* [US - MI HB 4429 ("Digital Age Assurance Act")](https://www.legislature.mi.gov/Bills/Bill?ObjectName=2025-HB-4429)
* [US - NY SB 2025-S8102A](https://www.nysenate.gov/legislation/bills/2025/S8102/amendment/A)
  
Currently both US - CA AB 1043 and US - CO SB 26-051 require the same age ranges. It is entierly possible that there will become multiple age brackets as new OS-level age verification laws get introduced or revised. This project is future-proofed against multiple age range brackets so that legacy data storage does not become an issue. This is done by asking users which jurisdiction applies. The use of IP address, precise location, time and date settings can be highly invasive and do not account for being in a different physical location. Dates of birth are being trusted to be correct, as should the region.

To ensure security, only root users should be able set age verification details of users. Additionally, details needed for age range must be encrypted and only readable in program memory when the age range API is called.

"Account setup" wizards can use this project by importing functions from [av_mgmt_core.py](src/av_mgnt_core.py); see [av_mgnt.py](src/av_mgnt.py) as an example of this. There a likely ways for non-Python programs to import the functions as well.

Root users can set age verification details of users after account creation using a terminal using the `av_mgmt` command.

## Privacy and security issues
This project recognises the [dangers](https://csa-scientist-open-letter.org/ageverif-Feb2026) of KYC, ID and biometric data collection:
* https://e-estonia.com/estonian-e-state-has-experienced-several-hacking-incidents-as-of-late-what-are-the-lessons-learned/
* https://www.biometricupdate.com/202208/id-me-finds-itself-accused-of-biometric-data-privacy-violation
* https://www.eff.org/deeplinks/2024/06/hack-age-verification-company-shows-privacy-danger-social-media-laws
* https://gbhackers.com/authorities-arrested-hacker-2/
* https://www.computerweekly.com/news/366622533/Government-faces-claims-of-serious-cyber-security-and-data-protection-problems-in-One-Login-digital-ID
* https://www.livemint.com/news/india/aadhaar-data-leak-massive-data-breach-exposes-815-million-indians-personal-information-on-dark-web-details-here-11698712793223.html
* https://www.idstrong.com/sentinel/tea-app-data-breach/
* https://reclaimthenet.org/age-verification-systems-france-privacy-risks-ai-forensics-report
* https://www.express.co.uk/news/politics/2113829/Starmer-ID-Card-security-threat
* https://www.bleepingcomputer.com/news/security/hackers-claim-discord-breach-exposed-data-of-55-million-users/
* https://cybernews.com/security/database-exposes-billions-records-linkedin-data/
* https://cyberinsider.com/verizon-owned-brand-total-wireless-suffers-breach-exposing-customer-data/
* https://cybernews.com/security/billions-chinese-records-data-leak/
* https://crypto.ro/en/analysis/sumsub-latest-security-breach-analyzed/
* https://www.openrightsgroup.org/press-releases/roblox-reddit-and-discord-users-compelled-to-use-biometric-id-system-backed-by-palantir-co-founder-peter-thiel/
* https://cybernews.com/security/global-data-leak-exposes-billion-records/
* https://www.malwarebytes.com/blog/news/2026/02/age-verification-vendor-persona-left-frontend-exposed
* https://reclaimthenet.org/yoti-gdpr-fine-age-verification
* https://cybernews.com/security/eu-age-verification-app-hack/
* https://cybernews.com/security/ants-hack-france-19-million-records-id-agency-breach/

Note that age ranges trasmitted via the API are still prone to misuse. Services have a legal duty to not misuse it, but there is not any real measure that would stop them from doing so. The only way to prevent this would be if such data was never sent in the first place. It would be significantly better if on-device parental controls were to be used instead, as this would prevent such data being transmitted in the first place.

## Compliance details
Compatibility for the following OS-level self-declared age verification age range API has been implemented:
* US - CA AB 1043
* US - CO SB 26-051

The age range API returns values in the following format:
* `>=a - <b` - eg `>=0 - <13`
* `>=a` - eg `>=18`
* `?` - Not required or unknown

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
* `av_mgnt_core.py` -> `/usr/lib/age-verification/av_mgnt_core.py`
* `dbus-AgeVerification.service` -> `/usr/share/dbus-1/system-services/com.example.AgeVerification.service`
* `dbus-AgeVerification.conf` -> `/usr/share/dbus-1/system.d/com.example.AgeVerification.conf`
* `dbus-AgeVerification.xml` -> `/usr/share/dbus-1/interfaces/com.example.AgeVerification.xml`
* `systemd-AgeVerification.service` -> `/usr/lib/systemd/system/com.example.AgeVerification.service`

## Registering age range API service
On systems using SystemD, users may need to run the following for the service to become active:
```
# systemctl daemon-reload
# systemctl enable com.example.AgeVerification.service
```

The dbus service may need to be restarted.
