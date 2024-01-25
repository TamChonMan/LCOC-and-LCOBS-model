# Modeling Levelized Cost of Charging & Levelized Cost of Battery Swapping

## Project Description
This research project aim to model the levelized cost of charging (LCOC) and levelized cost of battery swapping (LCOBS) for electric vehicles. By simulating the charging and battery swapping processes, we calculate the associated costs and provide insights into the economic aspects of these operations.

Our research result (Also a DEMO for code using): [LCOC_LCOBS_analysis.ipynb](https://github.com/NTU-E3group/unname-4/blob/main/LCOC_LCOBS_analysis.ipynb) 

### What is Levelized Cost of Charging (LCOC)?

The levelized cost of charging (LCOC) is a concept introduced by Borlaug et al. (2020), refers the total cost of owning and operating an electric vehicle (EV) charging station or infrastructure, expressed as a constant cost per kilowatt-hour (kWh) of electricity delivered. LCOC takes into account the variations in EV recharging and usage patterns, distributing all upfront and operating costs over the total energy supplied throughout the EVSE's (Electric Vehicle Supply Equipment) lifespan.

### What is Levelized Cost of Battery Swapping (LCOBS)?

Base on the LCOC concept, our research team model the Levelized Cost of Battery Swapping (LCOBS) which represents the comprehensive evaluation of costs associated with owning and operating a public battery swapping infrastructure designed for electric vehicles (EVs). 

The LCOC and LCOBS provides a comprehensive perspective on the economic aspects of EV recharging, allowing stakeholders to assess the long-term sustainability and feasibility of charging infrastructure investments.

#### Breakdown of LCOC & LCOBS Components:

**Capital Costs:**
- Equipment costs: chargers, cables, connectors, transformers, etc.
- Installation costs: labor, permits, trenching, etc.
- Land costs: purchase or lease of the charging station site.

**Operating and Maintenance Costs:**
- Electricity costs: power consumed by the charging station itself and losses during transmission.
- Maintenance costs: repairs, replacements, software updates, etc.

**Financial Costs:**
- Discount rate: reflects the time value of money.
  
**Other factors:**
- EVSE efficiency 
- Vechile kilometer travel
- Transaction fees
- Fuel consumption rate 
  
## How to Use Our Model

### Prerequisites

Before using the model, ensure you have the following prerequisites installed:

- Python 
- NumPy
- Pandas
- geopandas

### Getting Started

Follow these steps to utilize our model:

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/NTU-E3group/unname-4.git 

2. **Import the LCOC Module or LCOBS Module:**
    ```python
    import LCOC_mode as lcoc
    import LCOBS_mode as lcobs

### Levelized Cost of Chariging Model(LCOC)-- LCOC_model.py:
1. **Initialize the Calculator:**
    Create an instance of the `LCOCCalculator` class with the required parameters.
    ```python
    lcoc_calculator = LCOC_province_calculator(province_short_name,c_purchase,c_install, om_factor,c_r_electiricitr_evse_eff, r_tfs, dr, n, r_charging_mix, A_vkt, FE,L1,L2,w_workday,w_evse_eff,w_daily_output,c_w_electiricity,c_p_purchase,p_install_factor,p_om_factor,p_tfs,p_evese_eff,p_electiricity,p_charging_mix,p_daily_output,p_workday,combined_charging_mix,province_vkt,province_res_electiricity,province_work_electiricity,province_pub_electiricity,province_weight)
    ```
    Parameter Descriptions:
    - `short_name`: Identifier for the charging station or infrastructure.
    - `c_r_purchase`: Capital cost for residential charger purchase.
    - `c_r_install`: Installation cost for residential charger.
    - `om_factor`: Operating and maintenance cost factor.
    - `c_s_r_electiricity`: Cost of electricity for residential charging.
    - `r_evse_eff`: Efficiency of residential EVSE (Electric Vehicle Supply Equipment).
    - `r_tfs`: Transmission and distribution losses for residential charging.
    - `dr`: Discount rate for financial analysis.
    - `n`: Number of years for the cost analysis.
    - `r_charging_mix`: Proportion of residential charging in overall mix.
    - `A_vkt`: Average Vehicle Kilometers Traveled.
    - `FE`: Fuel Efficiency of the vehicles.
    - `l1`, `l2`: Weighting factors for residential charging costs.
    - `w_workday`: Number of workdays for workplace charging calculation.
    - `w_evse_eff`: Efficiency of workplace EVSE.
    - `w_daily_output`: Daily energy output for workplace charging.
    - `c_s_w_electiricity`: Cost of electricity for workplace charging.
    - `c_p_purchase`: Capital cost for public charger purchase.
    - `p_install_factor`: Installation factor for public chargers.
    - `p_om_factor`: Operating and maintenance factor for public chargers.
    - `p_tfs`: Transmission and distribution losses for public charging.
    - `p_evse_eff`: Efficiency of public EVSE.
    - `c_s_p_electiricity`: Cost of electricity for public charging.
    - `p_charging_mix`: Proportion of public charging in overall mix.
    - `p_daily_output`: Daily energy output for public charging.
    - `p_workday`: Number of workdays for public charging calculation.
    - `combined_charging_mix`: Combined charging mix for sensitivity analysis.


2. **Calculate LCOC:**
    You can calculate various types of LCOC, such as residential, workplace, and public, using the corresponding methods.

    ```python
    residential_LCOC = lcoc_calculator.cal_r_LCOC()
    workplace_LCOC = lcoc_calculator.cal_w_LCOC()
    public_LCOC = lcoc_calculator.cal_p_LCOC()
    combined_LCOC = lcoc_calculator.cal_combined_LCOC()
    ```
    Function Descriptions:
    1. `cal_LCOC(sum_of_om, dis_energy, c_capital, c_electricity, evse_eff, tfs)`
        Calculates the Levelized Cost of Charging (LCOC).
        - `sum_of_om`: Sum of operating and maintenance costs.
        - `dis_energy`: Discounted total energy output.
        - `c_capital`: Capital costs.
        - `c_electricity`: Cost of electricity.
        - `evse_eff`: Efficiency of the EVSE.
        - `tfs`: Transmission and distribution losses.


    2. `cal_sum_om(c_capital, om_factor)`
        Calculates the sum of operating and maintenance costs over the lifespan.
        - `c_capital`: Capital costs.
        - `om_factor`: Operating and maintenance factor.

    3. `cal_dis_energy(year_output)`
        Calculates the discounted total energy output over the lifespan.
        - `year_output`: Yearly energy output.

    4. `cal_r_LCOC():`
        Calculates the residential LCOC.

    5. `cal_r_weight_LCOC()`
        Calculates the weighted residential LCOC.

    6. `cal_w_LCOC()`
        Calculates the workplace LCOC.

    7. `cal_p_LCOC()`
       Calculates the public LCOC.

    8. `cal_combined_LCOC()`
        Calculates the combined LCOC for all types of infrastructures.


3. **Sensitivity Analysis (Optional):**
    The model allows for sensitivity analysis by changing specific parameters. Utilize the setup functions provided in the model to adjust these parameters.
    ```python
    lcoc_calculator.setup_c_r_capital(new_c_r_purchase, new_c_r_install)
    lcoc_calculator.setup_r_om_factor(new_om_factor)

4. **LCOC_province_calculator**
    The LCOC model also includes a subclass `LCOC_province_calculator` for calculating average LCOCs across different provinces. This can be initialized and used in a similar manner, with additional parameters specific to each province.


### Levelized Cost of Battery Swapping Model(LCOBS)-- LCOBS_model.py:
1. **Initialize the Calculator:**
    Create an instance of `LCOBScalculator` by providing the necessary parameters:

    ```python
    lcobs_calculator = LCOBScalculator(
        n, n_r_b, n_c, n_s_t, battery_capacity, ps, pc, n_s, n_t_b,
        c_rb, c_s, c_c, dr, ci, cp, co, alpha, r_m, c_h, n_h, nt, power_curve
    )
    ```

    Parameter Descriptions:
    - `n`: Number of years for the cost analysis.
    - `n_r_b`: Number of reserved battery packs.
    - `n_c`: Number of chargers.
    - `n_s_t`: Number of vehicles served each day.
    - `battery_capacity`: Capacity of each battery in kWh.
    - `ps`: Power used for non-charging purposes in MW.
    - `pc`: Charging power of each charger in MW.
    - `n_s`: Number of battery swappers.
    - `n_t_b`: Number of vehicle batteries being swapped at a Battery Swapping Station (BSS).
    - `c_rb`: Cost of batteries in RMB/kWh.
    - `c_s`: Price of swappers in RMB.
    - `c_c`: Price of chargers in RMB.
    - `dr`: Discount rate for financial analysis.
    - `ci`: Infrastructure section costs in RMB.
    - `cp`: Power facility costs in RMB.
    - `co`: Other expenses in RMB.
    - `alpha`: Government subsidy rate.
    - `r_m`: Infrastructure maintenance rate.
    - `c_h`: Annual wages per labor.
    - `n_h`: Number of labors.
    - `nt`: List of number of taxis coming.
    - `power_curve`: Power curve data.

2. **Using the Model Functions**
    Utilize various methods available in the `LCOBScalculator` class to calculate different aspects of the LCOBS:

   1. `cal_LCOBS()`
      Calculates the Levelized Cost of Battery Swapping.
      
   2. `cal_total_battery_cost()`
      Calculates the total cost of batteries.

   3. `cal_charging_swapping_f_cost()`
      Calculates the fixed cost of charging and swapping facilities.

   4. `cal_i_c_cost()`
      Computes the investment and construction costs.

   5. `cal_a_f_cost()`
      Calculates annual facility maintenance expenditure.

   6. `cal_annual_operating_cost()`
      Determines the annual operating cost of the facility.

   7. `cal_lifetime_operating_cost()`
      Calculates the lifetime operating cost of the facility.

   8. `taxi_coming_timeseries_model()`
      Models the time series of taxis coming for battery swapping.

   9. `describe()`
      Provides a detailed description of various cost components.

4. **Advanced Usage**
    The model also includes setup functions like `set_up_nt`, `set_up_battery_price`, and `set_up_alpha` for sensitivity analysis and adjusting model parameters.





