pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "your-dockerhub-username/weather-app"
    }

    stages {

        stage('Clone GitHub Repo') {
            steps {
                git 'https://github.com/your-username/weather-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t $DOCKER_IMAGE ."
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                        sh "echo $PASS | docker login -u $USER --password-stdin"
                        sh "docker push $DOCKER_IMAGE"
                    }
                }
            }
        }
    }
}
