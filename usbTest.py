import hid
# enumerate USB devices

for d in hid.enumerate():
    if d['usage_page']== 65329:
        path = d['path']

# try opening a device, then perform write and read

try:
    print("Opening the device")

    h = hid.device()
    h.open_path(path) # TREZOR VendorID/ProductID

    print("Manufacturer: %s" % h.get_manufacturer_string())
    print("Product: %s" % h.get_product_string())
    print("Serial No: %s" % h.get_serial_number_string())

    while True:
        d = h.read(64,25)
        if d:
            text = ""
            for x in d:
                text += chr(x)
            print(text)
        else:
            pass

    h.close()

except IOError as ex:
    print(ex)
    print("You probably don't have the hard coded device. Update the hid.device line")
    print("in this script with one from the enumeration list output above and try again.")

print("Done")