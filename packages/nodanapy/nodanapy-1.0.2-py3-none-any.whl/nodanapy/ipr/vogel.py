import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from _properties.oilProperties import OilProperties

class VogelRD:
    """
    ### Summary:
    This class is to determine IPR with the Vogel method for oil well with reservoir data.
    
    ### Methods:
    - productivity_index
    - __flow_bif_
    - __flow_v_
    - inflow: This method is to calculate the IPR.
    """ 
    def __init__(self, pressure: int|float, temperature: int|float, bubble_pressure: int|float=0, specific_gravity: float=0.65, api: int|float=40,
                permeability: int|float=10, compressibility: float=1e-5, skin: int|float=0, height_formation: int|float=10, 
                well_radius: int|float=0.35, reservoir_radius: int|float=1000, water_cut: float=0.0, 
                go_ratio: int|float=50, amount: int=25):
        """
        Args:
            pressure (int | float): Well Pressure [psia]
            temperature (int | float): Well Temperature [oR]
            bubble_pressure (int | float, optional): Bubble Pressure [psia]. Defaults to 0.
            specific_gravity (float, optional): Gas Specific Gravity. Defaults to 0.65.
            api (int | float, optional): API Gravity. Defaults to 40.
            permeability (int | float, optional): Permeability [md]. Defaults to 10.
            compressibility (float, optional): Total Compressibility [psia^-1]. Defaults to 1e-5.
            skin (int | float, optional): Skin Factor. Defaults to 0.
            height_formation (int | float, optional): Height Formation [ft]. Defaults to 10.
            well_radius (int | float, optional): Well Radius [ft]. Defaults to 0.35.
            reservoir_radius (int | float, optional): Reservoir Radius [ft]. Defaults to 1000.
            water_cut (float, optional): Water Cut. Defaults to 0.0.
            go_ratio (int | float, optional): Gas-Oil Ratio [scf/stb]. Defaults to 50.
            amount (int, optional): Number of Points. Defaults to 25.
        ### Private Args:
            delta_p (array): Pressures Assumed from 14.7 to well pressure [psia]
            _prop_oil (float): Properties of Oil
            j: Productivity Index
            q_b: Rate Biphasic
            q_v: Rate Vogel
            q_max: Rate Max            
        """     
        
        self.pressure = pressure
        self.temperature = temperature
        self.bubble_pressure = bubble_pressure
        self.specific_gravity = specific_gravity
        self.api = api
        self.permeability = permeability
        self.compressibility = compressibility
        self.skin = skin
        self.height_formation = height_formation
        self.well_radius = well_radius
        self.reservoir_radius = reservoir_radius
        self.water_cut = water_cut
        self.go_ratio = go_ratio
        self.amount = amount
        
        self.delta_p = np.linspace(self.pressure, 14.7, self.amount)
        
        self._prop_oil = OilProperties(self.pressure, self.temperature, self.specific_gravity, self.api, bubble_pressure=self.bubble_pressure)
        
        self.j = self.productivity_index()
        self.q_b = self._flow_bif_()
        self.q_v = self._flow_v_()
        self.q_max = self.q_b + self.q_v
    
    def productivity_index(self):
        return (self.permeability*self.height_formation)/(141.2*self._prop_oil.factor_volumetric_oil(self.compressibility)*self._prop_oil.viscosity_oil()*(np.log(self.reservoir_radius/self.well_radius)-(3/4)+self.skin))
        
    def _flow_bif_(self):
        return self.j*(self.pressure-self.bubble_pressure)
        
    def _flow_v_(self):
        return (self.j*self.bubble_pressure)/1.8
    
    def inflow(self):
        """
        Returns:
            List: It will return a list with the rates and flowing bottom hole pressure\n
            [ql (bbl/d), qg(Mscf/d), qo(bbl/d), qw(bbl/d), pwf(psia)]
        """ 
        if self.bubble_pressure == 0:
            qo = self.j*(self.pressure - self.delta_p)
        elif self.bubble_pressure >= self.pressure:
            qo = self.q_max*(1-0.2*(self.delta_p/self.pressure)-0.8*((self.delta_p/self.pressure)**2))
        elif self.bubble_pressure <= self.pressure:
            qo = np.where(self.delta_p<self.bubble_pressure, self.q_b + self.q_v*(1-0.2*(self.delta_p/self.bubble_pressure)-0.8*((self.delta_p/self.bubble_pressure)**2)), self.j*(self.pressure - self.delta_p))
        
        qg = qo*self.go_ratio
        qw = qo*self.water_cut/(1-self.water_cut)
        ql = qo + qw
        return [ql, qg/1000, qo, qw, self.delta_p]

