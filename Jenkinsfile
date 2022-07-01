#!/usr/bin/env groovy

// CODE_CHANGES = getGitChanges()
pipeline {
    agent any
    // enviroment { 
    //     VERSION = "1.3.0"
    //     SERVER_CREDENTIAL = credentials('server-credentials')
    // }
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
                    // echo "Building version ${VERSION}"
                }
            }
        }
        stage('test') {
            // when { 
            //     expression { 
            //         BRANCH_NAME == 'dev' || BRANCH_NAME == 'master'
            //     }
            // }
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
                    // echo "Deploying with ${SERVER_CREDENTIAL}"
                    // sh "${SERVER_CREDENTIAL}"
                }
            }
        }        
    }
}
