pipeline {
    agent any

    stages {

        stage('Install Dependencies') {
            steps {
                sh '''
                    echo "Python version:"
                    python3 --version

                    echo "Creating virtual environment..."
                    rm -rf venv
                    python3 -m venv venv

                    echo "Installing dependencies..."
                    ./venv/bin/pip install --upgrade pip
                    ./venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Build') {
            steps {
                sh '''
                    echo "Building Flask application..."
                    ./venv/bin/python3 -m py_compile app.py

                    echo "Build successful!"
                '''
            }
        }

        stage('Run Flask') {
            steps {
                sh '''
                    echo "Starting Flask..."

                    export JENKINS_NODE_COOKIE=dontKillMe

                    nohup ./venv/bin/python3 app.py > flask.log 2>&1 &

                    FLASK_PID=$!

                    echo "Flask PID: $FLASK_PID"

                    sleep 5

                    echo "===== FLASK LOG ====="
                    cat flask.log

                    echo "===== PROCESS ====="
                    ps -p $FLASK_PID -f || true

                    echo "===== PORT ====="
                    ss -lntp | grep 5000 || true

                    echo "===== CURL TEST ====="
                    curl -v http://127.0.0.1:5000 || true
                '''
            }
        }
    }

    post {
        success {
            echo 'Flask application started on port 5000'
        }

        failure {
            echo 'Pipeline failed!'
        }
    }
}