__これは公式ではなく、有志によって日本語へ翻訳されたものです。__  
__This isn't the official, but was translated into Japanese by a volunteer.__

---

# ビルドの工程 (GNU Arm Embedded Toolchain 10.3-2021.07)

__2021-07__  
__Copyright (C) 2012-2021 ARM Ltd.__  

## 目次

```
はじめに

第1章: LinuxとWindows用のGNUツールをビルドする
    1.1: Ubuntuのインストール
    1.2: インストールの依存関係
        1.2.1: Ubuntuのリポジトリで利用可能な依存関係をインストールする
    1.3: GNU Arm Embedded Toolchain をビルドする

第2章: Mac OS XでGNUツールをビルドする
    2.1: Mac OS X環境を準備する
    2.2: Xcode用のコマンドラインツールをインストールする
    2.3: Mac OS X で最新のBashを使用する
    2.4: GNUドキュメンテーションシステムをビルドする
    2.5: PDF形式のドキュメントを作成するために、MacTeXをインストールする
    2.6: Mac OS Xでツールチェーンをビルドする

追加 A: 既知の問題
```

## はじめに

このマニュアルは、Ubuntu 14.04 LTS 64bit op-up 上で "GNU Arm
Embedded Toolchain" のビルドに役立つ着実なガイドを提供します。  
以下の手順は、最新でない Ubuntu や、14.04 LTS 以外のバージョンでも動作する可能性があります。  
ですが、保証するものではありません。  
その場合は、"追加 A: 既知の問題" を参照してください。  
また、その他の問題が発生した場合は、ご自身で解決していただく必要があります。  
問題点や解決方法を共有していただけると幸いです。  

## 第1章: LinuxとWindows用のGNUツールをビルドする

### 1.1: Ubuntuのインストール

Ubuntu 14.04.5 の ISOイメージは、<http://releases.ubuntu.com/14.04/ubuntu-14.04.5-desktop-amd64.iso> です。  
ネイティブシステムまたは仮想マシンとしてインストールすることができます。  

### 1.2: インストールの依存関係

#### 1.2.1: Ubuntuのリポジトリで利用可能な依存関係をインストールする

これらのコマンドを実行して、ビルドに必要なツールをインストールします。  
`"$"` で始まる行は、そのまま入力する必要のあるコマンドです。  
`"#"` で始まる行はコメントであり、入力する必要はありません。  
`apt-get update`実行時に `"Ignoring Provides line"` と `"unknown Multi-Arch type"` という警告が表示されますが無害です。  
同様に、`update-alternatives`がシンボリックリンクの作成をスキップするという警告も無害です。  
だから、これらの警告を無視してもらって構いません。  

スーパーユーザへなります:  

```bash
sudo su
```

32bit用パッケージを有効化します:  

```bash
dpkg --add-architecture i386
```

aptで使用するリポジトリを追加します:  

```bash
$ apt-get update
$ apt-get install software-properties-common
$ add-apt-repository universe
$ cat > /etc/apt/sources.list.d/xenial.list << EOF
deb http://archive.ubuntu.com/ubuntu xenial main universe
deb-src http://archive.ubuntu.com/ubuntu xenial main universe
deb http://security.ubuntu.com/ubuntu xenial-security main
EOF
```

UbuntuTrusty のパッケージがデフォルトで選択されていることを確認します:  

```bash
echo 'APT::Default-Release "trusty";' > /etc/apt/apt.conf.d/00default
```

パッケージをインストールします:  

```bash
$ apt-get install -y -t xenial \
gcc-mingw-w64-i686 g++-mingw-w64-i686 binutils-mingw-w64-i686

$ apt-get -f install -y \
build-essential autoconf autogen bison dejagnu flex flip \
gawk git gperf gzip nsis openssh-client p7zip-full perl \
python-dev libisl-dev scons tcl texinfo tofrodos wget zip \
texlive texlive-extra-utils libncurses5-dev
```

スーパーユーザでの作業は以上です:  

```bash
exit
```

### 1.3: GNU Arm Embedded Toolchain をビルドする

