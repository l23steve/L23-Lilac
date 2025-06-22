NEVER remove functionality without first checking with the user.
NEVER write unit tests that depend on 3rd party services/databases. ALWAYS write mocks instead.
NEVER expose real credentials in code. ALWAYS use env variables.
NEVER use deprecated functions or libraries.
ALWAYS use the latest versions of libraries.
ALWAYS include relevant dependencies in the requirements.txt of the specific Tool or Service you're working on.
ALWAYS suggest highly valuable adjustments or features as new tasks.
ALWAYS retain backwards compatibility with API endpoints unless _explicitly_ stated otherwise by the user. Avoid breaking changes to API endpoints. Use schema extension instead of replacement.
ALWAYS use pytest for unit tests. Run the unit tests from the Service or Tool folder using `pytest`, not from the project root.
ALWAYS test both happy and unhappy paths.
ALWAYS ensure code and tests pass `ruff check`.
ALWAYS use FastAPI for internal or external API endpoints.