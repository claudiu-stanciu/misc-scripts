import os
import uuid
from datetime import datetime

import boto3

client = boto3.client('dynamodb')

max_items = os.getenv("DYNAMODB_MAX_SPAM", 10)
table_name = os.getenv("DYNAMODB_TABLE_NAME", "rmp_trip_tst")
message_to_store = {
    "tenant_id": "niancat",
    "route_points": [
        {
            "time": "2020-10-20T19:00:00+00:00",
            "lat": 23.123456789,
            "lon": -64.123456789,
        }
    ],

}


def get_key():
    return str(uuid.uuid4())


def _prepare_item(entry):
    rps = entry['route_points']
    tenant_id = None
    if 'tenant_id' in entry:
        tenant_id = entry['tenant_id']
    tenant_attr = {'S': tenant_id}

    extracted = []
    for rp in rps:
        extracted.append({
            'M': {
                'time': {'S': str(rp['time'])},
                'lat': {'N': format(rp['lat'], f'.6f')},
                'lon': {'N': format(rp['lon'], f'.6f')},
            }
        })

    expression_attribute_values = {
        ':empty_list': {'L': []},
        ':route_points': {'L': extracted},
    }

    update_expression = "SET "
    if tenant_attr.get('S') is not None:
        update_expression += "tenant_id = :tenant_id, "
        expression_attribute_values[':tenant_id'] = tenant_attr
    update_expression += "route_points = list_append(if_not_exists(route_points, :empty_list), :route_points)"
    return update_expression, expression_attribute_values


def write():
    count = 0
    run_check = True
    while run_check:
        run_check = count < max_items if max_items > 0 else True
        update_expression, expression_attribute_values = _prepare_item(message_to_store)
        start_time = datetime.now()
        response = client.update_item(
            TableName=table_name,
            Key={
                'id': {
                    'S': get_key()
                }
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="NONE"
        )
        end_time = datetime.now()
        if max_items > 0:
            count += 1
        process_time = (end_time - start_time)
        print(f"update time: {str(process_time)}")


if __name__ == "__main__":
    print("started")
    write()
    print("finished")
