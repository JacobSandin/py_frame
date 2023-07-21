import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
pd.options.mode.chained_assignment = None  # default='warn'


class PrepareData:
    def __init__(self, values):
        self.values = values
        self.support_resistance = self.values.get('config.preparedata.suport_resistance')
        self.bband = self.values.get('config.preparedata.bband')
        self.rsi = self.values.get('config.preparedata.rsi')
        self.macd_fast = self.values.get('config.preparedata.macd_fast')
        self.macd_slow = self.values.get('config.preparedata.macd_slow')
        self.macd_signal = self.values.get('config.preparedata.macd_signal')
        self.resample_data_hourly = self.values.get('config.preparedata.resample_data_hourly')
        self.resample_data_null = self.values.get('config.preparedata.resample_data_null')
        self.scale_data = self.values.get('config.preparedata.scale_data')
        self.use_weights = self.values.get('config.preparedata.use_weights')
        self.atr = self.values.get('config.preparedata.atr')
        self.volume_weight_level = self.values.get('config.preparedata.volume_weight_level')
        self.volume_weight = self.values.get('config.preparedata.volume_weight')
        self.bull_weight = self.values.get('config.preparedata.bull_weight')
        self.bear_weight = self.values.get('config.preparedata.bear_weight')
        self.just_plus_minus = self.values.get('config.preparedata.just_plus_minus')
        self.hist_change_shift = self.values.get('config.preparedata.hist_change_shift')
        self.trade_hours = self.values.get('config.preparedata.trade_hours')   
        self.suport_resistance = self.values.get('config.preparedata.suport_resistance')   

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

    def preprocess_data(self, df, include_predict=False,shift=0,ma1=0,ma2=0,digits=5):
        columns_to_keep = ['Open', 'High', 'Low', 'Close', 'Volume']
        df = df[columns_to_keep]
        
        
        if self.trade_hours['use_hours']:
            mask = (
                ((df.index.dayofweek == 0) & (df.index.hour >= self.trade_hours['monday_hours'][0]) & (df.index.hour < self.trade_hours['monday_hours'][1])) |
                ((df.index.dayofweek == 1) & (df.index.hour >= self.trade_hours['tuesday_hours'][0]) & (df.index.hour < self.trade_hours['tuesday_hours'][1])) |
                ((df.index.dayofweek == 2) & (df.index.hour >= self.trade_hours['wednesday_hours'][0]) & (df.index.hour < self.trade_hours['wednesday_hours'][1])) |
                ((df.index.dayofweek == 3) & (df.index.hour >= self.trade_hours['thursday_hours'][0]) & (df.index.hour < self.trade_hours['thursday_hours'][1])) |
                ((df.index.dayofweek == 4) & (df.index.hour >= self.trade_hours['friday_hours'][0]) & (df.index.hour < self.trade_hours['friday_hours'][1])) |
                ((df.index.dayofweek == 5) & (df.index.hour >= self.trade_hours['saturday_hours'][0]) & (df.index.hour < self.trade_hours['saturday_hours'][1])) |
                ((df.index.dayofweek == 6) & (df.index.hour >= self.trade_hours['sunday_hours'][0]) & (df.index.hour < self.trade_hours['sunday_hours'][1]))
            )

                
            df = df[~mask] 
            
                      
        # Handle non-finite values
        df['Open'] = df['Open'].replace([np.inf, -np.inf], np.nan)
        df['High'] = df['High'].replace([np.inf, -np.inf], np.nan)
        df['Low'] = df['Low'].replace([np.inf, -np.inf], np.nan)
        df['Close'] = df['Close'].replace([np.inf, -np.inf], np.nan)

        # Convert columns to the desired data types
        df['Open'] = df['Open'].astype(float)
        df['High'] = df['High'].astype(float)
        df['Low'] = df['Low'].astype(float)
        df['Close'] = df['Close'].astype(float)
        df['Volume'] = df['Volume'].astype(int)
        


        # df['year'] = df.index.year
        # df['month'] = df.index.month
        df['day'] = df.index.weekday
        df['hour'] = df.index.hour
        #df['minute'] = df.index.minute

        if self.suport_resistance:
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
            df.loc[asia_open, 'weight'] += self.asia_weight  # set Asia market open hours weight to 0.8
            df.loc[ny_open, 'weight'] += self.ny_weight  # set NY market open hours weight to 1

            
            df['weight']+=np.where(df.Open < df.Close, self.bull_weight,0)
            df['weight']+=np.where(df.Close < df.Open, self.bear_weight,0)


            if self.volume_weight_level > 0:
                df['weight'] += np.where(df.Volume > self.volume_weight_level, self.volume_weight, 0)

        df['momentum'] = df['Volume'] * (df['High'] - df['Low'])

        df['movement'] = df.apply(lambda row: 
            row['High'] - row['Low'] + row['Open'] - row['Low'] if row['Close'] > row['Open'] 
            else row['High'] - row['Low'] + row['High'] - row['Open'], axis=1)

        df['predict'] = round((df['Close'] - df['Open']) * 10 ** digits)
        df['currchange'] = round((df['Close'] - df['Open']) * 10 ** digits)


        if self.just_plus_minus:
            df['predict'] = np.where(df.predict < 0, -1, df.predict)
            df['predict'] = np.where(df.predict > 0, 1, df.predict)

        if self.hist_change_shift > 0:
            #df['histchange'] = 0
            for i in range(self.hist_change_shift):
                i += 1
                df['hist_'+str(i)] = df['predict'].shift(i)
                df['close:'+str(i)]=round((df['Close'].shift(i) - df['Close']) * 10 ** digits)
            
        
        if shift < 0:
            df['predict'] = df['predict'].shift(shift)# + df['predict'].shift(shift-1)
            df = df.fillna(0)
            df = df.iloc[:shift]

        df = df.dropna()
        df['predict'] = df['predict'].astype('int')
        if not ma1 == 0:
            df["MA1"] = df['Close'].rolling(window=ma1).mean()
            df['MA1'] = round((df['Close'] - df['MA1'])  * 10 ** digits)
            df = df.dropna()
            df['MA1'] = df['MA1'].astype('int')

        if not ma2 == 0:
            df["MA2"] = df['Close'].rolling(window=ma2).mean()
            df['MA2'] = round((df['Close'] - df['MA2'])  * 10 ** digits)
            df = df.dropna()
            df['MA2'] = df['MA2'].astype('int')


        df = df.drop(['Close','Open','High','Low','momentum'], axis=1)
        
        df = df.dropna()
        
        if include_predict:
            predict_col = df.pop('predict')
            df['predict'] = predict_col
        else:
            df = df.drop(['predict'], axis=1)
       
        
        if self.resample_data_hourly:
            if self.resample_data_null:
                df = df.resample('H').ffill().fillna(0)
            else:
                df = df.resample('H').ffill()

        if self.scale_data:
            df,_ = self._scale_data(df)
        else:
            df=df.copy()            

        return df

    def _scale_data(self, df):
        scalers = {}
        scaled_data = df.copy()
        for column in df.columns:
            if column not in ['predict', 'weight', 'Commodity']:
                scaler = MinMaxScaler()
                scaled_data[column] = scaler.fit_transform(df[column].values.reshape(-1, 1))
                scalers[column] = scaler
        return scaled_data, scalers


