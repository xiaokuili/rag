import weaviate
import json 
auth_config = weaviate.AuthApiKey(api_key="XDq1EPNJNYJdbCnI2gdaSbnYmLWJ4ERWOEVF")

client = weaviate.Client(
  url="https://my-test-t111r3yd.weaviate.network",
  auth_client_secret=auth_config
)

nearVector = {
  "vector": [0.1, -0.15, 0.3 ]  # Replace with a compatible vector
}

result = (
  client.query
  .get("LangChain_agent_docs", "title")
  .with_additional("source")
  .with_near_vector(nearVector)
  .do()
)


print(result)