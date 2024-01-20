import numpy as np
import pandas as pd

class LCOBScalculator:
    def __init__(self,n,n_r_b,n_c,n_s_t,battery_capacity,ps,pc,n_s,n_t_b,
                 c_rb,c_s,c_c,dr,ci,cp,co,alpha,r_m,c_h,n_h,nt,power_curve):
        self.n = n 
        self.n_r_b = n_r_b                          #no. of reserved battery pack
        self.n_c = n_c                              #no. of charger
        self.n_s_t = n_s_t                          # Number of vehicles served each day 
        self.battery_capacity = battery_capacity    #Battery capacity /kwh
        self.ps = ps                                #Amount of self-used electricity for other noncharging purposes /MW
        self.pc = pc                                #Charging power of each charger /MW
        self.n_s = n_s                              #Number of swappers 
        self.n_t_b = n_t_b                          #Number of vehicle batteries being swapped at a BSS
        self.c_rb = c_rb                            #Battery costs (RMB/kwh)
        self.c_s = c_s                              #Price of swappers (RMB)
        self.c_c = c_c                              #Price of chargers (RMB)
        self.dr = dr                                #Discount rate
        self.ci = ci                                #Infrastructure section costs (RMB)
        self.cp = cp                                #Power facility costs (RMB)
        self.co = co                                #Other expenses (RMB)
        self.alpha = alpha                          #Government subsidy rate
        self.r_m = r_m                              #Infrastructure maintenance rate
        self.c_h = c_h                              #Annual wages per labor
        self.n_h = n_h                              #Number of labors

        self.nt = nt                                #list of number of taxi coming
        self.power_curve = power_curve

        self.total_battery_csot = self.cal_total_battery_cost()
        self.charging_swapping_f_cost = self.cal_charging_swapping_f_cost()

        self.i_c_cost = self.cal_i_c_cost()
        self.a_f_cost = self.cal_a_f_cost()

        self.c_daily_e = 0
        self.energy_swapped_daily = 0
        self.df_time_series = pd.DataFrame()

        self.taxi_coming_timeseries_model()

    def cal_total_battery_cost(self):
        return self.battery_capacity*self.c_rb

    def cal_charging_swapping_f_cost(self):
        return self.c_s*self.n_s+self.c_c*self.n_c+self.total_battery_csot*(self.n_r_b+self.n_t_b)*(1+1/(1+self.dr)**5)
    
    def cal_i_c_cost(self): #Investment and construction costs
        return (self.charging_swapping_f_cost+self.ci+self.cp+self.co)*(1-self.alpha)
    
    def cal_a_f_cost(self): #Annual facility maintenance expenditure
        return (self.charging_swapping_f_cost+self.ci+self.cp)*self.r_m
    
    def taxi_coming_timeseries_model(self):
        nnb = [x * 4 for x in self.nt[:-2]]+[0,0]
        nfs = [0]*23 + [160]
        nb =  [x * 4 for x in self.nt]
        nes = [0]*24
        nbc = [0]*24
        nen = [0]*24

        for i in range(0, 23):
            nfs[i] = nfs[i-1] + nnb[i-2] - nb[i]

        for i in range (0,23):
            nbc[i] = nbc[i-1] +nnb[i] - nnb[i-2]

        for i in range (0,23):
            nes[i] = nb[i]+nes[i]

        for i in range (0,23):
            nen[i] = nes[i]-nnb[i]

        fb = [x * self.pc + self.ps for x in nbc]
        ce = [x * y for x , y in zip(self.power_curve,fb)]

        energy_swapped = [x/4 * self.battery_capacity for x in nb]
        time_series = {'Nt':self.nt,'Nfs':nfs,'Nnb':nnb,'Nes':nes,'Nbc':nbc,'Nb':nb,'Nen':nen,'Fb':fb,'Ce':ce,'Energy_swapped':energy_swapped}
        self.df_time_series = pd.DataFrame(time_series)

        self.energy_swapped_daily = sum(energy_swapped)
        self.c_daily_e = sum(ce)

    def cal_annual_operating_cost(self):
        return self.cal_a_f_cost()+self.c_h*self.n_h+self.c_daily_e * 365 
    
    def cal_lifetime_operating_cost(self):
        return self.cal_annual_operating_cost()* ((1 + self.dr) ** self.n - 1) / (self.dr * (1 + self.dr) ** self.n)

    def cal_LCOBS(self):
        return (self.cal_i_c_cost()+self.cal_lifetime_operating_cost())/(self.energy_swapped_daily * 365 * ((1 + self.dr) ** self.n - 1) / (self.dr * (1 + self.dr) ** self.n))

    def describe(self):
        pd.set_option('display.float_format', lambda x: '%.3f' % x)
        data = {
            "Investment and construction costs": [self.cal_i_c_cost()],
            "Annual facility maintenance expenditure": [self.cal_a_f_cost()],
            "Annual labor wages": [self.c_h * self.n_h],
            "lifetime operation cost": [self.cal_lifetime_operating_cost()],
            "lifetime electiricty cost": [self.c_daily_e * 365 * ((1 + self.dr) ** self.n - 1) / (self.dr * (1 + self.dr) ** self.n)],
            "lifetime maintenance and labor cost": [self.cal_lifetime_operating_cost() - self.c_daily_e * 365 * ((1 + self.dr) ** self.n - 1) / (self.dr * (1 + self.dr) ** self.n)],
            "lifetime swapped electiricity": [self.energy_swapped_daily * 365 * ((1 + self.dr) ** self.n - 1) / (self.dr * (1 + self.dr) ** self.n)]
        }
        df = pd.DataFrame(data)
        print(df.transpose())
