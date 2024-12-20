


# Perlib

This repository hosts the development of the Perlib library.

## About Perlib

Perlib is a framework written in Python where you can use deep and machine learning algorithms.

## Perlib is
Feature to use many deep or machine learning models easily
Feature to easily generate estimates in a single line with default parameters
Understanding data with simple analyzes with a single line
Feature to automatically preprocess data in a single line
Feature to easily create artificial neural networks
Feature to manually pre-process data, extract analysis or create models with detailed parameters, produce tests and predictions

## Usage
The core data structures are layers and models. For quick results with default parameters
To set up more detailed operations and structures, you should use the Perflib functional API, which allows you to create arbitrary layers or write models completely from scratch via subclassing.


## Install
```python
pip install perlib
```

```python
from perlib.forecaster import *
```

This is how you can use sample datasets.

```python
from perlib import datasets # or  from perlib.datasets import *
import pandas as pd
dataset = datasets.load_airpassengers()
data = pd.DataFrame(dataset)
data.index = pd.date_range(start="2022-01-01",periods=len(data),freq="d")
```

To read your own dataset;
```python 
import perlib
pr = perlib.dataPrepration()
data = pr.read_data("./datasets/winequality-white.csv",delimiter=";")
```

```python 
model_selector = perlib.ModelSelection(data_l)
model_selector.select_model()
```


```python

Dimension Reduction Analysis: Size reduction is not recommended.

Selected Models:
1. ('BILSTM', 'Data symmetric, BILSTM is available.')
2. ('CONVLSTM', 'There are spatial and temporal patterns, CONVLSTM can be used.')
3. ('SARIMA', 'No time series data found, SARIMA is not recommended.')
4. ('PROPHET', 'No time series data found, PROPHET is not recommended.')
5. ('LSTM', 'Insufficient dataset size, LSTM is not recommended.')
6. ('LSTNET', 'Insufficient dataset size, LSTNet is not recommended.')
7. ('TCN', 'No temporal dependencies, TCN is not recommended.')
8. ('XGBoost', 'No irregular and heterogeneous data, XGBoost is not recommended.')

```




## Features

- Automatic model architecture recommendation
- Data characteristics analysis
- Memory usage optimization
- Bottleneck detection
- Preprocessing requirement analysis
- Time series analysis capabilities
- Resource requirement estimation

## Quick Start

Basic usage of ModelSelectionDL:

```python
from modelSelection.selection import ModelSelectionDL
import pandas as pd

# Load your data
data = pd.read_csv('your_data.csv')

# Initialize the model selector
selector = ModelSelectionDL(data, target='target_column')

# Get recommendations
selector.display_results()
```

## Detailed Usage

### 1. Data Preparation

```python
import pandas as pd
import numpy as np

# Load and prepare your data
data = pd.read_csv('your_data.csv')

# Handle date columns if present
data['date_column'] = pd.to_datetime(data['date_column'])

# Handle missing values if needed
data = data.fillna(method='ffill').fillna(method='bfill')
```

### 2. Model Selection

```python
# Initialize with your data
selector = ModelSelectionDL(data, target='target_column')

# Get full recommendations
recommendations = selector.get_model_recommendations()

# Display formatted results
selector.display_results()
```

### 3. Accessing Specific Analysis

```python
# Get architecture details for a specific model
rnn_details = recommendations['architecture_details']['RNN']
print(rnn_details)

# Get top recommended models
top_models = recommendations['top_recommendations']
print(top_models)

# Get preprocessing requirements
preprocessing = recommendations['preprocessing_requirements']
print(preprocessing)
```

### 4. Memory Analysis

```python
# Get memory constraints analysis
memory_analysis = selector._analyze_memory_constraints()
print(memory_analysis)

# Get recommended batch size
batch_size = selector._recommend_batch_size_for_memory()
print(f"Recommended batch size: {batch_size}")
```

### 5. Quality Analysis

