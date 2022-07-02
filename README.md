## Kronolog Backend
The backend for 'Kronolog': the web app for collecting voice data for BUET CSE Fest 2022 Deep Learning Sprint Competition. See more: buetcsefest2022.com/dlsprint

## Resources
- Heroku Dyno
- Heroku Hobby PostgreSQL (10,000 rows limit)

## Important Notes
#### Clearing Database Entries
In order to clear `django_admin_log` entries from database, open the python shell from cloud provider.
```py
python manage.py shell
```
Then enter the following lines of code:
```py
from django.contrib.admin.models import LogEntry
LogEntry.objects.all().delete()
```
Exit the shell and terminal. It'll be gone.
