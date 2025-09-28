#include <sys/unistd.h>
#include <stdio.h>
#include "hal/gpio_types.h"
#include "driver/gpio.h"

#define LED_PIN GPIO_NUM_2

void app_main(void) {
	// Send message once
	printf("Hello, world! Message from ESP32 DevKit V1.\n");

	// Set led pin mode to OUTPUT
	gpio_set_direction(LED_PIN, GPIO_MODE_OUTPUT);

	// Create the main loop
	while (1) {
		printf("LED is now ON!\n");
		gpio_set_level(LED_PIN, 1);
		usleep(1000000);
		printf("LED is now OFF!\n");
		gpio_set_level(LED_PIN, 0);
		usleep(1000000);
	}
}
