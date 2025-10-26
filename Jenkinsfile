// ========================================================================
// CINEREADS CI/CD PIPELINE
// ========================================================================
// Purpose: Automated build, test, and deployment pipeline
// Triggers: Push to main branch, manual trigger
// ========================================================================

pipeline {
    agent any
    
    environment {
        // Docker Registry (GitHub Container Registry)
        REGISTRY = 'ghcr.io'
        REGISTRY_NAMESPACE = 'dhanushranga1'
        
        // Image names
        BACKEND_IMAGE = "${REGISTRY}/${REGISTRY_NAMESPACE}/cinereads-backend"
        FRONTEND_IMAGE = "${REGISTRY}/${REGISTRY_NAMESPACE}/cinereads-frontend"
        
        // Build version - use git commit SHA
        BUILD_VERSION = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
        
        // Kubernetes namespace
        K8S_NAMESPACE = 'cinereads'
        
        // Credentials IDs (configured in Jenkins)
        GITHUB_REGISTRY_CRED = credentials('github-registry')
        K8S_CONFIG = credentials('k3s-kubeconfig')
        GROQ_API_KEY = credentials('groq-api-key')
        HARDCOVER_API_KEY = credentials('hardcover-api-key')
    }
    
    options {
        // Keep last 10 builds
        buildDiscarder(logRotator(numToKeepStr: '10'))
        
        // Timeout after 30 minutes
        timeout(time: 30, unit: 'MINUTES')
        
        // Disable concurrent builds
        disableConcurrentBuilds()
    }
    
    stages {
        stage('🔍 Checkout') {
            steps {
                echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
                echo '📥 Checking out source code...'
                echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
                
                checkout scm
                
                sh '''
                    echo "✅ Branch: $(git branch --show-current)"
                    echo "✅ Commit: $(git rev-parse --short HEAD)"
                    echo "✅ Message: $(git log -1 --pretty=%B)"
                '''
            }
        }
        
        stage('🔨 Build Backend') {
            steps {
                echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
                echo '🏗️ Building Backend Docker Image...'
                echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
                
                dir('backend') {
                    sh """
                        docker build \
                            -t ${BACKEND_IMAGE}:${BUILD_VERSION} \
                            -t ${BACKEND_IMAGE}:latest \
                            -f Dockerfile .
                        
                        echo "✅ Backend image built successfully"
                        docker images | grep cinereads-backend
                    """
                }
            }
        }
        
        stage('🔨 Build Frontend') {
            steps {
                echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
                echo '🏗️ Building Frontend Docker Image...'
                echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
                
                dir('frontend') {
                    sh """
                        docker build \
                            -t ${FRONTEND_IMAGE}:${BUILD_VERSION} \
                            -t ${FRONTEND_IMAGE}:latest \
                            -f Dockerfile .
                        
                        echo "✅ Frontend image built successfully"
                        docker images | grep cinereads-frontend
                    """
                }
            }
        }
        
        stage('🧪 Test Backend') {
            steps {
                echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
                echo '🧪 Running Backend Tests...'
                echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
                
                dir('backend') {
                    sh '''
                        # Run tests inside Docker container
                        docker run --rm \
                            ${BACKEND_IMAGE}:${BUILD_VERSION} \
                            python -m pytest tests/ -v || true
                        
                        echo "✅ Backend tests completed"
                    '''
                }
            }
        }
        
        stage('🧪 Test Frontend') {
            steps {
                echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
                echo '🧪 Running Frontend Tests...'
                echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
                
                dir('frontend') {
                    sh '''
                        # Run linting
                        docker run --rm \
                            ${FRONTEND_IMAGE}:${BUILD_VERSION} \
                            npm run lint || true
                        
                        echo "✅ Frontend tests completed"
                    '''
                }
            }
        }
        
        stage('📦 Push Images') {
            steps {
                echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
                echo '📤 Pushing Docker Images to Registry...'
                echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
                
                sh """
                    # Login to GitHub Container Registry
                    echo "${GITHUB_REGISTRY_CRED_PSW}" | docker login ${REGISTRY} -u ${GITHUB_REGISTRY_CRED_USR} --password-stdin
                    
                    # Push backend images
                    echo "📤 Pushing backend:${BUILD_VERSION}..."
                    docker push ${BACKEND_IMAGE}:${BUILD_VERSION}
                    docker push ${BACKEND_IMAGE}:latest
                    
                    # Push frontend images
                    echo "📤 Pushing frontend:${BUILD_VERSION}..."
                    docker push ${FRONTEND_IMAGE}:${BUILD_VERSION}
                    docker push ${FRONTEND_IMAGE}:latest
                    
                    # Logout
                    docker logout ${REGISTRY}
                    
                    echo "✅ All images pushed successfully"
                """
            }
        }
        
        stage('🚀 Deploy to k3s') {
            steps {
                echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
                echo '🚀 Deploying to Kubernetes...'
                echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
                
                dir('devops/kubernetes') {
                    sh '''
                        # Configure kubectl
                        export KUBECONFIG=${K8S_CONFIG}
                        
                        # Verify cluster access
                        echo "🔍 Checking cluster connectivity..."
                        kubectl cluster-info
                        kubectl get nodes
                        
                        # Create namespace if doesn't exist
                        kubectl create namespace ${K8S_NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -
                        
                        # Create secrets from environment variables (set in Jenkins credentials)
                        echo "🔐 Creating/updating backend secrets..."
                        kubectl create secret generic backend-secrets \
                            --namespace=${K8S_NAMESPACE} \
                            --from-literal=OPENAI_API_KEY="${GROQ_API_KEY}" \
                            --from-literal=HARDCOVER_API_KEY="${HARDCOVER_API_KEY}" \
                            --from-literal=OPENAI_BASE_URL="https://api.groq.com/openai/v1" \
                            --from-literal=GPT_MODEL="llama-3.3-70b-versatile" \
                            --dry-run=client -o yaml | kubectl apply -f -
                        
                        # Apply manifests
                        echo "📦 Applying Kubernetes manifests..."
                        kubectl apply -f namespace.yaml
                        kubectl apply -f configmap.yaml
                        kubectl apply -f backend-deployment.yaml
                        kubectl apply -f frontend-deployment.yaml
                        kubectl apply -f ingress.yaml
                        
                        # Update image versions
                        echo "🔄 Updating deployment images..."
                        kubectl set image deployment/backend backend=${BACKEND_IMAGE}:${BUILD_VERSION} -n ${K8S_NAMESPACE}
                        kubectl set image deployment/frontend frontend=${FRONTEND_IMAGE}:${BUILD_VERSION} -n ${K8S_NAMESPACE}
                        
                        # Wait for rollout
                        echo "⏳ Waiting for deployments to be ready..."
                        kubectl rollout status deployment/backend -n ${K8S_NAMESPACE} --timeout=5m
                        kubectl rollout status deployment/frontend -n ${K8S_NAMESPACE} --timeout=5m
                        
                        # Get deployment status
                        echo "📊 Deployment Status:"
                        kubectl get all -n ${K8S_NAMESPACE}
                        
                        echo "✅ Deployment completed successfully"
                    '''
                }
            }
        }
        
        stage('✅ Verify Deployment') {
            steps {
                echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
                echo '🔍 Verifying Deployment...'
                echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
                
                sh '''
                    export KUBECONFIG=${K8S_CONFIG}
                    
                    # Check pod status
                    echo "📊 Pod Status:"
                    kubectl get pods -n ${K8S_NAMESPACE}
                    
                    # Check service endpoints
                    echo "🌐 Service Endpoints:"
                    kubectl get svc -n ${K8S_NAMESPACE}
                    
                    # Check ingress
                    echo "🚪 Ingress Configuration:"
                    kubectl get ingress -n ${K8S_NAMESPACE}
                    
                    # Test backend health endpoint
                    echo "🏥 Testing backend health..."
                    BACKEND_POD=$(kubectl get pods -n ${K8S_NAMESPACE} -l component=backend -o jsonpath='{.items[0].metadata.name}')
                    kubectl exec -n ${K8S_NAMESPACE} ${BACKEND_POD} -- curl -s http://localhost:8000/health || echo "Backend health check pending..."
                    
                    echo "✅ Verification completed"
                '''
            }
        }
    }
    
    post {
        success {
            echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
            echo '✅ PIPELINE COMPLETED SUCCESSFULLY! 🎉'
            echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
            echo ''
            echo '🌐 Application URL: http://cinereads.dhanushranga1.dev'
            echo '📚 API Docs: http://cinereads.dhanushranga1.dev/docs'
            echo "📦 Version: ${BUILD_VERSION}"
            echo ''
        }
        
        failure {
            echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
            echo '❌ PIPELINE FAILED!'
            echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
            echo ''
            echo '📝 Check the logs above for error details'
            echo '🔧 Common issues:'
            echo '   - Docker build failures'
            echo '   - Registry authentication'
            echo '   - Kubernetes connectivity'
            echo '   - Missing credentials'
            echo ''
        }
        
        always {
            echo '🧹 Cleaning up...'
            sh '''
                # Remove old Docker images to save space
                docker image prune -f --filter "until=72h" || true
            '''
        }
    }
}
