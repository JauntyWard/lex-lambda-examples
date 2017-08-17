

import json
import boto3

dynamodb_client = boto3.resource('dynamodb')
table = dynamodb_client.Table("players")


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


def handle_getPlayer(event):
    session_attributes = {}
    
    try:
        player_id = event["currentIntent"]["slots"]["player_id"]
        response = table.get_item(Key={"player_id": player_id })
        
        xp = response["Item"]["xp_per_min"] 
        if xp < 200:
            level = "novice"
        elif xp < 350:
            level = "intermediate"
        elif xp < 550:
            level = "advanced"
        elif xp < 750:
            xp = "world class"
        
        message = "{} is a {} player achieving {} XP per minute on average with an average kill-death ratio of {} to {}".format(player_id, level, response["Item"]["xp_per_min"], response["Item"]["avg_kills"], response["Item"]["avg_deaths"])
    except:
        message = "Unknown player"
        
    return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': message
        }
    )


def lambda_handler(event, context):
    return handle_getPlayer(event)
