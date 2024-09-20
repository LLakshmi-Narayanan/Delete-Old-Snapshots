import boto3
import requests
import datetime
import os

ec2_client = boto3.client('ec2')
print(ec2_client)

slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']

def lambda_handler(event, context):

    snapshots = ec2_client.describe_snapshots(OwnerIds=['self'])['Snapshots']
    print(snapshots)
    now = datetime.datetime.now(datetime.timezone.utc)
    cutoff_date = now - datetime.timedelta(days=180)
    snapshots_to_delete = []
    snapshot_names=[]
    for snapshot in snapshots:
        snapshot_time = snapshot['StartTime']
        if snapshot_time < cutoff_date:
            snapshots_to_delete.append(snapshot['SnapshotId'])
            for tag in snapshot.get('Tags', []):
                if tag['Key'] == 'Name':
                    snapshot_names.append(tag.get('Value'))
    for i in range(0,len(snapshots_to_delete)):
        #ec2_client.delete_snapshot(SnapshotId=snapshots_to_delete[i])
        send_slack_notification(snapshot_names[i])
    
    return {
        'statusCode': 404,
        'body': f"Deleted {len(snapshots_to_delete)} snapshots."
    }

def send_slack_notification(snapshot_name):
    message = {
        'text': f'Snapshot {snapshot_name} has been deleted because it is older than six months.'
    }
    response = requests.post(slack_webhook_url, json=message)
    if response.status_code != 200:
        raise ValueError(
            f'Request to Slack returned an error {response.status_code}, the response is:\n{response.text}'
        )
