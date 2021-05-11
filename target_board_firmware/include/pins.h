/*
 * NRF52840_detect_LED_flashing_by_observing_current
 *
 * Copyright (C) Casainho, 2021
 *
 * Released under the GPL License, Version 3
 * 
 */

#ifndef PINS_H_
#define PINS_H_

#include <stdio.h>
#include <stdbool.h>
#include "nrf_gpio.h"

void pins_init(void);

typedef enum {
  LED_R__PIN  = 8,
  LED_G__PIN  = 32 + 9, // P1.9
  LED_B__PIN  = 12,
} LED_pins_t;

#define BUTTON__PIN 32 + 6 // P1.6

#endif /* PINS_H_ */
