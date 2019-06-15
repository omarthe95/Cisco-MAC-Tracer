mkdir Script/output
mkdir -p /home/bin/P1/Script
cp -a Script/. /home/bin/P1/Script
cp -a Project-1.py /home/bin/P1
chmod +x /home/bin/P1/Project-1.py


file="/etc/profile"
if grep -qF 'export PATH="$PATH:/home/bin/P1"' "$file";then
   :
else
   echo 'export PATH="$PATH:/home/bin/P1"' >> "$file"
fi

source /etc/profile
echo $PATH


String1="Host *"
String2="    StrictHostKeyChecking no"
String3="    KexAlgorithms=+diffie-hellman-group1-sha1"

file="/root/.ssh/config"
if grep -qF "$String1" "$file";then
   :
else
   echo "$String1" >> "$file"
fi

if grep -qF "$String2" "$file";then
   :
else
   echo "$String2" >> "$file"
fi

if grep -qF "$String3" "$file";then
   :
else
   echo "$String3" >> "$file"
fi

sudo apt update
sudo apt install python3-pip
pip3 --version
pip3 install netmiko


while true; do
    read -p "Do you want to delete setup directory [y/n]?" yn
    case $yn in
        [Yy]* ) cd ..;rm -Rf P1; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

