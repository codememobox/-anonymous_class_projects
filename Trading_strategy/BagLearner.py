
import numpy as np
from scipy.stats import mode


class BagLearner(object):
    def __init__(self, learner=None, kwargs={}, bags=20,
                 boost=False, verbose=False):
        self.learner = learner
        self.kwargs = kwargs
        self.bags = bags
        self.boost = boost
        self.verbose = verbose
        self.learners = [self.learner(**kwargs) for i in range(self.bags)]

    def author(self):
        return "azhou90"  # replace tb34 with your Georgia Tech username

    def add_evidence(self, data_x, data_y):
        """
        Add training data to learner

        :param data_x: A set of feature values used to train the learner
        :type data_x: pandas dataframe
        :param data_y: The value we are attempting to predict given the X data
        :type data_y: pandas series
        """
        data_x = np.array(data_x)
        data_y = np.array(data_y)
        def bag_data(data_x, data_y):
            data_select = np.random.randint(0,data_y.shape[0], data_y.shape[0])
            return data_x[data_select], data_y[data_select]


        for learner in self.learners:
            select_x, select_y = bag_data(data_x, data_y)
            learner.add_evidence(select_x, select_y)

            # y_pred = learner.query(select_x)
            # print(np.sum(y_pred == select_y.squeeze())/len(y_pred))
            # print(data_y)


    def query(self, points):
        points = np.array(points)
        # print(points.shape)
        # initialize a list to store predicted values
        predict = []
        for learner in self.learners:
            y_hat = learner.query(points)
            # print(y_hat)
            predict.append(y_hat)

        # take the mode of predicted values from each tree (dim = 1)
        predict = mode(np.array(predict), axis=0).mode.squeeze()
        # print(predict.shape)
        # print(predict)
        return predict


if __name__ == "__main__":
    print("the secret clue is 'zzyzx'")