```python
# Get data quality analysis
quality_analysis = selector._analyze_data_quality_issues()
print(quality_analysis)

# Get preprocessing needs
preprocessing_needs = selector._analyze_preprocessing_needs()
print(preprocessing_needs)
```

## Example Output

The tool provides comprehensive analysis including:

```
================================================================================
TOP RECOMMENDED MODELS
================================================================================
1. RNN
2. LSTM
3. Transformer

================================================================================
DETAILED ARCHITECTURE ANALYSIS
================================================================================
MODEL: RNN
...
```

## Supported Models

- RNN/LSTM
- Transformer
- CNN
- N-BEATS
- Prophet
- ARIMA/SARIMA
- DeepAR
- And more...

## Output Details

The analysis includes:
- Model compatibility scores
- Architecture recommendations
- Preprocessing requirements
- Memory usage analysis
- Data quality assessment
- Resource requirements
- Training time estimates

## Advanced Features

### Custom Analysis

```python
# Get specific bottleneck analysis
bottlenecks = selector._identify_potential_bottlenecks()

# Get computational requirements
compute_reqs = selector._analyze_computational_requirements()

# Estimate training time
training_time = selector._estimate_training_time()
```

### Time Series Analysis

```python
# Get seasonality analysis
seasonality = selector._analyze_seasonality()

# Check stationarity
stationarity = selector._check_stationarity()
```


## Quick Start

Basic usage of ModelSelectionML:

```python
from modelSelection.selection import ModelSelectionML
import pandas as pd

# Load your data
data = pd.read_csv('your_data.csv')

# Initialize the model selector
selector = ModelSelectionML(data, target='target_column')

# Get recommendations
report = model_selector.generate_report()
```


### Dataset Characteristics
- Samples: 1,186
- Features: 27
- Feature Types: Time series, numeric, binary, categorical
- Memory Usage: ~385KB

### Data Quality Insights
- Most features have complete data (no missing values)
- Some financial features (Gross, Net) have ~73% missing values
- High unique ratios in financial indicators
- Moderate to low outlier ratios in most numeric features

### Feature Correlations
Strong correlations observed between:
- Financial indicators (USD, Euro, BIST100)
- Epidemiological data (Total cases, Total deaths)
- Market metrics (Open, Close, Max, Min prices)

### Model Recommendations

#### Regression Models (with evaluation scores)
```
XGBoost Regressor           | 0.90
LightGBM Regressor         | 0.89
Random Forest Regressor    | 0.88
CatBoost Regressor        | 0.87
Gradient Boosting         | 0.86
```

#### Dimensionality Reduction
```
PCA    | 0.90
UMAP   | 0.88
t-SNE  | 0.87
```

### Preprocessing Requirements
- Handle missing values in financial features
- Scale numeric features
- Encode categorical variables
- Consider dimensionality reduction for feature space optimization

This analysis demonstrates the tool's capability to:
- Analyze complex financial and time series data
- Identify data quality issues
- Recommend appropriate ML models
- Suggest preprocessing steps
- Evaluate feature relationships











The easiest way to get quick results is with the 'get_result' function.
You can choice modelname ;
"RNN", "LSTM", "BILSTM", "CONVLSTM", "TCN", "LSTNET", "ARIMA" ,"SARIMA" or all machine learning algorithms


```python 
forecast,evaluate = get_result(dataFrame=data,
                    y="Values",
                    modelName="Lstnet",
                    dateColumn=False,
                    process=False,
                    forecastNumber=24,
                    metric=["mape","mae","mse"],
                    epoch=2,
                    forecastingStartDate=2022-03-06
                    )
```
```python 

Parameters created
The model training process has been started.
Epoch 1/2
500/500 [==============================] - 14s 23ms/step - loss: 0.2693 - val_loss: 0.0397
Epoch 2/2
500/500 [==============================] - 12s 24ms/step - loss: 0.0500 - val_loss: 0.0092
Model training process completed

The model is being saved
1/1 [==============================] - 0s 240ms/step
1/1 [==============================] - 0s 16ms/step
1/1 [==============================] - 0s 10ms/step
1/1 [==============================] - 0s 16ms/step
              Values   Predicts
Date                            
2022-03-07         71  79.437263
2022-03-14         84  84.282906
2022-03-21         90  88.096298
2022-03-28         87  82.875603
MAPE: 3.576822717339706

```

