pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'ghcr-credentials',
                        usernameVariable: 'GHCR_USERNAME',
                        passwordVariable: 'GHCR_PASSWORD'
                    )
                ]) {
                    sh '''
                        set +x

                        printf '%s' "$GHCR_PASSWORD" |
                            docker login ghcr.io \
                                --username "$GHCR_USERNAME" \
                                --password-stdin

                        docker compose push

                        docker logout ghcr.io
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Docker images built and pushed successfully...'
        }

        failure {
            echo 'Docker image build or push failed.'
        }

        always {
            echo 'Pipeline execution completed.'
        }
    }
}