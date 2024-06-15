pipeline {
    agent none
  options {
      timeout(time: 1, unit: 'HOURS')
  }
    stages {
        stage('Build') {
            parallel{
                stage('Build:Windows') {
                    agent {
                        label 'windows'
                    }
                    steps {
                        script {
                            bat '''
                                echo "Hello from the Jenkins pipeline script!"
                                python --version
                                pip install -r "./requirements.txt"
                                python "./main.py" urls.txt feeds.txt

                            '''
                        }
                    }
                }
                stage('Build with Container Agent') {
                    agent {
                        // docker { image 'node:16-alpine' }
                        dockerfile true
                    }
                    steps {
                        sh 'node --version'
                        sh 'curl --version'
                    }
                }

                stage('Build:Linux') {
                    agent {label 'linux'}
                    steps {
                        script {
                            sh '''
                                python --version
                                whoami
                                pip install -r "./requirements.txt"
                                export PATH="$PATH:/var/lib/jenkins/.local/bin"
                                python "./main.py" urls_bilibili.txt feeds_bilibili.txt

                            '''
                        }
                    }
                }                
            }
        }

    }
}