```python 
forecast

            Predicts   Actual
Date                            
2022-03-07         71  79.437263
2022-03-08         84  84.282906
2022-03-09         90  88.096298
2022-03-10         87  82.875603
```

```python 
evaluate

{'mean_absolute_percentage_error': 3.576822717339706,
 'mean_absolute_error': 14.02137889193878,
 'mean_squared_error': 3485.26570064559}
```


he Time Series module helps to create many basic models
without using much code and helps to understand which models 
work better without any parameter adjustments.
```python 
from perlib.piplines.dpipline import Timeseries
pipline = Timeseries(dataFrame=data,
                       y="Values",
                       dateColumn=False,
                       process=False,
                       epoch=1,
                       forecastingStartDate="2022-03-06",
                       forecastNumber= 24,
                       models="all",
                       metrics=["mape","mae","mse"]
                       )
predictions = pipline.fit()

            mean_absolute_percentage_error | mean_absolute_error  | mean_squared_error
LSTNET                              14.05  |                67.70 |  5990.35
LSTM                                7.03   |                38.28 |  2250.69
BILSTM                              13.21  |                68.22 |  6661.60
CONVLSTM                            9.62   |                48.06 |  2773.69
TCN                                 12.03  |                65.44 |  6423.10
RNN                                 11.53  |                59.33 |  4793.62
ARIMA                               50.18  |                261.14|  74654.48
SARIMA                              10.48  |                51.25 |  3238.20
```


With the 'summarize' function you can see quick and simple analysis results.
```python 
summarize(dataFrame=data)
```


With the 'auto' function under 'preprocess', you can prepare the data using general preprocessing.
```python 
preprocess.auto(dataFrame=data)

12-2022 15:04:36.22    - DEBUG - Conversion to DATETIME succeeded for feature "Date"
27-12-2022 15:04:36.23 - INFO - Completed conversion of DATETIME features in 0.0097 seconds
27-12-2022 15:04:36.23 - INFO - Started encoding categorical features... Method: "AUTO"
27-12-2022 15:04:36.23 - DEBUG - Skipped encoding for DATETIME feature "Date"
27-12-2022 15:04:36.23 - INFO - Completed encoding of categorical features in 0.001252 seconds
27-12-2022 15:04:36.23 - INFO - Started feature type conversion...
27-12-2022 15:04:36.23 - DEBUG - Conversion to type INT succeeded for feature "Salecount"
27-12-2022 15:04:36.24 - DEBUG - Conversion to type INT succeeded for feature "Day"
27-12-2022 15:04:36.24 - DEBUG - Conversion to type INT succeeded for feature "Month"
27-12-2022 15:04:36.24 - DEBUG - Conversion to type INT succeeded for feature "Year"
27-12-2022 15:04:36.24 - INFO - Completed feature type conversion for 4 feature(s) in 0.00796 seconds
27-12-2022 15:04:36.24 - INFO - Started validation of input parameters...
27-12-2022 15:04:36.24 - INFO - Completed validation of input parameters
27-12-2022 15:04:36.24 - INFO - AutoProcess process completed in 0.034259 seconds
```



If you want to build it yourself;
```python 
from perlib.core.models.dmodels import models
from perlib.core.train import dTrain
from perlib.core.tester import dTester
```
 You can use many features by calling the 'dataPrepration' function for data preparation operations.
