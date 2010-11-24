# -*- coding: utf-8 -*-
require 'rubygems'
require 'ramaze'
require 'erb'
require 'json'

if RUBY_VERSION == "1.9.0"
alias :require_relative :require
end

require_relative 'ramaziki'
require_relative 'parser'
require_relative 'ramaziki_helper'

class RamazikiController < Ramaze::Controller
  map '/'
  engine :Erubis

  helper :paginate
  helper :ramazikihelper
  
  Ramaze::Log.start
  Ramaze::Log.debug "start"
  Ramaze::Log.level = Innate::LogHub::DEBUG
  Ramaze::Log.debug Ramaze::Log.level
#  trait :paginate => {
#    :limit => 3,
#    :var => 'page',
#  }

  def home
  end

  def news
    @pages = wiki.list(:sort_by => :modify_time).reverse! 
    @pager = paginate(@pages)
  end

  def index(mode = "")
    @pages = wiki.list
    #Ramaze::Log.debug pages.join(', ') 
    @pager = paginate(@pages)
  end

  def create(page)
  end

  def edit(page = nil)
    @content = page
    page ||= request['page']
    unless page
      flash[:error] = "ページが指定されていません。"
      redirect r(:home)
    end
    @page = url_decode page.to_s
    @text = wiki[@page]
    @title = "#{page} の編集"
  end

  def modify(page_uri)
    #page ||= request['page']
    page = URI.decode page_uri.to_s
    
    if request['text']
      text = request['text'].to_s
      if text.empty?
        wiki.delete page
        flash[:notice] = "#{page} を削除しました。"
        redirect r(:home)
      elsif wiki[page] == text
        flash[:notice] = "内容が変更されていません。"
        redirect r(:edit, page_uri)
      else
        wiki[page] = text
        flash[:notice] = "更新しました。"
        redirect r(:edit, page_uri)
      end
    else
        flash[:notice] = "テキストがありません。"
        redirect r(:show, page_uri)
    end
  end
  
  OutputCompileOption = {
  :peephole_optimization    =>true,
  :inline_const_cache       =>false,
  :specialized_instruction  =>false,
  :operands_unification     =>false,
  :instructions_unification =>false,
  :stack_caching            =>false,
  }
  
  def compile_ruby
    src ||= request['src']
    src = html_unescape src
    parse src
    begin
      if RUBY_VERSION == "1.9.0"
        VM::InstructionSequence.compile(src, "src", 1, OutputCompileOption).to_a.to_json
      else
        RubyVM::InstructionSequence.compile(src, "src", nil, 1, OutputCompileOption).to_a.to_json
      end
    rescue SyntaxError
      [$!.to_s].to_json
      #$!.backtrace.to_json
    end
  end
  
  def parse(src)
    src.gsub!(/require (["'])(.*)\1/) {
      lib = $2
      @loaded_features ||= {}
      unless @loaded_features.include? lib
        wiki[lib]
        @loaded_features[lib] = true
      end
    }
    src.gsub!(/attr_reader (:(\w+),*\s*)*/) {
      getter $2
    }
    src.gsub!(/attr_writer (:(\w+),*\s*)*/) { 
      setter $2
    }
    src.gsub!(/attr_accessor (:(\w+),*\s*)*/) { 
      getter($2) + setter($2)
    }
    src
  end

  def getter(s)
      %Q(  def #{s}; @#{s}; end\n) 
  end
  
  def setter(s)
      %Q(  def #{s}=(v); @#{s} = v; end\n) 
  end
  
end

DataDir = "data"

def wiki
  @wiki ||= Ramaziki.new(DataDir)
end

def parser
  @parser ||= Parser.new
end

Ramaze.start
