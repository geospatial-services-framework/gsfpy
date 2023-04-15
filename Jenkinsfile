// TODO: update to circleci?
@Library('conan-pipeline') _

pipeline {
    agent {
        docker {
            label rsidocker.getHost('linux-master')
            image rsidocker.imageMap['linux']
        }                            
    }
    triggers {
    }
    parameters {
        choice(name: 'BUILD_TYPE', choices: ['Development', 'Release'], description: 'Release or Development build')
    }
    options {
        timeout(time: 1, unit: 'HOURS')
        timestamps()
    }
    stages {
        stage('build-dev') {
            when { environment name: 'BUILD_TYPE', value: 'Development'}
            steps {
                sh(label: 'install requirements',
                    script: 'pip install -r requirements.txt')
                sh(label: 'Set resource permissions',
                    script: 'chmod -R 755 rsidist/resource/')
                sh(label: 'build wheel',
                    script: 'python setup.py egg_info --tag-build=dev${BUILD_NUMBER} bdist_wheel')
                sh(label: 'deploy',
                    script: 'twine upload dist/* -r rsi')
            }
        }
        stage('build-release') {
            when { environment name: 'BUILD_TYPE', value: 'Release'}
            steps {
                sh(label: 'install requirements',
                    script: 'pip install -r requirements.txt')
                sh(label: 'Set resource permissions',
                    script: 'chmod -R 755 rsidist/resource/')
                sh(label: 'build wheel',
                    script: 'python setup.py bdist_wheel')
                sh(label: 'deploy',
                    script: 'twine upload dist/* -r rsi')
            }
        }
    }
    post {
        always {
            deleteWorkspace()
        }
    }
}