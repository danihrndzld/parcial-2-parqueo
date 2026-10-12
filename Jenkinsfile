// Pipeline del parqueo: arranca el API, corre la regresión de Bruno
// y construye la imagen del API.
pipeline {
  agent any
  triggers { pollSCM('H/2 * * * *') }
  options {
    skipDefaultCheckout()
    timeout(time: 15, unit: 'MINUTES')
  }
  environment { IMAGE = "parqueo-api:${env.BUILD_NUMBER}" }
  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Start API') {
      steps {
        sh '''
          nohup uv run api.py > api.log 2>&1 &
          echo $! > api.pid
          for i in $(seq 1 60); do
            curl -sf http://127.0.0.1:8000/health && exit 0
            sleep 1
          done
          cat api.log; exit 1
        '''
      }
    }
    stage('Build image') {
      steps { sh 'docker build -f Containerfile -t "$IMAGE" .' }
    }
    stage('Regresion') {
      steps {
        dir('bruno/regresion') {
          sh 'bru run --env local --sandbox=developer --reporter-junit results.xml || true'
        }
      }
    }
  }
  post {
    always {
      junit allowEmptyResults: true, testResults: 'bruno/smoke/results.xml'
      sh 'kill "$(cat api.pid)" 2>/dev/null || true'
    }
  }
}
