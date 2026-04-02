# age-verification
Provides a secure age range API for self-declared ages on Linux systems as an optional standalone program. Non self-declared will never be included.

It is not the job of init systems such as SystemD to force asking for DOB, regardelss of jusristiction, and then store PII in plain text.

"Account setup" wizards can store encrypted dates of birth in the expected encrypted format in expected file locations. See `dob_mgmt.sh` as a reference implementation.

This is a proof-of-concept. It has not been fully tested.

# Dependencies
* bash
* coreutils
* python
* python-dateutil
* python-dbus-next
* gawk (optional - manage users' DOB as root)
* kdialog (optional - DOB decryption dialogs for KDE)
* yad (optional - DOB decryption dialogs for YAD)
* zenity (optional - DOB decryption dialogs for GTK)

# Interal file storage locations
* `age-range-api.py` -> `/usr/lib/age-verification/age-range-api.py`
* `dbus-AgeVerification.service` -> `/usr/share/dbus-1/system-services/com.example.AgeVerification.service`
* `dbus-AgeVerification.conf` -> `/usr/share/dbus-1/system.d/com.example.AgeVerification.conf`
* `dbus-AgeVerification.xml` -> `/usr/share/dbus-1/interfaces/com.example.AgeVerification.xml`
* `systemd-AgeVerification.service` -> `/usr/lib/systemd/system/com.example.AgeVerification.service`
* `dob_mgmt.sh` -> `/usr/lib/age-verification/dob_mgmt.sh`
* `utils.py` -> `/usr/lib/age-verification/utils.py`

# Registering age range API service
On systems using SystemD, users may need to run the following for the service to become active:
```
# $ sudo systemctl daemon-reload
# $ sudo systemctl enable com.example.AgeVerification.service
```
