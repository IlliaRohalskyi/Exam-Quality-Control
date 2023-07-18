
class Rule:
    def __init__(self, data_obj):

        self.data_obj = data_obj
        self.score, self.conflicts_df, self.plot_array = self.compute()

    def compute(self):
        raise NotImplementedError




