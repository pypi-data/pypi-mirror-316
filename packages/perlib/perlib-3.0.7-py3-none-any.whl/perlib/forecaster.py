from .core._requests import req_info,aR_info,m_info,prophet_info
from .core.models.dmodels import models as ddmodels
from .core.models.smodels import models as armodels
from .core.models import prophet as phmodels
from .core.train import dTrain,sTrain
from .core.tester import dTester,sTester
from .core.req_utils import *
from .core.metrics.regression import __ALL__
from .preprocessing.autopreprocess import Process
from .preprocessing._utils.dataframe import read_pandas
from .preprocessing._utils.tools import extract_archive,check_datetime
from .analysis.multivariate import MultiVariable
import time
from dateutil.parser import parse
from pandas.api.types import is_datetime64_any_dtype as is_datetime
import os
from datetime import datetime as dt
import numpy as np
import pandas as pd
#from analysis.plotting import plot_correlation,box_plot,kde_plot,regression_plot

statmodels = ["arima","arimax","sarima","sarimax"]
req_info       = req_info()
aR_info        = aR_info()
m_info         = m_info()
preprocess     = Process()
dmodels        = ddmodels
dTrain         = dTrain
dTester        = dTester

#def plot(self,
#         col1 : pd.Series,
#         col2:pd.Series=None,
#         data: pd.DataFrame = None,
#         max_pairs        = 5,
#         kind = "corr"):
#    """
#    kind = 'regression_plot: two Series' , 'kde: one Series', 'box: one Series'
#    :param kind:
#    :return:
#    """
#    if isinstance(kind, str):
#        arrays = []
#        for m in ["corr","kde","box","reg"]:
#            if m == kind:
#                arrays.append(m)
#        if len(arrays) == 0:
#            raise KeyError('must be valid parameters')
#    if kind   == "reg":
#        return regression_plot(col1,col2,labels=[col1.name,col2.name])
#    elif kind == "kde":
#        return kde_plot(col1,label=col1.name)
#    elif kind == "box":
#        return box_plot(col1,label=col1.name)
#    elif kind == "corr":
#        return plot_correlation(col1, max_pairs=max_pairs)


def summarize(path:str = None, dataFrame : pd.DataFrame = None) -> MultiVariable:
    if type(dataFrame) == pd.DataFrame:
        return MultiVariable(dataFrame)
    else:
        df = read_pandas(path)
        return MultiVariable(df)

