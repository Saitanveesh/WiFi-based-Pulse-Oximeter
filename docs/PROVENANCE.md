# Source provenance and third-party rights

This repository was first published with a short tutorial-style description, an extensionless Arduino sketch, and a circuit image. The old text and firmware closely match an earlier third-party tutorial:

- [How To Electronics — MAX30100 Pulse Oximeter with ESP8266](https://how2electronics.com/MAX30100-PULSE-OXIMETER-WITH-ESP8266/)
- [How To Electronics video tutorial](https://www.youtube.com/watch?v=_CWLcbRIWFc)
- [MAX30100 library by oxullo](https://github.com/oxullo/Arduino-MAX30100), whose upstream library code carries its own license
- [Blynk library and example project](https://github.com/blynkkk/blynk-library), also separately licensed

The tutorial is acknowledged as the source of the prior example's approach and closely matching code/text. Authorship and reuse permission for the image `Circuit Diagram .jpeg` have **not** been verified. Its inclusion here does not transfer ownership or grant permission to redistribute it elsewhere.

The current `firmware/PulseOximeter/PulseOximeter.ino` was rewritten for clearer organization, explicit local credential configuration, and better behavior when the cloud is unavailable. Those changes have not been compiled on hardware in this repository update. Using the same sensor and vendor APIs is not a claim to originality of the underlying technique.

**Rights boundary:** The maintainer can assert rights only in material that the maintainer actually authored and owns. Third-party tutorials, artwork, libraries, and prior contributions remain subject to their own terms. A new repository notice does not rewrite the legal status of earlier commits.

Before distributing this repository as a product or adopting a permissive or copyleft license, check the origins and permissions of the firmware baseline and circuit image. Consider replacing the historical image with a new verified diagram when the hardware is available for inspection.
