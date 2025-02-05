Let me break down the key issues and best practices:

1. Jupyter Installation
Problem: Jupyter wasn't explicitly installed in the project environment
Solution: 
- Always include Jupyter in project dependencies
- Use `poetry add jupyter` 
- Verify installation with `poetry run jupyter kernelspec list`

2. TensorFlow Installation
Challenges:
- Dependency conflicts
- Version compatibility
- Virtual environment isolation

Best Practices:
- Explicitly specify TensorFlow version in pyproject.toml
- Use `poetry install` to resolve dependencies
- If direct pip install is needed, use `poetry run pip install`
- Ensure Python version matches TensorFlow requirements (3.11 in your case)

3. Kernel Management
Steps to Prevent Future Issues:
- Always install IPython kernel in project venv
- Use a consistent naming convention
- Command: `poetry run python -m ipykernel install --user --name=project-name`

Recommended Workflow:
1. Define all dependencies in pyproject.toml
2. Use `poetry install` for consistent environment setup
3. Activate environment with `poetry shell`
4. Install Jupyter kernel
5. Verify imports and installations

Key Takeaway: Poetry helps manage these complexities, but you still need to be intentional about environment setup and dependency management.

Would you like me to elaborate on any of these points?