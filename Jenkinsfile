
pipeline {
    agent any

    stages {
        stage('Build Docker Images') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Push Docker Images') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'ghcr-credentials',
                        usernameVariable: 'GHCR_USERNAME',
                        passwordVariable: 'GHCR_TOKEN'
                    )
                ]) {
                    sh '''
                        printf '%s' "$GHCR_TOKEN" |
                            docker login ghcr.io \
                                --username "$GHCR_USERNAME" \
                                --password-stdin

                        docker compose push
                    '''
                }
            }
        }
    }
}
