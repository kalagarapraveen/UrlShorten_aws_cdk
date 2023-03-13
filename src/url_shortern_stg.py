import boto3
import hashlib
import json

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('shortened_urls')


def shorten_url(url):
    url_parts = urllib.parse.urlsplit(url)
    base_url = url_parts.scheme + '://' + url_parts.netloc + url_parts.path
    query_string = url_parts.query
    # Generate a unique hash for the URL
    url_hash = hashlib.sha256(base_url.encode()).hexdigest()[:8]
    # Store the shortened URL in the database
    table.put_item(
        Item={
            'url_hash': url_hash,
            'url': url
        }
    )
    # Return the shortened URL to the client
    shortened_url = base_url + '/' + url_hash
    if query_string:
        shortened_url += '?' + query_string
    return {
        'statusCode': 200,
        'body': shortened_url
    }


def redirect_url(url_hash):
    # Fetch the original URL from the database using the hash
    response = table.get_item(Key={'url_hash': url_hash})
    if 'Item' in response:
        original_url = response['Item']['url']
        return {
            'statusCode': 200,
            'body': json.dumps({'url': original_url})
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'URL not found'})
        }


def main(event, context):
    print(event)
    path = event['rawPath']
    
    if path=='/':
        return {
            'statusCode': 200,
            'body': json.dumps({'Messgae': 'Api working successfully'})
        }


    if path == '/api/shortenUrl':
        # Handle POST request to shorten URL
        request_body = json.loads(event['body'])
        url = request_body['url']
        return shorten_url(url)

        
    elif path == '/api/getUrl':
        # Handle GET request to get original URL from shortened URL
         url_hash = event['queryStringParameters']['hash']
         return redirect_url(url_hash)
        
    else:
        # Return error for unsupported API
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'API not found'})
        }
