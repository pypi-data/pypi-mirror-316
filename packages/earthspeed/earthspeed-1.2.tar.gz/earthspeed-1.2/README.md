# earthspeed

By Benjamin Lillard

**For finding the instantaneous velocity of the Earth with respect to the galactic dark matter halo** 

### DESCRIPTION: ##########################################################

This package tracks the effective DM wind velocity for a lab on Earth, including the annual effects from the Earth's orbit around the Sun. 
The parameters for the Earth-Sun system are taken from Lewin & Smith (1996), but with the corrected elliptical terms of arXiv:1312.1355. Updated values for the Local Standard of Rest (LSR) are taken from arXiv:2105.00599.
This notebook uses the astropy package to convert galactic coordinates to ICRS, so that the location of the DM wind source on the sky can be expressed using right ascension (RA) and declination. 
Given a location on Earth, the package can also find the altitude and azimuth angles of the DM wind at any time of day.

A Jupyter notebook "GalacticOrientations" demonstrates how to use the package with a few examples. The primary function is vEt(obstime), which returns the Earth velocity relative to the galactic center in Cartesian coordinates, at an observation date and time "obstime" provided in the format of the datetime package.


**References:**

J. D. Lewin and P. F. Smith, “Review of mathematics, numerical factors, and corrections for dark matter experiments based on elastic nuclear recoil,” Astropart. Phys. 6 (1996) 87–112.

C. McCabe, "The Earth’s velocity for direct detection experiments," JCAP 02, 027 (2014), arXiv:1312.1355 [astro-ph.CO].

D. Baxter et al., “Recommended conventions for reporting results from direct dark matter searches,” Eur. Phys. J. C 81 no. 10, (2021) 907, arXiv:2105.00599 [hep-ex].
