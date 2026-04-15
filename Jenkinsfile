pipeline {
    agent any

    environment {
        IMAGE_NAME = "weather-app"
        DOCKERHUB_USER = "valariembuh"
        IMAGE_TAG = "latest"
        FULL_IMAGE = "${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
    }

    stages {

        stage('Checkout Code') {
            steps {
                // Jenkins automatically checks out code from SCM
                echo 'Code already checked out by Jenkins SCM'
            }
        }

        stage('Verify Files') {
            steps {
                sh 'ls -la'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -f docker/Dockerfile ."
            }
        }

        stage('Tag Image') {
            steps {
                sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${FULL_IMAGE}"
            }
        }

        stage('Push Image to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-cred', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh """
                        echo $PASS | docker login -u $USER --password-stdin
                        docker push ${FULL_IMAGE}
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh "kubectl apply -f k8s/"
            }
        }
    }

    post {
        success {
            echo 'Pipeline executed successfully 🚀'
        }
        failure {
            echo 'Pipeline failed ❌ check logs'
        }
    }
}
