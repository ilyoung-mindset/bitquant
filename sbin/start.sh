#!/bin/sh

BIT_QUANT_HOME=`pwd`

python3 -m bitquant.app > ${BIT_QUANT_HOME}/log/std.log &