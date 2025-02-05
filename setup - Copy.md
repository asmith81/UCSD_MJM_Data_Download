Python ML Project Setup Procedure

1. Create and enter directory
mkdir D:\UCSD_CodeAlong_26_4_GAN_MNIST
cd D:\UCSD_CodeAlong_26_4_GAN_MNIST

2. Create virtual environment with Python 3.11
& "C:\Users\alden\AppData\Local\Programs\Python\Python311\python.exe" -m venv .venv

Verify Python version
& .venv\Scripts\python.exe --version

3. Create .gitignore and initialize git
@"
.venv/
pycache/
*.pyc
.env
.dvc/
.dvc/tmp
.dvc/cache
/data
/models
*.ipynb_checkpoints/
poetry.lock
*.dvc
gdrive_oath.json
"@ | Out-File -FilePath .gitignore

git init

4. Activate and setup poetry
venv\Scripts\Activate.ps1
pip install poetry
$env:POETRY_VIRTUALENVS_IN_PROJECT = "true"
poetry init --name "UCSD_MJM_Capstone" --python ">=3.11,<3.12" --no-interaction

4.1 Install jupyter poetry run pip install jupyter

5. Establish data version control
poetry add dvc
dvc init

6. Add required packages
poetry add "numpy>=1.26.0,<2.1.0" (best is 1.26.4)
poetry add pandas
poetry add scipy
poetry add scikit-learn
poetry add tensorflow (2.15.0)
  tensorflow-io-gcs-filesystem (0.31.0)
poetry add matplotlib
poetry add seaborn

# For Google-related imports
poetry add google-auth-oauthlib
poetry add google-api-python-client
poetry add google-auth-httplib2

# For PDF handling (PyMuPDF)
poetry add PyMuPDF

# For image processing
poetry add Pillow

poetry add ipykernel
python -m ipykernel install --user --name=UCSD_MJM_Capstone

7. Install dependencies
poetry install --no-root

8. Create file structure
mkdir data
mkdir models
mkdir notebooks