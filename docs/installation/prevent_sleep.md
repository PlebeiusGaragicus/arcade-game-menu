```sh
# Disable screen saver
echo "xset s off" >> ~/.xprofile

# Disable DPMS (Energy Star) features.
echo "xset -dpms" >> ~/.xprofile

sudo nano /etc/systemd/logind.conf

# uncomment these lines:
# IdleAction=ignore
# IdleActionSec=0
```
