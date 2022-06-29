import pymysql
from datetime import datetime, timedelta
import requests
import json
import math
import numpy as np
import joblib # sklearn 받아야 함






class DatabaseConnection():
    
    def __init__(self, host="34.64.61.218", port=3306, user="root", password="Tls!@1234", database='tbtest'):

        try:
            self.conn = pymysql.connect(host=host,
                                        user=user,
                                        password=password,
                                        port=port,
                                        database=database,
                                        charset='utf8',
                                        autocommit=False)
        except:
            raise



    def getConnection(self):
        return self.conn


    def closeConnection(self):
        try:
            self.conn.close()
        except:
            raise
        
        
    def getResults(self, weather, temperature, style):
        result_dict = dict(스냅='',모자=list(),상의=list(),바지=list(),아우터=list(),신발=list())
        cats = {"상의":0,"모자":0,"바지":0,"신발":0,"아우터":0}
        
        try:
            with self.conn.cursor() as cursor:
                
                cursor.callproc("get_results", (weather,style))
                if cursor.rowcount!=-1:
                    result = cursor.fetchall()
                    for row in result:
                        result_dict["스냅"] = row[6]
                        for k,v in result_dict.items():
                            if row[7]==k:
                                if result_dict[k]==[]:
                                    result_dict[k].append(dict(pname=row[0],img=row[1],price=int(row[2])))
                                    cats[k]+=1
                                else:                                
                                    result_dict[k].append(dict(pname=row[3],img=row[4],price=int(row[5])))
                                    cats[k]+=1
                                    
                else:
                    cursor.callproc("get_results2",(temperature,style))
                    result = cursor.fetchall()
                    for row in result:
                        result_dict["스냅"] = row[6]
                        for k,v in result_dict.items():
                            if row[7]==k:
                                if result_dict[k]==[]:
                                    result_dict[k].append(dict(pname=row[0],img=row[1],price=int(row[2])))
                                    cats[k]+=1
                                else:    
                                    result_dict[k].append(dict(pname=row[3],img=row[4],price=int(row[5])))
                                    cats[k]+=1
                        
                
                
                for k,v in cats.items():
                    if v==0 and (k=="상의" or k=="바지"):
                        cursor.callproc("get_else", (temperature,style,k))
                        if cursor.rowcount!=-1:
                            added = cursor.fetchall()
                            for a in added:
                                result_dict[k].append(dict(pname=a[0],img=a[1],price=int(a[2])))
                        else:
                             result_dict[k].append(dict(pname='없음',img='없음',price='없음'))
                            
                
                return result_dict

        except:
            raise



    def getImagesForWorldcup(self, temperature, amount):
        snap_dict = {}
        try:
            with self.conn.cursor() as cursor:
                cursor.callproc("select_worldcup",(temperature, amount))
                result = cursor.fetchall()
                for row in result:
                    if row[1] not in snap_dict.keys():
                        snap_dict[row[1]] = list()
                    snap_dict[row[1]].append(row[2])
                return snap_dict
            
        except:
            raise
        

    def loadForecast(self, fore, aff_label=-1, km_label=-1, base_date="1999-01-01", forecast_date="1999-01-01"):
        sql = f'''insert into daily_forecast_tbl (base_date, forecast_date, avg_temp, min_temp, max_temp, pty_time, 
        pcp_day, max_wsd, avg_wsd, avg_dew, min_reh, avg_reh, snow, sky_07, sky_13, sky_18, sky_21, pty_07, pty_13,
        pty_18, pty_21, weather_cluster, temperature_cluster) values(
        {base_date},{forecast_date},{fore["avg_temp"]},{fore["min_temp"]},{fore["max_temp"]},{fore["pty_time"]},{fore["pcp_day"]},
        {fore["max_wsd"]},{fore["avg_wsd"]},{fore["avg_dew"]},{fore["min_reh"]},{fore["avg_reh"]},{fore["snow"]},{fore["sky_07"]},
        {fore["sky_13"]},{fore["sky_18"]},{fore["sky_21"]},{fore["pty_07"]},{fore["pty_13"]},{fore["pty_18"]},{fore["pty_21"]},
        {aff_label},{km_label})'''
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                self.conn.commit()
        except:
            raise

        
    def getForecast(self, forecast_date):
        sql = f'''select * from daily_forecast_tbl where forecast_date={forecast_date}'''
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                fore = cursor.fetchone()
                forecast = [
                    fore[2],
                    fore[3],
                    fore[5],
                    fore[14],
                    fore[15],
                    fore[16],
                    fore[17],
                    fore[18],
                    fore[19],
                    fore[20],
                    fore[21]
                ]
                return forecast, fore[-2], fore[-1]
        except:
            raise
        


    def processTable(self):
        sql = "select * from sipn limit 10;"
        try:
            with self.conn.cursor() as cursor:

                cursor.execute(sql)
                names = [desc[0] for desc in cursor.description]

                data= cursor.fetchall()
                
                return names, data
        
        except:
            raise
        


    def similarTable(self):
        sql = "select * from similar_product_tbl limit 50;"
        try:
            with self.conn.cursor() as cursor:

                cursor.execute(sql)
                names = [desc[0] for desc in cursor.description]

                data= cursor.fetchall()

                return names, data

        except:
            raise





