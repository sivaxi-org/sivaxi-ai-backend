pipeline {
    agent any

    stages {
        stage('Build and Push Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'ghcr-credentials',
                        usernameVariable: 'GHCR_USERNAME',
                        passwordVariable: 'GHCR_PASSWORD'
                    )
                ]) {
                    sh '''
                        set -eu
                        set +x

                        IMAGE="ghcr.io/sivaxi-org/sivaxi-ai"
                        VERSION="${BUILD_NUMBER}"

                        printf '%s' "$GHCR_PASSWORD" |
                            docker login ghcr.io \
                                --username "$GHCR_USERNAME" \
                                --password-stdin

                        docker build \
                            -f Dockerfile \
                            -t "$IMAGE:$VERSION" \
                            -t "$IMAGE:latest" \
                            .

                        docker push "$IMAGE:$VERSION"
                        docker push "$IMAGE:latest"

                        docker logout ghcr.io
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Docker image built and pushed with version and latest tags.'
        }

        failure {
            echo 'Docker image build or push failed.'
        }

        always {
            echo 'Pipeline execution completed.'
        }
    }
}