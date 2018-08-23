#!/bin/sh

BIT_QUANT_HOME=`pwd`
export PYTHONPATH=${BIT_QUANT_HOME}/bitquant/api

jupyter notebook --ip='0.0.0.0' --notebook-dir ${BIT_QUANT_HOME}/notebook --no-browser  > ${BIT_QUANT_HOME}/log/notebook.std.log &
