import boto3

def move_files(source_bucket, destination_bucket):
    # Account aliases for better readability
    accA = 'SOURCE ACCOUNT NAME'
    accB = 'DESTINATION ACCOUNT NAME'

    # Create sessions for Account A and Account B
    accountA_session = boto3.Session(profile_name='SOURCE ACCOUNT NAME')
    accountB_session = boto3.Session(profile_name='DESTINATION ACCOUNT NAME')

    # Create S3 clients for Account A and Account B
    s3_accountA = accountA_session.client('s3')
    s3_accountB = accountB_session.client('s3')

    # List objects in the source bucket
    response = s3_accountA.list_objects_v2(Bucket=source_bucket)

    # Check if the source bucket is empty
    if 'Contents' not in response:
        print(f"Source bucket: {source_bucket} is empty. No files to move.")
        return
    
    objects = response['Contents']

    # Iterate over objects in the source bucket
    for obj in objects:
        # Get the key (object path) of the current object
        source_key = obj['Key']

        # Copy the object from Account A to Account B
        s3_accountB.copy_object(
            CopySource={'Bucket': source_bucket, 'Key': source_key},
            Bucket=destination_bucket,
            Key=source_key
        )

        # Print a success message for each file moved
        print(f"Moved file {source_key} from {accA} to {accB}")

# Usage: move_files('source-bucket', 'destination-bucket')
move_files('SOURCE BUCKET NAME', 'DESTINATION BUCKET NAME')

