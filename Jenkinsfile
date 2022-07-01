#!/usr/bin/env groovy

// CODE_CHANGES = getGitChanges()
pipeline {
    agent none
    stages {
        stage('build') {
            steps {
                // when { 
                //     expression{ 
                //         BRANCH_NAME == 'dev' && CODE_CHANGES=true
                //     }
                // }
                script {
                    echo "Building the application..."
                    echo "we will add a decralative pipeline later"
                }
            }
        }
        stage('test') {
            when { 
                expression { 
                    BRANCH_NAME == 'dev' || BRANCH_NAME == 'master'
                }
            }
            steps {
                script {
                    echo "Testing the application..."
                }
            }
        }
        stage('deploy') {
            steps {
                script {
                    echo "Deploying the application..."
                }
            }
        }
        post { 
            always{ 
                echo "This is always done"
            }
        success{ 
            echo "This build is done"
        }
        failure{ 
            echo "This build failed, why?"
        }
        }
        
    }
}
