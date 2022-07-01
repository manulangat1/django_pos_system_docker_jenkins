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
            steps {
                script {
                    gv.deployApp()
                }
            }
        }        
    }
}
