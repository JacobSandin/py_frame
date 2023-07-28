import pandas as pd
import pandas_ta as ta
import numpy as np
from sklearn.preprocessing import MinMaxScaler
pd.options.mode.chained_assignment = None  # default='warn'
import pickle
from classes.base.AddValues import AddValues

class PrepareData(AddValues):
    def __init__(self, values, config=None):
        self.values = values
        self.bband = 0
        self.atr = 0
        self.rsi = 0
        self.macd_fast = 0
        self.macd_slow = 0
        self.macd_signal = 0
        self.volume_weight_level = 0
        self.volume_weight = 0.2
        self.bull_weight = 0
        self.bear_weight = 0
        self.offset_years = 0
        self.hist_change_shift = 0
        self.percentile = 0
        self.shift = -1
        self.ma1 = 0
        self.ma2 = 0
        self.relative = False
        
        self.honkong_weight = 0.2
        self.london_weight = 0.2
        self.nyork_weight = 0.2

        #TODO        
        self.trade_hours = {
                'use_hours': False,
                'monday_hours': (4, 24),
                'tuesday_hours': (0, 24),
                'wednesday_hours': (0, 24),
                'thursday_hours': (0, 24),
                'friday_hours': (0, 0),
                'saturday_hours': (0, 0),
                'sunday_hours': (0, 0),
            }
        
        self.just_plus_minus = False
        self.resample_data_hourly = False
        self.resample_data_null = False
        self.do_scale_data = True
        self.use_weights = False
        self.suport_resistance = False
        
        if config is not None:
            self.parse(config)

    def load_config(self, config: dict):
        self.bband = config.get('bband', 0)
        self.rsi = config.get('rsi', 0)
        self.macd_fast = config.get('macd_fast', 0)
        self.macd_slow = config.get('macd_slow', 0)
        self.macd_signal = config.get('macd_signal', 0)
        self.atr = config.get('atr', 0)
        
        self.volume_weight_level = config.get('volume_weight_level', 0)
        self.volume_weight = config.get('volume_weight', 0.2)
        self.bull_weight = config.get('bull_weight', 0)
        self.bear_weight = config.get('bear_weight', 0)
        
        self.hist_change_shift = config.get('hist_change_shift', 0)

        self.support_resistance = config.get('support_resistance', False)
        self.just_plus_minus = config.get('just_plus_minus', False)
        self.trade_hours = config.get('trade_hours', { 'use_hours': False})
        
        self.resample_data_hourly = config.get('resample_data_hourly', False)
        self.resample_data_null = config.get('resample_data_null', False)
        self.do_scale_data = config.get('scale_data', True)
        self.use_weights = config.get('use_weights', False)
        self.offset_years = config.get('offset_years', 0)
        self.shift = config.get('shift', 0)
        self.relative = config.get('relative', False)

    def get_config(self):
        config = {
            'bband': self.bband,
            'rsi': self.rsi,
            'macd_fast': self.macd_fast,
            'macd_slow': self.macd_slow,
            'macd_signal': self.macd_signal,
            'atr': self.atr,
            'volume_weight_level': self.volume_weight_level,
            'volume_weight': self.volume_weight,
            'bull_weight': self.bull_weight,
            'bear_weight': self.bear_weight,
            'hist_change_shift': self.hist_change_shift,
            'support_resistance': self.support_resistance,
            'just_plus_minus': self.just_plus_minus,
            'trade_hours': self.trade_hours,
            'resample_data_hourly': self.resample_data_hourly,
            'resample_data_null': self.resample_data_null,
            'scale_data': self.do_scale_data,
            'use_weights': self.use_weights,
            'offset_years': self.offset_years,
            'ma1': self.ma1,
            'ma2': self.ma2,
            'honkong_weight': self.honkong_weight,
            'london_weight': self.london_weight,
            'nyork_weight': self.nyork_weight,
            'shift': self.shift,
            'relative': self.relative
        }
        return config
    # Set functions for each attribute in camelCase
    def setRelative(self, value:bool):
        self.relative = value
    
    def setOffsetYears(self, value):
        self.offset_years = value
        
    def setSupportResistance(self, value: bool):
        self.support_resistance = value

    def setShift(self, value:int):
        self.shift = value
        
    def setBband(self, value):
        self.bband = value

    def setRsi(self, value):
        self.rsi = value

    def setAtr(self, value):
        self.atr = value

    def setMacd(self, slow, fast, signal):
        self.macd_slow = slow
        self.macd_fast = fast
        self.macd_signal = signal

    def setResampleDataHourly(self, value: bool):
        self.resample_data_hourly = value

    def setResampleDataNull(self, value: bool):
        self.resample_data_null = value

    def setScaleData(self, value: bool):
        self.do_scale_data = value

    def setUseWeights(self, value: bool):
        self.use_weights = value

    def setVolumeWeightLevel(self, value):
        self.volume_weight_level = value

    def setVolumeWeight(self, value):
        self.volume_weight = value

    def setBullWeight(self, value):
        self.bull_weight = value

    def setBearWeight(self, value):
        self.bear_weight = value

    def setJustPlusMinus(self, value):
        self.just_plus_minus = value

    def setHistChangeShift(self, value):
        self.hist_change_shift = value

    def setTradeHours(self, days: dict):
        self.trade_hours = dict
        
    def setMa1(self, value):
        self.ma1 = value
    
    def setMa2(self, value):
        self.ma2 = value

        
    def getDataFrame(self,file):
        df =  pd.read_csv(file)
        df.columns = ['Date','Time','Open','High','Low','Close','Volume']
        df['Datetime']=df['Date'] +' '+ df['Time']
        df=df.drop(['Date','Time'], axis=1) # type: ignore
        df['Datetime'] = pd.to_datetime(df['Datetime'])
        df.set_index('Datetime', inplace=True)
        return df        
        
    def find_nearest_levels(self, price, level_type, decimal_places):
        if level_type == '00':
            multiplier = 10 ** (decimal_places - 2)
        elif level_type == '000':
            multiplier = 10 ** (decimal_places - 3)
        elif level_type == '0000':
            multiplier = 10 ** (decimal_places - 4)
        else:
            raise ValueError(f"Invalid level type: {level_type}")

        lower = int(price * multiplier) / multiplier
        upper = (int(price * multiplier) + 1) / multiplier

        return lower, upper

    def find_distance_to_levels(self, row, level_type, decimal_places):
        support_level, resistance_level = self.find_nearest_levels(row['Close'], level_type, decimal_places)

        distance_to_support = row['Close'] - support_level
        distance_to_resistance = resistance_level - row['Close']

        # Convert the distances to pips (assuming the specified number of decimal places for the currency pair)
        distance_to_support_pips = distance_to_support * (10 ** decimal_places)
        distance_to_resistance_pips = -distance_to_resistance * (10 ** decimal_places)

        return distance_to_support_pips, distance_to_resistance_pips

    def preprocess_data(self, df, digits=5, predict_change=False, drop_columns=['momentum','movement']): #, include_predict=False,shift=0,ma1=0,ma2=0,digits=5,offset_years=0, percentile=False):    
        if self.offset_years >0:
            df.index -= pd.DateOffset(years=self.offset_years)
        df['month'] = df.index.month
        df['week'] = df.index.isocalendar().week
        df['day'] = df.index.weekday
        df['hour'] = df.index.hour
        df['minute'] = df.index.minute
        
        
        if self.relative:
            df['Open'] = df['Open'] - df['Close']
            df['High'] = df['High'] - df['Close']
            df['Low'] = df['Low'] - df['Close']

        # df['day'] = df.index.weekday
        # df['hour'] = df.index.hour

        if self.support_resistance:
            df['DS2'], df['DR2'] = zip(*df.apply(lambda row: self.find_distance_to_levels(row, '00', digits), axis=1))
            df['DS3'], df['DR3'] = zip(*df.apply(lambda row: self.find_distance_to_levels(row, '000', digits), axis=1))
            df['DS4'], df['DR4'] = zip(*df.apply(lambda row: self.find_distance_to_levels(row, '0000', digits), axis=1))

        if self.bband>0:
            df[['bbl', 'bbm', 'bbu','bbb','bbp']] = df.ta.bbands(high='High', length=120)
            df['bbl']  = round((df['bbl'] - df['Close']) * 10 ** digits)
            df['bbm']  = round((df['bbm'] - df['Close']) * 10 ** digits)
            df['bbu']  = round((df['bbu'] - df['Close']) * 10 ** digits)
            df['bbb']  = round((df['bbb'] - df['Close']) * 10 ** digits)
            df['bbp']  = round((df['bbp'] - df['Close']) * 10 ** digits)
            #df = df.drop(['bbb','bbp','bbm'], axis=1)
            
        if self.rsi>0:
            df['rsi']=round(df.ta.rsi(length=self.rsi))
        if self.macd_fast>0:
            df[['macd','macd_signal','macd_hist']] =df.ta.macd(fast=self.macd_fast, slow=self.macd_slow, signal=self.macd_signal)
            df['macd'] = round(df['macd'] * 10 ** digits)
            df['macd_signal'] = round(df['macd_signal'] * 10 ** digits)
            df['macd_hist'] = round(df['macd_hist'] * 10 ** digits)
            
        if self.atr>0:
            df['ATR'] = df.ta.atr(high=df['High'], low=df['Low'], close=df['Close'], window=self.atr)


        # Define London, Asia, and NY market open hours
        london_open = (df.index.hour >= 8) & (df.index.hour <= 13)  # 9am-2pm London time
        asia_open = (df.index.hour >= 23) | (df.index.hour <= 4)  # 9am-2pm Tokyo time (2am-7am London time)
        ny_open = (df.index.hour >= 13) & (df.index.hour <= 18)  # 9am-2pm New York time
        
        if self.use_weights:
            # Set weights for London, Asia, and NY market open hours
            df['weight'] = 0.2  # set default weight to 1
            df.loc[london_open, 'weight'] += self.london_weight  # set London market open hours weight to 0.9
            df.loc[asia_open, 'weight'] += self.honkong_weight  # set Asia market open hours weight to 0.8
            df.loc[ny_open, 'weight'] += self.new_york_weight  # set NY market open hours weight to 1

            
            df['weight']+=np.where(df.Open < df.Close, self.bull_weight,0)
            df['weight']+=np.where(df.Close < df.Open, self.bear_weight,0)


            if self.volume_weight_level > 0:
                df['weight'] += np.where(df.Volume > self.volume_weight_level, self.volume_weight, 0)

        df['momentum'] = df['Volume'] * (df['High'] - df['Low'])
        #df['change']  = round((df['Close'] - df['Open']) * 10 ** digits)
        df['movement'] = df.apply(lambda row: 
            row['High'] - row['Low'] + row['Open'] - row['Low'] if row['Close'] > row['Open'] 
            else row['High'] - row['Low'] + row['High'] - row['Open'], axis=1)

        if predict_change:
            df['predict'] = round((df['Close'] - df['Open']) * 10 ** digits)
        else:
            df['predict'] = df['Close']    
        
        df['change'] = round((df['Close'] - df['Open']) * 10 ** digits)
        #df['currchange'] = round((df['Close'] - df['Open']) * 10 ** digits)
        # df['predict'] = np.where((df['predict'] >= -2) & (df['predict'] <= 2), 0,
        #             np.where(df['predict'] < -2, -100,
        #                 np.where(df['predict'] > 2, 100, df['predict'])))
        
        
        if self.percentile >0:
            df = self.percentile_column(df, 'predict', self.percentile)
            df = self.percentile_column(df,'currchange',self.percentile)
            df = self.percentile_column(df,'momentum',self.percentile)
            df = self.percentile_column(df,'movement',self.percentile)
            df = self.percentile_column(df,'Volume', self.percentile)

        if self.just_plus_minus:
            df['predict'] = np.where(df.predict < 0, -1, df.predict)
            df['predict'] = np.where(df.predict > 0, 1, df.predict)

        if self.hist_change_shift > 0:
            #df['histchange'] = 0
            for i in range(self.hist_change_shift):
                i += 1
                df['hist_'+str(i)] = df['predict'].shift(i)
                df['close_'+str(i)]=round((df['Close'].shift(i) - df['Close']) * 10 ** digits)
                
                if self.percentile > 0:
                    #df = percentile_column(df, 'hist_'+str(i))
                    df = self.percentile_column(df, 'close_'+str(i), self.percentile)
                
            
        
        if self.shift < 0:
            df['predict'] = df['predict'].shift(self.shift)# + df['predict'].shift(shift-1)
            df = df.fillna(0)
            df = df.iloc[:self.shift]

        df = df.dropna()
        #df['predict'] = df['predict'].astype('int')
        if not self.ma1 == 0:
            df["MA1"] = df['Close'].rolling(window=self.ma1).mean()
            df['MA1'] = round((df['Close'] - df['MA1'])  * 10 ** digits)
            #df['MA1'] = df['MA1'].fillna(0) # fill NaN with 0
            df = df.dropna()
            df['MA1'] = df['MA1'].astype('int')

        if not self.ma2 == 0:
            df["MA2"] = df['Close'].rolling(window=self.ma2).mean()
            df['MA2'] = round((df['Close'] - df['MA2'])  * 10 ** digits)
            df = df.dropna()
            df['MA2'] = df['MA2'].astype('int')

        predict_col = df.pop('predict')
        df['predict'] = predict_col

        df = df.dropna()

        if len(drop_columns) > 0:
            df = df.drop(drop_columns, axis=1)
        
        return df


    def percentile_column(self, df, column, proportion=25):
        # Calculate the percentile values
        low_limit = np.percentile(df[column], proportion)
        high_limit = np.percentile(df[column], 100 - proportion)

        # Truncate values below the low_limit and above the high_limit
        df[column] = df[column].clip(lower=low_limit, upper=high_limit)
        return df
    
    # def scale_data(self, df):
    #     scalers = {}
    #     scaled_data = df.copy()
    #     for column in df.columns:
    #         if column not in ['predict', 'weight', 'Commodity']:
    #             scaler = MinMaxScaler(feature_range=(-1,1))
    #             scaled_data[column] = scaler.fit_transform(df[column].values.reshape(-1, 1))
    #             scalers[column] = scaler
    #     return scaled_data, scalers
    def scale_data(self, df, scalers=None, columns=['predict']):
        if scalers is None:
            scalers = {}
            scaled_data = df.copy()
            for column in df.columns:
                if column not in columns:
                    scaler = MinMaxScaler(feature_range=(-1, 1))
                    scaled_data[column] = scaler.fit_transform(df[column].values.reshape(-1, 1))
                    scalers[column] = scaler
            return scaled_data, scalers
        else:
            scaled_data = df.copy()
            for column in df.columns:
                if column not in columns:
                    if column in scalers:
                        scaler = scalers[column]
                        scaled_data[column] = scaler.transform(df[column].values.reshape(-1, 1))
            return scaled_data    
        
    def save_scalers_to_file(self, scalers, filename):
        with open(filename, 'wb') as f:
            pickle.dump(scalers, f)
            
    def load_scalers_from_file(self, filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    
    def descale_data(self, df, scalers):
        scaled_data = df.copy()
        for column in df.columns:
            if column not in ['predict', 'weight', 'Commodity']:
                scaled_data[column] = scalers[column].inverse_transform(df[column].values.reshape(-1, 1))
        return scaled_data
            
    # def create_sequences(self, input_data: pd.DataFrame, target_column, sequence_length):
    #     sequences = []
    #     input_label = input_data[target_column]
    #     #Drop target_column
    #     input_data[target_column] = 0
    #     data_size=len(input_data)
    #     for i in range(data_size - sequence_length):
    #         sequence = input_data[i:i+sequence_length]
    #         label_position = i + sequence_length
    #         label = input_label.iloc[label_position]
    #         sequences.append((sequence, label))
    #     return sequences   
    
    
    def create_sequences(self, input_data: pd.DataFrame, target_column, sequence_length, num_predictions):
        sequences = []
        input_labels = input_data[target_column].tolist()
        input_data[target_column] = 0
        data_size = len(input_data)

        for i in range(data_size - sequence_length - num_predictions + 1):
            sequence = input_data[i : i + sequence_length]
            labels = input_labels[i + sequence_length : i + sequence_length + num_predictions]
            sequences.append((sequence, labels))

        return sequences
    
    
    def create_multi_column_sequences(self, input_data: pd.DataFrame, target_columns: pd.DataFrame, sequence_length, num_predictions):
        sequences = []
        input_labels = target_columns.values.tolist()
        #input_data[target_columns] = 0 #No need now that they are not future values
        data_size = len(input_data)

        for i in range(data_size - sequence_length - num_predictions + 1):
            sequence = input_data[i : i + sequence_length]
            labels = [input_labels[j] for j in range(i + sequence_length, i + sequence_length + num_predictions)]
            sequences.append((sequence, labels))

        return sequences
    
    # def preprocess_data_(self, df, include_predict=False,shift=0,ma1=0,ma2=0,digits=5):
    #     columns_to_keep = ['Open', 'High', 'Low', 'Close', 'Volume']
    #     df = df[columns_to_keep]
        
        
    #     if self.trade_hours['use_hours']:
    #         mask = (
    #             ((df.index.dayofweek == 0) & (df.index.hour >= self.trade_hours['monday_hours'][0]) & (df.index.hour < self.trade_hours['monday_hours'][1])) |
    #             ((df.index.dayofweek == 1) & (df.index.hour >= self.trade_hours['tuesday_hours'][0]) & (df.index.hour < self.trade_hours['tuesday_hours'][1])) |
    #             ((df.index.dayofweek == 2) & (df.index.hour >= self.trade_hours['wednesday_hours'][0]) & (df.index.hour < self.trade_hours['wednesday_hours'][1])) |
    #             ((df.index.dayofweek == 3) & (df.index.hour >= self.trade_hours['thursday_hours'][0]) & (df.index.hour < self.trade_hours['thursday_hours'][1])) |
    #             ((df.index.dayofweek == 4) & (df.index.hour >= self.trade_hours['friday_hours'][0]) & (df.index.hour < self.trade_hours['friday_hours'][1])) |
    #             ((df.index.dayofweek == 5) & (df.index.hour >= self.trade_hours['saturday_hours'][0]) & (df.index.hour < self.trade_hours['saturday_hours'][1])) |
    #             ((df.index.dayofweek == 6) & (df.index.hour >= self.trade_hours['sunday_hours'][0]) & (df.index.hour < self.trade_hours['sunday_hours'][1]))
    #         )

                
    #         df = df[~mask] 
            
                      
    #     # Handle non-finite values
    #     df['Open'] = df['Open'].replace([np.inf, -np.inf], np.nan)
    #     df['High'] = df['High'].replace([np.inf, -np.inf], np.nan)
    #     df['Low'] = df['Low'].replace([np.inf, -np.inf], np.nan)
    #     df['Close'] = df['Close'].replace([np.inf, -np.inf], np.nan)

    #     # Convert columns to the desired data types
    #     df['Open'] = df['Open'].astype(float)
    #     df['High'] = df['High'].astype(float)
    #     df['Low'] = df['Low'].astype(float)
    #     df['Close'] = df['Close'].astype(float)
    #     df['Volume'] = df['Volume'].astype(int)
        


    #     # df['year'] = df.index.year
    #     # df['month'] = df.index.month
    #     df['day'] = df.index.weekday
    #     df['hour'] = df.index.hour
    #     #df['minute'] = df.index.minute

    #     if self.suport_resistance:
    #         df['DS2'], df['DR2'] = zip(*df.apply(lambda row: self.find_distance_to_levels(row, '00', digits), axis=1))
    #         df['DS3'], df['DR3'] = zip(*df.apply(lambda row: self.find_distance_to_levels(row, '000', digits), axis=1))
    #         df['DS4'], df['DR4'] = zip(*df.apply(lambda row: self.find_distance_to_levels(row, '0000', digits), axis=1))

    #     if self.bband>0:
    #         df[['bbl', 'bbm', 'bbu','bbb','bbp']] = df.ta.bbands(high='High', length=120)
    #         df['bbl']  = round((df['bbl'] - df['Close']) * 10 ** digits)
    #         df['bbm']  = round((df['bbm'] - df['Close']) * 10 ** digits)
    #         df['bbu']  = round((df['bbu'] - df['Close']) * 10 ** digits)
    #         df['bbb']  = round((df['bbb'] - df['Close']) * 10 ** digits)
    #         df['bbp']  = round((df['bbp'] - df['Close']) * 10 ** digits)
    #         #df = df.drop(['bbb','bbp','bbm'], axis=1)
            
    #     if self.rsi>0:
    #         df['rsi']=round(df.ta.rsi(length=self.rsi))
            
    #     if self.macd_fast>0:
    #         df[['macd','macd_signal','macd_hist']] =df.ta.macd(fast=self.macd_fast, slow=self.macd_slow, signal=self.macd_signal)
    #         df['macd'] = round(df['macd'] * 10 ** digits)
    #         df['macd_signal'] = round(df['macd_signal'] * 10 ** digits)
    #         df['macd_hist'] = round(df['macd_hist'] * 10 ** digits)
            
    #     if self.atr>0:
    #         df['ATR'] = df.ta.atr(high=df['High'], low=df['Low'], close=df['Close'], window=self.atr)


    #     # Define London, Asia, and NY market open hours
    #     london_open = (df.index.hour >= 8) & (df.index.hour <= 13)  # 9am-2pm London time
    #     asia_open = (df.index.hour >= 23) | (df.index.hour <= 4)  # 9am-2pm Tokyo time (2am-7am London time)
    #     ny_open = (df.index.hour >= 13) & (df.index.hour <= 18)  # 9am-2pm New York time
        
    #     if self.use_weights:
    #         # Set weights for London, Asia, and NY market open hours
    #         df['weight'] = 0.2  # set default weight to 1
    #         df.loc[london_open, 'weight'] += self.london_weight  # set London market open hours weight to 0.9
    #         df.loc[asia_open, 'weight'] += self.asia_weight  # set Asia market open hours weight to 0.8
    #         df.loc[ny_open, 'weight'] += self.ny_weight  # set NY market open hours weight to 1

            
    #         df['weight']+=np.where(df.Open < df.Close, self.bull_weight,0)
    #         df['weight']+=np.where(df.Close < df.Open, self.bear_weight,0)


    #         if self.volume_weight_level > 0:
    #             df['weight'] += np.where(df.Volume > self.volume_weight_level, self.volume_weight, 0)

    #     df['momentum'] = df['Volume'] * (df['High'] - df['Low'])

    #     df['movement'] = df.apply(lambda row: 
    #         row['High'] - row['Low'] + row['Open'] - row['Low'] if row['Close'] > row['Open'] 
    #         else row['High'] - row['Low'] + row['High'] - row['Open'], axis=1)

    #     df['predict'] = round((df['Close'] - df['Open']) * 10 ** digits)
    #     df['currchange'] = round((df['Close'] - df['Open']) * 10 ** digits)


    #     if self.just_plus_minus:
    #         df['predict'] = np.where(df.predict < 0, -1, df.predict)
    #         df['predict'] = np.where(df.predict > 0, 1, df.predict)

    #     if self.hist_change_shift > 0:
    #         #df['histchange'] = 0
    #         for i in range(self.hist_change_shift):
    #             i += 1
    #             df['hist_'+str(i)] = df['predict'].shift(i)
    #             df['close:'+str(i)]=round((df['Close'].shift(i) - df['Close']) * 10 ** digits)
            
        
    #     if shift < 0:
    #         df['predict'] = df['predict'].shift(shift)# + df['predict'].shift(shift-1)
    #         df = df.fillna(0)
    #         df = df.iloc[:shift]

    #     df = df.dropna()
    #     df['predict'] = df['predict'].astype('int')
    #     if not ma1 == 0:
    #         df["MA1"] = df['Close'].rolling(window=ma1).mean()
    #         df['MA1'] = round((df['Close'] - df['MA1'])  * 10 ** digits)
    #         df = df.dropna()
    #         df['MA1'] = df['MA1'].astype('int')

    #     if not ma2 == 0:
    #         df["MA2"] = df['Close'].rolling(window=ma2).mean()
    #         df['MA2'] = round((df['Close'] - df['MA2'])  * 10 ** digits)
    #         df = df.dropna()
    #         df['MA2'] = df['MA2'].astype('int')


    #     df = df.drop(['Close','Open','High','Low','momentum'], axis=1)
        
    #     df = df.dropna()
        
    #     if include_predict:
    #         predict_col = df.pop('predict')
    #         df['predict'] = predict_col
    #     else:
    #         df = df.drop(['predict'], axis=1)
       
        
    #     if self.resample_data_hourly:
    #         if self.resample_data_null:
    #             df = df.resample('H').ffill().fillna(0)
    #         else:
    #             df = df.resample('H').ffill()

    #     if self.do_scale_data:
    #         df,_ = self._scale_data(df)
    #     else:
    #         df=df.copy()            

    #     return df



