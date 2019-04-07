### Database structure
Here are the list of tables:

staff_info
- staffID
- email
- fn
- ln

ice_account
- staffID: foreign key
- user_id: foreign key

users
- user_id
- username
- password

### How to create tables 
Check [how_to_change_db.md](how_to_change_db.md).

```bash
python manage.py dbshell
# then type in sqlite3 db commands: 
# e.g. .table
# e.g. CREATE TABLE xxxxxxx
```

