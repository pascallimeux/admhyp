#!/bin/bash
ADMUSERNAME=orangeadm
PUBKEY="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDKmfqZPFqSKmjrqBt/7+YhN2lhYaCpP3v6flEt3Ff9rwpe+gGRr/jaNbl3YNgufp10iM6Q5qEOf4e7/Sh2LAsXcEjP8g8zkxqrTbb5S7VrCYRNpz4wCHKNboqvFtmVRdjijZqd/7xWzkb/CxPOVdnGjD4ddYRzt6jlWWiC/O9obEClgHcmcQBL5VlhCFg+Wi6y5OFvCVg91YYGbdFEDjCaOoysWKJxwJEpUd8MYihCp7T75+p3esdkRtpK5rqTECTY7In9t87P7J+kcrkU3avE7OYs7gRZvT1QhxhycrjQTH1mpC0aEQaZ9NBVNIAH8qmgjQtzgXT2ajf70hDG635R pascal@pascal-VirtualBox"
SUDOERLINE="$ADMUSERNAME ALL=(ALL:ALL) NOPASSWD:ALL"
if id $ADMUSERNAME >/dev/null 2>&1; then
    echo -e "user $ADMUSERNAME already exists!"
else
    echo -e "create user $ADMUSERNAME"
    sudo useradd -m $ADMUSERNAME -s /bin/bash
fi
if [ ! -f /etc/sudoers.d/$ADMUSERNAME ]; then
    echo $SUDOERLINE > /tmp/$ADMUSERNAME
    sudo chown root.root /tmp/$ADMUSERNAME
    sudo chmod ug-w /tmp/$ADMUSERNAME
    sudo mv /tmp/$ADMUSERNAME /etc/sudoers.d/$ADMUSERNAME
    echo -e "create file /etc/sudoers.d/$ADMUSERNAME"
else
    echo -e "file /etc/sudoers.d/$ADMUSERNAME already exists!"
fi
if [ ! -d /home/$ADMUSERNAME/.ssh ]; then
    sudo mkdir /home/$ADMUSERNAME/.ssh
fi
sudo chmod 777 -R /home/$ADMUSERNAME/.ssh
echo $PUBKEY >> /home/$ADMUSERNAME/.ssh/authorized_keys
sudo chown -R $ADMUSERNAME.$ADMUSERNAME /home/$ADMUSERNAME/.ssh
sudo chmod 700 /home/$ADMUSERNAME/.ssh
sudo chmod 600 /home/$ADMUSERNAME/.ssh/authorized_keys
echo -e "add public key in /home/$ADMUSERNAME/.ssh/authorized_keys"

