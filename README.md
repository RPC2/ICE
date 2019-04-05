## Preparation
```
python3 manage.py runserver
# do the following after making changes to models.py
python3 manage.py makemigrations
python3 manage.py migrate
```

## Running the website
Open this URL in a browser: http://127.0.0.1:8000/instructor/

Log in with this User account (normal instructor):
```
username: tester
password: testertester 
```

## Managing database
Open this URL in a browser:
http://127.0.0.1:8000/admin/


Log in with this Super User account:
```
Username: gucci
Password: gucci_gang
Email: gucci@hku.hk
```
(Superuser was created by python3 manage.py createsuperuser.)

## How Authentication works

### 以instructor为例：
- 每次进入[instructor page](http://127.0.0.1:8000/instructor/)，一定会要求login
- 输入login (user: `tester`, password: `testertester`)之后，只会显示属于你的courses，详见[views.py](views.py)的实现。
- 在database的实现是在下面的appendix里面，所以每个course里面，都同时记录了instructor的instructor_id和user_id，以user_id作为authentication的标准。

### 新user的建立：
- 目前是在site admin里面建立，会需要name，password，和group（分组是：instructor_group，learner_group）
- permission是按group来set的，比如learner_group不能add_modules

### Appendix: Database structure
User Table
- user id (primary key)
- details (name, address, phone --i.e. common to a user of the system whether student or teacher.)

Student Table
- user id (foreign key relationship to user table)
- any student specific details (enrolment date, homeroom, etc.)

Teacher Table
- a user id (foreign key relationship to user table)
- teacher specific stuff (seniority, salary, etc.)

Classes Table
- a class id (primary key).
- details of the class
