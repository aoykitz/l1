<img width="858" height="525" alt="image" src="https://github.com/user-attachments/assets/92e51cd9-e594-40ff-bee2-108eb2615933" />
<img width="848" height="735" alt="image" src="https://github.com/user-attachments/assets/1f93fd86-e866-436b-bfe5-b137b3f82216" />
<img width="985" height="649" alt="image" src="https://github.com/user-attachments/assets/3f664910-ec3d-44c2-adb0-04ead9380bdf" />
sudo apt update
sudo apt install dotnet-sdk-8.0
dotnet --version
mkdir FifteenGame
cd FifteenGame
dotnet new console -n FifteenGame
cd FifteenGame
dotnet run

dotnet publish -c Release -r linux-x64 --self-contained true
./FifteenGame

sudo apt install mono-complete
mcs Program.cs -out:FifteenGame.exe
mono FifteenGame.exe
