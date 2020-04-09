#!/usr/bin/env groovy

@Library("texas-pipeline@master")
import texas.common.pipeline.Pipeline

Pipeline texasPipeline = new Pipeline()

pipeline {

    agent {
        label 'jenkins-slave'
    }


    environment {
        // The environment that this pipeline will deploy to
        // You can either have two Jenkinsfiles: for non-prod and prod
        // Or, use code logic in a single Jenkinsfile to set this variable to either "live-k8s-prod" or "live-k8s-nonprod"
        // possibly based on which branch you're building (e.g. master goes to prod, everything else to nonprod)
        // or based on a variable passed in from the Jenkins UI
        // It's up to each application how best to manage that, based on its own source control / build practices.
        ACCOUNT_SHORT_NAME='test-k8s'

        // Project specific variables
        JIRA_TICKET_PREFIX='TEX'
        GIT_PROJECT='texas/example-rds-python'

        BUILDS_TO_KEEP=7

        // Slack Configuration
        SLACK_TEAM_DOMAIN='TODO124'
        SLACK_TOKEN_ID='texas-slack-token'
        SLACK_CHANNEL='#jenkins'

        // Docker Configuration
        DOCKER_IMAGE_NAME='texas-example-rds-python'
        TEST_DOCKER_FILE='pipeline-test.dockerfile'
        BUILD_DOCKER_FILE='pipeline-build.dockerfile'
        RUNTIME_DOCKER_FILE='pipeline-runtime.dockerfile'
        TEST_RESULTS_XML='/app/result.xml'

        // AWS Secrets Management Configuration
        SECRET_NAME_PREFIX='texas-example-python-rds'

        // Deployment Configuration
        DEPLOYMENT_FILE='deployment/deploy.sh test'
        SECRET_DEPLOYMENT_KEY_ORDER='DATABASE_URL, DATABASE_ENGINE, DATABASE_PORT, DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD'
        ECR_REPO='texas-example-rds-python'
        NAMESPACE_PREFIX='ddc-example-rds-python'
        POD_NAME='ddc-example-rds-python'
        TIME_TO_LIVE=3

        // Verify and automated testing configuration
        TIME_TO_WAIT_FOR_DNS_SERVICE = 120
        ECR_TEST_REPO='none'
    }

    stages {
        stage('Prepare') {
            steps {
                script {
                    texasPipeline.prepare(this)
                    texasPipeline.sendTexasSlackNotification('STARTED', this)
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    texasPipeline.runUnitTests(this)
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    texasPipeline.buildBaseImage(this)
                }
            }
        }

        stage('Build Runtime') {
            steps {
                script {
                    texasPipeline.buildRuntimeImage(this)
                }
            }
        }

        stage('Push') {
            steps {
                script {
                    texasPipeline.pushImageToContainerRegistry(this)
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    texasPipeline.deploy(this)
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                script {
                    texasPipeline.checkDeployment(this)
                }
            }
        }

        stage('Verify DNS Service') {
            steps {
                script {
                    def serviceAvailable = texasPipeline.checkDnsService(this)

                    if(!serviceAvailable)
                    {
                        error();
                    }
                }
            }
        }
// Additional test options that can be invoked in a pipeline and require the end product to be built and deployed
//    stage('Run Smoke Tests') {
//      steps {
//        script {
//          texasPipeline.runSmokeTests(this)
//        }
//      }
//    }

//    stage('Run Acceptance Tests') {
//      steps {
//        script {
//          texasPipeline.runAcceptanceTests(this)
//        }
//      }
//    }

        stage('Tidy Up') {
            steps {
                script {
                    texasPipeline.tidyUp(this)
                }
            }
        }
    }

    post {
        failure {
            script {
                texasPipeline.emailBuildFailureToCulprits(this)
            }
        }
        cleanup {
            script {
                texasPipeline.clearWorkspace()
            }
        }
    }

// Examples of other post build actions that you can perform, if required.
//  post {
//    always {
//      echo 'Display the int test results in the UI and mark the build as failed if the unit tests were not successful'
//      junit '**/*.xml'
//    }
//    success {
//      echo 'Slack Notification of Success'
//       script {
//        texasPipeline.sendTexasSlackNotification('SUCCESSFUL', this)
//       }
//    }
//    unstable {
//      echo 'Slack Notify of unstable (i.e. some unit tests failed)'
//      script {
//        texasPipeline.sendTexasSlackNotification('UNSTABLE', this)
//      }
//    }
//    failure {
//      echo 'Slack Notify of failures'
//      script {
//        texasPipeline.sendTexasSlackNotification('FAILED', this)
//      }
//    }
//  }
}
