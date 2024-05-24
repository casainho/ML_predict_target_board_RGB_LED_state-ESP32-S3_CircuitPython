class RunningMode:
    USB_PC_DISABLED = 0
    USB_PC_ENABLED = 1
    
running_mode = RunningMode.USB_PC_ENABLED
# running_mode = RunningMode.USB_PC_DISABLED

if running_mode == RunningMode.USB_PC_ENABLED:
    # Disabling USB Mass Storage as the USB endpoints are needed to send data to PC
    import storage
    storage.disable_usb_drive()

    # Enable USB UART data and keep also the USB UART console data enabled
    import usb_cdc
    usb_cdc.enable(console=False, data=True)
