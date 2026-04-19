pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "valariembuh/weather-app:latest"
        K8S_DEPLOYMENT = "weather-app"
        K8S_SERVICE = "weather-app-service"
    }

    stages {

        stage('Checkout') {
            steps {
                // FIX: force correct branch (main)
                git branch: 'main',
                    url: 'https://github.com/valariembuh/weather-forecast-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t weather-app:latest -f docker/Dockerfile ."
            }
        }

        stage('Tag Image') {
            steps {
                sh "docker tag weather-app:latest ${DOCKER_IMAGE}"
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    '''
                }
            }
        }

        stage('Push Image') {
            steps {
                sh "docker push ${DOCKER_IMAGE}"
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl apply -f k8s/configmap.yaml
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                    kubectl apply -f k8s/hpa.yaml
                '''
            }
        }

        stage('Restart Deployment') {
            steps {
                sh "kubectl rollout restart deployment ${K8S_DEPLOYMENT}"
            }
        }
    }

    post {
        success {
            echo "🚀 Deployment successful! Weather app is live on Kubernetes."
        }

        failure {
            echo "❌ Pipeline failed. Check logs."
        }
    }
}
