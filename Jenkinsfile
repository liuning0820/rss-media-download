pipeline {
    agent {label 'windows'}
  options {
      timeout(time: 1, unit: 'HOURS')
  }
    stages {
        stage('Build') {
            parallel{
                stage('Build:Windows') {
                    agent {label 'windows'}
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
                stage('Build:Linux') {
                    agent any
                    steps {
                        script {
                            sh '''
                                python --version
                                sudo pip install -r "./requirements.txt"
                                export PATH="$PATH:/var/lib/jenkins/.local/bin"
                                sudo python "./main.py" urls_bilibili.txt feeds_bilibili.txt

                            '''
                        }
                    }
                }
            }
        }

    }
}
