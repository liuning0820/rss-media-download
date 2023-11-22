pipeline {
    agent {label 'windows'}

    stages {
        stage('Run Script') {
            steps {
                script {
                    sh '''
                        #!/bin/bash
                        echo "Hello from the Jenkins pipeline script!"
                        # Add your other commands here
                        sh ./run.sh
                    '''
                }
            }
        }
    }
}
