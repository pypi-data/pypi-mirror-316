import os
import pandas as pd
import numpy as np
import json
import joblib
from .models.smodels import models as smodels
from .models.mmodels import models as mmodels
from .models.lstnet import LSTNetModel
from .models.elm import ELM
from ..preprocessing.preparate import dataPrepration
import tensorflow as tf
from datetime import datetime
from .req_utils import *
from itertools import product
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.arima.model import ARIMA
from ..piplines.mpipline import Regressor,Classifier
from sklearn.linear_model import *
from sklearn.svm import *
from sklearn.ensemble import *
from xgboost import *
from sklearn.naive_bayes import *
from sklearn.neighbors import *
from sklearn.tree import *
from sklearn.linear_model import *
from sklearn.cluster import *
from sklearn.semi_supervised import LabelSpreading
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.calibration import CalibratedClassifierCV,IsotonicRegression
from .metrics.regression import *
from catboost import *
from lightgbm import *
from sklearn.neural_network import *
from .metrics.classification import *
from .metrics.regression import __ALL__ as r__ALL__
from .metrics.classification import __ALL__ as c__ALL__
from ..preprocessing._utils.tools import to_df
from .tester import dTester
from ..preprocessing._split import train_test_split
from pandas.api.types import is_object_dtype,is_categorical_dtype,is_integer_dtype
class mTrain:
    def __init__(self,
                 dataFrame: pd.DataFrame,
                 object = None
                 ):
        self.pr = dataPrepration()
        self.dataFrame = dataFrame
        self.object = object
        auto_summaryDf = None

    def _save_request_param(self,name):
        with open(str(name)+".json", "w") as outfile:
            json.dump(str(self.object.m_info.__dict__), outfile)

    def get_name_model(self,model=None):
        if self.object.m_info.auto is False:
            return check_M_modelname(modelname=self.object.m_info.modelname,auto=False)
        else:
            return type(model).__name__
    def check_mod(self):
        if self.object.m_info.modelname:
            if self.object.m_info.auto is False:
                if self.object.m_info.modelname in reg:
                    return Regressor
                else:
                    return Classifier
            else:
                if is_integer_dtype(self.dataFrame[self.object.m_info.y]):
                    self.dataFrame[
                        [col for col in self.dataFrame.columns if self.dataFrame[col].dtypes == self.dataFrame \
                            [self.object.m_info.y].dtypes.name]] = \
                        self.dataFrame[[col for col in self.dataFrame.columns if self.dataFrame \
                            [col].dtypes == self.dataFrame[self.object.m_info.y].dtypes.name]].astype('category')
                    if is_object_dtype(self.dataFrame[self.object.m_info.y]) or \
                            is_categorical_dtype(self.dataFrame[self.object.m_info.y]):
                        if hasattr(self.dataFrame[self.object.m_info.y], "cat"):
                            return Classifier
                else:
                    if hasattr(self.dataFrame[self.object.m_info.y], "cat"):
                        return Classifier
                    return Regressor

    def c_opt(self,X_train, X_test, y_train, y_test):
        if self.object.m_info.auto:
            mod = self.check_mod()
            model, predictions = mmodels.opt(X_train, X_test, y_train, y_test,mod=mod,scaler=self.pr.get_scaler(self.object.m_info.scaler))
            if model.shape[0] > 1:
                try:
                    model = model.sort_values("Accuracy", ascending=False)
                except:
                    model = model.sort_values("R-Squared", ascending=False)
                print(model)
                self.auto_summaryDf = model
                return model.head(1).index.tolist()[0]
            else:
                raise ValueError("No models found.")
        else:
            return False

    def __check_folder(self):
        if os.path.exists("models") is False:
            os.mkdir("models")

    def save_model(self,model):
        self.__check_folder()
        prefix="models/"
        model_name = f'Data-{mTrain.get_name_model(self,model=model)}-{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}'
        joblib.dump(model,prefix+model_name + '.pkl')
        mTrain._save_request_param(self,name=prefix+model_name)

    def check_dataFrame(self):
        if type(self.dataFrame) is pd.DataFrame or isinstance(self.dataFrame, pd.DataFrame):
            if self.dataFrame.shape[0] == 0:
                raise ValueError('Data is empty.')
            return True
        else:
            raise TypeError("must be datafarame")

    def data_split_(self):
        X = self.dataFrame.loc[:, self.dataFrame.columns != self.object.m_info.y].values
        y = self.dataFrame[[self.object.m_info.y]].values
        return X,y

    def _scaler(self,X,y):
        self.scalerX = self.pr.get_scaler(self.object.m_info.scaler)
        self.scalery = self.pr.get_scaler(self.object.m_info.scaler)
        self.X = self.scalerX.fit_transform(X)
        if self.check_mod().__name__ == "Regressor":
            self.y = self.scalery.fit_transform(y)
        else:
            self.y=y
        return self.X,self.y,self.scalerX,self.scalery

    def _test_size(self,X,y):
        if self.object.m_info.testsize is not None:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=self.object.m_info.testsize,shuffle=self.object.m_info.shuffle)
            return X_train, X_test, y_train, y_test
        else:
            return X,None,y,None


    def tr(self):
        if self.check_dataFrame():
            self.object.m_info.modelname = self.get_name_model()
            columns = self.dataFrame.columns
            remove_column = []
            for col in columns:
                column = self.dataFrame.loc[:, self.dataFrame.columns.str.startswith(col)].select_dtypes(
                    "object").columns.tolist()
                if len(column) != 0:
                    remove_column.extend(column)
            self.dataFrame = self.dataFrame.drop(remove_column, axis=1)
            X,y = self.data_split_()
            X,y,scalerX,scalery =self._scaler(X,y)
            X_train, X_test, y_train, y_test  = self._test_size(X,y)
            if self.object.m_info.auto:
                self.object.m_info.modelname = self.c_opt(X_train, X_test, y_train, y_test)
            m = eval(self.object.m_info.modelname)
            return m,scalerX,scalery,X_train,X_test, y_train, y_test

    def fit(self):
        m,scalerX,scalery,X_train,X_test, y_train, y_test = self.tr()
        if self.object.m_info.modelparams:
            try:
                model = m(**self.object.m_info.modelparams)
            except:
                model = ELM(self.object.m_info.modelparams)
        else:
            model = m()
        model.fit(X_train, y_train)
        return model,scalery,scalerX,X_test, y_test

    def predict(self,metric= "mape"):
        """
        :param metric: Classification metrics : {"accuracy_score": "acc", "confusion_matrix": "cm",
        "multilabel_confusion_matrix": "mcm", "cohen_kappa_score": "cks", "jaccard_score": "js",
        "matthews_corrcoef": "mc", "zero_one_loss": "zol", "f1_score": "fs", "hinge_loss": "hl",
        "hamming_loss": "hml", "classification_report": "cr", "precision_score": "ps", "recall_score": "rs",
        "balanced_accuracy_score": "bac", "precision_recall_fscore_support": "prfs", "fbeta_score": "fbs"}" or
        Regression metrics : {"max_error": "ma", "mean_absolute_error": "mae", "mean_squared_error": "mse",
        "mean_squared_log_error": "msle", "median_absolute_error": "meae", "mean_absolute_percentage_error": "mape"}
        :return:
        """
        model_fit,scalery,scalerX,X_test, y_test= self.fit()
        if X_test is not None and y_test is not None:
            if self.check_mod().__name__ == "Regressor":
                preds = scalery.inverse_transform(model_fit.predict(X_test).reshape(-1, 1))
                y_test = scalery.inverse_transform(y_test)
            else:
                preds = model_fit.predict(X_test)
            preds = to_df(preds, columns=["Predicts"])
            try:
                preds["Actual"] = y_test.values
            except:
                preds["Actual"] = y_test
            self.save_model(model=model_fit)
            evaluate = dTester.calculate(preds.Actual.values, preds.Predicts.values,metric=metric)
            return preds, evaluate
        self.save_model(model=model_fit)

    def tester(self,path,testData):
        model = joblib.load(path)
        columns = testData.columns
        remove_column = []
        for col in columns:
            column = testData.loc[:, testData.columns.str.startswith(col)].select_dtypes(
                "object").columns.tolist()
            if len(column) != 0:
                remove_column.extend(column)
        testData = testData.drop(remove_column, axis=1)
        preds = model.predict(self.scalerX.transform(testData)).reshape(-1,1)
        inverse_data = self.scalery.inverse_transform(preds)
        predicts_data = pd.DataFrame(inverse_data,columns=["Predicts"])
        return predicts_data

