import boto3
import hashlib
import base64
import json

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('shortened_urls')


def shorten_url(url):
    hash_object = hashlib.sha256(url.encode())
    hash_value = hash_object.digest()
    encoded_hash = base64.urlsafe_b64encode(hash_value).decode()
    url_hash = encoded_hash[:8]
    # Store the shortened URL in the database
    table.put_item(
        Item={
            'url_hash': url_hash,
            'url': url
        }
    )
    # Return the shortened URL to the client
    shortened_url =  'https://47yog43oux5eeyrmdc7bwfh4eu0ynryi.lambda-url.ap-south-1.on.aws/api/getUrl/?hash=' + url_hash
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
