# CodeChef Virtual Contest(CVC)
\- a way to replay past codechef contests.

This Web app lets you play Codechef Contests as virtual contests.  
It feels just like a real contest with real contestants competing alongside with the participant who participate a virtual contest.

WebApp is hosted at - [http://149.129.139.179](http://149.129.139.179)   

#### Technologies used - 
- Flask
- MongoDB
- Jinja2 Template 

#### How to Install -  

- `pip3 install -r requirements.txt`
- You also need to put your `client_id`, `client_secret`, `redirect_uri` in `app_data` collection in db.
- The Database server is hosted on Alibabacloud, thus requires URI, and password, which you need to set up in file `db_conn.py`, set `DB_PASS` environment variable which has passkey to your DB.
- Deploy using Gunicorn using `gunicorn app:app -b 127.0.0.1:5000`

---
Developed during [Codechef API Hackathon](https://www.codechef.com/CAH1801) by [Hasan Alirajpurwala](https://github.com/hasan356) and [Vishvanath Dutt Sharma](https://github.com/vishvanath45)
