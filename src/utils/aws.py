import boto3
from botocore.exceptions import ClientError, BotoCoreError


class S3Access:
    """
    A class to handle assuming an IAM role and accessing objects in an S3 bucket.

    Attributes:
        role_arn (str): The ARN of the IAM role to assume.
        bucket_name (str): The name of the S3 bucket to access.
        session (boto3.Session): A boto3 session with credentials obtained by assuming the role.
    """

    def __init__(self, role_arn, bucket_name):
        """
        Initializes the S3Access object, assumes the specified IAM role, and stores the session.

        Parameters:
            role_arn (str): The ARN of the IAM role to assume.
            bucket_name (str): The name of the S3 bucket to access.
        """
        self.role_arn = role_arn
        self.bucket_name = bucket_name
        self.session = self.assume_role()

    def assume_role(self):
        """
        Assumes the specified IAM role using AWS STS and returns a boto3 session with the obtained credentials.

        Returns:
            boto3.Session: A session initialized with the temporary security credentials of the assumed role,
                           or None if the role cannot be assumed.
        """
        try:
            sts_client = boto3.client("sts")
            assumed_role = sts_client.assume_role(RoleArn=self.role_arn, RoleSessionName="AssumeRoleSession")
            credentials = assumed_role["Credentials"]

            return boto3.Session(
                aws_access_key_id=credentials["AccessKeyId"],
                aws_secret_access_key=credentials["SecretAccessKey"],
                aws_session_token=credentials["SessionToken"],
            )
        except (ClientError, BotoCoreError) as e:
            print(f"Failed to assume role: {e}")
            raise e

    def get_object(self, object_key):
        """
        Retrieves an object from the specified S3 bucket using the session with assumed role credentials.

        Parameters:
            object_key (str): The key of the object to retrieve from the S3 bucket.

        Returns:
            bytes: The content of the retrieved object, or None if the operation fails.
        """
        try:
            s3 = self.session.client("s3")
            response = s3.get_object(Bucket=self.bucket_name, Key=object_key)
            return response["Body"].read()
        except (ClientError, BotoCoreError) as e:
            print(f"Failed to get object '{object_key}' from bucket '{self.bucket_name}': {e}")
            raise e
