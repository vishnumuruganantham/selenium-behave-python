// Prerequisites on the Jenkins side (none of this is configured by this
// file - it has to exist in Jenkins before this pipeline can pass):
//
//   1. Python 3 available on the agent (`python` on PATH).
//   2. Google Chrome installed on the agent. Selenium Manager resolves a
//      matching chromedriver automatically (same as it does locally / in
//      GitHub Actions) - it does NOT install Chrome itself. A bare
//      jenkins/jenkins:lts Docker image does not have Chrome; you'd need a
//      custom agent image, or install Chrome on the host if using a native
//      agent.
//   3. The "Allure Jenkins Plugin" installed (Manage Jenkins > Plugins),
//      and an Allure commandline tool configured under Manage Jenkins >
//      Tools (name it "allure" to match the `allure` step below, or adjust
//      the name here).
//   4. A pipeline job pointed at this repo (branch: master), using
//      "Pipeline script from SCM" so Jenkins picks up this file.
//
// Not verified against a real Jenkins instance - written to match
// documented declarative pipeline syntax, needs a first real run to confirm.

pipeline {
    agent any

    options {
        timestamps()
        // Keep the last 10 builds' artifacts/history instead of forever.
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    triggers {
        // No public webhook to reach a locally-run Jenkins, so poll instead.
        // Adjust the schedule once Jenkins can be reached by a GitHub
        // webhook (Settings > Webhooks on the repo), and use that instead.
        pollSCM('H/5 * * * *')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            python3 -m venv .venv
                            . .venv/bin/activate
                            pip install --upgrade pip
                            pip install -r requirements.txt
                        '''
                    } else {
                        bat '''
                            python -m venv .venv
                            call .venv\\Scripts\\activate.bat
                            pip install --upgrade pip
                            pip install -r requirements.txt
                        '''
                    }
                }
            }
        }

        stage('Run tests') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            . .venv/bin/activate
                            python -m behave -D browser=chrome -D headless=true
                        '''
                    } else {
                        bat '''
                            call .venv\\Scripts\\activate.bat
                            python -m behave -D browser=chrome -D headless=true
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            // Requires the Allure Jenkins Plugin + a configured Allure tool.
            allure(
                includeProperties: false,
                results: [[path: 'reports/allure-results']]
            )
            archiveArtifacts(
                artifacts: 'reports/test_run.log, screenshots/**, downloads/**',
                allowEmptyArchive: true
            )
        }
    }
}
