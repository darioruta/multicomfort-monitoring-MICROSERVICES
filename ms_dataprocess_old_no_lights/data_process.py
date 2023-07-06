import pandas as pd
import datetime
import json
import datetime as dt
import statistics
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#from psychrochart import PsychroChart, load_config
from shapely.geometry import Point, Polygon
from flask import Flask, send_file

class ComfortCalculator:
    """
    Lista dei campi del dataframe aspettati
    tmp
    wind_speed
    co2
    pm10
    mrt
    light
    hum
    acoustic
    date
    tmp_op
    """
    def __init__(self, df_raw, kit_id=0):

        def get_avg_measurment(df_raw):
            tot_tmp = 0
            tot_w_speed = 0
            tot_acoustic = 0
            tot_pm10 = 0
            tot_hum = 0
            tot_co2 = 0
            tot_mrt = 0
            tot_light = 0
            tot_op_tmp = 0

            for index, row in df_raw.iterrows():
                tot_tmp += row['tmp']
                tot_w_speed += row['wind_speed']
                tot_acoustic += row['acoustic']
                tot_pm10 += row['pm10']
                tot_hum += row['hum']
                tot_co2 += row['co2']
                tot_mrt += row['mrt']
                tot_light += row['light']
                tot_op_tmp += row['tmp_op']

            op_t = (tot_mrt + tot_tmp)/ 2
            '''PI = 3.1415
            if len(df_raw.index) == 0:
                return {
                    "mrt": PI,
                    "light": PI,
                    "tmp": PI,
                    "acoustic": PI,
                    "humidity": PI,
                    "co2": PI,
                    "pm10": PI,
                    "wind_speed": PI,
                    "tmp_op": PI
                }'''
            measurment = {
                "mrt": tot_mrt / len(df_raw.index),
                "light": tot_light / len(df_raw.index),
                "tmp": tot_tmp / len(df_raw.index),
                "acoustic": tot_acoustic / len(df_raw.index),
                "humidity": tot_hum / len(df_raw.index),
                "co2": tot_co2 / len(df_raw.index),
                "pm10": tot_pm10 / len(df_raw.index),
                "wind_speed": tot_w_speed / len(df_raw.index),
                "tmp_op" : tot_op_tmp / len(df_raw.index)
            }

            return measurment

        f = open('./ms_dataprocess/config.json')
        #self.plot_dir = '/plot/'
        self.id = f'{kit_id}'
        self.graph = True
        self.df_raw = df_raw
        self.config = json.load(f)
        self.avg_measurment = get_avg_measurment(df_raw=df_raw)

    def get_tmp(self):
        return self.avg_measurment['tmp']

    def get_mrt(self):
        return self.avg_measurment['mrt']

    def get_op_temp(self):
        return self.avg_measurment['tmp_op']

    def get_light(self):
        return self.avg_measurment['light']

    def get_acoustic(self):
        return self.avg_measurment['acoustic']

    def get_humidity(self):
        return self.avg_measurment['humidity']

    def get_co2(self):
        return self.avg_measurment['co2']

    def get_pm10(self):
        return self.avg_measurment['pm10']

    def get_wind_speed(self):
        return self.avg_measurment['wind_speed']

    def pmv_ppd(self, wme=0, standard="ISO 7730-2006") -> pd.DataFrame():
        """Return Predicted Mean Vote (PMV) and Predicted Percentage of
        Dissatisfied (PPD) calculated in accordance to ISO 7730-2006 standard.



        :param df: dataframe containing at least "Date/Time",
            "T_db_i[C]", "T_rad_i[C]" and "RH_i[%]" columns.
            Optional "Occupancy column" accepting only 0 and 1 values.
        :type df: class:`pandas.core.frame.DataFrame`
        :param vel: relative air speed, defaults 0.1
        :type vel: float, optional
        :param met: metabolic rate, [met] defaults 1.2
        :type met: float, optional
        :param clo: clothing insulation, [clo] defaults 0.5
        :type clo: float, optional
        :param wme: external work, [met] defaults 0
        :type wme: float, optional
        :param standard: Currentl unused, defaults to "ISO 7730-2006"
        :type standard: str, optional
        :param filter_by_occupancy: It can be set 0 or 1, depending on wether
            activate occupancy filtering on thermal comfort KPIs computation or
            not, defaults to 0.
        :type filter_by_occupancy: int, optional
        :return: 2 lists: 1 PMV 1 PPD for each hour
        :rtype: list
        """
        vel = self.avg_measurment['wind_speed']
        vel = 0.0
        #if np.isnan(vel):
        #    vel = 0.0

        met = self.config['params']['metabolism']
        clo = self.config['params']['clothing']

        df = self.df_raw
        df["date"] = pd.to_datetime(df["date"])
        df = df.set_index("date")
        df = df.resample("1H").mean()
        df = df.reset_index()
        df = df.dropna()

        #df = self.df_raw.resample("1H").mean()
        #rh = np.array(list(df["RH_i[%]"]))
        #ta = np.array(list(df["T_db_i[C]"]))
        #tr = np.array(list(df["T_rad_i[C]"]))
        # Da togliere i NaN: se ci sono intervalli di tempo filla con un NaN quel campo
        rh = np.array(list(df["hum"]))
        ta = np.array(list(df["tmp"]))
        tr = np.array(list(df["mrt"]))



        pmv = []
        ppd = []

        fnps = np.exp(16.6536 - 4030.183 / (ta + 235))  # water vapor pressure in ambient air kPa
        pa = rh * 10 * fnps  # partial water vapor pressure in ambient air
        icl = 0.155 * clo  # thermal insulation of the clothing in M2K/W
        m = met * 58.15  # metabolic rate in W/M2
        w = wme * 58.15  # external work in W/M2
        mw = m - w  # internal heat production in the human body

        # ratio of clothed body surface over total body surface
        if icl <= 0.078:
            fcl = 1 + (1.29 * icl)
        else:
            fcl = 1.05 + (0.645 * icl)

        # heat transfer coefficient by forced convection
        hcf = 12.1 * np.sqrt(float(vel))

        # temperatures in Kelvin
        taa = ta + 273
        tra = tr + 273

        # iterative computation of clothing surface temperature
        tcla = taa + (35.5 - ta) / (3.5 * icl + 0.1)  # first tempt

        p1 = icl * fcl
        p2 = p1 * 3.96
        p3 = p1 * 100
        p4 = p1 * taa
        p5 = (308.7 - 0.028 * mw) + (p2 * (tra / 100.0) ** 4)
        xn = tcla / 100
        xf = tcla / 50
        # end criterion
        eps = 0.00015
        for i in range(0, len(df)):
            n = 0  # number of iterations
            while abs(xn[i] - xf[i]) > eps:
                xf[i] = (xf[i] + xn[i]) / 2
                # heat transfer coefficient for natural convection
                hcn = 2.38 * abs(100.0 * xf[i] - taa[i]) ** 0.25
                if hcf > hcn:
                    hc = hcf
                else:
                    hc = hcn
                xn[i] = (p5[i] + p4[i] * hc - p2 * xf[i] ** 4) / (100 + p3 * hc)
                n += 1
                if n > 150:
                    pmv.append(np.inf)
                    ppd.append(100)

            # clothing surface temperature
            tcl = 100 * xn[i] - 273

            # heat loss diff. through skin
            hl1 = 3.05 * 0.001 * (5733 - (6.99 * mw) - pa[i])
            # heat loss by sweating
            if mw > 58.15:
                hl2 = 0.42 * (mw - 58.15)
            else:
                hl2 = 0
            # latent respiration heat loss
            hl3 = 1.7 * 0.00001 * m * (5867 - pa[i])
            # dry respiration heat loss
            hl4 = 0.0014 * m * (34 - ta[i])
            # heat loss by radiation
            hl5 = 3.96 * fcl * (xn[i] ** 4 - (tra[i] / 100.0) ** 4)
            # heat loss by convection
            hl6 = fcl * hc * (tcl - ta[i])
            # conversion coefficient of thermal sensation
            ts = 0.303 * np.exp(-0.036 * m) + 0.028

            # final formulas
            pmv.append(round(ts * (mw - hl1 - hl2 - hl3 - hl4 - hl5 - hl6), 1))
            ppd.append(int(100.0 - 95.0 * np.exp(-0.03353 * pow(pmv[-1], 4.0) - 0.2179 * pow(pmv[-1],2.0))))

        # to return list of all values
        df["ppd"] = ppd
        df["pmv"] = pmv

        pmv = statistics.mean(pmv)
        ppd = statistics.mean(ppd)

        # my_dict = {"pmv": pmv, "ppd": ppd}
        # new_df = pd.DataFrame(my_dict, index=df.index)
        # return my_dict

        # return df
        self.thermal_level = 100 - int(ppd)
        return pmv, ppd

    def acoustic_comfort(self):
        sound = self.avg_measurment['acoustic']
        thresholds = self.config['threshold']['acoustic']
        if thresholds[0] <= sound <= thresholds[1]:
            self.acoustic_level = 100
            return 0.0 # 'perfect_noise'
        elif thresholds[1] <= sound <= thresholds[2]:
            self.acoustic_level = 80
            return 1.0 # 'excellent_noise'
        elif thresholds[2] <= sound <= thresholds[3]:
            self.acoustic_level = 60
            return 2.0 # 'good_noise'
        elif thresholds[3] <= sound <= thresholds[4]:
            self.acoustic_level = 40
            return 3.0 # 'warning_noise'
        elif thresholds[4] <= sound <= thresholds[5]:
            self.acoustic_level = 20
            return 4.0 # 'severe_noise'
        elif thresholds[5] > sound :
            self.acoustic_level = 0
            return 5.0  # 'danger_noise'
        else:
            return -1.0 # 'error_noise'

    def visual_comfort(self):
        lux = self.avg_measurment['light']
        thresholds = self.config['threshold']['light']
        level = -1
        if thresholds[0] <= lux <= thresholds[1]:
            self.visual_level = 0
            return 2.0 # under illuminated
        elif thresholds[1] <= lux <= thresholds[2]:
            self.visual_level = 50
            return 1.0 # mid
        elif thresholds[2] <= lux <= thresholds[3]:
            self.visual_level = 100
            return 0.0 # perfect
        else:
            return -1.0 # error

    def indoor_air_quality(self):
        # mettici dentro umidità pm10 e co2, fai la stessa cosa e prendi quello peggiore
        iaq_comfort_level = []
        co2 = self.avg_measurment['co2']
        thresholds = self.config['threshold']['co2']
        if thresholds[0] <= co2 <= thresholds[1]:
            self.co2_level = 30
            iaq_comfort_level.append(1)
        elif thresholds[1] <= co2 <= thresholds[2]:
            self.co2_level = 100
            iaq_comfort_level.append(4)
        elif thresholds[2] <= co2 <= thresholds[3]:
            self.co2_level = 80
            iaq_comfort_level.append(3)
        elif thresholds[3] <= co2 <= thresholds[4]:
            self.co2_level = 0
            iaq_comfort_level.append(2)
        elif thresholds[4] <= co2 <= thresholds[5]:
            self.co2_level = 50
            iaq_comfort_level.append(1)
        else:
            self.co2_level = 0
            iaq_comfort_level.append(0)

        pm10 = self.avg_measurment['pm10']
        thresholds = self.config['threshold']['pm10']
        if thresholds[0] <= pm10 <= thresholds[1]:
            self.pm10_level = 100
            iaq_comfort_level.append(2)
        elif thresholds[1] <= pm10 <= thresholds[2]:
            self.pm10_level = 66
            iaq_comfort_level.append(1)
        elif thresholds[2] <= pm10 <= thresholds[3]:
            self.pm10_level = 33
            iaq_comfort_level.append(0)
        else:
            self.pm10_level = 0
            iaq_comfort_level.append(0)


        hum = self.avg_measurment['humidity']
        thresholds = self.config['threshold']['humidity']
        if thresholds[0] <= hum <= thresholds[1] or thresholds[4] <= hum <= thresholds[5]:
            self.hum_level = 0
            iaq_comfort_level.append(0)
        elif thresholds[1] <= hum <= thresholds[2] or thresholds[3] <= hum <= thresholds[4]:
            self.hum_level = 50
            iaq_comfort_level.append(1)
        else :
            self.hum_level = 100
            iaq_comfort_level.append(3)

        level = min(iaq_comfort_level)
        if level == 0:
            return 2.0 # danger
        elif level == 1:
            return 1.0 # mid
        else:
            return 0.0 # good

    def total_comfort(self):
        return (self.pm10_level + self.co2_level + self.hum_level + self.acoustic_level + self.thermal_level) / 5

    def compute_acm(self, eu_norm='16798-1:2019', alpha=0.8,
                    filter_by_occupancy=0,when={}) -> pd.DataFrame():
        """Compute running mean
        Filters according to occupancy or dates can be applied.

        :param df: dataframe should contain "Date/Time" column in format
            'year/month/day hour:minutes:seconds', "T_db_o[C]" preferably with a
            subhourly timestep and "T_op_i[C]". Optional "Occupancy" column
            accepting only 0/1 values.
        :type df: class:`pandas.core.frame.DataFrame`
        :param eu_norm: It can be set to '15251:2007' if old UE norm
            computation is desired, defaults to '16798-1:2019'.
        :type eu_norm: str, optional
        :param alpha: With old UE norm '15251:2007 alpha is a free parameter in
            range [0,1), defaults to 0.8
        :type alpha: float, optional
        :param filter_by_occupancy: It can be set 0 or 1, depending on wether
            activate occupancy filtering on thermal comfort KPIs computation
            or not, defaults to 0.
        :type filter_by_occupancy: int, optional
        :param when: dictionary with 'start' and 'end' keys and values in format 'year/month/day hour:minutes:seconds'
        :type when: dict, optional
        :return: Dataframe containing new 'T_rm' variable for the considered time period.
        :rtype: class:`pandas.core.frame.DataFrame`
        """
        df = self.df_raw
        df["date"] = pd.to_datetime(df["date"])
        df = df.set_index("date")
        df = df.resample("1H").mean()
        df = df.reset_index()

        col_index = df.columns.get_loc("tmp")

        # just in case passed with t air --> handle better
        #df = df.rename(columns={"tmp":"op_tmp"})

        if eu_norm == '16798-1:2019':
            for i in range(7*24,df.shape[0]):
                # df.loc[i,"T_rm"] = (df.iloc[i-1*24:i,col_index].mean() +\
                df.loc[i, "mrt"] = (df.iloc[i - 1 * 24:i, col_index].mean() + \
                                    0.8*df.iloc[i-2*24:i-1*24,\
                                                col_index].mean() +\
                                            0.6*df.iloc[i-3*24:i-2*24,\
                                                col_index].mean() +\
                                            0.5*df.iloc[i-4*24:i-3*24,\
                                                col_index].mean() +\
                                            0.4*df.iloc[i-5*24:i-4*24,\
                                                col_index].mean() +\
                                            0.3*df.iloc[i-6*24:i-5*24,\
                                                col_index].mean() +\
                                            0.2*df.iloc[i-7*24:i-6*24,\
                                                col_index].mean())/3.8

        if eu_norm == '15251:2007':
            # TODO still to be tested (verificare che funzioni e che abbia anche senso)
            # set first day running means
            for i in range(1*24,2*24):
                df.loc[i,"mrt"] = (1-alpha)*df.iloc[i-1*24:i,col_index].mean()

            for i in range(2*24+1,df.shape[0]):
                df.loc[i,"mrt"] = (1-alpha)*(df.iloc[i-1*24:i,\
                                              col_index].mean()) +\
                                              alpha*df.iloc[i-1*24,-1]

        if filter_by_occupancy:
            df = df.where(df["Occupancy"] != 0).dropna()

        if "start" in when.keys() and "end" in when.keys():
            #df = df.set_index("Date/Time") gia fatto prima di passarlo
            start = when["start"]
            end=when["end"]
            start = dt.datetime.strptime(start, "%Y/%m/%d %H:%M:%S")
            end = dt.datetime.strptime(end, "%Y/%m/%d %H:%M:%S")
            start_idx = df.index.get_loc(start, method='nearest')
            end_idx = df.index.get_loc(end, method='nearest')
            df = df.iloc[start_idx:end_idx+1, :]

        return df

    #@app.route('/adaptive_comfort')

    def adaptive_comfort_model(self, eu_norm='16798-1:2019', alpha=0.8,
                               filter_by_occupancy=0, when={}, color="indigo"):
        """Compute adaptive comfort model in a standardized format.

        :param df: dataframe should contain "Date/Time" column in format
            'year/month/day hour:minutes:seconds', "T_db_o[C]" preferably with a
            subhourly timestep and "T_op_i[C]". Optional "Occupancy" column
            accepting only 0/1 values.
        :type df: class:`pandas.core.frame.DataFrame`
        :param eu_norm: It can be set to '15251:2007' if old UE norm
            computation is desired, defaults to '16798-1:2019'.
        :type eu_norm: str, optional
        :param alpha: With old UE norm '15251:2007 alpha is a free parameter in
            range [0,1), defaults to 0.8
        :type alpha: float, optional
        :param filter_by_occupancy: It can be set 0 or 1, depending on wether
            activate occupancy filtering on thermal comfort KPIs computation or
            not, defaults to 0.
        :type filter_by_occupancy: int, optional
        :param when: dictionary with 'start' and 'end' keys and values in format 'year/month/day hour:minutes:seconds'
        :type when: dict, optional
        :return: Number of hours in each of the 7 comfort
            categories and POR computed as % of hours outside cat 2 boundaries.
        :rtype: dict
        """

        df = self.compute_acm()

        df_down = df.where(df["mrt"] < 10).dropna()
        df_middle = df.where((df["mrt"] >= 10) & (df["mrt"] <= 33)).dropna()
        df_up = df.where(df["mrt"] > 33).dropna()

        category_1 = ((df_middle["tmp_op"] >= (0.33 * df_middle["mrt"] + 18.8 - 3)) &
                      (df_middle["tmp_op"] <= (0.33 * df_middle["mrt"] + 18.8 + 2))).sum() + \
                     ((df_down["tmp_op"] >= (0.33 * 10 + 18.8 - 3)) &
                      (df_down["tmp_op"] <= (0.33 * 10 + 18.8 + 2))).sum() + \
                     ((df_up["tmp_op"] >= (0.33 * 33 + 18.8 - 3)) &
                      (df_up["tmp_op"] <= (0.33 * 33 + 18.8 + 2))).sum()

        category_2_up = ((df_middle["tmp_op"] > (0.33 * df_middle["mrt"] + 18.8 + 2)) &
                         (df_middle["tmp_op"] <= (0.33 * df_middle["mrt"] + 18.8 + 3))).sum() + \
                        ((df_down["tmp_op"] > (0.33 * 10 + 18.8 + 2)) &
                         (df_down["tmp_op"] <= (0.33 * 10 + 18.8 + 3))).sum() + \
                        ((df_up["tmp_op"] > (0.33 * 33 + 18.8 + 2)) &
                         (df_up["tmp_op"] <= (0.33 * 33 + 18.8 + 3))).sum()

        category_3_up = ((df_middle["tmp_op"] > (0.33 * df_middle["mrt"] + 18.8 + 3)) &
                         (df_middle["tmp_op"] <= (0.33 * df_middle["mrt"] + 18.8 + 4))).sum() + \
                        ((df_down["tmp_op"] > (0.33 * 10 + 18.8 + 3)) &
                         (df_down["tmp_op"] <= (0.33 * 10 + 18.8 + 4))).sum() + \
                        ((df_up["tmp_op"] > (0.33 * 33 + 18.8 + 3)) &
                         (df_up["tmp_op"] <= (0.33 * 33 + 18.8 + 4))).sum()

        category_over_3 = (df_middle["tmp_op"] > (0.33 * df_middle["mrt"] + 18.8 + 4)).sum() + \
                          (df_down["tmp_op"] > (0.33 * 10 + 18.8 + 4)).sum() + \
                          (df_up["tmp_op"] > (0.33 * 33 + 18.8 + 4)).sum()

        category_2_down = ((df_middle["tmp_op"] >= (0.33 * df_middle["mrt"] + 18.8 - 4)) &
                           (df_middle["tmp_op"] < (0.33 * df_middle["mrt"] + 18.8 - 3))).sum() + \
                          ((df_down["tmp_op"] >= (0.33 * 10 + 18.8 - 4)) &
                           (df_down["tmp_op"] < (0.33 * 10 + 18.8 - 3))).sum() + \
                          ((df_up["tmp_op"] >= (0.33 * 33 + 18.8 - 4)) &
                           (df_up["tmp_op"] < (0.33 * 33 + 18.8 - 3))).sum()

        category_3_down = ((df_middle["tmp_op"] >= (0.33 * df_middle["mrt"] + 18.8 - 5)) &
                           (df_middle["tmp_op"] < (0.33 * df_middle["mrt"] + 18.8 - 4))).sum() + \
                          ((df_down["tmp_op"] >= (0.33 * 10 + 18.8 - 5)) &
                           (df_down["tmp_op"] < (0.33 * 10 + 18.8 - 4))).sum() + \
                          ((df_up["tmp_op"] >= (0.33 * 33 + 18.8 - 5)) &
                           (df_up["tmp_op"] < (0.33 * 33 + 18.8 - 4))).sum()

        category_under_3 = (df_middle["tmp_op"] < (0.33 * df_middle["mrt"] + 18.8 - 5)).sum() + \
                           (df_down["tmp_op"] < (0.33 * 10 + 18.8 - 5)).sum() + \
                           (df_up["tmp_op"] < (0.33 * 33 + 18.8 - 5)).sum()

        if self.graph:
            plt.rcParams.update({"font.size": 45})

            fig = plt.figure(figsize=(18, 15), constrained_layout=True)
            plt.grid()
            X = np.linspace(-10, 40)
            Y_comfort = [x * 0.33 + 18.8 if 10 <= x <= 33 else 10 * 0.33 + 18.8 if x < 10 else 33 * 0.33 + 18.8 for x in
                         X]
            Y_cat1_up = [
                x * 0.33 + 18.8 + 2 if 10 <= x <= 33 else 10 * 0.33 + 18.8 + 2 if x < 10 else 33 * 0.33 + 18.8 + 2 for x
                in X]
            Y_cat1_down = [
                x * 0.33 + 18.8 - 3 if 10 <= x <= 33 else 10 * 0.33 + 18.8 - 3 if x < 10 else 33 * 0.33 + 18.8 - 3 for x
                in X]
            Y_cat2_up = [
                x * 0.33 + 18.8 + 3 if 10 <= x <= 33 else 10 * 0.33 + 18.8 + 3 if x < 10 else 33 * 0.33 + 18.8 + 3 for x
                in X]
            Y_cat2_down = [
                x * 0.33 + 18.8 - 4 if 10 <= x <= 33 else 10 * 0.33 + 18.8 - 4 if x < 10 else 33 * 0.33 + 18.8 - 4 for x
                in X]
            Y_cat3_up = [
                x * 0.33 + 18.8 + 4 if 10 <= x <= 33 else 10 * 0.33 + 18.8 + 4 if x < 10 else 33 * 0.33 + 18.8 + 4 for x
                in X]
            Y_cat3_down = [
                x * 0.33 + 18.8 - 5 if 10 <= x <= 33 else 10 * 0.33 + 18.8 - 5 if x < 10 else 33 * 0.33 + 18.8 - 5 for x
                in X]
            plt.plot(np.array(df["mrt"]), np.array(df["tmp_op"]), ls='', marker='o', color=color, alpha=0.8)

            plt.plot(X, Y_comfort, color='r', lw=4)
            plt.plot(X, Y_cat1_up, color='r', linestyle='--', lw=4)
            plt.plot(X, Y_cat1_down, color='r', linestyle='--', lw=4)
            plt.plot(X, Y_cat2_up, color='r', linestyle='-.', lw=4)
            plt.plot(X, Y_cat2_down, color='r', linestyle='-.', lw=4)
            plt.plot(X, Y_cat3_up, color='r', linestyle=':', lw=4)
            plt.plot(X, Y_cat3_down, color='r', linestyle=':', lw=4)
            plt.xlabel(r'$\theta_{\mathrm{rm}}$ [°C]')
            plt.ylabel(r'$\theta_{\mathrm{op}}$ [°C]')
            plt.ylim(15, 33)
            # plt.savefig(self.plot_dir / "KPI_adaptive_comfort_model.png",transparent=False)
            plt.savefig(f"adaptive_{self.id}.png", transparent=False)
            plt.close(fig)
            """
            fig, ax = plt.subplots(constrained_layout=True, figsize=(50, 25))
            x = np.sort(df["tmp_op"])
            y = np.arange(len(df["tmp_op"])) / float(len(df["tmp_op"]))
            ax.plot(x, y, linewidth=4)
            ax.set_xlabel('°C')
            plt.title("CDF indoor operative temperature")
            plt.grid()
            plt.savefig("cdf_t_op_i.png")
            plt.close(fig)
            """
        lenght = len(df)
        if len(df) == 0 :
            return -1
        # return No of hours in categories, add /len(df) to get fraction
        dict = {"cat I": category_1,
                "cat II up": category_2_up,
                "cat III up": category_3_up,
                "cat over III": category_over_3,
                "cat II down": category_2_down,
                "cat III down": category_3_down,
                "cat under III": category_under_3,
                "POR": (category_3_up + category_over_3 + category_3_down + category_under_3) / lenght
                }
        return dict["POR"]

    '''def carrier_plot(self, range_temp_c=[0, 35], range_humidity_g_kg=[0, 25],altitude_m=0, suffix=""):
        """Generate a Carrier psychrometric chart.

        :param range_temp_c: x-axis limits, defaults to [0, 35]
        :type range_temp_c: list, optional
        :param range_humidity_g_kg: y-axis limits, defaults to [0, 25]
        :type range_humidity_g_kg: list, optional
        :param altitude_m: Altitute in metres, used to perform calculations of
            absolute humidity, defaults to 0
        :type altitude_m: int, optional
        :param data: Points to plot on the chart, passed as a DataFrame
            containing dry_bulb_temperature and relative_humidity columns,
            defaults to None
        :type data:  class:`pandas.core.frame.DataFrame`, optional
        :param suffix: Suffix for title and filename, defaults to ""
        :type suffix: str, optional
        """

        def compute_mix_ratio(t, rh):
            p_atm = 101325
            # df["ro"] = [353.118/t for t in (df["T_db"] + 273.15)]
            pdin = 0  # TODO: in futuro sarà 0.5*ro*v2
            p = p_atm + pdin
            try:
                if -40 < t <= 0:
                    A = 22.376
                    B = 271.68
                    C = 6.4146
                elif 0 < t < 40:
                    A = 17.438
                    B = 239.78
                    C = 6.4147
                else:
                    raise ValueError("Invalid temperature range for mix ratio computation")
                pvs = np.exp((A * t) / (B + t) + C)
            except ValueError as e:
                if not np.isnan(t):
                    print(e )
                pvs = float("nan")

            pv = rh / 100 * pvs
            return 0.622 * (pv / (p - pv))

        custom_style = load_config("ashrae")
        custom_style = {
                "figure": {
                    "x_label": "Dry-Bulb Temp. $\mathregular{[°C]}$",
                    "y_label": "Humidity Ratio $\mathregular{[w, g_w / kg_{da}]}$",
                    "title": f"Psychrometric Chart (temperature + humidity)"
                },
                "limits": {
                    "range_temp_c": range_temp_c,
                    "range_humidity_g_kg": range_humidity_g_kg,
                    "altitude_m": altitude_m,
                    "step_temp": 0.5,
                },
                "chart_params": {
                    "with_constant_rh": True,
                    "constant_rh_curves": [10, 25, 50, 75],
                    "constant_rh_labels": [10, 25, 50, 75],
                    "with_constant_v": False,
                    "with_constant_h": False,
                    "with_constant_wet_temp": False,
                    "with_zones": True,
                    "constant_h_step": 10,
                    "constant_humid_step": 5,
                    "constant_humid_label_step": 5,
                    "constant_temp_step": 35,
                    "constant_temp_label_step": 5,
                },
            }


        givoni = {
            "zones": [
                {
                    "zone_type": "xy-points",
                    "style": {
                        "edgecolor": [0, 0.749, 0.0, 0.5],
                        "facecolor": [0, 0.749, 0.0, 0.3],
                        "linewidth": 0,#2,
                        "linestyle": "-",
                    },
                    "points_x": [20, 25, 27, 27, 20, 20],  # Temperature
                    "points_y": [12, 15, 12, 4, 4, 12],  # Absolute humidity
                }
            ]
        }
        polygon = Polygon(  # Temp. and absolute humidity
            [(20, 4), (20, 12), (25, 15), (27, 12), (27, 4), (20, 4)]
            )
        chart = PsychroChart(styles=custom_style, zones_file=givoni)
        plt.rcParams.update(plt.rcParamsDefault)  # Reset figsize
        plt.rcParams.update({"font.size": 12})
        fig, ax = plt.subplots()
        chart.plot(ax=ax)

        data = self.df_raw

        if data is not None:
            counter = 0
            for row, _ in data.iterrows():
                t = data.at[row, "tmp"]
                rh = data.at[row, "hum"]
                mr = compute_mix_ratio(t, rh)
                if polygon.contains(Point(t, mr*1000)):
                    counter += 1
                    c = 'forestgreen'
                else:
                    c = 'dimgrey'

                points = {
                    "points_series_name": {
                        "style": {
                            "color": c,
                            "markersize": 1,
                            'alpha': 1
                        },  'marker':'.',
                        "xy": (t, rh),
                    }
                }
                chart.plot_points_dbt_rh(points)

        plt.savefig(f"carrier_{self.id}.png", dpi=600, facecolor="w")
        plt.close(fig)
        #return {"Givoni": counter}'''

    def noise_percentage(self):
        df = self.df_raw

        cnt = 0
        for index, row in df.iterrows():
            if row['acoustic'] >= self.config['threshold']['acoustic'][3]:
                cnt += 1
        denom = len(df)
        if denom != 0:
            return (cnt*100)/len(df)
        else:
            return -3.14

    def lux_medi(self):
        df = self.df_raw
        df['date'] = pd.to_datetime(df['date'])
        filtered_df = df[(df['date'].dt.hour < 8) | (df['date'].dt.hour > 14)]
        return df['light'].mean()

    def hour_poorly_illuminated(self):
        df = self.df_raw
        if len(df) == 0:
            df['date'] = pd.to_datetime(df['date'])
            filtered_df = df[(df['date'].dt.hour < 8) | (df['date'].dt.hour > 14)]
            df = df.set_index('date')
            df_aggregated = df.resample('1H').mean()
            return len(df_aggregated)
        else:
            return -3.14


    def co2_out_of_range(self):
        df = self.df_raw
        df['date'] = pd.to_datetime(df['date'])
        # Togli ore non lavorative
        filtered_df = df[(df['date'].dt.hour > 8) & (df['date'].dt.hour < 14)]
        filtered_df = filtered_df.set_index('date')
        # aggregati per ore
        df_aggregated = filtered_df.resample('1H').mean()
        df_aggregated = df_aggregated.dropna()
        # togli giorni della settimana
        df_aggregated = df_aggregated[df_aggregated.index.weekday < 5]
        cnt = 0
        if len(df_aggregated) == 0:
            return -3.14
        else:
            for index, row in df_aggregated.iterrows():
                if row['co2'] >= 1300:
                    cnt += 1
            return (cnt * 100) / len(df_aggregated)

    def db_out_of_range(self):
        df = self.df_raw
        df['date'] = pd.to_datetime(df['date'])
        # Togli ore non lavorative
        filtered_df = df[(df['date'].dt.hour > 8) & (df['date'].dt.hour < 14)]
        filtered_df = filtered_df.set_index('date')
        # aggregati per ore
        df_aggregated = filtered_df.resample('1H').mean()
        df_aggregated = df_aggregated.dropna()
        # togli giorni della settimana
        df_aggregated = df_aggregated[df_aggregated.index.weekday < 5]
        cnt = 0
        if len(df_aggregated) == 0:
            return -3.14
        else:
            for index, row in df_aggregated.iterrows():
                if row['acoustic'] >= 85:
                    cnt += 1
            return (cnt * 100) / len(df_aggregated)

    def compute_pmv_ppd(self, ta, tr, rh, vel=0.1, met=1.2, clo=0.7, wme=0, standard="ISO 7730-2006"):
        """Return Predicted Mean Vote (PMV) and Predicted Percentage of
        Dissatisfied (PPD) calculated in accordance to ISO 7730-2006 standard.

        :param df: dataframe containing at least "Date/Time",
            "T_db_i[C]", "T_rad_i[C]" and "RH_i[%]" columns.
            Optional "Occupancy column" accepting only 0 and 1 values.
        :type df: class:`pandas.core.frame.DataFrame`
        :param vel: relative air speed, defaults 0.1
        :type vel: float, optional
        :param met: metabolic rate, [met] defaults 1.2
        :type met: float, optional
        :param clo: clothing insulation, [clo] defaults 0.5
        :type clo: float, optional
        :param wme: external work, [met] defaults 0
        :type wme: float, optional
        :param standard: Currentl unused, defaults to "ISO 7730-2006"
        :type standard: str, optional
        :param filter_by_occupancy: It can be set 0 or 1, depending on wether
            activate occupancy filtering on thermal comfort KPIs computation or
            not, defaults to 0.
        :type filter_by_occupancy: int, optional
        :return: DataFrame containing PMV and PPD hourly values.
        :rtype: class:`pandas.core.frame.DataFrame`
        """

        fnps = np.exp(16.6536 - 4030.183 / (ta + 235))  # water vapor pressure in ambient air kPa
        pa = rh * 10 * fnps  # partial water vapor pressure in ambient air
        icl = 0.155 * clo  # thermal insulation of the clothing in M2K/W
        m = met * 58.15  # metabolic rate in W/M2
        w = wme * 58.15  # external work in W/M2
        mw = m - w  # internal heat production in the human body

        # ratio of clothed body surface over total body surface
        if icl <= 0.078:
            fcl = 1 + (1.29 * icl)
        else:
            fcl = 1.05 + (0.645 * icl)

        # heat transfer coefficient by forced convection
        hcf = 12.1 * np.sqrt(vel)

        # temperatures in Kelvin
        taa = ta + 273
        tra = tr + 273

        # iterative computation of clothing surface temperature
        tcla = taa + (35.5 - ta) / (3.5 * icl + 0.1)  # first tempt

        p1 = icl * fcl
        p2 = p1 * 3.96
        p3 = p1 * 100
        p4 = p1 * taa
        p5 = (308.7 - 0.028 * mw) + (p2 * (tra / 100.0) ** 4)
        xn = tcla / 100
        xf = tcla / 50
        # end criterion
        eps = 0.00015

        n = 0  # number of iterations
        err = False
        while abs(xn - xf) > eps and err == False:
            xf = (xf + xn) / 2
            # heat transfer coefficient for natural convection
            hcn = 2.38 * abs(100.0 * xf - taa) ** 0.25
            if hcf > hcn:
                hc = hcf
            else:
                hc = hcn
            xn = (p5 + p4 * hc - p2 * xf ** 4) / (100 + p3 * hc)
            n += 1
            if n > 150:
                err = True

        if err:
            pmv = np.inf
            ppd = 100
        else:
            # clothing surface temperature
            tcl = 100 * xn - 273

            # heat loss diff. through skin
            hl1 = 3.05 * 0.001 * (5733 - (6.99 * mw) - pa)
            # heat loss by sweating
            if mw > 58.15:
                hl2 = 0.42 * (mw - 58.15)
            else:
                hl2 = 0
            # latent respiration heat loss
            hl3 = 1.7 * 0.00001 * m * (5867 - pa)
            # dry respiration heat loss
            hl4 = 0.0014 * m * (34 - ta)
            # heat loss by radiation
            hl5 = 3.96 * fcl * (xn ** 4 - (tra / 100.0) ** 4)
            # heat loss by convection
            hl6 = fcl * hc * (tcl - ta)
            # conversion coefficient of thermal sensation
            ts = 0.303 * np.exp(-0.036 * m) + 0.028

            # final formulas
            pmv = round(ts * (mw - hl1 - hl2 - hl3 - hl4 - hl5 - hl6), 1)
            ppd = int(100.0 - 95.0 * np.exp(-0.03353 * pow(pmv, 4.0) - 0.2179 * pow(pmv, 2.0)))

        return pmv, ppd

    def termal_comfort_out_of_range(self):

        df = self.df_raw
        df['date'] = pd.to_datetime(df['date'])
        # Togli ore non lavorative
        filtered_df = df[(df['date'].dt.hour > 8) & (df['date'].dt.hour < 14)]
        filtered_df = filtered_df.set_index('date')
        # aggregati per ore
        df_aggregated = filtered_df.resample('1H').mean()
        df_aggregated = df_aggregated.dropna()
        # togli giorni della settimana
        df_aggregated = df_aggregated[df_aggregated.index.weekday < 5]
        cnt = 0
        if len(df_aggregated) == 0:
            return -3.14
        else:
            for index, row in df_aggregated.iterrows():
                pmv = self.compute_pmv_ppd(ta=float(row['tmp']), tr=float(row['tmp_op']), rh=float(row['hum']))[0]
                if pmv <= -2 or pmv >= +2:
                    cnt += 1
            return (cnt * 100) / len(df_aggregated)

    def discomfort_out_of_range(self):
        df = self.df_raw
        df['date'] = pd.to_datetime(df['date'])
        # Togli ore non lavorative
        filtered_df = df[(df['date'].dt.hour > 8) & (df['date'].dt.hour < 14)]
        filtered_df = filtered_df.set_index('date')
        # aggregati per ore
        df_aggregated = filtered_df.resample('1H').mean()
        df_aggregated = df_aggregated.dropna()
        # togli giorni della settimana
        df_aggregated = df_aggregated[df_aggregated.index.weekday < 5]
        cnt = 0
        if len(df_aggregated) == 0:
            return -3.14
        else:
            for index, row in df_aggregated.iterrows():
                ppd = self.compute_pmv_ppd(ta=float(row['tmp']), tr=float(row['tmp_op']), rh=float(row['hum']))[1]
                if ppd >= 65:
                    cnt += 1

            return (cnt * 100) / len(df_aggregated)

    def main_run(self):
        data_to_send =  [
            ('a', self.get_tmp()),
            ('b', self.get_humidity()),
            ('c', self.get_pm10()),
            ('d', self.get_co2()),
            ('e', self.get_wind_speed()),
            ('f', self.get_acoustic()),
            ('g', self.get_light()),
            ('h', self.get_mrt()),
            ('j', self.get_op_temp()),
            ('k', self.acoustic_comfort()),
            ('l', self.visual_comfort()),
            ('m', self.indoor_air_quality()),
            ('n', self.adaptive_comfort_model()),
            ('o', self.pmv_ppd()[0]),
            ('p', self.pmv_ppd()[1]),
            ('q', self.noise_percentage()),
            ('r', self.lux_medi()),
            ('s', self.hour_poorly_illuminated()),
            ('t', self.co2_out_of_range()),
            ('u', self.db_out_of_range()),
            ('v', self.termal_comfort_out_of_range()),
            ('x', self.discomfort_out_of_range()),
            ('i', self.total_comfort())
        ]
        #self.carrier_plot()
        return data_to_send


class FlaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        #self.setup_routes()

    def setup_routes(self):
        @self.app.route('/img/adaptive_comfort')
        def get_adaptive_plot():
            return send_file('KPI_adaptive_comfort_model.png', mimetype='image/png')

        @self.app.route('/img/carrier')
        def get_carrier_plot():
            return send_file('carrier.png', mimetype='image/png')

    def run(self):
        self.setup_routes()
        self.app.run()
