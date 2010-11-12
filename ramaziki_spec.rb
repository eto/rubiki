# -*- coding: utf-8 -*-
require 'ramaziki'

describe Ramaziki, "について" do
  DataDir = "data_spec"

  before(:all) do
    Dir.chdir(DataDir) {
      Dir['*'].each { |f| File.unlink f }
    }
    @wiki = Ramaziki.new(DataDir)
    @wiki[".hidden"] = "hidden page"
    @wiki["最初"] = "1st page"
    @wiki["二番目"] = "2nd page"
    @wiki["3番目"] = "3rd page"
    @wiki["さいご"] = "final page"
    @wiki["alpha"] = "A"
    @wiki["Bravo"] = "B"
    @wiki["charlie"] = "C"
  end

  it "list は文字コード順のページ一覧を返す。" do
    @wiki.list.should == %w(3番目 Bravo alpha charlie さいご 二番目 最初)
  end

  it "list :sort_by => :modify_time は、更新が新しい順のページ一覧を返す。" do
    pending "mtime が秒単位なのでこのテストはうまくいかない。"
    @wiki.list(:sort_by => :modify_time).should == %w(最初 二番目 3番目 さいご alpha Bravo charlie)
  end

  it "[] でページ内容を得る" do
    @wiki[".hidden"].should == "hidden page"
    @wiki["最初"].should == "1st page"
    @wiki["二番目"].should == "2nd page"
    @wiki["3番目"].should == "3rd page"
    @wiki["さいご"].should == "final page"
  end

  it "存在しないページを[]で取ると nil を返す。" do
    @wiki["存在しない"].should be_nil
  end

  it "[]= でページ内容を変更する。" do
    @wiki["3番目"] = "modified"
    @wiki["3番目"].should == "modified"
  end

  it "存在しないページへの []= は、新しいページを作る。" do
    @wiki["新ページ"] = "nothing"
    @wiki["新ページ"].should == "nothing"
    @wiki.delete "新ページ"
  end

  it "delete でページを削除する。" do
    @wiki.delete "3番目"
    @wiki["3番目"].should == nil
  end
end
