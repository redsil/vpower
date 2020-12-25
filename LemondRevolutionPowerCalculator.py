from AbstractPowerCalculator import AbstractPowerCalculator


class LemondRevolutionPowerCalculator(AbstractPowerCalculator):
    #  INFO from http://bikeblather.blogspot.com/2013/01/whats-virtual-cda-and-crr-of-lemond.html
    # Power = (1/2 x air density x CdA x V^3) + (Mass * g * Crr * V),
    # Mass =  45.5 kg
    # Crr = .0094 
    # CdA = .350
    # acceleration is very noisy over this time scale, so it needs to be averaged
    def __init__(self):
        super(LemondRevolutionPowerCalculator, self).__init__()
        self.wheel_circumference = 2.122  # default value - can be overridden in config.py
        self.mass = 45.50 
        self.Crr = 0.0094
        self.CdA = 0.350
        self.g = 9.81
        self.sensor_cumulative_time = 0.0
        self.apower_sum = 0.0
        self.apower_avg = 0.0
    
    def power_from_speed(self, revs_per_sec, previous_revs_per_sec, time_gap):
        velocity = self.wheel_circumference * revs_per_sec; 
        self.sensor_cumulative_time += time_gap

        if self._DEBUG: print("power_from_speed velocity = " + repr(velocity))
        previous_velocity = self.wheel_circumference * previous_revs_per_sec; 
#        if self._DEBUG: print("power_from_speed previous_velocity = " + repr(previous_velocity))
        power = self.correction_factor * (0.5 * self.air_density * self.CdA * pow(velocity,3)) + (self.Crr * self.mass * self.g * velocity)
        if self._DEBUG: print("power_from_speed power = " + repr(power))

        if time_gap > 0:
            acceleration_power = 0.5 * self.mass * (pow(velocity,2) - pow(previous_velocity,2))/time_gap
        else:
            acceleration_power = 0.0

        self.apower_sum += acceleration_power * time_gap
            
        if (self.sensor_cumulative_time > 2):  # 2 second averaging
            self.apower_avg = self.apower_sum / self.sensor_cumulative_time
            self.sensor_cumulative_time = 0.0
            self.apower_sum = 0.0
            
        if self._DEBUG: print("power_from_speed apower = " + repr(self.apower_avg))
        
        return(power + self.apower_avg)

    def set_wheel_circumference(self, circumference):
        self.wheel_circumference = circumference