class WeatherPreprocess:
    
    def __init__(self):
        pass
    

    def avg_dew(self, temp, humid):
        b = 17.62
        c = 243.12
        dew = []
        for i in zip(temp,humid):
            gamma = (b * i[0] /(c + i[0])) + math.log(i[1] / 100.0)
            dew.append((c * gamma) / (b - gamma))
        return sum(dew) / 24
    
    
    def snow_sum(self, sno):
        snow = []
        for p in sno:
            if p=="적설없음" or p=="1.0cm 미만":
                snow.append(0)
            elif p=="5.0cm 이상":
                snow.append(5)
            else:
                snow.append(float(p[:-2]))
        return sum(snow)
    
    
    def pcp_sum(self, pcp):
        pcp_day = []
        for p in pcp:
            if p=="강수없음" or p=="1.0mm 미만":
                pcp_day.append(0)
            elif p=="30.0~50.0mm":
                pcp_day.append(37)
            elif p=="50.0mm 이상":
                pcp_day.append(50)
            else:
                pcp_day.append(float(p[:-2]))
        return sum(pcp_day)
    
    
    def pty_count(self, pty):
        pty_time = []
        for p in pty:
            if p!='0':
                pty_time.append(p)
        return len(pty_time)











class ApiControl(WeatherPreprocess):
    
    def __init__(self, api_key="%2FwayVOC5afi5hxAkKvwt9MomnrtSrTEcimm6M93Dw%2BtYD%2Bv23EQfg7yLv1EJNn%2F%2B8QLv72EwQFSs2wqVuAQfWg%3D%3D"):
        self.hourly = {}
        self.daily = {}
        self.api_key = api_key
        self.base_date = (datetime.now()-timedelta(days=1)).strftime("%Y%m%d")
        
        url = f'''http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?serviceKey={self.api_key}&numOfRows=300&pageNo=1&base_date={self.base_date}&base_time=2300&nx=63&ny=126&dataType=JSON'''
        res = requests.get(url)
        res_dict = json.loads(res.text)
        items = res_dict['response']['body']['items']['item']
        
        self.hourly["baseDate"] = items[1]["baseDate"]
        self.hourly["fcstDate"] = items[1]["fcstDate"]
        
        for i in range(290):
            item = items[i]
            if item['category'] not in self.hourly.keys():
                self.hourly[item['category']] = list()
            if item["category"] in ["TMP","TMX","TMN","WSD","REH"]:
                self.hourly[item['category']].append(float(item['fcstValue']))
            else:
                self.hourly[item['category']].append(item['fcstValue'])
            


    def getHourly(self):
        return self.hourly
    
    
    def getDaily(self):
          
        self.daily["avg_temp"] = np.round(sum(self.hourly["TMP"]) / 24, 1)
        self.daily["max_temp"] = sum(self.hourly["TMX"])
        self.daily["min_temp"] = sum(self.hourly["TMN"])
        self.daily["max_wsd"] = np.max(self.hourly["WSD"])
        self.daily["avg_wsd"] = np.round(sum(self.hourly["WSD"]) / 24, 1)
        self.daily["avg_dew"] = np.round(self.avg_dew(self.hourly["TMP"], self.hourly["REH"]), 1)
        self.daily["pty_time"] = self.pty_count(self.hourly["PTY"])
        self.daily["pcp_day"] = self.pcp_sum(self.hourly["PCP"])
        self.daily["snow"] = self.snow_sum(self.hourly["SNO"])
        self.daily["avg_reh"] = np.round(sum(self.hourly["REH"]) / 24, 1)
        self.daily["min_reh"] = np.min(self.hourly["REH"])
            
        self.daily["sky_07"] = self.hourly["SKY"][7]
        self.daily["sky_13"] = self.hourly["SKY"][13]
        self.daily["sky_18"] = self.hourly["SKY"][18]
        self.daily["sky_21"] = self.hourly["SKY"][21]
        self.daily["pty_07"] = self.hourly["PTY"][7]
        self.daily["pty_13"] = self.hourly["PTY"][13]
        self.daily["pty_18"] = self.hourly["PTY"][18]
        self.daily["pty_21"] = self.hourly["PTY"][21]
            
        return self.hourly["baseDate"], self.hourly["fcstDate"], self.daily
        
        
        


