#!/usr/bin/env groovy

// CODE_CHANGES = getGitChanges()
def gv
pipeline {
    agent any
    // enviroment { 
    //     VERSION = "1.3.0"
    //     SERVER_CREDENTIAL = credentials('server-credentials')
    // }
    stages {
        stage('init') { 
            steps{ 
                script {
                    gv = load "script.groovy" 

                }
            }
        }
        stage('build') {
            steps {
                script {
                    gv.buildApp()
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
                    // withCredentials([
                    //         usernamePassword(credentials: 'server-credentials', usernameVariable: USER , passwordVariable: PASSWORD)
                    //     ]) { 
                    //         sh "some script ,"
                        
                    // }
                }
            }
        }        
    }
}
