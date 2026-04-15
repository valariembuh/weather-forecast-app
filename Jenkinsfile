pipeline {
    agent any

    environment {
        APP_NAME = "weather-app"
        DOCKER_IMAGE = "valariembuh/weather-app:latest"
        KUBECONFIG = "/var/jenkins_home/.kube/config"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Image') {
            steps {
                sh 'docker build -t weather-app:latest -f docker/Dockerfile .'
            }
        }

        stage('Tag Image') {
            steps {
                sh 'docker tag weather-app:latest valariembuh/weather-app:latest'
            }
        }

        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-cred',
                    usernameVariable: 'USER',
                    passwordVariable: 'PASS'
                )]) {
                    sh '''
                        echo $PASS | docker login -u $USER --password-stdin
                        docker push valariembuh/weather-app:latest
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl get nodes
                    kubectl apply -f k8s/ --validate=false
                '''
            }
        }
    }

    post {
        success {
            echo "SUCCESS 🚀"
        }
        failure {
            echo "FAILED ❌"
        }
    }
}
