#!/bin/sh

BIT_QUANT_HOME=`pwd`
export PYTHONPATH=${BIT_QUANT_HOME}/bitquant/api

Jupyter notebook --ip='0.0.0.0' --notebook-dir ${BIT_QUANT_HOME}/bitquant/notebook --no-browser
