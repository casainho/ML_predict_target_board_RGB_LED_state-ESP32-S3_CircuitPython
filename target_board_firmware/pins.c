/*
 * NRF52840_detect_LED_flashing_by_observing_current
 *
 * Copyright (C) Casainho, 2021
 *
 * Released under the GPL License, Version 3
 * 
 */

#include <stdio.h>
#include <stdbool.h>
#include "nrf_gpio.h"
#include "pins.h"

void pins_init(void)
{
  nrf_gpio_cfg_output(MOTOR_POWER_ENABLE__PIN);
  nrf_gpio_pin_clear(MOTOR_POWER_ENABLE__PIN);
  nrf_gpio_cfg_output(BRAKE__PIN);
  nrf_gpio_pin_set(BRAKE__PIN);
  nrf_gpio_cfg_sense_input(PLUS__PIN, GPIO_PIN_CNF_PULL_Pullup, GPIO_PIN_CNF_SENSE_Low);
  nrf_gpio_cfg_sense_input(MINUS__PIN, GPIO_PIN_CNF_PULL_Pullup, GPIO_PIN_CNF_SENSE_Low);
  nrf_gpio_cfg_sense_input(ENTER__PIN, GPIO_PIN_CNF_PULL_Pullup, GPIO_PIN_CNF_SENSE_Low);
  nrf_gpio_cfg_sense_input(STANDBY__PIN, GPIO_PIN_CNF_PULL_Pullup, GPIO_PIN_CNF_SENSE_Low);
}

void motor_power_enable(bool state)
{
  if (state)
    nrf_gpio_pin_set(MOTOR_POWER_ENABLE__PIN);
  else
    nrf_gpio_pin_clear(MOTOR_POWER_ENABLE__PIN);
}
