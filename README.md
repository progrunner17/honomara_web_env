# ホノルルマラソンを走る会WEBサイト開発用環境

## はじめに
webサイトの開発には、WEBサーバーが必要になりますが、
実際に借りるのはお金がかかるので、仮想的に手元のパソコンにWEBサーバーと同様の環境（ローカル開発環境）を作る必要があります。

以下の手順を踏めば、簡単にローカル開発環境が作れるはずです。


## Prerequisites
このリポジトリを使うには以下の２つのソフトウェアが必要になります。
- Vagrant
- Virtualbox

Macの人は以下のコマンドでインストールできます
~~~console
$ brew cask install virtualbox
$ brew cask install vagrant
~~~
- ※Homebrewを入れてない人は、自分でインストールしてください

LinuxやWindowsの場合は、自分で以下公式サイトからインストーラをダウンロードしてインストールしましょう

- ※apt等でもインストールできるが、バージョンが古いことが多いため

## How to Use(使い方)

### 1.Clone this repo

VagrantとVirtualboxをインストールしたら、
このリポジトリを以下のコマンドでダウンロードしてください。

- ※リポジトリとは、簡単に説明すると、gitが管理するディレクトリ(フォルダ)のことです
- ※リポジトリをダウンロードすることを、「クローン」といいます。
~~~console
$ git clone https://github.com/progrunner17/honomara_web_env.git
~~~

### 2.Start the virtual machine
vagrant ディレクトリに移動して`vagrant up`コマンドを実行してください。

こうすることで、仮想的なサーバー（仮想マシン）が起動します。
- ※開発者はフォルダのことを「ディレクトリ」と呼びます。なれましょう
- ※vagrantコマンドは、実行するディレクトリで挙動が変わります。vagrantディレクトリにいることをしっかり確認しましょう。
    -（他のディレクトリで実行してもパソコンが壊れることはないですが、単純に動きません）
~~~console
$ cd vagrant
$ vagrant up
~~~

### 3.Connect to the virtual machine

`vagrant ssh`コマンドを実行してください。
こうすることで、仮想マシンに接続できます。

~~~console
$ vagrant ssh
~~~

以降、仮想マシンに接続した状態での操作となります。

~~~console:local
$ vagrant ssh
~~~
をした後
~~~console:guest
$ cd /vagrant/scripts
$ ./setup_all.sh
$ ./import_data_to_postgres.sh
$ ./migrate_data_to_mysql.sh
~~~
を実行して、`app`ディレクトリに [honomara_members_siteのリポジトリ](https://github.com/progrunner17/honomara_members_site) かそのフォークをcloneすれば
[127.0.0.1:8080/cgi-bin](http://127.0.0.1:8080/cgi-bin)  
からサイトを見れると思います。  
デバッグ時は、ゲストの`/vagrant/app`ディレクトリで`python3 app.py`を実行して  
[127.0.0.1:5000/cgi-bin](http://127.0.0.1:5000)  
から見ると良いと思います。

なお、現在更新されていませんが、  
以下の方法でjupyter noteookを見ると、大まかな解説が書いてあるので理解の助けになるかもしれません。  
ただ、重ねて注意ですが、現在メンテナンスされておらず、齟齬があるので、
詳しくは、上記のスクリプトを読むと良いでしょう。
~~~console:guest
$ cd /vagrant
$ ./scripts/setup_jupyter.sh
$ jupyter notebook &
~~~
を実行して

[127.0.0.1:9999](http://127.0.0.1:9999)
または
[localhost:9999](http://localhost:9999)
を開き、

`setup.ipynb`
を開いて、ノートブック中の説明を読んでください。

作成中のアプリを使えるようになるはずです。
また、setupノートブックで言及が無いノートブックも挙げてあるので、見てみると良いかもしれません。

### Exit from the virtual machine

なお、1度jupyter notebookを起動したらターミナルは閉じて構いません。
`exit` コマンドまたは `Ctrl+d` で仮想マシンから抜けられます。


### Halt or suspend the virtual machine
ただ仮想マシンから抜けるだけだと裏で仮想マシンが動いています。

なので、`vagrant ssh`コマンドを実行すると、再度仮想マシンに接続できます。

このままだと、パソコンの資源が食われて重いので、仮想マシンを中断または停止しましょう。

`vagrant halt`で停止（シャットダウン相当）`vagrant suspend`で休止します
それぞれ、再開する場合は`vagrant up` , `vagrant resume`コマンドを実行しましょう。


### Reset the virtual machine
vagrant ディレクトリで`vagrant destroy`仮想マシンを破壊できます。
「データをリセットしたい」、「よくわからなくなった」という場合は
このコマンドで仮想マシンを廃棄した後再度上から順に実行しましょう。

## tips
### Run SQL files
`psql`コマンドは-fオプションでSQLファイルを実行できます。
~~~console
$ psql -U honomara -d honomara -f SQLファイル名
~~~
setup_db.shファイルを読むと参考になるかもしれません。

単純にログインしてSQLを実行するのにも使えますが、整形が大変なのでノートブックからpythonでデータを取得するほうが遊びやすいと思います。

## Trouble shooting

### ホスト、ゲスト間のフォルダ共有ができない
`vagrant up`した際、[Qiita-Vagrant ファイル共有とマウントエラー対処法](https://qiita.com/KZ-taran/items/f78790b580e3f8227173#%E3%83%9E%E3%82%A6%E3%83%B3%E3%83%88%E3%82%A8%E3%83%A9%E3%83%BC)
のようなエラーメッセージが表示され、ホスト、ゲスト間のフォルダ共有ができていないことがあります。
原因はVirtualBox Guest Additions(ホストOSとゲストOSの統合を行うもの)のバージョンの不一致のようです。

解決法は他にもありますが、バージョンを一致させるのが良いです。

ホストの方が古い場合は、VirtualBoxの最新版をダウンロードしてインストールします。
(homebrewでインストールしてもバージョンが古い場合があります。)

ゲストの方が古い場合は、「vagrant-vbguest」(Guest Additionsを自動更新してくれるプラグイン)をインストールします。

以下のコマンドでインストールできます。
~~~console
$ vagrant plugin install vagrant-vbguest
~~~

仮想マシンを起動し、エラーメッセージが出なくなればOKです。

[こちら]( https://qiita.com/ozawan/items/9751dcfd9bd4c470cd82)の記事も参考になります。