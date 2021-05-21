echo "CyberDrop Downloader 🍑"

read -p "Install requirements? (y/n) " yn

if [[ "$yn" =~ ^([yY][eE][sS]|[yY])$ ]]
then
    echo "Installing requirements..."
    pip3 install -r requirements.txt
fi

read -p "Enter Album ID (last part of url): " album_id
echo "Start downloading from https://cyberdrop.me/a/$album_id..."

python3 main.py "$album_id"