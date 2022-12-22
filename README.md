# app_raspi_car
linux-PC, raspberry-pi, arduinoを用いたラジコンカー

## 構成
* 制御PC
* Raspberry-Pi

## 利用方法

### 0. Raspberry-Piへの接続
Raspberry-Piを制御PCからssh接続する。 
``` bash
# 疎通確認(mDNSを利用)
PC:$ ping raspberrypi.local
# SSH接続(mDNSを利用)
PC:$ ssh pi@raspberrypi.local
```

### 1. Raspberry-Piカメラの確認
Raspberry-Piカメラを制御PCから動作確認する。

``` bash
# mjpg-streamerのインストール先に移動し以下を実行
pi:$ ./mjpg-streamer -i "input_raspicam.so -fps 10 -q 20 -x 640 -y 480" -o "output_http.so -w ./www -p 9000"
```

mjpg-streamerの起動後に、制御PCのブラウザから`http://raspberrypi.local:9000`にアクセスする。

### 2. サーバ及びクライアントの準備
1. サーバのIPアドレスを取得  
    ifconfigコマンドでwlan0のIPアドレスを調べる。
    コマンド「make conf」を実行すると、自身のIPアドレスをconfig.iniに格納する。
1. クライアントにサーバのIPアドレスを設定
    先ほど調べたIPアドレスをクライアント側のconfig.iniに書き込む。
    コマンド「make host='192.168.x.x' conf」を実行すると、IPアドレスをconfig.iniに格納する。

### 3. サーバ->クライアントの順に起動
1. サーバでコマンド「make run」を実行。
1. クライアントでコマンド「make run」を実行。

### 番外0. デバッグモード
controller, cammera, arduinoのそれぞれがない場合は、以下のコマンドでconfig.iniを生成する。
* make has_controller='false' conf
* make has_cammera='false' conf
* make has_arduino='false' conf

### 番外1. Raspberry-PiへAndroidからSSH接続
1. Raspberry-PiとAndroidをUSB接続する。
1. AndoridをUSBテザリングモードにする。
1. アプリ「termux」を起動する。
1. コマンド「arp -a」を実行。rndis0のIPを調べる。
1. コマンド「ssh pi@{rndis0'sIP}」を実行。パスワードを入力してログインする。
1. コマンド「ifconfig wlan0」を実行。wlan0のIPを調べる。
1. linux-PCから、「ssh pi@{wlan0'sIP}」を実行。パスワードを入力してログインする。

### 番外2. Raspberry-PiへWifiアクセスポイントを登録

``` bash
# wpa_supplicant.confを編集し以下を追記して再起動
$ sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
>> network={
>>     ssid="SSIDの文字列"
>>     psk="パスワードの文字列"
>> }
```