これで、ツールチェーンをビルドする準備が整いました。以下の指示に従ってください。  
`~/toolchain` を、ツールチェーンをビルドしたいディレクトリに置き換えてください。  
尚、Windowsのツールチェーンに興味がない場合は、  
`install-sources.sh, build-prerequisites.sh、build-toolchain.sh` のすべてに `"--skip_steps=mingw32"` というオプションを渡すことで、ビルドを高速化できます。

```bash
# ツールチェーンをビルドするディレクトリを作成し、ソースコードをコピーします。
# そして、その中にパッケージを入れます。
$ mkdir ~/toolchain
$ cp gcc-arm-none-eabi-10.3-2021.07-src.tar.bz2 ~/toolchain

# tar玉を解凍します。
$ cd ~/toolchain
$ tar -jxvf gcc-arm-none-eabi-10.3-2021.07-src.tar.bz2
$ cd ./gcc-arm-none-eabi-10.3-2021.07
$ ./install-sources.sh

# ツールチェーンをビルドします。
$ ./build-prerequisites.sh
$ ./build-toolchain.sh
```

ビルドが完了すると、バイナリとソースコードのtar玉を見つけることができます。  
`~/toolchain/gcc-arm-none-eabi-10.3-2021.07/pkg`  
一緒にMD5チェックサムも行ってください。  

## 第2章: Mac OS XでGNUツールをビルドする

Ubuntu でのビルドに加えて、同じソースパッケージに含まれるビルドスクリプトは Mac OS X でも使用することができます。  
ホストが Mac OS X、ターゲットが arm-non-eabi のネイティブツールチェーンをビルドできます。  
この手順では、必要なソフトウェアコンポーネントのインストール方法と、ビルドスクリプトの実行方法を説明します。  
リリースされているものと同じツールチェーンを生成することができます。  
尚、リソースの関係上、このビルドは以下の環境でのみテストされています。  

```
・macOS Mojave 10.14.6
・macOS Catalina 10.15.4
```

### 2.1: Mac OS X環境を準備する

ハードウェアは `"x86-based Apple Mac family"` でなければなりません。  
また、OSは `"OSMac OS X 10.14.6"` 以降のバージョンを使用しなければなりません。  
Mac OS X のバージョンを確認するには、Appleメニューから "このMacについて" を選択するか、コマンドラインで次のように入力します:  

```bash
sw_vers -productVersion
```

### 2.2: Xcode用のコマンドラインツールをインストールする

このパッケージは次のコマンドでインストールできます。  

```bash
xcode-select --install
```

上記でエラーが発生した場合は次のサイトにアクセスしてください。  
<https://developer.apple.com/download/more/>  
例えば、Xcode 11.5 用の Command Line Tools などは、Appleのウェブページから直接ダウンロードできます。  
その際、Apple IDでのログインが必要となります。  

### 2.3: Mac OS X で最新のBashを使用する

この手順はオプションです。  
ツールチェーンのBashビルドスクリプトを実行する際には、Bash 5を使用することをお勧めします。  
私たちは現在、Bashを使用しています:  

```bash
$ bash --version
GNU bash, version 5.0.16(1)-release (x86_64-apple-darwin18.7.0)
```

最新バージョンのBashをインストールするには、homebrewを使用することをお勧めします:  

```bash
brew install bash
```

### 2.4: GNUドキュメンテーションシステムをビルドする

Texinfoは、GNUプロジェクトの公式ドキュメント形式です。  
Texinfoは、オンラインや印刷の両方で、さまざまな形式の出力を生成します。  
これらの形式には、`dvi, html, info, pdf, xml` などがあります。  
このパッケージは、マニュアルと方法を示したPDFドキュメントの作成に必要です。  
この工程は `"build-toolchain.sh"` に `"--skip_steps=howto,manual"` というオプションを渡すことで、スキップすることもできます。  

Texinfo 6.5 のソースを取得します:  

