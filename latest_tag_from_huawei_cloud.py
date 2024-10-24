import os
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkswr.v2 import SwrClient, ListRepositoryTagsRequest
from huaweicloudsdkswr.v2.region.swr_region import SwrRegion

ak = os.getenv('AK')
sk = os.getenv('SK') 

credentials = BasicCredentials(ak, sk)
client = SwrClient.new_builder() \
    .with_credentials(credentials) \
    .with_region(SwrRegion.value_of('region')) \
    .build()

try:
    namespace = os.getenv('namespace', 'namespace')
    repository = os.getenv('repository', 'repository')

    request = ListRepositoryTagsRequest(namespace=namespace, repository=repository)
    response = client.list_repository_tags(request)
    print(f'Response body: {response.body}')

    # Yanıtı doğru şekilde işleyelim
    if hasattr(response, 'body') and isinstance(response.body, list):
        tags = [item.tag for item in response.body if hasattr(item, 'tag')]  
        print(f'Fetched tags: {tags}')
        if tags:
            latest_tag = max(tags, key=int)  
            print(f'Latest tag: {latest_tag}')
            next_tag = str(int(latest_tag) + 1)  
            print(f'Next tag (dockerImageTag): {next_tag}')
            print(f"##vso[task.setvariable variable=dockerImageTag]{next_tag}") 
        else:
            next_tag = '1'
            print("No tags found.Starting with the 1")
    else:
        print("Response does not have a 'body' attribute or it is not a list.")

except Exception as e:
    print(f'Error fetching tags: {str(e)}')
