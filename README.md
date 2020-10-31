# TouchScreenRotate
This Rotates your screen and touchscreen input device accdording to it's position sensor on (Ubuntu-)Linux.

## set it up
Please find out what the name of your touchscreen input device is. To do so execute

`xinput --list`

and guess which one it is (it won't be your Touchpad...).

Then insert it the the according variable in the python script.

Maybe you will also need to configure an offset if the normal-mode isn't normal, the options are 0, 90, 180 and 270.

Finally I recommend you to autostart the script on system start.

## other hints

I created this for my OneMix S1 pocket netbook.

If you got here maybe you are looking for a driver for a Stylus for your device as well, I found this [Goodix Touchscreen driver from Adya](https://gitlab.com/AdyaAdya/goodix-touchscreen-linux-driver) that is working on my device, thanks for this, Adya!
