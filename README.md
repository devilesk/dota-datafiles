dota-datafiles
===============
Python scripts I use to generate json and other data files used in my dota website and projects like my [hero calculator](https://github.com/devilesk/hero-calculator)

Usage:

```
cd build

python3 parser.py --make_dirs --dotabuff --process
```

test client:

```
python3 parser.py --make_dirs --dotabuff_branch test-client-20161211 --dotabuff --process
```