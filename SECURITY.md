# Security and responsible use

## Previously exposed credentials

An earlier Git commit contained a hardcoded Blynk device token and Wi-Fi configuration. The current version uses `secrets.h`, which is excluded from Git.

**Removing values from the latest commit does not remove them from Git history.** If any of the earlier values were valid, revoke/regenerate the Blynk device token and change the Wi-Fi password. Assume the earlier values were disclosed publicly. Do not paste replacements into issues or commits.

History rewriting would require coordination with existing clones and forks; rotation is the first containment step.

## Network and health data

Blynk transmits sensor readings to a third-party cloud service. Use test/demo readings only unless you have obtained informed consent and reviewed the service's privacy, security, and retention policies. This hobby prototype is not a medical device and should never drive alerts or treatment.

For security concerns, contact [the repository maintainer](https://github.com/Saitanveesh) privately; do not post live tokens, passwords, or personal physiological data in public issues.
