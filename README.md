This is a lambda script which automates the deletion of old snaphsots.

Snapshots are created for backing up EBS volumes,but snaphots too incur costs,so we can delete snaphots which are old(say 6 months)


Make sure to add the SLACK_WEBHOOK_URL under Configuration->Environment variables in lambda
