## Amazon S3 in "Echoes of the Ancients"

Amazon S3 (Simple Storage Service) is used in "Echoes of the Ancients" to store static assets, such as lore text files. This provides a scalable and cost-effective way to manage and deliver these assets to the game.

**Key Functions:**
*   **Static Asset Storage:** S3 stores files that don't change frequently, such as:
    *   Lore text files containing background information about the game world.
    *   Potentially images (e.g., icons for items or locations) or other multimedia assets in the future.
*   **Scalability and Durability:** S3 provides highly scalable and durable storage, ensuring that game assets are readily available and protected against data loss.
*   **Cost-Effectiveness:** S3 offers various storage classes to optimize costs based on access frequency. For infrequently accessed lore files, a lower-cost storage class could be used.
*   **Integration with Lambda:** The Lambda function interacts with S3 to retrieve the required assets during gameplay.

**Creating an S3 Bucket and Uploading Assets:**

1.  **Bucket Creation:**
    *   Navigate to the Amazon S3 console in the AWS Management Console.
    *   Click "Create bucket."
    *   **Bucket name:** Choose a globally unique name (e.g., `echoes-of-the-ancients-assets-<your-aws-account-id>`). Bucket names must be globally unique across all AWS accounts.
    *   **Region:** Select the same AWS Region where your other services (Lambda, Lex, DynamoDB) are located. This minimizes latency and data transfer costs.
    *   **Object Ownership:** Choose "ACLs enabled".
    *   **Block Public Access settings for this bucket:** Uncheck "Block *all* public access." Then check "Block public access to buckets and objects granted through new access control lists (ACLs)" and "Block public access to buckets and objects granted through any access control lists (ACLs)". This is the most secure option. We will grant access through IAM roles.
    *   Leave other settings as default and click "Create bucket."

2.  **Creating Folders (Optional but Recommended):**
    *   Within your newly created bucket, create folders to organize your assets. For example:
        *   `lore`: For text files containing background information.
        *   `images`: For image files.
        *   `sounds`: For sound effects (if used).

3.  **Uploading Assets:**
    *   Upload your files to the appropriate folders in your S3 bucket. You can do this through the AWS Management Console, the AWS CLI, or the AWS SDKs.
    *   Ensure that file names are descriptive and follow a consistent naming convention (e.g., `ancient_scroll_lore.txt`, `key_icon.png`).

        *   `sounds`: For sound effects (if used).

3.  **Uploading Assets:**
    *   Upload your files to the appropriate folders in your S3 bucket. You can do this through the AWS Management Console, the AWS CLI, or the AWS SDKs.
    *   Ensure that file names are descriptive and follow a consistent naming convention (e.g., `ancient_scroll_lore.txt`, `key_icon.png`).

**Accessing S3 from Lambda:**

*   **IAM Role:** The Lambda function needs an IAM role with permissions to read objects from the S3 bucket. The `AmazonS3ReadOnlyAccess` managed policy (or a more restrictive custom policy) is attached to the Lambda function's execution role.
*   **Boto3 Code:** The Lambda function uses the Boto3 library to interact with S3:

```python
import boto3

s3 = boto3.client('s3')
BUCKET_NAME = "your-bucket-name"

def get_lore(lore_file):
    try:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=f"lore/{lore_file}")
        lore = obj['Body'].read().decode('utf-8')
        return lore
    except Exception as e:
        print(f"Error retrieving lore from S3: {e}")
        return "Lore not found."
```
**Workflow Summary:**
1.    Game assets (e.g., lore text files) are stored in an S3 bucket.
2.    When the game needs to access an asset (e.g., when the player uses the read command), the Lambda function calls the S3 API using Boto3.
3.    S3 returns the requested asset to the Lambda function.
4.    The Lambda function processes the asset (e.g., decodes the text) and sends it back to the game client.

**Benefits of Using S3:**
*    **Scalable and Durable Storage:** Ensures assets are always available.
*    **Cost-Effective:** Pay-as-you-go pricing based on storage used and data transfer.
*    **Easy Integration with Lambda:** Seamless integration with other AWS services.
*    **Centralized Asset Management:** Provides a central repository for all game assets.
