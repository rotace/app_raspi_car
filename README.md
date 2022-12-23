# app_raspi_car
制御PC, Raspberry-Pi, Arduinoを用いたラジコンカー

## 構成
* 制御PC
* Raspberry-Pi
* Arduino

## 利用方法

### 0. Raspberry-Piへの接続

【制御PC側】
``` bash
# 疎通確認(mDNSを利用)
pc:$ ping raspberrypi.local
# SSH接続(mDNSを利用)
pc:$ ssh pi@raspberrypi.local
```

### 1. Raspberry-Piカメラの確認

【Raspberry-Pi側】
``` bash
# 以下のコマンドを実行
pi:$ cd ${Inst Dir}/app_raspi_car/raspi/
pi:$ make stream
# もしくは、mjpg-streamerのインストール先に移動し以下を実行
pi:$ ./mjpg-streamer -i "input_raspicam.so -fps 10 -q 20 -x 640 -y 480" -o "output_http.so -w ./www -p 9000"
```

【制御PC側】
``` bash
# ブラウザから`http://raspberrypi.local:9000`にアクセスする。
# もしくは、以下を実行
pc:$ cd ${Inst Dir}/app_raspi_car/pc/
pc:$ python3 video_receiver.py
```

### 2. Arduinoへスケッチ書き込み

【Raspberry-Pi側】
``` bash
# arduino-cliのインストール
# https://arduino.github.io/arduino-cli/0.29/installation/
pi:$ cd ~/workspace/
pi:$ curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
# PATHを追加
pi:$ echo "export PATH=$PATH:$HOME/workspace/bin" >> ~/.bashrc
# パッケージのインストール
pi:$ arduino-cli core install arduino:avr
# スケッチへ移動
pi:$ cd ${Inst Dir}/app_raspi_car/arduino/
# スケッチをコンパイル
pi:$ arduino-cli compile -b arduino:avr:nano
# スケッチをアップロード
pi:$ arduino-cli upload -b arduino:avr:nano:cpu=atmega328old -p /dev/ttyUSB0
```

正しくスケッチが書き込まれるか確認する場合は、`https://github.com/arduino/arduino-examples`をクローンして「01.Basics/Blink」（Lチカ）のコンパイル＆アップロードを試してみる。

### 3. 起動

【Raspberry-Pi側】
``` bash
# カメラ起動
pi:$ cd ${Inst Dir}/app_raspi_car/raspi/
pi:$ make stream
# 中継ソフト起動
pi:$ cd ${Inst Dir}/app_raspi_car/raspi/
pi:$ python3 main.py
```

【制御PC側】
``` bash
# 制御ソフト起動
pc:$ cd ${Inst Dir}/app_raspi_car/pc/
pc:$ python3 main.py
```

### 番外1. 「Ctrl+C」で終了できない場合
1. 「Ctrl+Z」を押下し、一時停止する。
1. 「jobs」コマンドでジョブ番号（例:1）を確認する。
1. 「kill %1」でプロセスを終了する。

### 番外2. Raspberry-PiへAndroidからSSH接続
1. Raspberry-PiとAndroidをUSB接続する。
1. AndoridをUSBテザリングモードにする。
1. アプリ「termux」を起動する。
1. コマンド「arp -a」を実行。rndis0のIPを調べる。
1. コマンド「ssh pi@{rndis0'sIP}」を実行。パスワードを入力してログインする。
1. コマンド「ifconfig wlan0」を実行。wlan0のIPを調べる。
1. linux-PCから、「ssh pi@{wlan0'sIP}」を実行。パスワードを入力してログインする。

### 番外3. Raspberry-PiへWifiアクセスポイントを登録

``` bash
# wpa_supplicant.confを編集し以下を追記して再起動
$ sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
>> network={
>>     ssid="SSIDの文字列"
>>     psk="パスワードの文字列"
>> }
```
