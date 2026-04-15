pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "valariembuh/weather-app:latest"
        KUBE_CONFIG = "/var/jenkins_home/.kube/config"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
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

        stage('Login & Push DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-cred',
                    usernameVariable: 'USER',
                    passwordVariable: 'PASS')]) {

                    sh """
                        echo $PASS | docker login -u $USER --password-stdin
                        docker push ${DOCKER_IMAGE}
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh """
                    export KUBECONFIG=${KUBE_CONFIG}
                    kubectl version --client
                    kubectl apply -f k8s/
                    kubectl get pods
                    kubectl get svc
                """
            }
        }
    }

    post {
        success {
            echo "Pipeline SUCCESS 🚀"
        }
        failure {
            echo "Pipeline FAILED ❌"
        }
    }
}
