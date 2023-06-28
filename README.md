# Coin acceptor Micropython

This repository contains the code for controlling a coin acceptor using a microcontroller. The code is written in MicroPython and designed to run on any MicroPython boards but it is only tested on a esp32.

I used [this tutorial in arduino language](https://www.instructables.com/How-to-Control-CH-926-Coin-Acceptor-With-Arduino/) as a guide to developing a micropython implementation.

## Overview
The coin acceptor controller consists of several functions for counting pulses and calculating the equivalent money value based on predefined rules. It provides the following functionality:

- **Pulse Counter:** The pulse_counter() function counts the pulses received from the coin acceptor and updates the pulse count accordingly. It also handles detecting new coins.
- **New Coin Detection:** The check_for_new_coin() function checks if a new coin is introduced based on the time elapsed since the last pulse. It returns a boolean value indicating whether a new coin is detected.
- **Money Calculation:** The save_money_in_session() function saves the money introduced in the current session based on the pulse state. It uses the pulse_money_equivalences() function to calculate the equivalent money value based on the total number of pulses detected.
- **Coin Acceptor Initialization:** The coin_acceptor_constructor() function initializes the coin acceptor by setting the initial values and configuring the input pin with an interrupt service routine (ISR) to handle incoming pulse signals.


### Pin connections

Connect the pins as showed below:


| Pin Coin Acceptor                                               | Board  | Other                   |
|-----------------------------------------------------------------|--------|-------------------------|
| DC12                                                            | None   | Connect to a 12V source |
| GND                                                             | GND    | 12V ground              |
| COIN (through this pin impulses are sent to the microcontroller | Pin 15 |                         |

![horla](/assets/connections.jpeg)

*Note:* as show in the picture, you need to add a 10 KOhm resistance in the COIN pin.

## Setup acceptor swithches

### Impuls length

- fast(20ms) **select this**
- medium(50ms)
- slow(100ms)

### Normally open and Normally closed switch

- Select normally closed


### Progam the acceptor


Here is the procedure how to program the acceptor to recognise a set of different coins. 

1. Press the "Add" and "minus" buttons at the same time for about three seconds, then the letter "A" will appear from the LED display.
2. Press the "setup" button once, and the letter "E" will appear. Next, use the buttons to choose how many kinds of coins you would like to use; then press the "setup" button again to finish.
3. The letter "H" will appear after pressing the button. Use the "Add" and "minus" buttons to choose how many samples you would like to insert later. Next press the "setup" button again to finish.
4. The letter "P" will appear after pressing the button. Use the "Add" and "minus" buttons to choose the amount of output's signals/pulses you want. The quantity limited is 50 times. I recommend using something between 5 and 10 pulses. Next, press the "setup" button to finish.
5. The letter "F" will appear after pressing the button. Use the "Add" and "minus" buttons to choose accuracy. The value is from 1~30, and 1 is the most accurate. Normally, 5~10 will be fine.Next, press the "setup" button to finish.
6. So far, you have  set up the first coin.  repeat all above procedures until you have set up all the coins. The letter "A" will appear again after all above procedures are finished.
7. Press the "setup" button, and the letter "E" will appear. Finally, turn off and turn on the power. The setup will be stored.

After that you can stast start sampling process. The manufacter recommends using 20 different coins. The sampling process will affect the accuracy of coin selector.

## Interrupts and Their Necessity
The coin acceptor controller utilizes interrupts to handle incoming pulse signals from the coin acceptor. An interrupt is an event that interrupts the normal execution of a program and triggers a specific function called an interrupt service routine (ISR). Here's why interrupts are necessary in this context:

- **Real-Time Response:** The coin acceptor generates pulses at a rapid pace, and it's crucial to detect and respond to these pulses in real-time. By using interrupts, the microcontroller can immediately interrupt its ongoing tasks and execute the ISR as soon as a pulse is detected, ensuring timely and accurate pulse counting.
- **Non-Blocking Operation:** Interrupts allow the microcontroller to handle pulse detection and counting independently of other program operations. This non-blocking behavior ensures that the microcontroller can perform other tasks while waiting for pulses, such as updating display information or controlling other peripherals.

## Start counting coins

To start simply run main.py.
