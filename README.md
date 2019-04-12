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

### 4.Set up the Database
`vagrant ssh`コマンドを実行すると、vagrantというユーザー名で/home/vagrantディレクトリに入ります。  
その下のhost_dataディレクトリがリポジトリのvagrantディレクトリと同期するよう設定してあります。  

更にそのディレクトリにscriptsディレクトリがあり、  その中の`setup_db.sh`というスクリプトがあるので実行してください。

すると、データベース（postgresqlというソフト）がインストールされた後、ホノマラの過去のデータがデータベースにインポートされます。

接続設定は以下のとおりです

- database: honomara
- user(role): honomara
- password: honomara

~~~console
$ cd host_data
$ cd scripts
$ ./setup_db.sh
~~~


### Test and try the database
早速データベースを試してみましょう。  
`psql`というコマンドでデータベースに接続します。    
いろいろなSQLを試して、データを扱う練習をすると良いです。    

~~~console
$ psql -U honomara -d honomara
ここでパスワードを聞かれるので、honomaraと入力する
honomara=> SELECT * FROM person LIMIT 10;
それっぽいデータが表示される。
honomara=>\q
\qと入力すると終了する。
$
~~~

### Exit from the virtual machine
`exit`コマンドで仮想マシンから抜けられます。


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


## Loadmap
WEBサーバーや言語ランタイム(PHP,Python,Ruby)等の設定を追加していくつもりです。  
(一応設定スクリプトは書いたのですが、ドキュメントを書くのが疲れたので、今はここまで。  
気になる人は`vagrant/scripts`ディレクトリを見てみてください。)