def get_result(
            y                       : str,
            process                 : bool          = True,
            forecastNumber          : int           = 24,
            modelName               : str           = "lstm",
            metric                  : str           = "mape",
            epoch                   : int           = 10,
            dateColumn              : str           = False,
            path                    : str           = None,
            forecastingStartDate    : str           = None,
            dataFrame               : pd.DataFrame  = None,
            show                    : str           = False,
            cols_feat               : list          = None
               ):

    """Returns forecast,evaluate for the entered parameters. Select the
    "forecastingStartDate" and "forecastNumber" parameters correctly.
    To predict the future, send the last date of the data you use to the
    "forecastingStartDate" parameter. In this case, you won't get results
    with "evaluate", don't forget to adjust your output accordingly.
    Parameters
    ----------
    :param y:  Target variable to be estimated
    :param process: Default : True
    :param forecastNumber: Default : 24  , Number of forecasting < Int >
    :param modelName: Default : lstm,  {'LSTM','BILSTM','CONVLSTM','TCN','RNN','PROPHET','LSTNET','ARIMA','SARIMA'}
    :param metric: Default : mape  Note : "For multiple metric results, you must enter them in the list." examples : ["mape","mae"]
    :param epoch: Default : 10
    :param dateColumn: Default : False
    :param path: Default : None , It will be enough to give the file path of the data you want to use.
    :param forecastingStartDate: The start date you want to predict
    :param dataFrame: Default None
    :param show: Displays the build result for the resulting model.
    :return:
    -------
    """


    # if path is not check
    if path != None:
        if extract_archive(path) is True:
            # metric is str
            if isinstance(metric, str):
                arrays = []
                # metric is items check
                for m, n in __ALL__.items():
                    if metric == m or metric == n:
                        arrays.append(metric)
                # arrays lenght check
                if arrays.__len__() == 0:
                    raise KeyError('must be valid parameters')
        dataFrame = read_pandas(path)


    if hasattr(dataFrame,'shape') is False:
        raise TypeError('data passed must be of type pandas.DataFrame')
    else:
        if dataFrame.shape[0] == 0:
            raise ValueError('Data is empty.')

    if dateColumn is False:
        if type(dataFrame.index) != pd.DatetimeIndex:
            raise ValueError('The dateColumn parameter is null and the datetime index is not found')

    if modelName in statmodels:
        check_S_modelname(
                          aR_info.modelname)
    else:
        check_D_modelname(req_info.modelname)
    if bool(dateColumn) is True:
        if dateColumn in dataFrame.columns.tolist():
            if [column for column in dataFrame.columns if is_datetime(dataFrame[column])].__len__():
                dataFrame = dataFrame
            else:
                try:
                    dataFrame[dateColumn] = pd.to_datetime(dataFrame[dateColumn])
                    parse(str(dataFrame[dateColumn].head(1).values[0]), fuzzy=True)
                    if True:
                        dataFrame[dateColumn] = dataFrame[dateColumn].apply(lambda x: pd.to_datetime(x).tz_localize(None))
                except ValueError:
                    print(False)
        else:
            if type(dataFrame.index) == pd.DatetimeIndex:
                dataFrame = dataFrame.reset_index()
                dataFrame[dateColumn] = pd.to_datetime(dataFrame[dateColumn])
            else:
                raise ValueError("No datetime columns or index found in dataframe")
    else:
        if type(dataFrame.index) == pd.DatetimeIndex or check_datetime(dataFrame.index.values[0]):
            dcol = dataFrame.index.name
            if dcol is None:
                dcol = "Datetime"
                dataFrame.index.name = "Datetime"
            dataFrame = dataFrame.reset_index()

            dataFrame[dcol] = pd.to_datetime(dataFrame[dcol])
            dateColumn = [column for column in dataFrame.columns if is_datetime(dataFrame[column])]
            if dateColumn.__len__():
                dateColumn = dateColumn[0]
                dataFrame[dateColumn] = pd.to_datetime(dataFrame[dateColumn])
        else:
            raise ValueError("No datetime columns or index found in dataframe")
    if y not in dataFrame.columns.tolist():
        raise ValueError("y value not found in dataframe")
    else:
    # 'y' will be in training data
        dataFrame[y] = pd.to_numeric(dataFrame[y])
        if np.isinf(dataFrame[y].values).any():
            raise ValueError('Found infinity in column y.')


    columns = dataFrame.columns
    if process:
        dataFrame = preprocess.auto(dataFrame)
        remove_column = []
        for col in columns:
            column = dataFrame.loc[:, dataFrame.columns.str.startswith(col)].select_dtypes("object").columns.tolist()
            if len(column) != 0:
                remove_column.extend(column)
        dataFrame = dataFrame.drop(remove_column, axis=1)
        dataFrame = dataFrame.set_index(dateColumn)
    else:
        dataFrame = dataFrame[columns]
        dataFrame = dataFrame.set_index(dateColumn)



    #if isinstance(forecastNumber, int):
    #    if forecastNumber > \
    #        dataFrame[dataFrame.index >= forecastingStartDate].__len__():
    #        self.req_info.forecastNumber = \
    #            dataFrame[dataFrame.index >= forecastingStartDate].__len__()
    #else:
    #    raise TypeError\
    #        (f"Argument save must be of type bool, not {type(forecastNumber)}")

    def create_models(modelname):
        if modelname.lower() in statmodels:
            return aR_info
        elif modelname.lower() != "prophet":
            return req_info
        else:
            return prophet_info
        
    info = create_models(modelName)
    
    info.forecastingStartDate = forecastingStartDate
    info.forecastNumber = forecastNumber
    info.period = check_period(dataFrame)
    info.modelname = modelName
    def run(info,models,trainfunc,testfunc):
        if info:
            model_instance = models(info,show)
            print("Parameters created")
            train = trainfunc(dataFrame=dataFrame, object=model_instance)
            print("The model training process has been started.")
            if train:
                train.fit()
                print("Model training process completed")
            time.sleep(5)
            print("The model is being saved")
            model = _get_file()
            t = testfunc(dataFrame=dataFrame, object=model_instance, path=model, metric=metric)
            return t
        
    if info == prophet_info:
        dataFrame = dataFrame.reset_index()
        forecastingStartDate = pd.to_datetime(forecastingStartDate)
        if dateColumn not in dataFrame.columns:
            return "dateColumn not found in dataframe"
        prophet_model = phmodels.ProphetModel(dfnow=dataFrame, n_test_hours=forecastNumber,
                             datetime_test_start=forecastingStartDate,freq=info.period[0],
                             col_y=y, col_ds=dateColumn, cols_feat=cols_feat,metric=metric)
        forecast,evaluate = prophet_model.validate_singletrain()
        return forecast,evaluate
    
    elif info == req_info:
        req_info.targetCol = y
        req_info.epoch = epoch
        t = run(req_info,ddmodels,trainfunc=dTrain,testfunc=dTester)

    elif info == aR_info:
        t = run(aR_info,armodels,trainfunc=sTrain, testfunc=sTester)

    forecast = t.forecast()
    try:
        evaluate = t.evaluate()
        return forecast,evaluate
    except:
        return forecast

    


def _get_file():
    prefix="models/"
    postfix="/models"
    if os.path.exists("models") is False:
        os.mkdir("models")
    _, _, files = next(os.walk(os.getcwd()+postfix))
    if files.__len__() > 0 or _.__len__() > 0:
        twelve = time.time() - 12 * 60 * 60
        file_list = \
            {
                "Datetime": [],
                "File": []
            }
        for file in files:
            if file.endswith(".h5") or file.endswith(".pkl")  and os.path.getmtime(prefix+file) > twelve:
                file_list["Datetime"].append(pd.to_datetime(dt.fromtimestamp(os.path.getmtime(prefix+file))))
                file_list["File"].append(prefix+file)
        for file_ in _:
            if file_.endswith(".tf") and os.path.getmtime(prefix+file_) > twelve:
                file_list["Datetime"].append(pd.to_datetime(dt.fromtimestamp(os.path.getmtime(prefix+file_))))
                file_list["File"].append(prefix+file_)
        file_list = pd.DataFrame(file_list)
        file_list = file_list.sort_values("Datetime", ascending=False).iloc[0]["File"]
        return file_list
    raise FileNotFoundError(f'The saved model could not be found. {files,_}')









