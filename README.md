# Bitquant
For digital currency quantitative transaction

## Features

* Get arbitrage profit in same market
* Get arbitrage profit in different market
* Tools for Quant

# build
## python
python verion: python3
* install python3，
* install `pyton3 websocket` module
```bash
 python3 -m pip install websocket_client
```
* install `python-deamon`
```bash
python3 -m pip install 'python-daemon'
```
* install `pyton3 PyMySQL` module
```
python3 -m pip install PyMySQL
```

```
python3 -m pip install  sqlalchemy
```

## run app
```
python3 -m bitquant.app
```

## notebook environment
* install Jupyter
```
python3 -m pip install jupyter notebook
```
```
python3 -m pip install jupyter-echarts-pypkg
```
* install ta-lib see document here https://github.com/mrjbq7/ta-lib
* install numpy pandas matplotlib mpl_finance talib pyecharts
* init bitquant notebook config
```
jupyter notebook --generate-config
jupyter notebook password 
```
* run bitquant notebook 
```
sh sbin/start_notebook.sh
```

## stragery engine

