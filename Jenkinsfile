pipeline {
    agent any

    environment {
        IMAGE_NAME = "valariembuh/weather-app"
        IMAGE_TAG  = "latest"
        DOCKERHUB_CREDENTIALS = "dockerhub-creds"
    }

    stages {

        stage('Checkout Code') {
            steps {
                echo "📥 Cloning repository..."
                git branch: 'main',
                    url: 'https://github.com/valariembuh/weather-forecast-app.git'
            }
        }

        stage('Run Tests (optional)') {
            steps {
                echo "🧪 Running basic checks..."
                sh '''
                    if [ -f requirements.txt ]; then
                        echo "Python project detected"
                    fi
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🐳 Building Docker image..."
                sh """
                    docker build -t $IMAGE_NAME:$IMAGE_TAG -f docker/Dockerfile .
                """
            }
        }

        stage('Security & Image Validation') {
            steps {
                echo "🔍 Validating image..."
                sh "docker images | grep weather-app"
            }
        }

        stage('Docker Login') {
            steps {
                echo "🔐 Logging into DockerHub..."
                withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CREDENTIALS}",
                                                  usernameVariable: 'USER',
                                                  passwordVariable: 'PASS')]) {
                    sh '''
                        echo $PASS | docker login -u $USER --password-stdin
                    '''
                }
            }
        }

        stage('Tag & Push Image') {
            steps {
                echo "📤 Pushing image to DockerHub..."
                sh """
                    docker tag $IMAGE_NAME:$IMAGE_TAG $IMAGE_NAME:$IMAGE_TAG
                    docker push $IMAGE_NAME:$IMAGE_TAG
                """
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "☸️ Deploying to Minikube..."

                sh """
                    kubectl apply -f k8s/configmap.yaml
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                """
            }
        }

        stage('Verify Deployment') {
            steps {
                echo "📊 Checking rollout status..."
                sh """
                    kubectl get pods
                    kubectl get svc
                    kubectl rollout status deployment/weather-app
                """
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline SUCCESS - App deployed successfully!"
        }

        failure {
            echo "❌ Pipeline FAILED - check logs"
        }

        always {
            echo "🧹 Cleaning workspace..."
            cleanWs()
        }
    }
}
