"bloup bloup"

from ctypes import c_ulong
from time import time


def calculate_water_energy(grams, start_temp, end_temp):
    total_energy = 0

    if start_temp < 0:
        start_state = 1
    elif 0 < start_temp < 100:
        start_state = 2
    elif start_temp > 100:
        start_state = 3

    if end_temp < 0:
        end_state = 1
    elif 0 < end_temp < 100:
        end_state = 2
    elif end_temp > 100:
        end_state = 3
    
    # State 1 -> Ice
    # State 2 -> Water
    # State 3 -> Steam

    if start_state == 1:
        if end_state == 1:
            total_energy += grams * 2.03 * (end_temp - start_temp)
        elif end_state == 2:
            total_energy += grams * 2.03 * -start_temp
            total_energy += grams * 333.6
            total_energy += grams * 4.18 * end_temp
        elif end_state == 3:
            total_energy += grams * 2.03 * -start_temp
            total_energy += grams * 333.6
            total_energy += grams * 4.18 * 100
            total_energy += grams * 2263.6
            total_energy += grams * 2.01 * (end_temp - 100)
    
    elif start_state == 2:
        if end_state == 1:
            total_energy -= grams * 4.18 * start_temp
            total_energy -= grams * 333.6
            total_energy -= grams * 2.03 * end_temp
        elif end_state == 2:
            total_energy += grams * 4.18 * (end_temp - start_temp)
        elif end_state == 3:
            total_energy += grams * 4.18 * (100 - start_temp)
            total_energy += grams * 2263.6
            total_energy += grams * 2.01 * (end_temp - 100)
    
    elif start_state == 3:
        if end_state == 1:
            total_energy -= grams * 2.01 * (start_temp - 100)
            total_energy -= grams * 2263.6
            total_energy -= grams * 4.18 * 100
            total_energy -= grams * 333.6
            total_energy -= grams * 2.03 * -end_temp
        elif end_state == 2:
            total_energy -= grams * 2.01 * (start_temp - 100)
            total_energy -= grams * 2263.6
            total_energy -= grams * 4.18 * (100 - end_temp)
        elif end_state == 3:
            total_energy += grams * 2.01 * (end_temp - start_temp)
    return round(total_energy, 2)


def water(L,temp0,temp1,heating_day):
    grams = L *1000
    cth = 4.18 # [J*g-1*K-1]
    heating_power = heating_day/86400
    temp_reached = heating_power/(grams*cth)+temp0
    energy_to_heat = grams * cth * ( temp1 - temp0)
    delta_heat =  energy_to_heat - heating_power
    return temp_reached, delta_heat




def main():
    # parameters to enter
    L = 100 # [liters]
    temp0 = 20 # [20 °C]
    temp1 = 50 # [50 °C]
    grams = L *1000
    heating_power = 50 #[W]
    Efficiency = 1 
    cth = 4.18 # [J*g-1*K-1]
    energy_second = Efficiency*heating_power
    energy_day = energy_second*86400

    energy_to_heat = grams * cth * ( temp1 - temp0)
    # energy_to_heat = calculate_water_energy(grams, temp0, temp1)
    
    time_taken_toheat = energy_to_heat/(energy_second)
    print ('time to heat in seconds: ',time_taken_toheat)
    if (time_taken_toheat>86400):
        print('not reached temp wanted in 1 day')
        Energy_missing = energy_to_heat - energy_day
        print('Energy missing: ',Energy_missing)
        temp2 = energy_day/(grams*cth)+temp0
        print('temp reached: ', temp2)
        

if __name__ == '__main__':
    main()
