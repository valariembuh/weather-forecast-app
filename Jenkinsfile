pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "valariembuh/weather-forecast-app"
        KUBECONFIG = "/var/lib/jenkins/.kube/config"
    }

    stages {

        /* =========================
           1. CLONE REPO
        ========================== */
        stage('Clone Repository') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/valariembuh/weather-forecast-app.git'
            }
        }

        /* =========================
           2. BUILD DOCKER IMAGE
        ========================== */
        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:latest ."
                }
            }
        }

        /* =========================
           3. LOGIN TO DOCKERHUB
        ========================== */
        stage('Login to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh '''
                        echo $PASS | docker login -u $USER --password-stdin
                    '''
                }
            }
        }

        /* =========================
           4. PUSH IMAGE TO DOCKERHUB
        ========================== */
        stage('Push to DockerHub') {
            steps {
                script {
                    sh "docker push ${DOCKER_IMAGE}:latest"
                }
            }
        }

        /* =========================
           5. DEPLOY TO KUBERNETES
        ========================== */
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh '''
                        kubectl apply -f k8s/
                        kubectl rollout restart deployment weather-app
                        kubectl get pods
                    '''
                }
            }
        }
    }

    /* =========================
       POST ACTIONS
    ========================== */
    post {
        success {
            echo "✅ Pipeline executed successfully! Weather app deployed."
        }

        failure {
            echo "❌ Pipeline failed. Check logs."
        }
    }
}