class VogelPD:
    """
    ### Summary:
    This class is to determine IPR with the Vogel method for oil well with production data.
    
    ### Methods:
    - productivity_index
    - __flow_bif_
    - __flow_v_
    - inflow: This method is to calculate the IPR.
    """ 
    def __init__(self, pressure: int|float, bubble_pressure: int|float=0, q_test: int|float=100, pwf_test: int|float=1000, 
                water_cut: float=0.0, go_ratio: int|float=50, amount: int=25):
        """
        Args:
            pressure (int | float): Well Pressure [psia]
            bubble_pressure (int | float, optional): Well Temperature [oR]. Defaults to 0.
            q_test (int | float, optional): Oil Rate Test [bbl/d]. Defaults to 100.
            pwf_test (int | float, optional): Flowing Pressure Test [psia]. Defaults to 1000.
            water_cut (float, optional): Water Cut. Defaults to 0.0.
            go_ratio (int | float, optional): Gas-Oil Ratio. Defaults to 50.
            amount (int, optional): Number of Points. Defaults to 25.
        ### Private Args:
            delta_p (array): Pressures Assumed from 14.7 to well pressure [psia]
            j: Productivity Index
            q_b: Rate Biphasic
            q_v: Rate Vogel
            q_max: Rate Max
        """
        
        self.pressure = pressure
        self.bubble_pressure = bubble_pressure
        self.q_test = q_test
        self.pwf_test = pwf_test
        self.water_cut = water_cut
        self.go_ratio = go_ratio
        self.amount = amount
        
        self.delta_p = np.linspace(self.pressure, 14.7, self.amount)
        
        self.j = self.productivity_index()
        self.q_b = self._flow_bif_()
        self.q_v = self._flow_v_()
        self.q_max = self.q_b + self.q_v
    
    def productivity_index(self):
        if self.pwf_test > self.bubble_pressure:
            return self.q_test/(self.pressure-self.pwf_test)
        elif self.pwf_test <= self.bubble_pressure:
            return self.q_test/((self.pressure-self.bubble_pressure)+(self.bubble_pressure/1.8)*(1-0.2*(self.pwf_test/self.bubble_pressure)-0.8*((self.pwf_test/self.bubble_pressure)**2)))
    
    def _flow_bif_(self, ):
        return self.j*(self.pressure-self.bubble_pressure)
    
    def _flow_v_(self):
        return (self.j*self.bubble_pressure)/1.8
    
    def inflow(self):
        """
        Returns:
            List: It will return a list with the rates and flowing bottom hole pressure\n
            [ql (bbl/d), qg(Mscf/d), qo(bbl/d), qw(bbl/d), pwf(psia)]
        """      
        if self.bubble_pressure == 0:
            qo = self.j*(self.pressure - self.delta_p)
        elif self.bubble_pressure >= self.pressure:
            qo = self.q_max*(1-0.2*(self.delta_p/self.pressure)-0.8*((self.delta_p/self.pressure)**2))
        elif self.bubble_pressure <= self.pressure:
            qo = np.where(self.delta_p<self.bubble_pressure, self.q_b + self.q_v*(1-0.2*(self.delta_p/self.bubble_pressure)-0.8*((self.delta_p/self.bubble_pressure)**2)), self.j*(self.pressure - self.delta_p))
            
        qg = qo*self.go_ratio
        qw = qo*self.water_cut/(1-self.water_cut)
        ql = qo + qw
        return [ql, qg/1000, qo, qw, self.delta_p]

if __name__ == "__main__":
    
    #well = VogelRD(5651, 590, permeability=8.2, height_formation=53, reservoir_radius=2980, go_ratio=85, well_radius=0.328, bubble_pressure=6000)
    well = VogelPD(1309, 1000, q_test=100, pwf_test=1000,)
    
    # print("j", well.j, "qb", well.q_b, "qm", well.q_v, "qmb", well.q_max)
    
    #ql, qg, qo, qw, pw = well.inflow()
    #print(ql, qg, qo, qw, pw)
    
    # import matplotlib.pyplot as plt
    
    # fig, axs = plt.subplots(2, 2)
    # axs[0, 0].plot(ql, pw)
    # axs[0, 1].plot(qg, pw)
    # axs[1, 0].plot(qo, pw)
    # axs[1, 1].plot(qw, pw)
    # #plt.plot(qo, pw)
    # plt.show()