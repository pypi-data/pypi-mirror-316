import pandas as pd
import numpy as np
import statsmodels.api as sm
import re
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.preprocessing import StandardScaler
from scipy import stats
from sklearn.feature_selection import mutual_info_classif, mutual_info_regression
from sklearn.metrics import silhouette_score
import logging
from typing import Dict, List, Tuple, Union, Optional,Any
import warnings
from datetime import datetime


class ModelSelection:
    def __init__(self, data):
        self.data = data
        self.num_samples, self.num_features = self.data.shape
        self.features = self.data.columns
        self.feature_types = self.analyze_data()

    def analyze_data(self):
        feature_types = {}

        for feature in self.features:
            feature_type = self.determine_feature_type(feature)
            feature_types[feature] = feature_type

        return feature_types

    def is_categorical_feature(self, feature):
        sample_values = self.data[feature].head(100)
        string_values = [value for value in sample_values if isinstance(value, str)]
        if len(string_values) >= 90:
            return True
        return False

    def is_numeric_feature(self, feature):
        dtype = self.data[feature].dtype

        try:
            if np.issubdtype(dtype, np.number):
                return True
        except:pass

        valid_dtypes = [np.int_, np.float_, np.int32, np.int64, np.float32, np.float64]
        if dtype in valid_dtypes:
            return True

        return False

    def is_text_feature(self, feature):
        sample_values = self.data[feature].head(100)
        text_values = [value for value in sample_values if isinstance(value, str) and len(value.split()) > 2]
        return len(text_values) >= 10

    def determine_feature_type(self, feature):
        if self.is_time_series_feature(feature):
            return "time_series"
        elif self.is_categorical_feature(feature):
            return "categorical"
        elif self.is_numeric_feature(feature):
            return "numeric"
        elif self.is_text_feature(feature):
            return "text"
        else:
            return "unknown"

    def is_time_series_feature(self, feature):
        time_formats = [
            r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}",  # yyyy-mm-dd hh:mm:ss
            r"\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}",  # mm-dd-yyyy hh:mm:ss
            r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}",        # yyyy-mm-dd hh:mm
            r"\d{2}-\d{2}-\d{4} \d{2}:\d{2}",        # mm-dd-yyyy hh:mm
            r"\d{4}-\d{2}-\d{2}",                    # yyyy-mm-dd
            r"\d{2}-\d{2}-\d{4}",                    # mm-dd-yyyy
            r"\d{2}:\d{2}:\d{2}",                    # hh:mm:ss
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}",  # ISO 8601 format
        ]

        values = self.data[feature].head(100)
        if any(re.match(pattern, str(value)) for pattern in time_formats for value in values):
            return True
        return False

    def apply_dimensionality_reduction(self, X, y=None):
        num_samples, num_features = X.shape

        pca = PCA(n_components=num_features)
        pca_X = pca.fit_transform(X)
        explained_variance_ratio_pca = pca.explained_variance_ratio_

        if y is not None:
            lda = LinearDiscriminantAnalysis(n_components=min(num_samples, num_features))
            lda_X = lda.fit_transform(X, y)
            explained_variance_ratio_lda = lda.explained_variance_ratio_
        else:
            lda_X = None
            explained_variance_ratio_lda = None

        return pca_X, explained_variance_ratio_pca, lda_X, explained_variance_ratio_lda

    def analyze_dimensionality_reduction(self, pca_explained_variance, lda_explained_variance):
        results = []

        if pca_explained_variance is not None:
            if sum(pca_explained_variance) < 0.95:
                results.append("PCA may be recommended (95% of variance not explained).")

        if lda_explained_variance is not None:
            if sum(lda_explained_variance) < 0.95:
                results.append("LDA application may be recommended (95% of variance not explained).")

        if len(results) == 0:
            return "Size reduction is not recommended."


    def is_seasonal(self ):

        self.data['mean'] = self.data.mean(axis=1)
        decomposition = sm.tsa.seasonal_decompose(self.data['mean'], model='additive')
        if decomposition.seasonal.abs().mean() < 0.01:
            return 'Seasonality not detected'
        else:
            return 'Seasonality detected'

    def is_symmetric_data(self):
        correlation_matrix = self.data.corr()
        is_symmetric = (correlation_matrix == correlation_matrix.T).all().all()

        return is_symmetric

    def has_spatial_temporal_patterns(self):
        # Mekansal ve zamansal desen analizi yapın
        # Örnek olarak basit bir desen analizi yapılıyor
        # Bu fonksiyonu istediğiniz şekilde daha kapsamlı hale getirebilirsiniz

        # Örnek: Verinin ilk ve son yarısını iki parçaya ayırın
        half1 = self.data.iloc[:self.num_samples // 2]
        half2 = self.data.iloc[self.num_samples // 2:]

        # Basit bir desen analizi, ilk yarı verisinin ortalamasını alın ve ikinci yarıdaki değerlerle karşılaştırın
        pattern_detected = (half2.mean() > half1.mean()).all()

        return pattern_detected

    def has_irregular_heterogeneous_data(self):
        # Düzensiz ve heterojen veri analizi yapın
        # Örnek olarak basit bir analiz yapılıyor
        # Bu fonksiyonu istediğiniz şekilde daha kapsamlı hale getirebilirsiniz

        # Örnek: Verinin standart sapması düşükse (homojen) veya veri aralığı büyükse (heterojen) öneri yapın
        std_threshold = 0.5  # Düşük standart sapma için eşik değeri
        range_threshold = 1000  # Büyük veri aralığı için eşik değeri

        std = self.data.std()
        data_range = self.data.max() - self.data.min()

        is_irregular_heterogeneous = (std < std_threshold).any() or (data_range > range_threshold).any()

        return is_irregular_heterogeneous


    def analyze_stationarity_autocorrelation(self):

        adf_results = []
        for feature in self.data.columns:
            adf_result = sm.tsa.adfuller(self.data[feature])
            adf_results.append((feature, adf_result[1]))
        non_stationary_features = [feature for feature, p_value in adf_results if p_value > 0.05]

        autocorrelation_results = []
        for feature in self.data.columns:
            autocorrelation = sm.tsa.acf(self.data[feature])
            significant_lags = sum(1 for lag in range(1, len(autocorrelation)) if autocorrelation[lag] > 0.2)
            autocorrelation_results.append((feature, significant_lags))
        high_autocorrelation_features = [feature for feature, lags in autocorrelation_results if lags > 0]
        return non_stationary_features, high_autocorrelation_features


    def analyze_algorithm_feasibility(self, algorithm_name, time_series_column):

        if algorithm_name == "LSTM":
            if self.num_samples >= 1000:
                return True, "Suitable dataset size, LSTM can be used."
            else:
                return False, "Insufficient dataset size, LSTM is not recommended."
        elif algorithm_name == "LSTNET":
            if self.num_samples >= 5000:
                return True, "If the dataset size is appropriate, LSTNet can be used."
            else:
                return False, "Insufficient dataset size, LSTNet is not recommended."
        elif algorithm_name == "TCN":
            if time_series_column.__len__() != 0:
                return True, "There are temporal dependencies, TCN can be used."
            else:
                return False, "No temporal dependencies, TCN is not recommended."
        elif algorithm_name == "BILSTM":
            if self.is_symmetric_data():
                return True, "Data symmetric, BILSTM is available."
            else:
                return False, "Data is not symmetric, BILSTM is not recommended."
        elif algorithm_name == "CONVLSTM":
            if self.has_spatial_temporal_patterns():
                return True, "There are spatial and temporal patterns, CONVLSTM can be used."
            else:
                return False, "No spatial and temporal patterns, CONVLSTM is not recommended."
        elif algorithm_name == "XGBoost":
            if self.has_irregular_heterogeneous_data():
                return True, "If you have irregular and heterogeneous data, XGBoost can be used."
            else:
                return False, "No irregular and heterogeneous data, XGBoost is not recommended."
        elif algorithm_name == "ARIMA":
            if time_series_column.__len__() != 0:
                non_stationary_features, high_autocorrelation_features = self.analyze_stationarity_autocorrelation()
                if time_series_column[0] in non_stationary_features:
                    return f"Data is not static, {algorithm_name} is not recommended."
                elif time_series_column[0] in high_autocorrelation_features:
                    return False, f"High autocorrelation detected, {algorithm_name} is not recommended."
                else:
                    return True, f"If the data are stationary and autocorrelation properties are appropriate, {algorithm_name} can be used."
        elif algorithm_name in ["SARIMA", "PROPHET"]:
            if time_series_column.__len__() != 0:
                if self.is_seasonal():
                    return True, f"Seasonality detected, {algorithm_name} can be used."
                else:
                    return False, f"Seasonality not detected, {algorithm_name} is not recommended."
            else:
                return False, f"No time series data found, {algorithm_name} is not recommended."
        else:
            return False, "The specified algorithm was not found."


    def select_model(self):

        selected_models = []

        feature_types = self.analyze_data()

        if not feature_types:
            return "Data type could not be determined."

        numeric_features = [feature for feature, feature_type in feature_types.items() if feature_type == "numeric"]
        categorical_features = [feature for feature, feature_type in feature_types.items() if feature_type == "categorical"]
        text_features = [feature for feature, feature_type in feature_types.items() if feature_type == "text"]
        time_series_column = [feature for feature, feature_type in feature_types.items() if feature_type == "time_series"]

        # mevsimsellik durumu için
        if time_series_column.__len__() > 0:
            self.data[time_series_column] = self.data[time_series_column].apply(lambda x: pd.to_datetime(x))
            self.data = self.data.set_index(time_series_column)

        pca_X, pca_explained_variance, lda_X, lda_explained_variance = self.apply_dimensionality_reduction(self.data)
        dimensionality_reduction_results = self.analyze_dimensionality_reduction(pca_explained_variance, lda_explained_variance)

        time_series_models = {
            "ARIMA": 5,
            "SARIMA": 4,
            "PROPHET": 3,
            "LSTM": 2,
            "LSTNET": 1,
            "TCN": 2,
            "BILSTM": 3,
            "CONVLSTM": 1,
            "XGBoost": 4
        }


        text_analysis_models = [
            "CNN (Convolutional Neural Network)",
            "RNN (Recurrent Neural Network)",
            "LSTM (Long Short-Term Memory)",
            "Transformer",
            "BERT (Bidirectional Encoder Representations from Transformers)",
            "GPT (Generative Pre-trained Transformer)"
        ]

        other_models = [
            "Clustering Models",
            "Dimensionality Reduction (PCA, t-SNE)",
            "Ensemble Models",
            "Recommendation Systems",
            "Anomaly Detection Models"
        ]

        algorithm_results = []
        for algorithm in time_series_models:
            algorithm_feasibility = self.analyze_algorithm_feasibility(algorithm, time_series_column)
            if algorithm_feasibility != None:
                if algorithm_feasibility[0]:
                    algorithm_results.append((algorithm, algorithm_feasibility[0],algorithm_feasibility[1]))
                else:
                    algorithm_results.append((algorithm, algorithm_feasibility[0],algorithm_feasibility[1]))

        algorithm_results = sorted(algorithm_results, key=lambda x: x[1], reverse=True)
        # Algoritma sonuçlarını popülerlik sırasına ve kullanılabilirlik durumuna göre sıralayın

        # Diğer model analizlerini burada yapın ve algorithm_results listesine ekleyin
        # ...

        selected_models.extend([(x[0], x[2]) for x in algorithm_results])

        #if time_series_column and numeric_features:
        #    selected_models.extend(time_series_models)
#
        #if time_series_column and categorical_features:
        #    selected_models.extend(time_series_models)
#
        #if numeric_features:
        #    selected_models.extend(regression_models)
#
        #if categorical_features:
        #    selected_models.extend(classification_models)

        if text_features:
            selected_models.extend(text_analysis_models)

        # Diğer durumları ve özellikleri buraya ekleyebilirsiniz
        if not selected_models:
            selected_models = ["General Situation"]

        print("\nDimension Reduction Analysis:",dimensionality_reduction_results)
        print("\nSelected Models:")
        for idx, model in enumerate(selected_models, start=1):
            print(f"{idx}. {model}")













###############################################################################################


def print_table(headers, rows):
    max_lengths = [len(header) for header in headers]
    for row in rows:
        max_lengths = [max(len(str(item)), max_len) for item, max_len in zip(row, max_lengths)]

    header_line = " | ".join(f"{header:<{max_len}}" for header, max_len in zip(headers, max_lengths))
    separator_line = "-+-".join("-" * max_len for max_len in max_lengths)

    print(header_line)
    print(separator_line)
    for row in rows:
        row_line = " | ".join(f"{str(item):<{max_len}}" for item, max_len in zip(row, max_lengths))
        print(row_line)

def remove_duplicates(models):
    unique_models = {tuple(model.items()): model for model in models}
    return list(unique_models.values())

def display_recommendations(output_data):
    print("\nDataset Summary:\n")
    dataset_summary = output_data.get('dataset_summary', {})
    if dataset_summary:
        print_table(["Key", "Value"], dataset_summary.items())
    else:
        print("No dataset summary.")

    print("\nData Quality:\n")
    data_quality = output_data.get('data_quality', {})
    for feature, metrics in data_quality.items():
        print(f"\nFeature: {feature}\n")
        print_table(["Metric", "Value"], metrics.items())

    print("\nFeature Relationships:\n")
    feature_relationships = output_data.get('feature_relationships', {})
    high_corrs = feature_relationships.get('high_correlations', [])
    if high_corrs:
        print_table(["Feature 1", "Feature 2", "Correlation"], high_corrs)
    else:
        print("No high correlations.")

    print("\nRecommendations:\n")
    recommendations = output_data.get('recommendations', {})

    print("\nPrimary Recommendations:\n")
    primary_recommendations = remove_duplicates(recommendations.get('primary_recommendations', []))
    if primary_recommendations:
        print_table(["Model Name", "Evaluation Score"], [(model['name'], model.get('evaluation_score', model.get('fit_score', 'N/A'))) for model in primary_recommendations])
    else:
        print("No primary recommendations.")

    print("\nAlternative Recommendations:\n")
    alternative_recommendations = remove_duplicates(recommendations.get('alternative_recommendations', []))
    if alternative_recommendations:
        print_table(["Model Name", "Evaluation Score"], [(model['name'], model.get('evaluation_score', model.get('fit_score', 'N/A'))) for model in alternative_recommendations])
    else:
        print("No alternative recommendations.")

    print("\nWarnings:\n")
    warnings = recommendations.get('warnings', [])
    if warnings:
        print_table(["Warning"], [(warning,) for warning in warnings])
    else:
        print("No warnings.")

    print("\nPreprocessing Steps:\n")
    preprocessing_steps = recommendations.get('preprocessing_steps', [])
    if preprocessing_steps:
        print_table(["Step", "Methods", "Priority"], [(step['step'], ", ".join(step['methods']), step['priority']) for step in preprocessing_steps])
    else:
        print("No preprocessing steps.")

    print("\nRegression Recommendations:\n")
    regression_recommendations = remove_duplicates(recommendations.get('regression_recommendations', []))
    if regression_recommendations:
        print_table(["Model Name", "Evaluation Score"], [(model['name'], model.get('evaluation_score', model.get('fit_score', 'N/A'))) for model in regression_recommendations])
    else:
        print("No regression recommendations.")

    print("\nUnsupervised Learning Recommendations:\n")
    unsupervised_recommendations = recommendations.get('unsupervised_recommendations', [])
    for recommendation in unsupervised_recommendations:
        task = recommendation['task']
        models = remove_duplicates(recommendation['models'])
        print(f"\nTask: {task}\n")
        print_table(["Model Name", "Evaluation Score"], [(model['name'], model.get('evaluation_score', model.get('fit_score', 'N/A'))) for model in models])

    print("\nExecution Log:\n")
    execution_log = output_data.get('execution_log', [])
    if execution_log:
        print_table(["Log"], [(log,) for log in execution_log])
    else:
        print("No execution log.")



class DataValidationError(Exception):
    """Custom exception for data validation errors"""
    pass

class ModelSelectionError(Exception):
    """Custom exception for model selection errors"""
    pass

class ModelSelectionML:
    """
    A comprehensive class for analyzing datasets and recommending appropriate machine learning models.
    
    Attributes:
        data (pd.DataFrame): Input dataset
        target_column (str): Name of the target column for supervised learning
        logger (logging.Logger): Logger instance for tracking operations
        feature_types (dict): Dictionary mapping features to their types
        analysis_results (dict): Dictionary storing all analysis results
    """

    def __init__(self, data: pd.DataFrame, target_column: Optional[str] = None, 
                 log_level: int = logging.INFO):
        """
        Initialize ModelSelection with data validation and logging setup.
        
        Args:
            data: Input DataFrame
            target_column: Target variable name (optional)
            log_level: Logging level (default: INFO)
        
        Raises:
            DataValidationError: If data validation fails
        """
        self._setup_logging(log_level)
        self.logger.info(f"Initializing ModelSelection at {datetime.now()}")
        
        try:
            self._validate_input_data(data)
            self.data = data.copy()
            self.target_column = target_column
            self.num_samples, self.num_features = self.data.shape
            self.features = self.data.columns
            self.analysis_results = {}
            
            # Initialize feature types with validation
            self.feature_types = self._analyze_data_with_validation()
            
            self.logger.info(f"Successfully initialized with {self.num_samples} samples and {self.num_features} features")
            
        except Exception as e:
            self.logger.error(f"Initialization failed: {str(e)}")
            raise DataValidationError(f"Failed to initialize ModelSelection: {str(e)}")

    def _setup_logging(self, log_level: int) -> None:
        """Setup logging configuration"""
        self.logger = logging.getLogger(f'ModelSelection_{id(self)}')
        self.logger.setLevel(log_level)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def _validate_input_data(self, data: pd.DataFrame) -> None:
        """
        Validate input data for common issues.
        
        Raises:
            DataValidationError: If validation fails
        """
        if not isinstance(data, pd.DataFrame):
            raise DataValidationError("Input must be a pandas DataFrame")
        
        if data.empty:
            raise DataValidationError("DataFrame is empty")
            
        if data.isnull().values.any():
            self.logger.warning("DataFrame contains missing values")
            
        if data.select_dtypes(include=['object']).apply(lambda x: x.str.contains('^\s*$')).any().any():
            self.logger.warning("DataFrame contains empty strings or whitespace")


    def _analyze_data_with_validation(self) -> Dict[str, str]:
        """
        Analyze and validate data types with error handling.
        
        Returns:
            Dictionary mapping features to their types
        """
        feature_types = {}
        
        for feature in self.features:
            try:
                feature_type = self._determine_feature_type_safe(feature)
                feature_types[feature] = feature_type
                self.logger.debug(f"Feature '{feature}' classified as {feature_type}")
                
            except Exception as e:
                self.logger.warning(f"Error analyzing feature '{feature}': {str(e)}")
                feature_types[feature] = "unknown"
                
        return feature_types
    
    def _is_time_series_feature(self, feature):
        time_formats = [
            r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}",  # yyyy-mm-dd hh:mm:ss
            r"\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}",  # mm-dd-yyyy hh:mm:ss
            r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}",        # yyyy-mm-dd hh:mm
            r"\d{2}-\d{2}-\d{4} \d{2}:\d{2}",        # mm-dd-yyyy hh:mm
            r"\d{4}-\d{2}-\d{2}",                    # yyyy-mm-dd
            r"\d{2}-\d{2}-\d{4}",                    # mm-dd-yyyy
            r"\d{2}:\d{2}:\d{2}",                    # hh:mm:ss
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}",  # ISO 8601 format
        ]

    def _is_time_series_feature_enhanced(self, feature: str) -> bool:
        """Enhanced datetime detection"""
        try:
            series = self.data[feature]
            
            # Check if already datetime
            if pd.api.types.is_datetime64_any_dtype(series):
                return True
            
            # Check column name patterns
            time_related_patterns = [
                r'date', r'time', r'year', r'month', r'day', 
                r'timestamp', r'period', r'datetime'
            ]
            if any(re.search(pattern, feature.lower()) for pattern in time_related_patterns):
                # Try parsing a sample
                sample = series.dropna().head(1).iloc[0]
                try:
                    pd.to_datetime(sample)
                    return True
                except:
                    pass
            
            # Extended datetime pattern matching
            time_formats = [
                # Standard datetime formats
                r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
                r'\d{2}-\d{2}-\d{4}',  # DD-MM-YYYY
                r'\d{2}/\d{2}/\d{4}',  # DD/MM/YYYY
                r'\d{4}/\d{2}/\d{2}',  # YYYY/MM/DD
                r'\d{2}\.\d{2}\.\d{4}',  # DD.MM.YYYY
                r'\d{4}\.\d{2}\.\d{2}',  # YYYY.MM.DD
                
                # With time
                r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}',  # YYYY-MM-DD HH:MM
                r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',  # YYYY-MM-DD HH:MM:SS
                r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}',  # ISO format
                
                # Other common formats
                r'\d{2}-[A-Za-z]{3}-\d{4}',  # DD-Mon-YYYY
                r'[A-Za-z]{3} \d{2}, \d{4}',  # Mon DD, YYYY
                
                # Fiscal/Quarter patterns
                r'FY\d{2}Q[1-4]',  # Fiscal year quarters
                r'Q[1-4] \d{4}',  # Calendar quarters
            ]
            
            # Check if any of the patterns match
            sample_values = series.dropna().head(100)
            if any(re.match(pattern, str(value)) for value in sample_values for pattern in time_formats):
                return True

            # Additional fallback check
            values = self.data[feature].head(100)
            if any(re.match(pattern, str(value)) for pattern in time_formats for value in values):
                return True
    
        except Exception as e:
            self.logger.debug(f"Time series check failed for {feature}: {str(e)}")
            return False


    
    def _is_categorical_feature(self, feature):
        sample_values = self.data[feature].head(100)
        string_values = [value for value in sample_values if isinstance(value, str)]
        if len(string_values) >= 90:
            return True
        return False
    
    def _is_categorical_feature_enhanced(self, feature: str) -> bool:
        """Enhanced categorical type detection"""
        try:
            series = self.data[feature]
            n_unique = series.nunique()
            n_samples = len(series)
            
            # Check if already categorical
            if pd.api.types.is_categorical_dtype(series):
                return True
            
            # If very few unique values compared to sample size, likely categorical
            if n_unique < min(50, n_samples * 0.05):  # 5% threshold
                return True
            
            # Check for common categorical patterns
            sample_values = series.dropna().head(100)
            
            # Common categorical patterns
            categorical_patterns = [
                r'^[A-Za-z ]+$',  # Words only
                r'^(high|medium|low)$',  # Common ratings
                r'^(yes|no)$',  # Yes/No
                r'^(true|false)$',  # True/False
                r'^[A-F]{1}[+-]?$',  # Grades
                r'^(good|bad|neutral)$',  # Sentiments
                r'^(north|south|east|west)$',  # Directions
                r'^(small|medium|large|xl|xxl)$',  # Sizes
            ]
            
            # Check if values match categorical patterns
            pattern_matches = sum(1 for val in sample_values if isinstance(val, str) and
                                any(re.match(pattern, val.lower()) for pattern in categorical_patterns))
            
            if pattern_matches >= len(sample_values) * 0.8:  # 80% threshold
                return True
            
            return False
        
        except Exception as e:
            self.logger.debug(f"Categorical check failed for {feature}: {str(e)}")
            return False

    def _is_numeric_feature(self, feature):
        dtype = self.data[feature].dtype

        try:
            if np.issubdtype(dtype, np.number):
                return True
        except:pass

        valid_dtypes = [np.int_, np.float_, np.int32, np.int64, np.float32, np.float64]
        if dtype in valid_dtypes:
            return True

        return False

    def _is_text_feature(self, feature):
        sample_values = self.data[feature].head(100)
        text_values = [value for value in sample_values if isinstance(value, str) and len(value.split()) > 2]
        return len(text_values) >= 10
    

    def _is_text_feature_enhanced(self, feature: str) -> bool:
        """Enhanced text type detection"""
        try:
            series = self.data[feature]
            sample_values = series.dropna().head(100)
            
            # Check if strings with significant length
            text_values = [val for val in sample_values if isinstance(val, str) and 
                         len(val.split()) > 2]  # More than 2 words
            
            # Check average word length and character count
            if text_values:
                avg_words = np.mean([len(str(val).split()) for val in text_values])
                avg_chars = np.mean([len(str(val)) for val in text_values])
                
                # Likely text if on average > 3 words and > 15 characters
                return len(text_values) >= len(sample_values) * 0.5 and avg_words > 3 and avg_chars > 15
            
            return False
            
        except Exception as e:
            self.logger.debug(f"Text check failed for {feature}: {str(e)}")
            return False
        
    
    def _calculate_outliers_ratio(self, feature):
        Q1 = self.data[feature].quantile(0.25)
        Q3 = self.data[feature].quantile(0.75)
        IQR = Q3 - Q1
        outliers = ((self.data[feature] < (Q1 - 1.5 * IQR)) | (self.data[feature] > (Q3 + 1.5 * IQR))).mean()
        return outliers

    def _determine_feature_type_safe(self, feature: str) -> str:
        """
        Enhanced feature type detection with comprehensive checks.
        
        Args:
            feature: Feature name to analyze
            
        Returns:
            String indicating feature type
        """
        try:
            series = self.data[feature]
            
            # Handle completely empty columns
            if series.isna().all():
                self.logger.warning(f"Feature '{feature}' is completely empty")
                return "empty"
                
            # Get non-null values for analysis
            non_null_values = series.dropna()
            if len(non_null_values) == 0:
                return "empty"
                
            # Get sample values for analysis
            sample_values = non_null_values.head(100)
            
            # Check for datetime first
            if self._is_time_series_feature_enhanced(feature):
                return "time_series"
            
            # Check if binary
            unique_values = set(non_null_values.unique())
            if len(unique_values) == 2:
                # Check if boolean
                if unique_values == {0, 1} or unique_values == {True, False} or \
                   unique_values == {'0', '1'} or unique_values == {'true', 'false'} or \
                   unique_values == {'True', 'False'} or unique_values == {'yes', 'no'} or \
                   unique_values == {'Y', 'N'} or unique_values == {'t', 'f'}:
                    return "binary"
            
            # Check if numeric with extended checks
            if self._is_numeric_feature_enhanced(feature):
                if len(unique_values) < 10 and self.num_samples > 100:
                    return "categorical_numeric"  # For numeric categories like ratings 1-5
                return "numeric"
            
            # Check if categorical with enhanced logic
            if self._is_categorical_feature_enhanced(feature):
                return "categorical"
            
            # Check if text
            if self._is_text_feature_enhanced(feature):
                return "text"
            
            # Check if ID column
            if self._is_id_feature(feature):
                return "id"
            
            # Check if percentage
            if self._is_percentage_feature(feature):
                return "percentage"
            
            # Check if currency
            if self._is_currency_feature(feature):
                return "currency"
            
            # Check common column patterns
            common_patterns = self._check_common_column_patterns(feature)
            if common_patterns:
                return common_patterns
            
            # If still unknown, try to make an educated guess
            return self._make_educated_guess(feature)
            
        except Exception as e:
            self.logger.error(f"Error determining type for feature '{feature}': {str(e)}")
            return self._make_educated_guess(feature)
        except Exception as e:
            self.logger.error(f"Error determining type for feature '{feature}': {str(e)}")
            return "unknown"
        
    def _analyze_numeric_target(self) -> Dict[str, Any]:
        """Analyze numeric target variable statistics."""
        try:
            target_stats = {
                'mean': self.data[self.target_column].mean(),
                'median': self.data[self.target_column].median(),
                'std': self.data[self.target_column].std(),
                'min': self.data[self.target_column].min(),
                'max': self.data[self.target_column].max(),
                'skewness': float(stats.skew(self.data[self.target_column].dropna())),
                'kurtosis': float(stats.kurtosis(self.data[self.target_column].dropna())),
                'has_outliers': self._calculate_outliers_ratio(self.target_column) > 0.05,
                'linear_relationship': self._check_linear_relationship()
            }
            return target_stats
        except Exception as e:
            self.logger.error(f"Error analyzing numeric target: {str(e)}")
            return {}


    def _is_json_feature(self, feature: str) -> bool:
        """Check if feature contains JSON data"""
        try:
            sample = self.data[feature].dropna().head(1).iloc[0]
            if isinstance(sample, str):
                return bool(re.match(r'^\s*[{\[].*[}\]]\s*$', sample))
            return False
        except:
            return False

    def _is_coordinate_feature(self, feature: str) -> bool:
        """Check if feature contains coordinate data"""
        try:
            series = self.data[feature]
            if series.dtype == object:
                # Check for common coordinate patterns like "(lat, lon)" or "lat,lon"
                coord_pattern = r'^[-+]?\d*\.?\d+\s*[,;]\s*[-+]?\d*\.?\d+$'
                return series.str.match(coord_pattern).any()
            return False
        except:
            return False

    def analyze_data_quality(self) -> Dict[str, Dict]:
        """
        Perform comprehensive data quality analysis with improved error handling.
        
        Returns:
            Dictionary containing quality metrics for each feature
        """
        quality_metrics = {}
        
        try:
            for feature in self.features:
                metrics = {
                    'missing_ratio': float(self.data[feature].isnull().mean()),
                    'feature_type': self.feature_types[feature]
                }
                
                # Safely calculate unique ratio
                try:
                    unique_count = self.data[feature].nunique()
                    if pd.isna(unique_count):
                        metrics['unique_ratio'] = 0.0
                    else:
                        metrics['unique_ratio'] = float(unique_count) / len(self.data)
                except (TypeError, ValueError):
                    metrics['unique_ratio'] = 0.0
                    self.logger.warning(f"Could not calculate unique ratio for feature {feature}")
                
                # Only calculate statistical metrics for numeric features
                if self.feature_types[feature] == 'numeric':
                    try:
                        numeric_data = pd.to_numeric(self.data[feature], errors='coerce')
                        non_null_data = numeric_data.dropna()
                        
                        if len(non_null_data) > 0:
                            metrics.update({
                                'skewness': float(stats.skew(non_null_data)),
                                'kurtosis': float(stats.kurtosis(non_null_data)),
                                'outliers_ratio': self._calculate_outliers_ratio(feature)
                            })
                    except Exception as e:
                        self.logger.warning(f"Could not calculate statistical metrics for feature {feature}: {str(e)}")
                
                quality_metrics[feature] = metrics
                
            self.analysis_results['data_quality'] = quality_metrics
            return quality_metrics
            
        except Exception as e:
            self.logger.error(f"Error in data quality analysis: {str(e)}")
            raise ModelSelectionError(f"Failed to analyze data quality: {str(e)}")
        
    def _analyze_categorical_associations(self, cat_features: List[str]) -> Dict[str, Dict]:
        """
        Analyze associations between categorical features with improved error handling.
        """
        associations = {}
        for feature in cat_features:
            try:
                value_counts = self.data[feature].value_counts(normalize=True)
                associations[feature] = value_counts.to_dict()
            except Exception as e:
                self.logger.warning(f"Could not analyze categorical associations for feature {feature}: {str(e)}")
                associations[feature] = {}
        return associations
    
    def _analyze_categorical_target(self) -> Dict[str, Any]:
        """
        Analyze characteristics of a categorical or binary target variable.

        Returns:
            Dictionary containing key characteristics of the target variable.

        Raises:
            ModelSelectionError: If an error occurs during analysis.
        """
        try:
            if not self.target_column:
                raise ModelSelectionError("Target column is not defined.")

            target_series = self.data.get(self.target_column)

            # Ensure target series is valid and not empty
            if target_series is None:
                raise ModelSelectionError(f"Target column '{self.target_column}' not found.")
            if target_series.empty or target_series.isnull().all():
                raise ModelSelectionError("Target column is empty or contains only null values.")

            # Initialize analysis results
            target_analysis = {
                "unique_classes": target_series.nunique(),
                "class_distribution": {},
                "class_imbalance": "balanced",
                "mode": target_series.mode().iloc[0] if not target_series.mode().empty else None,
                "most_frequent_class_percentage": 0.0
            }

            # Calculate class distribution
            class_counts = target_series.value_counts(normalize=True).to_dict()
            target_analysis["class_distribution"] = class_counts

            # Identify class imbalance
            if len(class_counts) > 1:
                max_class_percentage = max(class_counts.values())
                target_analysis["most_frequent_class_percentage"] = max_class_percentage

                if max_class_percentage > 0.8:
                    target_analysis["class_imbalance"] = "severe"
                elif max_class_percentage > 0.6:
                    target_analysis["class_imbalance"] = "moderate"

            return target_analysis

        except KeyError:
            self.logger.error(f"Target column '{self.target_column}' not found in the dataset.")
            raise ModelSelectionError(f"Target column '{self.target_column}' not found.")

        except TypeError as e:
            self.logger.error(f"Type error in target analysis: {str(e)}")
            raise ModelSelectionError("Type error encountered during target analysis.")

        except ValueError as e:
            self.logger.error(f"Value error in target analysis: {str(e)}")
            raise ModelSelectionError("Value error encountered during target analysis.")

        except Exception as e:
            self.logger.error(f"Unexpected error during target analysis: {str(e)}")
            raise ModelSelectionError("Unexpected error encountered during target analysis.")

    
    def analyze_feature_relationships(self) -> Dict[str, Dict]:
        """
        Analyze relationships between features with enhanced handling for financial data.
        
        Returns:
            Dictionary containing relationship metrics
        """
        relationships = {}
        
        try:
            numeric_features = [f for f in self.features if self.feature_types[f] == 'numeric']
            
            if len(numeric_features) > 1:
                # Create preprocessed numeric DataFrame
                numeric_data = pd.DataFrame()
                for feature in numeric_features:
                    processed_series = self._preprocess_numeric_feature(feature)
                    if processed_series is not None:
                        numeric_data[feature] = processed_series
                
                # Remove features with all NULL values after preprocessing
                valid_features = numeric_data.columns[numeric_data.notna().any()].tolist()
                
                if len(valid_features) > 1:
                    # Correlation analysis
                    corr_matrix = numeric_data[valid_features].corr()
                    
                    # Find highly correlated features
                    high_corr_pairs = []
                    for i in range(len(valid_features)):
                        for j in range(i+1, len(valid_features)):
                            correlation = corr_matrix.iloc[i,j]
                            if pd.notna(correlation) and abs(correlation) > 0.8:
                                high_corr_pairs.append((
                                    valid_features[i],
                                    valid_features[j],
                                    correlation
                                ))
                    
                    relationships['high_correlations'] = high_corr_pairs
                    
                # Log features that were excluded
                excluded_features = set(numeric_features) - set(valid_features)
                if excluded_features:
                    self.logger.warning(f"Features excluded from correlation analysis due to invalid values: {excluded_features}")
            
            # Categorical relationships
            cat_features = [f for f in self.features if self.feature_types[f] in ['categorical', 'binary']]
            if len(cat_features) > 1:
                relationships['categorical_associations'] = self._analyze_categorical_associations(cat_features)
                
            self.analysis_results['feature_relationships'] = relationships
            return relationships
            
        except Exception as e:
            self.logger.error(f"Error in feature relationship analysis: {str(e)}")
            raise ModelSelectionError(f"Failed to analyze feature relationships: {str(e)}")

    def analyze_target_characteristics(self) -> Dict[str, Any]:
        """
        Analyze characteristics of the target variable for supervised learning.
        
        Returns:
            Dictionary containing target variable characteristics
        """
        if not self.target_column:
            return {}
            
        target_chars = {}
        
        try:
            target_type = self.feature_types[self.target_column]
            
            if target_type == 'numeric':
                target_chars.update(self._analyze_numeric_target())
            elif target_type in ['categorical', 'binary']:
                target_chars.update(self._analyze_categorical_target())
            
            self.analysis_results['target_characteristics'] = target_chars
            return target_chars
            
        except Exception as e:
            self.logger.error(f"Error in target analysis: {str(e)}")
            raise ModelSelectionError("Failed to analyze target variable")

    def get_model_recommendations(self) -> Dict[str, List[Dict]]:
        """
        Get comprehensive model recommendations based on all analyses.
        
        Returns:
            Dictionary containing model recommendations for different tasks
        """
        recommendations = {
            'primary_recommendations': [],
            'alternative_recommendations': [],
            'warnings': [],
            'preprocessing_steps': []
        }
        
        try:
            # Run all necessary analyses if not already done
            if not self.analysis_results.get('data_quality'):
                self.analyze_data_quality()
            if not self.analysis_results.get('feature_relationships'):
                self.analyze_feature_relationships()
            if not self.analysis_results.get('target_characteristics'):
                self.analyze_target_characteristics()
                
            # Get task-specific recommendations
            if self.target_column:
                target_type = self.feature_types[self.target_column]
                
                if target_type in ['categorical', 'binary']:
                    recommendations.update(self._get_classification_recommendations())
                elif target_type == 'numeric':
                    recommendations.update(self._get_regression_recommendations())
            
            # Get unsupervised learning recommendations
            recommendations.update(self._get_unsupervised_recommendations())
            
            # Add preprocessing recommendations
            recommendations['preprocessing_steps'] = self._get_preprocessing_recommendations()
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error generating model recommendations: {str(e)}")
            raise ModelSelectionError("Failed to generate model recommendations")

    def _get_classification_recommendations(self) -> Dict[str, List[Dict]]:
        """Get classification model recommendations based on dataset analysis."""
        recommendations = []
        target_chars = self.analysis_results.get('target_characteristics', {})

        # Base models to consider based on analysis
        models = {
            'balanced_data': [
                {'name': 'Random Forest', 'fit_score': 0.85},
                {'name': 'XGBoost', 'fit_score': 0.9},
                {'name': 'LightGBM', 'fit_score': 0.88},
                {'name': 'Logistic Regression', 'fit_score': 0.8},
                {'name': 'SVM', 'fit_score': 0.78},
                {'name': 'Gradient Boosting', 'fit_score': 0.87},
                {'name': 'CatBoost', 'fit_score': 0.89},
                {'name': 'Neural Network (MLP)', 'fit_score': 0.9},
                {'name': 'K-Nearest Neighbors (KNN)', 'fit_score': 0.75},
                {'name': 'Decision Tree', 'fit_score': 0.7},
                {'name': 'AdaBoost', 'fit_score': 0.77},
                {'name': 'Stacking Classifier', 'fit_score': 0.86}
            ],
            'imbalanced_data': [
                {'name': 'XGBoost', 'fit_score': 0.92},
                {'name': 'Random Forest with class_weight', 'fit_score': 0.88},
                {'name': 'LightGBM with class_weight', 'fit_score': 0.9},
                {'name': 'Balanced Bagging Classifier', 'fit_score': 0.85},
                {'name': 'SMOTE + Logistic Regression', 'fit_score': 0.83},
                {'name': 'SMOTE + Random Forest', 'fit_score': 0.87},
                {'name': 'Balanced Random Forest', 'fit_score': 0.86},
                {'name': 'EasyEnsemble Classifier', 'fit_score': 0.84}
            ],
            'high_dimensional': [
                {'name': 'LightGBM', 'fit_score': 0.9},
                {'name': 'Linear SVM', 'fit_score': 0.78},
                {'name': 'ElasticNet Classifier', 'fit_score': 0.75},
                {'name': 'Ridge Classifier', 'fit_score': 0.77},
                {'name': 'SGD Classifier', 'fit_score': 0.76}
            ]
        }

        # Evaluate dataset characteristics
        class_imbalance = target_chars.get('class_imbalance')
        unique_classes = target_chars.get('unique_classes', 0)
        num_samples = self.num_samples
        balanced_accuracy = target_chars.get('balanced_accuracy', 0)

        # Select models based on dataset analysis
        if class_imbalance == 'severe':
            recommendations.extend(models['imbalanced_data'])
        elif self.num_features > 100 or unique_classes > 20:
            recommendations.extend(models['high_dimensional'])
        else:
            recommendations.extend(models['balanced_data'])

        # Adjust recommendations based on specific scenarios
        if unique_classes > 10:
            recommendations.append({'name': 'Neural Network (MLP)', 'fit_score': 0.9})
        elif unique_classes == 2:
            recommendations.append({'name': 'Logistic Regression', 'fit_score': 0.8})

        # Evaluate numeric-categorical feature balance
        num_numeric_features = sum(1 for f in self.features if self.feature_types[f] == 'numeric')
        num_categorical_features = sum(1 for f in self.features if self.feature_types[f] == 'categorical')

        if num_numeric_features / max(num_categorical_features, 1) > 2:
            recommendations.append({'name': 'Gradient Boosting', 'fit_score': 0.87})
        elif num_categorical_features / max(num_numeric_features, 1) > 2:
            recommendations.append({'name': 'CatBoost', 'fit_score': 0.89})

        # Consider dataset size for model complexity
        if num_samples < 1000:
            recommendations = [model for model in recommendations if model['name'] not in ['Neural Network (MLP)']]

        # Add extra scoring-based priority boost
        if balanced_accuracy < 0.7:
            recommendations.insert(0, {'name': 'XGBoost', 'fit_score': 0.92})

        # Evaluate model performance metrics after training
        if hasattr(self, 'model_evaluation_scores'):
            model_scores = self.model_evaluation_scores
            recommendations = [
                {**model, 'evaluation_score': model_scores.get(model['name'], 0)}
                for model in recommendations
            ]
            recommendations.sort(key=lambda x: x['evaluation_score'], reverse=True)

        else:
            # Sort by fit_score if evaluation scores are unavailable
            recommendations = sorted(recommendations, key=lambda x: -x['fit_score'])

        return {'classification_recommendations': recommendations}
    


    def _get_regression_recommendations(self) -> Dict[str, List[Dict]]:
        """Get regression model recommendations based on dataset analysis."""
        recommendations = []
        target_chars = self.analysis_results.get('target_characteristics', {})

        # Base models to consider based on analysis
        models = {
            'linear': [
                {'name': 'Linear Regression', 'fit_score': 0.85},
                {'name': 'Ridge Regression', 'fit_score': 0.83},
                {'name': 'Lasso Regression', 'fit_score': 0.82},
                {'name': 'ElasticNet', 'fit_score': 0.8}
            ],
            'nonlinear': [
                {'name': 'XGBoost Regressor', 'fit_score': 0.9},
                {'name': 'Random Forest Regressor', 'fit_score': 0.88},
                {'name': 'LightGBM Regressor', 'fit_score': 0.89},
                {'name': 'CatBoost Regressor', 'fit_score': 0.87},
                {'name': 'Gradient Boosting Regressor', 'fit_score': 0.86}
            ],
            'robust': [
                {'name': 'Huber Regressor', 'fit_score': 0.8},
                {'name': 'RANSAC Regressor', 'fit_score': 0.75},
                {'name': 'TheilSen Regressor', 'fit_score': 0.78}
            ]
        }

        # Evaluate dataset characteristics
        linear_relationship = target_chars.get('linear_relationship', False)
        has_outliers = target_chars.get('has_outliers', False)
        balanced_accuracy = target_chars.get('balanced_accuracy', 0)
        num_samples = self.num_samples

        # Use a set to ensure unique model recommendations
        unique_recommendations = set()

        # Select models based on data characteristics
        if linear_relationship:
            unique_recommendations.update(tuple(model.items()) for model in models['linear'])
        if has_outliers:
            unique_recommendations.update(tuple(model.items()) for model in models['robust'])
        else:
            unique_recommendations.update(tuple(model.items()) for model in models['nonlinear'])

        # Convert back to list of dicts
        recommendations = [dict(model) for model in unique_recommendations]

        # Consider dataset size for model complexity
        if num_samples < 1000:
            recommendations = [model for model in recommendations if model['name'] not in ['XGBoost Regressor', 'Neural Network']]

        # Adjust priority based on performance
        if balanced_accuracy < 0.7:
            recommendations.insert(0, {'name': 'XGBoost Regressor', 'fit_score': 0.9})

        # Evaluate model performance metrics after training
        if hasattr(self, 'model_evaluation_scores'):
            model_scores = self.model_evaluation_scores
            recommendations = [
                {**model, 'evaluation_score': model_scores.get(model['name'], 0)}
                for model in recommendations
            ]
            recommendations.sort(key=lambda x: x['evaluation_score'], reverse=True)

        else:
            # Sort by fit_score if evaluation scores are unavailable
            recommendations = sorted(recommendations, key=lambda x: -x['fit_score'])

        return {'regression_recommendations': recommendations}



    def _get_unsupervised_recommendations(self) -> Dict[str, List[Dict]]:
        """Get unsupervised learning recommendations based on dataset analysis."""
        recommendations = []

        # Check for clustering potential
        if self._check_clustering_potential():
            recommendations.append({
                'task': 'clustering',
                'models': [
                    {'name': 'K-Means', 'fit_score': 0.85},
                    {'name': 'DBSCAN', 'fit_score': 0.83},
                    {'name': 'Hierarchical Clustering', 'fit_score': 0.82},
                    {'name': 'Gaussian Mixture', 'fit_score': 0.8},
                    {'name': 'Agglomerative Clustering', 'fit_score': 0.78},
                    {'name': 'Spectral Clustering', 'fit_score': 0.76}
                ]
            })

        # Check for dimensionality reduction potential
        if self.num_features > 10:
            recommendations.append({
                'task': 'dimensionality_reduction',
                'models': [
                    {'name': 'PCA', 'fit_score': 0.9},
                    {'name': 't-SNE', 'fit_score': 0.87},
                    {'name': 'UMAP', 'fit_score': 0.88}
                ]
            })

        # Check for anomaly detection potential
        if self._check_anomaly_detection_potential():
            recommendations.append({
                'task': 'anomaly_detection',
                'models': [
                    {'name': 'Isolation Forest', 'fit_score': 0.89},
                    {'name': 'Local Outlier Factor', 'fit_score': 0.87},
                    {'name': 'One-Class SVM', 'fit_score': 0.85},
                    {'name': 'Elliptic Envelope', 'fit_score': 0.8}
                ]
            })

        # Evaluate model performance metrics after training
        if hasattr(self, 'model_evaluation_scores'):
            for rec in recommendations:
                task_scores = self.model_evaluation_scores.get(rec['task'], {})
                rec['models'] = [
                    {**model, 'evaluation_score': task_scores.get(model['name'], model['fit_score'])}
                    for model in rec['models']
                ]
                rec['models'].sort(key=lambda x: x['evaluation_score'], reverse=True)

        return {'unsupervised_recommendations': recommendations}

    def _check_clustering_potential(self) -> bool:
        """Check if data is suitable for clustering"""
        try:
            numeric_features = [f for f in self.features if self.feature_types[f] == 'numeric']
            if len(numeric_features) < 2:
                return False
                
            # Check feature variance
            scaled_data = StandardScaler().fit_transform(self.data[numeric_features])
            variances = np.var(scaled_data, axis=0)
            
            return np.mean(variances) > 0.1
            
        except Exception as e:
            self.logger.warning(f"Error checking clustering potential: {str(e)}")
            return False
        
    def _check_linear_relationship(self) -> bool:
        """Check for linear relationships in the target variable."""
        corr_matrix = self.data.corr()
        target_corr = corr_matrix[self.target_column].drop(self.target_column, errors='ignore')
        max_corr = target_corr.abs().max() if not target_corr.empty else 0
        return max_corr > 0.7

    def _check_anomaly_detection_potential(self) -> bool:
        """Check if data is suitable for anomaly detection"""
        try:
            numeric_features = [f for f in self.features if self.feature_types[f] == 'numeric']
            if len(numeric_features) < 2:
                return False
                
            # Check for potential outliers using IQR method
            outlier_scores = []
            for feature in numeric_features:
                Q1 = self.data[feature].quantile(0.25)
                Q3 = self.data[feature].quantile(0.75)
                IQR = Q3 - Q1
                outlier_ratio = ((self.data[feature] < (Q1 - 1.5 * IQR)) | 
                               (self.data[feature] > (Q3 + 1.5 * IQR))).mean()
                outlier_scores.append(outlier_ratio)
                
            return max(outlier_scores) > 0.01
            
        except Exception as e:
            self.logger.warning(f"Error checking anomaly detection potential: {str(e)}")
            return False


    def _is_numeric_feature_enhanced(self, feature: str) -> bool:
        """Enhanced numeric type detection"""
        try:
            series = self.data[feature]
            
            # Check if already numeric
            if pd.api.types.is_numeric_dtype(series):
                return True
            
            # Try converting to numeric
            try:
                pd.to_numeric(series.dropna())
                return True
            except:
                pass
            
            # Check for string representations of numbers
            sample = series.dropna().head(100)
            numeric_pattern = r'^-?\d*\.?\d+$'  # Basic number pattern
            scientific_pattern = r'^-?\d*\.?\d+e[+-]\d+$'  # Scientific notation
            
            # Count how many values match numeric patterns
            numeric_count = sum(1 for val in sample if isinstance(val, str) and
                              (re.match(numeric_pattern, val.strip()) or
                               re.match(scientific_pattern, val.strip())))
            
            return numeric_count >= len(sample) * 0.9  # 90% threshold
            
        except Exception as e:
            self.logger.debug(f"Numeric check failed for {feature}: {str(e)}")
            return False
        
    def _get_preprocessing_recommendations(self) -> List[Dict]:
        """Get data preprocessing recommendations"""
        recommendations = []
        
        try:
            # Check for missing values
            if self.data.isnull().any().any():
                recommendations.append({
                    'step': 'missing_value_handling',
                    'methods': ['mean/median imputation', 'KNN imputation', 'iterative imputation'],
                    'priority': 1
                })
            
            # Check for scaling needs
            numeric_features = [f for f in self.features if self.feature_types[f] == 'numeric']
            if numeric_features:
                scales = self.data[numeric_features].max() - self.data[numeric_features].min()
                if (scales > 10).any():
                    recommendations.append({
                        'step': 'feature_scaling',
                        'methods': ['StandardScaler', 'MinMaxScaler', 'RobustScaler'],
                        'priority': 1
                    })
            
            # Check for encoding needs
            categorical_features = [f for f in self.features if self.feature_types[f] == 'categorical']
            if categorical_features:
                high_cardinality_features = [f for f in categorical_features 
                                           if self.data[f].nunique() > 10]
                if high_cardinality_features:
                    recommendations.append({
                        'step': 'categorical_encoding',
                        'methods': ['Target Encoding', 'Feature Hashing', 'Binary Encoding'],
                        'priority': 1
                    })
                else:
                    recommendations.append({
                        'step': 'categorical_encoding',
                        'methods': ['One-Hot Encoding', 'Label Encoding'],
                        'priority': 1
                    })
            
            # Check for feature selection needs
            if self.num_features > 50:
                recommendations.append({
                    'step': 'feature_selection',
                    'methods': ['SelectKBest', 'LASSO', 'Random Forest Importance'],
                    'priority': 2
                })
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error generating preprocessing recommendations: {str(e)}")
            return []

    def generate_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive analysis report.
        
        Returns:
            Dictionary containing all analysis results and recommendations
        """
        try:
            report = {
                'dataset_summary': {
                    'num_samples': self.num_samples,
                    'num_features': self.num_features,
                    'feature_types': self.feature_types,
                    'memory_usage': self.data.memory_usage(deep=True).sum(),
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                'data_quality': self.analyze_data_quality(),
                'feature_relationships': self.analyze_feature_relationships(),
                'target_analysis': self.analyze_target_characteristics() if self.target_column else None,
                'recommendations': self.get_model_recommendations(),
                'warnings': self._get_warnings(),
                'execution_log': self._get_execution_log()
            }
            
            display_recommendations(report)
            return report
            
            
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ModelSelectionError("Failed to generate analysis report")
        

        
    def _get_warnings(self) -> List[str]:
        """Collect all warnings and potential issues"""
        warnings = []
        
        try:
            # Data size warnings
            if self.num_samples < 100:
                warnings.append("Small dataset: Results may not be reliable")
            if self.num_samples > 1000000:
                warnings.append("Large dataset: Consider using distributed computing")
                
            # Missing value warnings
            missing_ratios = self.data.isnull().mean()
            high_missing = missing_ratios[missing_ratios > 0.2]
            if not high_missing.empty:
                warnings.append(f"High missing value ratio in features: {list(high_missing.index)}")
                
            # Feature warnings
            if len(self.features) > 100:
                warnings.append("High number of features: Consider dimensionality reduction")
                
            # Target warnings
            if self.target_column:
                target_chars = self.analysis_results.get('target_characteristics', {})
                if target_chars.get('class_imbalance') == 'severe':
                    warnings.append("Severe class imbalance detected in target variable")
                    
            return warnings
            
        except Exception as e:
            self.logger.error(f"Error generating warnings: {str(e)}")
            return ["Error collecting warnings"]

    def _get_execution_log(self) -> List[str]:
        """Get execution log messages"""
        if hasattr(self.logger, 'handler_list'):
            return [handler.format(record) for handler in self.logger.handlers 
                   for record in handler.records]
        return []
    
    def _preprocess_numeric_feature(self, feature: str) -> pd.Series:
        """
        Preprocess numeric feature with financial notation handling.
        
        Args:
            feature: Feature name
            
        Returns:
            Preprocessed series with numeric values
        """
        series = self.data[feature]
        if series.dtype == 'object':
            return series.apply(self._convert_financial_notation)
        return pd.to_numeric(series, errors='coerce')
    
    def _convert_financial_notation(self, value: str) -> float:
        """
        Convert financial notation (e.g., '2.30B', '500M', '10K') to float.
        
        Args:
            value: String value in financial notation
            
        Returns:
            Float value
        """
        try:
            if not isinstance(value, str):
                return float(value)
                
            # Remove any thousand separators
            value = value.replace(',', '')
            
            # Handle multiplier suffixes
            multipliers = {
                'B': 1e9,   # Billions
                'M': 1e6,   # Millions
                'K': 1e3,   # Thousands
                'T': 1e12   # Trillions
            }
            
            for suffix, multiplier in multipliers.items():
                if value.upper().endswith(suffix):
                    return float(value[:-1]) * multiplier
                    
            return float(value)
            
        except (ValueError, TypeError):
            return None

    def save_report(self, filepath: str) -> None:
        """
        Save analysis report to file.
        
        Args:
            filepath: Path to save the report
        """
        try:
            report = self.generate_report()
            
            if filepath.endswith('.json'):
                import json
                with open(filepath, 'w') as f:
                    json.dump(report, f, indent=4, default=str)
            elif filepath.endswith('.pkl'):
                import pickle
                with open(filepath, 'wb') as f:
                    pickle.dump(report, f)
            else:
                raise ValueError("Unsupported file format. Use .json or .pkl")
                
            self.logger.info(f"Report successfully saved to {filepath}")
            
        except Exception as e:
            self.logger.error(f"Error saving report: {str(e)}")
            raise ModelSelectionError(f"Failed to save report to {filepath}")

    def get_feature_importance(self) -> Dict[str, float]:
        """
        Calculate feature importance scores.
        
        Returns:
            Dictionary mapping features to importance scores
        """
        if not self.target_column:
            return {}
            
        try:
            numeric_features = [f for f in self.features if self.feature_types[f] == 'numeric']
            if not numeric_features:
                return {}
                
            X = self.data[numeric_features]
            y = self.data[self.target_column]
            
            # Standardize features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Calculate feature importance based on task type
            if self.feature_types[self.target_column] in ['categorical', 'binary']:
                importance_scores = mutual_info_classif(X_scaled, y)
            else:
                importance_scores = mutual_info_regression(X_scaled, y)
                
            return dict(zip(numeric_features, importance_scores))
            
        except Exception as e:
            self.logger.error(f"Error calculating feature importance: {str(e)}")
            return {}
        




# Previous imports remain the same
import numpy as np
import pandas as pd
from datetime import datetime
import json
import tensorflow as tf
from scipy import stats
import sys
import psutil
import gc
import re
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
import warnings
from typing import Dict, List, Any, Tuple, Optional,Union
import logging
import statsmodels.api as sm
from prophet import Prophet

class ModelSelectionDL:
    def __init__(self, data: pd.DataFrame, target: Optional[str] = None):
        self.data = data
        self.target = target
        self.analysis_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.execution_log = []
        self.warnings = []

    def analyze(self) -> Dict[str, Any]:
        """Performs comprehensive analysis of the dataset for deep learning applications."""
        try:
            analysis_result = {
                "dataset_summary": self._get_dataset_summary(),
                "data_quality": self._analyze_data_quality(),
                "deep_learning_compatibility": self._analyze_dl_compatibility(),
                "architecture_recommendations": self._get_architecture_recommendations(),
                "preprocessing_requirements": self._get_preprocessing_requirements(),
                "resource_requirements": self._estimate_resource_requirements(),
                "model_optimization_suggestions": self._get_optimization_suggestions(),
                "training_strategy": self._recommend_training_strategy(),
                "warnings": self.warnings,
                "execution_log": self.execution_log
            }
            return analysis_result
        except Exception as e:
            self.execution_log.append(f"Error in analysis: {str(e)}")
            raise

    
    def _get_dataset_summary(self) -> Dict[str, Any]:
        """Generates comprehensive dataset summary."""
        self.execution_log.append("Analyzing dataset summary")
        
        feature_types = self._analyze_feature_types()
        memory_usage = sys.getsizeof(self.data)
        
        return {
            "num_samples": len(self.data),
            "num_features": len(self.data.columns),
            "feature_types": feature_types,
            "memory_usage": memory_usage,
            "timestamp": self.analysis_timestamp,
            "target_variable": self.target,
            "data_dimensionality": {
                "high_dimensional": len(self.data.columns) > 100,
                "curse_of_dimensionality_risk": self._assess_dimensionality_risk()
            }
        }

    def _analyze_feature_types(self) -> Dict[str, str]:
        """Analyzes and categorizes features with proper type handling."""
        try:
            feature_types = {}
            
            for column in self.data.columns:
                # Check for datetime first
                try:
                    pd.to_datetime(self.data[column])
                    feature_types[column] = "time_series"
                    continue
                except:
                    pass
                    
                # Try numeric conversion
                try:
                    numeric_data = pd.to_numeric(self.data[column], errors='coerce')
                    if numeric_data.notna().any():
                        # Check if it's categorical
                        unique_ratio = numeric_data.nunique() / len(numeric_data)
                        if unique_ratio < 0.05:
                            feature_types[column] = "categorical"
                        else:
                            feature_types[column] = "numerical"
                        continue
                except:
                    pass
                    
                # Check for text/categorical
                if self.data[column].dtype == 'O':
                    unique_ratio = self.data[column].nunique() / len(self.data)
                    if unique_ratio < 0.05:
                        feature_types[column] = "categorical"
                    else:
                        feature_types[column] = "text"
                    continue
                    
                feature_types[column] = "unknown"
                
            return feature_types
            
        except Exception as e:
            self.warnings.append(f"Feature type analysis failed: {str(e)}")
            return {}

    def _analyze_data_quality(self) -> Dict[str, Dict[str, Any]]:
        """Analyzes data quality for each feature."""
        quality_analysis = {}
        
        for column in self.data.columns:
            column_stats = {
                "missing_ratio": self.data[column].isnull().mean(),
                "feature_type": self._analyze_feature_types()[column],
                "unique_ratio": len(self.data[column].unique()) / len(self.data),
                "statistical_properties": self._get_statistical_properties(column),
                "data_distribution": self._analyze_distribution(column),
                "quality_score": self._calculate_quality_score(column)
            }
            
            if column_stats["missing_ratio"] > 0.2:
                self.warnings.append(f"High missing ratio in {column}: {column_stats['missing_ratio']:.2f}")
                
            quality_analysis[column] = column_stats
            
        return quality_analysis

    def _analyze_dl_compatibility(self) -> Dict[str, Any]:
        """Analyzes dataset compatibility with different deep learning architectures."""
        return {
            "architectures": self._analyze_architecture_compatibility(),
            "data_characteristics": self._analyze_data_characteristics(),
            "complexity_metrics": self._calculate_complexity_metrics(),
            "bottlenecks": self._identify_potential_bottlenecks()
        }
    

    def _analyze_architecture_compatibility(self) -> Dict[str, Dict[str, Any]]:
        """Analyzes compatibility with various deep learning architectures."""
        architectures = {
            # Previous architectures remain...
            "CNN": self._analyze_cnn_compatibility(),
            "RNN": self._analyze_rnn_compatibility(),
            "Transformer": self._analyze_transformer_compatibility(),
            "AutoEncoder": self._analyze_autoencoder_compatibility(),
            "GAN": self._analyze_gan_compatibility(),
            "ResNet": self._analyze_resnet_compatibility(),
            "LSTM": self._analyze_lstm_compatibility(),
            "Attention": self._analyze_attention_compatibility(),
            "Graph_Neural_Network": self._analyze_gnn_compatibility(),
            "Vision_Transformer": self._analyze_vit_compatibility(),
            
            # Additional specialized models
            "Prophet": self._analyze_prophet_compatibility(),
            "LSTNet": self._analyze_lstnet_compatibility(),
            "ARIMA": self._analyze_arima_compatibility(),
            "SARIMA": self._analyze_sarima_compatibility(),
            "ConvLSTM": self._analyze_convlstm_compatibility(),
            "BiLSTM": self._analyze_bilstm_compatibility(),
            "TCN": self._analyze_tcn_compatibility(),
            "DeepAR": self._analyze_deepar_compatibility(),
            "TFT": self._analyze_tft_compatibility(),
            "N_BEATS": self._analyze_nbeats_compatibility()
        }
        return architectures

    def _analyze_prophet_compatibility(self) -> Dict[str, Any]:
        """Analyzes compatibility with Facebook Prophet."""
        try:
            time_series_features = [col for col, type_ in self._analyze_feature_types().items() 
                                if type_ == "time_series"]
            
            seasonality_info = self._analyze_seasonality()
            seasonality_strength = seasonality_info.get('seasonality_strength', 0.0)
            
            # Calculate compatibility score
            compatibility_score = float(len(time_series_features) > 0) * min(1.0, max(seasonality_strength, 0.3))
            
            return {
                "compatibility_score": compatibility_score,
                "suitable_features": time_series_features,
                "requirements": {
                    "minimum_samples": 100,
                    "recommended_samples": 1000,
                    "current_samples": len(self.data)
                },
                "seasonality_analysis": {
                    "has_seasonality": seasonality_strength > 0.3,
                    "seasonality_strength": seasonality_strength,
                    "recommended_seasonality_mode": "multiplicative" if seasonality_strength > 0.7 else "additive"
                },
                "preprocessing_requirements": ["date_formatting", "missing_value_handling"],
                "forecast_horizon": self._recommend_forecast_horizon()
            }
        except Exception as e:
            self.warnings.append(f"Prophet compatibility analysis failed: {str(e)}")
            return {"compatibility_score": 0.0}

    def _recommend_cnn_kernel_size(self) -> int:
        """Recommends CNN kernel size based on data characteristics."""
        try:
            # Default kernel size for most cases
            default_kernel_size = 3
            
            # If we have time series data, adjust based on frequency
            time_series_cols = [col for col, type_ in self._analyze_feature_types().items() 
                            if type_ == "time_series"]
            
            if time_series_cols:
                # Larger kernel for longer sequences
                sequence_length = self._analyze_sequence_length()
                if sequence_length and sequence_length > 100:
                    return 5
                
            return default_kernel_size
        except Exception as e:
            self.warnings.append(f"CNN kernel size recommendation failed: {str(e)}")
            return 3

    def _recommend_rnn_hidden_size(self) -> int:
        """Recommends RNN hidden size based on data complexity."""
        try:
            num_features = len(self.data.columns)
            # Rule of thumb: hidden size should be between input size and output size
            hidden_size = min(max(num_features * 2, 32), 256)
            return hidden_size
        except Exception as e:
            self.warnings.append(f"RNN hidden size recommendation failed: {str(e)}")
            return 64

    def _recommend_skip_length(self) -> int:
        """Recommends skip length for LSTNet architecture."""
        try:
            # For daily data, might skip a week
            # For hourly data, might skip a day
            sequence_length = self._analyze_sequence_length()
            if sequence_length:
                return min(max(sequence_length // 7, 1), 24)
            return 12  # Default skip length
        except Exception as e:
            self.warnings.append(f"Skip length recommendation failed: {str(e)}")
            return 12

    def _recommend_skip_rnn_size(self) -> int:
        """Recommends skip RNN size for LSTNet architecture."""
        try:
            # Generally smaller than main RNN size
            main_rnn_size = self._recommend_rnn_hidden_size()
            return main_rnn_size // 2
        except Exception as e:
            self.warnings.append(f"Skip RNN size recommendation failed: {str(e)}")
            return 32

    def _recommend_ar_window(self) -> int:
        """Recommends autoregressive window size for LSTNet architecture."""
        try:
            sequence_length = self._analyze_sequence_length()
            if sequence_length:
                # AR window should be smaller than sequence length
                return min(max(sequence_length // 10, 1), 24)
            return 12  # Default AR window
        except Exception as e:
            self.warnings.append(f"AR window recommendation failed: {str(e)}")
            return 12

    def _calculate_lstnet_score(self) -> float:
        """Calculates compatibility score for LSTNet architecture."""
        try:
            # Check for multiple related time series
            time_series_cols = [col for col, type_ in self._analyze_feature_types().items() 
                            if type_ == "time_series"]
            
            if not time_series_cols:
                return 0.0
            
            # Calculate score based on data characteristics
            sequence_length = self._analyze_sequence_length()
            if not sequence_length:
                return 0.0
            
            # Higher score for longer sequences and multiple series
            length_score = min(sequence_length / 1000, 1.0)
            series_score = min(len(time_series_cols) / 5, 1.0)
            
            return (length_score * 0.6 + series_score * 0.4)
        except Exception as e:
            self.warnings.append(f"LSTNet score calculation failed: {str(e)}")
            return 0.0

    def _analyze_lstnet_compatibility(self) -> Dict[str, Any]:
        """Analyzes compatibility with LSTNet architecture."""
        return {
            "compatibility_score": self._calculate_lstnet_score(),
            "architecture_recommendations": {
                "cnn_kernel_size": self._recommend_cnn_kernel_size(),
                "rnn_hidden_size": self._recommend_rnn_hidden_size(),
                "skip_length": self._recommend_skip_length(),
                "skip_rnn_hidden_size": self._recommend_skip_rnn_size(),
                "ar_window": self._recommend_ar_window()
            },
            "data_requirements": {
                "minimum_samples": 5000,
                "recommended_samples": 10000,
                "current_samples": len(self.data)
            },
            "preprocessing_requirements": ["normalization", "sequence_creation"]
        }

    def _calculate_arima_score(self) -> float:
        """Calculates ARIMA compatibility score with proper error handling."""
        try:
            # Check for time series features
            time_series_features = [col for col, type_ in self._analyze_feature_types().items() 
                                if type_ == "time_series"]
            
            if not time_series_features:
                return 0.0
                
            # Check stationarity
            stationarity_results = self._check_stationarity()
            stationarity_score = 0.7 if stationarity_results.get('is_stationary', False) else 0.3
            
            # Check autocorrelation
            autocorr_score = self._check_autocorrelation()
            
            # Calculate final score
            score = (stationarity_score * 0.6 + autocorr_score * 0.4)
            return float(score)  # Ensure float return
            
        except Exception as e:
            self.warnings.append(f"ARIMA score calculation failed: {str(e)}")
            return 0.0

    def _recommend_arima_orders(self) -> Dict[str, int]:
        """Recommends orders (p,d,q) for ARIMA model."""
        try:
            # Get main time series for analysis
            time_series = self._get_main_time_series()
            if time_series is None:
                return {"p": 1, "d": 1, "q": 1}
                
            # Determine differencing order (d)
            d = self._estimate_differencing_order(time_series)
            
            # Estimate AR order (p) using partial autocorrelation
            p = self._estimate_ar_order(time_series)
            
            # Estimate MA order (q) using autocorrelation
            q = self._estimate_ma_order(time_series)
            
            return {"p": p, "d": d, "q": q}
            
        except Exception as e:
            self.warnings.append(f"ARIMA order recommendation failed: {str(e)}")
            return {"p": 1, "d": 1, "q": 1}

    def _check_autocorrelation(self) -> float:
        """Checks for significant autocorrelation in the time series."""
        try:
            time_series = self._get_main_time_series()
            if time_series is None:
                return 0.0
                
            # Convert to numeric and handle missing/infinite values
            series = pd.to_numeric(time_series, errors='coerce')
            series = series.replace([np.inf, -np.inf], np.nan)
            series = series.fillna(method='ffill').fillna(method='bfill')
            
            if len(series) < 2:
                return 0.0
                
            # Calculate autocorrelation at first lag
            acf = sm.tsa.acf(series, nlags=1, fft=False)
            if len(acf) < 2:
                return 0.0
                
            return float(abs(acf[1]))
            
        except Exception as e:
            self.warnings.append(f"Autocorrelation check failed: {str(e)}")
            return 0.0

    def _check_partial_autocorrelation(self) -> float:
        """Checks for significant partial autocorrelation in the time series."""
        try:
            time_series = self._get_main_time_series()
            if time_series is None:
                return 0.0
                
            # Convert to numeric and handle missing/infinite values
            series = pd.to_numeric(time_series, errors='coerce')
            series = series.replace([np.inf, -np.inf], np.nan)
            series = series.fillna(method='ffill').fillna(method='bfill')
            
            if len(series) < 2:
                return 0.0
                
            # Calculate partial autocorrelation at first lag
            pacf = sm.tsa.pacf(series, nlags=1)
            if len(pacf) < 2:
                return 0.0
                
            return float(abs(pacf[1]))
            
        except Exception as e:
            self.warnings.append(f"Partial autocorrelation check failed: {str(e)}")
            return 0.0
        
        
    def _estimate_differencing_order(self, time_series: pd.Series) -> int:
        """Estimates the order of differencing needed for stationarity."""
        try:
            max_d = 2  # Maximum differencing order to consider
            d = 0
            
            # Convert to numeric and handle missing/infinite values
            series = pd.to_numeric(time_series, errors='coerce')
            series = series.replace([np.inf, -np.inf], np.nan)
            series = series.fillna(method='ffill').fillna(method='bfill')
            
            if len(series) < 2:
                return 0
                
            # Keep differencing until series becomes stationary or max_d is reached
            while d < max_d:
                # Perform ADF test
                try:
                    adf_result = sm.tsa.stattools.adfuller(series)
                    if adf_result[1] < 0.05:  # Series is stationary
                        break
                except:
                    break
                    
                # Difference the series
                series = series.diff().dropna()
                if len(series) < 2:
                    break
                    
                d += 1
                
            return d
            
        except Exception as e:
            self.warnings.append(f"Differencing order estimation failed: {str(e)}")
            return 1

    def _estimate_ar_order(self, time_series: pd.Series) -> int:
        """Estimates the AR order (p) using partial autocorrelation."""
        try:
            # Calculate PACF
            pacf = sm.tsa.pacf(time_series, nlags=10)
            
            # Find significant lags (using 95% confidence interval)
            significant_lags = 0
            threshold = 1.96 / np.sqrt(len(time_series))
            
            for i in range(1, len(pacf)):
                if abs(pacf[i]) > threshold:
                    significant_lags += 1
                else:
                    break
                    
            # Limit maximum AR order
            return min(significant_lags, 5)
            
        except Exception as e:
            self.warnings.append(f"AR order estimation failed: {str(e)}")
            return 1

    def _estimate_ma_order(self, time_series: pd.Series) -> int:
        """Estimates the MA order (q) using autocorrelation."""
        try:
            # Calculate ACF
            acf = sm.tsa.acf(time_series, nlags=10)
            
            # Find significant lags (using 95% confidence interval)
            significant_lags = 0
            threshold = 1.96 / np.sqrt(len(time_series))
            
            for i in range(1, len(acf)):
                if abs(acf[i]) > threshold:
                    significant_lags += 1
                else:
                    break
                    
            # Limit maximum MA order
            return min(significant_lags, 5)
            
        except Exception as e:
            self.warnings.append(f"MA order estimation failed: {str(e)}")
            return 1

    def _get_main_time_series(self) -> Optional[pd.Series]:
        """Gets the main time series from the data with proper type handling."""
        try:
            # If target is specified, try to convert it to numeric
            if self.target:
                try:
                    series = pd.to_numeric(self.data[self.target], errors='coerce')
                    if not series.empty and series.notna().any():
                        return series
                except:
                    pass
                
            # Look for numeric time series columns
            for col in self.data.columns:
                try:
                    series = pd.to_numeric(self.data[col], errors='coerce')
                    if not series.empty and series.notna().any():
                        return series
                except:
                    continue
                    
            return None
            
        except Exception as e:
            self.warnings.append(f"Main time series extraction failed: {str(e)}")
            return None

    def _detect_period(self) -> int:
        """Detects the period of the time series."""
        try:
            time_series = self._get_main_time_series()
            if time_series is None:
                return 1
                
            # Try to detect common periods
            n = len(time_series)
            
            if n >= 365:
                return 365  # Daily data with yearly seasonality
            elif n >= 52:
                return 52   # Weekly data with yearly seasonality
            elif n >= 12:
                return 12   # Monthly data with yearly seasonality
            elif n >= 7:
                return 7    # Daily data with weekly seasonality
            else:
                return 1    # No clear seasonality
                
        except Exception as e:
            self.warnings.append(f"Period detection failed: {str(e)}")
            return 1
    
    def _analyze_arima_compatibility(self) -> Dict[str, Any]:
        """Analyzes compatibility with ARIMA models."""
        stationarity_results = self._check_stationarity()
        return {
            "compatibility_score": self._calculate_arima_score(),
            "stationarity_analysis": stationarity_results,
            "order_recommendations": self._recommend_arima_orders(),
            "assumptions_check": {
                "stationarity": stationarity_results["is_stationary"],
                "autocorrelation": self._check_autocorrelation(),
                "partial_autocorrelation": self._check_partial_autocorrelation()
            },
            "preprocessing_requirements": ["differencing", "outlier_removal"]
        }
    

    def _calculate_sarima_score(self) -> float:
        """Calculates compatibility score for SARIMA models."""
        try:
            # Get seasonality information
            seasonality_info = self._analyze_seasonality()
            seasonality_strength = seasonality_info.get('seasonality_strength', 0.0)
            
            # Base score on ARIMA compatibility
            base_score = self._calculate_arima_score()
            
            # Adjust score based on seasonality
            seasonal_score = min(seasonality_strength, 1.0)
            
            # Combine scores (weighted average)
            final_score = (base_score * 0.4 + seasonal_score * 0.6)
            
            return final_score
            
        except Exception as e:
            self.warnings.append(f"SARIMA score calculation failed: {str(e)}")
            return 0.0

    def _recommend_seasonal_orders(self) -> Dict[str, int]:
        """Recommends seasonal orders (P,D,Q,s) for SARIMA model."""
        try:
            # Get main time series
            time_series = self._get_main_time_series()
            if time_series is None:
                return {"P": 1, "D": 1, "Q": 1, "s": 12}
            
            # Detect seasonal period
            s = self._detect_period()
            
            # Determine seasonal differencing order (D)
            D = self._estimate_seasonal_differencing_order(time_series, s)
            
            # Estimate seasonal AR order (P)
            P = self._estimate_seasonal_ar_order(time_series, s)
            
            # Estimate seasonal MA order (Q)
            Q = self._estimate_seasonal_ma_order(time_series, s)
            
            return {"P": P, "D": D, "Q": Q, "s": s}
            
        except Exception as e:
            self.warnings.append(f"Seasonal order recommendation failed: {str(e)}")
            return {"P": 1, "D": 1, "Q": 1, "s": 12}

    def _estimate_seasonal_differencing_order(self, time_series: pd.Series, period: int) -> int:
        """Estimates the seasonal differencing order needed for stationarity."""
        try:
            max_D = 2  # Maximum seasonal differencing order
            D = 0
            
            # Convert to numeric and handle missing/infinite values
            series = pd.to_numeric(time_series, errors='coerce')
            series = series.replace([np.inf, -np.inf], np.nan)
            series = series.fillna(method='ffill').fillna(method='bfill')
            
            if len(series) < period * 2:
                return 0
                
            while D < max_D:
                # Check seasonality strength
                try:
                    decomposition = sm.tsa.seasonal_decompose(series, period=period)
                    seasonal_strength = np.std(decomposition.seasonal) / np.std(series)
                    
                    if seasonal_strength < 0.1:  # Weak seasonality
                        break
                except:
                    break
                    
                # Apply seasonal differencing
                series = series.diff(period).dropna()
                if len(series) < period * 2:
                    break
                    
                D += 1
                
            return D
            
        except Exception as e:
            self.warnings.append(f"Seasonal differencing order estimation failed: {str(e)}")
            return 1

    def _estimate_seasonal_ar_order(self, time_series: pd.Series, period: int) -> int:
        """Estimates the seasonal AR order (P) using seasonal partial autocorrelation."""
        try:
            # Calculate PACF at seasonal lags
            seasonal_lags = min(4 * period, len(time_series) // 2)
            pacf = sm.tsa.pacf(time_series, nlags=seasonal_lags)
            
            # Look at seasonal lags only
            seasonal_pacf = pacf[period::period]
            
            # Find significant seasonal lags
            significant_lags = 0
            threshold = 1.96 / np.sqrt(len(time_series))
            
            for i in range(len(seasonal_pacf)):
                if abs(seasonal_pacf[i]) > threshold:
                    significant_lags += 1
                else:
                    break
                    
            # Limit maximum seasonal AR order
            return min(significant_lags, 2)
            
        except Exception as e:
            self.warnings.append(f"Seasonal AR order estimation failed: {str(e)}")
            return 1

    def _estimate_seasonal_ma_order(self, time_series: pd.Series, period: int) -> int:
        """Estimates the seasonal MA order (Q) using seasonal autocorrelation."""
        try:
            # Calculate ACF at seasonal lags
            seasonal_lags = min(4 * period, len(time_series) // 2)
            acf = sm.tsa.acf(time_series, nlags=seasonal_lags)
            
            # Look at seasonal lags only
            seasonal_acf = acf[period::period]
            
            # Find significant seasonal lags
            significant_lags = 0
            threshold = 1.96 / np.sqrt(len(time_series))
            
            for i in range(len(seasonal_acf)):
                if abs(seasonal_acf[i]) > threshold:
                    significant_lags += 1
                else:
                    break
                    
            # Limit maximum seasonal MA order
            return min(significant_lags, 2)
            
        except Exception as e:
            self.warnings.append(f"Seasonal MA order estimation failed: {str(e)}")
            return 1

    def _estimate_sarima_memory(self) -> Dict[str, Union[int, str]]:
        """Estimates memory requirements for SARIMA model."""
        try:
            # Get data characteristics
            n_samples = len(self.data)
            period = self._detect_period()
            
            # Estimate based on sample size and seasonal period
            base_memory = n_samples * 8  # 8 bytes per float
            seasonal_memory = base_memory * period
            
            total_memory = base_memory + seasonal_memory
            
            # Convert to MB
            memory_mb = total_memory / (1024 * 1024)
            
            return {
                "estimated_mb": round(memory_mb, 2),
                "recommendation": "low" if memory_mb < 100 else "medium" if memory_mb < 1000 else "high"
            }
            
        except Exception as e:
            self.warnings.append(f"SARIMA memory estimation failed: {str(e)}")
            return {"estimated_mb": 0, "recommendation": "unknown"}

    def _analyze_sarima_compatibility(self) -> Dict[str, Any]:
        """Analyzes compatibility with SARIMA models."""
        seasonality_info = self._analyze_seasonality()
        return {
            "compatibility_score": self._calculate_sarima_score(),
            "seasonality_analysis": seasonality_info,
            "order_recommendations": {
                "non_seasonal_orders": self._recommend_arima_orders(),
                "seasonal_orders": self._recommend_seasonal_orders()
            },
            "preprocessing_requirements": ["seasonal_differencing", "outlier_removal"],
            "performance_considerations": {
                "computation_intensity": "high",
                "memory_requirements": self._estimate_sarima_memory()
            }
        }

    def _analyze_convlstm_compatibility(self) -> Dict[str, Any]:
        """Analyzes compatibility with ConvLSTM architecture."""
        spatial_temporal_score = self._analyze_spatial_temporal_patterns()
        return {
            "compatibility_score": spatial_temporal_score,
            "architecture_recommendations": {
                "conv_filters": self._recommend_conv_filters(),
                "kernel_size": self._recommend_kernel_size(),
                "lstm_units": self._recommend_lstm_units(),
                "stacked_layers": self._recommend_stacked_layers()
            },
            "data_requirements": {
                "spatial_resolution": self._analyze_spatial_resolution(),
                "temporal_length": self._analyze_temporal_length(),
                "minimum_samples": 1000
            },
            "preprocessing_requirements": ["spatial_normalization", "temporal_alignment"]
        }

    def _analyze_bilstm_compatibility(self) -> Dict[str, Any]:
        """Analyzes compatibility with Bidirectional LSTM."""
        sequence_quality = self._analyze_sequence_quality()
        return {
            "compatibility_score": self._calculate_bilstm_score(),
            "architecture_recommendations": {
                "hidden_units": self._recommend_bilstm_units(),
                "num_layers": self._recommend_bilstm_layers(),
                "dropout_rate": self._recommend_dropout_rate(),
                "merge_mode": self._recommend_merge_mode()
            },
            "sequence_analysis": {
                "sequence_length": self._analyze_sequence_length(),
                "bidirectional_importance": self._analyze_bidirectional_importance(),
                "sequence_quality": sequence_quality
            },
            "preprocessing_requirements": ["sequence_padding", "normalization"]
        }

    def _analyze_tcn_compatibility(self) -> Dict[str, Any]:
        """Analyzes compatibility with Temporal Convolutional Network."""
        return {
            "compatibility_score": self._calculate_tcn_score(),
            "architecture_recommendations": {
                "num_filters": self._recommend_tcn_filters(),
                "kernel_size": self._recommend_tcn_kernel(),
                "dilation_base": self._recommend_dilation_base(),
                "num_levels": self._recommend_tcn_levels()
            },
            "receptive_field": self._calculate_receptive_field(),
            "causal_requirement": self._check_causality_requirement()
        }

    # Helper methods for analyzing time series characteristics

    def _analyze_seasonality(self) -> Dict[str, Any]:
        """Analyzes seasonality patterns in the data with proper error handling."""
        try:
            # Get main time series
            time_series = self._get_main_time_series()
            if time_series is None:
                return {"seasonality_strength": 0.0, "detected_frequencies": []}

            # Handle missing values
            time_series = time_series.fillna(method='ffill').fillna(method='bfill')
            
            if len(time_series) < 2:
                return {"seasonality_strength": 0.0, "detected_frequencies": []}

            # Perform decomposition
            period = self._detect_period()
            if period > len(time_series) // 2:
                period = len(time_series) // 2

            if period < 2:
                return {"seasonality_strength": 0.0, "detected_frequencies": []}

            decomposition = sm.tsa.seasonal_decompose(time_series, period=period)
            
            # Calculate seasonality strength
            seasonality_strength = np.std(decomposition.seasonal) / np.std(time_series)
            
            return {
                "seasonality_strength": float(seasonality_strength),
                "detected_frequencies": [period],
                "has_seasonality": seasonality_strength > 0.3
            }
            
        except Exception as e:
            self.warnings.append(f"Seasonality analysis failed: {str(e)}")
            return {"seasonality_strength": 0.0, "detected_frequencies": [], "has_seasonality": False}


    def _check_stationarity(self) -> Dict[str, Any]:
        """Checks stationarity of time series data."""
        try:
            time_series = self._get_main_time_series()
            if time_series is None:
                return {"is_stationary": False, "p_value": 1.0}

            # Augmented Dickey-Fuller test
            adf_result = sm.tsa.stattools.adfuller(time_series)
            
            return {
                "is_stationary": adf_result[1] < 0.05,
                "p_value": adf_result[1],
                "critical_values": adf_result[4],
                "num_differencing_required": self._estimate_differencing_order(time_series)
            }
        except Exception as e:
            self.warnings.append(f"Stationarity check failed: {str(e)}")
            return {"is_stationary": False, "p_value": 1.0}

    def _analyze_spatial_temporal_patterns(self) -> float:
        """Analyzes spatial-temporal patterns in the data."""
        try:
            # Check for spatial patterns
            spatial_features = self._identify_spatial_features()
            if not spatial_features:
                return 0.0

            # Check for temporal patterns
            temporal_score = self._analyze_temporal_patterns()
            
            # Combine scores
            return min(temporal_score * len(spatial_features) / len(self.data.columns), 1.0)
        except Exception as e:
            self.warnings.append(f"Spatial-temporal analysis failed: {str(e)}")
            return 0.0

    def _recommend_forecast_horizon(self) -> Dict[str, int]:
        """Recommends forecast horizon based on data characteristics."""
        try:
            data_length = len(self.data)
            return {
                "minimum": max(1, data_length // 100),
                "recommended": max(1, data_length // 10),
                "maximum": max(1, data_length // 2)
            }
        except Exception as e:
            self.warnings.append(f"Forecast horizon recommendation failed: {str(e)}")
            return {"minimum": 1, "recommended": 1, "maximum": 1}

    # Additional helper methods for model-specific recommendations


    def _calculate_series_correlation(self) -> float:
        """Calculates correlation between multiple time series."""
        try:
            # Get numeric columns
            numeric_cols = self.data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) < 2:
                return 0.0
                
            # Calculate correlation matrix
            corr_matrix = self.data[numeric_cols].corr().abs()
            
            # Calculate mean correlation excluding diagonal
            n = len(corr_matrix)
            if n < 2:
                return 0.0
                
            total_corr = (corr_matrix.sum().sum() - n) / (n * n - n)
            return float(total_corr)
            
        except Exception as e:
            self.warnings.append(f"Series correlation calculation failed: {str(e)}")
            return 0.0
    

    def _calculate_lstnet_score(self) -> float:
        """Calculates compatibility score for LSTNet."""
        try:
            # Check for multiple related time series
            num_time_series = len([col for col, type_ in self._analyze_feature_types().items() 
                                 if type_ == "time_series"])
            
            if num_time_series < 2:
                return 0.0
                
            # Check for sufficient data
            if len(self.data) < 5000:
                return 0.0
                
            # Calculate score based on various factors
            data_size_score = min(len(self.data) / 10000, 1.0)
            correlation_score = self._calculate_series_correlation()
            
            return (data_size_score * 0.4 + correlation_score * 0.6)
        except Exception as e:
            self.warnings.append(f"LSTNet score calculation failed: {str(e)}")
            return 0.0

    def _recommend_bilstm_units(self) -> List[int]:
        """Recommends number of units for BiLSTM layers."""
        try:
            sequence_length = self._analyze_sequence_length()
            feature_dim = len(self.data.columns)
            
            # Base number of units on sequence length and feature dimensionality
            base_units = min(max(sequence_length, feature_dim), 512)
            
            # Create decreasing layer sizes
            units = [
                base_units,
                base_units // 2,
                base_units // 4
            ]
            
            return [u for u in units if u >= 32]  # Ensure minimum size
        except Exception as e:
            self.warnings.append(f"BiLSTM units recommendation failed: {str(e)}")
            return [64, 32]

    def _recommend_tcn_filters(self) -> List[int]:
        """Recommends number of filters for TCN layers."""
        try:
            sequence_length = self._analyze_sequence_length()
            feature_dim = len(self.data.columns)
            
            # Base number of filters on data characteristics
            base_filters = min(max(sequence_length // 2, feature_dim * 2), 256)
            
            return [
                base_filters,
                base_filters * 2,
                base_filters * 4
            ]
        except Exception as e:
            self.warnings.append(f"TCN filters recommendation failed: {str(e)}")
            return [64, 128, 256]

    def _analyze_sequence_quality(self) -> Dict[str, float]:
        """Analyzes the quality of sequences in the data."""
        try:
            return {
                "completeness": self._calculate_sequence_completeness(),
                "consistency": self._calculate_sequence_consistency(),
                "noise_level": self._estimate_sequence_noise()
            }
        except Exception as e:
            self.warnings.append(f"Sequence quality analysis failed: {str(e)}")
            return {"completeness": 0.0, "consistency": 0.0, "noise_level": 1.0}
    

    def _get_preprocessing_requirements(self) -> List[str]:
        """Determines required preprocessing steps based on data analysis."""
        try:
            requirements = []
            
            # Check for missing values
            if self.data.isnull().any().any():
                requirements.append("missing_value_handling")
                
            # Check for categorical variables
            if any(self._is_categorical(col) for col in self.data.columns):
                requirements.append("categorical_encoding")
                
            # Check for numerical variables that need scaling
            numerical_cols = [col for col in self.data.columns if self._is_numerical(col)]
            if numerical_cols:
                requirements.append("numerical_scaling")
                
            # Check for text data
            if any(self._is_text_data(col) for col in self.data.columns):
                requirements.append("text_preprocessing")
                
            # Check for time series data
            if any(self._is_time_series(col) for col in self.data.columns):
                requirements.append("temporal_preprocessing")
                
            # Check for dimensionality reduction needs
            if len(self.data.columns) > 100:
                requirements.append("dimensionality_reduction")
                
            return requirements
            
        except Exception as e:
            self.warnings.append(f"Preprocessing requirements analysis failed: {str(e)}")
            return ["missing_value_handling", "numerical_scaling"] 


    def get_model_recommendations(self) -> Dict[str, Any]:
        """Returns focused model recommendations based on data analysis."""
        try:
            # First perform general analysis
            analysis = self._analyze_dl_compatibility()
            
            # Get architecture compatibilities
            architectures = self._analyze_architecture_compatibility()
            
            # Sort architectures by compatibility score
            sorted_architectures = dict(sorted(
                architectures.items(),
                key=lambda item: item[1].get('compatibility_score', 0.0) if isinstance(item[1], dict) else 0.0,
                reverse=True
            ))
            
            # Get top recommendations
            recommendations = {
                "top_recommendations": list(sorted_architectures.keys())[:3],
                "architecture_details": sorted_architectures,
                "data_characteristics": analysis["data_characteristics"],
                "preprocessing_steps": self._get_preprocessing_requirements(),
                "training_recommendations": {
                    "batch_size": self._recommend_batch_size(),
                    "learning_rate": self._recommend_learning_rate(),
                    "optimizer": self._recommend_optimizer(),
                    "regularization": self._recommend_regularization()
                },
                "warnings": self.warnings
            }
            
            return recommendations
            
        except Exception as e:
            self.execution_log.append(f"Error in getting model recommendations: {str(e)}")
            raise


    def _recommend_batch_size(self) -> int:
        """Recommends appropriate batch size based on data characteristics."""
        try:
            num_samples = len(self.data)
            num_features = len(self.data.columns)
            
            # Base calculation on data size and complexity
            if num_samples < 1000:
                return min(32, num_samples)
            elif num_samples < 10000:
                return 64
            elif num_samples < 100000:
                return 128
            else:
                return 256
                
        except Exception as e:
            self.warnings.append(f"Batch size recommendation failed: {str(e)}")
            return 32

    def _recommend_learning_rate(self) -> float:
        """Recommends learning rate based on model and data characteristics."""
        try:
            # Start with standard learning rate
            base_lr = 0.001
            
            # Adjust based on data size
            if len(self.data) > 100000:
                base_lr *= 0.1
            elif len(self.data) < 1000:
                base_lr *= 10
                
            # Adjust based on feature complexity
            if len(self.data.columns) > 100:
                base_lr *= 0.1
                
            return base_lr
            
        except Exception as e:
            self.warnings.append(f"Learning rate recommendation failed: {str(e)}")
            return 0.001

    def _recommend_optimizer(self) -> Dict[str, Any]:
        """Recommends optimizer configuration."""
        try:
            # Analyze data characteristics
            data_size = len(self.data)
            feature_complexity = len(self.data.columns)
            
            if data_size > 100000 or feature_complexity > 100:
                return {
                    "optimizer": "Adam",
                    "parameters": {
                        "learning_rate": self._recommend_learning_rate(),
                        "beta_1": 0.9,
                        "beta_2": 0.999,
                        "epsilon": 1e-07
                    }
                }
            else:
                return {
                    "optimizer": "RMSprop",
                    "parameters": {
                        "learning_rate": self._recommend_learning_rate(),
                        "rho": 0.9,
                        "momentum": 0.0,
                        "epsilon": 1e-07
                    }
                }
                
        except Exception as e:
            self.warnings.append(f"Optimizer recommendation failed: {str(e)}")
            return {"optimizer": "Adam", "parameters": {"learning_rate": 0.001}}

    def _recommend_regularization(self) -> Dict[str, Any]:
        """Recommends regularization techniques and parameters."""
        try:
            num_features = len(self.data.columns)
            num_samples = len(self.data)
            
            # Calculate ratio of samples to features
            ratio = num_samples / num_features
            
            recommendations = {
                "dropout_rate": 0.2 if ratio > 10 else 0.3,
                "l1_regularization": 0.01 if ratio < 5 else 0.001,
                "l2_regularization": 0.01 if ratio < 5 else 0.001,
                "batch_normalization": ratio < 20,
                "early_stopping": {
                    "monitor": "val_loss",
                    "patience": 10,
                    "min_delta": 0.001
                }
            }
            
            return recommendations
            
        except Exception as e:
            self.warnings.append(f"Regularization recommendation failed: {str(e)}")
            return {"dropout_rate": 0.2, "l2_regularization": 0.01}


    def _analyze_cnn_compatibility(self) -> Dict[str, Any]:
        """Analyzes compatibility with Convolutional Neural Networks."""
        try:
            # Check for image-like data structures
            feature_types = self._analyze_feature_types()
            image_features = [col for col, type_ in feature_types.items() if type_ == "image"]
            
            # Calculate compatibility score
            score = len(image_features) / len(self.data.columns) if len(self.data.columns) > 0 else 0
            
            return {
                "compatibility_score": score,
                "suitable_features": image_features,
                "architecture_recommendations": {
                    "num_layers": self._recommend_cnn_layers(),
                    "filter_sizes": self._recommend_filter_sizes(),
                    "pooling_layers": bool(score > 0),
                    "activation": "relu"
                },
                "data_requirements": {
                    "minimum_samples": 1000,
                    "recommended_samples": 10000,
                    "current_samples": len(self.data)
                }
            }
            
        except Exception as e:
            self.warnings.append(f"CNN compatibility analysis failed: {str(e)}")
            return {"compatibility_score": 0.0}
        
    def _recommend_cnn_layers(self) -> int:
        """Recommends number of CNN layers based on data characteristics."""
        try:
            # Analyze data complexity
            data_size = len(self.data)
            num_features = len(self.data.columns)
            
            # Base recommendation on data size and complexity
            if data_size > 10000 and num_features > 50:
                return 4  # Deep architecture
            elif data_size > 5000 or num_features > 20:
                return 3  # Moderate depth
            else:
                return 2  # Shallow architecture
                
        except Exception as e:
            self.warnings.append(f"CNN layers recommendation failed: {str(e)}")
            return 2
        

    def _analyze_thetas_dims(self, forecast_length: int) -> Dict[str, List[int]]:
        """Analyzes and recommends dimensions for N-BEATS theta parameters."""
        try:
            if forecast_length <= 0:
                return {"trend": [2], "seasonality": [1], "generic": [1]}
                
            period = self._detect_period()
            
            return {
                "trend": [2, forecast_length],  # Linear trend
                "seasonality": [min(period * 2, forecast_length * 2)],  # Seasonal components
                "generic": [forecast_length * 2]  # Generic basis
            }
            
        except Exception as e:
            self.warnings.append(f"Thetas dimensions analysis failed: {str(e)}")
            return {"trend": [2], "seasonality": [1], "generic": [1]}

    def _recommend_filter_sizes(self) -> List[int]:
        """Recommends filter sizes for CNN layers."""
        try:
            num_layers = self._recommend_cnn_layers()
            
            # Start with small filters and gradually increase
            filter_sizes = [3] * num_layers
            
            # For deeper networks, use larger filters in later layers
            if num_layers > 2:
                filter_sizes[-1] = 5
            if num_layers > 3:
                filter_sizes[-2] = 5
                
            return filter_sizes
            
        except Exception as e:
            self.warnings.append(f"Filter sizes recommendation failed: {str(e)}")
            return [3, 3, 3]

    def _analyze_rnn_compatibility(self) -> Dict[str, Any]:
        """Analyzes compatibility with Recurrent Neural Networks."""
        try:
            # Check for sequential or time series data
            feature_types = self._analyze_feature_types()
            sequential_features = [col for col, type_ in feature_types.items() 
                                if type_ in ["sequential", "time_series", "text"]]
            
            score = len(sequential_features) / len(self.data.columns) if len(self.data.columns) > 0 else 0
            
            return {
                "compatibility_score": score,
                "suitable_features": sequential_features,
                "architecture_recommendations": {
                    "cell_type": "LSTM" if len(self.data) > 5000 else "SimpleRNN",
                    "num_layers": 2 if score > 0.5 else 1,
                    "bidirectional": self._check_bidirectional_benefit()
                }
            }
        except Exception as e:
            self.warnings.append(f"RNN compatibility analysis failed: {str(e)}")
            return {"compatibility_score": 0.0}

    def _analyze_transformer_compatibility(self) -> Dict[str, Any]:
        """Analyzes compatibility with Transformer architecture."""
        try:
            # Check for sequential data with long-range dependencies
            sequence_length = self._analyze_sequence_length()
            has_long_range = sequence_length > 100 if sequence_length else False
            
            score = 0.8 if has_long_range else 0.3
            
            return {
                "compatibility_score": score,
                "architecture_recommendations": {
                    "num_layers": min(6, sequence_length // 100) if sequence_length else 2,
                    "num_heads": 8,
                    "d_model": 512 if sequence_length and sequence_length > 1000 else 256
                }
            }
        except Exception as e:
            self.warnings.append(f"Transformer compatibility analysis failed: {str(e)}")
            return {"compatibility_score": 0.0}

    def _analyze_autoencoder_compatibility(self) -> Dict[str, Any]:
        """Analyzes compatibility with Autoencoder architecture."""
        try:
            # Check for high-dimensional data
            num_features = len(self.data.columns)
            feature_correlation = self._analyze_feature_correlation()
            
            score = min(1.0, num_features / 100) * feature_correlation
            
            return {
                "compatibility_score": score,
                "architecture_recommendations": {
                    "encoding_dims": [num_features // 2, num_features // 4, num_features // 8],
                    "activation": "relu",
                    "use_denoising": feature_correlation < 0.5
                }
            }
        except Exception as e:
            self.warnings.append(f"Autoencoder compatibility analysis failed: {str(e)}")
            return {"compatibility_score": 0.0}

    def _analyze_gan_compatibility(self) -> Dict[str, Any]:
        """Analyzes compatibility with Generative Adversarial Networks."""
        try:
            # Check for complex data distributions
            distribution_complexity = self._analyze_distribution_complexity()
            
            return {
                "compatibility_score": distribution_complexity,
                "architecture_recommendations": {
                    "generator_dims": [64, 128, 256],
                    "discriminator_dims": [256, 128, 64],
                    "latent_dim": 100
                }
            }
        except Exception as e:
            self.warnings.append(f"GAN compatibility analysis failed: {str(e)}")
            return {"compatibility_score": 0.0}

    def _analyze_resnet_compatibility(self) -> Dict[str, Any]:
        """Analyzes compatibility with ResNet architecture."""
        try:
            # Check for deep network requirements
            data_complexity = self._analyze_data_complexity()
            sample_size = len(self.data)
            
            score = min(1.0, (data_complexity * sample_size / 10000))
            
            return {
                "compatibility_score": score,
                "architecture_recommendations": {
                    "num_blocks": [3, 4, 6, 3],
                    "channels": [64, 128, 256, 512],
                    "use_bottleneck": sample_size > 50000
                }
            }
        except Exception as e:
            self.warnings.append(f"ResNet compatibility analysis failed: {str(e)}")
            return {"compatibility_score": 0.0}

    def _analyze_lstm_compatibility(self) -> Dict[str, Any]:
        """Analyzes compatibility with LSTM architecture."""
        try:
            # Check for sequential data with memory requirements
            sequence_length = self._analyze_sequence_length()
            memory_requirements = self._analyze_memory_requirements()
            
            score = min(1.0, sequence_length / 100) * memory_requirements if sequence_length else 0
            
            return {
                "compatibility_score": score,
                "architecture_recommendations": {
                    "num_units": [64, 128] if score > 0.5 else [32, 64],
                    "dropout_rate": 0.2 if len(self.data) > 10000 else 0.1,
                    "recurrent_dropout": 0.1
                }
            }
        except Exception as e:
            self.warnings.append(f"LSTM compatibility analysis failed: {str(e)}")
            return {"compatibility_score": 0.0}

    def _analyze_attention_compatibility(self) -> Dict[str, Any]:
        """Analyzes compatibility with Attention mechanisms."""
        try:
            # Check for data with important long-range dependencies
            dependency_score = self._analyze_temporal_dependencies()
            
            return {
                "compatibility_score": dependency_score,
                "architecture_recommendations": {
                    "attention_heads": 8 if dependency_score > 0.7 else 4,
                    "key_dim": 64,
                    "attention_dropout": 0.1
                }
            }
        except Exception as e:
            self.warnings.append(f"Attention compatibility analysis failed: {str(e)}")
            return {"compatibility_score": 0.0}

    def _analyze_gnn_compatibility(self) -> Dict[str, Any]:
        """Analyzes compatibility with Graph Neural Networks."""
        try:
            # Check for graph-structured data
            has_graph_structure = self._check_graph_structure()
            
            return {
                "compatibility_score": 1.0 if has_graph_structure else 0.0,
                "architecture_recommendations": {
                    "graph_conv_layers": [64, 128, 256],
                    "pooling_type": "mean",
                    "use_residual": True
                }
            }
        except Exception as e:
            self.warnings.append(f"GNN compatibility analysis failed: {str(e)}")
            return {"compatibility_score": 0.0}

    def _analyze_vit_compatibility(self) -> Dict[str, Any]:
        """Analyzes compatibility with Vision Transformer."""
        try:
            # Check for image data suitable for ViT
            feature_types = self._analyze_feature_types()
            image_features = [col for col, type_ in feature_types.items() if type_ == "image"]
            
            score = len(image_features) / len(self.data.columns) if len(self.data.columns) > 0 else 0
            
            return {
                "compatibility_score": score,
                "architecture_recommendations": {
                    "patch_size": 16,
                    "num_layers": 12,
                    "num_heads": 12,
                    "mlp_dim": 3072
                }
            }
        except Exception as e:
            self.warnings.append(f"ViT compatibility analysis failed: {str(e)}")
            return {"compatibility_score": 0.0}

    # Helper methods for analysis

    def _analyze_feature_correlation(self) -> float:
        """Analyzes correlation between numeric features."""
        try:
            # Get only numeric columns
            numeric_data = self.data.select_dtypes(include=[np.number])
            
            if numeric_data.empty or len(numeric_data.columns) < 2:
                return 0.0
                
            # Calculate correlation matrix
            correlation_matrix = numeric_data.corr().abs()
            
            # Calculate mean correlation excluding diagonal
            n = len(correlation_matrix)
            if n < 2:
                return 0.0
                
            total_corr = (correlation_matrix.sum().sum() - n) / (n * n - n)
            return float(total_corr)
            
        except Exception as e:
            self.warnings.append(f"Feature correlation analysis failed: {str(e)}")
            return 0.0



    def _analyze_distribution_complexity(self) -> float:
        """Analyzes complexity of numeric feature distributions."""
        try:
            # Get only numeric columns
            numeric_data = self.data.select_dtypes(include=[np.number])
            
            if numeric_data.empty:
                return 0.0
                
            # Calculate moments for each numeric column
            complexity_scores = []
            
            for column in numeric_data.columns:
                try:
                    series = numeric_data[column].dropna()
                    if len(series) < 2:
                        continue
                        
                    # Calculate skewness and kurtosis
                    skew = abs(stats.skew(series))
                    kurt = abs(stats.kurtosis(series))
                    
                    # Combine into complexity score
                    column_score = min((skew + kurt) / 10, 1.0)
                    complexity_scores.append(column_score)
                    
                except:
                    continue
                    
            if not complexity_scores:
                return 0.0
                
            # Return average complexity
            return float(np.mean(complexity_scores))
            
        except Exception as e:
            self.warnings.append(f"Distribution complexity analysis failed: {str(e)}")
            return 0.0


    def _analyze_data_complexity(self) -> float:
        """Analyzes overall data complexity."""
        try:
            feature_correlation = self._analyze_feature_correlation()
            distribution_complexity = self._analyze_distribution_complexity()
            return (feature_correlation + distribution_complexity) / 2
        except Exception as e:
            self.warnings.append(f"Data complexity analysis failed: {str(e)}")
            return 0.0

    def _analyze_sequence_length(self) -> Optional[int]:
        """Analyzes typical sequence length in the data."""
        try:
            # Implement sequence length detection logic
            return None  # Placeholder
        except Exception as e:
            self.warnings.append(f"Sequence length analysis failed: {str(e)}")
            return None

    def _analyze_temporal_dependencies(self) -> float:
        """Analyzes temporal dependencies in the data."""
        try:
            # Implement temporal dependency analysis
            return 0.5  # Placeholder
        except Exception as e:
            self.warnings.append(f"Temporal dependency analysis failed: {str(e)}")
            return 0.0

    def _check_graph_structure(self) -> bool:
        """Checks if data has graph structure."""
        try:
            # Implement graph structure detection
            return False  # Placeholder
        except Exception as e:
            self.warnings.append(f"Graph structure check failed: {str(e)}")
            return False

    def _check_bidirectional_benefit(self) -> bool:
        """Checks if bidirectional processing would be beneficial."""
        try:
            # Implement bidirectional benefit analysis
            return True  # Placeholder
        except Exception as e:
            self.warnings.append(f"Bidirectional benefit check failed: {str(e)}")
            return False

    def _analyze_memory_requirements(self) -> float:
        """Analyzes memory requirements of the data."""
        try:
            # Implement memory requirement analysis
            return 0.5  # Placeholder
        except Exception as e:
            self.warnings.append(f"Memory requirements analysis failed: {str(e)}")
            return 0.0
        

    def _is_image_data(self, column: str) -> bool:
        """Checks if a column contains image data."""
        try:
            # Check if data type is bytes/object and contains image-like data
            sample = self.data[column].iloc[0]
            if isinstance(sample, (bytes, bytearray)):
                return True
            elif isinstance(sample, str):
                # Check if string contains image path patterns
                image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
                return any(ext in sample.lower() for ext in image_extensions)
            return False
        except Exception as e:
            self.warnings.append(f"Image data check failed for column {column}: {str(e)}")
            return False

    def _is_text_data(self, column: str) -> bool:
        """Checks if a column contains text data."""
        try:
            # Check if data type is object/string and contains text-like data
            if self.data[column].dtype == 'O':
                sample = str(self.data[column].iloc[0])
                # Check for text characteristics (words, sentences)
                words = len(sample.split())
                return words > 3
            return False
        except Exception as e:
            self.warnings.append(f"Text data check failed for column {column}: {str(e)}")
            return False

    def _is_time_series(self, column: str) -> bool:
        """Checks if a column contains time series data."""
        try:
            # Check if data can be converted to datetime
            if pd.api.types.is_datetime64_any_dtype(self.data[column]):
                return True
            
            # Try converting to datetime
            try:
                pd.to_datetime(self.data[column])
                return True
            except:
                pass
            
            # Check for numeric sequential patterns
            if pd.api.types.is_numeric_dtype(self.data[column]):
                # Check if values are monotonic
                return self.data[column].is_monotonic
                
            return False
        except Exception as e:
            self.warnings.append(f"Time series check failed for column {column}: {str(e)}")
            return False

    def _is_categorical(self, column: str) -> bool:
        """Checks if a column contains categorical data."""
        try:
            # Check if data type is already categorical
            if pd.api.types.is_categorical_dtype(self.data[column]):
                return True
                
            # Check number of unique values
            unique_ratio = self.data[column].nunique() / len(self.data)
            
            # If less than 5% unique values, likely categorical
            if unique_ratio < 0.05:
                return True
                
            # Check if string column with limited unique values
            if self.data[column].dtype == 'O':
                return unique_ratio < 0.2
                
            return False
        except Exception as e:
            self.warnings.append(f"Categorical check failed for column {column}: {str(e)}")
            return False

    def _is_numerical(self, column: str) -> bool:
        """Checks if a column contains numerical data."""
        try:
            # Check if data type is numeric
            if pd.api.types.is_numeric_dtype(self.data[column]):
                # Exclude likely categorical numerics
                if not self._is_categorical(column):
                    return True
            return False
        except Exception as e:
            self.warnings.append(f"Numerical check failed for column {column}: {str(e)}")
            return False

    def _is_sequential(self, column: str) -> bool:
        """Checks if a column contains sequential data."""
        try:
            # Check if already identified as time series
            if self._is_time_series(column):
                return True
                
            if pd.api.types.is_numeric_dtype(self.data[column]):
                # Check for sequential patterns
                diffs = self.data[column].diff().dropna()
                
                # Check if differences are consistent
                if len(diffs.unique()) < len(diffs) * 0.1:
                    return True
                    
            return False
        except Exception as e:
            self.warnings.append(f"Sequential check failed for column {column}: {str(e)}")
            return False
        

    def _recommend_conv_filters(self) -> List[int]:
        """Recommends number of convolutional filters for ConvLSTM layers."""
        try:
            # Base number of features in the data
            num_features = len(self.data.columns)
            
            # Calculate base number of filters
            base_filters = min(max(num_features * 2, 32), 256)
            
            # Create progression of filter sizes
            filters = [
                base_filters,
                base_filters * 2,
                base_filters * 4
            ]
            
            return [f for f in filters if f <= 512]  # Cap maximum filters
            
        except Exception as e:
            self.warnings.append(f"Conv filters recommendation failed: {str(e)}")
            return [32, 64, 128]

    def _recommend_kernel_size(self) -> Tuple[int, int]:
        """Recommends kernel size for ConvLSTM layers."""
        try:
            # Analyze spatial resolution
            spatial_res = self._analyze_spatial_resolution()
            
            # Default kernel size
            default_size = (3, 3)
            
            if spatial_res is None:
                return default_size
                
            # Adjust kernel size based on spatial resolution
            if spatial_res.get('width', 0) > 64 or spatial_res.get('height', 0) > 64:
                return (5, 5)
            
            return default_size
            
        except Exception as e:
            self.warnings.append(f"Kernel size recommendation failed: {str(e)}")
            return (3, 3)

    def _recommend_lstm_units(self) -> List[int]:
        """Recommends number of LSTM units for ConvLSTM layers."""
        try:
            # Base on data characteristics
            sequence_length = self._analyze_temporal_length()
            num_features = len(self.data.columns)
            
            # Calculate base units
            base_units = min(max(sequence_length or num_features, 32), 256)
            
            # Create decreasing progression of units
            units = [
                base_units,
                base_units // 2,
                base_units // 4
            ]
            
            return [u for u in units if u >= 16]  # Ensure minimum size
            
        except Exception as e:
            self.warnings.append(f"LSTM units recommendation failed: {str(e)}")
            return [64, 32, 16]

    def _recommend_stacked_layers(self) -> int:
        """Recommends number of stacked ConvLSTM layers."""
        try:
            # Consider data complexity and size
            data_size = len(self.data)
            feature_complexity = self._analyze_feature_complexity()
            
            # Base recommendation on data characteristics
            if data_size > 10000 and feature_complexity > 0.7:
                return 3
            elif data_size > 5000 or feature_complexity > 0.5:
                return 2
            else:
                return 1
                
        except Exception as e:
            self.warnings.append(f"Stacked layers recommendation failed: {str(e)}")
            return 2

    def _analyze_spatial_resolution(self) -> Optional[Dict[str, int]]:
        """Analyzes spatial resolution of the data."""
        try:
            # Look for image-like features
            image_features = [col for col, type_ in self._analyze_feature_types().items() 
                            if type_ == "image"]
            
            if not image_features:
                return None
                
            # Try to determine spatial dimensions
            sample = self.data[image_features[0]].iloc[0]
            
            if hasattr(sample, 'shape'):
                return {
                    "height": sample.shape[0],
                    "width": sample.shape[1]
                }
            
            return None
            
        except Exception as e:
            self.warnings.append(f"Spatial resolution analysis failed: {str(e)}")
            return None

    def _analyze_temporal_length(self) -> Optional[int]:
        """Analyzes temporal length of sequences in the data."""
        try:
            # Look for time series or sequential features
            time_features = [col for col, type_ in self._analyze_feature_types().items() 
                            if type_ in ["time_series", "sequential"]]
            
            if not time_features:
                return None
                
            # Get sequence length from first temporal feature
            sequence = self.data[time_features[0]]
            
            if hasattr(sequence, 'shape'):
                return sequence.shape[-1]
                
            # For time series, count consecutive non-null values
            return len(sequence.dropna())
            
        except Exception as e:
            self.warnings.append(f"Temporal length analysis failed: {str(e)}")
            return None

    def _analyze_spatial_temporal_patterns(self) -> float:
        """Analyzes presence and strength of spatial-temporal patterns."""
        try:
            # Check for spatial structure
            spatial_res = self._analyze_spatial_resolution()
            has_spatial = spatial_res is not None
            
            # Check for temporal structure
            temporal_length = self._analyze_temporal_length()
            has_temporal = temporal_length is not None
            
            if not (has_spatial and has_temporal):
                return 0.0
                
            # Calculate score based on data characteristics
            spatial_score = min(
                (spatial_res['height'] * spatial_res['width']) / (64 * 64), 
                1.0
            ) if spatial_res else 0.0
            
            temporal_score = min(
                temporal_length / 100, 
                1.0
            ) if temporal_length else 0.0
            
            # Combine scores
            return (spatial_score * 0.5 + temporal_score * 0.5)
            
        except Exception as e:
            self.warnings.append(f"Spatial-temporal pattern analysis failed: {str(e)}")
            return 0.0
        

    def _analyze_data_characteristics(self) -> Dict[str, Any]:
        """Analyzes general characteristics of the dataset."""
        try:
            return {
                "data_types": {
                    "numerical_columns": [col for col in self.data.columns if self._is_numerical(col)],
                    "categorical_columns": [col for col in self.data.columns if self._is_categorical(col)],
                    "text_columns": [col for col in self.data.columns if self._is_text_data(col)],
                    "time_series_columns": [col for col in self.data.columns if self._is_time_series(col)],
                    "image_columns": [col for col in self.data.columns if self._is_image_data(col)],
                    "sequential_columns": [col for col in self.data.columns if self._is_sequential(col)]
                },
                "missing_values": self.data.isnull().sum().to_dict(),
                "dimensionality": {
                    "rows": len(self.data),
                    "columns": len(self.data.columns),
                    "sparsity": self.data.isnull().sum().sum() / (len(self.data) * len(self.data.columns))
                }
            }
        except Exception as e:
            self.warnings.append(f"Data characteristics analysis failed: {str(e)}")
            return {}

    def _calculate_complexity_metrics(self) -> Dict[str, float]:
        """Calculates various complexity metrics for the dataset."""
        try:
            return {
                "feature_complexity": self._analyze_feature_complexity(),
                "distribution_complexity": self._analyze_distribution_complexity(),
                "correlation_complexity": self._analyze_feature_correlation(),
                "temporal_complexity": self._analyze_temporal_complexity()
            }
        except Exception as e:
            self.warnings.append(f"Complexity metrics calculation failed: {str(e)}")
            return {}

    def _recommend_batch_size_for_memory(self) -> int:
        """Recommends batch size based on memory constraints."""
        try:
            # Calculate memory per sample
            memory_per_sample = self.data.memory_usage(deep=True).sum() / len(self.data)
            
            # Target using no more than 10% of 16GB RAM for batches
            target_memory = (16 * 1024 * 1024 * 1024) * 0.1  # 10% of 16GB in bytes
            
            # Calculate recommended batch size
            recommended_batch_size = int(target_memory / memory_per_sample)
            
            # Constrain to reasonable bounds
            recommended_batch_size = min(max(recommended_batch_size, 16), 1024)
            
            # Round to nearest power of 2
            return 2 ** int(np.log2(recommended_batch_size))
            
        except Exception as e:
            self.warnings.append(f"Batch size recommendation failed: {str(e)}")
            return 32

    def _identify_potential_bottlenecks(self) -> Dict[str, Any]:
        """Identifies potential bottlenecks in using the data for deep learning."""
        try:
            # Analyze various potential bottlenecks
            memory_constraints = self._analyze_memory_constraints()
            preprocessing_needs = self._analyze_preprocessing_needs()
            data_quality_issues = self._analyze_data_quality_issues()
            computational_requirements = self._analyze_computational_requirements()
            
            # Combine all analyses
            return {
                "memory_constraints": memory_constraints,
                "preprocessing_needs": preprocessing_needs,
                "data_quality_issues": data_quality_issues,
                "computational_requirements": computational_requirements
            }
            
        except Exception as e:
            self.warnings.append(f"Bottleneck identification failed: {str(e)}")
            return {}


    def _analyze_preprocessing_needs(self) -> Dict[str, List[str]]:
        """Analyzes preprocessing requirements."""
        try:
            needs = {
                "critical": [],
                "recommended": [],
                "optional": []
            }
            
            # Check for missing values
            missing_ratio = self.data.isnull().mean().mean()
            if missing_ratio > 0.1:
                needs["critical"].append("missing_value_handling")
            elif missing_ratio > 0:
                needs["recommended"].append("missing_value_handling")
                
            # Check for categorical variables
            categorical_cols = [col for col in self.data.columns 
                            if self.data[col].dtype == 'object']
            if categorical_cols:
                needs["critical"].append("categorical_encoding")
                
            # Check for scaling needs
            numeric_cols = self.data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                needs["recommended"].append("feature_scaling")
                
            # Check for dimensionality
            if len(self.data.columns) > 100:
                needs["recommended"].append("dimensionality_reduction")
                
            return needs
            
        except Exception as e:
            self.warnings.append(f"Preprocessing needs analysis failed: {str(e)}")
            return {"critical": [], "recommended": [], "optional": []}

    def _analyze_data_quality_issues(self) -> Dict[str, Any]:
        """Analyzes data quality issues."""
        try:
            issues = {}
            
            # Check missing values
            missing_ratios = self.data.isnull().mean()
            issues["missing_values"] = {
                "columns_with_missing": missing_ratios[missing_ratios > 0].to_dict(),
                "total_missing_ratio": missing_ratios.mean()
            }
            
            # Check duplicates
            duplicate_ratio = len(self.data[self.data.duplicated()]) / len(self.data)
            issues["duplicates"] = {
                "duplicate_ratio": duplicate_ratio,
                "needs_attention": duplicate_ratio > 0.01
            }
            
            # Check outliers in numeric columns
            numeric_cols = self.data.select_dtypes(include=[np.number]).columns
            outlier_info = {}
            for col in numeric_cols:
                Q1 = self.data[col].quantile(0.25)
                Q3 = self.data[col].quantile(0.75)
                IQR = Q3 - Q1
                outlier_ratio = len(self.data[(self.data[col] < Q1 - 1.5*IQR) | 
                                            (self.data[col] > Q3 + 1.5*IQR)]) / len(self.data)
                if outlier_ratio > 0.01:
                    outlier_info[col] = outlier_ratio
                    
            issues["outliers"] = outlier_info
            
            return issues
            
        except Exception as e:
            self.warnings.append(f"Data quality analysis failed: {str(e)}")
            return {}

    def _analyze_computational_requirements(self) -> Dict[str, Any]:
        """Analyzes computational requirements."""
        try:
            num_samples = len(self.data)
            num_features = len(self.data.columns)
            
            return {
                "estimated_training_time": self._estimate_training_time(),
                "gpu_recommended": num_samples * num_features > 1000000,
                "parallelization_recommended": num_samples > 10000,
                "memory_requirements": {
                    "minimum_ram_gb": round(self.data.memory_usage(deep=True).sum() / (1024**3) * 3, 2),
                    "recommended_ram_gb": round(self.data.memory_usage(deep=True).sum() / (1024**3) * 5, 2)
                }
            }
            
        except Exception as e:
            self.warnings.append(f"Computational requirements analysis failed: {str(e)}")
            return {}

    def _estimate_training_time(self) -> str:
        """Estimates training time based on data characteristics."""
        try:
            num_samples = len(self.data)
            num_features = len(self.data.columns)
            
            # Very rough estimation
            if num_samples * num_features > 10000000:
                return "several hours"
            elif num_samples * num_features > 1000000:
                return "about an hour"
            elif num_samples * num_features > 100000:
                return "several minutes"
            else:
                return "few minutes"
                
        except Exception as e:
            self.warnings.append(f"Training time estimation failed: {str(e)}")
            return "unknown"

    def _analyze_feature_complexity(self) -> float:
        """Analyzes complexity of features."""
        try:
            # Implement feature complexity analysis
            return 0.5  # Placeholder
        except Exception as e:
            self.warnings.append(f"Feature complexity analysis failed: {str(e)}")
            return 0.0

    def _analyze_temporal_complexity(self) -> float:
        """Analyzes temporal complexity of the data."""
        try:
            # Implement temporal complexity analysis
            return 0.5  # Placeholder
        except Exception as e:
            self.warnings.append(f"Temporal complexity analysis failed: {str(e)}")
            return 0.0
        

    def _calculate_bilstm_score(self) -> float:
        """Calculates compatibility score for Bidirectional LSTM architecture."""
        try:
            # Check for sequential/time series data
            sequence_features = [col for col, type_ in self._analyze_feature_types().items() 
                            if type_ in ["sequential", "time_series", "text"]]
            
            if not sequence_features:
                return 0.0
            
            # Analyze bidirectional importance
            bidirectional_score = self._analyze_bidirectional_importance()
            
            # Analyze sequence quality
            sequence_quality = self._analyze_sequence_quality()
            quality_score = (
                sequence_quality.get('completeness', 0.0) * 0.4 +
                sequence_quality.get('consistency', 0.0) * 0.3 +
                (1 - sequence_quality.get('noise_level', 1.0)) * 0.3
            )
            
            # Calculate final score
            final_score = (bidirectional_score * 0.6 + quality_score * 0.4)
            return min(max(final_score, 0.0), 1.0)
            
        except Exception as e:
            self.warnings.append(f"BiLSTM score calculation failed: {str(e)}")
            return 0.0

    def _analyze_bidirectional_importance(self) -> float:
        """Analyzes importance of bidirectional processing for the sequences."""
        try:
            # Get main sequence for analysis
            sequence = self._get_main_sequence()
            if sequence is None:
                return 0.0
            
            # Calculate forward and backward correlations
            forward_corr = self._calculate_forward_correlation(sequence)
            backward_corr = self._calculate_backward_correlation(sequence)
            
            # If both directions show significant correlation, bidirectional is important
            importance = max(min(forward_corr + backward_corr, 1.0), 0.0)
            
            return importance
            
        except Exception as e:
            self.warnings.append(f"Bidirectional importance analysis failed: {str(e)}")
            return 0.0

    def _recommend_bilstm_layers(self) -> int:
        """Recommends number of BiLSTM layers based on data complexity."""
        try:
            # Analyze sequence complexity
            sequence_length = self._analyze_sequence_length()
            feature_complexity = self._analyze_feature_complexity()
            
            if sequence_length is None:
                return 2  # Default recommendation
                
            # Recommend layers based on sequence length and complexity
            if sequence_length > 100 and feature_complexity > 0.7:
                return 3
            elif sequence_length > 50 or feature_complexity > 0.5:
                return 2
            else:
                return 1
                
        except Exception as e:
            self.warnings.append(f"BiLSTM layers recommendation failed: {str(e)}")
            return 2

    def _recommend_dropout_rate(self) -> float:
        """Recommends dropout rate for BiLSTM layers."""
        try:
            # Analyze overfitting risk
            num_samples = len(self.data)
            num_features = len(self.data.columns)
            sequence_length = self._analyze_sequence_length() or 1
            
            # Calculate complexity ratio
            complexity_ratio = (num_features * sequence_length) / num_samples
            
            # Recommend dropout based on complexity ratio
            if complexity_ratio > 1.0:
                return 0.5  # High dropout for complex models
            elif complexity_ratio > 0.5:
                return 0.3  # Medium dropout
            else:
                return 0.2  # Low dropout
                
        except Exception as e:
            self.warnings.append(f"Dropout rate recommendation failed: {str(e)}")
            return 0.3

    def _recommend_merge_mode(self) -> str:
        """Recommends merge mode for combining forward and backward states."""
        try:
            # Analyze sequence characteristics
            sequence_quality = self._analyze_sequence_quality()
            bidirectional_importance = self._analyze_bidirectional_importance()
            
            # Choose merge mode based on characteristics
            if bidirectional_importance > 0.8:
                return "concat"  # Preserve most information
            elif sequence_quality.get('noise_level', 0.0) > 0.5:
                return "ave"     # Average to reduce noise
            else:
                return "mul"     # Multiplicative interaction
                
        except Exception as e:
            self.warnings.append(f"Merge mode recommendation failed: {str(e)}")
            return "concat"

    def _calculate_forward_correlation(self, sequence: pd.Series) -> float:
        """Calculates forward temporal correlation in sequence."""
        try:
            # Calculate lag-1 correlation
            if len(sequence) < 2:
                return 0.0
                
            forward_corr = sequence.autocorr(1)
            return abs(forward_corr) if not pd.isna(forward_corr) else 0.0
            
        except Exception as e:
            self.warnings.append(f"Forward correlation calculation failed: {str(e)}")
            return 0.0

    def _calculate_backward_correlation(self, sequence: pd.Series) -> float:
        """Calculates backward temporal correlation in sequence."""
        try:
            # Calculate correlation with next value
            if len(sequence) < 2:
                return 0.0
                
            backward_corr = sequence[::-1].autocorr(1)
            return abs(backward_corr) if not pd.isna(backward_corr) else 0.0
            
        except Exception as e:
            self.warnings.append(f"Backward correlation calculation failed: {str(e)}")
            return 0.0

    def _get_main_sequence(self) -> Optional[pd.Series]:
        """Gets the main sequence from the data for analysis."""
        try:
            # If target is specified and is sequential, use it
            if self.target and any(t in self._analyze_feature_types()[self.target] 
                                for t in ["sequential", "time_series", "text"]):
                return self.data[self.target]
                
            # Otherwise, look for sequential columns
            sequence_cols = [col for col, type_ in self._analyze_feature_types().items() 
                            if type_ in ["sequential", "time_series", "text"]]
            
            if sequence_cols:
                return self.data[sequence_cols[0]]
                
            return None
            
        except Exception as e:
            self.warnings.append(f"Main sequence extraction failed: {str(e)}")
            return None
        


    def _calculate_tcn_score(self) -> float:
        """Calculates compatibility score for Temporal Convolutional Network."""
        try:
            # Check for sequential/time series data
            sequence_features = [col for col, type_ in self._analyze_feature_types().items() 
                            if type_ in ["sequential", "time_series"]]
            
            if not sequence_features:
                return 0.0
            
            # Analyze key characteristics
            sequence_length = self._analyze_sequence_length() or 0
            receptive_field = self._calculate_receptive_field()
            causal_importance = float(self._check_causality_requirement())
            
            # Calculate subscores
            length_score = min(sequence_length / 1000, 1.0)
            coverage_score = min(receptive_field / sequence_length, 1.0) if sequence_length > 0 else 0.0
            
            # Combine scores with weights
            final_score = (
                length_score * 0.3 +
                coverage_score * 0.4 +
                causal_importance * 0.3
            )
            
            return min(max(final_score, 0.0), 1.0)
            
        except Exception as e:
            self.warnings.append(f"TCN score calculation failed: {str(e)}")
            return 0.0
        



    def _analyze_memory_constraints(self) -> Dict[str, Any]:
        """Analyzes memory constraints and requirements."""
        try:
            # Get current dataset memory usage
            data_memory = self.data.memory_usage(deep=True).sum()
            data_memory_gb = data_memory / (1024 ** 3)  # Convert to GB
            
            # Estimate memory requirements for different operations
            num_samples = len(self.data)
            num_features = len(self.data.columns)
            
            # Estimate batch processing memory
            batch_size = min(num_samples, 1024)
            batch_memory_gb = (data_memory_gb / num_samples) * batch_size
            
            # Estimate model memory (rough approximation)
            model_memory_gb = (num_features * 4 * 1000) / (1024 ** 3)  # Assuming 4 bytes per parameter
            
            return {
                "current_data_size_gb": round(data_memory_gb, 3),
                "estimated_batch_memory_gb": round(batch_memory_gb, 3),
                "estimated_model_memory_gb": round(model_memory_gb, 3),
                "total_estimated_memory_gb": round(data_memory_gb + model_memory_gb, 3),
                "recommendations": {
                    "batch_size": self._recommend_batch_size_for_memory(),
                    "memory_efficient_mode": data_memory_gb > 1.0,
                    "needs_data_reduction": data_memory_gb > 10.0
                }
            }
            
        except Exception as e:
            self.warnings.append(f"Memory constraints analysis failed: {str(e)}")
            return {
                "current_data_size_gb": 0.0,
                "recommendations": {
                    "batch_size": 32,
                    "memory_efficient_mode": False,
                    "needs_data_reduction": False
                }
            }

    def _recommend_tcn_filters(self) -> List[int]:
        """Recommends number of filters for TCN layers."""
        try:
            num_features = len(self.data.columns)
            sequence_length = self._analyze_sequence_length() or 0
            
            # Base number of filters on data characteristics
            base_filters = min(max(num_features * 2, 32), 128)
            
            # Create growing progression of filters
            filters = [
                base_filters,
                base_filters * 2,
                base_filters * 4
            ]
            
            # Adjust for very long sequences
            if sequence_length > 1000:
                filters = [f * 2 for f in filters]
            
            return [f for f in filters if f <= 512]  # Cap maximum filters
            
        except Exception as e:
            self.warnings.append(f"TCN filters recommendation failed: {str(e)}")
            return [64, 128, 256]

    def _recommend_tcn_kernel(self) -> int:
        """Recommends kernel size for TCN layers."""
        try:
            sequence_length = self._analyze_sequence_length() or 0
            
            # Adjust kernel size based on sequence length
            if sequence_length > 1000:
                return 7
            elif sequence_length > 100:
                return 5
            else:
                return 3
                
        except Exception as e:
            self.warnings.append(f"TCN kernel recommendation failed: {str(e)}")
            return 3

    def _recommend_dilation_base(self) -> int:
        """Recommends dilation base for TCN layers."""
        try:
            sequence_length = self._analyze_sequence_length() or 0
            
            # Choose dilation base based on sequence length
            if sequence_length > 1000:
                return 4
            elif sequence_length > 100:
                return 2
            else:
                return 2
                
        except Exception as e:
            self.warnings.append(f"Dilation base recommendation failed: {str(e)}")
            return 2

    def _recommend_tcn_levels(self) -> int:
        """Recommends number of TCN levels (determines receptive field)."""
        try:
            sequence_length = self._analyze_sequence_length() or 0
            
            # Calculate number of levels needed to cover sequence length
            kernel_size = self._recommend_tcn_kernel()
            dilation_base = self._recommend_dilation_base()
            
            if sequence_length <= 1:
                return 1
                
            # Calculate levels needed to achieve desired receptive field
            receptive_field = kernel_size
            levels = 1
            
            while receptive_field < sequence_length and levels < 10:
                levels += 1
                receptive_field += (kernel_size - 1) * dilation_base ** (levels - 1)
            
            return min(levels, 8)  # Cap maximum levels
            
        except Exception as e:
            self.warnings.append(f"TCN levels recommendation failed: {str(e)}")
            return 4

    def _calculate_receptive_field(self) -> int:
        """Calculates receptive field size of recommended TCN architecture."""
        try:
            kernel_size = self._recommend_tcn_kernel()
            num_levels = self._recommend_tcn_levels()
            dilation_base = self._recommend_dilation_base()
            
            # Calculate total receptive field
            receptive_field = kernel_size
            for level in range(1, num_levels):
                receptive_field += (kernel_size - 1) * dilation_base ** level
                
            return receptive_field
            
        except Exception as e:
            self.warnings.append(f"Receptive field calculation failed: {str(e)}")
            return 0

    def _check_causality_requirement(self) -> bool:
        """Checks if causal convolutions are required for the task."""
        try:
            # Check if we're doing time series prediction
            if self.target and self._is_time_series(self.target):
                return True
                
            # Check if we have multiple time series features
            time_series_features = [col for col, type_ in self._analyze_feature_types().items() 
                                if type_ == "time_series"]
            
            if len(time_series_features) > 0:
                return True
                
            return False
            
        except Exception as e:
            self.warnings.append(f"Causality requirement check failed: {str(e)}")
            return True  # Default to causal to be safe
        


    def _analyze_deepar_compatibility(self) -> Dict[str, Any]:
        """Analyzes compatibility with DeepAR (Deep Auto-Regressive) architecture."""
        try:
            # Calculate base compatibility score
            score = self._calculate_deepar_score()
            
            return {
                "compatibility_score": score,
                "architecture_recommendations": {
                    "num_layers": self._recommend_deepar_layers(),
                    "hidden_size": self._recommend_deepar_hidden_size(),
                    "likelihood": self._recommend_likelihood_model(),
                    "context_length": self._recommend_context_length()
                },
                "data_requirements": {
                    "minimum_length": 100,
                    "recommended_length": 1000,
                    "current_length": len(self.data)
                },
                "probabilistic_features": {
                    "supports_uncertainty": True,
                    "distribution_type": self._recommend_distribution_type(),
                    "quantile_levels": [0.1, 0.5, 0.9]
                },
                "preprocessing_requirements": [
                    "scaling",
                    "missing_value_handling",
                    "feature_normalization"
                ]
            }
        except Exception as e:
            self.warnings.append(f"DeepAR compatibility analysis failed: {str(e)}")
            return {"compatibility_score": 0.0}

    def _calculate_deepar_score(self) -> float:
        """Calculates compatibility score for DeepAR model."""
        try:
            # Check for time series features
            time_series_features = [col for col, type_ in self._analyze_feature_types().items() 
                                if type_ == "time_series"]
            
            if not time_series_features:
                return 0.0
            
            # Analyze key characteristics
            data_length = len(self.data)
            has_multiple_series = len(time_series_features) > 1
            seasonality_info = self._analyze_seasonality()
            stationarity_results = self._check_stationarity()
            
            # Calculate subscores
            length_score = min(data_length / 1000, 1.0)
            multiple_series_score = 0.3 if has_multiple_series else 0.0
            seasonality_score = min(seasonality_info.get('seasonality_strength', 0.0), 1.0)
            stationarity_score = 0.7 if stationarity_results.get('is_stationary', False) else 0.3
            
            # Combine scores
            final_score = (
                length_score * 0.3 +
                multiple_series_score * 0.2 +
                seasonality_score * 0.3 +
                stationarity_score * 0.2
            )
            
            return min(max(final_score, 0.0), 1.0)
            
        except Exception as e:
            self.warnings.append(f"DeepAR score calculation failed: {str(e)}")
            return 0.0

    def _recommend_deepar_layers(self) -> int:
        """Recommends number of layers for DeepAR model."""
        try:
            data_size = len(self.data)
            feature_complexity = self._analyze_feature_complexity()
            
            if data_size > 10000 and feature_complexity > 0.7:
                return 3
            elif data_size > 5000 or feature_complexity > 0.5:
                return 2
            else:
                return 1
                
        except Exception as e:
            self.warnings.append(f"DeepAR layers recommendation failed: {str(e)}")
            return 2

    def _recommend_deepar_hidden_size(self) -> int:
        """Recommends hidden size for DeepAR model."""
        try:
            num_features = len(self.data.columns)
            sequence_length = self._analyze_sequence_length() or 0
            
            # Base hidden size on data characteristics
            base_size = min(max(num_features * 4, sequence_length // 4, 32), 256)
            
            # Round to nearest power of 2
            return 2 ** int(np.log2(base_size))
            
        except Exception as e:
            self.warnings.append(f"DeepAR hidden size recommendation failed: {str(e)}")
            return 64

    def _recommend_likelihood_model(self) -> str:
        """Recommends likelihood model for DeepAR predictions."""
        try:
            # Analyze target variable characteristics
            if self.target is None:
                return "gaussian"
                
            target_data = self.data[self.target]
            
            # Check for count data
            if all(target_data.dropna() >= 0) and all(target_data.dropna().round() == target_data.dropna()):
                return "negative_binomial"
                
            # Check for heavy tails
            kurtosis = stats.kurtosis(target_data.dropna())
            if abs(kurtosis) > 3:
                return "student_t"
                
            return "gaussian"
            
        except Exception as e:
            self.warnings.append(f"Likelihood model recommendation failed: {str(e)}")
            return "gaussian"

    def _recommend_context_length(self) -> int:
        """Recommends context length for DeepAR model."""
        try:
            # Get seasonality information
            period = self._detect_period()
            
            # Context length should cover at least 2 seasonal periods
            if period > 1:
                return min(period * 2, len(self.data) // 4)
            
            # Default to sequence length based recommendation
            sequence_length = self._analyze_sequence_length() or 0
            return min(max(sequence_length // 4, 30), sequence_length)
            
        except Exception as e:
            self.warnings.append(f"Context length recommendation failed: {str(e)}")
            return 30

    def _recommend_distribution_type(self) -> str:
        """Recommends probability distribution type for DeepAR model."""
        try:
            if self.target is None:
                return "gaussian"
                
            target_data = self.data[self.target]
            
            # Check data characteristics
            is_count = all(target_data.dropna() >= 0) and all(target_data.dropna().round() == target_data.dropna())
            is_positive = all(target_data.dropna() > 0)
            skewness = stats.skew(target_data.dropna())
            kurtosis = stats.kurtosis(target_data.dropna())
            
            if is_count:
                return "negative_binomial"
            elif is_positive and skewness > 1:
                return "gamma"
            elif abs(kurtosis) > 3:
                return "student_t"
            else:
                return "gaussian"
                
        except Exception as e:
            self.warnings.append(f"Distribution type recommendation failed: {str(e)}")
            return "gaussian"
        

    def _analyze_tft_compatibility(self) -> Dict[str, Any]:
        """Analyzes compatibility with Temporal Fusion Transformer architecture."""
        try:
            # Calculate base compatibility score
            score = self._calculate_tft_score()
            
            return {
                "compatibility_score": score,
                "architecture_recommendations": {
                    "hidden_size": self._recommend_tft_hidden_size(),
                    "attention_heads": self._recommend_attention_heads(),
                    "dropout_rate": self._recommend_tft_dropout(),
                    "num_layers": self._recommend_tft_layers()
                },
                "variable_selection": {
                    "known_future": self._identify_known_future_inputs(),
                    "static": self._identify_static_features(),
                    "time_varying": self._identify_time_varying_features()
                },
                "temporal_parameters": {
                    "context_length": self._recommend_tft_context_length(),
                    "forecast_horizon": self._recommend_tft_horizon()
                },
                "preprocessing_requirements": [
                    "variable_categorization",
                    "scaling",
                    "missing_value_handling",
                    "temporal_alignment"
                ]
            }
        except Exception as e:
            self.warnings.append(f"TFT compatibility analysis failed: {str(e)}")
            return {"compatibility_score": 0.0}

    def _calculate_tft_score(self) -> float:
        """Calculates compatibility score for TFT model."""
        try:
            # Check for required data characteristics
            time_varying_features = self._identify_time_varying_features()
            static_features = self._identify_static_features()
            known_future = self._identify_known_future_inputs()
            
            # Calculate base scores
            data_complexity_score = min(len(time_varying_features) / 10, 1.0)
            static_score = min(len(static_features) / 5, 1.0)
            future_score = min(len(known_future) / 3, 1.0)
            
            # Check data volume
            data_volume_score = min(len(self.data) / 5000, 1.0)
            
            # Combine scores with weights
            final_score = (
                data_complexity_score * 0.4 +
                static_score * 0.2 +
                future_score * 0.2 +
                data_volume_score * 0.2
            )
            
            return min(max(final_score, 0.0), 1.0)
            
        except Exception as e:
            self.warnings.append(f"TFT score calculation failed: {str(e)}")
            return 0.0

    def _recommend_tft_hidden_size(self) -> int:
        """Recommends hidden layer size for TFT model."""
        try:
            num_features = len(self.data.columns)
            time_varying = len(self._identify_time_varying_features())
            
            # Base size on feature counts
            base_size = min(max(num_features * 2, time_varying * 4, 32), 256)
            
            # Round to nearest multiple of 8 for attention heads compatibility
            return (base_size // 8) * 8
            
        except Exception as e:
            self.warnings.append(f"TFT hidden size recommendation failed: {str(e)}")
            return 64

    def _recommend_attention_heads(self) -> int:
        """Recommends number of attention heads for TFT model."""
        try:
            hidden_size = self._recommend_tft_hidden_size()
            
            # Number of heads should divide hidden size
            possible_heads = [2, 4, 8]
            valid_heads = [h for h in possible_heads if hidden_size % h == 0]
            
            if not valid_heads:
                return 4
            
            # Choose based on complexity
            if len(self.data) > 10000:
                return max(valid_heads)
            elif len(self.data) > 5000:
                return valid_heads[len(valid_heads)//2]
            else:
                return min(valid_heads)
                
        except Exception as e:
            self.warnings.append(f"Attention heads recommendation failed: {str(e)}")
            return 4

    def _recommend_tft_dropout(self) -> float:
        """Recommends dropout rate for TFT model."""
        try:
            # Consider feature counts and data volume
            num_features = len(self.data.columns)
            data_points = len(self.data)
            
            # Calculate complexity ratio
            complexity_ratio = num_features / (data_points ** 0.5)
            
            if complexity_ratio > 1.0:
                return 0.3
            elif complexity_ratio > 0.5:
                return 0.2
            else:
                return 0.1
                
        except Exception as e:
            self.warnings.append(f"TFT dropout recommendation failed: {str(e)}")
            return 0.2

    def _recommend_tft_layers(self) -> int:
        """Recommends number of layers for TFT model."""
        try:
            # Base on data volume and feature complexity
            data_points = len(self.data)
            feature_complexity = len(self._identify_time_varying_features())
            
            if data_points > 10000 and feature_complexity > 10:
                return 3
            elif data_points > 5000 or feature_complexity > 5:
                return 2
            else:
                return 1
                
        except Exception as e:
            self.warnings.append(f"TFT layers recommendation failed: {str(e)}")
            return 2

    def _identify_known_future_inputs(self) -> List[str]:
        """Identifies variables that are known in advance with proper type handling."""
        try:
            future_inputs = []
            feature_types = self._analyze_feature_types()
            
            for col in self.data.columns:
                if col != self.target and feature_types.get(col) == "time_series":
                    # Convert to numeric if possible
                    try:
                        series = pd.to_numeric(self.data[col], errors='coerce')
                        series = series.dropna()
                        
                        if len(series) > 1:
                            # Check if values follow a pattern
                            diff = series.diff().dropna()
                            if len(diff) > 0 and diff.std() < diff.mean() * 0.1:
                                future_inputs.append(col)
                    except:
                        continue
                        
            return future_inputs
            
        except Exception as e:
            self.warnings.append(f"Known future inputs identification failed: {str(e)}")
            return []

    def _identify_static_features(self) -> List[str]:
        """Identifies static (non-time-varying) features."""
        try:
            static_features = []
            
            for col in self.data.columns:
                if col != self.target:
                    # Check if values are constant or nearly constant
                    unique_ratio = self.data[col].nunique() / len(self.data)
                    if unique_ratio < 0.01:
                        static_features.append(col)
                        
            return static_features
            
        except Exception as e:
            self.warnings.append(f"Static features identification failed: {str(e)}")
            return []

    def _identify_time_varying_features(self) -> List[str]:
        """Identifies time-varying features."""
        try:
            known_future = self._identify_known_future_inputs()
            static_features = self._identify_static_features()
            
            # Time varying features are those that are neither static nor known future
            time_varying = [col for col in self.data.columns 
                        if col not in static_features 
                        and col not in known_future 
                        and col != self.target]
            
            return time_varying
            
        except Exception as e:
            self.warnings.append(f"Time varying features identification failed: {str(e)}")
            return []

    def _recommend_tft_context_length(self) -> int:
        """Recommends context length for TFT model."""
        try:
            # Consider seasonality for context length
            period = self._detect_period()
            sequence_length = self._analyze_sequence_length() or 0
            
            if period > 1:
                # At least 2 seasonal periods
                context_length = min(period * 2, sequence_length // 4)
            else:
                # Default to sequence length based
                context_length = min(sequence_length // 4, 100)
                
            return max(context_length, 10)  # Ensure minimum context
            
        except Exception as e:
            self.warnings.append(f"TFT context length recommendation failed: {str(e)}")
            return 30

    def _recommend_tft_horizon(self) -> int:
        """Recommends forecast horizon for TFT model."""
        try:
            sequence_length = self._analyze_sequence_length() or 0
            period = self._detect_period()
            
            if period > 1:
                # One full season
                horizon = min(period, sequence_length // 8)
            else:
                # Default based on sequence length
                horizon = min(sequence_length // 8, 50)
                
            return max(horizon, 5)  # Ensure minimum horizon
            
        except Exception as e:
            self.warnings.append(f"TFT horizon recommendation failed: {str(e)}")
            return 10




    def _analyze_nbeats_compatibility(self) -> Dict[str, Any]:
        """Analyzes compatibility with N-BEATS architecture."""
        try:
            # Calculate base compatibility score
            score = self._calculate_nbeats_score()
            
            return {
                "compatibility_score": score,
                "architecture_recommendations": {
                    "stack_types": self._recommend_stack_types(),
                    "num_blocks": self._recommend_num_blocks(),
                    "hidden_layer_units": self._recommend_nbeats_hidden_units(),
                    "thetas_dims": self._recommend_thetas_dims()
                },
                "forecast_parameters": {
                    "backcast_length": self._recommend_backcast_length(),
                    "forecast_length": self._recommend_forecast_length()
                },
                "interpretability": {
                    "supports_decomposition": True,
                    "trend_analysis": True,
                    "seasonality_analysis": True
                },
                "preprocessing_requirements": [
                    "scaling",
                    "missing_value_handling"
                ]
            }
        except Exception as e:
            self.warnings.append(f"N-BEATS compatibility analysis failed: {str(e)}")
            return {"compatibility_score": 0.0}

    def _calculate_nbeats_score(self) -> float:
        """Calculates compatibility score for N-BEATS model with proper error handling."""
        try:
            if self.target is None:
                return 0.0
                
            # Get seasonality info safely
            seasonality_info = self._analyze_seasonality()
            seasonality_strength = seasonality_info.get('seasonality_strength', 0.0)
            
            # Check trend presence
            has_trend = self._check_trend_presence()
            
            # Get data length
            data_length = len(self.data)
            
            # Calculate subscores
            seasonality_score = min(float(seasonality_strength), 1.0)
            trend_score = 0.8 if has_trend else 0.2
            length_score = min(data_length / 1000, 1.0)
            
            # Combine scores
            final_score = (
                seasonality_score * 0.4 +
                trend_score * 0.3 +
                length_score * 0.3
            )
            
            return min(max(final_score, 0.0), 1.0)
            
        except Exception as e:
            self.warnings.append(f"N-BEATS score calculation failed: {str(e)}")
            return 0.0

    def _recommend_stack_types(self) -> List[str]:
        """Recommends stack types for N-BEATS model with proper error handling."""
        try:
            # Get seasonality info safely
            seasonality_info = self._analyze_seasonality()
            has_seasonality = seasonality_info.get('has_seasonality', False)
            
            # Check trend
            has_trend = self._check_trend_presence()
            
            stacks = []
            
            # Add trend stack if trend is present
            if has_trend:
                stacks.append("trend")
                
            # Add seasonality stack if seasonality is present
            if has_seasonality:
                stacks.append("seasonality")
                
            # Always include generic stack for flexibility
            stacks.append("generic")
            
            return stacks
            
        except Exception as e:
            self.warnings.append(f"Stack types recommendation failed: {str(e)}")
            return ["generic"]

    def _recommend_num_blocks(self) -> Dict[str, int]:
        """Recommends number of blocks per stack."""
        try:
            data_size = len(self.data)
            
            # Base number of blocks on data size
            if data_size > 10000:
                base_blocks = 3
            elif data_size > 5000:
                base_blocks = 2
            else:
                base_blocks = 1
                
            # Recommend blocks for each stack type
            return {
                "trend": base_blocks,
                "seasonality": base_blocks * 2,
                "generic": base_blocks * 3
            }
            
        except Exception as e:
            self.warnings.append(f"Number of blocks recommendation failed: {str(e)}")
            return {"trend": 1, "seasonality": 2, "generic": 3}

    def _recommend_nbeats_hidden_units(self) -> int:
        """Recommends number of hidden units per block."""
        try:
            data_size = len(self.data)
            sequence_length = self._analyze_sequence_length() or 0
            
            # Base units on data characteristics
            base_units = min(max(sequence_length * 2, 64), 512)
            
            # Adjust based on data size
            if data_size > 10000:
                base_units *= 2
            elif data_size < 1000:
                base_units = max(base_units // 2, 64)
                
            return base_units
            
        except Exception as e:
            self.warnings.append(f"Hidden units recommendation failed: {str(e)}")
            return 128

    def _recommend_thetas_dims(self) -> Dict[str, List[int]]:
        """Recommends dimensions for basis expansion coefficients."""
        try:
            period = self._detect_period()
            forecast_length = self._recommend_forecast_length()
            
            return {
                "trend": [2, forecast_length],  # Linear trend
                "seasonality": [min(period * 2, forecast_length * 2)],  # Seasonal components
                "generic": [forecast_length * 2]  # Generic basis
            }
            
        except Exception as e:
            self.warnings.append(f"Thetas dimensions recommendation failed: {str(e)}")
            return {"trend": [2], "seasonality": [8], "generic": [16]}

    def _recommend_backcast_length(self) -> int:
        """Recommends backcast length for N-BEATS model."""
        try:
            period = self._detect_period()
            forecast_length = self._recommend_forecast_length()
            
            if period > 1:
                # Use multiple of seasonal period
                backcast_length = period * 2
            else:
                # Default to 3x forecast length
                backcast_length = forecast_length * 3
                
            return min(backcast_length, len(self.data) // 4)
            
        except Exception as e:
            self.warnings.append(f"Backcast length recommendation failed: {str(e)}")
            return 30

    def _recommend_forecast_length(self) -> int:
        """Recommends forecast length for N-BEATS model."""
        try:
            period = self._detect_period()
            sequence_length = self._analyze_sequence_length() or 0
            
            if period > 1:
                # One seasonal period
                forecast_length = period
            else:
                # Default based on sequence length
                forecast_length = max(sequence_length // 8, 5)
                
            return min(forecast_length, sequence_length // 4)
            
        except Exception as e:
            self.warnings.append(f"Forecast length recommendation failed: {str(e)}")
            return 10

    def _check_trend_presence(self) -> bool:
        """Checks for significant trend with proper type handling."""
        try:
            if self.target is None:
                return False
                
            # Convert to numeric and handle missing values
            try:
                series = pd.to_numeric(self.data[self.target], errors='coerce')
                series = series.fillna(method='ffill').fillna(method='bfill')
                
                if len(series) < 2:
                    return False
                    
                # Perform Mann-Kendall test
                result = stats.kendalltau(range(len(series)), series)
                return bool(result.pvalue < 0.05)
            except:
                return False
                
        except Exception as e:
            self.warnings.append(f"Trend presence check failed: {str(e)}")
            return False
        


    def _calculate_sequence_completeness(self) -> float:
        """Calculates the completeness ratio of sequences."""
        try:
            if self.target is None:
                return 0.0
                
            # Calculate ratio of non-null values
            series = self.data[self.target]
            completeness = series.notna().mean()
            
            return float(completeness)
            
        except Exception as e:
            self.warnings.append(f"Sequence completeness calculation failed: {str(e)}")
            return 0.0

    def _calculate_sequence_consistency(self) -> float:
        """Calculates the consistency of time intervals in sequences."""
        try:
            # Get time-based columns
            time_cols = [col for col, type_ in self._analyze_feature_types().items() 
                        if type_ == "time_series"]
            
            if not time_cols:
                return 0.0
                
            # Check first time column
            try:
                times = pd.to_datetime(self.data[time_cols[0]], errors='coerce')
                times = times.dropna()
                
                if len(times) < 2:
                    return 0.0
                    
                # Calculate intervals
                intervals = times.diff()[1:]
                mean_interval = intervals.mean()
                std_interval = intervals.std()
                
                if pd.isna(mean_interval) or pd.isna(std_interval) or mean_interval.total_seconds() == 0:
                    return 0.0
                    
                # Calculate consistency score
                cv = std_interval.total_seconds() / mean_interval.total_seconds()
                consistency = 1.0 / (1.0 + cv)
                
                return float(consistency)
                
            except:
                return 0.0
                
        except Exception as e:
            self.warnings.append(f"Sequence consistency calculation failed: {str(e)}")
            return 0.0

    def _estimate_sequence_noise(self) -> float:
        """Estimates noise level in sequences."""
        try:
            if self.target is None:
                return 1.0
                
            # Convert to numeric and handle missing values
            try:
                series = pd.to_numeric(self.data[self.target], errors='coerce')
                series = series.fillna(method='ffill').fillna(method='bfill')
                
                if len(series) < 2:
                    return 1.0
                    
                # Calculate noise using rolling statistics
                window = min(len(series) // 10, 10)
                if window < 2:
                    return 1.0
                    
                rolling_mean = series.rolling(window=window).mean()
                residuals = series - rolling_mean
                
                # Calculate noise ratio
                signal_power = np.std(rolling_mean)
                noise_power = np.std(residuals)
                
                if signal_power == 0:
                    return 1.0
                    
                noise_ratio = noise_power / signal_power
                return min(float(noise_ratio), 1.0)
                
            except:
                return 1.0
                
        except Exception as e:
            self.warnings.append(f"Sequence noise estimation failed: {str(e)}")
            return 1.0

    def _analyze_sequence_quality(self) -> Dict[str, float]:
        """Analyzes the quality of sequences in the data."""
        try:
            completeness = self._calculate_sequence_completeness()
            consistency = self._calculate_sequence_consistency()
            noise_level = self._estimate_sequence_noise()
            
            return {
                "completeness": completeness,
                "consistency": consistency,
                "noise_level": noise_level
            }
            
        except Exception as e:
            self.warnings.append(f"Sequence quality analysis failed: {str(e)}")
            return {"completeness": 0.0, "consistency": 0.0, "noise_level": 1.0}

    def _recommend_bilstm_units(self) -> List[int]:
        """Recommends number of units for BiLSTM layers with proper error handling."""
        try:
            sequence_length = self._analyze_sequence_length()
            feature_dim = len(self.data.columns)
            
            # Base number of units with safe comparison
            if sequence_length is None:
                base_units = feature_dim
            else:
                base_units = max(sequence_length, feature_dim)
                
            base_units = min(base_units, 512)
            
            # Create decreasing layer sizes
            units = [
                base_units,
                base_units // 2,
                base_units // 4
            ]
            
            return [u for u in units if u >= 32]  # Ensure minimum size
            
        except Exception as e:
            self.warnings.append(f"BiLSTM units recommendation failed: {str(e)}")
            return [64, 32]

    def _check_stationarity(self) -> Dict[str, Any]:
        """Checks stationarity of time series data with proper error handling."""
        try:
            time_series = self._get_main_time_series()
            if time_series is None:
                return {"is_stationary": False, "p_value": 1.0}
                
            # Clean the series
            time_series = pd.to_numeric(time_series, errors='coerce')
            time_series = time_series.fillna(method='ffill').fillna(method='bfill')
            
            if len(time_series) < 2:
                return {"is_stationary": False, "p_value": 1.0}
                
            # Remove infinite values
            time_series = time_series.replace([np.inf, -np.inf], np.nan).dropna()
            
            if len(time_series) < 2:
                return {"is_stationary": False, "p_value": 1.0}
                
            # Perform ADF test
            adf_result = sm.tsa.stattools.adfuller(time_series)
            
            return {
                "is_stationary": adf_result[1] < 0.05,
                "p_value": float(adf_result[1]),
                "critical_values": adf_result[4],
                "num_differencing_required": self._estimate_differencing_order(time_series)
            }
            
        except Exception as e:
            self.warnings.append(f"Stationarity check failed: {str(e)}")
            return {"is_stationary": False, "p_value": 1.0}
        



    def print_analysis_results(self, recommendations: Dict[str, Any]) -> None:
        """Prints a detailed analysis of model recommendations and architectures."""
        try:
            # Print Top Recommendations
            print("\n" + "="*80)
            print("TOP RECOMMENDED MODELS".center(80))
            print("="*80)
            for i, model in enumerate(recommendations['top_recommendations'], 1):
                print(f"{i}. {model}")

            # Print Detailed Architecture Analysis
            print("\n" + "="*80)
            print("DETAILED ARCHITECTURE ANALYSIS".center(80))
            print("="*80)
            
            for model_name, details in recommendations['architecture_details'].items():
                print(f"\n{'*'*80}")
                print(f"MODEL: {model_name}".center(80))
                print(f"{'*'*80}")
                
                # Print compatibility score
                print(f"\nCompatibility Score: {details.get('compatibility_score', 'N/A'):.4f}")
                
                # Print architecture recommendations
                if 'architecture_recommendations' in details:
                    print("\nArchitecture Recommendations:")
                    print("-" * 40)
                    for param, value in details['architecture_recommendations'].items():
                        if isinstance(value, dict):
                            print(f"\n{param}:")
                            for sub_param, sub_value in value.items():
                                print(f"  {sub_param}: {sub_value}")
                        else:
                            print(f"{param}: {value}")
                
                # Print forecast parameters if available
                if 'forecast_parameters' in details:
                    print("\nForecast Parameters:")
                    print("-" * 40)
                    for param, value in details['forecast_parameters'].items():
                        print(f"{param}: {value}")
                
                # Print preprocessing requirements
                if 'preprocessing_requirements' in details:
                    print("\nPreprocessing Requirements:")
                    print("-" * 40)
                    for req in details['preprocessing_requirements']:
                        print(f"- {req}")
                
                # Print model-specific analyses
                if 'seasonality_analysis' in details:
                    print("\nSeasonality Analysis:")
                    print("-" * 40)
                    for metric, value in details['seasonality_analysis'].items():
                        print(f"{metric}: {value}")
                
                if 'stationarity_analysis' in details:
                    print("\nStationarity Analysis:")
                    print("-" * 40)
                    for metric, value in details['stationarity_analysis'].items():
                        if isinstance(value, dict):
                            print(f"\n{metric}:")
                            for sub_metric, sub_value in value.items():
                                print(f"  {sub_metric}: {sub_value}")
                        else:
                            print(f"{metric}: {value}")
                
                # Print suitable features if available
                if 'suitable_features' in details:
                    print("\nSuitable Features:")
                    print("-" * 40)
                    for feature in details['suitable_features']:
                        print(f"- {feature}")
                        
                # Print interpretability info if available
                if 'interpretability' in details:
                    print("\nInterpretability Features:")
                    print("-" * 40)
                    for feature, value in details['interpretability'].items():
                        print(f"{feature}: {value}")
                        
            # Print Warnings
            if recommendations.get('warnings'):
                print("\n" + "="*80)
                print("WARNINGS".center(80))
                print("="*80)
                for warning in recommendations['warnings']:
                    print(f"- {warning}")
                    
        except Exception as e:
            print(f"Error printing analysis results: {str(e)}")

    # Add this method to your ModelSelectionDL class
    def display_results(self):
        """Displays formatted analysis results."""
        recommendations = self.get_model_recommendations()
        self.print_analysis_results(recommendations)