```bash
$ cd /tmp
$ curl -OL https://ftp.gnu.org/gnu/texinfo/texinfo-6.5.tar.xz
$ tar -Jxvf texinfo-6.5.tar.xz
$ cd texinfo-6.5/

# この例では、Texinfoを任意のディレクトリ (今回は /tmp/texinfo) にインストールします。
# ディレクトリを作成します。
$ mkdir /tmp/texinfo
$ ./configure --prefix=/tmp/texinfo
$ make
$ make install
```

Texinfo6.5をインストールしたディレクトリを環境変数PATHに追加します:  

```bash
export PATH=/tmp/texinfo/bin:$PATH
```

### 2.5: PDF形式のドキュメントを作成するために、MacTeXをインストールする

これはオプションの手順で、PDF形式のドキュメントが必要ない場合はスキップすることができます。  
ビルドプロセスでは、MacTeX-2012 で提供されている TeXエンジニア を使用して、PDF形式のドキュメントを生成します。  
このコンポーネントは以下の公式FTPサーバーから自由に入手できます。  
<ftp://ftp.tug.org/historic/systems/mactex/2012/MacTeX.pkg>  
オリジナルのファイルサイズは約2.1GBです。  
ダウンロードが完了したら、`"MacTeX.pkg"` ファイルをダブルクリックして、インストールしてください。  
デフォルトでは、関連するTeXの実行ファイルは `"/usr/bin"` のようなデフォルトのパスにはインストールされません。  
だから、ビルドスクリプトを実行する前に端末を再起動する必要があります。  

尚、Homebrewを使って MacTeX をインストールすることも可能です。  

Caskを経由します:  

```bash
brew install Caskroom/cask/mactex
```

GUI無しの MacTex をインストールしたい場合は、次のコマンドが利用できます:  

```bash
brew install Caskroom/cask/mactex-no-gui
```

### 2.6: Mac OS Xでツールチェーンをビルドする

すべての依存関係がインストールされたら、Mac OS上でネイティブのツールチェーンのビルドを開始できます。  
以下に、使用するコマンドと手順を示します。  

```bash
# ソースコードを ~/mac-build/ ディレクトリにコピーします。
$ cp gcc-arm-none-eabi-10.3-2021.07-src.tar.bz2 ~/mac-build

# ソースコードを準備します。(tar玉の解凍)
$ cd ~/mac-build
$ tar -jxvf gcc-arm-none-eabi-10.3-2021.07-src.tar.bz2
$ cd ./gcc-arm-none-eabi-10.3-2021.07
$ ./install-sources.sh

# ツールチェーンのビルドを開始します。
$ ./build-prerequisites.sh
$ ./build-toolchain.sh
```

ツールチェーンのビルドが完了したら、pkg/ 以下のバイナリとソースのMD5チェックサムを確認してください:  

```bash
~/mac-build/gcc-arm-none-eabi-10.3-2021.07/pkg $ ls -l
gcc-arm-none-eabi-10.3-2021.07-mac-10.15.4.tar.bz2
gcc-arm-none-eabi-10.3-2021.07-src.tar.bz2
md5-x86_64-darwin.txt
```

## 追加 A: 既知の問題

異なるビルド環境やツールを使用している場合、binutils が正常にビルドできないという問題に遭遇するかもしれません。  
これの原因はおそらく binutils のバグ13036です。  
詳細については <http://sourceware.org/bugzilla/show_bug.cgi?id=13036> を参照してください。  

gccやその他のパッケージに含まれる一部のシェルスクリプトは、Ubuntu 14.04 LTS のデフォルトの `/bin/sh` である
ダッシュシェル (Ubuntu 14.04 LTS のデフォルトは `/bin/sh`) との互換性がありません。  
この場合は `/bin/sh` を、サポートされているシェルのいずれかへのシンボリックリンクにする必要があります。  
Bashを使用してください。  
Ubuntu 14.04 LTS システムでは、次のコマンドを実行することで実現できます。  

```bash
sudo dpkg-reconfigure -plow dash
```

その後、`"Configuring dash"` のポップアップダイアログで `"No"` を選択してください。  
以下のコマンドを実行して、`/bin/sh` が `"bash"` を指していることを確認できます。  

```bash
$ ls -l /bin/sh
...... /bin/sh -> bash
```
