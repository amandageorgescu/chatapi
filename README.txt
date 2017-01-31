Welcome to my simple chat API.

In order to chat, follow the steps below:

1. You must first register yourself as a user. You can do that with the following command, inserting your own name and email address:

curl -H "Content-type: application/json" -X POST https://protected-beyond-84593.herokuapp.com/users -d '{"name":"Amanda Georgescu","email":"georgescu.amanda@gmail.com"}'

2. Now, use the following command to see who else you can chat with:

curl -H "Content-type: application/json" -X GET https://protected-beyond-84593.herokuapp.com/users

This will return the names and email addresses of everyone who has registered to use the chat API.  

3. Now, in order to chat with someone, use the below command, inserting your email address as "sender", the email address of the person you want to chat with as "receiver", and the message you want to send as "text":

curl -H "Content-type: application/json" -X POST https://protected-beyond-84593.herokuapp.com/messages -d '{"sender":"georgescu.amanda@gmail.com","receiver":"bobsmith@gmail.com","text":"Hey Bob"}'

In order for this to work, the receiver must also have registered to chat via Step 1.  If all went well, your own message will be returned and theoretically printed out when the front end is implemented.

4. Now, wait a few moments and use the below command to query for a reply, inserting the email address of the person you are chatting with as "sender", and your email address as "receiver":

curl -H "Content-type: application/json" -X GET https://protected-beyond-84593.herokuapp.com/messages -d '{"sender":"bobsmith@gmail.com","receiver":"georgescu.amanda@gmail.com"}'

If the person you are chatting with has replied already, their message will be returned.  If they haven't replied yet, nothing will be returned.  You can always try the above command again after waiting a few more moments, or set up a process that runs in a loop to query for replies.  

5. In order to keep chatting, just continue using the commands described in Steps 3 and 4. 

Enjoy!





 
