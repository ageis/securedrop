#!/usr/bin/python

import sqlite3 as lite
import sys
import os
import subprocess

con = None

sourceint = sys.argv[1]
docint = sys.argv[2]

bookmarks = [     ['http://' + docint, 'Document Interface', 'toolbar', ['SecureDrop']],
r          ['http://' + sourceint, 'Source Interface', 'toolbar', ['SecureDrop']]]
tag = 'SecureDrop'

sub = subprocess.call(['killall','firefox'])
placesdb = "/home/amnesia/.mozilla/firefox/bookmarks/places.sqlite"

print "Bookmarks to be inserted in %s" % placesdb

try:
    con = lite.connect(placesdb)
  
    cur = con.cursor()    

    cur.execute("SELECT rowid FROM moz_bookmarks_roots where root_name = 'toolbar'")
    toolbarRoot = int(cur.fetchone()[0])

    cur.execute("SELECT rowid FROM moz_bookmarks_roots where root_name = 'places'")
    placesRoot = int(cur.fetchone()[0])

    cur.execute("SELECT rowid FROM moz_bookmarks_roots where root_name = 'menu'")
    menuRoot = cur.fetchone()

    cur.execute("SELECT rowid FROM moz_bookmarks_roots where root_name = 'tags'")
    tagsRoot = int(cur.fetchone()[0])

    cur.execute('INSERT INTO "main"."moz_bookmarks" ("type","parent","title") VALUES (?1,?2,?3)',(2,tagsRoot,tag))
    
    con.commit()
    
    for bookmark in bookmarks:
      cur.execute('INSERT INTO moz_places ("url","title") VALUES (?1,?2)',(bookmark[0],bookmark[1]))
      con.commit()
      place = cur.lastrowid
      cur.execute('INSERT INTO "main"."moz_bookmarks" ("type","fk","parent","title","position") VALUES (?1,?2,?3,?4,3)',(1,place, menuRoot if bookmark[2]=='menu' else toolbarRoot,bookmark[1]))
      con.commit()
      
      for tag in bookmark[3]:
	cur.execute('SELECT id FROM moz_bookmarks where title="' + tag + '"')
	tagid = int(cur.fetchone()[0])#
	cur.execute('INSERT INTO "main"."moz_bookmarks" ("type","fk","parent","title","position") VALUES (?1,?2,?3,?4,?5)',(1,place, tagid,bookmark[1],0))
      
      print(bookmark[1] + " added")
    
    con.commit()
       
except lite.Error, e:
    
    print "Error %s:" % e.args[0]
    sys.exit(1)
    
finally:
    
    if con:
        con.close()
