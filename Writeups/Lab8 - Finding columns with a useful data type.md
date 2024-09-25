After we determined the number of required columns, we can probe each column to test whether it can hold string data. We can submit a series of **_UNION SELECT_** payloads that place a string value into each column in turn. For example, if the query returns four columns, you would submit:

>' UNION SELECT 'a',NULL,NULL,NULL--<br>
' UNION SELECT NULL,'a',NULL,NULL--<br>
' UNION SELECT NULL,NULL,'a',NULL--<br>
' UNION SELECT NULL,NULL,NULL,'a'--

**<h2>Problem:</h2>**
This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response, so we can use a UNION attack to retrieve data from other tables. <br>

The lab will provide a random value that we need to make appear within the query results. To solve the lab, we perform a SQL injection UNION attack that ``returns an additional row containing the value provided``. This technique helps us determine which columns are compatible with string data.

<h4>Goal: We need to retrieve the data "7kKMxP".

**<h2>Solution:</h2>**
- Check for the number of columns present using  ``' order by ``  attack; which gives us the required columns to be 3.
- Check for the data type of the columns using union attack; ``' union select 'a',NULL,NULL--``. 
- We get the response for the ``'union select NULL,'a',NULL--`` query. Now replace the data by required data type to add a row.
![alt text](/images/lab8dataentry.png)