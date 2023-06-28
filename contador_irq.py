from machine import Pin
from time import sleep
import time
import helper_functions.globals as globals_file


## -------------------------------------------------------------------------

def pulse_counter(pin, new_coin):#, money_coin):
    global pulse_count
    global pulse_last_state
    global pulse_state
    global money_in_session
    
    pulse_state = pin.value()

    # counter
    if pulse_state == 0 and pulse_last_state == 0:  #// this means we entered a new pulse
        
        pulse_last_state = 1 #// set the previous state

        # re reinicia el conteo si es una nueva moneda
        if new_coin is True:
            pulse_count = 0  #// increment the pulse counter
            total_pulses = 0


    elif pulse_state == 1 and pulse_last_state == 1: #// this means a pulse just ended
        pulse_last_state = 0
        pulse_count = pulse_count + 1  #// increment the pulse counter
       
    # saves last pulse time
    time_last_pulse = time.time()
    
    return pulse_count

def check_for_new_coin(time_last_pulse, time_now):
    # checks if a new coin is introduced and returns boolean
    # also resets totla_pulses counter

    if time_last_pulse != 0:
        if time_now - time_last_pulse > 1:
            # New coin time
            print("New coin time")
            total_pulses = 0
            new_coin = True
        else:
            # Same coin time
            print("Same coin time")
            new_coin = False
    else:
        print("time_last_pulse EQ 0")
        new_coin = False

    return new_coin

def save_money_in_session(pulse_state, pulse_count, money_in_session):
    """
    Saves the money introduced in the current session based on the pulse state.

    Args:
        pulse_state (int): The state of the pulse.
        pulse_count (int): The count of pulses.
        money_in_session (float): The amount of money in the current session.

    Returns:
        tuple: A tuple containing the money earned by pulses and the updated money in session.
    """
    if pulse_state == 1:
        money_by_pulses, money_in_session = pulse_money_equivalences(pulse_count, money_in_session)
        print("pulse_last_state:", pulse_state)
        print("pulse_count:", pulse_count)
        print("money_by_pulses:", money_by_pulses)
        print("money_in_session:", money_in_session)
    else:
        pass

    return money_in_session

def pulse_money_equivalences(total_pulses, money_in_session):
    
    """
    Given a total number of pulses, returns the equivalent money value based on hardcoded rules
    and returns money in session
    
    Parameters
    total_pulses
        int: The total number of pulses to convert to a money value
    
    Returns
        int: The equivalent money value for the given number of pulses, or None if an invalid
        number of pulses is provided
    """

    if total_pulses  == 5:
        money = 1
        money_in_session += money

    elif total_pulses == 6:
        money = 2
        money_in_session += money - 1
    
    elif total_pulses == 7:
        
        money =  5
        money_in_session += money - 2

    elif total_pulses == 8:
        
        money =  10
        money_in_session += money - 5

    else:
        # print(f"other total pulses: {total_pulses:.1f}")
        money =  0
    
    return money, money_in_session
    

def coin_callback(p):
    global time_last_pulse
    global total_pulses
    global money_by_pulses
    global money_in_session

    time_now = time.time()

    # Check if money_in_session is initialized
    if money_in_session is None:
        money_in_session = 0

    # checks if a new coin is introduced
    new_coin = check_for_new_coin(time_last_pulse, time_now)

    # contabilizar los pulsos
    total_pulses = pulse_counter(pin=p, new_coin=new_coin)
    
    # guardar dinero introducido en la sesión
    money_in_session = save_money_in_session(pulse_state, pulse_count, money_in_session)
    globals_file.money_in_session = money_in_session
    
    time_last_pulse = time.time()

    print("END CALLBACK \n\n")
    

def coin_acceptor_constructor(pin_coin_acceptor):
    """ 
    This function initializes the coin acceptor by setting the initial values of
    pulse_last_state, bill_pulse_count, and total_pulses to 0. The function then sets
    up an interrupt service routine (ISR) for the input pin of the coin acceptor to
    handle incoming pulse signals. Finally, the function calls the
    pulse_money_equivalences() function to calculate the total amount of money based
    on the total number of pulses detected.

    Parameters:
    pin_coin_acceptor
        int. This parameter represents the pin number of the input pin connected to the
        coin acceptor.

    Global Variables:
    pulse_last_state
        int. This variable represents the previous state of the pulse.
    bill_pulse_count
        int. This variable represents the total number of coin pulses detected.
    total_pulses
        int. This variable represents the total number of pulses detected plus one.

    Returns:
    None
    """

    global pulse_count, pulse_last_state, total_pulses
    global money_counted, total_pulses_prev, total_pulses
    global time_last_pulse


    pulse_last_state = 0
    pulse_count = 0 
    total_pulses = 0
    total_pulses_prev = 0
    time_last_pulse = 0

    
    global money_in_session
    money_in_session = 0

    
    # pin initialize and callback
    pin_coin =  Pin(pin_coin_acceptor, Pin.IN)
    pin_coin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=coin_callback)



# -----------------------------------

