browser-shots-tool
==================
This tool is the part of Internet Memory in the SCAPE project. 
Browser-shots-tool allows to take screenshots of a list of URLs with different browsers using an automatic navigation.

This work is developed in a Debian Squeeze server (64 bits) with Python and uses other tools, whose Selenium and marcalizer, and that make  our project depending on other packages.
- Versions :
 - Python 2.6 at least
 - Selenium 2.24.1
 - Marcalizer 0.9
 - Firefox 3.6

- Dependencies :
 - Selenium driver of browser (for python) : provided by Selenium in its official website (the driver of Firefox is used in this project)
 - If the Graphical User Interface (GUI) is not available in your system, you can use an X server (We used Xvfb v 11)
 - This point is not needed if you have a GUI :
  - Packages to be installed : xvfb, xfonts-base, xfonts-75dpi, xfonts-100dpi, libgl1-mesa-dri, xfonts-scalable, xfonts-cyrillic, gnome-icon-theme-symbolic 