```python 
data = dataPrepration.read_data(path="./dataset/Veriler/ayakkabı_haftalık.xlsx")
```
```python 
data = dataPrepration.trainingFordate_range(dataFrame=data,dt1="2013-01-01",dt2="2022-01-01")
```

You can use the 'preprocess' function for data preprocessing.
```python 
data = preprocess.missing_num(dataFrame=data)
```
```python 
data = preprocess.find_outliers(dataFrame=data)
```
```python 
data = preprocess.encode_cat(dataFrame=data)
```
```python 
data = preprocess.dublicates(dataFrame=data,mode="auto")
```

You should create an architecture like below.
```python 
layers = {
            "unit":[150,100], 
            "activation":["tanh","tanh"],
            "dropout"  :[0.2,0.2]
         }
```

You can set each parameter below it by calling the 'req_info' object.
```python 
from perlib.forecaster import req_info,dmodels
from perlib.core.train import dTrain
from perlib.core.tester import dTester

#layers = {
#        "CNNFilters":100,
#        "CNNKernel":6,
#        "GRUUnits":50,
#        "skip" : 25,
#        "highway" : 1
#          }

req_info.layers = None
req_info.modelname = "lstm"
req_info.epoch  =  30
#req_info.learning_rate = 0.001
req_info.loss  = "mse"
req_info.lookback = 30
req_info.optimizer = "adam"
req_info.targetCol = "Values"
req_info.forecastingStartDate = "2022-01-06 15:00:00"
req_info.period = "daily"
req_info.forecastNumber = 30
req_info.scaler = "standard"
s = dmodels(req_info)

```

It will be prepared after importing it into models.
```python 
s = models(req_info)
```

After sending the dataframe and the prepared architecture to the dTrain, you can start the training process by calling the .fit() function.
```python 
train = dTrain(dataFrame=data,object=s)
train.fit()
```
After the training is completed, you can see the results by giving the dataFrame,object,path,metric parameters to 'dTester'.
```python 
t = dTester(dataFrame=data,object=s,path="Data-Lstm-2022-12-14-19-56-28.h5",metric=["mape","mae"])
```
```python 
t.forecast()
```
```
1/1 [==============================] - 0s 21ms/step
1/1 [==============================] - 0s 20ms/step
1/1 [==============================] - 0s 19ms/step
1/1 [==============================] - 0s 20ms/step
1/1 [==============================] - 0s 20ms/step
1/1 [==============================] - 0s 21ms/step
1/1 [==============================] - 0s 20ms/step
1/1 [==============================] - 0s 20ms/step
1/1 [==============================] - 0s 21ms/step
1/1 [==============================] - 0s 21ms/step
1/1 [==============================] - 0s 21ms/step
1/1 [==============================] - 0s 22ms/step
1/1 [==============================] - 0s 21ms/step

```

```python 
t.evaluate()

MAPE: 3.35
```

```python 
from perlib.core.models.smodels import models as armodels
from perlib.core.train import  sTrain
from perlib.core.tester import sTester
```
```python 
aR_info.modelname = "sarima"
aR_info.forcastingStartDate = "2022-6-10"
```
```python 
ar = armodels(aR_info)
#train = sTrain(dataFrame=data,object=ar)
res = train.fit()
```
```python 
r = sTester(dataFrame=data,object=ar,path="Data-sarima-2022-12-30-23-49-03.pkl")
r.forecast()
r.evaluate()
```

```python 
from perlib.core.models.mmodels import models
from perlib.core.train import mTrain
```

```python 
m_info.testsize = .01
m_info.y        = "quality"
m_info.modelname= "SVR"
m_info.auto  = False
```

```python 
m = models(m_info)
train = mTrain(dataFrame=data,object=m)
preds, evaluate = train.predict()
```

```python 
# If you want to make any other data predictions you can use the train.tester
# func after train.predict. You can make predictions with
predicts = train.tester(path="Data-SVR-2023-01-08-09-50-37.pkl", testData=data.iloc[:,1:][-20:])
```
