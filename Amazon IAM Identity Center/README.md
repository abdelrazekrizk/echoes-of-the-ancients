## Identity and Access Management (IAM) in "Echoes of the Ancients"

IAM (Identity and Access Management) is fundamental to securing your AWS resources. <p>In "Echoes of the Ancients," we use IAM to control who (or what) has access to the various AWS services the game uses (Lambda, DynamoDB, Bedrock, S3, Polly). <p>There are two main approaches to managing access: IAM Roles and AWS IAM Identity Center (formerly AWS SSO).

**1. IAM Roles (Used for Lambda):**

IAM roles are used to grant permissions to AWS services, like Lambda, without needing to manage long-term access keys.

**Creating an IAM Role for Lambda:**

1.  **Navigate to IAM:** Go to the IAM console in the AWS Management Console.
2.  **Create Role:** Click "Roles" in the left navigation pane, then "Create role."
3.  **Trusted entity type:** Select "AWS service."
4.  **Choose a use case:** Select "Lambda."
5.  **Next:** Click "Next."
6.  **Add permissions:** Search for and attach the necessary AWS managed policies. For "Echoes of the Ancients," you'll need policies that grant appropriate access to the services your Lambda function uses. It's best practice to follow the principle of least privilege and use custom policies or more restrictive managed policies whenever possible. Here are some examples of managed policies you might need:
    *   `AmazonDynamoDBFullAccess` (or more restrictive policies like    *   `AmazonDynamoDBReadOnlyAccess` or custom policies)
    *   `AmazonBedrockFullAccess` (or more restrictive custom policies)
    *   `AmazonS3ReadOnlyAccess` (or more restrictive custom policies)
    *   `AmazonPollyReadOnlyAccess` (or more restrictive custom policies)
    *   `AWSLambdaBasicExecutionRole` (This is essential for Lambda to execute and write logs)
7.  **Next:** Click "Next."
8.  **Role name:** Provide a descriptive name for your role (e.g., `LambdaGameAccessRole`).
9.  **Create role:** Click "Create role."

**Attaching the IAM Role to Lambda:**

1.  **Go to your Lambda function:** In the Lambda console, navigate to your function.
2.  **Configuration -> Permissions:** Go to the "Configuration" tab and select "Permissions."
3.  **Edit:** Click "Edit."
4.  **Execution role:** Select "Use an existing role" and choose the role you created (e.g., `LambdaGameAccessRole`).
5.  **Save:** Click "Save."

**2. AWS IAM Identity Center (Formerly AWS SSO) (Used for Local Development):**

IAM Identity Center simplifies managing access to AWS accounts and applications for users. It's particularly helpful for local development when you want to avoid managing long-term access keys in your `.env` file.

**Setting up AWS IAM Identity Center:**

1.  **Enable IAM Identity Center:** In the AWS Management Console, search for "IAM Identity Center" and enable it if it's not already.
2.  **Configure Users and Groups (Optional):** You can create users and groups in IAM Identity Center to manage access at a more granular level.
3.  **Assign Users/Groups to AWS Accounts:** Assign the necessary permissions to users or groups for accessing your AWS account(s). This is done through permission sets.
4.  **AWS CLI Configuration:** After setting up IAM Identity Center, configure the AWS CLI. The easiest way is to use the `aws configure sso` command:

    ```bash
    aws configure sso
    ```

    Follow the prompts. This will open a browser window for you to authenticate with your organization's identity provider. Once authenticated, the CLI will store your SSO credentials locally.

**Difference between accessing services with IAM Role and AWS IAM Identity Center**

**IAM Role:**

*   Used by AWS services (like Lambda) to access other AWS services.
*   No long-term credentials are stored within the service itself.
*   Best practice for granting permissions to AWS resources.

**AWS IAM Identity Center:**

*   Used by users (like developers) to access AWS accounts and resources.
*   Provides centralized management of user access.
*   Uses short-lived credentials, enhancing security.

**.env file differences:**
Create a `.env` file in the project root and add your AWS credentials:
*    **AWS IAM Identity Center:**
*    Using AWS IAM Identity Center (Recommended for Local Development)
       ```markdown
        AWS_PROFILE=   # Your SSO profile name configured with `aws configure sso`
        region=        # `Your AWS region e.g., us-east-1`
       ```
**Using Session in your code:**

```python
import os
import boto3
import json
from dotenv import load_dotenv
import playsound
import tempfile  # For creating temporary files

load_dotenv()

# Get the profile name from environment or use a default
profile_name = os.getenv("AWS_PROFILE")

# Create a session using the profile
session = boto3.Session(profile_name=profile_name)

# Create clients using the session
bedrock = session.client(service_name="bedrock-runtime", region_name=os.getenv("region"))
dynamodb = session.resource('dynamodb', region_name=os.getenv("region"))
table = dynamodb.Table('player_data')
lex = session.client('lex-runtime', region_name=os.getenv("region"))
polly = session.client('polly', region_name=os.getenv("region"))
s3 = session.client('s3', region_name=os.getenv("region"))
BUCKET_NAME = "echoes-of-the-ancients-assets-<your-aws-account-id>" # Replace with your bucket name
```
**Using a Session in `game.py`:**

The `game.py` code leverages a session object to interact with AWS services. This session uses the profile name retrieved from the environment variable `AWS_PROFILE`. This profile name should be associated with your IAM Identity Center configuration.

*    **AWS Identity and Access Management:**
-    Using Access Keys (Less Secure, Avoid if Possible)

        ```markdown
        AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY
        AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY
        AWS_DEFAULT_REGION=YOUR_AWS_REGION
        ```
```python
import os
import boto3
import json
from dotenv import load_dotenv
import playsound
import tempfile  # For creating temporary files

load_dotenv()

bedrock = boto3.client(service_name="bedrock-runtime", region_name=os.getenv("AWS_DEFAULT_REGION"), aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))
dynamodb = boto3.resource('dynamodb', region_name=os.getenv("AWS_DEFAULT_REGION"), aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))
table = dynamodb.Table('player_data')
lex = boto3.client('lex-runtime', region_name=os.getenv("AWS_DEFAULT_REGION"), aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))
polly = boto3.client('polly', region_name=os.getenv("AWS_DEFAULT_REGION"), aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))
s3 = boto3.client('s3', region_name=os.getenv("AWS_DEFAULT_REGION"), aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))
BUCKET_NAME = "echoes-of-the-ancients-assets-<your-aws-account-id>" # Replace with your bucket name
```
**Key takeaway:**
*    For your Lambda function, use an IAM role.
*    For local development, use AWS IAM Identity Center.
*    Avoid storing long-term access keys directly in your .env file whenever possible.
> This significantly improves the security of your AWS environment.
