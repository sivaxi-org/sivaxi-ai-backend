
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

                        echo "=== Logging in to GHCR ==="
                        printf '%s' "$GHCR_PASSWORD" |
                            docker login ghcr.io \
                                --username "$GHCR_USERNAME" \
                                --password-stdin

                        echo "=== Building Docker image ==="
                        docker build \
                            -f Dockerfile \
                            -t "$IMAGE:$VERSION" \
                            -t "$IMAGE:latest" \
                            .

                        echo "=== Pushing version: $VERSION ==="
                        docker push "$IMAGE:$VERSION"

                        echo "=== Pushing latest ==="
                        docker push "$IMAGE:latest"

                        echo "=== Logging out of GHCR ==="
                        docker logout ghcr.io

                        echo "=== Docker image publishing completed ==="
                    '''
                }
            }
        }

        stage('Trigger Render Deployment') {
            steps {
                withCredentials([
                    string(
                        credentialsId: 'render-deploy-hook',
                        variable: 'RENDER_DEPLOY_HOOK_URL'
                    )
                ]) {
                    sh '''
                        set -eu
                        set +x

                        echo "=== Triggering Render deployment ==="

                        curl \
                            --fail \
                            --silent \
                            --show-error \
                            --retry 3 \
                            --retry-delay 2 \
                            "$RENDER_DEPLOY_HOOK_URL"

                        echo "=== Render deployment triggered successfully ==="
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Docker images published and Render deployment triggered.'
        }

        failure {
            echo 'FAILED: Check the console log for the failing stage.'
        }

        always {
            echo 'Pipeline execution completed.'
        }
    }
}
