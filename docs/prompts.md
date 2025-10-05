Prompt 1:Your primary challenge is to build a small, functional application. Core Technical Requirements: Authentication System: Implement a basic username/password login. CRUD Operations: Select a domain object (e.g., Task, Product) and implement Create, Read, Update, and Delete endpoints. The object must include a Text field, an Enum (dropdown selection), a Boolean field, and one calculated field (derived from ≥2 inputs). You must provide a simple UI using React, another framework, or minimal HTML. Listing & Data Management: Implement pagination (5-10 items per page) and at least one useful filter. Development Approach: Build from scratch or use established frameworks (like Next.js or Flask). You must avoid low/no-code tools that auto-generate full applications. Code Quality: Apply OOP concepts (encapsulation, modularity) and write clean, organized code.

Context: The first prompt giving overview of the objective.
Model: Set out to begin the project. Made directories, virtual environment, installed dependencies. First worked on backend and app.py file. The database selected was SQLLite and Flask was used to design the backend. Then moved on to design the froned, the html elements, .js and .css files. All in all the skeletal structure was completed.

Prompt 2: Create a register page as well for new users and ensure new users are prompted to register first.
Context: The login page showed no message to prompt the user to register themselves
Model: Started to work on making register function in app.py and made required changes in frontend files as well to prompt the user.


Prompt 3: Use JWT token for increased security.
Context: After some iterations the backend and frontend had the bare bones, and so moved on to security
Model: Made the required changes in the backend to enhance security, using jwt tokens.

Prompt 4: Do not store passwords in plaintext, use hashes.
Context: An overview of the code showed passwords being stored in plaintest and checked using that.
Model: Used werkzeug.security module to store passwords as hashes and compare the hashes itself. This increased authentication and security.

Prompt 5: Add Filters based on urgency and overdue and complexity of task.
Context: The model after several itnerations had not yet implemented the filters correctly.
Model: Went on to work on this. Took some iterations to get the dynamics right but in the end solved the issue. Hence did not push it towards searching and sorting.

Prompt 6: Push the contents into a github repo.
Context: After some time, the initial development was complete and finally the code was to be pushed into git repo
Model: Added the requirements.txt file using pip freeze, and files like .gitignore. Designed the readme file and made the structure ready to push. However the git id it referred to did not seem correct so push was done manually.


Prompt 7:  Deploy the project using render.
Context: after several iterations the project was deemed ready for deployment.
Model: Gave steps to make account to render and vercel and made the required changes in the files like removing hardcorded variables and localhosts ids. This took a long time, and several errors were faced. The database was changed from SqlLite to Postgress. This ensured Consistency in the database. The username was used as primary id. In the end, backend and database were deployed using render and vercel was used for frontend deployment. 

Prompt 8: Perfrom tests: Testing Coverage : Include comprehensive test cases for: Validation Testing (Invalid/missing fields, incorrect enum values). Boundary Testing (Pagination limits, calculated field edge cases). Security Testing (Unauthorized access attempts). Integration Testing (End-to-end CRUD operations)
Context: Once the deployment was successful and changes made, testing was performed.
Model : created a test_app.py file to test the app on above paramters. Conducted tests using python unit-test. Initally 3 tests were failed but in the end, the problems were corrected and final correct code was pushed into GitHub and redeployed.
