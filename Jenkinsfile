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
            steps {
                script {
                    gv.testApp()
                }
            }
        }
        stage('deploy') {
            input { 
                message "Select the enviroment you want to deploy to:"
                ok "done"
                parameters{
                    choice(name: 'ENV', choices: ['dev', 'staging', 'prod'], description: '')
                }
            }
            steps {
                script {
                    gv.deployApp()
                    echo "Deploying to ${ENV}"
                }
            }
        }        
    }
}
