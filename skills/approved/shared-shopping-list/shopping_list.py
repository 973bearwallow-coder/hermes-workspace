#!/usr/bin/env python3
"""Shared, auditable shopping lists for Atlas, Amy, voice, phone, and desktop."""
from __future__ import annotations
import argparse, json, re, sqlite3
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_DB = Path.home()/'.local/share/atlas-home/shopping.db'
LOCATIONS={'falls church':'Falls Church','falls':'Falls Church','home':'Falls Church','farm':'Farm','west augusta':'Farm'}
STORES={'aldi':'Aldi','costco':'Costco','amazon':'Amazon','lowes':'Hardware','lowe’s':'Hardware',"lowe's":'Hardware','home depot':'Hardware','hardware':'Hardware','grocery':'Grocery'}
HARDWARE_WORDS={'screw','screws','nail','nails','lumber','drill','paint','bolt','bolts','washer','washers','tool','tools','caulk'}
COSTCO_WORDS={'paper towels','toilet paper','trash bags','detergent','batteries'}

def now(): return datetime.now(timezone.utc).isoformat()
def connect(path=DEFAULT_DB):
 path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
 db=sqlite3.connect(path); db.row_factory=sqlite3.Row
 db.executescript('''PRAGMA journal_mode=WAL; CREATE TABLE IF NOT EXISTS items(
 id INTEGER PRIMARY KEY, item TEXT NOT NULL COLLATE NOCASE, location TEXT NOT NULL,
 store TEXT NOT NULL, quantity TEXT NOT NULL DEFAULT '', status TEXT NOT NULL DEFAULT 'needed',
 source TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
 UNIQUE(item,location,store,status)); CREATE TABLE IF NOT EXISTS audit(
 id INTEGER PRIMARY KEY, at TEXT NOT NULL, source TEXT NOT NULL, action TEXT NOT NULL, detail TEXT NOT NULL);''')
 return db

def norm_location(value):
 if not value: raise ValueError('location_required')
 key=value.strip().lower()
 if key not in LOCATIONS: raise ValueError('location_must_be_falls_church_or_farm')
 return LOCATIONS[key]
def infer_store(item, store=None):
 if store:
  key=store.strip().lower()
  if key not in STORES: return store.strip().title()
  return STORES[key]
 low=item.lower()
 if any(re.search(rf'\b{re.escape(w)}\b',low) for w in HARDWARE_WORDS): return 'Hardware'
 if low in COSTCO_WORDS: return 'Costco'
 raise ValueError('store_required_or_ambiguous')
def add(db,item,location,store=None,quantity='',source='atlas'):
 item=' '.join(item.split()).strip();
 if not item: raise ValueError('item_required')
 location=norm_location(location); store=infer_store(item,store); ts=now()
 row=db.execute("SELECT id,quantity FROM items WHERE item=? AND location=? AND store=? AND status='needed'",(item,location,store)).fetchone()
 if row:
  if quantity: db.execute('UPDATE items SET quantity=?,updated_at=? WHERE id=?',(quantity,ts,row['id']))
  action='deduplicated'
  ident=row['id']
 else:
  cur=db.execute('INSERT INTO items(item,location,store,quantity,status,source,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?)',(item,location,store,quantity,'needed',source,ts,ts)); ident=cur.lastrowid; action='added'
 detail={'id':ident,'item':item,'location':location,'store':store,'quantity':quantity,'status':'needed'}
 db.execute('INSERT INTO audit(at,source,action,detail) VALUES(?,?,?,?)',(ts,source,action,json.dumps(detail,sort_keys=True))); db.commit()
 return {'ok':True,'action':action,**detail}
def list_items(db,location=None,store=None,status='needed'):
 clauses=['status=?']; args=[status]
 if location: clauses.append('location=?'); args.append(norm_location(location))
 if store: clauses.append('store=?'); args.append(infer_store('',store))
 rows=db.execute('SELECT id,item,location,store,quantity,status,source,updated_at FROM items WHERE '+' AND '.join(clauses)+' ORDER BY store,location,item',args).fetchall()
 return {'ok':True,'count':len(rows),'items':[dict(r) for r in rows]}
def mark(db,ident,source='atlas'):
 row=db.execute("SELECT * FROM items WHERE id=? AND status='needed'",(ident,)).fetchone()
 if not row: raise ValueError('needed_item_not_found')
 ts=now(); db.execute("UPDATE items SET status='purchased',updated_at=? WHERE id=?",(ts,ident)); db.execute('INSERT INTO audit(at,source,action,detail) VALUES(?,?,?,?)',(ts,source,'purchased',json.dumps({'id':ident,'item':row['item']}))); db.commit()
 return {'ok':True,'action':'purchased','id':ident,'item':row['item']}
def remove(db,ident,source='atlas'):
 row=db.execute("SELECT * FROM items WHERE id=? AND status='needed'",(ident,)).fetchone()
 if not row: raise ValueError('needed_item_not_found')
 ts=now(); db.execute("UPDATE items SET status='removed',updated_at=? WHERE id=?",(ts,ident)); db.execute('INSERT INTO audit(at,source,action,detail) VALUES(?,?,?,?)',(ts,source,'removed',json.dumps({'id':ident,'item':row['item']}))); db.commit()
 return {'ok':True,'action':'removed','id':ident,'item':row['item']}
def amazon_preview(db,ident):
 row=db.execute("SELECT * FROM items WHERE id=? AND status='needed' AND store='Amazon'",(ident,)).fetchone()
 if not row: raise ValueError('needed_amazon_item_not_found')
 return {'ok':True,'action':'cart_preview_required','item':row['item'],'quantity':row['quantity'],'location':row['location'],'constraints':['verify exact product, size, seller, price, delivery, subscription status','fresh Add it to the cart confirmation required','checkout, Buy Now, subscriptions, and spending blocked']}
def main(argv=None):
 p=argparse.ArgumentParser(); p.add_argument('--db',default=str(DEFAULT_DB)); p.add_argument('--source',default='atlas',choices=['atlas','amy','voice','phone','desktop','test'])
 s=p.add_subparsers(dest='cmd',required=True)
 a=s.add_parser('add'); a.add_argument('item'); a.add_argument('--location',required=True); a.add_argument('--store'); a.add_argument('--quantity',default='')
 l=s.add_parser('list'); l.add_argument('--location'); l.add_argument('--store'); l.add_argument('--status',default='needed')
 for name in ('purchased','remove','amazon-preview'): q=s.add_parser(name); q.add_argument('id',type=int)
 ns=p.parse_args(argv); db=connect(ns.db)
 try:
  if ns.cmd=='add': out=add(db,ns.item,ns.location,ns.store,ns.quantity,ns.source)
  elif ns.cmd=='list': out=list_items(db,ns.location,ns.store,ns.status)
  elif ns.cmd=='purchased': out=mark(db,ns.id,ns.source)
  elif ns.cmd=='remove': out=remove(db,ns.id,ns.source)
  else: out=amazon_preview(db,ns.id)
 except ValueError as e: out={'ok':False,'error':str(e)}
 print(json.dumps(out,ensure_ascii=False,sort_keys=True)); return 0 if out['ok'] else 2
if __name__=='__main__': raise SystemExit(main())
