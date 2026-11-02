// SPDX-License-Identifier: Apache-2.0
// OpenPet ESP32-S3 body controller. Phase 0: toolchain smoke test only.
// The servo bus driver, IMU loop, micro-ROS bridge and safety layer arrive in Phase 2.

#include "esp_log.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

static const char *TAG = "openpet";

void app_main(void)
{
    for (int i = 0;; i++) {
        ESP_LOGI(TAG, "body controller alive #%d", i);
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}
