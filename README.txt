= Rubiki 0.2

by あさひみちはる <fusuian[at]gmail.com>
2010/11/1

== これは何？
Ruby プログラムの書ける Wiki エンジンです。
作成したページを開いて「Run」ボタンをクリックすると、サーバでソースがバイトコードにコンパイルされ、ブラウザ上で実行されます。

== 注意！
HotRuby から JavaScript の DOM を利用して、任意のタグを生成することができます。
Rubiki を動作させるドメインで別のサービスが動いていると、XSS脆弱性を突いた被害が発生する可能性があります。
充分ご注意ください。

== インストール
Ruby 1.9.0 で動きます。
ramaze と erubis が必要なので、gem でインストールしておいてください。

== サーバ起動
ターミナルから ruby index.cgi を実行してください。

== アクセス
ブラウザから、サーバのポート7000にアクセスしてください。
(例) http://localhost:7000
HotRubyのサンプルと同じものがいくつか入っているので、Runしてみましょう。

= 利用しているプログラム
== HotRuby について
小林 悠氏による、JavaScript で書かれた RubyVM です。
http://hotruby.yukoba.jp/
Rubiki では、この HotRuby に独自の修正を加えたものを利用しています。

== EditArea について
Christophe Dolivet 氏によるライブラリで、textarea を拡張してソースコードをハイライト表示します。
http://www.cdolivet.com/index.php?page=editArea

== printf.js について
Masanao Izumo 氏によるコードです。
http://www.onicos.com/staff/iz/amuse/javascript/expert/
Rubiki では、これを HotRuby に合わせて修正したものを利用しています。
