import tempfile, unittest
from pathlib import Path
import shopping_list as s
class ShoppingTests(unittest.TestCase):
 def setUp(self): self.t=tempfile.TemporaryDirectory(); self.db=s.connect(Path(self.t.name)/'x.db')
 def tearDown(self): self.db.close(); self.t.cleanup()
 def test_locations_stores_and_views(self):
  s.add(self.db,'deck screws','farm',source='amy')
  s.add(self.db,'milk','Falls Church','Aldi',source='voice')
  self.assertEqual(s.list_items(self.db,store='Hardware')['items'][0]['location'],'Farm')
  self.assertEqual(s.list_items(self.db,location='Falls Church')['items'][0]['store'],'Aldi')
 def test_duplicate_is_idempotent(self):
  a=s.add(self.db,'milk','home','Aldi'); b=s.add(self.db,'MILK','Falls Church','aldi')
  self.assertEqual(b['action'],'deduplicated'); self.assertEqual(s.list_items(self.db)['count'],1)
 def test_ambiguous_store_clarifies(self):
  with self.assertRaisesRegex(ValueError,'store_required_or_ambiguous'): s.add(self.db,'milk','farm')
 def test_purchased_removes_from_needed_view(self):
  x=s.add(self.db,'trash bags','home'); s.mark(self.db,x['id'],'amy')
  self.assertEqual(s.list_items(self.db)['count'],0); self.assertEqual(s.list_items(self.db,status='purchased')['count'],1)
 def test_amazon_requires_preview_and_never_orders(self):
  x=s.add(self.db,'USB-C cable','home','Amazon'); p=s.amazon_preview(self.db,x['id'])
  self.assertEqual(p['action'],'cart_preview_required'); self.assertTrue(any('spending blocked' in x for x in p['constraints']))
 def test_invalid_location_rejected(self):
  with self.assertRaisesRegex(ValueError,'location_must'): s.add(self.db,'milk','unknown','Aldi')
if __name__=='__main__': unittest.main()
