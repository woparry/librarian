#!/bin/env python
'''
  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
  MA 02110-1301, USA.
'''
'''
Usage:
printf "$(python barscan.py)"
Requires:
zbar-pygtk
biblio.webquery
'''
# TODO we don't always get a title and author from a single lookup
# need to test this and try alternate lookup.
# TODO Needs a live internet connection!  No good for portable apps. without wireless.
#   Need a db update app.
#   Change author name parsing.  Also parse to authors table for future normalisation.
#     Biblio lookup returns a list of authors.

import zbar
import webbrowser
from biblio.webquery.xisbn import XisbnQuery
import biblio.webquery
import qrencode
import MySQLdb
import sys
import ConfigParser
import logging
import load_config
import gettext
import book
import datetime

_ = gettext.gettext

logger = logging.getLogger("barscan")
logging.basicConfig(format='%(module)s: %(levelname)s:%(message)s: LINE %(lineno)d', level=logging.DEBUG)


try:
	import pygtk
	pygtk.require("2.0")
except:
	pass
try:
	import gtk
except:
	print_("GTK Not Availible")
	sys.exit(1)

config = load_config.load_config()
db_user = config.db_user
db_pass = config.db_pass
db_base = config.db_base
db_host = config.db_host



################## BEGIN scanner class #################################
class scanner:
  ''' Scanner class. Scans books, queries isbndb and adds book to database, or CSV'''
  def __init__(self):
    self.abook = book.book()
    qr_img = ""
    #vid_dev = "/dev/video0" # Need to scan for this and make it work in windows?
    builder = gtk.Builder()
    builder.add_from_file("ui/gui.glade")
    self.window = builder.get_object("window1")
    builder.connect_signals(self)
    self.text_view = builder.get_object("textview1")
    self.qr_img = builder.get_object("image1")
    self.cur = None
    try:
      self.db = MySQLdb.connect(host=db_host, db=db_base,  passwd = db_pass);
    except:
      print (_("No database connection.  Check config file"))
      self.db = False
    if self.db:
      self.cur = self.db.cursor()




  def on_button_scan_clicked(self, widget):
    buff = self.text_view.get_buffer()
    buff.set_text(_("To begin press scan."))
    self.text_view.set_buffer(buff)
    try: device = '/dev/video0'
    except:device = '/dev/video1'
    # create a Processor
    proc = zbar.Processor()
    # configure the Processor
    proc.parse_config('enable')
    buff = self.text_view.get_buffer()
    # enable the preview window
    proc.init(device)
    proc.visible = True
    # read at least one barcode (or until window closed)
    proc.process_one()
    # hide the preview window
    proc.visible = False
    logging.info(proc.results)
    try:
      for symbol in proc.results:
        bar = symbol.data
        logging.info(bar)
        self.abook.webquery(bar)
        logging.info(len(self.abook.print_book()))
        if len(self.abook.print_book()) <= 3:
          buff.set_text (_("No data returned, retry?"))
          self.text_view.set_buffer(buff)
        logging.info(self.abook.print_book())
        buff.set_text(self.abook.print_book())
    except:
      #logging.info(self.abook.print_book())
      buff.set_text (_("Dodgy scan, retry?"))
      self.text_view.set_buffer(buff)
      return
    # DONE Check if exists and increment book count if so.

    try:
		self.cur.execute("SELECT COUNT(*) as count FROM books WHERE isbn = %s;",str(self.abook.isbn))
		count = self.cur.fetchone()[0]
		if count > 0:
		  buff.insert_at_cursor (_("\n\nYou already have " + str(count) + " in the database!\n"))
		self.text_view.set_buffer(buff)
    except:
      pass
    del buff


  def make_qr_code():
    '''
    Although kinda fun to produce QR codes it's seems pretty pointless for this app, so
    I'm commenting it out.
    # Do the QR thang
    qr = qrencode.encode('ISBN:'+ bar + ' TITLE:' + str(nn.title) + ' AUTHORS:' + str(nn.authors))
    # Rescale using the size and add a 1 px border
    size = qr[1]
    qr = qrencode.encode_scaled('ISBN:'+ bar + ' TITLE:' + str(nn.title) + ' AUTHORS:' + str(nn.authors), (size*3)+2)
    img = qr[2]
    img.save('../ISBN:' + bar + '.png', 'png')
    self.qr_img.set_from_file('../ISBN:' + bar + '.png')
    '''


  def on_button_remove_clicked(self, widget):
    # Remove a scanned book from the database.  Why?
    print "You removed this book."
    buff = self.text_view.get_buffer()
    try:
      self.cur.execute("DELETE FROM books WHERE isbn = %s;", str(self.abook.isbn))
      buff.insert_at_cursor (_( "\n\nYou removed this book."))
      self.text_view.set_buffer(buff)
    except:
      buff.insert_at_cursor (_( "\n\nCould not remove book!"))
      self.text_view.set_buffer(buff)

  def on_button_add_clicked(self, widget):

    # DONE Check if exists and increment copy counter if so.
    # Arguably I could have used "ON DUPLICATE KEY", using the isbn as the key,
    # here but it may happen that several books will have empty isbn values
    # for instance, books printed before ISBN was invented.
    # result = self.cur.execute ("SELECT count(isbn) as count FROM books WHERE isbn = %s;",
    #      str(self.abook.isbn))
    #if self.cur.fetchone()[0] == 0:
      # Insert the author into the authors table
    a_name = str(self.abook.authors)
    self.cur.execute("INSERT IGNORE INTO authors(name) values(%s);", [a_name])
    self.cur.execute("SELECT * FROM authors WHERE name=%s;",[a_name])
    result = self.cur.fetchall()
    author_id = result[0][0]
    self.cur.execute("INSERT INTO books\
    (title, author, isbn,abstract, year, publisher, city, copies, author_id, add_date)\
    VALUES(%s, %s, %s,%s,%s,%s,%s,%s,%s,%s);", \
  (str(self.abook.title), str(self.abook.authors), str(self.abook.id),
        str(self.abook.abstract),str(self.abook.year),
        str(self.abook.publisher),str(self.abook.city),1,author_id,
        datetime.date.today()))
    '''
    else:
      self.cur.execute("UPDATE books set copies = copies+1 WHERE isbn = %s;",str(self.abook.id))
    '''
    buff = self.text_view.get_buffer()
    buff.insert_at_cursor(_( "\n\nYou added this book."))
    self.text_view.set_buffer(buff)
    print "You added this book."


  def append_text(self, text):
    pass

  def get_book_data(self):
    #self.scanner
    pass


  def gtk_main_quit(self, widget):
    # Quit when we destroy the GUI only if main application, else don't quit
    if __name__ == "__main__":
      gtk.main_quit()
      quit(0)
    else:
      self.window.hide()
      del self
    pass
################## END scanner class ###################################



# we start here.
if __name__ == "__main__":
	app = scanner()
	gtk.main()

