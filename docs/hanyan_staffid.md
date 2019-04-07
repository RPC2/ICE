### Database structure
Here are the list of tables:

staff_info [prior knowledge]
- staffID
- email
- firstname
- lastname

Example way to pass the staffID in: `url/base64encode?token=99`

users [created on the fly]
- user_id
- username
- password

ice_account [created on the fly]
- staffID: foreign key
- user_id: foreign key

### How to create tables 
Check [how_to_change_db.md](how_to_change_db.md).

```bash
python manage.py dbshell
# then type in sqlite3 db commands: 
# e.g. .table
# e.g. CREATE TABLE xxxxxxx
```

