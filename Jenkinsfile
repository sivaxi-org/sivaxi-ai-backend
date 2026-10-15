
pipeline {
    agent any

    environment {
        GHCR_CREDENTIALS = credentials('ghcr-credentials')
    }

    stages {
        stage('Build Docker Images') {
            steps {
                sh 'docker-compose build'
            }
        }

        stage('Push Docker Images') {
            steps {
                sh '''
                    printf '%s' "$GHCR_CREDENTIALS_PSW" |
                      docker login ghcr.io \
                        -u "$GHCR_CREDENTIALS_USR" \
                        --password-stdin

                    docker-compose push
                '''
            }
        }
    }
}