class WeatherClustering(ApiControl):
    
    def __init__(self, scaler, affin, kmeans):
        super(WeatherClustering, self).__init__()
        _, _, self.data = self.getDaily()
        self.scaler = joblib.load(scaler)
        self.affin = joblib.load(affin)
        self.kmeans = joblib.load(kmeans)
    
    
    
    def getCluster(self):
        
        # columns = ['평균기온(C)',
        #            '최저기온(C)',
        #            '최고기온(C)',
        #            '강수 계속시간(hr)',
        #            '일강수량(mm)',
        #            '최대 풍속(m/s)',
        #            '평균 풍속(m/s)',
        #            '평균 이슬점온도(C)',
        #            '최소 상대습도(%)',
        #            '평균 상대습도(%)',
        #            '합계 3시간 신적설(cm)']
        
        # fore = pd.DataFrame([self.daily["avg_temp"],
        #                     self.daily["min_temp"],
        #                     self.daily["max_temp"],
        #                     self.daily["pty_time"],
        #                     self.daily["pcp_day"],
        #                     self.daily["max_wsd"],
        #                     self.daily["avg_wsd"],
        #                     self.daily["avg_dew"],
        #                     self.daily["min_reh"],
        #                     self.daily["avg_reh"],
        #                     self.daily["snow"]],
        #                     columns=columns,
        #                     index=[0])
        
        fore = np.array([self.daily["avg_temp"],
                         self.daily["min_temp"],
                         self.daily["max_temp"],
                         self.daily["pty_time"],
                         self.daily["pcp_day"],
                         self.daily["max_wsd"],
                         self.daily["avg_wsd"],
                         self.daily["avg_dew"],
                         self.daily["min_reh"],
                         self.daily["avg_reh"],
                         self.daily["snow"]])
        
        scaled = self.scaler.transform(fore.reshape((1,11)))
        
        
        # scaled_df = pd.DataFrame(scaled, columns=columns, index=[0])
        scaled_km = scaled[0][0:3].reshape((1,3))
        km_label = self.kmeans.predict(scaled_km)
        
        
        # scaled_df = pd.DataFrame(scaled, columns=columns, index=[0])
        # scaled_df[['최고기온(C)','최저기온(C)','평균기온(C)']] *= 2.4
        # scaled_df[['일강수량(mm)','강수 계속시간(hr)','합계 3시간 신적설(cm)']] *= 1.1
        scaled[0][0:3] *= 2.4
        scaled[0][[3,4,10]] *= 1.1
        aff_label = self.affin.predict(scaled)
        
        
        return sum(aff_label), sum(km_label)
        
        


