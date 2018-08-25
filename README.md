# Bitquant
For digital currency quantitative transaction

## Features

* Get arbitrage profit in same market
* Get arbitrage profit in different market
* Tools for Quant

## build
### python
python verion: python3
* install python3，
* install `pyton3` module
```bash
python3 -m pip install requests
python3 -m pip install websocket_client
python3 -m pip install 'python-daemon'
python3 -m pip install PyMySQL
python3 -m pip install sqlalchemy
python3 -m pip install DBUtils
python3 -m pip install flask
```

### Mysql
* install mysql
* create database `bitquant`
```sql
CREATE DATABASE `bitquant` DEFAULT CHARACTER SET utf8;
CREATE USER bitquant@'localhost' IDENTIFIED BY 'bitquant!';
GRANT ALL PRIVILEGES ON bitquant.* TO bitquant;
GRANT ALL PRIVILEGES ON bitquant.* TO bitquant@'%' IDENTIFIED BY 'bitquant!';
FLUSH PRIVILEGES;
```
* create mysql tables `db/tables.sql`

## run app
```
python3 -m bitquant.app
```

## notebook environment
* install Jupyter
```bash
python3 -m pip install jupyter notebook
python3 -m pip install jupyter-echarts-pypkg
```
* install ta-lib see document here https://github.com/mrjbq7/ta-lib
* install numpy pandas matplotlib mpl_finance talib pyecharts
* init bitquant notebook config
```bash
jupyter notebook --generate-config
jupyter notebook password 
```
* run bitquant notebook 
```bash
sh sbin/start_notebook.sh
```

## stragery engine

