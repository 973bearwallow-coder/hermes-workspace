# Shared Shopping List

Use `shopping_list.py` as the single authoritative shopping-list store for Atlas, Amy, voice, phone, desktop, and the Food and Home specialist.

Commands:
- Add: `python shopping_list.py --source amy add "milk" --location "Falls Church" --store Aldi`
- Read by store: `python shopping_list.py list --store Costco`
- Read by property: `python shopping_list.py list --location Farm`
- Mark purchased: `python shopping_list.py --source voice purchased ID`
- Remove: `python shopping_list.py --source atlas remove ID`
- Amazon candidate preview: `python shopping_list.py amazon-preview ID`

Rules:
- Preserve the two property locations: `Falls Church` and `Farm`.
- Group lists by retailer/category. Lowe's and Home Depot default to `Hardware`; retain another named retailer when Tom specifies it.
- Infer a store only when unambiguous; otherwise ask Tom.
- Every mutation returns the exact normalized item, property, store, quantity, status, and stable ID for spoken read-back.
- Duplicate adds are idempotent and auditable.
- Amy may relay routine add, read, remove, and purchased updates using `--source amy`; relaying grants no authority for sensitive actions.
- Amazon is a list and preview destination only here. Adding to a live cart requires an authenticated browser, exact product preview, fresh confirmation, and cart read-back. Never check out, use Buy Now, create a subscription, or spend money.
