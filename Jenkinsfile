pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "valariembuh/weather-app"
        DOCKER_CREDENTIALS = "dockerhub-creds"
        KUBE_CONFIG = "/var/jenkins_home/.kube/config"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Set Build Tag') {
            steps {
                script {
                    env.IMAGE_TAG = "${BUILD_NUMBER}"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} -f docker/Dockerfile .
                """
            }
        }

        stage('Login to DockerHub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: "${DOCKER_CREDENTIALS}",
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh """
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    """
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                sh """
                docker push ${DOCKER_IMAGE}:${IMAGE_TAG}
                """
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh """
                export KUBECONFIG=${KUBE_CONFIG}

                kubectl apply -f k8s/configmap.yaml
                kubectl apply -f k8s/deployment.yaml
                kubectl apply -f k8s/service.yaml
                kubectl apply -f k8s/hpa.yaml

                kubectl set image deployment/weather-app weather-app=${DOCKER_IMAGE}:${IMAGE_TAG}
                """
            }
        }

        stage('Verify Deployment') {
            steps {
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
            echo "✅ Pipeline SUCCESS: App deployed successfully!"
        }

        failure {
            echo "❌ Pipeline FAILED: Check logs."
        }
    }
}
