pipeline {
    agent {label 'windows'}

    stages {
        stage('Run Script') {
            steps {
                script {
                    bat '''
                        echo "Hello from the Jenkins pipeline script!"

                        pip install -r "./requirements.txt"

                        python --version

                        python "./main.py"

                    '''
                }
            }
        }
    }
}
