# Health

Types:

```python
from mechanix.types import HealthRetrieveResponse
```

Methods:

- <code title="get /health">client.health.<a href="./src/mechanix/resources/health.py">retrieve</a>() -> <a href="./src/mechanix/types/health_retrieve_response.py">object</a></code>

# Root

Types:

```python
from mechanix.types import RootRetrieveResponse
```

Methods:

- <code title="get /">client.root.<a href="./src/mechanix/resources/root.py">retrieve</a>() -> str</code>

# Users

Types:

```python
from mechanix.types import UserModel
```

Methods:

- <code title="post /api/v1/users/view">client.users.<a href="./src/mechanix/resources/users.py">view</a>(\*\*<a href="src/mechanix/types/user_view_params.py">params</a>) -> <a href="./src/mechanix/types/user_model.py">UserModel</a></code>

# Tools

Types:

```python
from mechanix.types import ToolSearchResponse, ToolSummarizeResponse
```

Methods:

- <code title="post /api/v1/tools/search">client.tools.<a href="./src/mechanix/resources/tools.py">search</a>(\*\*<a href="src/mechanix/types/tool_search_params.py">params</a>) -> <a href="./src/mechanix/types/tool_search_response.py">ToolSearchResponse</a></code>
- <code title="post /api/v1/tools/summarize">client.tools.<a href="./src/mechanix/resources/tools.py">summarize</a>(\*\*<a href="src/mechanix/types/tool_summarize_params.py">params</a>) -> <a href="./src/mechanix/types/tool_summarize_response.py">object</a></code>
