pipeline {
    agent any

    environment {
        APP_NAME = "weather-app"
        DOCKER_IMAGE = "valariembuh/weather-app:latest"
        KUBECONFIG = "/var/jenkins_home/.kube/config"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Verify Files') {
            steps {
                sh 'ls -la'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                    docker build -t ${APP_NAME}:latest -f docker/Dockerfile .
                """
            }
        }

        stage('Tag Image') {
            steps {
                sh """
                    docker tag ${APP_NAME}:latest ${DOCKER_IMAGE}
                """
            }
        }

        stage('Push Image to DockerHub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-cred',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh """
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker push ${DOCKER_IMAGE}
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh """
                    echo "Using kubeconfig: $KUBECONFIG"
                    kubectl version --client
                    kubectl get nodes
                    kubectl apply -f k8s/ --validate=false
                """
            }
        }
    }

    post {
        success {
            echo "Pipeline SUCCESS 🚀"
        }
        failure {
            echo "Pipeline FAILED ❌ check logs"
        }
    }
}}
