import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Data import data_obj

class RuleEight:
    def __init__(self):
        self.score, self.conflicts_df, self.plot_arr = self.compute()


