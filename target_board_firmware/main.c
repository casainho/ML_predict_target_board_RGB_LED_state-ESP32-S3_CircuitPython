/*
 * NRF52840_detect_LED_flashing_by_observing_current
 *
 * Copyright (C) Casainho, 2021
 *
 * Released under the GPL License, Version 3
 * 
 */

#include <stdio.h>
#include "nrf_log.h"
#include "nrf_log_ctrl.h"
#include "nrf_log_default_backends.h"
#include "nrf_drv_clock.h"
#include "nrf.h"
#include "hardfault.h"
#include "app_error.h"
#include "app_timer.h"
#include "nrf_pwr_mgmt.h"
#include "nrf_sdh.h"
#include "ble.h"
#include "ble_err.h"
#include "ble_hci.h"
#include "ble_srv_common.h"
#include "ble_advdata.h"
#include "ble_conn_params.h"
#include "ble_conn_state.h"
#include "peer_manager.h"
#include "peer_manager_handler.h"
#include "ble_advdata.h"
#include "ble_advertising.h"
#include "nrf_sdh.h"
#include "nrf_sdh_ble.h"
#include "nrf_ble_gatt.h"
#include "nrf_ble_qwr.h"
#include "nrf_drv_uart.h"
#include "app_util_platform.h"
#include "nrf_delay.h"
#include "nrf_power.h"
#include <stdbool.h>
#include "pins.h"
#include "nrf_gpio.h"

static void lfclk_config(void)
{
  uint32_t err_code = nrf_drv_clock_init();
  APP_ERROR_CHECK(err_code);

  nrf_drv_clock_lfclk_request(NULL);
}

int main(void)
{
  uint8_t leds_state = 0;

  lfclk_config(); // needed by the APP_TIMER

  nrf_gpio_cfg_output(LED_R__PIN);
  nrf_gpio_cfg_output(LED_G__PIN);
  nrf_gpio_cfg_output(LED_B__PIN);

  nrf_gpio_pin_set(LED_R__PIN);
  nrf_gpio_pin_set(LED_G__PIN);
  nrf_gpio_pin_set(LED_B__PIN);

  while (1) {
    
    if (leds_state & 1) {
      nrf_gpio_pin_clear(LED_R__PIN);
      leds_state &= ~1; 
    } else {
      nrf_gpio_pin_set(LED_R__PIN);
      leds_state |= 1; 
    }

    nrf_delay_ms(1000);  
  }
}
