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
To use simply enter: ```python level3.py <SiteID> <ProductID>```

Example:
To obtain the latest TDWR Reflectivity Image from Charlotte-Douglas Intl you would enter: 
```python level3.py CLT TR0```
