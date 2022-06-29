from TJproject import DatabaseConnection, ApiControl, WeatherClustering

        
baseDate, fcstDate, daily = ApiControl().getDaily()

wc, tc = WeatherClustering(scaler="/root/test_env/models/scaler.pkl",
                            affin="/root/test_env/models/affin_112.pkl",
                            kmeans="/root/test_env/models/km_15.pkl").getCluster()

dbc = DatabaseConnection()
dbc.loadForecast(fore=daily, base_date=baseDate, forecast_date=fcstDate, aff_label=wc, km_label=tc)
dbc.closeConnection()
