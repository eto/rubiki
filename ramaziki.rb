# -*- coding: utf-8 -*-
require 'uri'

class Ramaziki
#  DataDir = 'data'
  Version = "0.1"

  def initialize(data_dir)
    @data_dir = data_dir
    Dir.mkdir @data_dir unless File.exist? @data_dir
  end

  def list(mode = {})
    pages = Dir.chdir(@data_dir) { Dir["*"] }
    case mode[:sort_by]
    when :modify_time
      pages = pages.sort_by { |filename| File.mtime(File.join(@data_dir, filename)) }
      pages.map { |filename| to_pagename(filename) }
    else # 名前順
      pages.map! { |filename| to_pagename(filename)}
      pages.sort
    end
  end

  def get(page)
    filename = to_filename(page)
    if File.exist? filename
      File.read filename
    end
  end

  alias :[] :get

  def write(page, data = "")
    open(to_filename(page), "wb") { |out|
      out.flock(File::LOCK_EX)
      out.write data
      out.flock(File::LOCK_UN)
    }
  end

  alias :[]= :write

  def delete(page)
    File.unlink to_filename(page)
  end

  def hidden?(page)
    (page =~ /^\./) == true
  end

  def exists?(page)
    File.exists? to_filename(page)
  end
  
  def editable?(page)
    page != nil  
  end

private
  def to_filename(page)
    File.join @data_dir, URI.encode(page)
  end

  def to_pagename(filename)
    URI.unescape filename
  end

end
