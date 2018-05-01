# app-raspi-car
linux-PC, raspberry-pi, arduinoを用いたラジコンカー

### 構成
* サーバ：linux-PC
* クライアント：raspberry-pi または linux-PC 

# 起動手順
## 0. raspberry-piへの接続
raspberry-piをlinux-PCからssh接続でリモート操作する。クライアントもlinux-PCの場合はこの手順は不要となる。raspberry-piのIPアドレスがわからない場合のために、androidアプリを利用した方法を説明する。  

参考WEB: [Raspberry Pi Zero に Android からUSBテザリングでSSH接続](http://homemadegarbage.0t0.jp/pizero-android-usbtethering)
1. raspberry-piとandroidをUSB接続する。
1. andoridをUSBテザリングモードにする。
1. アプリ「termux」を起動する。
1. コマンド「arp -a」を実行。rndis0のIPを調べる。
1. コマンド「ssh pi@{rndis0'sIP}」を実行。パスワードを入力してログインする。
1. コマンド「ifconfig wlan0」を実行。wlan0のIPを調べる。
1. linux-PCから、「ssh pi@{wlan0'sIP}」を実行。パスワードを入力してログインする。

## 1. サーバ及びクライアントの準備
1. サーバのIPアドレスを取得  
    ifconfigコマンドでwlan0のIPアドレスを調べる。
    コマンド「make conf」を実行すると、自身のIPアドレスをconfig.iniに格納する。
1. クライアントにサーバのIPアドレスを設定
    先ほど調べたIPアドレスをクライアント側のconfig.iniに書き込む。
    コマンド「make host='192.168.x.x' conf」を実行すると、IPアドレスをconfig.iniに格納する。

## 2. サーバ->クライアントの順に起動
1. サーバでコマンド「make run」を実行。
1. クライアントでコマンド「make run」を実行。

# デバッグモード
controller, cammera, arduinoのそれぞれがない場合は、以下のコマンドでconfig.iniを生成する。
* make has_controller='false' conf
* make has_cammera='false' conf
* make has_arduino='false' conf