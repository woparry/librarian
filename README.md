# README FIRST


Requires some flavour of Linux and Python.  
Windows user will have to figure out how it works themselves and edit 
the code to suit.

Also requires the python packages:
biblio
zbar
MySQLdb
copy
gtk
sqlite3
reportlab
qrencode - optional

Get the code with:
git clone git://github.com/EvansMike/librarian.git


Install with python setup.py install

I wanted to catalog all my books using their barcodes as input and track who
borrows my books.  That's all.  I looked online for a program that would
do just that and couldn't find any that supported barcode input.  The idea
of typing in book details didn't appeal, so wrote this.

This is a simple application to catalogue your library using the ISBN barcode
and the zbarcam application with an ordinary webcam.
The scan triggers a lookup on the database and the book details are downloaded
then commited to the local database.

It uses MySQL or sqlite.  The database config file is created if none exists.
Use database.sql, after creating the database,  to populate the database, like:
mysql -p books < database.sql
You have to create the database first using your favourite method/tool.
The database name (books in the example above) can be anything as long as the
config file matches.  If the config file contains a password so take care to 
make it secure from prying eyes.

Can also use sqlite.  Edit db_conf.cfg to use whatever database you like.
The sqlite file will be created it it doesn't already exist.  Sqlite is 
easier to set up but not so useful if you want to access the data from 
multiple computers.

See INSTALL for install instructions.

## QR Codes
Everytime you scan a book a qrcode can be generated. You may not want this behaviour.
BY default the behaviour is turned off in the config file.
It seemed like a good idea at the time but I admit to never have used the 
qrcodes for anything. :)


Older books without bar codes can be manually input via the Query/Edit book
interface.  It's a bit of a pain though if you have lots of books.


## DB NOTES:
To get a list of borrowed books from mysql:
SELECT o_date, title, author, borrowers.name
  FROM borrows, borrowers, books
  where borrows.borrower = borrowers.id
  and books.id = borrows.book
  and borrows.i_date IS NULL;

To insert a borrower in the mysql shell:
insert into borrowers(name) values ('Borrower Name');
It's just a text field, the id is auto incremented.
Obviously there should be a nice user friendly GUI for this. :)
Update: There is now.

The sqlite2 database file is createed from the books.schema.sql file with:
./mysql2sqlite --no-data  -p books | sqlite3 books_schema.db


### Update:  2012-04-12 
You can now scan DVDs and CDs provided you have a Amazon web
services account.  http://aws.amazon.com to sign up.  As far as I know, low
useage will attract no charge, likely to be most domestic users.
CD lookup uses Amazon to get CD data from the barcode, if it's not in
Amazon's database this will fail.  Not sure what other databases there are 
for CD case barcodes.  Perhaps an application to add CD's as they are played 
using freedb?

Setting user database password stuff is up to you for the moment.  
I will add a GUI. NOTE:  Passwords are stored as plain text in the config file.  
This is not good and some encryption method should (will) be used when 
the config GUI is written.  On first run a refault .db_config.cnf file is
writting in your home directory, note that this is a hidden dot-file.  
This must edited with the details of your database.

To create the tables you will need the books_schema.sql  file from the sources.
After creating the database run: mysql <-p> books < books_schema.sql to 
create the tables.  The -p is required if your DB is password protected.
Obviously you can call the DB anything you like, it doesn't have to be 
books, as long as the .db_config.cfg file contains matching details.

  To get who borrowed what and for how long:
  select title, name, DAtediff(i_date,o_date) as days 
      from borrows, borrowers, books 
      where borrows.borrower=borrowers.id 
      and books.id=borrows.book;
      



## Windows Users

Apologies to Windows users.  You may have to adapt the code to suit.  Please
send any relavent stuff back to me and I'll try to incorporate into the 
code.
      

