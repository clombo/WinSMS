# WinSMS Module
*********
#### Description

The module allows you to interact with the [WinSMS XML API](https://www.winsms.co.za/). The API allows you to do the following:

* Send SMS's in bulk at a specific time (scheduled) or immediately
* Delete scheduled SMS's
* Get replies
* Get status of SMS messages.

Note: You will need an account with [WinSMS](https://www.winsms.co.za/registration/) to send SMS's through the gateway. Sign up and add credits to start.
      The same login details you use to sign in is used by the module to communicate with the API.

Please feel free to use this code as is on your applications or adjust it according to your needs.

#### Disclaimer

This module or application was not developed by or for WinSMS, and was purely done for fun and educational purposes by myself.


#### Todo
* Schedule not working
* Add help clauses to module
* finish documentation
***

#### Usage


##### Clone and setup module

You can clone the module via github or use git:

```shell
git clone https://github.com/clombo/WinSMS.git
```

Once clone make sure to install the necessary dependencies from the requirements.txt file:

```shell
pip install -r requirements.txt
```

The module has the following imports:

* send
* delete
* replies
* batchStatus

To import the above use the following:

```python
from WinSMS.sms import send,delete,replies,batchStatus
```


##### Send SMS's

The send import is used to send SMS's once imported, create a "send" object passing your username
and password for your WinSMS profile:

```python
  send = send('username','password')
```

Once the object is created you can start adding messages using the Messages method of the send class:

```python
send.Message('Some message you want to send')
```

After adding a message you can start adding numbers using the AddNumbers method, you can add multiple numbers separated by commas. Note that a message must be present otherwise you cannot add numbers.

NOTE: Please make sure to add the numbers with the country code(without + simbol) otherwise WinSMS will automatically use the South-African code (27)

```python
send.AddNumbers('some number 1','some number 2')
```

You can add more messages by simply calling the Message method again. It will automatically add your previous message with its numbers to the XML that will sent to the WinSMS gateway.

Once you've added all the messages with the selected numbers you can POST the data to the gateway by calling the SendSMS method. The method will also automatically add the last message with the selected numbers to the XML object.

```python
  sent = send.sendSMS()
```

Once sent you will receive a JSON response indicating if it was successful or not. make sure to store the data if you wish to use it later on with the other classes available.

##### Delete Scheduled Message

Create a delete object with your WinSMS username and password

```python
  Delete = delete('username','password')
```

After creating the delete object you can simply call the delete method passing the message id provided by WinSMS and the CLI. The CLI is normally the number you sent the message to. The CLI is optional and you can completely omit it from your call if you wish.

It will return a JSON object as the response.

```python
  resp = Delete.delete('messageid','cli')
```

##### Check status of sent messages

Same rules apply to get the status of a batch as the delete class above.

```python
Status = batchStatus('username','password')
```

```python
resp = Status.GetStatus('messageid','cli')
```
##### Get replies

Create a replies object passing your WinSMS login details

```python
Replies = replies('username','password')
```

Once created you can pull the replies using the get method:

```python
resp = Replies.get()
```
