# CodeChef Virtual Contest(CVC)
\- a way to replay past codechef contests.

This Web app lets you play Codechef Contests as virtual contests.  
It feels just like a real contest with real contestants competing alongside with the participants who participate a virtual contest.

WebApp is hosted at - [~~http://149.129.145.244~~](http://149.129.145.244) (not anymore, since Codechef made their API private) 

Please refer to [Video link](https://drive.google.com/file/d/1gWXbUoU-yJK3NUkPO--LcB2_d_7aOZY1/view?usp=sharing) or [Slides](https://docs.google.com/presentation/d/1pY5egzHQp-wdqPZP5a9booA7QRfu0frSLaXEnb-2Qmk/edit?usp=sharing) for better understanding of project.


It will be very helpful for the preparation of short contests. Few of the features are :

- You can add friends and see their separate rank list during the live virtual contest.
- Several people can play the virtual contest together and see each other's ranking.
- All COOKOFF's starting from COOK01 to recent COOK98A/B are available to play as a virtual contest.
- You can compare yourself with other people while the virtual contest is in play.
- Video tutorial to Use WebApp : [Video link](https://drive.google.com/file/d/1gWXbUoU-yJK3NUkPO--LcB2_d_7aOZY1/view?usp=sharing) (Just a short 12 min video, you can watch at 1.5x :P)

Slides for a better understanding of App: [Slides](https://docs.google.com/presentation/d/1pY5egzHQp-wdqPZP5a9booA7QRfu0frSLaXEnb-2Qmk/edit?usp=sharing)(We both are very poor in making slides, we apologize beforehand _/\\\_)

Note: Judgement result takes a while to reflect in standings as Codechef restricts no. of API requests in a min.(6 calls/min), just refresh the page in a while.

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