class sTrain:
    def __init__(self,
                 dataFrame: pd.DataFrame,
                 verbose = None,
                 object = None
                 ):
        self.dataFrame = dataFrame
        self.object    = object
        self.verbose   = verbose

    def _save_request_param(self,name):
        with open(str(name)+".json", "w") as outfile:
            json.dump(str(self.object.aR_info.__dict__), outfile)
    def get_name_model(self):
        return self.object.aR_info.modelname

    def set_params(self, object):
        object.max_p = range(0, object.max_p, 1)
        object.max_d = range(0, object.max_d, 1)
        object.max_q = range(0, object.max_q, 1)
        object.max_P = range(0, object.max_P, 1)
        object.max_D = range(0, object.max_D, 1)
        object.max_Q = range(0, object.max_Q, 1)

    def __check_folder(self):
        if os.path.exists("models") is False:
            os.mkdir("models")

    def fit(self):
        prefix="models/"
        if type(self.dataFrame) is pd.DataFrame or isinstance(self.dataFrame, pd.DataFrame):
            if self.dataFrame.shape[0] == 0:
                raise ValueError('Data is empty.')
        else:
            raise TypeError("must be datafarame")
        check_forecast_date(
            dataFrame=self.dataFrame,
            info=self.object.aR_info
        )
        column = self.dataFrame.columns.tolist()[0]
        self.dataFrame = self.dataFrame.iloc[:,:1]
        self.dataFrame[column] = self.dataFrame[column].astype(float)
        data = np.log(self.dataFrame)
        data_train = data[data.index < self.object.aR_info.forecastingStartDate]
        data_test = data[data.index > data_train.index[-1]]
        if not isinstance(self.object.aR_info.max_p, range):
            self.set_params(self.object.aR_info)

        params = product(self.object.aR_info.max_p,
                         self.object.aR_info.max_d,
                         self.object.aR_info.max_q,
                         self.object.aR_info.max_P,
                         self.object.aR_info.max_D,
                         self.object.aR_info.max_Q)

        params_list = list(params)
        res_df = smodels.opt(name=self.object.aR_info.modelname,params=params_list, s=self.object.aR_info.s, train=data_train,test=data_test)
        order = res_df.iloc[0][0]
        or_a = order[:3]
        or_s = order[3:]
        if self.object.aR_info.modelname.lower() == "sarima":
            model_fit = SARIMAX(data_train, order=or_a, seasonal_order=(or_s[0],
                                                                        or_s[1],
                                                                        or_s[2],
                                                                        self.object.aR_info.s)).fit()
        else:
            model_fit = ARIMA(data_train, order=(or_a)).fit()
        model_fit.summary()
        model_name = f'Data-{self.get_name_model()}-{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}'
        self.__check_folder()
        model_fit.save(prefix+model_name+'.pkl')
        self._save_request_param(name=prefix+model_name)
        return model_fit

