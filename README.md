# flask_ssh

A Flask application with Jenkins CI/CD pipeline using SSH authentication for GitHub.

## Project Structure

```
flask_ssh/
├── Jenkinsfile          # Jenkins pipeline configuration
├── app.py               # Flask application
├── requirements.txt     # Python dependencies
├── tests/
│   └── test_app.py      # Unit tests
└── README.md
```

## Flask Application

A simple Flask app with two endpoints:

| Endpoint  | Description            |
|-----------|------------------------|
| `GET /`   | Health-check / status  |
| `GET /hello` | Greeting message    |

## Jenkins Pipeline Setup

### Prerequisites

1. **Jenkins** installed with the following plugins:
   - Git plugin
   - SSH Credentials plugin
   - Pipeline plugin
2. **Python 3** installed on the Jenkins agent
3. **SSH key pair** for GitHub authentication

### SSH Key Configuration

1. **Generate an SSH key pair** on the Jenkins server:
   ```bash
   ssh-keygen -t ed25519 -C "jenkins@your-server" -f ~/.ssh/jenkins_github_key
   ```

2. **Add the public key to GitHub**:
   - Go to your repository → **Settings** → **Deploy keys** → **Add deploy key**
   - Paste the contents of `~/.ssh/jenkins_github_key.pub`
   - Enable **Allow write access** if needed

3. **Add the private key to Jenkins**:
   - Go to **Jenkins** → **Manage Jenkins** → **Manage Credentials**
   - Add a new credential of type **SSH Username with private key**
   - Set the **ID** to `github-ssh-key` (must match the Jenkinsfile)
   - Enter the private key from `~/.ssh/jenkins_github_key`

4. **Test connectivity** from the Jenkins server:
   ```bash
   ssh -T git@github.com
   ```

### Running the Pipeline

1. Create a new **Pipeline** job in Jenkins
2. Under **Pipeline**, select **Pipeline script from SCM**
3. Set SCM to **Git**, enter the SSH URL: `git@github.com:vivek1234-byte/flask_ssh.git`
4. Set credentials to the SSH key configured above
5. Set the branch to `main`
6. The `Jenkinsfile` in the repository root will be used automatically

### Pipeline Stages

| Stage | Description |
|-------|-------------|
| **Checkout** | Authenticates via SSH and pulls latest code |
| **Setup Python Virtual Environment** | Creates a Python venv |
| **Install Dependencies** | Installs packages from `requirements.txt` |
| **Lint** | Runs `flake8` for code quality checks |
| **Test** | Runs `pytest` unit tests |
| **Build / Run Flask App** | Starts the app, performs a smoke test, then shuts down |

## Local Development

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Run tests
pip install pytest
pytest tests/ -v
```
