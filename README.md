# blaze-terminal

**only tested on mac os x, but will probably work on linux too**

## install

```sh
# install npm, and install python deps
conda install npm blaze -c cpcloud -c blaze

# install spark 1.3
conda install -c https://conda.binstar.org/blaze/channel/dev spark

# install bower and coffee-react from npm
npm install -g bower coffee-react

# clone the repo
git clone git://github.com/cpcloud/blaze-terminal

cd blaze-terminal

bower install
```

## Example

Fire up IPython and start a blaze server
```python
In [2]: import pandas as pd

In [3]: import numpy as np

In [4]: df = pd.DataFrame({'a': np.random.randn(1000),
   ...:                    'b': np.random.randint(0, 10, size=1000)})
   ...:

In [5]: from blaze import Server

In [6]: Server({'db': df}).run()  # <- blocking call, default port is 6363
```

Fire up two more terminals
* one for the coffee-script jsx watcher
* one for the application

Coffee Script JSX
```sh
# from the blaze-terminal directory
cjsx --compile --bare --output app/static/js --watch app/static/coffee
```

Application
```sh
# same blaze-terminal dir
./run.sh
```