class dTrain:

    def __init__(self,
                 dataFrame: pd.DataFrame,
                 object = None
                 ):
        self.pr = dataPrepration()
        self.dataFrame = dataFrame
        self.object = object
        self.model = self.model()


    def model(self):

        global model
        if type(self.dataFrame) is pd.DataFrame or isinstance(self.dataFrame, pd.DataFrame):
            if self.dataFrame.shape[0] == 0:
                raise ValueError('Data is empty.')
        else:
            raise TypeError("must be datafarame")
        check_forecast_date(
            dataFrame=self.dataFrame,
            info=self.object.req_info
        )
        self.dataFrame = self.pr.trainingFordate_range(dataFrame=self.dataFrame,
                                                              dt1=self.dataFrame.index[0],
                                                              dt2=self.object.req_info.forecastingStartDate)
        # scaler = self.pr.get_scaler(self.object.req_info.scaler)
        #dataset = scaler.fit_transform(self.dataFrame)
        #X, y = self.pr.unvariate_data_create_dataset(dataset=dataset, window=self.object.req_info.lookback)

        X,y = self._get_data()
        BATCH_SIZE = self.object.req_info.batch_size
        self.BUFFER_SIZE = 150
        train_data_multi = tf.data.Dataset.from_tensor_slices((X, y))
        train_data_multi = train_data_multi.cache().shuffle(self.BUFFER_SIZE).batch(BATCH_SIZE).repeat()
        val_data_multi = tf.data.Dataset.from_tensor_slices((X, y))
        val_data_multi = val_data_multi.batch(BATCH_SIZE).repeat()
        if self.object.req_info.modelname.lower() == "lstnet":
            if self.object.req_info.layers is not None:
                model = LSTNetModel(input_shape=X.shape,
                                lookback=self.object.req_info.lookback,
                                **self.object.req_info.layers)
            else:
                model = LSTNetModel(input_shape=X.shape,
                                lookback=self.object.req_info.lookback)
        else:
            self.object.set_inputShape((X.shape[-2:]))
            self.object.build_model()
            model = self.object.model_multi
        self.train_data_multi = train_data_multi
        self.val_data_multi   = val_data_multi
        try:
            self.name = model.input_names[0]
        except:
            self.name = "Bilstm"
        return model

    def __multiDataSplit(self, dataFrame = pd.DataFrame):
        if isinstance(dataFrame, pd.DataFrame):
            self.dataFrame = dataFrame
        Xn = self.dataFrame.iloc[:,0:].values
        yn = self.dataFrame.loc[:,self.dataFrame.columns == self.object.req_info.targetCol].values
        return Xn,yn

    def get_name_model(self):
        return self.object.req_info.modelname

    def _save_json_model_param(self, model, name):
        json_model = model.to_json()
        with open(str(name)+'.json', 'w') as json_file:
            json_file.write(json_model)

    def _save_request_param(self,name):
        with open(str(name)+".json", "w") as outfile:
            json.dump(self.object.req_info.__dict__, outfile)

    def _check_modelName(self):
        return self.object.req_info.modelname

    def _save_format(self):
        if self.object.req_info.modelname == "tcn":
            return ".tf"
        else:
            return ".h5"

    def _get_data(self):
        if self.dataFrame.shape[1] == 1:
            scaler = self.pr.get_scaler(self.object.req_info.scaler)
            dataset = scaler.fit_transform(self.dataFrame)
            X, y = self.pr.unvariate_data_create_dataset(dataset=dataset, window=self.object.req_info.lookback)
            return X, y
        elif self.dataFrame.shape[1] != 1:
            scalerX = self.pr.get_scaler(self.object.req_info.scaler)
            scalerY = self.pr.get_scaler(self.object.req_info.scaler)
            X_data = scalerX.fit_transform(self.dataFrame.values)
            Y_data = scalerY.fit_transform(self.dataFrame[self.object.req_info.targetCol].values.reshape(-1, 1))
            X, y = self.pr.multivariate_data_create_dataset(dataset=X_data, target=Y_data,window=self.object.req_info.lookback)
            return X, y

    def __check_folder(self):
        if os.path.exists("models") is False:
            os.mkdir("models")

    def fit(self):
        self.__check_folder()
        prefix="models/"
        model_name = f'Data-{self.get_name_model()}-{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}'
        callbacks_list = [tf.keras.callbacks.EarlyStopping(monitor='val_loss',patience=10,),
                          tf.keras.callbacks.ModelCheckpoint(filepath=prefix+model_name+str(self._save_format()), monitor='val_loss', mode='min',
                                                          save_freq='epoch', save_best_only=True, ),tf.keras.callbacks.TensorBoard(log_dir='./logs')]
        self.model =  self.model.fit(self.train_data_multi, batch_size=self.object.req_info.batch_size,
                              steps_per_epoch = 500,
                              epochs=self.object.req_info.epoch,
                              validation_data=self.val_data_multi,
                              validation_steps=50,
                              verbose=1,
                              callbacks = callbacks_list)
        self._save_request_param(name=prefix+model_name)
        #self._save_json_model_param(self.model.model,model_name)
        return self.model


    """
    Multivariate
    """
    #def model(self):
    #    scX, scY, X_data, Y_data = \
    #        self.pr.scaler(dataFrame=self.dataFrame, col=self.col)
    #    X,y = self.pr.multivariate_data_create_dataset(dataset=X_data,
    #                                                   target=Y_data,window=self.object.req_lstm.lookback)
    #    BATCH_SIZE = self.object.req_lstm.batch_size
    #    self.BUFFER_SIZE = 150
#
    #    train_data_multi = tf.data.Dataset.from_tensor_slices((X, y))
    #    train_data_multi = train_data_multi.cache().shuffle(self.BUFFER_SIZE).batch(BATCH_SIZE).repeat()
    #    val_data_multi = tf.data.Dataset.from_tensor_slices((X, y))
    #    val_data_multi = val_data_multi.batch(BATCH_SIZE).repeat()
    #    self.object.set_inputShape((X.shape[-2:]))
    #    model = self.object.build_model()
    #    self.train_data_multi = train_data_multi
    #    self.val_data_multi   = val_data_multi
    #    self.name = model.input_names[0]
    #    self.scX = scX
    #    self.scY = scY
    #    return model