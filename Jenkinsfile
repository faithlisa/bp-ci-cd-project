pipeline {
    agent any

    environment {
        IMAGE_NAME = "bp-app"
    }

    stages {

        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/faithlisa/bp-ci-cd-project.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${IMAGE_NAME}")
                }
            }
        }

        stage('Run Tests') {
            steps {
                sh 'docker run --rm ${IMAGE_NAME} pytest'
            }
        }

        stage('Deploy Application') {
            steps {
                sh '''
                docker stop bp_container || true
                docker rm bp_container || true
                docker run -d -p 8000:8000 --name bp_container ${IMAGE_NAME}
                '''
            }
        }
    }
}
