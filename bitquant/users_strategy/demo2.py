import time
from datetime import datetime
import numpy as np
import pandas as pd
from bitquant.api import bqdata
import matplotlib.pyplot as plt
from matplotlib.pylab import date2num
import mpl_finance as mpf
import talib

def initialize(context):
    print('initialize')
    
def handle_data(context):
    context.order(context.market, 'ethbtc', 1000, 100)

def handle_tick(context):
    context.order(context.market, 'ethbtc', 1000, 200)
