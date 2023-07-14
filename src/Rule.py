
class Rule:
    def __init__(self, data):

        self.data = data
        self.score, self.conflicts_df, self.plot_array = self.compute()

    def compute(self):
        raise NotImplementedError




