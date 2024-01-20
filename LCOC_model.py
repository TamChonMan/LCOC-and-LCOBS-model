import numpy as np
import pandas as pd

class LCOCCalculator:
    def __init__(self,short_name, c_r_purchase , c_r_install , om_factor, c_s_r_electiricity, r_evse_eff, r_tfs, dr, n, 
                 r_charging_mix, A_vkt, FE, l1, l2, w_workday,w_evse_eff,w_daily_output,c_s_w_electiricity,c_p_purchase,p_install_factor,
                 p_om_factor,p_tfs,p_evse_eff,c_s_p_electiricity,p_charging_mix,p_daily_output,p_workday,combined_charging_mix,province_A_vkt,
                 c_r_electiricity,c_w_electiricity,c_p_electiricity,province_weight):
       
        
        #Combined
        self.combined_charging_mix = combined_charging_mix #sensitivity

        #Residential
        self.c_r_capital = c_r_purchase + c_r_install #sensitivity
        self.r_om_factor = om_factor
        self.c_r_electiricity = c_s_r_electiricity
        self.r_evse_eff = r_evse_eff  #sensitivity
        self.r_tfs = r_tfs
        self.dr = dr #sensitivity
        self.n = n
        self.r_charging_mix = r_charging_mix #sensitivity
        self.A_vkt = A_vkt #sensitivity
        self.FE = FE #sensitivity
        self.L1 = l1 #sensitivity
        self.L2 = l2 

        #Workplace
        self.w_workday = w_workday
        self.w_evse_eff = w_evse_eff #sensitivity
        self.w_daily_output = w_daily_output
        self.c_w_electiricity = c_s_w_electiricity #sensitivity

        #Public
        self.c_p_purchase = c_p_purchase #array #sensitivity
        self.p_install_factor = p_install_factor #sensitivity
        self.p_om_factor = p_om_factor
        self.p_tfs = p_tfs
        self.p_evse_eff = p_evse_eff #sensitivity
        self.c_p_electiricity = c_s_p_electiricity #sensitivity
        self.p_charging_mix = p_charging_mix #array #sensitivity
        self.p_daily_output = p_daily_output 
        self.p_workday = p_workday

        #province 
        self.province_shortname = short_name
        self.province_c_r_electiricity = c_r_electiricity #array
        self.province_A_vkt = province_A_vkt #array
        self.province_c_w_electiricity = c_w_electiricity #array
        self.province_c_p_electiricity = c_p_electiricity #array
        self.province_weight = province_weight

        # self.df_province_data = province_data
        self.province_result = pd.DataFrame()

        #Excute
        self.province_lcoc()
        
    #Model
    def cal_LCOC(self, sum_of_om, dis_enegry, c_capital,c_electiricity,evse_eff, tfs):
        return (((c_capital + sum_of_om) / dis_enegry + c_electiricity / evse_eff) * (1 + tfs))
        
    def cal_sum_om(self,c_capital, om_factor):
        return ((c_capital * om_factor) * ((1 + self.dr) ** self.n - 1) / (self.dr * (1 + self.dr) ** self.n))
    
    def cal_dis_enegry(self,year_output):
        return (year_output * ((1 + self.dr) ** self.n - 1) / (self.dr * (1 + self.dr) ** self.n))
    
    # residential LCOC
    def cal_r_year_output(self, r_charging_mix, A_vkt, FE):
        return (r_charging_mix * A_vkt * FE)

    def cal_r_dis_enegry(self):
        year_output = self.cal_r_year_output(self.r_charging_mix, self.A_vkt, self.FE)
        return self.cal_dis_enegry(year_output)
    
    def cal_r_LCOC(self):
        sum_of_om = self.cal_sum_om(self.c_r_capital,self.r_om_factor)
        dis_enegry = self.cal_r_dis_enegry()
        return self.cal_LCOC(sum_of_om, dis_enegry,self.c_r_capital,self.c_r_electiricity,self.r_evse_eff, self.r_tfs)
    
    def cal_r_weight_LCOC(self):  # weighted residential LCOC
        return (self.cal_r_LCOC() * self.L2 + self.c_r_electiricity * self.L1)
    
    #workplace LCOC
    def cal_w_dis_enegry(self):
        year_output = self.w_daily_output * self.w_workday
        return self.cal_dis_enegry(year_output)
    
    def cal_w_LCOC(self):
        sum_of_om = self.cal_sum_om(self.c_r_capital,self.r_om_factor)
        dis_enegry = self.cal_w_dis_enegry()
        return self.cal_LCOC(sum_of_om, dis_enegry,self.c_r_capital,self.c_w_electiricity,self.w_evse_eff,self.r_tfs)
    
    #Public
    def cal_p_installation(self,c_purchase):
        return c_purchase*self.p_install_factor
    
    def cal_p_dis_enegry(self):
        year_output = self.p_daily_output * self.p_workday
        return self.cal_dis_enegry(year_output)
    
    def cal_p_LCOC(self):
        p_lcoc = np.array([])
        dis_enegry = self.cal_p_dis_enegry()
        for p in self.c_p_purchase:
            c_capital = p+ p*self.p_install_factor
            sum_of_om = self.cal_sum_om(c_capital,self.p_om_factor)
            p_lcoc = np.append(p_lcoc,self.cal_LCOC(sum_of_om, dis_enegry, c_capital,self.c_p_electiricity,self.p_evse_eff,self.p_tfs))
        return np.dot(p_lcoc,self.p_charging_mix)
    
    #combined_LCOC
    def cal_combined_LCOC(self):
        c_lcoc = np.array([self.cal_r_weight_LCOC(),self.cal_w_LCOC(),self.cal_p_LCOC()])
        return np.dot(c_lcoc,self.combined_charging_mix)

    # #Province
    def province_lcoc(self):
        result = pd.DataFrame([])
        for i in range(len(self.province_shortname)):
            self.setup_provnice_data(self.province_c_r_electiricity[i], self.province_A_vkt[i], self.province_c_w_electiricity[i])
            new_row = pd.DataFrame([[self.province_shortname.loc[i][0], self.cal_r_weight_LCOC(), self.cal_w_LCOC(), self.cal_p_LCOC(),self.cal_combined_LCOC()]],
                                    columns=['Province', 'Res', 'Workplace', 'Public','Combined'])
            result = pd.concat([result, new_row], ignore_index=True)
        self.province_result = result
        return result
    
    def cal_national_w_lcoc(self):
        result = self.province_result["Combined"].to_numpy()
        return np.dot(self.province_weight,result)
    
    #setup
    def setup_provnice_data(self,c_r_electiricity,A_vkt,c_w_electiricity):
        self.c_r_electiricity = c_r_electiricity
        self.A_vkt = A_vkt
        self.c_w_electiricity = c_w_electiricity
        self.c_p_electiricity = c_w_electiricity
   
     # Sensitivity setup functions
    def setup_c_r_capital(self, c_r_purchase, c_r_install):
        self.c_r_capital = c_r_purchase + c_r_install
        self.province_lcoc()
        return self

    def setup_r_om_factor(self, om_factor):
        self.r_om_factor = om_factor
        self.province_lcoc()
        return self

    def setup_evse_eff(self, r_evse_eff, p_evse_eff):
        self.r_evse_eff = r_evse_eff
        self.w_evse_eff = r_evse_eff
        self.p_evse_eff = p_evse_eff
        self.province_lcoc()
        return self

    def setup_dr(self, dr):
        self.dr = dr
        self.province_lcoc()
        return self

    def setup_r_charging_mix(self, r_charging_mix):
        self.r_charging_mix = r_charging_mix
        self.province_lcoc()
        return self

    def setup_A_vkt(self, A_vkt):
        self.A_vkt = A_vkt
        self.province_lcoc()
        return self

    def setup_FE(self, FE):
        self.FE = FE
        self.province_lcoc()
        return self

    def setup_L1_L2(self, l1, l2):
        self.L1 = l1
        self.L2 = l2
        self.province_lcoc()
        return self

    def setup_w_daily_output(self, w_daily_output):
        self.w_daily_output = w_daily_output
        self.province_lcoc()
        return self

    def setup_c_w_electiricity(self, c_w_electiricity):
        self.c_w_electiricity = c_w_electiricity
        self.province_lcoc()
        return self

    def setup_c_p_capitial(self, c_p_purchase,p_install_factor):
        self.c_p_purchase = c_p_purchase
        self.p_install_factor = p_install_factor
        self.province_lcoc()
        return self

    def setup_p_om_factor(self, p_om_factor):
        self.p_om_factor = p_om_factor
        self.province_lcoc()
        return self

    def setup_c_p_electiricity(self, c_p_electiricity):
        self.c_p_electiricity = c_p_electiricity
        self.province_lcoc()
        return self

    def setup_p_charging_mix(self, p_charging_mix):
        self.p_charging_mix = p_charging_mix
        self.province_lcoc()
        return self

    def setup_p_daily_output(self, p_daily_output):
        self.p_daily_output = p_daily_output
        self.province_lcoc()
        return self

    def setup_combined_charging_mix(self, combined_charging_mix):
        self.combined_charging_mix = combined_charging_mix
        self.province_lcoc()
        return self
    
    def setup_for_sen_charging_mix(self,r_charging_mix,combined_charging_mix):
        self.r_charging_mix = r_charging_mix
        self.setup_combined_charging_mix(combined_charging_mix)
        self.province_lcoc()
        return self

    def setup_vkt(self,vkt):
        self.province_A_vkt = vkt
        self.province_lcoc()
        return self
    
    def setup_provnice_c_w_electricity(self,provnice_c_w_electricity):
        self.province_c_w_electiricity = provnice_c_w_electricity #array
        self.province_lcoc()
        return self
    
    def setup_provnice_c_p_electricity(self,provnice_c_p_electricity):
        self.province_c_p_electiricity = provnice_c_p_electricity #array
        self.province_lcoc()
        return self