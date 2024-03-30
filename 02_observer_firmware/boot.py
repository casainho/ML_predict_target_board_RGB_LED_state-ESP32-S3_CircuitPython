# running_mode = 'usb_pc_disabled'
running_mode = 'usb_pc_enabled'

if running_mode == 'usb_pc_enabled':
    import usb_cdc
    import storage
    
    # Disabling USB Mass Storage as the USB endpoints are needed to send data to PC
    storage.disable_usb_drive()

    # Enable USB UART data and keep also the USB UART console data enabled
    usb_cdc.enable(console=False, data=True)

