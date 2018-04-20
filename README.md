#TTNC's Python API Client

A simple Python library that handles connection, authentication, requests and parsing of responses to and from TTNC's API. For more information on TTNC's API visit [TTNC's main API page](https://help.ttnc.co.uk/docs/api)

A list of function requests available via the API can be found in the [documentation](https://help.ttnc.co.uk/docs/api)

## Requirements

- An account with [TTNC](http://www.ttnc.co.uk).
- A VKey (Application) created via [myTTNC](https://www.myttnc.co.uk).

## Usage

The API can be constructed as follows;
```python
	api = TTNCApi('<username>', '<password>', '<vkey>')
```

Requests can then be 'spooled' in the object until the *makerequests* method is called. While not required, each request should be given an ID which can be used to retrieve the response later on;

```python
	request = api.newrequest('NoveroNumbers', 'ListNumbers', 'Request1')
```

### Basic Usage
```python
	api = TTNCApi('<username>', '<password>', '<vkey>')
	request = api.newrequest('NoveroNumbers', 'ListNumbers', 'Request1')
	api.makerequest()
	p request.getresponse()
```

In order to send data in a request - the *setdata* method can  be called on the *Request* object;

```python
	api = TTNCApi('<username>', '<password>', '<vkey>')
	request = api.newrequest('NoveroNumbers', 'SetDestination', 'Request1')
	request.setdata('Number', '02031511000')
	request.setdata('Destination', '07512312312')
	api.makerequest()
	p request.getresponse()
```

### Parsing Responses

The response can be retrieved from the request object after *makerequests* has been called.
```python
	p request.getresponse()
```

Alternatively, you can retrieve the response from the response from the API based on the ID passed to the request;

```python
	p api.getresponsefromid('Request1')
```

### Advanced Usage

The client deals automatically with the *Auth* requests for you, however, in order to perform some more advanced actions on the API (such as ordering numbers via the *AddToBasket* request) you may need to save the session state between script executions. In order to do this it's necessary to access the *SessionRequest* Response and retrieve the returned SessionId. This can then be stored in your own code for use on the next request;

```python
	api = TTNCApi('<username>', '<password>', '<vkey>')
    request = api.newrequest('Order', 'AddToBasket', 'Request1Id');
    request.setdata('number', '02031231231');
    request.setdata('type', 'number');
    api.makerequest()
    response = api.getresponsefromid('SessionRequest');

	# Store response['SessionId'] in your own code.
```

Then on repeat requests, to retrieve the same basket you can construct the object without authentication and then parse in the SessionId to use on Requests;

```python
    api = TTNCApi();
    api.usesession(sessionId) # From the previous request, stored in your own code.
    request = api.newrequest('Order', 'ViewBasket', 'Request1Id');
    api.makerequest()
    response = request.getresponse()
    # Response now contains a representation of your basket.
```

## Getting Support

If you have any questions or support queries then first please read the [Developers Site](https://help.ttnc.co.uk/docs/api) and then email support@ttnc.co.uk.
