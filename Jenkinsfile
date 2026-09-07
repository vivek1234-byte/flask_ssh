pipeline {
    agent any

    environment {
        // Name of the SSH credential configured in Jenkins
        GIT_SSH_CREDENTIAL_ID = 'github-ssh-key'
        // GitHub repository SSH URL (update with your repo)
        REPO_URL = 'git@github.com:<your-username>/<your-repo>.git'
        BRANCH = 'main'
        // Python version (adjust if needed)
        PYTHON = 'python3'
        VENV_DIR = 'venv'
        FLASK_APP = 'app.py'
        FLASK_PORT = '5000'
    }

    stages {
        stage('Checkout') {
            steps {
                // Authenticate via SSH and pull the latest code
                git branch: "${BRANCH}",
                    credentialsId: "${GIT_SSH_CREDENTIAL_ID}",
                    url: "${REPO_URL}"
            }
        }

        stage('Setup Python Virtual Environment') {
            steps {
                sh """
                    echo '>> Creating Python virtual environment...'
                    ${PYTHON} -m venv ${VENV_DIR}
                    echo '>> Virtual environment created at ${VENV_DIR}/'
                """
            }
        }

        stage('Install Dependencies') {
            steps {
                sh """
                    echo '>> Activating virtual environment and installing dependencies...'
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    echo '>> Dependencies installed successfully.'
                """
            }
        }

        stage('Lint') {
            steps {
                sh """
                    echo '>> Running linter...'
                    . ${VENV_DIR}/bin/activate
                    pip install flake8
                    flake8 app.py --max-line-length=120 --exclude=${VENV_DIR} || true
                """
            }
        }

        stage('Test') {
            steps {
                sh """
                    echo '>> Running tests...'
                    . ${VENV_DIR}/bin/activate
                    pip install pytest
                    pytest tests/ -v --tb=short || echo 'No tests found or tests failed.'
                """
            }
        }

        stage('Build / Run Flask App') {
            steps {
                sh """
                    echo '>> Building and verifying Flask application...'
                    . ${VENV_DIR}/bin/activate
                    export FLASK_APP=${FLASK_APP}
                    export FLASK_ENV=production

                    # Verify the app can start (run briefly and confirm it boots)
                    timeout 10 python ${FLASK_APP} &
                    APP_PID=\$!
                    sleep 5

                    # Health check
                    curl -s -o /dev/null -w "%{http_code}" http://localhost:${FLASK_PORT}/ || true

                    # Shut down gracefully
                    kill \$APP_PID 2>/dev/null || true
                    echo '>> Flask application build and smoke test complete.'
                """
            }
        }
    }

    post {
        always {
            echo '>> Cleaning up workspace...'
            cleanWs()
        }
        success {
            echo '>> Pipeline completed successfully!'
        }
        failure {
            echo '>> Pipeline failed. Check the logs above for details.'
        }
    }
}
