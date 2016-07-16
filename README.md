# NEXpy
NEXpy is a simple Python radar tool using siphon to obtain the data and metPy for color tables. Requirements are subject to change as we find the most stable (and fast!) configuration for this program.

Requirements
------
* Numpy
* Matplotlib
* Cartopy
* Siphon
* metPy

Usage
------
To use simply enter: ```python level3.py <SiteID> <ProductID> <animate?>```

Example:
To obtain the latest TDWR Reflectivity Image from Charlotte-Douglas Intl you would enter: 
```python level3.py CLT TR0 false```

If you would like to try out what I have accomplished with animating the data so far, you simply change the false flag to true.

Installation Tutorial
------
Once the project matures some, I will consider bundling it into an installation package so the whole family can have fun! For now, we have source. Personally I prefer Anaconda (or miniconda if that's how you roll) because it makes installing Python packages, almost, a non-event.

1. [Get Anaconda](https://www.continuum.io/downloads)
2. Open your terminal/command prompt/button masher
3. Install the base packages:
  * ```conda install pip numpy matplotlib ```
4. Now use pip to install the other requirements:
  * ```pip install metpy siphon cartopy ```
5. Congratulations! Now you can run the command under "Usage" to get started
